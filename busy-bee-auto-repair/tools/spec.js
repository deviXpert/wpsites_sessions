// usage: node spec.js url width out  -> element spec dump (text, boxes, type, colours, backgrounds)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [url, w, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: +w, height: 900 }, reducedMotion: 'reduce' });
  await ctx.addInitScript(() => { try { sessionStorage.setItem('busy-bee-winter-preview','seen'); } catch(e){} });
  const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle', timeout: 120000 });
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 700) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(40); }
  await p.evaluate(() => scrollTo(0, 0));
  const r = await p.evaluate(() => {
    const L = [];
    for (const e of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(e), r = e.getBoundingClientRect();
      if (!r.width || cs.display === 'none' || cs.visibility === 'hidden' || ['SCRIPT','STYLE','PATH','CIRCLE','RECT','LINE','POLYLINE'].includes(e.tagName.toUpperCase())) continue;
      const txt = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
      const bgI = cs.backgroundImage !== 'none' ? cs.backgroundImage.slice(0, 120) : '';
      const bgC = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' ? cs.backgroundColor : '';
      const bd = cs.borderTopWidth !== '0px' || cs.borderBottomWidth !== '0px' || cs.borderLeftWidth !== '0px' ? `bd=${cs.borderTopWidth}/${cs.borderRightWidth}/${cs.borderBottomWidth}/${cs.borderLeftWidth} ${cs.borderTopColor}` : '';
      const img = e.tagName === 'IMG' ? 'img=' + e.getAttribute('src') + ' fit=' + cs.objectFit + ' pos=' + cs.objectPosition : '';
      if (!txt && !bgI && !bgC && !bd && !img && e.tagName !== 'svg' && e.tagName !== 'INPUT' && e.tagName !== 'SELECT' && e.tagName !== 'TEXTAREA') continue;
      const box = `[${Math.round(r.left)},${Math.round(r.top + scrollY)} ${Math.round(r.width)}x${Math.round(r.height)}]`;
      const type = txt ? `fs=${cs.fontSize} fw=${cs.fontWeight} lh=${cs.lineHeight} ls=${cs.letterSpacing} tt=${cs.textTransform} c=${cs.color} ff=${cs.fontFamily.split(',')[0]}` : '';
      const misc = `${cs.borderRadius !== '0px' ? 'rad=' + cs.borderRadius : ''} ${cs.boxShadow !== 'none' ? 'sh=' + cs.boxShadow.slice(0, 60) : ''} ${cs.opacity !== '1' ? 'op=' + cs.opacity : ''} pad=${cs.padding}`;
      L.push(`${e.tagName.toLowerCase()} ${box} ${txt ? JSON.stringify(txt.slice(0, 70)) : ''} ${type} ${bgC ? 'bg=' + bgC : ''} ${bgI ? 'bgi=' + bgI : ''} ${bd} ${img} ${misc}`.replace(/\s+/g, ' '));
    }
    return L.join('\n');
  });
  require('fs').writeFileSync(out, r); console.log(out, r.split('\n').length); await b.close();
})();
