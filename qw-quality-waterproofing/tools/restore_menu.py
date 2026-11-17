"""Restore the real page links in 'QW Main Menu' (saved in menu_backup.json) once the draft pages are published."""
import json, wp
for it in json.load(open('menu_backup.json')):
    if it['type'] == 'post_type':
        d = wp.req(f"wp/v2/menu-items/{it['id']}", 'POST', {'type': 'post_type', 'object': it['object'], 'object_id': it['object_id']})
        print(it['id'], d.get('url', d))
