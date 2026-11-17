// usage: node overflow.js [widths...]  – checks every page for horizontal overflow
const { chromium } = require('playwright');
const pages = Object.keys(require('./pages.json')).map(s => s === 'home' ? '/' : `/${s}/`);
const widths = process.argv.slice(2).map(Number).filter(Boolean);
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  for (const w of widths.length ? widths : [360, 390, 768, 1024, 1440, 1920]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true, isMobile: w < 800, hasTouch: w < 800 });
    const p = await ctx.newPage();
    for (const path of pages) {
      await p.goto(process.env.WP_URL.replace(/\/$/, '') + path, { waitUntil: 'networkidle', timeout: 90000 });
      const r = await p.evaluate(() => {
        const vw = document.documentElement.clientWidth, sw = document.documentElement.scrollWidth;
        const bad = [];
        for (const e of document.querySelectorAll('body *')) {
          const rc = e.getBoundingClientRect();
          if (rc.width && rc.height && !e.closest('.elementor-nav-menu--dropdown[aria-hidden="true"]') && (rc.right > vw + 1 || rc.left < -1) && getComputedStyle(e).position !== 'fixed') {
            const inBad = bad.some(x => x.el.contains(e));
            if (!inBad) bad.push({ el: e, d: `${e.tagName.toLowerCase()}.${String(e.className).split(' ').slice(0, 3).join('.')} [${Math.round(rc.left)}→${Math.round(rc.right)}]` });
          }
        }
        return { vw, sw, bad: bad.slice(0, 6).map(x => x.d) };
      });
      const flag = r.sw > r.vw ? 'OVERFLOW' : (r.bad.length ? 'clipped' : 'ok');
      console.log(w, path, flag, r.sw > r.vw ? `${r.sw}>${r.vw}` : '', flag === 'ok' ? '' : r.bad.join(' | '));
    }
    await ctx.close();
  }
  await b.close();
})();
