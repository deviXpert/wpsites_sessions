const {chromium,devices}=require('playwright');const D='/home/user/wpsites_sessions/evtron/qa/v3/';
(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}});
for(const [n,opt] of [['d',{viewport:{width:1440,height:900}}],['t',{viewport:{width:1024,height:1366}}],['m',{...devices['iPhone 13']}]]){
 const p=await b.newPage(opt);const L=[];p.on('pageerror',e=>L.push(e.message));
 await p.goto('https://evtron.co.uk/home-v3/?v='+Date.now(),{waitUntil:'networkidle'});await p.waitForTimeout(2000);
 if(n==='d'){await p.click('.v3-sw:nth-child(4)').catch(e=>L.push('click '+e.message));await p.waitForTimeout(300)}
 const secs=await p.evaluate(()=>[...document.querySelectorAll('main > section')].map(s=>({top:Math.round(s.getBoundingClientRect().top+scrollY),h:s.offsetHeight,t:((s.querySelector('h1,h2')||{}).textContent||'').trim().slice(0,30)})));
 for(let i=0;i<secs.length;i++){await p.evaluate(async(y)=>{for(let k=window.scrollY;k<=y;k+=300){window.scrollTo(0,k);await new Promise(r=>setTimeout(r,40))}window.scrollTo(0,y)},Math.max(0,secs[i].top-(i?80:0)));await p.waitForTimeout(900);await p.screenshot({path:D+`s${i}-${n}.png`})}
 const r=await p.evaluate(()=>({hs:document.documentElement.scrollWidth>innerWidth,sw:document.querySelector('.v3-sw[aria-checked=true]')?.getAttribute('aria-label'),bar:document.querySelector('.v3-bar')?.className,over:[...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,3).map(e=>e.className.toString().slice(0,40))}));
 console.log(n,JSON.stringify(secs.map(s=>s.h+':'+s.t)),JSON.stringify(r),L);await p.close()}
await b.close()})();
