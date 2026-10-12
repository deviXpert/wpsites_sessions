"""Add a Blog link to the custom header mega-menu (desktop + mobile drawer) and the footer Company links.
Header/footer live in templates 1202/1203 and are also embedded in the Canvas home page 1208. Idempotent.
Usage: python3 add_blog_nav.py [--apply] [--backup DIR]"""
import sys, os, json, wp
BLOG = 'https://aadrecovery.co.uk/blog/'
ABOUT = 'https://aadrecovery.co.uk/about-us/'
DESK = (f'<li><a class="x-mm-link" href="{ABOUT}">About Us</a></li>', f'<li><a class="x-mm-link" href="{BLOG}">Blog</a></li>')
DRAW = (f'<a class="x-dw-main" href="{ABOUT}">About Us</a>', f'<a class="x-dw-main" href="{BLOG}">Blog</a>')
apply = '--apply' in sys.argv
bk = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
def walk(e, n):
    s = e.get('settings', {})
    if e.get('widgetType') == 'html' and BLOG not in s.get('html', ''):
        for old, new in (DESK, DRAW):
            if old in s['html']: s['html'] = s['html'].replace(old, old + new); n[0] += 1
    if e.get('widgetType') == 'icon-list' and any((i.get('link') or {}).get('url') == ABOUT for i in s.get('icon_list', [])) \
            and not any((i.get('link') or {}).get('url') == BLOG for i in s['icon_list']):
        k = [(i.get('link') or {}).get('url') for i in s['icon_list']].index(ABOUT)
        tpl = s['icon_list'][k]
        s['icon_list'].insert(k + 1, {**tpl, '_id': tpl['_id'][:-1] + 'b', 'text': 'Blog', 'link': {**tpl['link'], 'url': BLOG}}); n[0] += 1
    for c in e.get('elements', []): walk(c, n)
for kind, tid in (('elementor_library', 1202), ('elementor_library', 1203), ('pages', 1208)):
    x = wp.req(f'wp/v2/{kind}/{tid}?context=edit')
    d = json.loads(x['meta']['_elementor_data']); n = [0]
    for e in d: walk(e, n)
    print(kind, tid, 'insertions:', n[0])
    if n[0] and bk:
        os.makedirs(bk, exist_ok=True); json.dump(x, open(f'{bk}/{kind}-{tid}.json', 'w'))
    if n[0] and apply:
        r = wp.req(f'wp/v2/{kind}/{tid}', 'POST', {'meta': {'_elementor_data': json.dumps(d)}})
        if '_err' in r: print('  ERROR', r)
