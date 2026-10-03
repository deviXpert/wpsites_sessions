const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(await p.evaluate(()=>[...document.querySelectorAll('.bp-header')].map(h=>{const a=[];let n=h;while(n&&a.length<8){a.push((n.getAttribute&&(n.getAttribute('data-elementor-id')||n.getAttribute('data-id')))+':'+(n.className||'').toString().slice(0,40));n=n.parentElement}return a.join(' < ')}).join('\n')));await b.close()})()
