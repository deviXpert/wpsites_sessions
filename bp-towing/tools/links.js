const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY}});const c=await b.newContext({ignoreHTTPSErrors:true});
const L=[...new Set(JSON.parse(fs.readFileSync('dump/links.json')).map(u=>u.split('#')[0]))].filter(u=>u.startsWith('https://bptowingservice.ca'));
for(const u of L){try{const r=await c.request.get(u,{maxRedirects:0,timeout:30000});if(r.status()!=200)console.log(r.status(),u,r.headers().location||'')}catch(e){console.log('ERR',u)}}
console.log('checked',L.length);
const ext=[...new Set(JSON.parse(fs.readFileSync('dump/links.json')))].filter(u=>!u.startsWith('https://bptowingservice.ca'));console.log(ext.join('\n'));
await b.close()})();
