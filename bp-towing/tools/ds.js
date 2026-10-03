(function () {
  if (window.__bpDS) return; window.__bpDS = 1;
  var d = document, de = d.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  function init() {
    de.classList.add('bp-js');
    // header: scrolled state
    var h = d.querySelector('.bp-header');
    if (h) { var on = function () { h.classList.toggle('is-scrolled', scrollY > 30) }; on(); addEventListener('scroll', on, { passive: true }) }
    // scroll progress bar
    var bar = d.createElement('div'); bar.className = 'bp-progress'; d.body.appendChild(bar);
    var tick = false, prog = function () { var m = de.scrollHeight - innerHeight; bar.style.transform = 'scaleX(' + (m > 0 ? scrollY / m : 0) + ')'; tick = false };
    prog(); addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(prog) } }, { passive: true });
    // staggered reveal for list items / ticks / brand logos
    var groups = d.querySelectorAll('.bp-list ul, .bp-ticks .elementor-icon-list-items, .bp-brands, .bp-stagger');
    var items = [];
    groups.forEach(function (g) { [].slice.call(g.children).forEach(function (c, i) { c.classList.add('bp-rv'); c.style.transitionDelay = Math.min(i * 70, 560) + 'ms'; items.push(c) }) });
    if (reduce || !('IntersectionObserver' in window)) items.forEach(function (e) { e.classList.add('is-in') });
    else {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target) } }) }, { threshold: .1, rootMargin: '0px 0px -40px 0px' });
      items.forEach(function (e) { io.observe(e) });
    }
    // count-up stats (numbers are server-rendered final values; JS only animates them)
    var cnt = d.querySelectorAll('.bp-count[data-to]');
    var run = function (el) { var to = +el.getAttribute('data-to'), t0 = null, dur = 1800; var step = function (t) { if (!t0) t0 = t; var p = Math.min((t - t0) / dur, 1); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step) }; el.textContent = '0'; requestAnimationFrame(step) };
    if (!reduce && 'IntersectionObserver' in window) { var co = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { run(e.target); co.unobserve(e.target) } }) }, { threshold: .6 }); cnt.forEach(function (e) { co.observe(e) }) }
    // mark linked service cards
    d.querySelectorAll('.bp-card').forEach(function (c) { if (c.querySelector('a[href]')) c.classList.add('bp-linked') });
    if (reduce || !fine) return;
    // cursor spotlight on glass cards
    d.querySelectorAll('.bp-spot').forEach(function (c) {
      c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px') });
    });
    // subtle 3D tilt on cards
    d.querySelectorAll('.bp-card, .bp-tilt').forEach(function (c) {
      c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; c.style.transform = 'perspective(1000px) rotateX(' + (-y * 5) + 'deg) rotateY(' + (x * 6) + 'deg) translateY(-8px)' });
      c.addEventListener('pointerleave', function () { c.style.transform = '' });
    });
    // magnetic primary buttons
    d.querySelectorAll('.bp-btn .elementor-button, .bp-form .elementor-button').forEach(function (b) {
      b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX - r.left - r.width / 2) * .12) + 'px ' + ((e.clientY - r.top - r.height / 2) * .2) + 'px' });
      b.addEventListener('pointerleave', function () { b.style.translate = '' });
    });
  }
  if (d.readyState !== 'loading') init(); else d.addEventListener('DOMContentLoaded', init);
})();
