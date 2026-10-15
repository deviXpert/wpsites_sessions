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
  // Trustindex Google reviews + desktop mega menu
  await p.locator('.bb-trustindex').scrollIntoViewIfNeeded(); await p.waitForTimeout(2500);
  const ti=await p.evaluate(()=>{const e=document.querySelector('.bb-trustindex');return e?e.innerText.includes('Google reviews'):false;});
  ok('Trustindex Google reviews widget renders', ti);
  await p.evaluate(()=>scrollTo(0,0)); await p.locator('.bb-mega-home:not(.bb-mmenu) .e-n-menu-title',{hasText:'Services'}).first().hover(); await p.waitForTimeout(800);
  const mega=await p.evaluate(()=>[...document.querySelectorAll('.bb-mega-home:not(.bb-mmenu) .bb-mega-link')].filter(a=>a.getBoundingClientRect().height>0).map(a=>a.getAttribute('href')));
  ok('Mega menu lists the 11 service pages', mega.length===11, mega.slice(0,3).join(','));
  await p.mouse.move(5,600);
  // FAQ toggle
  await p.locator('.bb-faq .elementor-tab-title').nth(1).scrollIntoViewIfNeeded();
  await p.locator('.bb-faq .elementor-tab-title').nth(1).click(); await p.waitForTimeout(600);
  const faqOpen=await p.evaluate(()=>{const c=document.querySelectorAll('.bb-faq .elementor-tab-content')[1];return getComputedStyle(c).display!=='none' && c.textContent.trim();});
  ok('FAQ question opens', !!faqOpen, faqOpen||'');
  await p.locator('.bb-faq .elementor-tab-title').nth(2).click(); await p.waitForTimeout(700);
  const openCount=await p.evaluate(()=>[...document.querySelectorAll('.bb-faq .elementor-tab-content')].filter(c=>getComputedStyle(c).display!=='none').length);
  ok('FAQ accordion keeps one answer open', openCount===1, openCount+' open');
  const schema=await p.evaluate(()=>[...document.querySelectorAll('script[type="application/ld+json"]')].some(s=>s.textContent.includes('FAQPage')));
  ok('FAQ schema (FAQPage JSON-LD) present', schema);
  // booking popup
  await p.evaluate(()=>scrollTo(0,0)); await p.locator('a.elementor-button:visible',{hasText:/Book an Appointment/i}).first().click(); await p.waitForTimeout(900);
  ok('Book an Appointment opens booking popup', await p.locator('#elementor-popup-modal-347').isVisible());
  await p.keyboard.press('Escape'); await p.waitForTimeout(500);
  // symptom checker
  await p.selectOption('[name="form_fields[make]"]','Toyota'); await p.selectOption('[name="form_fields[model]"]','Toyota Camry'); await p.selectOption('[name="form_fields[year]"]','2019'); await p.fill('[name="form_fields[mileage]"]','120000');
  await p.waitForTimeout(2500);
  ok('Symptom checker shows selected car', await p.$eval('.bb-veh-img img',i=>i.src.includes('modelFamily=camry')&&i.naturalWidth>0));
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
  const links=await p.evaluate(()=>{const a=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));return {tel:a.filter(h=>h.startsWith('tel:')).length, wa:a.filter(h=>h.includes('wa.me')).length, maps:a.filter(h=>h.includes('google.com/maps')).length, mail:a.filter(h=>h.startsWith('mailto:')).length, empty:a.filter(h=>h==='#'||h==='').length}});
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
  await p.click('.bb-mmenu .e-n-menu-toggle'); await p.waitForTimeout(700);
  const mm=await p.evaluate(()=>{const n=document.querySelector('.bb-mmenu .e-n-menu-wrapper');return !!n&&n.getBoundingClientRect().height>150;});
  ok('Mobile menu opens', mm);
  await p.locator('.bb-mmenu .e-n-menu-title-container',{hasText:'Contact'}).click(); await p.waitForLoadState('domcontentloaded'); await p.waitForTimeout(800);
  ok('Mobile menu link opens Contact page', p.url().includes('/contact-us/'), p.url());
  await p.goto(URL, { waitUntil: 'networkidle' });
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
