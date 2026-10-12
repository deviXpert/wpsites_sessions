const { chromium } = require('/opt/node-tools/node_modules/playwright');
const URL='https://papayawhip-ostrich-717285.hostingersite.com/?nc='+Date.now();
const res=[]; const ok=(n,c,d='')=>res.push(`${c?'PASS':'FAIL'}  ${n}${d?' — '+d:''}`);
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  // ---------- desktop
  let ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, ignoreHTTPSErrors: true });
  let p = await ctx.newPage(); const errs=[]; p.on('pageerror', e=>errs.push(e.message)); p.on('console', m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto(URL, { waitUntil: 'networkidle' });
  ok('No JS errors on load', errs.length===0, errs.slice(0,3).join(' | '));
  // typing
  const t1=await p.textContent('.bb-hero .bb-typed'); await p.waitForTimeout(700); const t2=await p.textContent('.bb-hero .bb-typed');
  ok('Hero "trust" typing animation runs', t1!==t2 || t2.length<5, `${JSON.stringify(t1)} → ${JSON.stringify(t2)}`);
  // vehicle buttons
  await p.click('.bb-hero .bb-vbtn[data-slide="2"] a');
  await p.waitForTimeout(1200);
  const st=await p.evaluate(()=>({act:[...document.querySelectorAll('.bb-hero .bb-slide.is-active')].map(e=>e.dataset.slide),name:document.querySelector('.bb-hero .bb-vname').textContent,btn:document.querySelector('.bb-hero .bb-vbtn.is-active').dataset.slide}));
  ok('Hero vehicle button switches slide (Mercedes)', st.act.includes('2') && st.name==='Mercedes' && st.btn==='2', JSON.stringify(st));
  // nav anchors
  await p.click('.bb-nav a:has-text("Pricing")'); await p.waitForTimeout(1500);
  const y=await p.evaluate(()=>Math.abs(document.querySelector('#pricing').getBoundingClientRect().top));
  ok('Header nav "Pricing" scrolls to section', y<120, `offset ${Math.round(y)}px`);
  // popup auto (scroll)
  await p.evaluate(()=>{sessionStorage.removeItem('busy-bee-winter-preview')}); await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(300);
  await p.evaluate(()=>scrollTo(0,800)); await p.waitForTimeout(1500);
  let vis=await p.evaluate(()=>{const m=document.querySelector('#elementor-popup-modal-'+document.querySelector('[data-popup]').dataset.popup);return !!m && getComputedStyle(m).display!=='none';});
  ok('Winter popup opens after scrolling 650px (desktop)', vis);
  if(vis){ await p.click('.elementor-popup-modal .dialog-close-button'); await p.waitForTimeout(800); }
  vis=await p.evaluate(()=>[...document.querySelectorAll('.elementor-popup-modal')].some(m=>getComputedStyle(m).display!=='none'));
  ok('Popup closes with ✕', !vis);
  await p.evaluate(()=>scrollTo(0,3000)); await p.waitForTimeout(600); await p.evaluate(()=>scrollTo(0,200)); await p.waitForTimeout(600);
  vis=await p.evaluate(()=>[...document.querySelectorAll('.elementor-popup-modal')].some(m=>getComputedStyle(m).display!=='none'));
  ok('Popup only shows once per session', !vis);
  // offer cards
  for (const [i,name] of [[0,'tires'],[1,'oil'],[2,'battery']]) {
    await p.locator('.bb-offer').nth(i).scrollIntoViewIfNeeded(); await p.locator('.bb-offer').nth(i).click(); await p.waitForTimeout(1000);
    const shown=await p.evaluate(()=>{const m=[...document.querySelectorAll('.elementor-popup-modal')].find(m=>getComputedStyle(m).display!=='none'); return m? m.textContent.replace(/\s+/g,' ').slice(0,60):null;});
    ok(`Offer card "${name}" opens its popup`, !!shown, shown||'');
    await p.keyboard.press('Escape'); await p.waitForTimeout(600);
  }
  // filters
  await p.click('.bb-filter[data-filter="Repair"] a'); await p.waitForTimeout(300);
  let f=await p.evaluate(()=>[...document.querySelectorAll('#services [data-cat]')].filter(c=>getComputedStyle(c).display!=='none').map(c=>c.dataset.cat));
  ok('Services filter "Repair"', f.length===5 && f.every(c=>c==='Repair'), f.join(','));
  await p.click('.bb-filter[data-filter="Tires"] a'); await p.waitForTimeout(300);
  f=await p.evaluate(()=>[...document.querySelectorAll('#services [data-cat]')].filter(c=>getComputedStyle(c).display!=='none').map(c=>c.dataset.cat));
  ok('Services filter "Tires"', f.length===1 && f[0]==='Tires', f.join(','));
  await p.click('.bb-filter[data-filter="All"] a'); await p.waitForTimeout(300);
  f=await p.evaluate(()=>[...document.querySelectorAll('#services [data-cat]')].filter(c=>getComputedStyle(c).display!=='none').length);
  ok('Services filter "All"', f===9, f+' cards');
  // reviews arrows
  const before=await p.evaluate(()=>document.querySelector('.bb-review-track').scrollLeft);
  await p.click('.bb-rev-next a'); await p.waitForTimeout(900);
  const after=await p.evaluate(()=>document.querySelector('.bb-review-track').scrollLeft);
  ok('Reviews "next" arrow scrolls cards', after>before, `${before} → ${after}`);
  // reveal
  const rv=await p.evaluate(()=>[...document.querySelectorAll('.bb-reveal')].filter(e=>e.classList.contains('is-in')).length);
  ok('Review cards reveal on scroll', rv>0, rv+' revealed');
  // FAQ toggle
  await p.locator('.bb-faq .elementor-tab-title').nth(1).scrollIntoViewIfNeeded();
  await p.locator('.bb-faq .elementor-tab-title').nth(1).click(); await p.waitForTimeout(600);
  const faqOpen=await p.evaluate(()=>{const c=document.querySelectorAll('.bb-faq .elementor-tab-content')[1];return getComputedStyle(c).display!=='none' && c.textContent.trim();});
  ok('FAQ question opens', !!faqOpen, faqOpen||'');
  const schema=await p.evaluate(()=>[...document.querySelectorAll('script[type="application/ld+json"]')].some(s=>s.textContent.includes('FAQPage')));
  ok('FAQ schema (FAQPage JSON-LD) present', schema);
  // symptom checker
  await p.fill('[name="form_fields[make]"]','Toyota'); await p.fill('[name="form_fields[model]"]','Camry'); await p.fill('[name="form_fields[year]"]','2019'); await p.fill('[name="form_fields[mileage]"]','120,000');
  const vt=await p.evaluate(()=>[document.querySelector('.bb-veh-title .elementor-heading-title').textContent,document.querySelector('.bb-veh-year').textContent,document.querySelector('.bb-veh-km').textContent]);
  ok('Symptom checker live vehicle title', vt[0]==='Toyota Camry' && vt[1]==='2019' && vt[2]==='120,000 km', vt.join(' | '));
  await p.click('.bb-chips button[data-add="Warning light"]'); await p.click('.bb-chips button[data-add="Vibration"]');
  const iss=await p.inputValue('[name="form_fields[issue]"]');
  ok('Symptom chips add text', iss.includes('Warning light') && iss.includes('Vibration'), JSON.stringify(iss));
  // booking form required validation (no submit to avoid emailing the shop)
  const v=await p.evaluate(()=>{const n=document.querySelector('[name="form_fields[name]"]');const ph=document.querySelector('[name="form_fields[phone]"]');return [n.required, ph.required, ph.type]});
  ok('Booking form: name + phone required, phone is tel', v[0]&&v[1]&&v[2]==='tel', JSON.stringify(v));
  const radios=await p.evaluate(()=>document.querySelectorAll('[name="form_fields[reason]"]').length);
  ok('Booking form: 9 visit reasons', radios===9, radios+'');
  await p.locator('.bb-book-form label:has-text("Brake issue")').click();
  const chk=await p.evaluate(()=>{const r=[...document.querySelectorAll('[name="form_fields[reason]"]')].find(r=>r.checked);return r&&r.value;});
  ok('Booking form: reason chip selectable', chk==='Brake issue', chk);
  // links
  const links=await p.evaluate(()=>{const a=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));return {tel:a.filter(h=>h.startsWith('tel:')).length, wa:a.filter(h=>h.includes('wa.me')).length, maps:a.filter(h=>h.includes('maps.google')).length, mail:a.filter(h=>h.startsWith('mailto:')).length, empty:a.filter(h=>h==='#'||h==='').length}});
  ok('Call / WhatsApp / Maps / email links present', links.tel>3&&links.wa>0&&links.maps>0&&links.mail>0, JSON.stringify(links));
  // marquee
  const m1=await p.evaluate(()=>getComputedStyle(document.querySelector('.bb-marquee-track')).transform); await p.waitForTimeout(500);
  const m2=await p.evaluate(()=>getComputedStyle(document.querySelector('.bb-marquee-track')).transform);
  ok('Supplier logo marquee moving', m1!==m2);
  const imgs=await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}return [...document.images].filter(i=>i.offsetParent&&(!i.complete||i.naturalWidth===0)).map(i=>i.src.split('/').pop())});
  ok('All visible images load', imgs.length===0, imgs.join(','));
  const webp=await p.evaluate(()=>[...document.images].map(i=>i.currentSrc||i.src).filter(s=>s.includes('/uploads/')&&!s.endsWith('.webp')));
  ok('All uploaded images are WebP', webp.length===0, webp.slice(0,3).join(','));
  await ctx.close();
  // ---------- mobile
  ctx = await b.newContext({ viewport: { width: 390, height: 844 }, ignoreHTTPSErrors: true, isMobile:true, hasTouch:true });
  p = await ctx.newPage(); await p.goto(URL, { waitUntil: 'networkidle' });
  await p.click('.bb-mmenu .elementor-menu-toggle'); await p.waitForTimeout(600);
  const mm=await p.evaluate(()=>{const n=document.querySelector('.bb-mmenu nav.elementor-nav-menu--dropdown');return n&&getComputedStyle(n).display!=='none'&&n.getBoundingClientRect().height>100;});
  ok('Mobile menu opens', mm);
  await p.locator('.bb-mmenu nav.elementor-nav-menu--dropdown a:has-text("FAQ")').click(); await p.waitForTimeout(1500);
  const fy=await p.evaluate(()=>Math.abs(document.querySelector('#faq').getBoundingClientRect().top));
  ok('Mobile menu link scrolls to FAQ', fy<150, Math.round(fy)+'px');
  await p.evaluate(()=>scrollTo(0,0)); await p.click('.bb-mhero .bb-vbtn[data-slide="1"] a'); await p.waitForTimeout(800);
  const ms=await p.evaluate(()=>({pts:document.querySelector('.bb-mhero .bb-pts.is-active').dataset.slide,name:document.querySelector('.bb-mhero .bb-vname').textContent}));
  ok('Mobile hero vehicle switch + points', ms.pts==='1'&&ms.name==='Pickup truck', JSON.stringify(ms));
  await p.evaluate(()=>{sessionStorage.removeItem('busy-bee-winter-preview');scrollTo(0,1500)}); await p.waitForTimeout(1200);
  const mp=await p.evaluate(()=>[...document.querySelectorAll('.elementor-popup-modal')].some(m=>getComputedStyle(m).display!=='none'));
  ok('Winter popup does NOT auto-open on mobile (as design)', !mp);
  const ov=await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1);
  ok('No horizontal scroll on mobile', ov, await p.evaluate(()=>document.documentElement.scrollWidth+''));
  await ctx.close(); await b.close();
  console.log(res.join('\n'));
})();
