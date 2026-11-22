// Submits one clearly-marked test review through the real Site Reviews form in a browser
const { chromium } = require('playwright');
(async () => {
  const url = require('fs').readFileSync(process.argv[2], 'utf8').trim(); // signed preview URL of the draft Reviews page
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
  const p = await (await b.newContext({ viewport: { width: 1280, height: 900 }, ignoreHTTPSErrors: true })).newPage();
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.waitForTimeout(6000); // let the spam-timer elapse like a real visitor
  const f = p.locator('form.glsr-review-form').first();
  await f.locator('select[name="site-reviews[rating]"]').selectOption('5').catch(async () => { await f.locator('.glsr-star-rating span').last().click(); });
  await f.locator('[name="site-reviews[title]"]').fill('TEST – please delete');
  await f.locator('[name="site-reviews[content]"]').fill('Automated test of the website review form. Please ignore and delete.');
  await f.locator('[name="site-reviews[name]"]').fill('Website Test');
  await f.locator('[name="site-reviews[email]"]').fill('test@example.com');
  await f.locator('[name="site-reviews[terms]"]').check();
  await f.locator('button[type="submit"]').click();
  await p.waitForTimeout(5000);
  console.log('message:', (await p.locator('.glsr-form-message').first().innerText().catch(() => '(none)')).trim());
  await b.close();
})();
