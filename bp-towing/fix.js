(function(){var t=document.querySelector('.bp-mobnav .elementor-menu-toggle');if(!t)return;
function close(){if(t.classList.contains('elementor-active'))t.click()}
document.addEventListener('click',function(e){if(t.classList.contains('elementor-active')&&!e.target.closest('.bp-mobnav'))close()},true);
document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
document.querySelectorAll('.bp-mobnav .elementor-nav-menu--dropdown a').forEach(function(a){a.addEventListener('click',function(){if(!a.parentElement.classList.contains('menu-item-has-children')||a.closest('.sub-menu'))close()})});
new MutationObserver(function(){document.documentElement.style.overflow=t.classList.contains('elementor-active')?'hidden':''}).observe(t,{attributes:true,attributeFilter:['class']});
})();
