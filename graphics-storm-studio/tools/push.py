"""Push Elementor JSON to the site as DRAFTS (never touches published pages)."""
import json, os
import wp, el
HERE = os.path.dirname(os.path.abspath(__file__))
IDS_F = os.path.join(HERE, 'created.json')
IDS = json.load(open(IDS_F)) if os.path.exists(IDS_F) else {}
def _save(): json.dump(IDS, open(IDS_F, 'w'), indent=1)

def page(key, title, elements, slug=None, template='elementor_header_footer'):
    """Create (once) and update a draft page. Returns post id."""
    el.finalize(elements)
    pid = IDS.get(key)
    if not pid:
        r = wp.ability('elementor/create-page', {'title': title, 'template': template, 'hide_title': True})
        pid = r['post_id'] if 'post_id' in r else r.get('id')
        if not pid: raise SystemExit(r)
        IDS[key] = pid; _save()
    cur = wp.req(f'wp/v2/pages/{pid}?context=edit')
    qa = cur.get('slug', '').startswith('gss-qa-')   # temporarily published for visual QA only
    if cur.get('status') == 'publish' and not qa:
        raise SystemExit(f'{key} ({pid}) is published – refusing to overwrite')
    body = {'title': title, 'status': cur['status'] if qa else 'draft', 'template': template,
            'meta': {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page'}}
    if slug and not qa: body['slug'] = slug
    r = wp.req(f'wp/v2/pages/{pid}', 'POST', body)
    print(key, pid, 'saved' if 'id' in r else r, el.count(elements))
    return pid

def part(key, ptype, title, elements, conditions=None):
    """Theme Builder part (header/footer/section). Created as draft by Elementor's own API."""
    el.finalize(elements)
    pid = IDS.get(key)
    if not pid:
        op = {'action': 'create', 'type': ptype, 'title': title}
        if conditions is not None: op['conditions'] = conditions
        r = wp.ability('elementor/manage-site-parts', {'operations': [op]})
        res = (r.get('results') or [r])[0]
        pid = res.get('post_id') or res.get('id')
        if not pid: raise SystemExit(r)
        IDS[key] = pid; _save()
    r = wp.req(f'wp/v2/elementor_library/{pid}', 'POST', {'title': title,
            'meta': {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder'}})
    print(key, pid, 'saved' if 'id' in r else r, el.count(elements))
    return pid


def live(orig_id, elements):
    """Update a PUBLISHED page in place (post-launch). Saves through Elementor so CSS regenerates."""
    el.finalize(elements)
    r = wp.req(f'wp/v2/pages/{orig_id}', 'POST', {'meta': {'_elementor_data': json.dumps(elements)}})
    s = wp.ability('elementor/update-page-settings', {'post_id': orig_id, 'settings': {'hide_title': 'yes'}})
    if s.get('staged'): wp.ability('elementor/publish-document', {'post_id': orig_id}, 'DELETE')
    print('live', orig_id, 'saved' if 'id' in r else r, el.count(elements))


def published(key, title, slug, elements):
    """Create (once) and update a PUBLISHED new page (e.g. legal pages) and regenerate its CSS."""
    el.finalize(elements)
    pid = IDS.get(key)
    if not pid:
        r = wp.ability('elementor/create-page', {'title': title, 'template': 'elementor_header_footer', 'hide_title': True})
        pid = r.get('post_id') or r.get('id'); IDS[key] = pid; _save()
    r = wp.req(f'wp/v2/pages/{pid}', 'POST', {'title': title, 'slug': slug, 'status': 'publish', 'template': 'elementor_header_footer',
            'meta': {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page'}})
    s = wp.ability('elementor/update-page-settings', {'post_id': pid, 'settings': {'hide_title': 'yes'}})
    if s.get('staged'): wp.ability('elementor/publish-document', {'post_id': pid}, 'DELETE')
    print(key, pid, r.get('status'), r.get('link'), el.count(elements))
    return pid
