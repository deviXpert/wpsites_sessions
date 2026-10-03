"""Push design-system snippet, header/footer site parts, shared templates and page drafts. State in created.json."""
import json, os, sys, wp, mcp
STATE = 'created.json'
st = json.load(open(STATE)) if os.path.exists(STATE) else {'drafts': {}, 'templates': {}}
def save(): json.dump(st, open(STATE, 'w'), indent=1)
def ability(name, params):
    r = mcp.call('mcp-adapter-execute-ability', {'ability_name': name, 'parameters': params})
    t = r.get('result', {}).get('content', [{}])[0].get('text', '') if 'result' in r else json.dumps(r)
    try: return json.loads(t)
    except Exception: return {'raw': t}
mcp.init()

def lib_template(key, title, data, ttype='container'):
    body = {'title': title, 'status': 'publish', 'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': ttype, '_elementor_data': json.dumps(data)}}
    if key in st['templates']: r = wp.req(f"wp/v2/elementor_library/{st['templates'][key]}", 'POST', {'meta': body['meta']})
    else:
        r = wp.req('wp/v2/elementor_library', 'POST', body); st['templates'][key] = r['id']; save()
    assert 'id' in r, r
    return r['id']

def draft_page(key, title, data, template='elementor_header_footer'):
    meta = {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': json.dumps(data)}
    if key in st['drafts']: r = wp.req(f"wp/v2/pages/{st['drafts'][key]}", 'POST', {'meta': meta, 'template': template})
    else:
        r = wp.req('wp/v2/pages', 'POST', {'title': title, 'status': 'draft', 'template': template, 'meta': meta})
        st['drafts'][key] = r['id']; save()
    assert 'id' in r, r
    return r['id']

def conditions():
    return [f'include/singular/page/{i}' for i in st['drafts'].values()] + st.get('extra_conditions', [])

def site_part(key, ptype, title, data=None, code=None, location='elementor_head'):
    if key not in st['templates']:
        r = ability('elementor/manage-site-parts', {'operations': [{'action': 'create', 'type': ptype, 'title': title, 'conditions': conditions()}]})
        pid = r.get('data', r).get('results', [{}])[0].get('id') if isinstance(r.get('data', r), dict) else None
        if not pid: print(json.dumps(r)[:800]); raise SystemExit('site part create failed')
        st['templates'][key] = pid; save()
    pid = st['templates'][key]
    ability('elementor/manage-site-parts', {'operations': [{'action': 'update', 'post_id': pid, 'conditions': conditions()}]})
    if code is not None:
        r = wp.req(f'wp/v2/elementor_snippet/{pid}', 'POST', {'meta': {'_elementor_code': code, '_elementor_location': location, '_elementor_priority': 5}})
    else:
        r = wp.req(f'wp/v2/elementor_library/{pid}', 'POST', {'meta': {'_elementor_data': json.dumps(data)}})
    assert 'id' in r, r
    print(key, pid, ability('elementor/publish-document', {'post_id': pid}).get('data', {}).get('status', ''))
    return pid

def snippet_code():
    css = open('ds.css').read(); js = open('ds.js').read()
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Manrope:wght@400..800&display=swap">'
            f'<style id="bp-ds">{css}</style><script id="bp-ds-js">{js}</script>')

def assets():
    import build_hf
    lib_template('hdr', 'BP Redesign — Header', build_hf.header())
    lib_template('ftr', 'BP Redesign — Footer', build_hf.footer())

def page(sections):
    """canvas page = header template + sections + footer template"""
    import lib
    wrap = lambda tid, cls: {'id': lib.rid(), 'elType': 'container', 'isInner': False, 'settings': {'content_width': 'full', 'css_classes': cls}, 'elements': [lib.W('template', '', template_id=tid)]}
    return [wrap(st['templates']['hdr'], 'bp bp-hdr-wrap')] + sections + [wrap(st['templates']['ftr'], 'bp bp-ftr-wrap')]

def clear_cache(): print('cache', wp.req('elementor/v1/cache', 'DELETE'))

if __name__ == '__main__':
    what = sys.argv[1:]
    if 'assets' in what or 'home' in what: assets()
    if 'home' in what:
        import build_home as bh
        bh.STATS_ID = lib_template('stats', 'BP Redesign — Stats', bh.stats_template())
        pid = draft_page('home', 'Home — Redesign Draft', page(bh.build()), template='elementor_canvas')
        print('home draft', pid)
    clear_cache()
