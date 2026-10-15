const {chromium}=require('playwright');const B='https://papayawhip-ostrich-717285.hostingersite.com';
const urls=['/','/services/','/engine-repair-calgary/','/brake-repair-calgary/','/oil-change-calgary/','/tire-shop-calgary/','/wheel-alignment-calgary/','/car-battery-replacement-calgary/','/auto-electrical-diagnostics-calgary/','/suspension-repair-calgary/','/transmission-repair-calgary/','/radiator-repair-calgary/','/car-maintenance-calgary/','/about-us/','/contact-us/','/blog/','/check-engine-light-calgary/','/winter-tires-calgary-when-to-switch/','/how-often-oil-change-calgary/'];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});const internal=new Set(),external=new Set();
for(const u of urls){await p.goto(B+u+'?v='+Date.now(),{waitUntil:'domcontentloaded'});await p.waitForTimeout(1000);
const r=await p.evaluate(()=>{const issues=[];const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));const hrefs=[];
for(const a of document.querySelectorAll('a')){const h=a.getAttribute('href');const vis=a.getBoundingClientRect().width>0||a.closest('.elementor-popup-modal, [data-elementor-type=popup]');
 const label=(a.innerText||a.getAttribute('aria-label')||a.querySelector('img')?.alt||'').trim().replace(/\s+/g,' ').slice(0,40);
 if(h===null){if(vis)issues.push('NO HREF: '+label);continue;}
 if(h.startsWith('#elementor-action'))continue;
 if(h==='#'||h===''){if(a.getAttribute('role')!=='button'&&!a.closest('.bb-vbtn,.bb-sm-sel,.bb-filter,.bb-rev-prev,.bb-rev-next,.e-n-menu,.bb-filters'))issues.push('EMPTY #: '+label+' ['+String(a.closest('[class*=bb-]')?.className).match(/bb-[\w-]+/)?.[0]+']');continue;}
 if(h.startsWith('#')){if(!ids.has(h.slice(1)))issues.push('MISSING ANCHOR '+h+': '+label);continue;}
 hrefs.push(h);}
for(const btn of document.querySelectorAll('.elementor-button')){if(btn.tagName!=='A'&&!btn.closest('form')&&btn.getBoundingClientRect().width>0)issues.push('BUTTON NOT LINK: '+btn.innerText.trim().slice(0,30));}
return {issues:[...new Set(issues)],hrefs};});
for(const h of r.hrefs){if(h.startsWith('/')||h.includes('hostingersite.com'))internal.add(h.replace(/https?:\/\/[^/]+/,'').split('?')[0].split('#')[0]||'/');else if(h.startsWith('http'))external.add(h);}
console.log(u.padEnd(42),r.issues.length?'\n   '+r.issues.join('\n   '):'OK');}
console.log('\nINTERNAL TARGETS',internal.size);
for(const h of internal){if(!h.startsWith('/'))continue;const res=await p.request.get(B+h,{maxRedirects:0}).catch(e=>null);const st=res?res.status():'ERR';if(st!==200)console.log('  ',st,h);}
console.log('EXTERNAL',[...external].map(e=>e.slice(0,90)).join('\n  '));await b.close();})();
