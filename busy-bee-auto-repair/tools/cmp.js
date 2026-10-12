// usage: node cmp.js url out.png width [fullpage:0/1] [waitms]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [url, out, w, full='1', wait='1500'] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  const ctx = await b.newContext({ viewport: { width: +w, height: 900 }, ignoreHTTPSErrors: true, reducedMotion: 'reduce' });
  await ctx.addInitScript(() => { try { sessionStorage.setItem('busy-bee-winter-preview','seen'); sessionStorage.setItem('bb-popup-seen','1'); } catch(e){} });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
  if (full === '1') {
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 400) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(80); }
    await p.evaluate(() => scrollTo(0, 0));
  }
  await p.waitForTimeout(+wait);
  await p.screenshot({ path: out, fullPage: full === '1' });
  await b.close();
})();
