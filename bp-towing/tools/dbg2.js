const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto('file://'+process.cwd()+'/prev/home.html',{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
await p.evaluate(()=>{document.documentElement.style.scrollBehavior='auto';scrollTo(0,document.body.scrollHeight)});await p.waitForTimeout(1500);
const f=await p.$('.bp-footer');await f.screenshot({path:'prev/footer.png'});
console.log(await p.evaluate(()=>{const e=document.querySelector('.bp-fbottom .bp-copy');return e.getBoundingClientRect().width+' '+getComputedStyle(e).width}));
await b.close()})()
