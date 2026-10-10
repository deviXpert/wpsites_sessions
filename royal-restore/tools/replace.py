"""Replace 'Rapid Restore' brand text with 'Royal Restore' in all REST-reachable content (uses backup/*.json as source)."""
import json, re, sys
from wp import req
PAIRS = [('Rapid Restore', 'Royal Restore'), ('RAPID RESTORE', 'ROYAL RESTORE'), ('rapid restore', 'royal restore')]
def fix(s):
    for a, b in PAIRS: s = s.replace(a, b)
    return s
DRY = '--apply' not in sys.argv
types = {'page': 'pages', 'post': 'posts', 'elementor_library': 'elementor_library', 'wp_block': 'blocks', 'wp_template': 'templates', 'wp_template_part': 'template-parts', 'elementskit_content': 'elementskit_content', 'astra-advanced-hook': 'astra-advanced-hook', 'nav_menu_item': 'menu-items'}
for t, rb in types.items():
    for it in json.load(open(f'backup/{t}.json')):
        body = {}
        for k in ('title', 'content', 'excerpt'):
            v = it.get(k, {}); raw = v.get('raw') if isinstance(v, dict) else None
            if raw and fix(raw) != raw: body[k] = fix(raw)
        ed = (it.get('meta') or {}).get('_elementor_data')
        if isinstance(ed, str) and fix(ed) != ed: body['meta'] = {'_elementor_data': fix(ed)}
        if not body: continue
        print(t, it['id'], it.get('slug'), list(body), end=' ')
        if DRY: print('(dry)'); continue
        r = req(f'wp/v2/{rb}/{it["id"]}', 'POST', body); print(r.get('id'), r.get('_err', ''), r.get('body', '')[:150])
