const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
await p.locator('.bp-mobnav .elementor-menu-toggle').first().click({force:true});await p.waitForTimeout(600);
console.log(await p.evaluate(()=>JSON.stringify([...document.querySelectorAll('.bp-mobnav .elementor-nav-menu--dropdown > ul > li > a')].map(a=>{const r=a.getBoundingClientRect();const c=getComputedStyle(a);return [a.textContent.trim(),Math.round(r.y),Math.round(r.height),c.display,c.visibility]}))));
await b.close()})()
