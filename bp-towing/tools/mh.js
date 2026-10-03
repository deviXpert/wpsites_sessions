const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
let i=0;for(const u of process.argv.slice(2)){const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844},deviceScaleFactor:2});
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});await p.waitForTimeout(800);
await p.screenshot({path:`prev/mh${i}.png`,clip:{x:0,y:0,width:390,height:260}});
await p.evaluate(()=>{document.documentElement.style.scrollBehavior='auto';scrollTo(0,900)});await p.waitForTimeout(700);
await p.screenshot({path:`prev/mh${i}s.png`,clip:{x:0,y:0,width:390,height:140}});i++;await p.close()}await b.close()})()
