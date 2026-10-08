"""WordPress REST helper for the Jim Towing site. Credentials come ONLY from environment variables
(JIM_WP_URL / JIM_WP_USER / JIM_WP_APP_PASSWORD preferred, falling back to WP_URL / WP_USER / WP_APP_PASSWORD).
Refuses to run unless the URL host is jimtowing.ca (override with JIM_EXPECTED_HOST if the site moves)."""
import os, json, base64, urllib.request, urllib.parse, mimetypes
def _env(k): return os.environ.get('JIM_' + k) or os.environ.get(k)
U = (_env('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('JIM_EXPECTED_HOST', 'jimtowing.ca')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r}.')
AUTH = 'Basic ' + base64.b64encode(f"{_env('WP_USER')}:{_env('WP_APP_PASSWORD')}".encode()).decode()
H = {'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

def req(path, method='GET', data=None):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H, data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            b = f.read()
            return json.loads(b) if b.strip() else {}
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:600]}

def ability(name, inp):
    """Run a WordPress Abilities API ability (e.g. elementor/manage-site-parts)."""
    return req(f'wp-abilities/v1/abilities/{name}/run', 'POST', {'input': inp})

def upload(path, title, alt):
    name = os.path.basename(path)
    h = {'Authorization': AUTH, 'User-Agent': 'Mozilla/5.0', 'Content-Disposition': f'attachment; filename="{name}"',
         'Content-Type': mimetypes.guess_type(name)[0] or 'image/jpeg'}
    r = urllib.request.Request(U + '/wp-json/wp/v2/media', method='POST', headers=h, data=open(path, 'rb').read())
    with urllib.request.urlopen(r, timeout=300) as f: m = json.load(f)
    req(f"wp/v2/media/{m['id']}", 'POST', {'title': title, 'alt_text': alt})
    return m
