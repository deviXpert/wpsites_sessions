// Opens each FAQ item in turn and records the column widths -> must stay constant.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const w of [1466,1920]){for(const path of ['/','/services/','/about-us/','/languages/']){
const p=await (await b.newContext({ignoreHTTPSErrors:true,viewport:{width:w,height:900}})).newPage();
await p.goto('https://pak-translations.com'+path+'?nc='+Date.now(),{waitUntil:'networkidle'});
const titles=p.locator('.x-faq .elementor-tab-title');const n=await titles.count();const res=[];
for(let i=0;i<n;i++){await titles.nth(i).scrollIntoViewIfNeeded();await titles.nth(i).click();await p.waitForTimeout(700);
 res.push(await p.evaluate(()=>{const s=document.querySelector('.x-faq-side').getBoundingClientRect().width,f=document.querySelector('.x-faq').getBoundingClientRect().width,open=document.querySelectorAll('.x-faq .elementor-tab-title.elementor-active').length;return `${Math.round(s)}/${Math.round(f)}(open:${open})`}));}
console.log(w,path,res.join(' '));await p.close();}}
await b.close()})();
