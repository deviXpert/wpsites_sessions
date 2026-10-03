"""WordPress REST helper for BP Towing (bptowingservice.ca). Credentials come ONLY from env vars
WP_URL / WP_USER / WP_APP_PASSWORD. Refuses to run unless host is bptowingservice.ca."""
import os, json, base64, urllib.request, urllib.parse
U = (os.environ.get('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('BP_EXPECTED_HOST', 'bptowingservice.ca')
if urllib.parse.urlparse(U).netloc.removeprefix('www.') != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r}')
_pw = os.environ.get('WP_APP_PASS') or os.environ.get('WP_APP_PASSWORD') or ''
H = {'Authorization': 'Basic ' + base64.b64encode(f"{os.environ.get('WP_USER')}:{_pw}".encode()).decode(),
     'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
def req(path, method='GET', data=None):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H,
                               data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r, timeout=60) as f:
            b = f.read(); return json.loads(b) if b.strip() else {}
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:400]}
def all(path):
    out = []; p = 1
    while True:
        sep = '&' if '?' in path else '?'
        d = req(f"{path}{sep}per_page=100&page={p}")
        if not isinstance(d, list): return out if out else d
        out += d
        if len(d) < 100: return out
        p += 1
