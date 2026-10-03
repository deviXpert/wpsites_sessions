"""Push preview pages (password-protected, Canvas template w/ new header+footer embedded). Live pages are untouched.
usage: python3 push_preview.py home [about ...]"""
import json, sys, os, secrets, importlib
import wp
from lib import header, footer, D
st = os.path.join(D, 'preview_state.json')   # git-ignored: holds preview page IDs + password
S = json.load(open(st)) if os.path.exists(st) else {'password': secrets.token_urlsafe(6), 'pages': {}}
for name in sys.argv[1:]:
    mod = importlib.import_module(name)
    body = mod.build()
    data = [header()] + body + [footer()]
    title = getattr(mod, 'TITLE', name.title())
    payload = {'title': f'[Redesign Preview] {title}', 'slug': f'redesign-preview-{name}', 'status': 'publish', 'password': S['password'],
               'template': 'elementor_canvas', 'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': json.dumps(data)}}
    pid = S['pages'].get(name)
    r = wp.req(f'wp/v2/pages/{pid}', 'POST', payload) if pid else wp.req('wp/v2/pages', 'POST', payload)
    if r.get('id'): S['pages'][name] = r['id']
    print(name, r.get('id'), r.get('link'), r.get('_err') or '', (r.get('body') or '')[:300])
json.dump(S, open(st, 'w'), indent=1)
print('cache clear', wp.req('elementor/v1/cache', 'DELETE'))
