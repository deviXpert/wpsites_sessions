// usage: node elshot.js URL prefix sel1 sel2 ... -> element screenshots (last match of each selector) desktop+mobile
const {chromium}=require('playwright');(async()=>{
const [url,pre,...sels]=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [n,w,h,m] of [['d',1440,900,false],['m',390,844,true]]){
 const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h},isMobile:m,hasTouch:m});
 await p.goto(url,{waitUntil:'networkidle',timeout:120000}).catch(e=>console.log(e.message));
 const H=await p.evaluate(()=>document.body.scrollHeight);
 for(let y=0;y<H;y+=700){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(100);}
 for(const [k,s] of sels.entries()){const els=await p.$$(s.startsWith("#id:")?`[data-id="${s.slice(4)}"]`:s); if(!els.length){console.log('none',s);continue;}
   const el=els[els.length-1]; await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
   await el.screenshot({path:`shots/${pre}_${k}_${n}.png`});}
 await p.close();}
await b.close()})()
