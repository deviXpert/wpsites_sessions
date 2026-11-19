#!/bin/bash
# usage: mcp.sh <ability-name> '<json params>'   |  mcp.sh list
EXPECTED_HOST="${QW_EXPECTED_HOST:-meteoric-cornflowerblue-pheasant-37.hostingersite.com}"; case "$WP_URL" in *"$EXPECTED_HOST"*) ;; *) echo "Refusing: WP_URL is not $EXPECTED_HOST" >&2; exit 1;; esac
D=$(dirname "$0"); U="${WP_URL%/}/wp-json/mcp/mcp-adapter-default-server"
if [ ! -s "$D/.sid" ]; then curl -sS -D "$D/.h.txt" -o /dev/null -u "$WP_USER:$WP_APP_PASSWORD" -H 'Content-Type: application/json' "$U" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"cc","version":"1"}}}'; grep -i '^mcp-session-id' "$D/.h.txt" | cut -d' ' -f2 | tr -d '\r' > "$D/.sid"; fi
P=${2:-'{}'}
if [ "$1" = "list" ]; then BODY='{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mcp-adapter-discover-abilities","arguments":{}}}'
elif [ "$1" = "info" ]; then BODY=$(python3 -c "import json,sys;print(json.dumps({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'mcp-adapter-get-ability-info','arguments':{'ability_name':sys.argv[1]}}}))" "$P")
else BODY=$(python3 -c "import json,sys;print(json.dumps({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'mcp-adapter-execute-ability','arguments':{'ability_name':sys.argv[1],'parameters':json.loads(sys.argv[2])}}}))" "$1" "$P"); fi
call() { curl -sS -u "$WP_USER:$WP_APP_PASSWORD" -H 'Content-Type: application/json' -H "Mcp-Session-Id: $(cat $D/.sid)" -H "MCP-Protocol-Version: 2025-06-18" "$U" --data-binary "$BODY"; }
OUT=$(call)
if echo "$OUT" | grep -q 'Session not found'; then  # MCP session expired: start a new one and retry once
  rm -f "$D/.sid"; curl -sS -D "$D/.h.txt" -o /dev/null -u "$WP_USER:$WP_APP_PASSWORD" -H 'Content-Type: application/json' "$U" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"cc","version":"1"}}}'
  grep -i '^mcp-session-id' "$D/.h.txt" | cut -d' ' -f2 | tr -d '\r' > "$D/.sid"; OUT=$(call)
fi
echo "$OUT" | python3 -c "
import sys,json;d=json.load(sys.stdin);r=d.get('result',d)
if 'content' in r: print(r['content'][0]['text'])
else: print(json.dumps(r))"
