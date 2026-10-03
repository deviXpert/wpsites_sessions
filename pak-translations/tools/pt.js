(function(){var d=document,h=d.documentElement;if(h.classList.contains('x-js'))return;h.classList.add('x-js');
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function init(){
 var els=d.querySelectorAll('.rv,.rv-st');
 if(!('IntersectionObserver' in window)||rm){els.forEach(function(e){e.classList.add('is-in')});}
 else{var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('is-in');io.unobserve(x.target);}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});els.forEach(function(e){io.observe(e)});}
 var bar=d.createElement('div');bar.id='x-progress';d.body.appendChild(bar);
 var t=false;function prog(){var m=h.scrollHeight-innerHeight;bar.style.transform='scaleX('+(m>0?scrollY/m:0)+')';t=false;}
 addEventListener('scroll',function(){if(!t){t=true;requestAnimationFrame(prog);}},{passive:true});prog();
 if(!rm&&matchMedia('(hover:hover)').matches){d.querySelectorAll('.x-card').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px');});});}
}
if(d.readyState!=='loading')init();else d.addEventListener('DOMContentLoaded',init);
})();
