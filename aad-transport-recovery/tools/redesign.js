(function(){if(window.__xA)return;window.__xA=1;function init(){var d=document;d.documentElement.classList.add('x-js');
var h=d.querySelector('.x-header');if(h){var on=function(){h.classList.toggle('is-scrolled',scrollY>40)};on();addEventListener('scroll',on,{passive:true})}
var els=[].slice.call(d.querySelectorAll('.rv'));
if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){els.forEach(function(e){e.classList.add('is-in')});return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
els.forEach(function(e){io.observe(e)});
d.querySelectorAll('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(ev){var t=d.querySelector(a.getAttribute('href'));if(t){ev.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'})}})})}
if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init)})();
(function(){if(window.__xB)return;window.__xB=1;function init(){var d=document;
var bar=d.createElement('div');bar.className='x-progress';d.body.appendChild(bar);
var up=function(){var h=d.documentElement.scrollHeight-innerHeight;bar.style.transform='scaleX('+(h>0?scrollY/h:0)+')'};up();addEventListener('scroll',up,{passive:true});
if(matchMedia('(hover:hover) and (pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
d.querySelectorAll('.x-sc,.x-fcard,.x-wcard,.x-fc,.x-dest').forEach(function(c){c.classList.add('x-tilt');c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateX('+(-y*5)+'deg) rotateY('+(x*5)+'deg) translateY(-6px)'});c.addEventListener('mouseleave',function(){c.style.transform=''})})}
var toc=d.querySelector('.x-toc-list'),pr=d.querySelector('.x-prose');
if(toc&&pr){var hs=pr.querySelectorAll('h2,h3,h4');if(hs.length<2){var t=d.querySelector('.x-toc');if(t)t.style.display='none'}
hs.forEach(function(h,i){h.id=h.id||'sec-'+i;var a=d.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;toc.appendChild(a)});
var links=toc.querySelectorAll('a');if('IntersectionObserver' in window){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(l){l.classList.toggle('is-active',l.getAttribute('href')=='#'+e.target.id)})}})},{rootMargin:'-20% 0px -70% 0px'});hs.forEach(function(h){o.observe(h)})}}
}
if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init)})();
(function(){if(window.__xM)return;window.__xM=1;function init(){var d=document,de=d.documentElement;
var norm=function(u){try{return new URL(u,location.href).pathname.replace(/\/+$/,'')||'/'}catch(e){return u}},here=norm(location.href);
d.querySelectorAll('.x-mm a,.x-dw a').forEach(function(a){if(norm(a.href)===here&&a.getAttribute('href').indexOf('tel:')&&a.getAttribute('href').indexOf('mailto:'))a.classList.add('is-current')});
d.querySelectorAll('.x-mm-has').forEach(function(li){var a=li.querySelector('.x-mm-link');if(li.querySelector('.x-mm-item.is-current'))a.classList.add('is-current');
var set=function(o){li.classList.toggle('is-open',o);a.setAttribute('aria-expanded',o?'true':'false')};
li.addEventListener('mouseenter',function(){li.classList.remove('is-closed');set(true)});li.addEventListener('mouseleave',function(){li.classList.remove('is-closed');set(false)});
li.addEventListener('focusin',function(e){if(e.target!==a)li.classList.remove('is-closed');set(true)});li.addEventListener('focusout',function(e){if(!li.contains(e.relatedTarget))set(false)});
a.addEventListener('pointerdown',function(e){a._touch=e.pointerType!=='mouse'});
a.addEventListener('click',function(e){if(a._touch&&!li.classList.contains('is-open')){e.preventDefault();li.classList.remove('is-closed');set(true)}});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&li.classList.contains('is-open')){li.classList.add('is-closed');set(false);a.focus()}});
d.addEventListener('pointerdown',function(e){if(!li.contains(e.target))set(false)})});
var dws=d.querySelectorAll('.x-dw');for(var i=1;i<dws.length;i++)dws[i].remove();var dw=dws[0];if(!dw)return;d.body.appendChild(dw);
var pane=dw.querySelector('.x-dw-pane'),last=null,t=null;
dw.querySelectorAll('.x-dw-acc').forEach(function(b){b.addEventListener('click',function(){b.setAttribute('aria-expanded',b.getAttribute('aria-expanded')==='true'?'false':'true')});
if(b.nextElementSibling.querySelector('.is-current'))b.setAttribute('aria-expanded','true')});
var bs=d.querySelectorAll('.x-burger');
var open=function(b){last=b;clearTimeout(t);dw.hidden=false;void dw.offsetWidth;dw.classList.add('is-open');de.classList.add('x-lock');bs.forEach(function(x){x.setAttribute('aria-expanded','true')});dw.querySelector('.x-dw-x').focus()};
var close=function(){if(dw.hidden)return;dw.classList.remove('is-open');de.classList.remove('x-lock');bs.forEach(function(x){x.setAttribute('aria-expanded','false')});t=setTimeout(function(){dw.hidden=true},350);if(last)last.focus()};
bs.forEach(function(b){b.addEventListener('click',function(){open(b)})});
dw.querySelectorAll('[data-x-close]').forEach(function(x){x.addEventListener('click',close)});
dw.addEventListener('keydown',function(e){if(e.key==='Escape')close();if(e.key!=='Tab')return;var f=[].filter.call(pane.querySelectorAll('a,button'),function(x){return x.offsetParent!==null});if(!f.length)return;
if(e.shiftKey&&d.activeElement===f[0]){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&d.activeElement===f[f.length-1]){e.preventDefault();f[0].focus()}});
addEventListener('resize',function(){if(innerWidth>1024)close()})}
if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init)})();
