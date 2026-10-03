// usage: node tools/shot.js <url> <outprefix> [password]   -> full-page desktop + mobile screenshots
const {chromium}=require('playwright');(async()=>{const [url,out,pw]=process.argv.slice(2);
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
for(const [n,w,h] of [['d',1440,900],['m',390,844]]){const ctx=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:w,height:h}});const p=await ctx.newPage();
await p.goto(url+(url.includes('?')?'&':'?')+'nc='+Date.now(),{waitUntil:'networkidle',timeout:120000}).catch(e=>console.log('goto',e.message));
if(pw&&await p.$('input[name=post_password]')){await p.fill('input[name=post_password]',pw);await Promise.all([p.waitForNavigation({timeout:120000}).catch(()=>{}),p.click('input[type=submit]')]);await p.waitForLoadState('networkidle').catch(()=>{});}
await p.addStyleTag({content:'.rv,.x-js .rv,.x-js .rv-st>*{opacity:1!important;transform:none!important}'});const ow=await p.evaluate(()=>{const W=document.documentElement.clientWidth;return [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>W+1).slice(0,8).map(e=>e.tagName+'.'+String(e.className).slice(0,60)+' '+Math.round(e.getBoundingClientRect().right))});if(ow.length)console.log(n,'overflow',JSON.stringify(ow));
const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=600){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(120);}
await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(600);
await p.screenshot({path:`${out}_${n}.png`,fullPage:true});await ctx.close();}
await b.close()})();
