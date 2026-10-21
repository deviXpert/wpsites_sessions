// usage: node megatest.js URL prefix [inject]  -> hover Services and screenshot (desktop 1440 + 1100) + mobile menu
const {chromium}=require('playwright');const fs=require('fs');(async()=>{
const [url,pre,inject]=process.argv.slice(2);
const code=fs.readFileSync('mega-menu.html','utf8');
const css=code.match(/<style>([\s\S]*?)<\/style>/)[1], js=code.match(/<script>([\s\S]*?)<\/script>/)[1];
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [n,w,h] of [['d',1440,900],['s',1100,800]]){
 const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});
 await p.goto(url,{waitUntil:'networkidle',timeout:120000}).catch(e=>{});
 if(inject){await p.addStyleTag({content:css}); await p.evaluate(js.replace("document.addEventListener('DOMContentLoaded', function () {","(function(){").replace(/\}\);\s*$/,'})();'));}
 await p.hover('#menu-item-144 > a'); await p.waitForTimeout(900);
 await p.screenshot({path:`shots/${pre}_${n}.png`,clip:{x:0,y:0,width:w,height:620}});
 await p.close();}
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844},isMobile:true,hasTouch:true});
await p.goto(url,{waitUntil:'networkidle',timeout:120000}).catch(e=>{});
if(inject){await p.addStyleTag({content:css}); await p.evaluate(js.replace("document.addEventListener('DOMContentLoaded', function () {","(function(){").replace(/\}\);\s*$/,'})();'));}
await p.click('.elementskit-menu-hamburger').catch(e=>console.log('no burger'));await p.waitForTimeout(700);
await p.click('#menu-item-144 > a .elementskit-submenu-indicator').catch(e=>console.log('no ind'));await p.waitForTimeout(700);
await p.screenshot({path:`shots/${pre}_m.png`});
await b.close()})()
