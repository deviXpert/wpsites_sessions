const {chromium}=require('playwright');(async()=>{
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:400,height:786},isMobile:true,hasTouch:true});
await p.goto('https://ktctowing.ca/?nc=7',{waitUntil:'networkidle',timeout:120000}).catch(e=>{});
const r=await p.evaluate(()=>{const o={sw:document.documentElement.scrollWidth};
 const wide=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>401&&r.width>0&&getComputedStyle(e).position!=='fixed'}).slice(0,15).map(e=>e.className.toString().slice(0,60)+' '+Math.round(e.getBoundingClientRect().right));
 o.wide=wide; const m=document.querySelector('.elementor-element-447526f').getBoundingClientRect(); o.marq=[m.top+scrollY,m.height];
 const h=document.querySelector('.elementor-element-678e4f8').getBoundingClientRect(); o.hero=[h.top+scrollY,h.height];
 const a=document.querySelector('.elementor-element-c0c4479').getBoundingClientRect(); o.about=[a.top+scrollY];return o});
console.log(JSON.stringify(r,null,1));
await p.evaluate(()=>scrollTo(0,document.querySelector('.elementor-element-447526f').getBoundingClientRect().top+scrollY-400));
await p.waitForTimeout(800); await p.screenshot({path:'shots/probe_m.png'});
await b.close()})()
