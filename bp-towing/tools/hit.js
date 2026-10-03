const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(await p.evaluate(()=>{const a=document.querySelector('.bp-has-mega .bp-mlink a');const r=a.getBoundingClientRect();const e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
const path=[];let n=e;while(n&&path.length<6){path.push(n.tagName+'.'+(n.className&&n.className.baseVal===undefined?n.className:'').toString().slice(0,90));n=n.parentElement}
const h=document.querySelector('.bp-header');let s=[];let m=h;while(m){const c=getComputedStyle(m);if(c.zIndex!=='auto'||c.transform!=='none'||c.isolation==='isolate')s.push(m.className.toString().slice(0,60)+' z='+c.zIndex+' t='+c.transform.slice(0,20)+' iso='+c.isolation);m=m.parentElement}
return JSON.stringify({rect:[r.x,r.y],hit:path,stack:s},null,1)}));await b.close()})()
