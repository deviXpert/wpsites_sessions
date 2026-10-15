const {chromium}=require('playwright');const B='https://papayawhip-ostrich-717285.hostingersite.com';
const urls=['/','/services/','/engine-repair-calgary/','/brake-repair-calgary/','/oil-change-calgary/','/tire-shop-calgary/','/wheel-alignment-calgary/','/car-battery-replacement-calgary/','/auto-electrical-diagnostics-calgary/','/suspension-repair-calgary/','/transmission-repair-calgary/','/radiator-repair-calgary/','/car-maintenance-calgary/','/about-us/','/contact-us/','/blog/','/check-engine-light-calgary/','/winter-tires-calgary-when-to-switch/','/how-often-oil-change-calgary/'];
const OKTEL={'4039305888':'(403) 930-5888','8255401995':'(825) 540-1995'};const OKMAIL=['busybeeautocalgary@gmail.com'];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});const all={};
for(const u of urls){await p.goto(B+u+'?v='+Date.now(),{waitUntil:'domcontentloaded'});await p.waitForTimeout(800);
const r=await p.evaluate(()=>{const html=document.documentElement.outerHTML;const txt=document.body.innerText;
return {phones:[...new Set(txt.match(/\(?\d{3}\)?[\s.-]?\d{3}[\s.-]\d{4}/g)||[])],emails:[...new Set(html.match(/[\w.+-]+@[\w-]+\.[\w.]+/g)||[])].filter(e=>!/\.(png|webp|js|css|svg)$/.test(e)),
tels:[...document.querySelectorAll('a[href^="tel:"]')].map(a=>a.getAttribute('href')+' => '+(a.innerText||a.getAttribute('aria-label')||'').trim().replace(/\s+/g,' ').slice(0,40)),
mails:[...document.querySelectorAll('a[href^="mailto:"]')].map(a=>a.getAttribute('href'))};});
const bad=[];for(const t of r.tels){const d=t.split(' => ')[0].replace(/\D/g,'').replace(/^1/,'');if(!OKTEL[d])bad.push('BAD TEL '+t);else{const txt=t.split(' => ')[1];const m=txt.match(/\(?\d{3}\)?[\s.-]?\d{3}[\s.-]\d{4}/);if(m&&m[0].replace(/\D/g,'')!==d)bad.push('MISMATCH '+t);}}
for(const ph of r.phones){if(!OKTEL[ph.replace(/\D/g,'')])bad.push('BAD PHONE TEXT '+ph);}
for(const e of r.emails){if(!OKMAIL.includes(e.toLowerCase())&&!/wordpress|sentry|example|w3\.org|schema|elementor|trustindex|yoast/i.test(e))bad.push('OTHER EMAIL '+e);}
for(const m of r.mails){if(!OKMAIL.includes(m.replace('mailto:','').split('?')[0]))bad.push('BAD MAILTO '+m);}
console.log(u.padEnd(42),'tel:',r.tels.length,'mailto:',r.mails.length,'phones:',r.phones.join(','),bad.length?'\n   '+bad.join('\n   '):'OK');
for(const t of r.tels)all[t.split(' => ')[0]]=(all[t.split(' => ')[0]]||0)+1;}
console.log('tel hrefs used:',JSON.stringify(all));await b.close();})();
