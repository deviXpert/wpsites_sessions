import re, html, json
from html.parser import HTMLParser

src = open('gdoc.html').read()
css = src[src.find('<style'):src.find('</style>')]
BOLD = set(re.findall(r'\.(c\d+)\{[^}]*font-weight:700', css))

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.blocks = []; s.cur = None; s.lists = []; s.span_bold = []; s.tbl = 0; s.row = -1; s.col = -1
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ('ol', 'ul'): s.lists.append(t)
        if t == 'table': s.tbl += 1; s.row = -1
        if t == 'tr': s.row += 1; s.col = -1
        if t == 'td': s.col += 1
        if t in ('p', 'li', 'h1', 'h2', 'h3', 'h4'):
            s.cur = {'tag': t, 'parts': [], 'list': s.lists[-1] if t == 'li' and s.lists else None}
        if t == 'span' and s.cur is not None:
            s.span_bold.append(bool(set((a.get('class') or '').split()) & BOLD))
    def handle_endtag(s, t):
        if t == 'table': s.tbl = 0
        if t in ('ol', 'ul') and s.lists: s.lists.pop()
        if t == 'span' and s.span_bold: s.span_bold.pop()
        if t in ('p', 'li', 'h1', 'h2', 'h3', 'h4') and s.cur is not None:
            txt = ''.join(x for x, _ in s.cur['parts']).strip()
            boldtxt = ''.join(x for x, b in s.cur['parts'] if b).strip()
            if txt:
                blk = {'tag': s.cur['tag'], 'text': re.sub(r'\s+', ' ', txt), 'bold': bool(boldtxt) and len(boldtxt) >= len(txt) - 2, 'list': s.cur['list']}
                if s.tbl: blk.update(cell=[s.tbl, s.row, s.col])
                s.blocks.append(blk)
            s.cur = None
    def handle_data(s, d):
        if s.cur is not None: s.cur['parts'].append((d, bool(s.span_bold and s.span_bold[-1])))

p = P(); p.feed(src)
B = p.blocks

# split into pages by slug markers
pages, cur = [], None
i = 0
while i < len(B):
    b = B[i]; t = b['text']
    m = re.search(r'(/[a-z0-9-]+-birmingham/|/vehicle-transport-birmingham/)', t)
    if m and re.search(r'slug|url', t, re.I) or (m and i > 0 and re.search(r'slug|url', B[i - 1]['text'], re.I) and len(t) < 60):
        cur = {'slug': m.group(1).strip('/'), 'blocks': []}; pages.append(cur); i += 1; continue
    if cur is not None: cur['blocks'].append(b)
    i += 1

SKIP = re.compile(r'^(Meta Title|Meta Description|Suggested|CTA$|\[.*\]$|Phone:|Email:|Availability:|Available 24/7$|A\.A\.D Transport & Recovery$|Walsall Rd|The existing A\.A\.D website|H1:?$|URL)', re.I)
for pg in pages:
    bl = []; meta = {}
    for k, b in enumerate(pg['blocks']):
        t = b['text']
        if re.match(r'Meta Title:?\s*(.*)', t): meta['title'] = re.sub(r'Meta Title:?\s*', '', t) or (pg['blocks'][k + 1]['text'] if k + 1 < len(pg['blocks']) else '')
        if re.match(r'Meta Description:?\s*(.*)', t): meta['desc'] = re.sub(r'Meta Description:?\s*', '', t) or (pg['blocks'][k + 1]['text'] if k + 1 < len(pg['blocks']) else '')
    started = False
    for b in pg['blocks']:
        t = b['text']
        if b['tag'] == 'h1' or t.startswith('H1:'):
            started = True; t = re.sub(r'^H1:\s*', '', t)
            if t: bl.append({'tag': 'h1', 'text': t, 'bold': True, 'list': None})
            continue
        if not started or SKIP.match(t) or t == meta.get('title') or t == meta.get('desc'): continue
        bl.append(dict(b, text=t))
    pg['blocks'] = bl; pg['meta'] = meta

json.dump(pages, open('doc_pages.json', 'w'), indent=1)
for pg in pages: print(pg['slug'], len(pg['blocks']), pg['meta'].get('title', '')[:50])
