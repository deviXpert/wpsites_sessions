// usage: node full.js <file|url> <out-prefix>
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const [u,out]=[process.argv[2],process.argv[3]];
for(const [n,w,h] of [['desktop',1440,900],['mobile',390,844]]){const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h},deviceScaleFactor:n=='mobile'?2:1});
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(e=>{});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){scrollTo(0,y);await new Promise(r=>setTimeout(r,140))}});
await p.waitForTimeout(1500);await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);
await p.addStyleTag({content:'.elementor-invisible{visibility:visible!important}.animated{animation:none!important}.bp-hero-copy{transform:none!important;opacity:1!important}.bp-header{position:absolute!important}'});
await p.screenshot({path:`${out}-${n}.png`,fullPage:true});await p.close()}await b.close()})()
