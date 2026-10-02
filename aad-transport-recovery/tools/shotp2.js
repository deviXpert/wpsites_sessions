const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const only=process.argv[2];
for(const f of fs.readdirSync('prev').filter(f=>f.endsWith('.html')&&(!only||f.startsWith(only)))){for(const [n,w,h] of [['d',1440,1000],['m',390,844]]){
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});
await p.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='.rv{opacity:1!important;transform:none!important}';document.head.appendChild(s)})});
await p.goto('file://'+process.cwd()+'/prev/'+f,{waitUntil:'networkidle',timeout:90000}).catch(e=>{});
const H=await p.evaluate(()=>document.body.scrollHeight);let k=0;
for(let y=0;y<H;y+=h){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(350);await p.screenshot({path:`prev/${f.replace('.html','')}_${n}_${String(k++).padStart(2,'0')}.png`});}
await p.close();}}
await b.close()})()
