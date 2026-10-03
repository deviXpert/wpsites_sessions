import json, sys, re
pages = {p['id']: p for p in json.load(open('wp-backup/pages.json'))}
def short(v): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', str(v)))[:70]
def walk(e, d=0):
    s = e.get('settings') or {}
    if not isinstance(s, dict): s = {}
    keys = [k for k in ('title', 'editor', 'text', 'title_text', 'button_text', 'header_size', '_css_classes', 'css_classes', 'html', 'shortcode', 'form_name') if s.get(k)]
    print('  ' * d + f"{e['id']} {e.get('widgetType') or e['elType']} " + ' '.join(f"{k}={short(s[k])!r}" for k in keys))
    for c in e.get('elements', []): walk(c, d + 1)
for e in json.loads(pages[int(sys.argv[1])]['meta']['_elementor_data']): walk(e)
