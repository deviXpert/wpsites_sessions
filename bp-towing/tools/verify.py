"""Content integrity: every text fragment + link in the original must exist in the rebuild."""
import json, re, html
from lib import tree, LIB
TEXTKEYS = {'title', 'editor', 'description_text', 'title_text', 'text', 'button_text', 'item_title', 'subtitle', 'html', 'shortcode',
            'ending_number', 'suffix', 'field_label', 'placeholder', 'testimonial_content', 'tab_title', 'tab_content'}
def norm(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', str(s)))).strip()
def harvest(els, texts, links, expand=True):
    for e in els:
        s = e.get('settings') or {}
        if not isinstance(s, dict): s = {}
        if e.get('widgetType') == 'template' and expand and s.get('template_id'):
            tid = int(s['template_id'])
            if tid in LIB: harvest(json.loads(LIB[tid]['meta']['_elementor_data']), texts, links)
        if e.get('widgetType') == 'global' and expand:
            tid = int(e.get('templateID') or 0)
            if tid in LIB: harvest(json.loads(LIB[tid]['meta']['_elementor_data']), texts, links)
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in TEXTKEYS and isinstance(v, (str, int)) and norm(v):
                        if k == 'html':
                            texts.update(norm(x) for x in re.findall(r'>([^<>]+)<', str(v)) if norm(x) and not re.search(r'[{};]', x))
                        else: texts.add(norm(v))
                    if k in ('link', 'url') and isinstance(v, dict) and v.get('url'): links.add(v['url'])
                    if isinstance(v, str): links.update(re.findall(r'href="([^"]+)"', v))
                    walk(v)
            elif isinstance(o, list):
                for i in o: walk(i)
        walk(s)
        harvest(e.get('elements', []), texts, links, expand)
def check(orig_els, new_els, extra_templates=None, ignore_links=()):
    ot, ol, nt, nl = set(), set(), set(), set()
    harvest(orig_els, ot, ol); harvest(new_els, nt, nl)
    for t in (extra_templates or []): harvest(t, nt, nl)
    blob = ' || '.join(nt)
    miss_t = sorted(t for t in ot if t not in nt and t not in blob)
    miss_l = sorted(l for l in ol if l not in nl and l not in ignore_links)
    return miss_t, miss_l, sorted(nl - ol)
