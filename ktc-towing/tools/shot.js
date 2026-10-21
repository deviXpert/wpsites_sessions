// usage: node shot.js URL prefix  -> full-page desktop + mobile screenshots in shots/
const {chromium}=require('playwright');(async()=>{
const [url,pre]=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [n,w,h,m] of [['d',1440,900,false],['m',390,844,true]]){
 const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h},isMobile:m,hasTouch:m});
 await p.goto(url,{waitUntil:'networkidle',timeout:120000}).catch(e=>console.log(e.message));
 const H=await p.evaluate(()=>document.body.scrollHeight);
 for(let y=0;y<H;y+=600){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(150);}
 await p.waitForTimeout(1500);
 await p.screenshot({path:`shots/${pre}_${n}.png`,fullPage:true});
 console.log(n,H);
 await p.close();}
await b.close()})()
