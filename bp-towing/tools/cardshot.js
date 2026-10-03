const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [u,o,w] of [['https://bptowingservice.ca/?nc='+Date.now(),'prev/cw_d.png',1440],['https://bptowingservice.ca/services/?nc='+Date.now(),'prev/cw_m.png',390]]){
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:900}});await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
await p.addStyleTag({content:'html{scroll-behavior:auto!important}.elementor-invisible{visibility:visible!important}.bp-header{display:none!important}'});
const el=await p.$('.bp-card-wide');await el.scrollIntoViewIfNeeded();await p.waitForTimeout(900);
const bb=await el.boundingBox();await p.screenshot({path:o,clip:{x:0,y:Math.max(0,bb.y-300),width:w,height:Math.min(900,bb.height+340)}});await p.close()}await b.close()})()
