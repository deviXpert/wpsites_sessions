const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const slug of process.argv.slice(2)){for(const [n,w,h] of [['d',1440,900],['m',390,844]]){
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,80)));
await p.goto('https://bptowingservice.ca/'+slug+'/?nc='+Date.now(),{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
await p.evaluate(async()=>{document.documentElement.style.scrollBehavior='auto';for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,90))}});await p.waitForTimeout(800);
const r=await p.evaluate(()=>{const o={};const W=innerWidth;
o.hscroll=document.documentElement.scrollWidth>W+1?document.documentElement.scrollWidth:0;
o.collapsed=[...document.querySelectorAll('.bp .elementor-widget')].filter(e=>{const t=e.innerText.trim();const r=e.getBoundingClientRect();return t.length>20&&r.width>0&&r.width<80}).map(e=>e.innerText.trim().slice(0,30));
o.overflowX=[...document.querySelectorAll('.bp .elementor-widget, .bp .e-con')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>W+2||r.left<-2)&&!e.closest('.bp-tk,.swiper,.bp-ticker,.bp-mpanel,.elementor-nav-menu--dropdown')}).map(e=>(e.className||'').toString().slice(0,50)+' '+Math.round(e.getBoundingClientRect().left)+'..'+Math.round(e.getBoundingClientRect().right)).slice(0,5);
o.brokenImg=[...document.querySelectorAll('.bp img')].filter(i=>i.complete&&i.naturalWidth===0&&!i.closest('.swiper-slide-duplicate')).map(i=>i.src.split('/').pop()).slice(0,5);
o.noAlt=[...document.querySelectorAll('.bp img')].filter(i=>!i.alt).map(i=>i.src.split('/').pop()).slice(0,8);
o.olMarkers=[...document.querySelectorAll('.bp ol>li')].filter(li=>getComputedStyle(li).listStyleType!=='none').length;
o.gaps=[...document.querySelectorAll('.bp-split')].map(s=>{const k=[...s.querySelectorAll(':scope>.e-con-inner>.e-con')];if(k.length<2)return null;const hs=k.map(x=>x.getBoundingClientRect().height);return Math.round(Math.max(...hs)-Math.min(...hs))}).filter(x=>x>250);
o.lorem=document.body.innerText.includes('Lorem ipsum');return o});
console.log(slug.slice(0,22).padEnd(22),n,JSON.stringify(r),errs.length?'JSERR:'+errs[0]:'');await p.close()}}await b.close()})()
