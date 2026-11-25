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
    if cur.get('status') == 'publish':
        raise SystemExit(f'{key} ({pid}) is published – refusing to overwrite')
    body = {'title': title, 'status': 'draft', 'template': template,
            'meta': {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page'}}
    if slug: body['slug'] = slug
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
