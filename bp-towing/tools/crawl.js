const {chromium}=require('playwright');const fs=require('fs');
const urls=JSON.parse(fs.readFileSync('dump/urls.json'));
(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}});
const out={};const links=new Set();
for(const vp of [['m',390,844],['d',1440,900]]){
const c=await b.newContext({viewport:{width:vp[1],height:vp[2]},isMobile:vp[0]=='m',hasTouch:vp[0]=='m',ignoreHTTPSErrors:true});
for(const u of urls){const p=await c.newPage();const errs=[];
p.on('pageerror',e=>errs.push('JS:'+e.message.slice(0,150)));
p.on('response',r=>{if(r.status()>=400&&!/google|facebook|doubleclick|gstatic/.test(r.url()))errs.push(r.status()+' '+r.url().slice(0,150))});
let st;try{const r=await p.goto(u,{waitUntil:'networkidle',timeout:60000});st=r.status()}catch(e){st='ERR '+e.message.slice(0,80)}
await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}});await p.waitForTimeout(500);
const info=await p.evaluate(()=>{const W=document.documentElement.clientWidth;const wide=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>W+2&&getComputedStyle(e).position!='fixed'&&!e.closest('.swiper,.bp-tk,[class*=marquee],.elementor-nav-menu--dropdown,.bp-mpanel'))wide.push((e.className||e.tagName).toString().slice(0,50)+' r='+Math.round(r.right))});
const imgs=[...document.images].filter(i=>i.complete&&i.naturalWidth==0&&i.src).map(i=>i.src.slice(0,120));
const noalt=[...document.images].filter(i=>!i.hasAttribute('alt')).length;
const h1=document.querySelectorAll('h1').length;
const t=document.body.innerText;const dd=t.split('\n').filter(l=>/--|—|–/.test(l)).map(l=>l.slice(0,140));
const as=[...document.querySelectorAll('a[href]')].map(a=>a.href);
const empty=[...document.querySelectorAll('a')].filter(a=>{const h=a.getAttribute('href');return !h||h=='#'}).map(a=>(a.innerText||a.className).slice(0,40));
return {sw:document.documentElement.scrollWidth,W,wide:wide.slice(0,6),imgs,noalt,h1,dd,as,empty:empty.slice(0,10),title:document.title}});
info.as.forEach(a=>links.add(a));delete info.as;
out[vp[0]+' '+u]={st,errs:[...new Set(errs)].slice(0,10),...info};
if(vp[0]=='m')await p.screenshot({path:'shots/'+u.slice(27).replace(/\W+/g,'_')+'.png',fullPage:true}).catch(()=>{});
await p.close()}
await c.close()}
fs.writeFileSync('dump/crawl.json',JSON.stringify(out,null,1));fs.writeFileSync('dump/links.json',JSON.stringify([...links]));await b.close()})();
