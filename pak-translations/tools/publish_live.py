"""Rebuild and update LIVE pages in place (data only; title/slug/status untouched). usage: python3 publish_live.py home"""
import json, sys, importlib, wp
from lib import header, footer
LIVE = {'home': (39107, True)}   # name -> (page id, embeds header/footer (Canvas template))
for name in sys.argv[1:]:
    pid, embed = LIVE[name]
    body = importlib.import_module(name).build()
    data = [header()] + body + [footer()] if embed else body
    r = wp.req(f'wp/v2/pages/{pid}', 'POST', {'meta': {'_elementor_data': json.dumps(data)}})
    print(name, r.get('id'), r.get('link'), r.get('_err') or '')
print('cache clear', wp.req('elementor/v1/cache', 'DELETE'))
