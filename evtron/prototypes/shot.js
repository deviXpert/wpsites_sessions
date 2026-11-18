const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const f of ['a-spec-sheet','b-showroom','c-guided']){
 for(const [m,vp] of [['desktop',{width:1440,height:900}],['mobile',{width:390,height:844}]]){
  const p=await b.newPage({viewport:vp,deviceScaleFactor:1});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+process.cwd()+'/'+f+'.html');await p.waitForTimeout(1500);
  const hs=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  await p.screenshot({path:`shots/${f}-${m}.png`,fullPage:true});console.log(f,m,'hscroll',hs,errs);await p.close();}}
await b.close();})();
