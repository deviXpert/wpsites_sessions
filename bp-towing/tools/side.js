const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:+(process.argv[3]||1440),height:900}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(await p.evaluate(()=>{const m=document.querySelector('.bp-post-main'),a=document.querySelector('.bp-post-aside');const o={};
for(const [k,e] of [['main',m],['aside',a],['form',document.querySelector('.bp-post-form')],['recent',document.querySelector('.bp-post-recent')]]){const r=e.getBoundingClientRect(),c=getComputedStyle(e);o[k]={top:Math.round(r.top+scrollY),h:Math.round(r.height),x:Math.round(r.x),w:Math.round(r.width),mt:c.marginTop,pt:c.paddingTop,as:c.alignSelf,pos:c.position,top_:c.top}}
o.inner=getComputedStyle(a.parentElement).alignItems;return JSON.stringify(o)}));await b.close()})()
