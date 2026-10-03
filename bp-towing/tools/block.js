const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const ctx=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
const p=await ctx.newPage();
if(process.argv[3]==='block') await p.route(/widget-nav-menu|widget-icon-list|widget-icon-box|post-4486\.css/,r=>r.abort());
await p.goto(process.argv[2],{waitUntil:'load',timeout:90000}).catch(()=>{});await p.waitForTimeout(800);
await p.screenshot({path:'prev/blk_'+(process.argv[3]||'normal')+'.png',clip:{x:0,y:0,width:390,height:300}});
await p.locator('.bp-mobnav .elementor-menu-toggle').first().tap().catch(e=>console.log('tap',e.message.slice(0,60)));await p.waitForTimeout(700);
await p.screenshot({path:'prev/blk_'+(process.argv[3]||'normal')+'_open.png'});
await p.locator('.bp-mobnav .elementor-menu-toggle').first().tap().catch(()=>{});await p.waitForTimeout(700);
console.log(process.argv[3]||'normal','closed again:',await p.evaluate(()=>{const c=document.querySelector('.bp-mobnav .elementor-nav-menu__container');return c.getBoundingClientRect().height<5||getComputedStyle(c).transform.includes('0, 0')}));
await b.close()})()
