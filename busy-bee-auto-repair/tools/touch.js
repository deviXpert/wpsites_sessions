const {chromium}=require('playwright');const B='https://papayawhip-ostrich-717285.hostingersite.com';
const urls=['/','/services/','/engine-repair-calgary/','/brake-repair-calgary/','/oil-change-calgary/','/tire-shop-calgary/','/wheel-alignment-calgary/','/car-battery-replacement-calgary/','/auto-electrical-diagnostics-calgary/','/suspension-repair-calgary/','/transmission-repair-calgary/','/radiator-repair-calgary/','/car-maintenance-calgary/','/about-us/','/contact-us/','/blog/','/check-engine-light-calgary/','/winter-tires-calgary-when-to-switch/','/how-often-oil-change-calgary/'];
(async()=>{const b=await chromium.launch();
for(const w of [390,768]){const p=await b.newPage({viewport:{width:w,height:900},isMobile:w<500});
await p.addInitScript(()=>{try{sessionStorage.setItem('busy-bee-winter-preview','seen')}catch(e){}});
for(const u of urls){await p.goto(B+u+'?v='+Date.now(),{waitUntil:'domcontentloaded'});const H=await p.evaluate(()=>document.documentElement.scrollHeight);
for(let y=0;y<H;y+=800){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(40);}await p.waitForTimeout(600);
const r=await p.evaluate(()=>{const out=[];
const card=e=>{const s=getComputedStyle(e);return (s.backgroundColor!=='rgba(0, 0, 0, 0)'||s.backgroundImage!=='none'||parseFloat(s.borderTopWidth)>0||s.boxShadow!=='none')};
for(const par of document.querySelectorAll('.e-con')){const ps=getComputedStyle(par);if(ps.display!=='flex'&&ps.display!=='grid')continue;
 const kids=[...par.children].filter(k=>{const s=getComputedStyle(k);const r=k.getBoundingClientRect();return r.height>0&&s.position!=='absolute'&&s.position!=='fixed'&&s.display!=='none'});
 for(let i=1;i<kids.length;i++){const a=kids[i-1].getBoundingClientRect(),c=kids[i].getBoundingClientRect();
  if(Math.abs(a.left-c.left)>4&&c.top<a.bottom-2)continue; // side by side
  const gap=c.top-a.bottom;if(gap<6&&card(kids[i-1])&&card(kids[i])&&!kids[i].closest('.e-n-menu,.bb-faq-cards,.bb-callbar,.bb-sm-trust,.bb-foot-links,.elementor-location-popup'))
   out.push(Math.round(gap)+'px '+((String(kids[i-1].className).match(/bb-[\w-]+/)||[kids[i-1].dataset.id])[0])+' → '+((String(kids[i].className).match(/bb-[\w-]+/)||[kids[i].dataset.id])[0])+' @'+Math.round(c.top+scrollY));}}
return [...new Set(out)];});
if(r.length)console.log(w,u,'\n   '+r.slice(0,12).join('\n   '));}
await p.close();}await b.close();console.log('done');})();
