"""WordPress REST helper for the AAD site. Credentials come ONLY from environment variables.
Prefers AAD_WP_URL / AAD_WP_USER / AAD_WP_APP_PASSWORD, falls back to WP_URL / WP_USER / WP_APP_PASSWORD.
Refuses to run unless the URL host matches AAD_EXPECTED_HOST (default: the AAD staging site)."""
import os, json, base64, urllib.request, urllib.parse
def _env(k): return os.environ.get('AAD_' + k) or os.environ.get(k)
U = (_env('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('AAD_EXPECTED_HOST', 'maroon-raven-160825.hostingersite.com')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r} (set AAD_EXPECTED_HOST if the AAD site moved).')
H = {'Authorization': 'Basic ' + base64.b64encode(f"{_env('WP_USER')}:{_env('WP_APP_PASSWORD')}".encode()).decode(), 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
def req(path, method='GET', data=None):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H, data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r) as f: return json.load(f)
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:300]}
def all(path):
    out = []; p = 1
    while True:
        sep = '&' if '?' in path else '?'
        d = req(f"{path}{sep}per_page=100&page={p}")
        if not isinstance(d, list): return out if out else d
        out += d
        if len(d) < 100: return out
        p += 1
