"""Minimal WordPress REST client for the Busy Bee Auto Repair site (stdlib only)."""
import base64, json, os, urllib.request, urllib.error

# Safety: only ever talk to the Busy Bee site. Other clients (AAD, EHMC) live in this repo.
EXPECTED = os.environ.get('BB_EXPECTED_HOST', 'papayawhip-ostrich-717285.hostingersite.com')
U = (os.environ.get('BB_WP_URL') or os.environ.get('WP_URL', '')).rstrip('/')
if EXPECTED not in U:
    raise SystemExit('Refusing to run: WP_URL is not ' + EXPECTED)
_USER = os.environ.get('BB_WP_USER') or os.environ['WP_USER']
_PASS = os.environ.get('BB_WP_APP_PASSWORD') or os.environ['WP_APP_PASSWORD']
_AUTH = 'Basic ' + base64.b64encode(f'{_USER}:{_PASS}'.encode()).decode()


def req(method, path, body=None, headers=None, raw=None):
    url = path if path.startswith('http') else U + '/wp-json/' + path.lstrip('/')
    h = {'Authorization': _AUTH, 'User-Agent': 'bb-tools'}
    data = raw
    if body is not None:
        data = json.dumps(body).encode(); h['Content-Type'] = 'application/json'
    h.update(headers or {})
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            t = resp.read().decode()
    except urllib.error.HTTPError as e:
        t = e.read().decode()
        try:
            return json.loads(t)
        except Exception:
            raise SystemExit(f'{method} {path}: HTTP {e.code} {t[:300]}')
    return json.loads(t) if t else None


def get(path): return req('GET', path)
def post(path, body): return req('POST', path, body)
def delete(path): return req('DELETE', path)


def upload(filepath, filename, mime, alt=''):
    with open(filepath, 'rb') as f:
        d = req('POST', 'wp/v2/media', raw=f.read(),
                headers={'Content-Type': mime, 'Content-Disposition': f'attachment; filename="{filename}"'})
    if 'id' not in d:
        raise SystemExit(f'upload {filename} failed: {d}')
    if alt:
        post(f'wp/v2/media/{d["id"]}', {'alt_text': alt})
    return d


_SID = None
def mcp(ability, params=None):
    """Call an ability on the site's MCP adapter (used for Elementor CSS regeneration / preview links)."""
    global _SID
    url = U + '/wp-json/mcp/mcp-adapter-default-server'
    def call(body, sid=None):
        h = {'Authorization': _AUTH, 'Content-Type': 'application/json'}
        if sid: h['Mcp-Session-Id'] = sid
        r = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers=h)
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.headers.get('Mcp-Session-Id'), resp.read().decode()
    if not _SID:
        _SID, _ = call({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
            'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'bb', 'version': '1'}}})
    _, t = call({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {
        'name': 'mcp-adapter-execute-ability', 'arguments': {'ability_name': ability, 'parameters': params or {}}}}, _SID)
    d = json.loads(t)
    r = d.get('result', d)
    try:
        return json.loads(r['content'][0]['text'])
    except Exception:
        return r
