"""Build + push the Jim Towing redesign as DRAFTS (live pages untouched).
Usage: python3 publish.py [page ...]    (no args = everything; names: header footer menu home <service-slug> about services areas pricing contact)
IDs are recorded in created.json. Header/footer site parts are scoped (conditions) to the draft pages only until go-live."""
import json, sys, os, importlib
from wp import req, ability
import lib
C_PATH = os.path.join(lib.D, 'created.json')
c = json.load(open(C_PATH)) if os.path.exists(C_PATH) else {}
def save(): json.dump(c, open(C_PATH, 'w'), indent=1)
want = set(sys.argv[1:])
def on(n): return not want or n in want

def push_page(key, title, data, slug, parent=0, seo=None):
    body = {'title': title, 'status': 'draft', 'template': 'elementor_header_footer', 'parent': parent,
            'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': json.dumps(data),
                     '_elementor_page_settings': {'hide_title': 'yes'}}}
    if slug: body['slug'] = slug
    import time; body['content'] = f'<!-- jim build {int(time.time())} -->'  # forces a new revision so preview links show the latest build
    pid = c.setdefault('pages', {}).get(key)
    if pid:  # existing (possibly live) page: only update the build, never title/slug/status/parent
        for k in ('title', 'status', 'parent', 'slug'): body.pop(k, None)
    r = req(f'wp/v2/pages/{pid}', 'POST', body) if pid else req('wp/v2/pages', 'POST', body)
    if '_err' in r: print('ERR', key, r); return
    c['pages'][key] = r['id']; save(); print('page', key, r['id'], r['status'])
    if seo: c.setdefault('seo', {})[key] = seo; save()

def ensure_menu():
    if c.get('menu'): return c['menu']
    m = req('wp/v2/menus', 'POST', {'name': 'Jim Main Menu', 'slug': 'jim-main-menu'})
    if '_err' in m: print('menu err', m); return None
    mid = m['id']; o = 0
    def item(t, u, parent=0):
        nonlocal o; o += 1
        r = req('wp/v2/menu-items', 'POST', {'title': t, 'url': u, 'menus': mid, 'parent': parent, 'menu_order': o, 'type': 'custom', 'status': 'publish'})
        return r.get('id')
    item('Home', lib.PAGES['home'])
    sv = item('Services', lib.PAGES['services'])
    for s, t, *_ in lib.SVC: item(t, lib.surl(s), sv)
    item('Service Areas', lib.PAGES['areas']); item('Pricing', lib.PAGES['pricing']); item('About', lib.PAGES['about']); item('Contact', lib.PAGES['contact'])
    c['menu'] = mid; c['menu_slug'] = m.get('slug', 'jim-main-menu'); save(); print('menu', mid)
    return mid

def site_part(kind, data):
    pid = c.get(kind)
    if not pid:
        r = ability('elementor/manage-site-parts', {'operations': [{'action': 'create', 'type': kind, 'title': f'Jim {kind.title()} (redesign)'}]})
        pid = r['results'][0]['id']; c[kind] = pid; save()
    r = req(f'wp/v2/elementor_library/{pid}', 'POST', {'status': 'publish', 'meta': {'_elementor_data': json.dumps(data), '_elementor_edit_mode': 'builder'}})
    print(kind, pid, r.get('status'), r.get('_err') or '')

def scope_parts():
    """Show the new header/footer only on the redesign drafts (live pages keep their current look)."""
    conds = [f'include/singular/page/{i}' for i in c.get('pages', {}).values()]
    if c.get('live'): conds = ['include/general']
    ops = [{'action': 'update', 'post_id': c[k], 'conditions': conds} for k in ('header', 'footer') if c.get(k)]
    if ops: print('conditions', ability('elementor/manage-site-parts', {'operations': ops}).get('status'), len(conds))

if __name__ == '__main__':
    if on('menu') or on('header'): ensure_menu()
    if on('header'): site_part('header', lib.header(c.get('menu_slug', 'jim-main-menu')))
    if on('footer'): site_part('footer', lib.footer())
    import p_home
    if on('home'): push_page('home', 'Home (redesign)', p_home.build(), 'home-redesign', seo=('Towing Calgary | 24/7 Tow Truck & Roadside Assistance | Jim Towing', 'Need towing in Calgary? Jim Towing provides 24/7 emergency towing, flatbed towing, roadside assistance, long-distance transport, battery jump-starts and fuel delivery.'))
    if os.path.exists(os.path.join(lib.D, 'p_services.py')):
        import p_services
        for slug, title, data, seo in p_services.build_all():
            if on(slug): push_page(slug, title, data, slug, parent=161, seo=seo)
    if os.path.exists(os.path.join(lib.D, 'p_pages.py')):
        import p_pages
        for key, title, data, seo in p_pages.build_all():
            if on(key): push_page(key, title, data, key + '-redesign', seo=seo)
    scope_parts()
    req('elementor/v1/cache', 'DELETE')
