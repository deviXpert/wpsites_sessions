"""LAUNCH (run only after the user approves the drafts):
  1. copies each redesign draft's Elementor data into the ORIGINAL page (same ID/URL, keeps SEO)
  2. sets Header/Footer display conditions to Entire Site
  3. moves the redesign drafts to Trash
python3 launch.py --dry   (default) shows what would happen;  python3 launch.py --go  does it."""
import json, sys
import wp, build
from push import IDS

GO = '--go' in sys.argv
for key, (_, title, orig, _) in build.PAGES.items():
    draft = wp.req(f"wp/v2/pages/{IDS[key]}?context=edit")
    meta = {k: draft['meta'][k] for k in ('_elementor_data', '_elementor_edit_mode', '_elementor_page_settings') if draft['meta'].get(k)}
    print(f'{key:9} draft {IDS[key]} -> original {orig}', 'COPY' if GO else '(dry)')
    if GO:
        r = wp.req(f'wp/v2/pages/{orig}', 'POST', {'meta': meta, 'template': 'elementor_header_footer'})
        print('   ', 'ok' if 'id' in r else r)
if GO:
    print(wp.ability('elementor/manage-site-parts', {'operations': [
        {'action': 'update', 'post_id': IDS['header'], 'conditions': ['include/general']},
        {'action': 'update', 'post_id': IDS['footer'], 'conditions': ['include/general']}]}))
    for key in build.PAGES:
        print('trash draft', IDS[key], 'ok' if 'id' in wp.req(f"wp/v2/pages/{IDS[key]}", 'DELETE') else 'fail')
    print('Now: Elementor → Tools → Clear Files & Data, then visit every page once.')
