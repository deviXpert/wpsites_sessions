// Submits each Elementor form on the live site once (marked TEST) and reports the server response.
const {chromium}=require('playwright');(async()=>{const file=process.argv[2];
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY},args:['--ignore-certificate-errors']});
const T='TEST – website form check, please ignore';
const forms={
 '/':{ 'form_fields[name]':'Website Test','form_fields[email]':'info@pak-translations.com','form_fields[phone]':'+92 300 0000000','form_fields[source_language]':'Urdu','form_fields[target_language]':'English','form_fields[message]':T},
 '/contact-us/':{'form_fields[name]':'Website Test','form_fields[email]':'info@pak-translations.com','form_fields[subject]':T,'form_fields[message]':T},
 '/your-order/':{'form_fields[name]':'Website Test','form_fields[email]':'info@pak-translations.com','form_fields[phone]':'+92 300 0000000','form_fields[source_language]':'Urdu','form_fields[target_language]':'English','form_fields[message]':T},
 '/career/':{'form_fields[name]':'Website Test','form_fields[email]':'info@pak-translations.com','form_fields[experience]':'5','form_fields[input_language_1]':'Urdu','form_fields[output_language]':'English','form_fields[services]':'Translation','form_fields[payment_method]':'Bank','form_fields[additional_info]':T},
};
const only=(process.env.ONLY||'').split(',').filter(Boolean);for(const [path,vals] of Object.entries(forms)){if(only.length&&!only.includes(path))continue;
 const p=await (await b.newContext({ignoreHTTPSErrors:true,viewport:{width:1366,height:900}})).newPage();
 await p.goto('https://pak-translations.com'+path+'?nc='+Date.now(),{waitUntil:'networkidle'});
 const f=p.locator('form.elementor-form').first();
 for(const [n,v] of Object.entries(vals)){const el=f.locator(`[name="${n}"]`);if(await el.count())await el.first().fill(v);else console.log(path,'missing field',n);}
 if(path==='/career/'){await f.locator('[name="form_fields[cv]"], [name="form_fields[cv][]"]').first().setInputFiles(file);}
 const resp=p.waitForResponse(r=>r.url().includes('admin-ajax.php')&&r.request().method()==='POST',{timeout:60000}).catch(e=>null);
 await f.locator('button[type=submit]').click();
 const r=await resp;let body=r?await r.text():'no ajax response';
 await p.waitForTimeout(1500);
 const msg=await p.locator('.elementor-message').allInnerTexts().catch(()=>[]);
 console.log(path,'| HTTP',r&&r.status(),'|',body.slice(0,180),'| shown:',JSON.stringify(msg));
 await p.close();}
// social links in a real browser
if(!only.length)for(const u of ['https://www.facebook.com/PakTranslationsCompany','https://www.proz.com/profile/1415308']){const p=await (await b.newContext({ignoreHTTPSErrors:true})).newPage();const r=await p.goto(u,{waitUntil:'domcontentloaded',timeout:60000}).catch(e=>null);console.log(u,'->',r&&r.status(),await p.title().catch(()=>''));await p.close();}
await b.close()})();
