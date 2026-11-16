// usage: node shot.js <path> <out.png> [mobile]
const { chromium, devices } = require('playwright');
(async () => {
  const [, , path, out, mob] = process.argv;
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  const ctx = await b.newContext(mob ? { ...devices['iPhone 13'], deviceScaleFactor: 1, ignoreHTTPSErrors: true } : { viewport: { width: 1440, height: 900 }, ignoreHTTPSErrors: true });
  const p = await ctx.newPage();
  const url = process.env.WP_URL.replace(/\/$/, '') + path;
  await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 350) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 300)); } window.scrollTo(0, 0); });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out, fullPage: true });
  console.log(await p.title(), await p.evaluate(() => document.body.scrollHeight));
  await b.close();
})();
