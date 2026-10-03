"""Write a service draft's design into the ORIGINAL page (same ID/URL/title/Yoast). Usage: python3 golive.py <pid> [...]"""
import sys, json, wp, build_service as bs, build_pages as bp
st = json.load(open('created.json'))
for a in sys.argv[1:]:
    pid = int(a); key = bs.SVC.get(pid) or bp.PAGES_MAP[pid]; did = st['drafts'][('svc-' if pid in bs.SVC else 'pg-') + key]
    before = wp.req(f'wp/v2/pages/{pid}?context=edit')
    data = wp.req(f'wp/v2/pages/{did}?context=edit')['meta']['_elementor_data']
    r = wp.req(f'wp/v2/pages/{pid}', 'POST', {'template': 'elementor_canvas', 'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': data}})
    after = wp.req(f'wp/v2/pages/{pid}?context=edit')
    same = all(before[k] == after[k] for k in ('slug', 'link', 'status')) and before['title']['raw'] == after['title']['raw']
    print(key, pid, 'written:', after['meta']['_elementor_data'] == data, '| url/slug/title/status unchanged:', same, after['link'])
print('cache', wp.req('elementor/v1/cache', 'DELETE'))
