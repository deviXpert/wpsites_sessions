const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
console.log(await p.evaluate(()=>{let n=document.querySelector('.bp-post-aside');const o=['scrollY='+scrollY];while(n){const c=getComputedStyle(n);if(c.overflow!=='visible'||c.overflowX!=='visible'||c.overflowY!=='visible'||c.transform!=='none'||c.contain!=='none')o.push(n.tagName+'.'+(n.className||'').toString().slice(0,50)+' ov='+c.overflowX+'/'+c.overflowY+' tf='+c.transform.slice(0,15)+' contain='+c.contain);n=n.parentElement}
const a=document.querySelector('.bp-post-aside');a.style.position='static';const st=a.getBoundingClientRect().top+scrollY;a.style.position='';o.push('static top='+Math.round(st));return o.join('\n')}));await b.close()})()
