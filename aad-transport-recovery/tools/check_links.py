"""Crawl the live AAD site (from home + Yoast sitemaps) and check every link, image, script, stylesheet and #anchor.
Usage: cd tools && python3 check_links.py"""
import re, html, random, urllib.request, urllib.parse, concurrent.futures as cf, collections, ssl
from wp import U
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
HOST = urllib.parse.urlparse(U).netloc
def get(u, body=True):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA, method='GET'), timeout=30)
        return r.status, (r.read().decode('utf-8', 'replace') if body else ''), r.geturl()
    except urllib.error.HTTPError as e: return e.code, '', u
    except Exception as e: return str(e)[:60], '', u
def clean(u): return u.split('#')[0]
seen, pages, queue = set(), {}, [U + '/']
st, sm, _ = get(U + '/sitemap_index.xml')
for loc in re.findall(r'<loc>([^<]+)</loc>', sm):
    for l2 in re.findall(r'<loc>([^<]+)</loc>', get(loc)[1]): queue.append(l2)
while queue:
    u = queue.pop()
    if u in seen or urllib.parse.urlparse(u).netloc != HOST or re.search(r'\.(jpe?g|png|webp|gif|svg|pdf|xml|css|js)$|/wp-(json|admin|content|includes)|/feed/', u): continue
    seen.add(u); code, body, final = get(u + ('&' if '?' in u else '?') + f'nc={random.randint(1, 10**9)}')
    pages[u] = (code, body)
    for h in re.findall(r'<a\b[^>]*href="([^"]+)"', body):
        h = urllib.parse.urljoin(u, html.unescape(h))
        if urllib.parse.urlparse(h).netloc == HOST: queue.append(clean(h))
refs = collections.defaultdict(set); anchors = []
for u, (code, body) in pages.items():
    body = re.sub(r'<script type="application/ld\+json".*?</script>|<script type="speculationrules">.*?</script>', '', body, flags=re.S)
    ids = set(re.findall(r'\bid="([^"]+)"', body))
    for tag, attr in (('a', 'href'), ('img', 'src'), ('link', 'href'), ('script', 'src'), ('iframe', 'src'), ('source', 'srcset')):
        for v in re.findall(rf'<{tag}\b[^>]*\s{attr}="([^"]+)"', body):
            v = html.unescape(v).split(' ')[0]
            if v.startswith('#'):
                if len(v) > 1 and v[1:] not in ids: anchors.append((u, v))
                continue
            if v.startswith(('tel:', 'mailto:', 'javascript:', 'data:')):
                if v.startswith('tel:') and not re.fullmatch(r'tel:\+?[0-9]{10,13}', v): refs['BADTEL:' + v].add(u)
                continue
            full = urllib.parse.urljoin(u, v)
            if 'xmlrpc' in full or 'fonts.gstatic.com' == urllib.parse.urlparse(full).netloc and full.rstrip('/').endswith('gstatic.com'): continue
            refs[clean(full) if tag == 'a' else full].add(u)
print(f'pages crawled: {len(pages)}')
for u, (c, _) in sorted(pages.items()): 
    if c != 200: print('PAGE', c, u)
targets = [t for t in refs if not t.startswith('BADTEL:')]
with cf.ThreadPoolExecutor(12) as ex: res = dict(zip(targets, ex.map(lambda t: get(t, False)[0], targets)))
bad = {t: c for t, c in res.items() if c != 200}
print(f'unique links/assets checked: {len(targets)}  broken: {len(bad)}  bad tel: {sum(1 for t in refs if t.startswith("BADTEL:"))}  missing #anchors: {len(anchors)}')
for t, c in sorted(bad.items(), key=lambda x: str(x[1])): print(' ', c, t, '<- on', len(refs[t]), 'page(s), e.g.', sorted(refs[t])[0])
for t in refs:
    if t.startswith('BADTEL:'): print('  BAD TEL', t[7:], '<- on', sorted(refs[t]))
for u, a in sorted(set(anchors)): print('  MISSING ANCHOR', a, 'on', u)
