const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [n,w,h,u] of [['L',1440,1000,'/'],['LM',390,844,'/']]){const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});
p.on('pageerror',e=>console.log(n,'ERR',e.message.slice(0,100)));
await p.goto(process.env.WP_URL+u+'?nc='+Date.now(),{waitUntil:'networkidle',timeout:90000}).catch(e=>console.log(e.message));
console.log(n,await p.evaluate(()=>({h:document.body.scrollHeight,headers:document.querySelectorAll('.x-header').length,footers:document.querySelectorAll('.x-footer').length,oldHdr:document.querySelectorAll('[data-elementor-id="241"],[data-elementor-id="272"]').length,astraHdr:document.querySelectorAll('#masthead,.site-footer').length,font:getComputedStyle(document.querySelector('h1')||document.body).fontFamily,tpl:document.body.className.match(/page-template-\S+/)?.[0]})));
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){scrollTo(0,y);await new Promise(r=>setTimeout(r,80))}});
const H=await p.evaluate(()=>document.body.scrollHeight);let k=0;for(let y=0;y<H&&k<30;y+=h){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(600);await p.screenshot({path:`${n}_${k++}.png`});}}
await b.close()})()
