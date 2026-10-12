// usage: node probe.js url width selector  -> prints tree of boxes under selector (depth 4)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [url, w, sel, depth='4'] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  const ctx = await b.newContext({ viewport: { width: +w, height: 900 }, ignoreHTTPSErrors: true, reducedMotion: 'reduce' });
  await ctx.addInitScript(() => { try { sessionStorage.setItem('busy-bee-winter-preview','seen'); } catch(e){} });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
  const r = await p.evaluate(([sel,depth]) => {
    const root=document.querySelector(sel); if(!root) return 'no root'; const R=root.getBoundingClientRect(); const out=[];
    (function walk(e,d){ if(d>depth) return; const r=e.getBoundingClientRect(); const cs=getComputedStyle(e);
      out.push('  '.repeat(d)+`${e.tagName.toLowerCase()}.${(e.className+'').replace(/elementor-element-[a-z0-9]+|e-con-full|e-flex|e-con|elementor-element|e-child|e-parent|elementor-widget/g,'').trim().slice(0,60)} [${Math.round(r.left-R.left)},${Math.round(r.top-R.top)} ${Math.round(r.width)}x${Math.round(r.height)}] pad=${cs.padding} mar=${cs.margin} lh=${cs.lineHeight} fs=${cs.fontSize}`);
      for(const c of e.children) walk(c,d+1);})(root,0);
    return out.join('\n');
  }, [sel,+depth]);
  console.log(r); await b.close();
})();
