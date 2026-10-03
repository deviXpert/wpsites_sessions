"""Crawl the live site's pages and check every link (internal, external, #anchors)."""
import re, urllib.request, urllib.parse, html, ssl
from concurrent.futures import ThreadPoolExecutor
U = 'https://pak-translations.com'
PAGES = ['/', '/about-us/', '/services/', '/languages/', '/sample/', '/career/', '/contact-us/', '/your-order/']
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r: return r.status, r.read().decode('utf-8', 'ignore'), r.geturl()
    except urllib.error.HTTPError as e: return e.code, '', u
    except Exception as e: return str(e)[:60], '', u
src, ids, links = {}, {}, {}
for p in PAGES:
    st, body, _ = get(U + p); src[p] = body
    ids[p] = set(re.findall(r'\sid="([^"]+)"', body))
    b = body[body.find('<body'):]
    for h in re.findall(r'<a\s[^>]*href="([^"]+)"', b):
        h = html.unescape(h)
        if h.startswith(('mailto:', 'tel:', 'javascript:')) or h == '#': continue
        links.setdefault(h, set()).add(p)
print('pages:', {p: len(src[p]) > 1000 for p in PAGES}, '| unique links:', len(links))
def check(h):
    pages = links[h]
    if h.startswith('#'):
        return h, all(h[1:] in ids[p] for p in pages), 'anchor', pages
    full = urllib.parse.urljoin(U + '/', h); base, _, frag = full.partition('#')
    st, body, final = get(base)
    ok = isinstance(st, int) and st < 400
    if ok and frag: ok = f'id="{frag}"' in body; st = f'{st} #{frag} ' + ('found' if ok else 'MISSING')
    return h, ok, st, pages
bad = []
with ThreadPoolExecutor(8) as ex:
    for h, ok, st, pages in ex.map(check, sorted(links)):
        print(('OK  ' if ok else 'FAIL'), st, h, '' if ok else sorted(pages))
        if not ok: bad.append(h)
print('\nBROKEN:', bad)
