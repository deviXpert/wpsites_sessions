// QA for the EV-Tron product page: layout shots + configurator behaviour (no form submission). Usage: node product.js [outdir]
const { chromium, devices } = require('playwright');
const out = process.argv[2] || 'product';
const URL = process.env.PP_URL || 'https://evtron.co.uk/product/evtron-tethered-ev-charger/';
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  for (const [n, opt] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
    const p = await b.newPage(opt); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL + '?v=' + Date.now(), { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
    await p.screenshot({ path: `${out}/p-${n}-1hero.png` });
    const pageH = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let s = 0; s < pageH; s += 500) { await p.evaluate(v => window.scrollTo(0, v), s); await p.waitForTimeout(40); }
    // configurator: pick Space Grey, 10m, 5-year, CT clamp + black post, then steel post (should replace black)
    const click = async t => p.evaluate(t => { const o = [...document.querySelectorAll('.pp-opt')].find(x => x.querySelector('p').textContent.trim() === t); o.click(); }, t);
    for (const t of ['Space Grey', '10 metres', '5-year warranty', 'CT clamp', 'Black charging post', 'Steel charging post']) await click(t);
    const st = await p.evaluate(() => ({
      on: [...document.querySelectorAll('.pp-opt.on')].map(o => o.querySelector('p').textContent.trim()),
      total: [...document.querySelectorAll('.pp-summary p')].map(x => x.textContent.trim()).find(t => /^£/.test(t)),
      sel: (document.getElementById('pp-selection') || {}).value,
      img: [...document.querySelectorAll('.pp-stage')].map(s => [...s.querySelectorAll('img')].findIndex(i => i.classList.contains('on'))),
      colour: [...document.querySelectorAll('main p')].map(x => x.textContent.trim()).find(t => /^(Mythos Black|Space Grey|Midnight Green|Crimson Red)$/.test(t)),
      detailsHidden: getComputedStyle(document.querySelector('.pp-details')).display === 'none',
      hscroll: document.documentElement.scrollWidth > innerWidth,
    }));
    console.log(n, JSON.stringify(st), errs.slice(0, 3));
    await p.evaluate(() => document.getElementById('configure').scrollIntoView()); await p.waitForTimeout(600);
    await p.screenshot({ path: `${out}/p-${n}-2config.png` });
    await p.evaluate(() => [...document.querySelectorAll('a')].find(a => /Continue to details/.test(a.textContent)).click()); await p.waitForTimeout(1500);
    console.log(n, 'details open', await p.evaluate(() => getComputedStyle(document.querySelector('.pp-details')).display !== 'none'), 'focused', await p.evaluate(() => document.activeElement && document.activeElement.id));
    await p.screenshot({ path: `${out}/p-${n}-3details.png` });
    for (const [lbl, t] of [['4features', 'Smart where it matters'], ['5specs', 'The technical detail'], ['6install', 'What a standard installation covers'], ['7faq', 'Good questions']]) {
      await p.evaluate(t => { const h = [...document.querySelectorAll('main h2')].find(x => x.textContent.includes(t)); h.closest('section').scrollIntoView(); }, t); await p.waitForTimeout(600);
      await p.screenshot({ path: `${out}/p-${n}-${lbl}.png` });
    }
    await p.close();
  }
  await b.close();
})();
