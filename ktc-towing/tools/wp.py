import os, json, base64, urllib.request, urllib.parse
U = os.environ["WP_URL"].rstrip("/")
assert urllib.parse.urlparse(U).hostname in ("ktctowing.ca", os.environ.get("KTC_EXPECTED_HOST", "ktctowing.ca")), "WP_URL is not the KTC site: " + U
AUTH = "Basic " + base64.b64encode(f'{os.environ["WP_USER"]}:{os.environ["WP_APP_PASSWORD"]}'.encode()).decode()

def req(method, path, data=None, auth=True):
    url = path if path.startswith("http") else U + "/wp-json/" + path.lstrip("/")
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method, headers={"Content-Type": "application/json", "User-Agent": "ktc-tools"})
    if auth: r.add_header("Authorization", AUTH)
    with urllib.request.urlopen(r, timeout=90) as resp:
        return json.loads(resp.read())

get = lambda p, **k: req("GET", p, **k)
post = lambda p, d: req("POST", p, d)
