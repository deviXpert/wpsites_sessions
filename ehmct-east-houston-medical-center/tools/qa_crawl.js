const {chromium}=require("playwright");const fs=require("fs");
(async()=>{const pages=JSON.parse(fs.readFileSync("pages.json")).map(p=>p.link);
const b=await chromium.launch();const report={};const links=new Map();
for(const url of pages){const slug=url.replace(/https?:\/\/[^/]+/,"").replace(/\//g,"")||"home";report[slug]={};
 for(const w of [1440,1024,393]){const p=await b.newPage({viewport:{width:w,height:900}});const errs=[];const bad=[];
  p.on("pageerror",e=>errs.push(e.message.slice(0,120)));
  p.on("response",r=>{if(r.status()>=400&&!/google|gstatic|facebook|doubleclick|trustindex/.test(r.url()))bad.push(r.status()+" "+r.url().slice(0,110))});
  try{await p.goto(url+"?qa="+Date.now(),{waitUntil:"networkidle",timeout:90000})}catch(e){errs.push("goto "+e.message.slice(0,80))}
  for(let y=0;y<16000;y+=700){await p.evaluate(v=>scrollTo(0,v),y);await p.waitForTimeout(100)}await p.waitForTimeout(1200);await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(300);
  const r=await p.evaluate((w)=>{const out={sw:document.documentElement.scrollWidth,h:document.body.scrollHeight,over:[],brokenImg:[],emptyLinks:[],links:[],smallTap:0,tinyText:[]};
   document.querySelectorAll("body *").forEach(e=>{if(!e.offsetParent&&getComputedStyle(e).position!="fixed")return;const b=e.getBoundingClientRect();if(b.width>0&&b.right>w+1&&!e.closest(".swiper,.e-n-carousel,.elementor-nav-menu--dropdown,[aria-hidden=true]")){out.over.push((e.className&&e.className.baseVal===undefined?String(e.className).slice(0,60):e.tagName)+" r="+Math.round(b.right))}});
   document.querySelectorAll("img").forEach(i=>{if(i.complete&&i.naturalWidth===0&&i.offsetParent)out.brokenImg.push(i.src.slice(0,100))});
   document.querySelectorAll("a").forEach(a=>{const h=a.getAttribute("href");if(!a.offsetParent)return;const t=(a.textContent||a.getAttribute("aria-label")||"").trim().slice(0,40);if(h===null||h===""||h==="#")out.emptyLinks.push(t+" ["+h+"]");else out.links.push([h,t])});
   return out},w);
  if(w===1440)await p.screenshot({path:`${slug}_1440.png`,fullPage:true});if(w===393)await p.screenshot({path:`${slug}_393.png`,fullPage:true});
  r.links.forEach(([h,t])=>{if(!links.has(h))links.set(h,new Set());links.get(h).add(slug)});
  report[slug][w]={sw:r.sw,h:r.h,over:[...new Set(r.over)].slice(0,6),brokenImg:r.brokenImg,emptyLinks:[...new Set(r.emptyLinks)],errs,bad:[...new Set(bad)].slice(0,8)};
  await p.close()}}
fs.writeFileSync("report.json",JSON.stringify(report,null,1));fs.writeFileSync("links.json",JSON.stringify([...links].map(([h,s])=>[h,[...s]])));await b.close()})()
