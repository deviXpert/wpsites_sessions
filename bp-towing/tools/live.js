// usage: node live.js <path> <outprefix> [maxShots]
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const [u,out,max]=[process.argv[2]||'/',process.argv[3]||'prev/live',+(process.argv[4]||4)];
for(const [n,w,h] of [['d',1440,900],['m',390,844]]){const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});
p.on('pageerror',e=>console.log(n,'JSERR',e.message.slice(0,120)));
const url=u.startsWith('http')||u.startsWith('file')?u:process.env.WP_URL.replace(/\/$/,'')+u;
await p.goto(url,{waitUntil:'networkidle',timeout:90000}).catch(e=>console.log(e.message));
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,120))}scrollTo(0,0)});
await p.waitForTimeout(800);
const H=await p.evaluate(()=>document.body.scrollHeight);console.log(n,'height',H);let k=0;
for(let y=0;y<H&&k<max;y+=h){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(700);await p.screenshot({path:`${out}_${n}_${String(k++).padStart(2,'0')}.png`});}
await p.close()}await b.close()})()
