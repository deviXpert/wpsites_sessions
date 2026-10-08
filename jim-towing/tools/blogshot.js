const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [u,n] of [['/blog/','blog'],['/what-to-do-while-waiting-for-a-tow-calgary/','post']]) for(const [w,h,t] of [[1440,900,'d'],[390,844,'m']]){
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});
await p.goto('https://jimtowing.ca'+u+'?nc='+Date.now(),{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(60)}
await p.evaluate(()=>{scrollTo(0,0);document.querySelectorAll('.rv').forEach(e=>e.classList.add('is-in'));document.querySelectorAll('.j-header').forEach(e=>e.style.position='absolute');document.querySelectorAll('.j-fab,.j-mbar,.j-totop').forEach(e=>e.style.display='none')});await p.waitForTimeout(1200);
await p.screenshot({path:`../shots/${n}_${t}.jpg`,type:'jpeg',quality:50,fullPage:true});
console.log(n,t,await p.evaluate(()=>({h1:[...document.querySelectorAll('h1')].map(e=>e.textContent.trim()),cards:document.querySelectorAll('.elementor-post').length,sw:document.documentElement.scrollWidth,title:document.title})));await p.close()}
await b.close()})()
