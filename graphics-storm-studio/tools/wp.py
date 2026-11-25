"""WordPress REST helper for Graphics Storm Studio. Credentials come ONLY from env vars
(GSS_WP_URL/GSS_WP_USER/GSS_WP_APP_PASSWORD preferred, else WP_URL/WP_USER/WP_APP_PASSWORD).
Refuses to run unless the host is graphicsstormstudio.com (override: GSS_EXPECTED_HOST)."""
import os, json, base64, urllib.request, urllib.parse, urllib.error
def _env(k): return os.environ.get('GSS_' + k) or os.environ.get(k)
U = (_env('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('GSS_EXPECTED_HOST', 'graphicsstormstudio.com')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r}')
H = {'Authorization': 'Basic ' + base64.b64encode(f"{_env('WP_USER')}:{_env('WP_APP_PASSWORD')}".encode()).decode(),
     'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (gss-build)'}
def req(path, method='GET', data=None, raw=False):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H,
                               data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r, timeout=120) as f: return json.load(f)
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:500]}
def all(path):
    out, p = [], 1
    while True:
        d = req(f"{path}{'&' if '?' in path else '?'}per_page=100&page={p}")
        if not isinstance(d, list): return out or d
        out += d
        if len(d) < 100: return out
        p += 1
def ability(name, params=None, method='POST'):
    """Run a WP Abilities API ability (Elementor tools). Read-only abilities need GET,
    destructive ones DELETE (input passed as ?input=JSON), others POST."""
    p = 'wp-abilities/v1/abilities/' + name + '/run'
    if method in ('GET', 'DELETE'):
        q = ('?' + urllib.parse.urlencode({f'input[{k}]': (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in params.items()})) if params else ''
        return req(p + q, method)
    return req(p, 'POST', {'input': params or {}})
