#!/bin/bash
# usage: warm.sh post_id  -> prints a preview URL whose CSS file is generated
D=$(dirname "$0"); PID=$1
for i in 1 2 3 4; do
  (cd $D && python3 -c "from el import regen; regen($PID)" >/dev/null); sleep 4
  URL=$($D/mcp.sh elementor/create-preview-link "{\"post_id\":$PID}" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['url'])")
  curl -sS -o /dev/null "$URL"; sleep 2; curl -sS -o /dev/null "$URL"
  C=$(curl -sS -o /dev/null -w "%{http_code}" "$WP_URL/wp-content/uploads/elementor/css/post-$PID.css?r=$RANDOM")
  [ "$C" = 200 ] && { echo "$URL"; exit 0; }
  sleep 3
done
echo "FAIL" >&2; exit 1
