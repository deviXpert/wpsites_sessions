// QA for the 19 Nov V2 changes: utility row, 3-colour hero, range, process. Usage: node v2changes.js [outdir]
const { chromium, devices } = require('playwright');
const out = process.argv[2] || 'v2';
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  for (const [n, opt] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['tablet', { viewport: { width: 1024, height: 1366 } }], ['mobile', { ...devices['iPhone 13'] }]]) {
    const p = await b.newPage(opt); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto('https://evtron.co.uk/?v=' + Date.now(), { waitUntil: 'networkidle' }); await p.waitForTimeout(2500);
    const r = await p.evaluate(() => ({
      hscroll: document.documentElement.scrollWidth > innerWidth,
      on: [...document.querySelectorAll('.v2-stack img')].map(i => i.classList.contains('on')),
      usps: [...document.querySelectorAll('.ev-usp')].filter(u => getComputedStyle(u).display !== 'none').length,
      stale: (document.body.innerText.match(/£1,295|fully installed|£945 installed/g) || []),
    }));
    console.log(n, JSON.stringify(r), errs.slice(0, 3));
    await p.screenshot({ path: `${out}/c-${n}-hero.png` });
    for (const [lbl, txt] of [['range', 'EV-Tron, plus solar-ready'], ['process', 'From order to first charge'], ['process2', 'Installed and ready']]) {
      const y = await p.evaluate(t => { const c = [...document.querySelectorAll('main h2, main h3')].find(x => x.textContent.includes(t)); return c ? c.getBoundingClientRect().top + scrollY - 200 : -1; }, txt);
      if (y < 0) { console.log('missing', txt); continue; }
      for (let s = 0; s <= y; s += 400) { await p.evaluate(v => window.scrollTo(0, v), s); await p.waitForTimeout(60); }
      await p.evaluate(v => window.scrollTo(0, v), y);
      await p.waitForTimeout(900);
      await p.screenshot({ path: `${out}/c-${n}-${lbl}.png`, fullPage: false });
    }
    if (n === 'desktop') { await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(3600); await p.screenshot({ path: `${out}/c-desktop-hero2.png`, clip: { x: 720, y: 80, width: 720, height: 760 } }); }
    await p.close();
  }
  await b.close();
})();
