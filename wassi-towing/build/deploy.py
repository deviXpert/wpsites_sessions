"""Deploy the Wassi build to WordPress over the REST API (application password).

  python3 deploy.py check            # auth + discovery only
  python3 deploy.py media            # upload icons/logos -> media.json
  python3 deploy.py all              # kit, templates, menu, home page

Needs WP_URL, WP_USER, WP_APP_PASSWORD in the environment.
"""
import base64, json, os, sys, time, urllib.error, urllib.request, mimetypes, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ['WP_URL'].rstrip('/')
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
HANDOFF = os.path.join(HERE, '..', 'handoff', 'Wassi_Towing_Website_Handoff')
STATE_F = os.path.join(HERE, 'state.json')
STATE = json.load(open(STATE_F)) if os.path.exists(STATE_F) else {}

def save_state():
    json.dump(STATE, open(STATE_F, 'w'), indent=1)

def req(method, path, data=None, raw=None, headers=None, tries=5):
    url = path if path.startswith('http') else f'{BASE}/wp-json/{path.lstrip("/")}'
    h = {'Authorization': AUTH, 'Accept': 'application/json'}
    body = None
    if raw is not None:
        body = raw
    elif data is not None:
        body = json.dumps(data).encode()
        h['Content-Type'] = 'application/json'
    h.update(headers or {})
    for i in range(tries):
        r = urllib.request.Request(url, data=body, method=method, headers=h)
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                txt = resp.read().decode()
        except urllib.error.HTTPError as e:
            txt = e.read().decode()
            if txt.lstrip().startswith('{') or txt.lstrip().startswith('['):
                raise RuntimeError(f'{method} {path} -> {e.code}: {txt[:600]}')
        if txt.lstrip()[:1] in '{[':
            return json.loads(txt)
        time.sleep(6 + 4 * i)   # host bot-check page; wait and retry
    raise RuntimeError(f'{method} {path}: non-JSON response after retries')

# ---------------------------------------------------------------- discovery
def check():
    me = req('GET', 'wp/v2/users/me?context=edit')
    print('user:', me['id'], me['name'], me.get('roles'), 'unfiltered_html' in str(me.get('capabilities', {})))
    libs = req('GET', 'wp/v2/elementor_library?per_page=100&context=edit&status=any')
    for t in libs:
        print('lib', t['id'], t['title']['raw'], t['meta'].get('_elementor_template_type'), t['status'])
    print('kit:', find_kit())
    return me

def find_kit():
    libs = req('GET', 'wp/v2/elementor_library?per_page=100&context=edit&status=any')
    kits = [t['id'] for t in libs if t['meta'].get('_elementor_template_type') == 'kit']
    return kits[0] if kits else None

# ---------------------------------------------------------------- media
def upload(path, name=None):
    name = name or os.path.basename(path)
    mt = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    if name.endswith('.svg'):
        mt = 'image/svg+xml'
    data = open(path, 'rb').read()
    return req('POST', 'wp/v2/media', raw=data,
               headers={'Content-Type': mt, 'Content-Disposition': f'attachment; filename="{name}"'})

def media():
    mfile = os.path.join(HERE, 'media.json')
    M = json.load(open(mfile)) if os.path.exists(mfile) else {}
    files = [os.path.join(HERE, 'icons', f) for f in sorted(os.listdir(os.path.join(HERE, 'icons')))]
    files += [os.path.join(HERE, f) for f in ('hero-road.svg', 'symbol-navy.svg')]
    files += [os.path.join(HANDOFF, 'brand', 'logo', 'WassiTowing_horizontal_reversed.svg')]
    for f in files:
        n = os.path.basename(f)
        if n in M:
            continue
        r = upload(f, 'wt-' + n if not n.startswith('Wassi') else n)
        M[n] = {'id': r['id'], 'url': r['source_url']}
        print('uploaded', n, r['id'])
        json.dump(M, open(mfile, 'w'), indent=1)
    return M

# ---------------------------------------------------------------- kit / global settings
def kit():
    kid = find_kit()
    k = req('GET', f'wp/v2/elementor_library/{kid}?context=edit')
    ps = k['meta'].get('_elementor_page_settings') or {}
    if isinstance(ps, str):
        ps = json.loads(ps or '{}')
    col = lambda _id, title, c: {'_id': _id, 'title': title, 'color': c}
    ps['system_colors'] = [col('primary', 'Navy', '#101D32'), col('secondary', 'Orange', '#FF6B00'),
                           col('text', 'Muted', '#5A6577'), col('accent', 'Orange-Text', '#B84D00')]
    ps['custom_colors'] = [col('wtink', 'Ink', '#0B1424'), col('wtnavy2', 'Navy-2', '#1A2B47'),
                           col('wttint', 'Orange-Tint', '#FFF1E6'), col('wtbg', 'BG', '#F5F6F8'),
                           col('wtline', 'Line', '#E2E6EC'), col('wtondark', 'On-Dark', '#C5CEDB'),
                           col('wtwhite', 'White', '#FFFFFF')]
    T = lambda _id, title, fam, w, style=None, size=None: dict(
        {'_id': _id, 'title': title, 'typography_typography': 'custom', 'typography_font_family': fam,
         'typography_font_weight': str(w)},
        **({'typography_font_style': style} if style else {}),
        **({'typography_font_size': {'unit': 'px', 'size': size, 'sizes': []}} if size else {}))
    ps['system_typography'] = [T('primary', 'Display', 'Montserrat', 900, 'italic'),
                               T('secondary', 'Secondary', 'Montserrat', 800),
                               T('text', 'Body', 'Inter', 400, size=16),
                               T('accent', 'Accent', 'Inter', 600)]
    ps.update({
        'container_width': {'unit': 'px', 'size': 1200, 'sizes': []},
        'container_padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
        'space_between_widgets': {'unit': 'px', 'row': '0', 'column': '0', 'size': 0, 'isLinked': True},
        'body_color': '#5A6577', 'body_typography_typography': 'custom', 'body_typography_font_family': 'Inter',
        'body_typography_font_size': {'unit': 'px', 'size': 16, 'sizes': []},
        'link_normal_color': '#101D32', 'link_hover_color': '#B84D00',
        'custom_css': open(os.path.join(HERE, 'global.css')).read(),
        'site_name': 'Wassi Towing Ltd.', 'site_description': 'Towing & Roadside Assistance in Calgary',
    })
    req('POST', f'wp/v2/elementor_library/{kid}', {'meta': {'_elementor_page_settings': ps}})
    print('kit updated', kid)

# ---------------------------------------------------------------- templates & pages
def upsert_template(key, title, ttype, content, conditions=None):
    meta = {'_elementor_edit_mode': 'builder', '_elementor_template_type': ttype,
            '_elementor_data': json.dumps(content)}
    if conditions is not None:
        meta['_elementor_conditions'] = conditions
    body = {'title': title, 'status': 'publish', 'meta': meta}
    if STATE.get(key):
        r = req('POST', f'wp/v2/elementor_library/{STATE[key]}', body)
    else:
        r = req('POST', 'wp/v2/elementor_library', body)
        STATE[key] = r['id']
        save_state()
    print(title, '->', r['id'])
    return r['id']

def ensure_menu():
    menus = req('GET', 'wp/v2/menus?context=edit')
    m = next((x for x in menus if x['slug'] == 'primary'), None)
    if not m:
        m = req('POST', 'wp/v2/menus', {'name': 'Primary', 'slug': 'primary'})
        for i, (t, u) in enumerate([('Home', '/'), ('Services', '/services/'), ('About', '/about/'), ('FAQs', '/faqs/')]):
            req('POST', 'wp/v2/menu-items', {'title': t, 'url': BASE + u, 'menus': m['id'], 'menu_order': i + 1,
                                             'type': 'custom', 'status': 'publish'})
    print('menu', m['id'])

def load_build():
    sys.path.insert(0, HERE)
    import lib, build
    importlib.reload(lib); importlib.reload(build)
    return build

def deploy_all():
    b = load_build()
    kit()
    ensure_menu()
    cb = upsert_template('callband', 'Wassi Call Band', 'container', b.callband())
    upsert_template('header', 'Wassi Header', 'header', b.header(), ['include/general'])
    upsert_template('footer', 'Wassi Footer', 'footer', b.footer(), ['include/general'])
    home = json.loads(json.dumps(b.home()).replace('{{CALLBAND_ID}}', str(cb)))
    hid = STATE.get('home') or 19
    req('POST', f'wp/v2/pages/{hid}', {
        'title': 'Home', 'status': 'publish', 'template': 'elementor_header_footer',
        'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page',
                 '_elementor_data': json.dumps(home),
                 '_elementor_page_settings': {'hide_title': 'yes', 'template': 'elementor_header_footer'}}})
    STATE['home'] = hid; save_state()
    req('POST', 'wp/v2/settings', {'show_on_front': 'page', 'page_on_front': hid,
                                   'title': 'Wassi Towing Ltd.',
                                   'description': 'Towing & Roadside Assistance in Calgary'})
    print('home page', hid)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    {'check': check, 'media': media, 'kit': kit, 'all': deploy_all}[cmd]()
