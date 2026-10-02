const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const u='https://maroon-raven-160825.hostingersite.com/flat-battery-service-birmingham/?nc='+Date.now();
let p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(e=>console.log(e.message));
await p.hover('.x-mm-has>.x-mm-link');await p.waitForTimeout(500);await p.screenshot({path:'prevmm/live_d.png'});
p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844},isMobile:true,hasTouch:true});
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(e=>console.log(e.message));
await p.tap('.x-burger');await p.waitForTimeout(600);await p.screenshot({path:'prevmm/live_m.png'});
await b.close()})()
