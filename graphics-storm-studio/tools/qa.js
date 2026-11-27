// Visual + responsive QA: node qa.js <outdir> <url>...  (screens at 1440/1024/768/390, overflow + contrast via axe)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const axe = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
  const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
  for (const url of urls) {
    const name = url.split('/').filter(Boolean).pop();
    for (const w of [1440, 1024, 768, 390]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true });
      await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 }).catch(e => console.log('goto', e.message));
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
      await p.waitForTimeout(1500);
      const r = await p.evaluate(() => {
        const vw = document.documentElement.clientWidth, wide = [];
        document.querySelectorAll('body *').forEach(e => { const b = e.getBoundingClientRect(); if (b.right > vw + 1 && b.width > 0 && getComputedStyle(e).position !== 'fixed') wide.push((e.className || e.tagName).toString().slice(0, 60)); });
        return { overflow: document.documentElement.scrollWidth - vw, wide: wide.slice(0, 5), h1: document.querySelectorAll('h1').length,
                 small: [...document.querySelectorAll('p,li,a,span')].filter(e => e.offsetParent && parseFloat(getComputedStyle(e).fontSize) < 12).length };
      });
      let axeRes = '';
      if (w === 1440 || w === 390) {
        await p.addScriptTag({ content: axe });
        const a = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] })).violations.map(v => `${v.id}(${v.nodes.length})`));
        axeRes = ' axe:' + a.join(',');
      }
      console.log(`${name} @${w}: overflow=${r.overflow} h1=${r.h1} tiny-text=${r.small} ${r.wide.length ? 'WIDE:' + r.wide.join('|') : ''}${axeRes}`);
      await p.screenshot({ path: `${out}/${name}-${w}.png`, fullPage: true });
      await p.close();
    }
  }
  await b.close();
})();
