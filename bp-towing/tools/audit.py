import json, re, html
pages = json.load(open('wp-backup/pages.json'))
lib = {t['id']: t for t in json.load(open('wp-backup/elementor_library.json'))}
media = {m['id']: m for m in json.load(open('wp-backup/media.json'))}
def strip(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))).strip()
TEXTKEYS = ['title', 'editor', 'description_text', 'title_text', 'text', 'button_text', 'tab_title', 'tab_content',
            'heading', 'testimonial_content', 'testimonial_name', 'starting_number', 'ending_number', 'prefix', 'suffix',
            'item_title', 'item_description', 'content', 'alert_title', 'alert_description', 'html', 'shortcode',
            'before_text', 'highlighted_text', 'after_text', 'rotating_text', 'link_text', 'description', 'inner_text']
def alt_of(img):
    if not isinstance(img, dict) or not img.get('url'): return None
    m = media.get(img.get('id'))
    a = (m or {}).get('alt_text') or img.get('alt') or ''
    return {'url': img['url'].split('/uploads/')[-1], 'id': img.get('id'), 'alt': a}
def links(s, out):
    for k, v in (s or {}).items():
        if isinstance(v, dict) and v.get('url') is not None and ('is_external' in v or 'nofollow' in v):
            if v['url']: out.append(v['url'])
        if isinstance(v, str): out += re.findall(r'href="([^"]+)"', v)
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict): links(it, out)
def texts(s, out):
    for k, v in (s or {}).items():
        if k in TEXTKEYS and isinstance(v, str) and strip(v): out.append(strip(v) if k != 'html' else '[HTML] ' + strip(v)[:300])
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict): texts(it, out)
def imgs(s, out):
    for k, v in (s or {}).items():
        if isinstance(v, dict) and 'url' in v and re.search(r'\.(png|jpe?g|webp|gif|svg)$', str(v.get('url')), re.I):
            a = alt_of(v); a and out.append((k, a))
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    if 'url' in it and 'id' in it and re.search(r'\.(png|jpe?g|webp|gif|svg)$', str(it['url']), re.I):
                        a = alt_of(it); a and out.append((k, a))
                    else: imgs(it, out)
def walk(el, depth, out, info):
    s = el.get('settings') or {}
    if not isinstance(s, dict): s = {}
    wt = el.get('widgetType') or el['elType']
    t, l, im = [], [], []
    texts(s, t); links(s, l); imgs(s, im)
    tag = s.get('header_size', '')
    if el['elType'] == 'widget' and wt == 'template':
        tid = int(s.get('template_id') or 0)
        out.append(f"{'  '*depth}- [template #{tid}: {lib.get(tid,{}).get('title',{}).get('raw','?')}]")
        info['templates'].add(tid)
    elif el['elType'] == 'widget' and wt == 'global':
        tid = int(el.get('templateID') or 0); out.append(f"{'  '*depth}- [global widget #{tid}: {lib.get(tid,{}).get('title',{}).get('raw','?')}]"); info['templates'].add(tid)
    elif el['elType'] == 'widget' or t or im:
        line = f"{'  '*depth}- {wt}{'('+tag+')' if tag else ''}"
        if t: line += ': ' + ' | '.join(t)
        out.append(line)
    for u in l: out.append(f"{'  '*depth}    → link: {u}"); info['links'].add(u)
    for k, a in im:
        out.append(f"{'  '*depth}    🖼 {k}: {a['url']} (id {a['id']}) alt={a['alt']!r}")
        info['imgs'].append(a)
    for c in el.get('elements', []): walk(c, depth + 1, out, info)
def audit(data):
    out, info = [], {'links': set(), 'imgs': [], 'templates': set()}
    for i, top in enumerate(data, 1):
        out.append(f"\n### Section {i} ({top['elType']} {top['id']})")
        walk(top, 0, out, info)
    return out, info
if __name__ == '__main__':
    import sys
    report = []
    for p in sorted(pages, key=lambda p: p['menu_order'] or p['id']):
        d = json.loads(p['meta'].get('_elementor_data') or '[]')
        out, info = audit(d)
        y = p.get('yoast_head_json') or {}
        report.append(f"\n\n## {p['title']['raw']} — /{p['slug']}/ (ID {p['id']}, template {p['template'] or 'default'})")
        report.append(f"SEO title: {y.get('title')!r}\nMeta description: {y.get('description')!r}")
        report.append(f"Top-level sections: {len(d)} | images: {len(info['imgs'])} (missing alt: {sum(1 for a in info['imgs'] if not a['alt'])}) | unique links: {len(info['links'])} | embedded templates: {sorted(map(int,info['templates']))}")
        report += out
    report.append('\n\n# Embedded library templates')
    for tid, t in lib.items():
        d = json.loads(t['meta'].get('_elementor_data') or '[]')
        out, info = audit(d)
        report.append(f"\n## Template #{tid} {t['title']['raw']} ({t['meta'].get('_elementor_template_type')})"); report += out
    open('audit.md', 'w').write('\n'.join(report))
