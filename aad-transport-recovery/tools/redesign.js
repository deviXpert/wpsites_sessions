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
