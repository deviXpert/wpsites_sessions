const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(await p.evaluate(()=>JSON.stringify({headers:document.querySelectorAll('.bp-header').length,toggles:[...document.querySelectorAll('.bp-mobnav .elementor-menu-toggle')].map(t=>{const r=t.getBoundingClientRect();return [r.x,r.y,r.width,getComputedStyle(t).display]}),navs:document.querySelectorAll('.bp-mobnav').length,svcLinks:document.querySelectorAll('.bp-has-mega .bp-mlink a').length})));await b.close()})()
