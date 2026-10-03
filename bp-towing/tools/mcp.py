"""Minimal JSON-RPC client for the site's MCP adapter endpoint (Streamable HTTP), auth via WP app password."""
import json, urllib.request, wp
EP = wp.U + '/wp-json/mcp/mcp-adapter-default-server'
SID = None
def rpc(method, params=None, _id=[0]):
    global SID
    _id[0] += 1
    body = {'jsonrpc': '2.0', 'id': _id[0], 'method': method, 'params': params or {}}
    h = dict(wp.H, Accept='application/json, text/event-stream')
    if SID: h['Mcp-Session-Id'] = SID
    r = urllib.request.Request(EP, data=json.dumps(body).encode(), headers=h, method='POST')
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            SID = f.headers.get('Mcp-Session-Id') or SID
            t = f.read().decode()
    except urllib.error.HTTPError as e: return {'_err': e.code, 'body': e.read().decode()[:600]}
    if t.startswith('event:') or t.startswith('data:'):
        t = [l[5:] for l in t.splitlines() if l.startswith('data:')][-1]
    return json.loads(t) if t.strip() else {}
def init():
    r = rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'cc', 'version': '1'}})
    rpc('notifications/initialized'); return r
def call(name, args=None):
    r = rpc('tools/call', {'name': name, 'arguments': args or {}})
    return r
