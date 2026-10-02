"""Set Yoast SEO title + meta description on the 13 service pages from service_metas.json (copied from the Google Doc).
Uses Yoast's bulk-editor REST route (Yoast 28+), then re-saves each page so Yoast rebuilds its indexable.
Usage:  cd tools && python3 apply_metas.py"""
import json, time
from wp import req
c = json.load(open('created.json'))['svc']
m = json.load(open('service_metas.json'))
items = [{'id': c[s], 'seo_title': t, 'meta_description': d} for s, (t, d) in m.items()]
for r in req('yoast/v1/bulk_editor/update_search', 'POST', {'items': items}).get('results', []):
    if not r.get('success'): print('FAILED', r)
for s in m:
    p = req(f"wp/v2/pages/{c[s]}?context=edit")
    req(f"wp/v2/pages/{c[s]}", 'POST', {'title': p['title']['raw']})
n = int(time.time())
got = {p['id']: p for p in req(f"yoast/v1/bulk_editor/posts?content_type=page&per_page=100&_={n}&" + '&'.join(f'include[]={i}' for i in c.values()))['posts']}
for s, (t, d) in m.items():
    g = got.get(c[s], {})
    print('OK ' if (g.get('seo_title'), g.get('meta_description')) == (t, d) else 'MISMATCH', c[s], s)
