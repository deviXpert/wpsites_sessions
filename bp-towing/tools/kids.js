const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(await p.evaluate(()=>{const a=document.querySelector('.bp-post-aside');const par=a.parentElement;const c=getComputedStyle(par);
return [par.className.slice(0,80),'dir='+c.flexDirection,'ai='+c.alignItems,'gap='+c.gap,...[...par.children].map(k=>{const r=k.getBoundingClientRect();const s=getComputedStyle(k);return k.className.slice(0,60)+' top='+Math.round(r.top+scrollY)+' h='+Math.round(r.height)+' as='+s.alignSelf+' mt='+s.marginTop+' trf='+s.transform.slice(0,30)+' anim='+s.animationName})].join('\n')}));await b.close()})()
