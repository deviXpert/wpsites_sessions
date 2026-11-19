// Renders src/*.html to print-ready PDFs, plus PNG previews with --png. Usage: node render.js [--png]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const docs = [
  ['user-manual', 'EV-Tron-User-Manual-EMS3-70-C.pdf'],
  ['app-guide', 'EV-Tron-App-Guide.pdf'],
];

(async () => {
  const browser = await chromium.launch();
  const png = process.argv.includes('--png');
  for (const [src, out] of docs) {
    const file = path.join(__dirname, 'src', src + '.html');
    if (!fs.existsSync(file)) continue;
    const page = await browser.newPage();
    await page.goto('file://' + file, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(__dirname, out), preferCSSPageSize: true, printBackground: true });
    const pages = await page.$$('.page');
    if (png) {
      const dir = path.join(__dirname, 'preview');
      fs.mkdirSync(dir, { recursive: true });
      for (let i = 0; i < pages.length; i++) {
        await pages[i].screenshot({ path: path.join(dir, `${src}-${String(i + 1).padStart(2, '0')}.png`) });
      }
    }
    console.log(out, pages.length, 'pages');
    await page.close();
  }
  await browser.close();
})();
