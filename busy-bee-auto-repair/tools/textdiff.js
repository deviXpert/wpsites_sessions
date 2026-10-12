// usage: node textdiff.js width designSel liveSel [threshold]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [w, dsel, lsel, th='2'] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY } });
  const res = {};
  for (const [name,url,sel] of [['d','https://busy-bee-auto-repair-preview.mightycarp65.chatgpt.site/',dsel],['l','https://papayawhip-ostrich-717285.hostingersite.com/?nc='+Date.now(),lsel]]) {
    const ctx = await b.newContext({ viewport: { width: +w, height: 900 }, ignoreHTTPSErrors: true, reducedMotion: 'reduce' });
    await ctx.addInitScript(() => { try { sessionStorage.setItem('busy-bee-winter-preview','seen'); } catch(e){} });
    const p = await ctx.newPage();
    await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 500) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(40); }
    await p.waitForTimeout(800);
    res[name] = await p.evaluate((sel) => {
      const root=document.querySelector(sel); if(!root) return null; const R=root.getBoundingClientRect();
      const out=[]; const seen={};
      const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
      while(walker.nextNode()){const t=walker.currentNode; const s=t.textContent.trim(); if(s.length<2) continue; const e=t.parentElement; if(!e.offsetParent && getComputedStyle(e).position!=='fixed') continue;
        const rg=document.createRange(); rg.selectNodeContents(t); const r=rg.getBoundingClientRect(); if(!r.width) continue;
        const cs=getComputedStyle(e); let k=s.slice(0,28); seen[k]=(seen[k]||0)+1; if(seen[k]>1)k+='#'+seen[k];
        out.push([k,Math.round(r.left-R.left),Math.round(r.top-R.top),Math.round(r.width),Math.round(r.height),cs.fontSize,cs.fontWeight,cs.lineHeight,cs.fontFamily.split(',')[0].replace(/"/g,'')]);}
      return {H:Math.round(R.height),W:Math.round(R.width),items:out};
    }, sel);
    await ctx.close();
  }
  if(!res.d||!res.l){console.log('missing',!!res.d,!!res.l);process.exit(0);}
  console.log('section H design',res.d.H,'live',res.l.H);
  const L={}; res.l.items.forEach(i=>L[i[0]]=i);
  for(const d of res.d.items){const l=L[d[0]]; if(!l){console.log('MISSING ',d[0]);continue;}
    const dx=l[1]-d[1],dy=l[2]-d[2],dw=l[3]-d[3],dh=l[4]-d[4]; const f=(d[5]!==l[5]||d[6]!==l[6]||d[8]!==l[8]);
    if(Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dw),Math.abs(dh))>=+th||f) console.log(`${d[0].padEnd(30)} d(${d[1]},${d[2]} ${d[3]}x${d[4]} ${d[5]}/${d[6]}/${d[7]} ${d[8]}) l(${l[1]},${l[2]} ${l[3]}x${l[4]} ${l[5]}/${l[6]}/${l[7]} ${l[8]}) Δ ${dx},${dy},${dw},${dh}`);}
  await b.close();
})();
