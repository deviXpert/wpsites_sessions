"""Build a local preview of an Elementor page while the site is in maintenance mode:
rendered page/header/footer HTML from the REST API + the site's real CSS. Output: ../qa/preview-<slug>.html"""
import wp, json, re, sys, urllib.request
pid = int(sys.argv[1]); slug = sys.argv[2]
U = 'https://evtron.co.uk'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf8', 'ignore')
try:
    head = get(U + '/?pv=1')
except urllib.error.HTTPError as e:
    head = e.read().decode('utf8', 'ignore')
links = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]*>', head) + re.findall(r'<style[^>]*>.*?</style>', head, re.S)
links = [l for l in links if 'post-45' not in l]
def rendered(kind, i):
    d = wp.req(f'wp/v2/{kind}/{i}')
    return d['content']['rendered']
body = []
for kind, i in [('pages', pid)]:
    body.append(rendered(kind, i))
    links.append(f'<link rel="stylesheet" href="{U}/wp-content/uploads/elementor/css/post-{i}.css">')
extra = ''.join(re.findall(r'<style[^>]*>.*?</style>', ''.join(body), re.S))
html = '<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' + ''.join(links) + '</head><body class="elementor-default">' + ''.join(body) + '</body></html>'
open(f'../qa/preview-{slug}.html', 'w').write(html)
print('ok', len(html))
