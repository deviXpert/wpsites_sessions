const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  for (const w of [1440, 390]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, ignoreHTTPSErrors: true });
  await p.goto(process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } });
  await p.waitForTimeout(1500);
  console.log(w, 'invisible:', await p.evaluate(() => [...document.querySelectorAll('.elementor-invisible')].map(e => e.dataset.id + ':' + (e.dataset.settings||'').slice(0,80))));
  await p.addScriptTag({ content: fs.readFileSync(require.resolve('axe-core/axe.min.js'),'utf8') });
  const v = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a','wcag2aa'] })).violations.map(v => v.id + ': ' + v.nodes.map(n => n.target.join(' ') + ' => ' + (n.any[0]||{}).message).join(' || ')));
  console.log(v.join('\n'));
  await p.close(); }
  await b.close();
})();
