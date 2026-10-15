const {chromium}=require('playwright');const B='https://papayawhip-ostrich-717285.hostingersite.com';
const urls=['/','/services/','/engine-repair-calgary/','/brake-repair-calgary/','/oil-change-calgary/','/tire-shop-calgary/','/wheel-alignment-calgary/','/car-battery-replacement-calgary/','/auto-electrical-diagnostics-calgary/','/suspension-repair-calgary/','/transmission-repair-calgary/','/radiator-repair-calgary/','/car-maintenance-calgary/','/about-us/','/contact-us/','/blog/','/check-engine-light-calgary/','/winter-tires-calgary-when-to-switch/','/how-often-oil-change-calgary/'];
(async()=>{const b=await chromium.launch();for(const w of (process.argv[2]||"390,768,1024").split(",").map(Number)){const p=await b.newPage({viewport:{width:w,height:900},isMobile:w<500,hasTouch:w<500});
for(const u of urls){const r=await p.goto(B+u+'?v='+Date.now(),{waitUntil:'domcontentloaded'});await p.waitForTimeout(1200);
const o=await p.evaluate(()=>{const W=document.documentElement.clientWidth;const bad=[];
function clipped(e){for(let a=e.parentElement;a&&a!==document.body;a=a.parentElement){const s=getComputedStyle(a);if(/hidden|clip|auto|scroll/.test(s.overflowX))return true;}return false;}
for(const e of document.querySelectorAll('body *')){const r=e.getBoundingClientRect();if(!r.width||getComputedStyle(e).position==='fixed')continue;if((r.right>W+1||r.left<-1)&&!clipped(e))bad.push(String(e.className).split(' ').filter(c=>/bb-|widget-/.test(c)).slice(0,2).join('.')+':'+Math.round(r.right));}
return {sw:document.documentElement.scrollWidth,W,bad:[...new Set(bad)].slice(0,4),h1:document.querySelectorAll('h1').length,title:document.title};});
console.log(w,r.status(),u,'h1='+o.h1,o.sw>o.W?'OVERFLOW '+o.sw:'ok',o.bad.join(' '),w==390?'| '+o.title:'');}
await p.close();}await b.close();})();
