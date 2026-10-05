#!/bin/bash
# usage: shot.sh post_id name [widths...]
D=$(dirname "$0"); PID=$1; N=$2; shift 2; WS=${@:-1440 1024 390}
URL=$($D/mcp.sh elementor/create-preview-link "{\"post_id\":$PID}" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['url'])")
for i in 1 2 3; do curl -sS -o /dev/null "$URL"; C=$(curl -sS -o /dev/null -w "%{http_code}" "$WP_URL/wp-content/uploads/elementor/css/post-$PID.css?r=$RANDOM"); [ "$C" = 200 ] && break; sleep 2; done
NODE_PATH=$(npm root -g) node -e '
const {chromium}=require("playwright");
(async()=>{const b=await chromium.launch();
for(const w of process.argv[3].split(" ")){const p=await b.newPage({viewport:{width:+w,height:900}});
await p.goto(process.argv[1],{waitUntil:"networkidle",timeout:90000});for(let y=0;y<20000;y+=600){await p.evaluate(v=>window.scrollTo(0,v),y);await p.waitForTimeout(120);}await p.evaluate(()=>window.scrollTo(0,0));await p.waitForTimeout(1500);
await p.screenshot({path:process.argv[2]+"_"+w+".png",fullPage:true});
const h=await p.evaluate(()=>document.body.scrollHeight);const sw=await p.evaluate(()=>document.documentElement.scrollWidth);console.log(w,"height",h,"scrollWidth",sw);await p.close();}
await b.close();})()' "$URL" "$D/qa/$N" "$WS"
