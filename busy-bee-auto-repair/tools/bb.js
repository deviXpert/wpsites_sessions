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

  /* ---------- symptom checker: make→model dropdowns, vehicle preview, instant guidance ---------- */
  /* Imagin.studio customer key: renders with the demo key are watermarked, so the Civic photo is used until a key is set */
  var IMAGIN_KEY = '';  // Imagin demo key 'img' is watermarked – off
  /* CarImages API (carimagesapi.com) – preferred provider once a key is pasted here. Use the PUBLIC key from the dashboard and lock it
     to the site's domain there (never the API secret). When set, it replaces the Imagin demo above. */
  var CARIMAGES_KEY = 'ci_6349daebb71d3e88d8d5b77501f062455b0c32b8f432378bb80da4c4';
  /* Free CarImages plan is watermarked, so photos stay OFF until the account is on Pro – then set this to true.
     Meanwhile the checker shows our own drawn illustration for the vehicle's body style (car_svg.py → window.BB_CARSVG). */
  var CARIMAGES_PRO = false;
  var USE_DRAWN = false;   // drawn body-style illustrations (car_svg.py) – off at the client's request
  var CAR_COLOURS = ['#c8102e', '#f1f3f4', '#1f3a5f', '#8a9399', '#2b2f33', '#6b1d1d', '#ffffff', '#3f5e4a', '#b9bfc3', '#0f4c81']; // 'img' = Imagin demo key (watermarked) – replace with the shop's commercial key
  var RULES = [
    { k: /brak|squeal|grind|pedal|stopping/i, t: 'Brakes', u: 2, svc: 'Brake repair & replacement',
      c: ['Worn brake pads or rotors', 'Sticking caliper or slide pins', 'Low or contaminated brake fluid'],
      d: 'Drive gently and leave extra stopping distance. If the pedal feels soft or the car pulls hard, stop driving and call us.',
      f: 'Listen for grinding when braking and check the brake-fluid level under the hood.' },
    { k: /start|crank|click|battery|dead|jump/i, t: 'Starting & charging', u: 1, svc: 'Battery & alternator service',
      c: ['Weak or failing battery (common in Calgary cold)', 'Corroded battery terminals', 'Faulty starter or alternator'],
      d: 'Usually safe once running, but avoid short trips and switch off accessories until it is tested.',
      f: 'Look for white or green corrosion on the battery terminals.' },
    { k: /overheat|temp|coolant|steam|radiator|antifreeze/i, t: 'Cooling system', u: 3, svc: 'Cooling system & radiator',
      c: ['Low coolant or a leak', 'Failing thermostat or water pump', 'Radiator fan not switching on'],
      d: 'Do not keep driving an overheating engine – pull over, switch off and call us. Never open a hot radiator cap.',
      f: 'With the engine cold, check the coolant reservoir level and look for puddles under the car.' },
    { k: /check engine|engine light|warning light|misfire|rough idle|stall|hesitat/i, t: 'Engine & diagnostics', u: 2,
      svc: 'Computer diagnostics & electrical',
      c: ['Ignition fault – spark plugs or coils', 'Sensor fault (O2, MAF) or vacuum leak', 'Loose fuel cap (evap code)'],
      d: 'A steady light: book soon. A flashing light means a misfire – reduce speed and avoid hard acceleration.',
      f: 'Tighten the fuel cap and note whether the light is steady or flashing.' },
    { k: /vibrat|shak|wobble|pull|align|steering|clunk|bump|suspension/i, t: 'Suspension, steering & tires', u: 2,
      svc: 'Suspension & steering repair',
      c: ['Wheel balance or tire wear', 'Worn suspension or steering parts', 'Alignment out after potholes'],
      d: 'Keep speeds moderate. If the steering feels loose, get it checked before highway driving.',
      f: 'Check tire pressures and look for uneven wear or bulges on the tires.' },
    { k: /transmission|gear|shift|slip|clutch/i, t: 'Transmission', u: 2, svc: 'Transmission repair',
      c: ['Low or old transmission fluid', 'Worn clutch or shift solenoid', 'Software/adaptation fault'],
      d: 'Avoid heavy loads and towing until it is checked – slipping can cause further damage.',
      f: 'Note when it happens: cold, hot, a specific gear or under acceleration.' },
    { k: /oil|leak|smoke|burn|smell/i, t: 'Leaks, smoke & smells', u: 2, svc: 'Engine maintenance & repair',
      c: ['Oil leaking onto hot exhaust parts', 'Overdue oil change or low oil', 'Coolant or fluid leak'],
      d: 'If you see smoke from under the hood or smell burning, stop and call us. Otherwise book soon.',
      f: 'Check the dipstick oil level and the colour of any drips under the car.' },
    { k: /noise|rattle|squeak|hum|whine|knock|tick/i, t: 'Unusual noise', u: 1, svc: 'Computer diagnostics & electrical',
      c: ['Loose heat shield or exhaust part', 'Worn belt, bearing or pulley', 'Suspension or brake hardware'],
      d: 'Usually OK to drive to the shop. A loud knock from the engine is the exception – stop and call.',
      f: 'Note when the noise happens: speed, turning, braking or idle.' }
  ];
  var URG = ['', 'Low – book at your convenience', 'Medium – book in the next few days', 'High – stop driving and call us'];

  function checker(sec) {
    var f = function (id) { return $('[name="form_fields[' + id + ']"]', sec); };
    var title = $('.bb-veh-title .elementor-heading-title', sec), year = $('.bb-veh-year', sec), km = $('.bb-veh-km', sec);
    var cap = $('.bb-veh-cap .elementor-heading-title', sec), note = $('.bb-veh-note .elementor-heading-title', sec);
    var img = $('.bb-veh-img img', sec), out = $('.bb-result', sec), form = $('form', sec);
    var issue = f('issue'), make = f('make'), model = f('model'), cars = window.BB_CARS || {};
    var civic = img ? { src: img.getAttribute('src'), srcset: img.getAttribute('srcset') } : null;
    if (img) img.addEventListener('error', function () { if (civic && img.src !== civic.src) { img.src = civic.src; } });
    var opts = model ? Array.prototype.slice.call(model.options) : [];

    function filterModels() {
      var mk = make ? make.value : '';
      opts.forEach(function (o, i) {
        var show = i === 0 || o.value === 'Other / not listed' || (mk && o.value.indexOf(mk + ' ') === 0 && cars[mk]);
        o.hidden = o.disabled = !show;
      });
      if (model && model.selectedOptions[0] && model.selectedOptions[0].disabled) model.value = '';
      model && (model.disabled = !mk);
    }
    var reqId = 0, studio = img ? img.closest('.bb-studio') : null;
    function setImage() {
      if (!img) return;
      var mk = make.value, md = model.value, c = cars[mk];
      // model chosen → that model; make only → the make's most popular model (first in the list) as a preview
      var shown = c ? (c.models[md] ? md : Object.keys(c.models)[0]) : '', fam = c && c.models[shown];
      var y = parseInt((f('year') || {}).value, 10), id = ++reqId;
      if (USE_DRAWN && !(CARIMAGES_PRO && CARIMAGES_KEY) && c && window.BB_CARSVG) {
        var kind = (c.body && c.body[shown]) || 'suv', h = 0;
        for (var k = 0; k < shown.length; k++) h = (h * 31 + shown.charCodeAt(k)) >>> 0;
        var svgTxt = window.BB_CARSVG[kind].replace(/var\(--car,#d8dde0\)/g, CAR_COLOURS[h % CAR_COLOURS.length]);
        if (studio) studio.classList.remove('is-loading');
        img.removeAttribute('srcset'); img.removeAttribute('sizes');
        img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgTxt); img.alt = shown + ' illustration';
        img.classList.add('bb-veh-drawn'); fam = fam || shown;
      } else if (CARIMAGES_PRO && CARIMAGES_KEY && c) {
        if (studio) studio.classList.add('is-loading');
        var label = shown.replace(mk + ' ', '');
        fetch('https://carimagesapi.com/api/v1/signed-url?api_key=' + encodeURIComponent(CARIMAGES_KEY) + '&make=' + encodeURIComponent(mk) +
              '&model=' + encodeURIComponent(label) + (y ? '&year=' + y : '') + '&width=800&format=webp&view=front34')
          .then(function (r) { return r.json(); })
          .then(function (d) {
            if (id !== reqId || !d || !d.url) throw 0;
            var pre2 = new Image();
            pre2.onload = function () {
              if (id !== reqId) return;
              img.removeAttribute('srcset'); img.removeAttribute('sizes'); img.src = d.url; img.alt = shown + ' studio render';
              if (studio) studio.classList.remove('is-loading');
            };
            pre2.onerror = function () { if (studio) studio.classList.remove('is-loading'); };
            pre2.src = d.url;
          })
          .catch(function () { if (id === reqId && studio) studio.classList.remove('is-loading'); });
        fam = fam || label;
      } else if (IMAGIN_KEY && fam) {
        var u = 'https://cdn.imagin.studio/getImage?customer=' + encodeURIComponent(IMAGIN_KEY) + '&make=' + c.slug +
          '&modelFamily=' + fam + (y ? '&modelYear=' + y : '') + '&angle=23&zoomType=fullscreen&width=800';
        if (studio) studio.classList.add('is-loading');
        var pre = new Image();          // preload, then swap – keeps the old picture until the new render has arrived
        pre.onload = function () {
          if (id !== reqId) return;
          img.removeAttribute('srcset'); img.removeAttribute('sizes'); img.src = u; img.alt = shown + ' studio render';
          if (studio) studio.classList.remove('is-loading');
        };
        pre.onerror = function () { if (id === reqId && studio) studio.classList.remove('is-loading'); };
        pre.src = u;
      } else if (civic) {
        if (studio) studio.classList.remove('is-loading');
        img.classList.remove('bb-veh-drawn');
        img.src = civic.src; civic.srcset ? img.setAttribute('srcset', civic.srcset) : img.removeAttribute('srcset');
      }
      var drawn = img.classList.contains('bb-veh-drawn');
      var swapped = drawn || (CARIMAGES_PRO && CARIMAGES_KEY) || IMAGIN_KEY;
      if (cap) cap.textContent = (fam && swapped) ? shown.toUpperCase() + (drawn ? ' · ' + ((c.body && c.body[shown]) || 'suv').replace('bigsuv', 'full-size suv').replace('hatch', 'hatchback').toUpperCase() + ' ILLUSTRATION' : ' · ILLUSTRATIVE PREVIEW') : 'HONDA CIVIC · ILLUSTRATIVE PREVIEW';
      if (note) note.textContent = !swapped ? 'Sample vehicle photo' : !fam ? 'Select a make and model to preview it'
        : (c.models[md] ? (drawn ? 'Illustration by body style' : 'Colour and trim may differ') : 'Popular ' + mk + ' shown – pick your model');
    }
    // warm the connection to the image CDN as soon as the checker is on screen
    if (CARIMAGES_KEY || IMAGIN_KEY) { var pc = document.createElement('link'); pc.rel = 'preconnect'; pc.href = CARIMAGES_KEY ? 'https://carimagesapi.com' : 'https://cdn.imagin.studio'; document.head.appendChild(pc); }
    function upd() {
      var md = model && model.value && model.value !== 'Other / not listed' ? model.value : (make ? make.value : '');
      var y = (f('year') || {}).value || '', m = (f('mileage') || {}).value || '';
      if (title) title.textContent = md || 'Let’s meet your car.';
      if (year) year.textContent = y || 'Year';
      if (km) km.textContent = m ? Number(m).toLocaleString('en-CA') + ' km' : 'Mileage';
    }
    if (make) make.addEventListener('change', function () { filterModels(); setImage(); upd(); });
    if (model) model.addEventListener('change', function () { setImage(); upd(); });
    ['year', 'mileage'].forEach(function (k) { var i = f(k); if (i) { i.addEventListener('input', upd); i.addEventListener('change', function () { setImage(); upd(); }); } });
    filterModels();
    $$('.bb-chips button', sec).forEach(function (b) {
      b.addEventListener('click', function () {
        if (!issue) return;
        var add = b.getAttribute('data-add');
        issue.value = issue.value ? issue.value.replace(/\s+$/, '') + (/[.!?]$/.test(issue.value.trim()) ? ' ' : '. ') + add : add;
        issue.focus();
      });
    });

    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function guidance() {
      var txt = issue ? issue.value : '', hits = RULES.filter(function (r) { return r.k.test(txt); }).slice(0, 2);
      var u = hits.reduce(function (a, r) { return Math.max(a, r.u); }, 1);
      var veh = (title && title.textContent !== 'Let’s meet your car.') ? title.textContent : 'your vehicle';
      var h = '<div class="bb-res-head"><span>03 / INSTANT GUIDANCE</span><span class="bb-res-urg bb-u' + u + '">' + URG[u] + '</span></div>' +
        '<h4>What could be happening with ' + esc(veh) + '</h4>';
      if (!hits.length) {
        h += '<p>We couldn’t match your description to a common pattern – that’s fine. A technician will read it and call you with next steps.</p>';
      }
      hits.forEach(function (r) {
        h += '<div class="bb-res-block"><strong>' + r.t + '</strong><ul>' + r.c.map(function (c) { return '<li>' + c + '</li>'; }).join('') +
          '</ul><p><b>Can I drive it?</b> ' + r.d + '</p><p><b>Quick check:</b> ' + r.f + '</p>' +
          '<a href="#services">Related service: ' + r.svc.replace(/&/g, '&amp;') + ' ↗︎</a></div>';
      });
      h += '<p class="bb-res-note">This is general guidance, not a diagnosis. Your details have been sent to our shop.</p>' +
        '<div class="bb-res-cta"><a class="bb-res-book" href="#book">Book an inspection</a><a class="bb-res-call" href="tel:+14039305888">Call (403) 930-5888</a></div>';
      out.innerHTML = h; out.classList.add('is-shown');
    }
    if (form && out && window.jQuery) {
      jQuery(form).on('submit_success', function () { guidance(); setTimeout(function () { out.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 50); });
    }
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

  /* ---------- seamless marquees: clone groups until the strip is wider than the screen ---------- */
  function marquee(track, pxPerSec) {
    var groups = Array.prototype.slice.call(track.children);
    if (!groups.length) return;
    var first = groups[0];
    function setup() {
      var gw = first.getBoundingClientRect().width + (parseFloat(getComputedStyle(track).columnGap) || 0);
      if (!gw) return;
      while (track.children.length < 40 && track.scrollWidth < window.innerWidth + gw * 2) {
        var c = first.cloneNode(true); c.setAttribute('aria-hidden', 'true');
        c.querySelectorAll('img').forEach(function (i) { i.alt = ''; i.loading = 'eager'; });
        track.appendChild(c);
      }
      track.style.setProperty('--bb-shift', (-gw) + 'px');
      track.style.animationDuration = (gw / pxPerSec) + 's';
      track.classList.add('bb-loop');
    }
    setup();
    window.addEventListener('resize', setup);
    window.addEventListener('load', setup);
  }

  /* ---------- /services/: hero photo switch, service cards → request form, form → WhatsApp ---------- */
  function servicesPage(hero) {
    var slides = $$('.bb-sm-slide', hero), btns = $$('.bb-sm-sel', hero), cur = 0, timer;
    function go(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('is-active', i === cur); });
      btns.forEach(function (b, i) { b.classList.toggle('is-active', i === cur); var a = $('a', b); if (a) a.setAttribute('aria-pressed', i === cur); });
    }
    btns.forEach(function (b, i) {
      var a = $('a', b) || b; a.setAttribute('role', 'button');
      a.addEventListener('click', function (e) { e.preventDefault(); go(i); clearInterval(timer); timer = setInterval(function () { go(cur + 1); }, 8000); });
    });
    timer = setInterval(function () { go(cur + 1); }, 8000);
  }
  function serviceRequest(form) {
    var val = function (id) { var f = $('[name="form_fields[' + id + ']"]', form); return f ? f.value.trim() : ''; };
    $$('.bb-sm-card[data-service]').forEach(function (c) {
      c.addEventListener('click', function () {
        var sel = $('[name="form_fields[service]"]', form); if (sel) sel.value = c.getAttribute('data-service');
      });
    });
    // Elementor submits the form (email to the shop); we also open WhatsApp with the same details
    form.addEventListener('submit', function () {
      if (!form.checkValidity()) return;
      var lines = ['Hi Busy Bee, I\'d like to request a service.', 'Name: ' + val('name'), 'Phone: ' + val('phone')];
      if (val('vehicle')) lines.push('Vehicle: ' + val('vehicle'));
      if (val('service')) lines.push('Service: ' + val('service'));
      if (val('issue')) lines.push('Issue: ' + val('issue'));
      window.open('https://wa.me/14039305888?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }

  /* ---------- form guard: blocks bots and sales pitches before Elementor sends the email ----------
     Runs in the capture phase on document, so a blocked submit never reaches Elementor's handler.
     1) bots: no real typing/selection in the form, or submitted < 3 s after the first interaction
     2) links: website addresses are not needed for a car-service request
     3) solicitation: SEO / guest-post / marketing / web-design / crypto pitches
     Server-side backup: Elementor's native honeypot field on every form (see el.harden_forms). */
  var BB_SPAM = /\b(seo|search engine|guest ?post(s|ing)?|back ?links?|link ?building|outreach|digital marketing|marketing (agency|services|campaign)|social media (marketing|management)|lead generation|generate (more )?leads|web ?site (design|redesign|development)|web design|web developer|app development|first page (of|on) google|google (ranking|ads|my business optimi[sz]ation)|rank(ing)? (higher|your|on google)|domain authority|sponsored (post|article|content)|content writ(ing|er)|article submission|ppc|adwords|white ?label|virtual assistant|outsourc(e|ing)|crypto|bitcoin|forex|casino|betting|loan offer|business proposal|partnership opportunit(y|ies)|increase (your )?traffic|grow your business)\b/i;
  function formGuard() {
    var started = new WeakMap();
    document.addEventListener('input', function (e) { var f = e.target.closest && e.target.closest('.bb-guard form'); if (f && !started.has(f)) started.set(f, Date.now()); }, true);
    document.addEventListener('change', function (e) { var f = e.target.closest && e.target.closest('.bb-guard form'); if (f && !started.has(f)) started.set(f, Date.now()); }, true);
    function say(form, msg) {
      var box = form.querySelector('.bb-guard-msg');
      if (!box) { box = document.createElement('div'); box.className = 'bb-guard-msg'; box.setAttribute('role', 'alert'); form.appendChild(box); }
      box.textContent = msg;
    }
    document.addEventListener('submit', function (e) {
      var form = e.target; if (!form.closest || !form.closest('.bb-guard')) return;
      var text = Array.prototype.map.call(form.querySelectorAll('input[type=text],input[type=email],input:not([type]),textarea'),
        function (i) { return i.value; }).join(' ');
      var t0 = started.get(form), why = '';
      if (!t0 || Date.now() - t0 < 3000) why = 'Please take a moment to fill in the form, then send it again.';
      else if (/(https?:\/\/|www\.|\b[a-z0-9-]+\.(com|net|org|io|co|biz|info|xyz|online|site|agency)\b)/i.test(text.replace(/[\w.+-]+@[\w-]+\.[\w.]+/g, '')))
        why = 'Please remove website links – we only need your vehicle details.';
      else if (BB_SPAM.test(text)) why = 'This form is for vehicle service requests only. For anything else, please call (403) 930-5888.';
      if (why) { e.preventDefault(); e.stopImmediatePropagation(); say(form, why); }
      else { var b = form.querySelector('.bb-guard-msg'); if (b) b.remove(); }
    }, true);
  }

  function init() {
    formGuard();
    $$('.bb-sm-hero').forEach(servicesPage);
    $$('.bb-sm-form form').forEach(serviceRequest);
    $$('.bb-sm-brand-track').forEach(function (t) { marquee(t, 57.8); });
    $$('.bb-marquee-track').forEach(function (t) { marquee(t, 940 / 30); });
    $$('.bb-ribbon-track').forEach(function (t) { marquee(t, 1083 / 35); });
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
