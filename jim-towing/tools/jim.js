(function(){if(window.__jim)return;window.__jim=1;
var d=document,RM=matchMedia('(prefers-reduced-motion: reduce)').matches,FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
function $$(s,c){return [].slice.call((c||d).querySelectorAll(s))}
function init(){
d.documentElement.classList.add('j-js');d.body.classList.add('j-page');
var editor=d.body.classList.contains('elementor-editor-active');
/* progress bar + header + floating buttons */
var bar=d.createElement('div');bar.className='j-progress';d.body.appendChild(bar);
var h=d.querySelector('.j-header'),fab=d.querySelector('.j-fab'),mbar=d.querySelector('.j-mbar'),top=d.querySelector('.j-totop'),ring=top&&top.querySelector('circle'),last=0;
function onScroll(){var y=scrollY,max=d.documentElement.scrollHeight-innerHeight,p=max>0?y/max:0;bar.style.transform='scaleX('+p+')';
if(h){h.classList.toggle('is-scrolled',y>40);if(!editor)h.classList.toggle('is-hidden',y>500&&y>last+4&&!h.matches(':hover,:focus-within'));if(y<last-4)h.classList.remove('is-hidden')}
var show=y>innerHeight*.6;if(fab)fab.classList.toggle('on',show);if(mbar)mbar.classList.toggle('on',y>200);if(top)top.classList.toggle('on',show);if(ring)ring.style.strokeDashoffset=138-138*p;
last=y;road()}
addEventListener('scroll',onScroll,{passive:true});
if(top)top.addEventListener('click',function(){scrollTo({top:0,behavior:RM?'auto':'smooth'})});
/* reveal */
var els=$$('.rv,.j-stats,.j-map');
if(!('IntersectionObserver' in window)||RM||editor){els.forEach(function(e){e.classList.add('is-in')})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{threshold:.14,rootMargin:'0px 0px -40px 0px'});els.forEach(function(e){io.observe(e)})}
/* counters */
var cio='IntersectionObserver' in window&&!RM&&!editor?new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;cio.unobserve(e.target);var el=e.target,to=parseFloat(el.dataset.count),dec=(el.dataset.count.split('.')[1]||'').length,t0=null;
if(RM){el.textContent=to.toFixed(dec);return}
function step(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1600),v=to*(1-Math.pow(1-k,4));el.textContent=v.toFixed(dec);if(k<1)requestAnimationFrame(step)}requestAnimationFrame(step)})},{threshold:.1}):null;
$$('[data-count]').forEach(function(e){if(cio){e.textContent='0';cio.observe(e)}});
/* route map path lengths */
$$('.j-map .route').forEach(function(p){try{p.style.setProperty('--len',Math.ceil(p.getTotalLength()))}catch(e){}});
/* tilt + magnetic */
if(FINE&&!RM){
$$('.j-sc,.j-wc,.j-fc,.j-pc,.j-tilt-me').forEach(function(c){c.classList.add('j-tilt');c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(1000px) rotateX('+(-y*5)+'deg) rotateY('+(x*6)+'deg) translateY(-6px)'});c.addEventListener('mouseleave',function(){c.style.transform=''})});
$$('.j-btn .elementor-button,.j-hcall').forEach(function(b){b.addEventListener('mousemove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18)+'px,'+((e.clientY-r.top-r.height/2)*.3-2)+'px)'});b.addEventListener('mouseleave',function(){b.style.transform=''})});}
/* scrolly */
$$('.j-scrolly').forEach(function(w){var bs=$$('.j-sb',w),fs=$$('.j-sticky figure',w),ds=$$('.j-sticky-dots i',w);if(!bs.length)return;
function set(i){bs.forEach(function(b,k){b.classList.toggle('on',k===i)});fs.forEach(function(f,k){f.classList.toggle('on',k===i)});ds.forEach(function(f,k){f.classList.toggle('on',k===i)})}set(0);
if('IntersectionObserver' in window){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)set(bs.indexOf(e.target))})},{rootMargin:'-45% 0px -45% 0px'});bs.forEach(function(b){o.observe(b)})}});
/* situation tabs */
$$('.j-sit').forEach(function(w){var tabs=$$('.j-sit-tab',w),ps=$$('.j-sit-panel',w);
function go(i,f){tabs.forEach(function(t,k){t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1});ps.forEach(function(p,k){p.classList.toggle('on',k===i);p.hidden=false;p.setAttribute('aria-hidden',k!==i)});if(f)tabs[i].focus()}
tabs.forEach(function(t,i){t.addEventListener('click',function(){go(i)});t.addEventListener('keydown',function(e){var k=e.key,n=tabs.length;if(k==='ArrowDown'||k==='ArrowRight'){e.preventDefault();go((i+1)%n,1)}if(k==='ArrowUp'||k==='ArrowLeft'){e.preventDefault();go((i-1+n)%n,1)}})});go(0)});
/* gallery: duplicate for loop + lightbox */
$$('.j-gal-in').forEach(function(g){if(g.dataset.dup)return;g.dataset.dup=1;$$('figure',g).forEach(function(f){var c=f.cloneNode(true);c.setAttribute('aria-hidden','true');g.appendChild(c)})});
var lb=null;d.addEventListener('click',function(e){var f=e.target.closest('.j-gal figure');if(!f)return;var img=f.querySelector('img');
if(!lb){lb=d.createElement('div');lb.className='j-lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.innerHTML='<img alt=""><button aria-label="Close">&#10005;</button>';d.body.appendChild(lb);lb.addEventListener('click',function(ev){if(ev.target.tagName!=='IMG')lb.classList.remove('on')});d.addEventListener('keydown',function(ev){if(ev.key==='Escape')lb.classList.remove('on')})}
var li=lb.querySelector('img');li.src=img.dataset.full||img.currentSrc||img.src;li.alt=img.alt;lb.classList.add('on');lb.querySelector('button').focus()});
/* live Calgary clock */
$$('.j-clock').forEach(function(el){var sh=el.parentNode.querySelector('.j-shift');function t(){try{var d=new Date(),s=d.toLocaleTimeString('en-CA',{hour:'numeric',minute:'2-digit',timeZone:el.dataset.tz||'America/Edmonton'}),h=+new Intl.DateTimeFormat('en-CA',{hour:'numeric',hour12:false,timeZone:el.dataset.tz||'America/Edmonton'}).format(d);el.textContent=s.replace(/\./g,'').toUpperCase();if(sh)sh.textContent=(h>=22||h<6?'night shift':h<12?'morning shift':h<18?'day shift':'evening shift')+' · dispatching now'}catch(e){}}t();setInterval(t,30000)});
onScroll()}
/* steps road: fill + truck follows scroll */
function road(){$$('.j-road').forEach(function(r){var b=r.getBoundingClientRect(),vh=innerHeight,p=Math.max(0,Math.min(1,(vh*.8-b.top)/(b.height+vh*.35)));var f=r.querySelector('.j-road-fill'),t=r.querySelector('.j-truck');if(f)f.style.width=(p*100)+'%';if(t)t.style.left=(p*100)+'%';
$$('.j-step',r).forEach(function(s,i,a){s.classList.toggle('on',p>=(i/(a.length))+.02)})})}
if(d.readyState!=='loading')init();else d.addEventListener('DOMContentLoaded',init);
})();
