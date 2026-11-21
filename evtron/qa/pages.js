// QA for the site pages: status, console errors, horizontal overflow, full-page shots. Usage: node pages.js <outdir> [slug ...]
const { chromium, devices } = require('playwright');
const out = process.argv[2] || 'pages';
const slugs = process.argv.slice(3).length ? process.argv.slice(3) : ['installation', 'faqs', 'contact', 'warranty', 'ev-charger-grants', 'terms', 'privacy-policy', 'cookie-policy', 'cancellations-returns', 'about', 'basket'];
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  for (const [n, opt] of [['d', { viewport: { width: 1440, height: 900 } }], ['m', { ...devices['iPhone 13'] }]]) {
    for (const s of slugs) {
      const p = await b.newPage(opt); const errs = []; p.on('pageerror', e => errs.push(e.message));
      const r = await p.goto(`https://evtron.co.uk/${s}/?v=${Date.now()}`, { waitUntil: 'networkidle' });
      const H = await p.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += 450) { await p.evaluate(v => window.scrollTo(0, v), y); await p.waitForTimeout(40); }
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(1200);
      const info = await p.evaluate(() => ({ h: document.documentElement.scrollWidth > innerWidth, v2: document.documentElement.classList.contains('ev-v2'), forms: document.querySelectorAll('.v2-form').length, req: !!document.getElementById('request') }));
      console.log(n, s, r.status(), JSON.stringify(info), errs.slice(0, 2));
      await p.screenshot({ path: `${out}/${n}-${s}.png`, fullPage: true }); await p.close();
    }
  }
  await b.close();
})();
