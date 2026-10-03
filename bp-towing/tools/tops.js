const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const s of process.argv.slice(2)){const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto('https://bptowingservice.ca/'+s+'/?nc='+Date.now(),{waitUntil:'networkidle',timeout:90000}).catch(()=>{});await p.waitForTimeout(1500);
await p.screenshot({path:'prev/top_'+s+'.png'});await p.close()}await b.close()})()
