const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const [u,out,y]=process.argv.slice(2);const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});await p.addStyleTag({content:'html{scroll-behavior:auto!important}.elementor-invisible{visibility:visible!important}'});
await p.evaluate(y=>scrollTo(0,+y),y||0);await p.waitForTimeout(1200);await p.screenshot({path:out});await b.close()})()
