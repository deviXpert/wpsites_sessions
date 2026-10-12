/* Busy Bee Auto Repair – site behaviour (Elementor → Custom Code "Busy Bee – Scripts").
   Source of truth: tools/bb.js in the wpsites_sessions repo (pushed by code.py). */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- typing word ("trust") ---------- */
  function typing(el) {
    var word = el.getAttribute('data-word') || el.textContent.trim();
    el.setAttribute('aria-label', word);
    el.innerHTML = '<span aria-hidden="true" class="bb-typed"></span><span aria-hidden="true" class="bb-caret"></span><span aria-hidden="true" class="bb-rest"></span>';
    var typed = el.firstChild, rest = el.lastChild;
    function show(n) { typed.textContent = word.slice(0, n); rest.textContent = word.slice(n); }
    show(word.length);
    if (reduce) return;
    var i = 0;
    function step() {
      if (i <= word.length) { show(i); i++; setTimeout(step, 170); }
      else { setTimeout(function () { i = 0; step(); }, 3200); }
    }
    setTimeout(step, 600);
  }

  /* ---------- hero vehicle slideshow (10s, buttons jump) ---------- */
  function heroSlider(hero) {
    var slides = $$('.bb-slide', hero), btns = $$('.bb-vbtn', hero), names = $$('.bb-vname', hero);
    if (!slides.length) return;
    var count = slides.length, cur = 0, timer;
    var pts = $$('.bb-pts', hero);
    var labels = btns.map(function (b) { return b.getAttribute('data-label') || b.textContent.trim(); });
    function go(n) {
      cur = (n + count) % count;
      slides.forEach(function (s, i) { s.classList.toggle('is-active', i === cur || i === 0); });
      hero.classList.toggle('is-alt', cur !== 0);
      pts.forEach(function (p, i) { p.classList.toggle('is-active', i === cur); });
      btns.forEach(function (b, i) {
        b.classList.toggle('is-active', i === cur);
        var a = $('a', b); if (a) a.setAttribute('aria-pressed', i === cur ? 'true' : 'false');
      });
      var label = labels[cur] || labels[0];
      names.forEach(function (n) { n.textContent = label; });
    }
    function start() { clearInterval(timer); timer = setInterval(function () { go(cur + 1); }, 10000); }
    btns.forEach(function (b, i) {
      var a = $('a', b) || b;
      a.setAttribute('role', 'button');
      a.addEventListener('click', function (e) { e.preventDefault(); go(i); start(); });
    });
    go(0); start();
  }

  /* ---------- services filter ---------- */
  function serviceFilter(sec) {
    var btns = $$('.bb-filter', sec), cards = $$('[data-cat]', sec);
    btns.forEach(function (b) {
      var a = $('a', b) || b;
      a.setAttribute('role', 'button');
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var f = b.getAttribute('data-filter');
        btns.forEach(function (x) { x.classList.toggle('is-active', x === b); });
        cards.forEach(function (c) {
          var cat = c.getAttribute('data-cat');
          c.classList.toggle('is-filtered', !(f === 'All' || cat === f));
        });
      });
    });
  }

  /* ---------- reveal on scroll (reviews) ---------- */
  function reveal() {
    var els = $$('.bb-reveal');
    if (!('IntersectionObserver' in window) || reduce) { els.forEach(function (e) { e.classList.add('is-in'); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.15 });
    els.forEach(function (e, i) { if (e.classList.contains('bb-review')) e.style.setProperty('--reveal-delay', (i % 6) * 0.06 + 's'); io.observe(e); });
  }

  /* ---------- reviews arrows ---------- */
  function reviewArrows(sec) {
    var track = $('.bb-review-track', sec);
    if (!track) return;
    [['.bb-rev-prev', -1], ['.bb-rev-next', 1]].forEach(function (p) {
      var el = $(p[0] + ' a', sec) || $(p[0], sec);
      if (!el) return;
      el.setAttribute('role', 'button');
      el.setAttribute('aria-label', p[1] < 0 ? 'Previous reviews' : 'Next reviews');
      el.addEventListener('click', function (e) {
        e.preventDefault();
        track.scrollBy({ left: p[1] * Math.min(track.clientWidth * 0.9, 560), behavior: 'smooth' });
      });
    });
  }

  /* ---------- symptom checker: live vehicle title + suggestion chips ---------- */
  function checker(sec) {
    var f = function (id) { return $('[name="form_fields[' + id + ']"]', sec); };
    var title = $('.bb-veh-title .elementor-heading-title', sec), year = $('.bb-veh-year', sec), km = $('.bb-veh-km', sec);
    var issue = f('issue');
    function upd() {
      var mk = (f('make') || {}).value || '', md = (f('model') || {}).value || '';
      var y = (f('year') || {}).value || '', m = (f('mileage') || {}).value || '';
      if (title) title.textContent = (mk || md) ? [mk, md].filter(Boolean).join(' ') : 'Let’s meet your car.';
      if (year) year.textContent = y || 'Year';
      if (km) km.textContent = m ? m + ' km' : 'Mileage';
    }
    ['make', 'model', 'year', 'mileage'].forEach(function (k) { var i = f(k); if (i) i.addEventListener('input', upd); });
    $$('.bb-chips button', sec).forEach(function (b) {
      b.addEventListener('click', function () {
        if (!issue) return;
        var add = b.getAttribute('data-add');
        issue.value = issue.value ? issue.value.replace(/\s+$/, '') + (/[.!?]$/.test(issue.value.trim()) ? ' ' : '. ') + add : add;
        issue.focus();
      });
    });
  }

  /* ---------- winter popup: once per session after 650px of scroll (≥901px) ---------- */
  function winterPopup() {
    var sec = $('[data-popup]');
    if (!sec) return;
    var id = sec.getAttribute('data-popup');
    function onScroll() {
      if (window.innerWidth < 901 || window.scrollY < 650 || $('.elementor-popup-modal:not([style*="display: none"])')) return;
      try { if (sessionStorage.getItem('busy-bee-winter-preview')) { window.removeEventListener('scroll', onScroll); return; }
            sessionStorage.setItem('busy-bee-winter-preview', 'seen'); } catch (e) { return; }
      window.removeEventListener('scroll', onScroll);
      if (window.elementorProFrontend && elementorProFrontend.modules && elementorProFrontend.modules.popup) {
        elementorProFrontend.modules.popup.showPopup({ id: id });
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function init() {
    $$('.bb-type').forEach(typing);
    $$('.bb-hero, .bb-mhero').forEach(heroSlider);
    $$('.bb-services').forEach(serviceFilter);
    $$('.bb-reviews').forEach(reviewArrows);
    $$('.bb-checker').forEach(checker);
    reveal();
    winterPopup();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
