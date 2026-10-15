"""Meta descriptions (design/content-seo.md) – Yoast's description field can't be written over the API, so each page gets a tiny
Elementor Custom Code snippet (head, condition: that page only).  If a description is later typed into Yoast, delete the matching
"Busy Bee – Meta: …" snippet (Elementor → Custom Code) so the page doesn't carry two."""
import json, html
import wp
from service_content import PAGES as SVC
from sitemap import SERVICE_PAGES
import build_pages

ids = json.load(open('ids.json'))
DESC = {
    ('home', 'front_page', ''): 'Family-owned auto repair shop in NE Calgary. Certified mechanics for brakes, tires, oil changes and '
                               'diagnostics on all makes. Walk-ins welcome. Call today.',
    ('services', 'page', ids['services']): 'Complete car repair and maintenance in NE Calgary: engine, brakes, tires, alignment, oil '
                                           'changes, batteries, and diagnostics. All makes and models.',
    ('about', 'page', ids['page_about']): build_pages.PAGES['about'][4],
    ('contact', 'page', ids['page_contact']): build_pages.PAGES['contact'][4],
}
for k, *_ in SERVICE_PAGES:
    DESC[(k, 'page', ids['page_' + k])] = SVC[k]['meta']
DESC[('blog', 'archive', '')] = ('Car care tips from Busy Bee Auto Repair in NE Calgary: warning lights, winter tires, oil changes, '
                                 'brakes and the maintenance that keeps your car out of the shop.')
for p_ in wp.get('wp/v2/posts?per_page=100&_fields=id,slug,excerpt'):
    import re
    DESC[('post-' + p_['slug'], 'post', p_['id'])] = re.sub('<[^>]+>', '', p_['excerpt']['rendered']).strip()[:158]

meta_ids = ids.setdefault('meta_snippets', {})
for (key, sub, pid), text in DESC.items():
    body = {'title': f'Busy Bee – Meta: {key}', 'status': 'publish',
            'meta': {'_elementor_location': 'elementor_head', '_elementor_priority': 1,
                     '_elementor_code': f'<meta name="description" content="{html.escape(text, quote=True)}">'}}
    d = wp.post(f'wp/v2/elementor_snippet/{meta_ids[key]}', body) if key in meta_ids else wp.post('wp/v2/elementor_snippet', body)
    meta_ids[key] = d['id']
    cond = ({'type': 'include', 'name': 'archive', 'sub_name': '', 'sub_id': ''} if sub == 'archive' else
            {'type': 'include', 'name': 'singular', 'sub_name': sub, 'sub_id': str(pid) if pid else ''})
    wp.req('PUT', f'elementor/v1/site-editor/templates-conditions/{d["id"]}', {'conditions': [cond]})
    print(key, d['id'], len(text))
json.dump(ids, open('ids.json', 'w'), indent=1)
