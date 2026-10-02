"""Rebuild and publish the 13 new service pages (from the Google Doc) to the AAD site as DRAFTS.
Usage:  cd tools && python3 publish_services.py            (rebuild + push drafts)
        python3 publish_services.py --assets                (also push header/footer CSS+JS + home)"""
import json, sys, subprocess, re
subprocess.run([sys.executable, 'build_services.py'], check=True)
subprocess.run([sys.executable, 'build.py'], check=True)
from wp import req
def fix(s): return s.replace('-scaled.jpg', '-scaled.webp').replace('IBM Plex Sans', 'Figtree').replace('"Archivo"', '"Outfit"')
c = json.load(open('created.json'))
if '--assets' in sys.argv:
    b = json.loads(fix(open('built.json').read()))
    print('home', req(f"wp/v2/pages/{c['home']}", 'POST', {'meta': {'_elementor_data': json.dumps(b['home'])}}).get('id'))
    for k in ('header', 'footer'):
        print(k, req(f"wp/v2/elementor_library/{c[k]}", 'POST', {'meta': {'_elementor_data': json.dumps(b[k])}}).get('id'))
bs = json.loads(fix(open('built_services.json').read()))
c.setdefault('svc', {})
for slug, v in bs.items():
    body = {'title': v['title'], 'slug': slug, 'template': 'elementor_header_footer',
            'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': json.dumps(v['data'])}}
    r = req(f"wp/v2/pages/{c['svc'][slug]}", 'POST', body) if c['svc'].get(slug) else req('wp/v2/pages', 'POST', {**body, 'status': 'draft'})  # existing pages keep their status
    c['svc'][slug] = r.get('id'); print(slug, r.get('id'), r.get('_err') or '')
json.dump(c, open('created.json', 'w'), indent=1)
subprocess.run([sys.executable, 'link_pages.py', '--apply'], check=True)  # re-add internal links (rebuilds above drop them)
