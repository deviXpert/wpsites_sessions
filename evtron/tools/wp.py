"""WordPress REST helper for evtron.co.uk. Credentials come ONLY from environment variables.
Uses EVTRON_WP_USER / EVTRON_WP_APP_PASSWORD / EVTRON_WP_URL if set, else WP_USER / WP_APP_PASSWORD / WP_URL.
Refuses to run unless the URL host is evtron.co.uk (guards against pointing at another client's site)."""
import os, json, base64, urllib.request, urllib.parse, mimetypes

def _env(k): return os.environ.get('EVTRON_' + k) or os.environ.get(k)

U = (_env('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('EVTRON_EXPECTED_HOST', 'evtron.co.uk')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r}.')
_AUTH = 'Basic ' + base64.b64encode(f"{_env('WP_USER')}:{_env('WP_APP_PASSWORD')}".encode()).decode()
H = {'Authorization': _AUTH, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (evtron-build)'}


def req(path, method='GET', data=None, timeout=120):
    r = urllib.request.Request(U + '/wp-json/' + path.lstrip('/'), method=method, headers=H,
                               data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as f:
            b = f.read()
            return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        return {'_err': e.code, 'body': e.read().decode('utf8', 'ignore')[:600]}


def all(path):
    out, p = [], 1
    while True:
        sep = '&' if '?' in path else '?'
        d = req(f"{path}{sep}per_page=100&page={p}")
        if not isinstance(d, list):
            return out if out else d
        out += d
        if len(d) < 100:
            return out
        p += 1


def upload(path, title=None, alt=None):
    """Upload a local file to the media library."""
    name = os.path.basename(path)
    ctype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    h = {'Authorization': _AUTH, 'Content-Type': ctype, 'User-Agent': H['User-Agent'],
         'Content-Disposition': f'attachment; filename="{name}"'}
    r = urllib.request.Request(U + '/wp-json/wp/v2/media', method='POST', headers=h, data=open(path, 'rb').read())
    try:
        with urllib.request.urlopen(r, timeout=180) as f:
            m = json.load(f)
    except urllib.error.HTTPError as e:
        return {'_err': e.code, 'body': e.read().decode('utf8', 'ignore')[:600]}
    upd = {}
    if title: upd['title'] = title
    if alt is not None: upd['alt_text'] = alt
    if upd: req(f"wp/v2/media/{m['id']}", 'POST', upd)
    return m


def eset(key, value):
    """Set an Elementor option via /elementor/v1/settings/<key>."""
    return req(f'elementor/v1/settings/{key}', 'POST', {'value': value})


def ability(name, args=None, method='POST'):
    """Run a WordPress Abilities API ability."""
    return req(f'wp-abilities/v1/abilities/{name}/run', method, {'input': args or {}})
