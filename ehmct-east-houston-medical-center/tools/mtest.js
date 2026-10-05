const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();
const m=await b.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});await m.goto(process.argv[2]+"/?nc="+Date.now(),{waitUntil:"networkidle"});
await m.tap(".elementor-menu-toggle");await m.waitForTimeout(600);await m.screenshot({path:"qa/mm1.png"});
await m.tap(".elementor-nav-menu--dropdown .sub-arrow").catch(e=>console.log("no arrow"));await m.waitForTimeout(700);await m.screenshot({path:"qa/mm2.png"});
console.log(await m.evaluate(()=>{const d=document.querySelector("nav.elementor-nav-menu--dropdown");const r=d.getBoundingClientRect();return {top:r.top,h:r.height,sw:document.documentElement.scrollWidth,bodyScroll:document.body.scrollHeight}}));
await m.tap(".elementor-menu-toggle");await m.waitForTimeout(600);await m.screenshot({path:"qa/mm3.png"});
await b.close()})()
