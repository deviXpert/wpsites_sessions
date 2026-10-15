// Site-wide quality audit: node qa.js [widths]  – console errors, failed requests, broken images, alt text, overflow,
// H1 / title / meta description, tiny text, small tap targets.  Prints only problems.
const {chromium}=require('playwright');const B='https://papayawhip-ostrich-717285.hostingersite.com';
const urls=['/','/services/','/engine-repair-calgary/','/brake-repair-calgary/','/oil-change-calgary/','/tire-shop-calgary/','/wheel-alignment-calgary/','/car-battery-replacement-calgary/','/auto-electrical-diagnostics-calgary/','/suspension-repair-calgary/','/transmission-repair-calgary/','/radiator-repair-calgary/','/car-maintenance-calgary/','/about-us/','/contact-us/','/blog/','/check-engine-light-calgary/','/winter-tires-calgary-when-to-switch/','/how-often-oil-change-calgary/'];
const widths=(process.argv[2]||'1440,768,390').split(',').map(Number);
(async()=>{const b=await chromium.launch();
for(const w of widths){const ctx=await b.newContext({viewport:{width:w,height:900},isMobile:w<500,hasTouch:w<500});
await ctx.addInitScript(()=>{try{sessionStorage.setItem('busy-bee-winter-preview','seen')}catch(e){}});
for(const u of urls){const p=await ctx.newPage();const errs=[],fails=[];
p.on('pageerror',e=>errs.push(e.message.slice(0,100)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,100))});
p.on('response',r=>{if(r.status()>=400&&!/google|gstatic|trustindex|facebook|doubleclick/.test(r.url()))fails.push(r.status()+' '+r.url().slice(0,90))});
await p.goto(B+u+'?v='+Date.now(),{waitUntil:'domcontentloaded'});const H=await p.evaluate(()=>document.documentElement.scrollHeight);
for(let y=0;y<H;y+=700){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(60);}await p.waitForTimeout(900);
const r=await p.evaluate((w)=>{const out=[];const W=document.documentElement.clientWidth;
const vis=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&+s.opacity>0.05&&!e.closest('.elementor-popup-modal,[aria-hidden=true],.e-n-menu-content:not(.e-active)')};
const lab=e=>(e.innerText||e.getAttribute('aria-label')||e.alt||'').trim().replace(/\s+/g,' ').slice(0,30)+' ['+((String(e.closest('[class*="bb-"]')?.className||'').match(/bb-[\w-]+/)||[''])[0])+']';
if(document.documentElement.scrollWidth>W+1)out.push('OVERFLOW '+document.documentElement.scrollWidth);
const h1=[...document.querySelectorAll('h1')].filter(vis);if(h1.length!==1)out.push('H1 count '+h1.length);
if(!document.title||document.title.length<20)out.push('short title');
for(const i of document.querySelectorAll('img')){if(!vis(i))continue;if(i.complete&&i.naturalWidth===0)out.push('BROKEN IMG '+(i.currentSrc||i.src).slice(-50));if(!i.hasAttribute('alt'))out.push('NO ALT '+(i.currentSrc||i.src).slice(-40));}
for(const a of document.querySelectorAll('a,button,select,input:not([type=hidden]),textarea')){if(!vis(a)||a.closest('.e-n-menu-content'))continue;const r=a.getBoundingClientRect();
 if(w<500&&(r.height<32||r.width<32)&&!a.closest('.elementor-post__text,.bb-post-content,.trustindex,.ti-widget,p'))out.push('SMALL TAP '+Math.round(r.width)+'x'+Math.round(r.height)+' '+lab(a));
 if(a.tagName==='A'&&!a.innerText.trim()&&!a.getAttribute('aria-label')&&!a.querySelector('img[alt]:not([alt=""]),svg title'))out.push('UNLABELLED LINK '+(a.getAttribute('href')||'').slice(0,40)+' '+lab(a));}
const tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n,seen=new Set();while(n=tw.nextNode()){const e=n.parentElement;if(!n.textContent.trim()||seen.has(e)||!vis(e)||e.closest('script,style,.ti-widget'))continue;seen.add(e);
 const fs=parseFloat(getComputedStyle(e).fontSize);if(fs<10)out.push('TINY TEXT '+fs+'px '+lab(e));
 const r=e.getBoundingClientRect();if(r.right>W+1)out.push('TEXT OFFSCREEN '+lab(e));}
return out;},w);
const meta=await p.evaluate(()=>document.querySelector('meta[name=description]')?.content||'');
const all=[...new Set([...r,...errs.map(e=>'JS '+e),...fails.map(f=>'HTTP '+f)])];
if(w===1440&&!meta)all.push('no meta description');
if(all.length)console.log(w,u,'\n   '+all.slice(0,60).join('\n   ')+(all.length>14?'\n   …+'+(all.length-14):''));
await p.close();}await ctx.close();}
await b.close();console.log('done');})();
