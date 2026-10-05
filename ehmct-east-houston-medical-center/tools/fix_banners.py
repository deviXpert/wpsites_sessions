"""Mobile only: push inner-page banner content below the header's mobile action row (ends at y=138).
Pattern: page[0] > banner (min_height, centered) > content container whose first widget is 'Hero – Kicker'/'Hero – Title'.
Sets banner flex_justify_content_mobile=flex-start and content padding_mobile top=150 (keeps its bottom/sides).
usage: python3 fix_banners.py [--apply]
"""
import sys, json
from patch import fetch, save, _api

TOP = 150
pages = []
for pg in (1, 2):
    r = _api('GET', f'wp/v2/pages?per_page=100&page={pg}&status=publish&_fields=id,slug')
    if not isinstance(r, list) or not r: break
    pages += r
apply = '--apply' in sys.argv
for p in pages:
    if p['id'] in (32, 994, 997): continue
    doc = fetch(p['id'], backup=apply)
    d = doc['data']
    try:
        banner = d[0]['elements'][0]; content = banner['elements'][0]
        first = content['elements'][0]['settings'].get('_title', '')
    except (IndexError, KeyError):
        print('skip (no pattern)', p['id'], p['slug']); continue
    if first not in ('Hero – Kicker', 'Hero – Title') or 'min_height' not in banner['settings']:
        print('skip (no pattern)', p['id'], p['slug'], first); continue
    cs = content['settings']
    old = cs.get('padding_mobile') or cs.get('padding') or {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
    new = dict(old, top=str(TOP), isLinked=False)
    if str(new.get('bottom', '0')) in ('', '0'): new['bottom'] = '30'
    print(p['id'], p['slug'], 'content pad', old.get('top'), '->', TOP, '| banner justify mobile -> flex-start')
    if apply:
        cs['padding_mobile'] = new
        banner['settings']['flex_justify_content_mobile'] = 'flex-start'
        save(doc)
