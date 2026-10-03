// node tools/shot1920.js <url> <out.png> <scrollToSelector?>  -> 1920x1000 viewport screenshot
const {chromium}=require('playwright');(async()=>{const [url,out,sel]=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});const p=await (await b.newContext({ignoreHTTPSErrors:true,viewport:{width:1920,height:1000}})).newPage();
await p.goto(url+'?nc='+Date.now(),{waitUntil:'networkidle'});await p.addStyleTag({content:'.x-js .rv,.x-js .rv-st>*{opacity:1!important;transform:none!important}'});
if(sel){await p.evaluate(s=>{const e=document.querySelector(s);if(e)scrollTo(0,e.getBoundingClientRect().top+scrollY-120)},sel);}
await p.waitForTimeout(1200);await p.screenshot({path:out});await b.close()})();
