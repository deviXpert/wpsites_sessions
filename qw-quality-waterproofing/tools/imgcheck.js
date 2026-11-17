// flags any <img> rendered at a different aspect ratio than its natural one without object-fit cover/contain
const { chromium } = require('playwright');
const pages = Object.keys(require('./pages.json')).map(s => s === 'home' ? '/' : `/${s}/`);
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  let bad = 0, total = 0;
  for (const w of [1440, 1024, 768, 390]) {
    const p = await (await b.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true })).newPage();
    for (const path of pages) {
      await p.goto(process.env.WP_URL.replace(/\/$/, '') + path, { waitUntil: 'networkidle', timeout: 90000 });
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } });
      await p.waitForTimeout(800);
      const r = await p.evaluate(() => [...document.images].filter(i => i.naturalWidth && i.getBoundingClientRect().width > 0).map(i => {
        const rc = i.getBoundingClientRect(), fit = getComputedStyle(i).objectFit;
        const dist = Math.abs((rc.width / rc.height) / (i.naturalWidth / i.naturalHeight) - 1);
        return { src: i.currentSrc.split('/').pop().slice(0, 50), fit, dist: +dist.toFixed(2) };
      }));
      total += r.length;
      for (const x of r) if (x.dist > 0.03 && !['cover', 'contain'].includes(x.fit)) { bad++; console.log(w, path, x.src, 'fit=' + x.fit, 'distortion=' + x.dist); }
    }
  }
  console.log('checked', total, 'image renders; distorted:', bad);
  await b.close();
})();
