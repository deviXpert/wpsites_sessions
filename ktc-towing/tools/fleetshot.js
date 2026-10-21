const {chromium}=require('playwright');(async()=>{
const [url,pre]=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [n,w,h,m] of [['d',1440,900,false],['m',390,844,true]]){
 const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h},isMobile:m,hasTouch:m});
 await p.goto(url,{waitUntil:'networkidle',timeout:120000}).catch(e=>console.log(e.message));
 const el=await p.$('.ktc-fleet'); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(1500);
 if(n==='d'){const c=await p.$('.ktc-fc:nth-of-type(1)');}
 await el.screenshot({path:`shots/${pre}_${n}.png`});
 await p.close();}
await b.close()})()
