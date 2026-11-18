"""Short QA window (approved by the user): switch Elementor maintenance mode off, screenshot pages at
desktop / tablet / phone widths, then ALWAYS switch it back on (try/finally).
Usage: python3 qa_window.py / [/other-path/ ...]   -> ../qa/shots/<slug>-<width>.png + layout report"""
import sys, json, subprocess, time, wp

paths = sys.argv[1:] or ['/']
JS = r"""
const {chromium}=require('playwright');
(async()=>{const paths=JSON.parse(process.argv[2]);const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}});
for(const pth of paths){for(const w of [1440,1024,390]){
 const p=await b.newPage({viewport:{width:w,height:900},ignoreHTTPSErrors:true});const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,120)));
 const r=await p.goto('https://evtron.co.uk'+pth+'?qa='+Date.now(),{waitUntil:'networkidle',timeout:60000});await p.waitForTimeout(800);await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}window.scrollTo(0,0)});await p.waitForTimeout(1600);
 const info=await p.evaluate(()=>{const hb=document.querySelector('header');const nav=document.querySelector('.elementor-nav-menu--main');
   return {status:document.title,hscroll:document.documentElement.scrollWidth>innerWidth,header:hb?Math.round(hb.getBoundingClientRect().height):null,
   navH:nav?Math.round(nav.getBoundingClientRect().height):null,
   containers:[...document.querySelectorAll('.ev-container')].slice(0,3).map(e=>Math.round(e.getBoundingClientRect().width)),
   over:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,6).map(e=>e.tagName+'.'+(e.className.baseVal??e.className).toString().slice(0,60)+' r='+Math.round(e.getBoundingClientRect().right)),sections:[...document.querySelectorAll('main section')].map(s=>{const cs=getComputedStyle(s);return cs.paddingTop+'/'+cs.paddingBottom})}});
 const slug=(pth.replace(/\//g,'_')||'_');await p.screenshot({path:`../qa/shots/${slug}-${w}.png`,fullPage:true});
 console.log(pth,w,r&&r.status(),JSON.stringify(info),errs.slice(0,3));await p.close();}}
await b.close();})();
"""
open('/tmp/claude-0/-home-user-wpsites-sessions/6142b919-30ff-596b-a508-75c2c060554a/scratchpad/qa.js', 'w').write(JS)
orig = wp.req('elementor/v1/settings/elementor_maintenance_mode_mode')['data']['value'] or 'maintenance'
try:
    print('maintenance off', wp.eset('elementor_maintenance_mode_mode', '').get('success'))
    time.sleep(2)
    subprocess.run(['node', '/tmp/claude-0/-home-user-wpsites-sessions/6142b919-30ff-596b-a508-75c2c060554a/scratchpad/qa.js', json.dumps(paths)], timeout=420)
finally:
    print('maintenance restored', wp.eset('elementor_maintenance_mode_mode', orig).get('success'), orig)
