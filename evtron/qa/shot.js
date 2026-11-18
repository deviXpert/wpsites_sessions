const {chromium}=require('playwright');
const [,,url,name]=process.argv;
(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}});
for(const [m,vp] of [['desktop',{width:1440,height:900}],['mobile',{width:390,height:844}]]){
 const p=await b.newPage({viewport:vp,ignoreHTTPSErrors:true});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',c=>{if(c.type()==='error')errs.push(c.text().slice(0,160))});
 await p.goto(url,{waitUntil:'networkidle',timeout:60000}).catch(e=>errs.push(String(e).slice(0,100)));await p.waitForTimeout(1000);
 const info=await p.evaluate(()=>({hs:document.documentElement.scrollWidth>innerWidth,bg:getComputedStyle(document.body).backgroundColor,fonts:[...new Set([...document.querySelectorAll('h1,p')].map(e=>getComputedStyle(e).fontFamily.split(',')[0]))],loaded:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight)}));
 await p.screenshot({path:`shots/${name}-${m}.png`,fullPage:true});console.log(name,m,JSON.stringify(info),errs.slice(0,5));await p.close();}
await b.close();})();
