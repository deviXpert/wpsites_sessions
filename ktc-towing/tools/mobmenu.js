// usage: node mobmenu.js prefix [inject]  -> open off-canvas menu, expand Services (+ first group), screenshot
const {chromium}=require('playwright');const fs=require('fs');(async()=>{
const [pre,inject]=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844},isMobile:true,hasTouch:true});
await p.goto('https://ktctowing.ca/about-us/?nc='+Date.now(),{waitUntil:'networkidle',timeout:120000}).catch(e=>{});
if(inject){const code=fs.readFileSync('mega-menu.html','utf8');
  await p.evaluate(()=>document.querySelectorAll('style,script').forEach(n=>{if((n.textContent||'').includes('ktc-mega'))n.remove()}));

  const css=code.match(/<style>([\s\S]*?)<\/style>/)[1], js=code.match(/<script>([\s\S]*?)<\/script>/)[1];
  await p.addStyleTag({content:css}); await p.evaluate(js.replace("document.addEventListener('DOMContentLoaded', function () {","(function(){").replace(/\}\);\s*$/,'})();'));}
const info=await p.evaluate(()=>{const t=[...document.querySelectorAll('.elementskit-menu-hamburger,.elementskit-menu-toggler,[class*=hamburger]')].map(e=>e.className);return t});
console.log(info);
await p.tap('.elementskit-menu-hamburger').catch(e=>console.log('tap fail',e.message.slice(0,80)));await p.waitForTimeout(800);
await p.screenshot({path:`shots/${pre}_1.png`});
const svc=await p.$('#menu-item-144 > a'); const box=await svc.boundingBox(); console.log(box);
await p.tap('#menu-item-144 > a .elementskit-submenu-indicator').catch(async e=>{console.log('ind fail');await p.tap('#menu-item-144 > a').catch(()=>{})});
await p.waitForTimeout(800); await p.screenshot({path:`shots/${pre}_2.png`});
await p.evaluate(()=>{const d=document.querySelector('#menu-main');d.scrollTop=520;});await p.waitForTimeout(500);console.log(await p.evaluate(()=>[...document.querySelectorAll('.elementskit-menu-container, .elementskit-menu-container > ul, #ekit-submenu-144')].map(e=>[e.id||e.className.slice(0,40),e.scrollHeight,e.clientHeight,getComputedStyle(e).overflowY,getComputedStyle(e).height,getComputedStyle(e).maxHeight])));
await p.screenshot({path:`shots/${pre}_3.png`,fullPage:false});
console.log(p.url());
await b.close()})()
