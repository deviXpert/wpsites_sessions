const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto('file://'+process.cwd()+'/prev/home.html',{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(JSON.stringify(await p.evaluate(()=>{const o=[];for(const s of ['.bp-fbottom','.bp-fbottom .bp-copy','.bp-ffollow','.bp-ftop','.bp-fgrid']){const e=document.querySelector(s);if(!e){o.push([s,'none']);continue}const c=getComputedStyle(e);o.push([s,e.getBoundingClientRect().width,c.display,c.flexDirection,c.flex,c.width,e.parentElement.className.slice(0,80)])}return o}),null,1));
await b.close()})()
