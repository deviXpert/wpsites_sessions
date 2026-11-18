const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}});
for(const [n,opt] of [['desktop',{viewport:{width:1440,height:900},deviceScaleFactor:2}],['laptop',{viewport:{width:1280,height:800},deviceScaleFactor:1}],['tablet',{viewport:{width:1024,height:1366},deviceScaleFactor:1}],['mobile',{...devices['iPhone 13']}]]){
 const p=await b.newPage(opt);const L=[];p.on('pageerror',e=>L.push(e.message));
 await p.goto('https://evtron.co.uk/home-v2/?v='+Date.now(),{waitUntil:'networkidle'});await p.waitForTimeout(3200);
 const r=await p.evaluate(()=>({hs:document.documentElement.scrollWidth>innerWidth,over:[...document.querySelectorAll('.v2-hero *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1&&!e.closest('.v2-aurora')&&!e.closest('.v2-beam')}).slice(0,4).map(e=>e.className.toString().slice(0,50)),hdr:Math.round(document.querySelector('header.elementor-element').getBoundingClientRect().top),heroH:Math.round(document.querySelector('.v2-hero').getBoundingClientRect().height),bf:getComputedStyle(document.querySelector('header.elementor-element')).backdropFilter}));
 console.log(n,JSON.stringify(r),L.slice(0,3));await p.screenshot({path:`v2/hero-${n}.png`});
 if(n==='desktop'){await p.mouse.move(1200,300);await p.waitForTimeout(900);await p.screenshot({path:'v2/hero-desktop-parallax.png'});await p.hover('.elementor-nav-menu--main .menu-item-has-children > a');await p.waitForTimeout(600);await p.screenshot({path:'v2/hero-desktop-dropdown.png',clip:{x:0,y:0,width:1440,height:500}});
   await p.evaluate(()=>window.scrollTo(0,700));await p.waitForTimeout(900);await p.screenshot({path:'v2/hero-desktop-scrolled.png'})}
 await p.close()}
await b.close()})();
