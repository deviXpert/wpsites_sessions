"""WordPress REST helper for the Quality Waterproofing site. Credentials come ONLY from env vars WP_URL / WP_USER / WP_APP_PASSWORD.
Refuses to run unless WP_URL host matches QW_EXPECTED_HOST (default: the QW staging site)."""
import os, json, base64, urllib.request, urllib.parse, mimetypes
U = (os.environ.get('WP_URL') or '').rstrip('/')
EXPECTED = os.environ.get('QW_EXPECTED_HOST', 'meteoric-cornflowerblue-pheasant-37.hostingersite.com')
if urllib.parse.urlparse(U).netloc != EXPECTED:
    raise SystemExit(f'Refusing to run: WP_URL host is {urllib.parse.urlparse(U).netloc!r}, expected {EXPECTED!r}')
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
H = {'Authorization': AUTH, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
def req(path, method='GET', data=None):
    r = urllib.request.Request(U + '/wp-json/' + path, method=method, headers=H, data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(r, timeout=120) as f: return json.load(f)
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:400]}
def upload(fp, name=None):
    name = name or os.path.basename(fp)
    h = {'Authorization': AUTH, 'Content-Disposition': f'attachment; filename="{name}"', 'Content-Type': mimetypes.guess_type(name)[0] or 'application/octet-stream', 'User-Agent': 'Mozilla/5.0'}
    r = urllib.request.Request(U + '/wp-json/wp/v2/media', method='POST', headers=h, data=open(fp, 'rb').read())
    with urllib.request.urlopen(r, timeout=300) as f: return json.load(f)
