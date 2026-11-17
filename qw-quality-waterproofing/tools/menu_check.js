const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  const U = process.env.WP_URL.replace(/\/$/, '');
  let p = await (await b.newContext({ viewport: { width: 1920, height: 1000 }, ignoreHTTPSErrors: true })).newPage();
  await p.goto(U + '/', { waitUntil: 'networkidle' });
  console.log('inner widths @1920:', await p.evaluate(() => [...new Set([...document.querySelectorAll('.e-con-boxed > .e-con-inner')].map(e => Math.round(e.getBoundingClientRect().width)))]));
  await p.screenshot({ path: process.argv[2] + '/w1920.png' });
  p = await (await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1, ignoreHTTPSErrors: true })).newPage();
  await p.goto(U + '/', { waitUntil: 'networkidle' });
  await p.click('.elementor-menu-toggle'); await p.waitForTimeout(800);
  const sub = await p.$('.elementor-nav-menu--dropdown .menu-item-has-children > a'); if (sub) { await sub.click(); await p.waitForTimeout(600); }
  console.log('open menu:', await p.evaluate(() => { const n = document.querySelector('.elementor-nav-menu--dropdown'); const r = n.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.right), document.documentElement.clientWidth, document.documentElement.scrollWidth]; }));
  await p.screenshot({ path: process.argv[2] + '/menu.png' });
  await b.close();
})();
