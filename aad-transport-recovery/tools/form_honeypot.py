"""Add Elementor Pro's hidden Honeypot field to every form (pages + templates); Elementor rejects submissions that fill it.
Idempotent. Usage: python3 form_honeypot.py [--apply] [--backup DIR]"""
import sys, os, json, wp
apply = '--apply' in sys.argv
bk = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
def walk(e, n):
    if e.get('widgetType') == 'form':
        ff = e['settings']['form_fields']
        if not any(f.get('field_type') == 'honeypot' for f in ff):
            ff.append({'_id': 'hp' + e['id'][:5], 'field_type': 'honeypot', 'field_label': 'Leave this empty', 'custom_id': 'hp_trap', 'width': '100'}); n[0] += 1
    for c in e.get('elements', []): walk(c, n)
for t in ('pages', 'elementor_library'):
    for x in wp.all(f'wp/v2/{t}?context=edit&status=any'):
        raw = (x.get('meta') or {}).get('_elementor_data') if isinstance(x.get('meta'), dict) else None
        if not raw: continue
        d = json.loads(raw); n = [0]
        for e in d: walk(e, n)
        if not n[0]: continue
        print(t, x['id'], x['slug'], 'forms updated:', n[0])
        if bk: os.makedirs(bk, exist_ok=True); json.dump(x, open(f'{bk}/{t}-{x["id"]}.json', 'w'))
        if apply:
            r = wp.req(f'wp/v2/{t}/{x["id"]}', 'POST', {'meta': {'_elementor_data': json.dumps(d)}})
            if '_err' in r: print('  ERROR', r)
