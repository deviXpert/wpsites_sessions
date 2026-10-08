"""Elementor JSON builders + shared site parts for Jim Towing. Pure functions -> python dicts (Elementor _elementor_data)."""
import json, os, random, html as _h
D = os.path.dirname(os.path.abspath(__file__))
M = {str(k): v for k, v in json.load(open(os.path.join(D, 'media.json'))).items()}
SITE = 'https://jimtowing.ca'
PHONE, TEL = '587-914-0130', 'tel:+15879140130'
EMAIL = 'jimtowingltd@gmail.com'
MAPS = 'https://maps.app.goo.gl/KbZ8JuHkDmVXuvDW6'
SOC = [('facebook-f', 'Facebook', 'https://www.facebook.com/share/1Dq5gCGQfT/'),
       ('instagram', 'Instagram', 'https://www.instagram.com/jimtowingltd'),
       ('tiktok', 'TikTok', 'https://www.tiktok.com/@jim.towing.ltd')]
RATING, REVIEWS = '4.9', '51'

# image keys -> media id
IMG = {'downtown': 397, 'moto_night': 398, 'moto': 399, 'equip': 400, 'construction': 401, 'suv_op': 402, 'longdist': 403,
       'luxury': 404, 'lift': 405, 'redsuv': 406, 'dealer': 407, 'logo_truck': 408, 'heavy_night': 409, 'winter': 410,
       'dusk': 366, 'night_sedan': 364, 'shop': 365, 'minivan': 363}
def iu(k, size='large'): return M[str(IMG[k])][size]
def ia(k): return M[str(IMG[k])]['alt']
LOGO = M['logo']

# service registry (final URLs)
SVC = [
    ('emergency-towing-calgary', '24/7 Emergency Towing', 'truck-pickup', 'redsuv', 'Breakdowns, accidents and vehicles that are unsafe to drive — towed to your home, mechanic, body shop or dealership.'),
    ('flatbed-towing-calgary', 'Professional Flatbed Towing', 'truck-loading', 'luxury', 'All four wheels off the road for AWD, luxury, lowered, motorcycle and accident-damaged vehicles.'),
    ('roadside-assistance-calgary', 'Roadside Assistance', 'tools', 'suv_op', 'Jump-starts, flat tire changes, fuel delivery and lockout help — often fixed on the spot, no tow needed.'),
    ('long-distance-towing-alberta', 'Long-Distance Vehicle Transport', 'route', 'longdist', 'Secure transport from Calgary to Airdrie, Okotoks, Cochrane, Red Deer, Edmonton and across Alberta.'),
    ('battery-jump-start-calgary', 'Battery Jump-Start Service', 'car-battery', 'dusk', 'Dead or weak battery at home, work or in a parkade? We come to you with professional boost equipment.'),
    ('emergency-fuel-delivery-calgary', 'Emergency Fuel Delivery', 'gas-pump', 'night_sedan', 'Ran out of gas? We bring enough fuel to get you to the nearest station — day or night.'),
]
def surl(slug): return f'{SITE}/services/{slug}/'
PAGES = {'home': SITE + '/', 'services': SITE + '/services/', 'areas': SITE + '/service-areas/', 'pricing': SITE + '/pricing/',
         'about': SITE + '/about/', 'contact': SITE + '/contact/'}

# ---------------- element primitives ----------------
_rng = random.Random(1)
def seed(s): _rng.seed(s)
def rid(): return '%07x' % _rng.getrandbits(28)
def _z(): return {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
def C(els, cls='', tag='div', **s):
    st = {'content_width': 'full', 'flex_direction': s.pop('fd', 'column'), 'padding': _z(), 'margin': _z(),
          'flex_gap': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'isLinked': True},
          'css_classes': (cls + ' e-no-lazyload').strip(), 'html_tag': tag}
    st.update(s)
    return {'id': rid(), 'elType': 'container', 'isInner': False, 'settings': st, 'elements': [e for e in els if e]}
def W(t, cls='', **s):
    if cls: s['_css_classes'] = cls
    return {'id': rid(), 'elType': 'widget', 'widgetType': t, 'isInner': False, 'settings': s, 'elements': []}
def ICO(v, lib='fa-solid'): return {'value': ('fab fa-' if lib == 'fa-brands' else 'fas fa-') + v, 'library': lib}
def H(t, tag='h2', cls='j-h2'): return W('heading', 'j-h ' + cls, title=t, header_size=tag)
def T(html, cls=''): return W('text-editor', ('j-t ' + cls).strip(), editor=html)
def P(txt, cls=''): return T(f'<p>{txt}</p>', cls)
def RAW(h, cls=''): return W('html', cls, html=h)
def EB(t): return T(f'<p>{t}</p>', 'j-eyebrow')
def BTN(t, url, cls='', icon=None, after=False):
    if icon is None: icon = 'phone-alt' if url.startswith('tel:') else 'arrow-right'
    extra = ' j-ring' if url.startswith('tel:') else ''
    return W('button', ('j-btn ' + cls + extra).strip(), text=t, link={'url': url, 'is_external': '', 'nofollow': ''},
             selected_icon=ICO(icon), icon_align='row-reverse' if after else 'row', icon_indent={'unit': 'px', 'size': 10})
def CALL(cls=''): return BTN(f'Call {PHONE}', TEL, cls)
def QUOTE(cls='j-btn-ghost', url=None): return BTN('Request Service', url or PAGES['contact'] + '#request', cls, 'paper-plane', True)
def BTNS(*b, cls=''): return C(list(b), 'j-btns ' + cls, fd='row')
def IMGW(k, cls='j-img', size='large'):
    return W('image', cls, image={'url': iu(k, 'full'), 'id': IMG[k]}, image_size=size)
def ul(items, cls='j-checks'): return T('<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>', cls)
def ol(items): return T('<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>', 'j-ol')
def esc(s): return _h.escape(s, quote=True)
def hl(s): return f'<span class="j-hl">{s}</span>'
def sec(els, cls='', tag='section', inner_cls='', **kw):
    return C([C(els, 'j-in j-col ' + inner_cls)], 'j-sec ' + cls, tag=tag, **kw)
def head(eyebrow, title, lead=None, center=False, cls=''):
    return C([EB(eyebrow), H(title, 'h2', 'j-h2'), P(lead, 'j-lead') if lead else None], f'j-head rv {"j-center" if center else ""} {cls}')
def headrow(eyebrow, title, lead, btn=None):
    return C([C([EB(eyebrow), H(title, 'h2', 'j-h2')], 'j-col'), C([P(lead, 'j-lead'), btn], 'j-col')], 'j-headrow j-row j-wrap rv', fd='row')

# ---------------- shared assets ----------------
CSS = open(os.path.join(D, 'jim.css')).read()
JS = open(os.path.join(D, 'jim.js')).read()
LD = {'@context': 'https://schema.org', '@type': 'AutomotiveBusiness', 'additionalType': 'https://schema.org/TowingService',
      '@id': SITE + '/#business', 'name': 'Jim Towing Ltd.', 'url': SITE + '/', 'telephone': '+1-587-914-0130', 'email': EMAIL,
      'image': iu('downtown'), 'logo': LOGO['full'], 'priceRange': 'From $69',
      'address': {'@type': 'PostalAddress', 'addressLocality': 'Calgary', 'addressRegion': 'AB', 'addressCountry': 'CA'},
      'openingHoursSpecification': {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '00:00', 'closes': '23:59'},
      'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': RATING, 'reviewCount': REVIEWS},
      'areaServed': ['Calgary', 'Airdrie', 'Chestermere', 'Okotoks', 'Cochrane', 'Red Deer', 'Edmonton'],
      'hasMap': MAPS, 'sameAs': [u for _, _, u in SOC]}
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400..900&family=Figtree:wght@400..800&display=swap"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">'
def assets(): return RAW(f'{FONTS}<script type="application/ld+json">{json.dumps(LD)}</script><style>{CSS}</style><script>{JS}</script>', 'j-assets')

def stars(n=5): return '<span class="j-stars" aria-hidden="true">' + '★' * n + '</span>'

# ---------------- header ----------------
def header(menu_slug):
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Jim Towing on {n}"><i class="fab fa-{i}"></i></a>' for i, n, u in SOC)
    top = C([RAW(f'<div class="j-tb"><span class="j-live"><span class="j-dot"></span>Dispatch online 24/7 &middot; Calgary &amp; surrounding areas</span>'
                 f'<a class="j-hide-m" href="{MAPS}" target="_blank" rel="noopener">{stars()} {RATING} on Google &middot; {REVIEWS} reviews</a></div>'),
             RAW(f'<div class="j-tb"><a class="j-hide-m" href="mailto:{EMAIL}"><i class="fas fa-envelope"></i>{EMAIL}</a><span class="j-soc">{soc}</span></div>')],
            'j-in j-row', fd='row')
    nav = W('nav-menu', 'j-nav', menu=menu_slug, layout='horizontal', align_items='center', submenu_icon={'value': 'fas fa-chevron-down', 'library': 'fa-solid'},
            pointer='none', dropdown='tablet', toggle='burger', full_width='stretch', text_align='aside', toggle_align='right')
    main = C([
        RAW(f'<a class="j-brand" href="{SITE}/" aria-label="Jim Towing Ltd. home"><img src="{LOGO["full"]}" alt="Jim Towing Ltd. logo" width="830" height="773" style="width:64px;height:auto"></a>', 'j-logo'),
        nav,
        RAW(f'<a class="j-hcall" href="{TEL}" aria-label="Call Jim Towing at {PHONE}"><span class="j-ic"><i class="fas fa-phone-alt"></i></span><span><small>24/7 Dispatch</small><b>{PHONE}</b></span></a>', 'j-hcta'),
    ], 'j-in j-row', fd='row')
    hdr = C([C([top], 'j-topbar'), C([main], 'j-mainbar')], 'j-header', tag='header')
    return [C([assets(), hdr, RAW('<div class="j-hspace" aria-hidden="true"></div>')], 'j-root')]

# ---------------- footer ----------------
FMAP = (f'<div class="j-fmap"><iframe title="Jim Towing service area map — Calgary, Alberta" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
        f'src="https://maps.google.com/maps?q=Calgary%2C%20AB&amp;z=10&amp;output=embed"></iframe><i class="fas fa-map-marker-alt j-fmap-pin" aria-hidden="true"></i>'
        f'<div class="j-fmap-card"><b>Serving Calgary &amp; surrounding areas — 24/7</b><p>Airdrie, Chestermere, Okotoks, Cochrane and long-distance transport across Alberta.</p>'
        f'<a href="{MAPS}" target="_blank" rel="noopener"><i class="fab fa-google"></i> View us on Google Maps</a></div></div>')
def footer():
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Jim Towing on {n}"><i class="fab fa-{i}"></i></a>' for i, n, u in SOC)
    svc = ''.join(f'<li><a href="{surl(s)}">{t}</a></li>' for s, t, *_ in SVC)
    comp = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in [('Home', PAGES['home']), ('All Services', PAGES['services']), ('Service Areas', PAGES['areas']), ('Pricing', PAGES['pricing']), ('About Us', PAGES['about']), ('Contact', PAGES['contact'])])
    grid = RAW(f'''<div class="j-foot-grid"><div class="j-fabout"><img src="{LOGO['full']}" alt="Jim Towing Ltd. logo" width="830" height="773" loading="lazy"><p>24/7 towing and roadside assistance in Calgary and surrounding Alberta communities — fast dispatch, safe vehicle handling and clear communication when you need it most.</p><div class="j-soc">{soc}</div></div>
<nav aria-label="Services"><h4>Services</h4><ul class="j-flinks">{svc}</ul></nav>
<nav aria-label="Company"><h4>Company</h4><ul class="j-flinks">{comp}</ul></nav>
<div><h4>Get Help Now</h4><div class="j-fcontact"><a href="{TEL}"><i class="fas fa-phone-alt"></i><span><small>Call or text 24/7</small><b>{PHONE}</b></span></a><a href="mailto:{EMAIL}"><i class="fas fa-envelope"></i><span><small>Email</small><b style="font-size:15px">{EMAIL}</b></span></a><a href="{MAPS}" target="_blank" rel="noopener"><i class="fas fa-map-marker-alt"></i><span><small>Service area</small><b style="font-size:15px">Calgary, Alberta &amp; area</b></span></a><div><i class="fas fa-clock"></i><span><small>Hours</small><b style="font-size:15px">Open 24 hours, 7 days</b></span></div></div></div></div>''')
    f = C([
        C([RAW(FMAP), grid], 'j-in'),
        RAW('<div class="j-fbig" aria-hidden="true">Jim Towing</div>'),
        C([RAW(f'<div class="j-fbottom"><span>&copy; <span class="j-year">2026</span> Jim Towing Ltd. All rights reserved.</span><span>Towing &amp; roadside assistance &middot; Calgary, Alberta</span></div>')], 'j-in'),
    ], 'j-footer', tag='footer')
    floats = RAW(f'''<a class="j-fab" href="{TEL}" aria-label="Call Jim Towing 24/7 at {PHONE}"><span><i class="fas fa-phone-alt"></i></span>Call 24/7</a>
<button class="j-totop" aria-label="Back to top"><svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22"/></svg><i class="fas fa-arrow-up"></i></button>
<nav class="j-mbar" aria-label="Quick contact"><a class="call" href="{TEL}"><i class="fas fa-phone-alt"></i>Call Now</a><a href="{PAGES['contact']}#request"><i class="fas fa-paper-plane"></i>Get a Quote</a></nav>''')
    return [C([f, floats], 'j-root')]

# ---------------- shared sections ----------------
def marquee(items=None):
    items = items or ['24/7 Emergency Towing', 'Flatbed Towing', 'Roadside Assistance', 'Long-Distance Transport', 'Battery Jump-Starts', 'Emergency Fuel Delivery', 'Calgary & Area']
    s = ''.join(f'<a href="{surl(sl)}"><i class="fas fa-{ic}" aria-hidden="true"></i>{t}</a>' for sl, t, ic, *_ in SVC)
    return C([RAW(f'<nav class="j-marq-in" aria-label="Our services">{s}<span aria-hidden="true" style="display:contents">{s.replace("<a ", "<a tabindex=" + chr(34) + "-1" + chr(34) + " ")}</span></nav>')], 'j-marq')

def faq_section(items, title='Frequently Asked ' + hl('Questions'), lead='Straight answers to the questions Calgary drivers ask us most. Still unsure? Call — a real person answers 24/7.', cls='j-white'):
    acc = W('accordion', 'j-faq', tabs=[{'_id': rid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in items], faq_schema='yes',
            selected_icon=ICO('plus'), selected_active_icon=ICO('minus'), title_html_tag='h3', icon_align='right')
    return sec([C([
        C([EB('FAQs'), H(title, 'h2', 'j-h2'), P(lead, 'j-lead'), BTNS(CALL())], 'j-faq-intro j-col rv'),
        C([acc], 'j-col rv rv-d1'),
    ], 'j-split', fd='row')], cls)

def cta(title='Need Towing in ' + hl('Calgary?'), text="Don't let a breakdown, accident or roadside emergency leave you stranded. Jim Towing is ready 24/7 — one call gets the right help moving.", cls='j-white'):
    tags = ''.join(f'<span><i class="fas fa-check-circle"></i>{t}</span>' for t in ['Fast response', 'Professional service', 'Safe vehicle transport', '24/7 assistance'])
    return sec([C([
        C([H(title, 'h2', 'j-h2'), P(text), RAW(f'<div class="j-tags">{tags}</div>')], 'j-cta-copy j-col'),
        C([RAW(f'<a class="j-bigphone" href="{TEL}"><small>Call now — 24/7 dispatch</small>{PHONE}</a>'), BTNS(QUOTE('j-btn'))], 'j-cta-phone j-col'),
    ], 'j-cta rv rv-s', fd='row')], cls + ' j-sec-tight')

def reviews(cls='j-paper'):
    badge = RAW(f'<a class="j-gbadge" href="{MAPS}" target="_blank" rel="noopener"><span class="g"><i class="fab fa-google" style="color:#4285F4"></i></span><b>{RATING}</b><span>{stars()}<small>Based on {REVIEWS} Google reviews</small></span></a>')
    acts = BTNS(BTN('Read our Google reviews', MAPS, 'j-btn-dark j-btn-sm', 'external-link-alt', True))
    return sec([C([C([EB('Reviews'), H('Calgary Drivers ' + hl('Trust Jim Towing'), 'h2', 'j-h2'), P(f'Rated {RATING} out of 5 by {REVIEWS} customers on Google — for fast dispatch, fair pricing and careful handling.', 'j-lead')], 'j-col'), C([badge, acts], 'j-col j-stack')], 'j-headrow j-row j-wrap rv', fd='row'),
                C([W('shortcode', 'j-reviews-sc', shortcode='[trustindex no-registration=google]')], 'rv')], cls + ' j-sec-tight')

def related(slugs, title='Related ' + hl('Services')):
    cards = ''
    for s, t, ic, im, d in SVC:
        if s in slugs:
            cards += f'<a class="j-rc rv" href="{surl(s)}"><img src="{iu(im, "med")}" alt="{esc(ia(im))}" loading="lazy" width="225" height="300"><span><b>{t}</b><small>Learn more</small></span><i class="fas fa-arrow-right" aria-hidden="true"></i></a>'
    for k, t, d in [('pricing', 'Pricing', 'Rates from $69'), ('areas', 'Service Areas', 'Calgary &amp; Alberta')]:
        if k in slugs:
            cards += f'<a class="j-rc rv" href="{PAGES[k]}"><img src="{iu("downtown" if k == "areas" else "logo_truck", "med")}" alt="" loading="lazy" width="225" height="300"><span><b>{t}</b><small>{d}</small></span><i class="fas fa-arrow-right" aria-hidden="true"></i></a>'
    return sec([head('Keep exploring', title), RAW(f'<div class="j-rel">{cards}</div>')], 'j-paper j-sec-tight')

def gallery(keys=None, cls='j-dark j-grain', title='On The Job ' + hl('Across Calgary')):
    keys = keys or ['downtown', 'winter', 'moto_night', 'dealer', 'construction', 'heavy_night', 'luxury', 'lift', 'minivan', 'suv_op', 'shop', 'logo_truck']
    figs = ''.join(f'<figure><img src="{iu(k, "ml")}" data-full="{iu(k, "large")}" alt="{esc(ia(k))}" decoding="async" width="768" height="1024"></figure>' for k in keys)
    return C([C([head('Our work', title, 'Real jobs, real trucks, real Calgary roads — from downtown pickups to winter recoveries and motorcycle transport.', True)], 'j-in j-col'),
              RAW(f'<div class="j-gal"><div class="j-gal-in">{figs}</div></div>')], 'j-sec ' + cls, tag='section')

def steps(items, title='How Jim Towing ' + hl('Works'), eyebrow='Simple process', light=False, lead=None):
    st = ''.join(f'<div class="j-step" data-n="{i + 1:02d}"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(items))
    road = f'<div class="j-road{" j-light" if light else ""}"><div class="j-road-line"><div class="j-road-fill"></div></div><i class="fas fa-truck-pickup j-truck" aria-hidden="true"></i><div class="j-steps">{st}</div></div>'
    return sec([head(eyebrow, title, lead), RAW(road, 'rv')], ('j-paper' if light else 'j-dark j-grain'))

def page_hero(crumb, h1, lead, facts, img=None, extra=None):
    dl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    ticket = RAW(f'<aside class="j-ticket" aria-label="Key facts"><div class="j-ticket-in"><h2>Key facts</h2><dl>{dl}</dl></div><div class="j-ticket-foot"><b>Dispatch online now</b><a href="{TEL}"><i class="fas fa-phone-alt"></i> Call</a></div></aside>', 'j-ticket-w rv rv-r')
    bg = W('image', 'j-hero-bg', image={'url': iu(img, 'full'), 'id': IMG[img]}, image_size='1536x1536') if img else None
    cr = f'<nav class="j-crumb" aria-label="Breadcrumb"><a href="{SITE}/">Home</a><span>/</span>' + ''.join(f'<a href="{u}">{t}</a><span>/</span>' for t, u in crumb[:-1]) + f'<em>{crumb[-1][0]}</em></nav>'
    return C([bg, C([C([RAW(cr), H(h1, 'h1', 'j-splitw'), P(lead, 'j-lead rv'), BTNS(CALL(), QUOTE()), extra], 'j-phero-copy j-col'), ticket], 'j-in', fd='row')], 'j-phero', tag='section')

def wrap(els): return [C(els, 'j-root')]
