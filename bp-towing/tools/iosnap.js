// Emulate the Safari failure mode in Chromium: force flex-basis:0 + column wrap like WebKit computes, and confirm our rules neutralise it
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const ctx=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:375,height:812},deviceScaleFactor:2,isMobile:true,hasTouch:true});
for(const u of ['/','/roadside-assistance/','/long-distance-towing/','/about-us/']){const p=await ctx.newPage();
const resp=await p.goto('https://bptowingservice.ca'+u+'?nc='+Date.now(),{waitUntil:'networkidle',timeout:90000}).catch(e=>null);console.log('status',resp&&resp.status(),await p.evaluate(()=>document.querySelectorAll('.bp-f1').length));
const r=await p.evaluate(()=>{const bad=[];document.querySelectorAll('.bp .e-con').forEach(c=>{const s=getComputedStyle(c);if(s.flexDirection==='column'&&s.flexWrap!=='nowrap')bad.push(c.className.slice(0,40))});
const sideBySide=[...document.querySelectorAll('.bp-col')].filter(c=>{const k=[...c.children].filter(x=>x.getBoundingClientRect().height>0);return k.length>1&&k.some((x,i)=>i&&Math.abs(x.getBoundingClientRect().left-k[0].getBoundingClientRect().left)>40&&x.getBoundingClientRect().top<k[i-1].getBoundingClientRect().bottom-5)}).length;
const f1=[...document.querySelectorAll('.bp-f1')].map(e=>getComputedStyle(e).flexBasis);
return {columnsThatCanWrap:bad.length,sideBySideColumns:sideBySide,f1Basis:[...new Set(f1)],hscroll:document.documentElement.scrollWidth>innerWidth+1}});
console.log(u.padEnd(24),JSON.stringify(r));await p.close()}await b.close()})()
