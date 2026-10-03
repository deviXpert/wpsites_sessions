const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const [u,out]=[process.argv[2],process.argv[3]];
for(const [n,w,h] of [['d',1440,900],['m',390,844]]){const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h},deviceScaleFactor:n=='m'?2:1});
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(e=>{});
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=300){scrollTo(0,y);await new Promise(r=>setTimeout(r,120))}});
await p.addStyleTag({content:'html{scroll-behavior:auto!important}.elementor-invisible{visibility:visible!important}.animated{animation:none!important}.bp-hero-copy{transform:none!important;opacity:1!important}.bp-rv{opacity:1!important;transform:none!important}'});
await p.evaluate(()=>{document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,0)});await p.waitForTimeout(1000);const H=await p.evaluate(()=>document.body.scrollHeight);let k=0;
for(let y=0;y<H;y+=h){await p.evaluate(y=>window.scrollTo({top:y,behavior:'instant'}),y);await p.waitForTimeout(600);await p.screenshot({path:`${out}_${n}_${String(k++).padStart(2,'0')}.png`});}
await p.close()}await b.close()})()
