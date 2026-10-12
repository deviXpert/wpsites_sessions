const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [w] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  const out = {};
  for (const [name,url,sel] of [['design','https://busy-bee-auto-repair-preview.mightycarp65.chatgpt.site/','main > section, main > div, footer'],
                                ['live','https://papayawhip-ostrich-717285.hostingersite.com/?nc='+Date.now(),'[data-elementor-type="wp-page"] > .e-con, footer.elementor-location-footer > .e-con, .elementor-location-footer > .e-con']]) {
    const ctx = await b.newContext({ viewport: { width: +w, height: 900 }, ignoreHTTPSErrors: true, reducedMotion: 'reduce' });
    await ctx.addInitScript(() => { try { sessionStorage.setItem('busy-bee-winter-preview','seen'); } catch(e){} });
    const p = await ctx.newPage();
    await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 500) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(50); }
    out[name] = await p.evaluate((sel) => [...document.querySelectorAll(sel)].filter(e=>e.offsetHeight>0).map(e => {const r=e.getBoundingClientRect(); return [(e.id||e.className.split(' ').find(c=>c.startsWith('bb-'))||e.tagName).slice(0,22), Math.round(r.top+scrollY), Math.round(r.height)];}), sel);
    await ctx.close();
  }
  const n=Math.max(out.design.length,out.live.length);
  for (let i=0;i<n;i++){const d=out.design[i]||['',0,0],l=out.live[i]||['',0,0];console.log(`${d[0].padEnd(24)} ${String(d[1]).padStart(6)} ${String(d[2]).padStart(5)} | ${l[0].padEnd(24)} ${String(l[1]).padStart(6)} ${String(l[2]).padStart(5)}  dh=${l[2]-d[2]}`);}
  await b.close();
})();
