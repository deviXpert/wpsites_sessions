const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  for (const w of (process.argv[3] || '1440,1920,1280,768,390').split(',').map(Number)) {
    const p = await (await b.newContext({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true })).newPage();
    await p.goto(process.env.WP_URL.replace(/\/$/, '') + process.argv[2], { waitUntil: 'networkidle' });
    console.log(w, JSON.stringify(await p.evaluate(() => {
      const L = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().left) : null; };
      return { topbar: L('header .elementor-icon-list-item'), logo: L('header .elementor-widget-image img'), eyebrow: L('.qw-hero p.elementor-heading-title'), h1: L('.qw-hero h1'),
               lead: L('.qw-hero .elementor-widget-text-editor'), btn: L('.qw-hero .elementor-button'), trust: L('.qw-hero .elementor-icon-list-item'),
               sec2: L('main section:nth-of-type(2) .elementor-heading-title, .elementor-location-single section:nth-of-type(2) h2'), footerLogo: L('footer .elementor-widget-image img') };
    })));
  }
  await b.close();
})();
