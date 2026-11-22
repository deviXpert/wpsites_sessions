"""Publish the Reviews feature – only if Site Reviews holds new reviews for approval.
1) submits a clearly-marked test review through the real form (browser), 2) checks it is NOT public, 3) deletes it,
4) publishes /reviews/, adds the menu item, rebuilds home + footer + reviews, refreshes Yoast.
Run with WP_URL / QW_EXPECTED_HOST set for the target site."""
import json, subprocess, sys, os, wp
D = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(os.path.join(D, 'pages.json'))); RID = P['reviews']
def mcp(a, p): return subprocess.run([D + '/mcp.sh', a, json.dumps(p)], capture_output=True, text=True).stdout
def reviews(st):
    r = wp.req(f'site-reviews/v1/reviews?status={st}&per_page=100')
    return [dict(x, ID=x.get('ID', x.get('id'))) for x in r] if isinstance(r, list) else []
# fresh revision so the preview shows the current layout, then a signed preview URL for the browser test
wp.req(f'wp/v2/pages/{RID}', 'POST', {'excerpt': 'Read and write customer reviews for Quality Waterproofing. '})
url = json.loads(mcp('elementor/create-preview-link', {'post_id': RID}))['data']['url']
open(D + '/.prev_url', 'w').write(url)
before = {r['ID'] for r in reviews('all')}
print(subprocess.run(['node', D + '/review_test.js', D + '/.prev_url'], capture_output=True, text=True).stdout.strip())
new = [r for r in reviews('all') if r['ID'] not in before]
if not new: sys.exit('Test review was not saved – check the form manually. Nothing published.')
public = [r for r in new if r['ID'] in {x['ID'] for x in reviews('approved')}]
for r in new: wp.req(f"site-reviews/v1/reviews/{r['ID']}?force=true", 'DELETE')
print('test review(s) deleted:', [r['ID'] for r in new])
if public: sys.exit('STOP: new reviews are published instantly. Turn on Site Reviews → Settings → General → Require Approval, then run again.')
print('approval required ✓ – publishing')
wp.req(f'wp/v2/pages/{RID}', 'POST', {'status': 'publish'})
items = sorted(wp.req('wp/v2/menu-items?menus=4&per_page=100&context=edit'), key=lambda i: i['menu_order'])
if not any(i['title']['raw'] == 'Reviews' for i in items):
    contact = [i for i in items if i['title']['raw'] == 'Contact'][0]
    for it in items:
        if it['menu_order'] >= contact['menu_order']: wp.req(f"wp/v2/menu-items/{it['id']}", 'POST', {'menu_order': it['menu_order'] + 1})
    wp.req('wp/v2/menu-items', 'POST', {'title': 'Reviews', 'menus': 4, 'parent': 0, 'menu_order': contact['menu_order'], 'status': 'publish', 'type': 'post_type', 'object': 'page', 'object_id': RID})
print(subprocess.run(['python3', D + '/build.py', 'reviews', 'home', 'footer'], capture_output=True, text=True, cwd=D).stdout[-300:])
print(subprocess.run(['python3', D + '/yoast.py'], capture_output=True, text=True, cwd=D).stdout[-200:])
