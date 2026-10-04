"""WordPress REST helper for the Pak Translations site. Credentials come ONLY from environment variables
(PAK_WP_URL / PAK_WP_USER / PAK_WP_APP_PASSWORD preferred, falls back to WP_URL / WP_USER / WP_APP_PASSWORD).
Refuses to run unless the URL host matches PAK_EXPECTED_HOST (default: pak-translations.com)."""
import os, json, base64, urllib.request, urllib.parse
def _env(k): return os.environ.get('PAK_' + k) or os.environ.get(k)
U = (_env('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('PAK_EXPECTED_HOST', 'pak-translations.com')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r}.')
H = {'Authorization': 'Basic ' + base64.b64encode(f"{_env('WP_USER')}:{_env('WP_APP_PASSWORD')}".encode()).decode(), 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
def req(path, method='GET', data=None):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H, data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            b = f.read()
            if not b.strip(): return {"_empty": f.status}
            try: return json.loads(b)
            except ValueError:   # Elementor (CSS print method "internal") echoes <style> blocks before the JSON on saves
                i = b.find(b'{"id":'); return json.loads(b[i:]) if i >= 0 else {'_err': 'non-json', 'body': b[:300].decode(errors='replace')}
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:500]}
def all(path):
    out = []; p = 1
    while True:
        sep = '&' if '?' in path else '?'
        d = req(f"{path}{sep}per_page=100&page={p}")
        if not isinstance(d, list): return out if out else d
        out += d
        if len(d) < 100: return out
        p += 1
