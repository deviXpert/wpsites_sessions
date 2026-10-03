// node secshot.js <slug> <selectorText-substring> <out>  — screenshot the section containing a heading text
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const [slug,txt,out,w]=process.argv.slice(2);const p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:+(w||1440),height:900}});
await p.goto('https://bptowingservice.ca/'+slug+'/?nc='+Date.now(),{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
await p.addStyleTag({content:'.elementor-invisible{visibility:visible!important}.animated{animation:none!important}.bp-header{display:none!important}'});
const h=await p.evaluateHandle(t=>{const e=[...document.querySelectorAll('.elementor-heading-title')].find(x=>x.textContent.includes(t));return e&&e.closest('.bp-sec')},txt);
const el=h.asElement();if(!el){console.log('notfound',slug,txt);await b.close();return}
await el.scrollIntoViewIfNeeded();await p.waitForTimeout(800);await el.screenshot({path:out});await b.close()})()
