const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const u=process.argv[2], out=process.argv[3];
let p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:1440,height:900}});
p.on('pageerror',e=>console.log('JSERR',e.message.slice(0,120)));
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
const r=await p.evaluate(()=>{const a=document.querySelector('.bp-has-mega .bp-mlink a').getBoundingClientRect();return [a.x+a.width/2,a.y+a.height/2]});await p.mouse.move(r[0],r[1]);await p.mouse.move(r[0],r[1]+60,{steps:5});await p.waitForTimeout(700);await p.screenshot({path:out+'_mega.png',clip:{x:0,y:0,width:1440,height:560}});
await p.close();
p=await b.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844},deviceScaleFactor:2});
await p.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
await p.locator('.bp-mobnav .elementor-menu-toggle').click({force:true}).catch(e=>console.log('toggle',e.message.slice(0,80)));await p.waitForTimeout(600);
const sub=await p.$('.bp-mobnav .elementor-nav-menu--dropdown .sub-arrow');if(sub){await sub.click({force:true});await p.waitForTimeout(500)}
await p.screenshot({path:out+'_mob.png'});await b.close()})()
