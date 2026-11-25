"""Turn a client Google Doc (File → Download → HTML export) into a service_content override dict.

Doc layout the client uses (Nov 2026 service-page docs):
  Meta title: / Meta description:   (heading or bullet, value on the next line)
  H1 page title, next line = subtitle, then intro paragraphs
  H2 sections; H3 sub-items inside a section (≥2 H3s → card grid, numbered when the doc numbers them)
  "Book …"/"Visit …" H2 → yellow callout;  "Frequently Asked Questions …" H2 → FAQ accordion (H3 = question)
Copy is kept word for word: bold runs → <strong>, doc hyperlinks → relative site links, bullets → <ul>/<ol>.
Used by docs_copy2.py (cached exports live in docs/*.html so builds are reproducible offline)."""
import html
import re
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse

SITE = 'busybeeautorepair.ca'


def clean_href(h):
    u = urlparse(h)
    if u.netloc.endswith('google.com') and u.path == '/url':
        h = parse_qs(u.query).get('q', [h])[0]
        u = urlparse(h)
    if u.netloc.endswith(SITE):
        return u.path or '/'
    return h


class _P(HTMLParser):
    BLOCK = {'h1', 'h2', 'h3', 'h4', 'p', 'li'}

    def __init__(self, bold, ital):
        super().__init__(convert_charrefs=True)
        self.bold, self.ital = bold, ital
        self.blocks = []          # (tag, list_kind or None, html, plain)
        self.cur = None
        self.lists = []
        self.spans = []
        self.href = None
        self.in_style = False
        self.table = None         # list of rows (list of cell-html lists) while inside a <table>

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'style':
            self.in_style = True
        elif tag in ('ul', 'ol'):
            self.lists.append(tag)
        elif tag == 'table':
            self.table = []
        elif tag == 'tr' and self.table is not None:
            self.table.append([])
        elif tag == 'td' and self.table is not None:
            self.table[-1].append([])
        elif tag in self.BLOCK:
            self.cur = [tag, self.lists[-1] if (tag == 'li' and self.lists) else None, [], []]
        elif tag == 'span' and self.cur is not None:
            cls = set((a.get('class') or '').split())
            b, i = bool(cls & self.bold), bool(cls & self.ital)
            self.spans.append((b, i))
            if b:
                self.cur[2].append('<strong>')
            if i:
                self.cur[2].append('<em>')
        elif tag == 'a' and self.cur is not None and a.get('href'):
            self.href = clean_href(a['href'])
            self.cur[2].append(f'<a href="{html.escape(self.href, quote=True)}">')
        elif tag == 'br' and self.cur is not None:
            self.cur[2].append('<br>')

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        elif tag in ('ul', 'ol'):
            if self.lists:
                self.lists.pop()
        elif tag == 'table' and self.table is not None:
            rows, self.table = self.table, None
            head = ''.join(f'<th>{"<br>".join(c)}</th>' for c in rows[0])
            body = ''.join('<tr>' + ''.join(f'<td>{"<br>".join(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
            txt = ' '.join(' '.join(c) for r in rows for c in r)
            self.blocks.append(('table', None, f'<div class="bb-table"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>',
                                re.sub(r'<[^>]+>', ' ', txt)))
        elif tag == 'span' and self.cur is not None and self.spans:
            b, i = self.spans.pop()
            if i:
                self.cur[2].append('</em>')
            if b:
                self.cur[2].append('</strong>')
        elif tag == 'a' and self.cur is not None and self.href:
            self.cur[2].append('</a>')
            self.href = None
        elif tag in self.BLOCK and self.cur is not None:
            t, lk, h, plain = self.cur
            body = tidy(''.join(h))
            txt = re.sub(r'\s+', ' ', ''.join(plain)).strip()
            if txt and self.table is not None and self.table and self.table[-1]:
                self.table[-1][-1].append(body)
            elif txt:
                self.blocks.append((t, lk, body, txt))
            self.cur = None

    def handle_data(self, d):
        if self.in_style or self.cur is None:
            return
        self.cur[2].append(html.escape(d, quote=False))
        self.cur[3].append(d)


def tidy(h):
    h = h.replace('\xa0', ' ')
    for t in ('strong', 'em'):
        h = re.sub(rf'</{t}>(\s*)<{t}>', r'\1', h)
        h = re.sub(rf'<{t}>(\s*)</{t}>', r'\1', h)
    h = re.sub(r'<a href="[^"]*">(\s*)</a>', r'\1', h)
    for t in ('strong', 'em'):  # move edge whitespace out of inline tags
        h = re.sub(rf'<{t}>(\s+)', r'\1<' + t + '>', h)
        h = re.sub(rf'(\s+)</{t}>', '</' + t + r'>\1', h)
    h = re.sub(r'\s+', ' ', h).strip()
    h = re.sub(r'<strong>([^<]*)</strong>$', lambda m: m.group(0), h)
    return h.replace(' ,', ',').replace(' .', '.')


def blocks(raw):
    css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', raw, re.S))
    bold = set(re.findall(r'\.(c\d+)\{[^}]*font-weight:700', css))
    ital = set(re.findall(r'\.(c\d+)\{[^}]*font-style:italic', css))
    p = _P(bold, ital)
    p.feed(raw)
    return p.blocks


def strip_num(t):
    return re.sub(r'^\d+[.)]\s*', '', t).strip()


def is_num(t):
    return bool(re.match(r'^\d+[.)]\s', t))


def to_html(bl):
    """Blocks (p / li) → HTML with lists grouped.  A paragraph that is all bold reads as a sub-heading."""
    out, lst = [], None
    for t, lk, h, txt in bl:
        if t == 'li':
            if lst != lk:
                if lst:
                    out.append(f'</{lst}>')
                out.append(f'<{lk}>')
                lst = lk
            out.append(f'<li>{h}</li>')
            continue
        if lst:
            out.append(f'</{lst}>')
            lst = None
        if t in ('h3', 'h4'):
            out.append(f'<h3>{h}</h3>')
        elif t == 'table':
            out.append(h)
        else:
            out.append(f'<p>{h}</p>')
    if lst:
        out.append(f'</{lst}>')
    return ''.join(out)


def strip_tags(h):
    return re.sub(r'<[^>]+>', '', h)


def parse(raw, lead_head, photo=None):
    bl = blocks(raw)
    d, i = {}, 0
    # --- meta lines
    while i < len(bl):
        t, lk, h, txt = bl[i]
        low = txt.lower().rstrip(':').strip()
        if low in ('meta title', 'meta description'):
            d['seo_title' if 'title' in low else 'meta'] = bl[i + 1][3]
            i += 2
        elif low.startswith('url -') or low.startswith('url:'):
            i += 1
        elif t == 'h1':
            break
        else:
            i += 1
    title = bl[i][3]
    i += 1
    sub = bl[i][3]
    i += 1
    head = title.replace(' Calgary', '').strip()
    d['h1'] = f'{html.escape(head)} <em>Calgary</em><span class="bb-h1-sub">{html.escape(sub)}</span>'
    d['focus'] = title.lower()
    intro = []
    while i < len(bl) and bl[i][0] != 'h2':
        intro.append(bl[i])
        i += 1
    d['intro'] = strip_tags(intro[0][2])
    sections = []
    if intro[1:]:
        sections.append(('rich', lead_head, to_html(intro[1:]), photo))
    # --- H2 sections
    groups = []
    while i < len(bl):
        t, lk, h, txt = bl[i]
        if t == 'h2':
            groups.append([txt, []])
        elif groups:
            groups[-1][1].append(bl[i])
        i += 1
    faqs = []
    for head2, body in groups:
        low = head2.lower()
        if low.startswith('frequently asked'):
            q = None
            for b in body:
                if b[0] in ('h3', 'h4'):
                    q = [strip_num(b[3]), []]
                    faqs.append(q)
                elif q:
                    q[1].append(b)
            continue
        h3 = [k for k, b in enumerate(body) if b[0] in ('h3', 'h4')]
        if low.startswith(('book ', 'visit ')):
            sections.append(('callout', head2, to_html(body)))
        elif len(h3) >= 2:
            pre = to_html(body[:h3[0]])
            cards, num = [], all(is_num(body[k][3]) for k in h3)
            for n, k in enumerate(h3):
                end = h3[n + 1] if n + 1 < len(h3) else len(body)
                cards.append((strip_num(body[k][3]), to_html(body[k + 1:end])))
            cols = 2 if len(cards) in (2, 4) else 3
            sections.append(('cards', head2, pre, cards, num, None, cols))
        else:
            sections.append(('rich', head2, to_html(body)))
    d['sections'] = sections
    d['faqs'] = [(q, faq_html(b)) for q, b in faqs]
    return d


def faq_html(bl):
    """Accordion answers are wrapped in <p>…</p> by svc.faq; multi-block answers are passed as full HTML."""
    if len(bl) == 1 and bl[0][0] == 'p':
        return bl[0][2]
    return to_html(bl)
