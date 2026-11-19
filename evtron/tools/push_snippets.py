"""Push design/custom-code/*.html into their Elementor Custom Code snippets (code only; location/conditions unchanged).
Run: EVTRON_WP_USER=<admin login> python3 push_snippets.py [01 03 05 ...]"""
import json
import sys

import wp

MAP = {'01': (44, '01-critical-head.html'), '02': (99, '02-home-interactions.html'), '03': (112, '03-motion.html'),
       '05': (145, '05-v2-glass.html'), '06': (186, '06-v3-simple.html'),
       '07': (json.load(open('created.json'))['snippet_product'], '07-product.html'),
       '08': (json.load(open('created.json'))['snippet_woo'], '08-woo.html')}

for key in (sys.argv[1:] or MAP):
    sid, name = MAP[key]
    code = open(f'../design/custom-code/{name}').read()
    r = wp.req(f'wp/v2/elementor_snippet/{sid}', 'POST', {'meta': {'_elementor_code': code}})
    ok = r.get('id') == sid and r.get('meta', {}).get('_elementor_code') == code
    print(key, sid, 'ok' if ok else r)
wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
