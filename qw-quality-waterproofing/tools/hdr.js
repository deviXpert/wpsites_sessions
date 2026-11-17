const { chromium, devices } = require('playwright');
(async () => {
  const S = process.argv[2]; const U = process.env.WP_URL.replace(/\/$/, '');
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  let p = await (await b.newContext({ viewport: { width: 1440, height: 700 }, ignoreHTTPSErrors: true })).newPage();
  await p.goto(U + '/', { waitUntil: 'networkidle' });
  await p.hover('header .elementor-nav-menu--main .menu-item-has-children > a'); await p.waitForTimeout(700);
  await p.screenshot({ path: S + '/hdr_d.png', clip: { x: 0, y: 0, width: 1440, height: 420 } });
  p = await (await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1, ignoreHTTPSErrors: true })).newPage();
  await p.goto(U + '/', { waitUntil: 'networkidle' }); await p.screenshot({ path: S + '/hdr_m.png', clip: { x: 0, y: 0, width: 390, height: 260 } });
  await p.click('.elementor-menu-toggle'); await p.waitForTimeout(800); await p.screenshot({ path: S + '/hdr_m2.png' });
  await b.close();
})();
