const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const ctx=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
const p=await ctx.newPage();const cdp=await ctx.newCDPSession(p);
await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:150,downloadThroughput:200*1024,uploadThroughput:100*1024});
const late=[];p.on('response',r=>{const u=r.url();if(u.endsWith('.css')||u.includes('.css?'))late.push(u.split('/').slice(-1)[0].slice(0,50))});
p.goto(process.argv[2],{waitUntil:'load',timeout:120000}).catch(()=>{});
await p.waitForEvent('domcontentloaded',{timeout:120000}).catch(()=>{});
for(let i=0;i<6;i++){await p.screenshot({path:`prev/fouc${i}.png`,clip:{x:0,y:0,width:390,height:420}}).catch(()=>{});await p.waitForTimeout(500)}
// which SVGs are big at this moment
console.log(await p.evaluate(()=>[...document.querySelectorAll('svg')].filter(s=>s.getBoundingClientRect().width>60&&s.getBoundingClientRect().top<900).map(s=>(s.getAttribute('class')||'')+' '+Math.round(s.getBoundingClientRect().width)+'px in '+(s.closest('[class*=elementor-widget-]')||{className:''}).className.toString().match(/elementor-widget-[a-z-]+/)?.[0]).slice(0,10)));
await b.close()})()
