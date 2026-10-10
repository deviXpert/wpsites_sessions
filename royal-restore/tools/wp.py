"""WordPress REST helper for the Royal Restore site. Credentials from env (WP_URL/WP_USER/WP_APP_PASSWORD).
Refuses to run unless host matches RR_EXPECTED_HOST."""
import os, json, base64, urllib.request, urllib.parse
U = os.environ.get('WP_URL', '').rstrip('/')
EXPECTED = os.environ.get('RR_EXPECTED_HOST', 'mediumpurple-mule-193176.hostingersite.com')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: host {urllib.parse.urlparse(U).netloc!r} != {EXPECTED!r}')
H = {'Authorization': 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode(), 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
def req(path, method='GET', data=None):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H, data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r) as f: return json.load(f)
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:300]}
def all(path):
    out = []; p = 1
    while True:
        d = req(f"{path}{'&' if '?' in path else '?'}per_page=100&page={p}")
        if not isinstance(d, list): return out or d
        out += d
        if len(d) < 100: return out
        p += 1
