// node shot.js <url> <outprefix> [w] [h]  -> full-page screenshot split into chunks (after scrolling to trigger reveals)
const {chromium}=require('playwright');(async()=>{const [u,out,w='1440',h='900']=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:+w,height:+h}});const errs=[];
p.on('pageerror',e=>errs.push(e.message.slice(0,160)));p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text().slice(0,160))});
await p.goto(u,{waitUntil:'load',timeout:120000}).catch(e=>errs.push(e.message));
await p.waitForTimeout(1500);
const H=await p.evaluate(()=>document.documentElement.scrollHeight);
for(let y=0;y<H;y+=300){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(90)}
await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(1200);
await p.addStyleTag({content:'.j-header{position:absolute!important}.j-fab,.j-mbar,.j-totop{display:none!important}.rv{opacity:1!important;transform:none!important}'});
await p.screenshot({path:out+'.png',fullPage:true});
const info=await p.evaluate(()=>({h:document.documentElement.scrollHeight,w:document.documentElement.scrollWidth,hdr:document.querySelectorAll('.j-header').length,ftr:document.querySelectorAll('.j-footer').length,astraHdr:document.querySelectorAll('#masthead').length,h1:[...document.querySelectorAll('h1')].map(x=>x.textContent.trim().slice(0,60)),font:getComputedStyle(document.querySelector('h1')||document.body).fontFamily}));
console.log(JSON.stringify(info));if(errs.length)console.log('ERRORS',errs.slice(0,10));await b.close()})()
