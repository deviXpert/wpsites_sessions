"""Elementor JSON builders + shared site parts for Jim Towing. Pure functions -> python dicts (Elementor _elementor_data)."""
import json, os, random, html as _h
D = os.path.dirname(os.path.abspath(__file__))
M = {str(k): v for k, v in json.load(open(os.path.join(D, 'media.json'))).items()}
SITE = 'https://jimtowing.ca'
PHONE, TEL = '587-914-0130', 'tel:+15879140130'
EMAIL = 'jimtowingltd@gmail.com'
MAPS = 'https://maps.app.goo.gl/KbZ8JuHkDmVXuvDW6'
MAP_EMBED = 'https://maps.google.com/maps?cid=5630118754390366668&amp;output=embed'
SOC = [('facebook-f', 'Facebook', 'https://www.facebook.com/share/1Dq5gCGQfT/'),
       ('instagram', 'Instagram', 'https://www.instagram.com/jimtowingltd'),
       ('tiktok', 'TikTok', 'https://www.tiktok.com/@jim.towing.ltd')]
RATING, REVIEWS = '4.9', '51'
BRAND = {
 'facebook-f': '<svg viewBox="0 0 320 512" aria-hidden="true"><path d="M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z"/></svg>',
 'instagram': '<svg viewBox="0 0 448 512" aria-hidden="true"><path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/></svg>',
 'tiktok': '<svg viewBox="0 0 448 512" aria-hidden="true"><path d="M448 209.91a210.06 210.06 0 0 1-122.77-39.25v178.72A162.55 162.55 0 1 1 185 188.31v89.89a74.62 74.62 0 1 0 52.23 71.18V0h88a121.18 121.18 0 0 0 1.86 22.17A122.18 122.18 0 0 0 381 102.39a121.43 121.43 0 0 0 67 20.14z"/></svg>',
 'google': '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'}
def bi(name): return f'<i class="j-bi">{BRAND[name]}</i>'


# image keys -> media id
IMG = {'downtown': 397, 'moto_night': 398, 'moto': 399, 'equip': 400, 'construction': 401, 'suv_op': 402, 'longdist': 403,
       'luxury': 404, 'lift': 405, 'redsuv': 406, 'dealer': 407, 'logo_truck': 408, 'heavy_night': 409, 'winter': 410,
       'dusk': 366, 'night_sedan': 364, 'shop': 365, 'minivan': 363}
def iu(k, size='large'): return M[str(IMG[k])][size]
def ia(k): return M[str(IMG[k])]['alt']
LOGO = M['logo']
LOGO_SM = M['logo_sm']

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
def LIMG(k, eager=False):
    m = M[str(IMG[k])]
    return (f'<img src="{m["ml"]}" srcset="{m.get("h640", m["ml"])} 640w, {m["ml"]} 768w" sizes="(max-width:767px) 92vw, 50vw" width="768" height="1024" alt="{esc(m["alt"])}" '
            + ('' if eager else 'loading="lazy" ') + 'decoding="async">')
def IMGW(k, cls='j-img', size='large'):
    return RAW(LIMG(k), cls)
def _IMGW_old(k, cls='j-img', size='large'):
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
import re as _re
CSS = _re.sub(r'\s*([{}:;,>])\s*', r'\1', _re.sub(r'/\*.*?\*/', '', open(os.path.join(D, 'jim.css')).read(), flags=_re.S)).replace(';}', '}')
JS = open(os.path.join(D, 'jim.js')).read()
LD = {'@context': 'https://schema.org', '@type': 'AutomotiveBusiness', 'additionalType': 'https://schema.org/TowingService',
      '@id': SITE + '/#business', 'name': 'Jim Towing Ltd.', 'url': SITE + '/', 'telephone': '+1-587-914-0130', 'email': EMAIL,
      'image': iu('downtown'), 'logo': LOGO['full'], 'priceRange': 'From $69',
      'address': {'@type': 'PostalAddress', 'addressLocality': 'Calgary', 'addressRegion': 'AB', 'addressCountry': 'CA'},
      'openingHoursSpecification': {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '00:00', 'closes': '23:59'},
      'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': RATING, 'reviewCount': REVIEWS},
      'areaServed': ['Calgary', 'Airdrie', 'Chestermere', 'Okotoks', 'Cochrane', 'Red Deer', 'Edmonton'],
      'hasMap': MAPS, 'sameAs': [u for _, _, u in SOC]}
_GF = 'https://fonts.googleapis.com/css2?family=Outfit:wght@400..900&family=Figtree:wght@400..800&display=swap'
_FA = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
GF_FACES = open(os.path.join(D, 'gfonts.css')).read()
FONTS = (f'<link rel="preload" as="font" type="font/woff2" href="https://fonts.gstatic.com/s/outfit/v15/QGYvz_MVcBeNP4NJtEtq.woff2" crossorigin><link rel="preload" as="font" type="font/woff2" href="https://fonts.gstatic.com/s/figtree/v9/_Xms-HUzqDCFdgfMm4S9DQ.woff2" crossorigin><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>'
         f'<link rel="preload" as="style" href="{_FA}" onload="this.onload=null;this.rel=\'stylesheet\'">'
         f'<noscript><link rel="stylesheet" href="{_FA}"></noscript>')
def assets(): return RAW(f'{FONTS}<script type="application/ld+json">{json.dumps(LD)}</script><style>{GF_FACES}{CSS}</style><script>{JS}</script>', 'j-assets')

def stars(n=5): return '<span class="j-stars" aria-hidden="true">' + '★' * n + '</span>'

# ---------------- header ----------------
def header(menu_slug):
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Jim Towing on {n}">{bi(i)}</a>' for i, n, u in SOC)
    top = C([RAW(f'<div class="j-tb"><span class="j-live"><span class="j-dot"></span>Dispatch online 24/7 &middot; Calgary &amp; surrounding areas</span>'
                 f'<a class="j-hide-m" href="{MAPS}" target="_blank" rel="noopener">{stars()} {RATING} on Google &middot; {REVIEWS} reviews</a></div>'),
             RAW(f'<div class="j-tb"><a class="j-hide-m" href="mailto:{EMAIL}"><i class="fas fa-envelope"></i>{EMAIL}</a><span class="j-soc">{soc}</span></div>')],
            'j-in j-row', fd='row')
    nav = W('nav-menu', 'j-nav', menu=menu_slug, layout='horizontal', align_items='center', submenu_icon={'value': 'fas fa-chevron-down', 'library': 'fa-solid'},
            pointer='none', dropdown='tablet', toggle='burger', full_width='stretch', text_align='aside', toggle_align='right')
    main = C([
        RAW(f'<a class="j-brand" href="{SITE}/" aria-label="Jim Towing Ltd. home"><img src="{LOGO_SM["full"]}" alt="Jim Towing Ltd. logo" width="240" height="224" fetchpriority="high"></a>', 'j-logo'),
        nav,
        RAW(f'<a class="j-hcall" href="{TEL}" aria-label="Call Jim Towing at {PHONE}"><span class="j-ic"><i class="fas fa-phone-alt"></i></span><span><small>24/7 Dispatch</small><b>{PHONE}</b></span></a>', 'j-hcta'),
    ], 'j-in j-row', fd='row')
    hdr = C([C([top], 'j-topbar'), C([main], 'j-mainbar')], 'j-header', tag='header')
    return [C([hdr, RAW('<div class="j-hspace" aria-hidden="true"></div>')], 'j-root')]  # CSS/JS/fonts live in kit Custom CSS + Custom Code (assets.py)

# ---------------- footer ----------------
FMAP = f'<div class="j-fmap"><iframe title="Jim Towing Ltd. on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAP_EMBED}"></iframe></div>'

def footer():
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Jim Towing on {n}">{bi(i)}</a>' for i, n, u in SOC)
    svc = ''.join(f'<li><a href="{surl(s)}">{t}</a></li>' for s, t, *_ in SVC)
    comp = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in [('Home', PAGES['home']), ('All Services', PAGES['services']), ('Service Areas', PAGES['areas']), ('Pricing', PAGES['pricing']), ('About Us', PAGES['about']), ('Contact', PAGES['contact'])])
    areas = {'emergency-towing-calgary': 'Calgary + area', 'flatbed-towing-calgary': 'Calgary + area', 'roadside-assistance-calgary': 'All Calgary',
             'long-distance-towing-alberta': 'Across Alberta', 'battery-jump-start-calgary': 'All Calgary', 'emergency-fuel-delivery-calgary': 'Calgary + area'}
    rows = ''.join(f'<a class="j-db-row" href="{surl(s)}"><span class="n">{i + 1:02d}</span><span class="s"><i class="fas fa-{ic}" aria-hidden="true"></i>{t}</span>'
                   f'<span class="a">{areas[s]}</span><span class="st"><span class="j-dot"></span>Available now</span><i class="fas fa-arrow-right go" aria-hidden="true"></i></a>'
                   for i, (s, t, ic, *_) in enumerate(SVC))
    board = (f'<div class="j-db rv"><div class="j-db-head"><div><small>Live dispatch board</small><b>Jim Towing &middot; Calgary, AB</b></div>'
             f'<div class="j-db-clock"><span class="j-clock" data-tz="America/Edmonton">--:--</span><small>Calgary time &middot; <em class="j-shift">open 24/7</em></small></div></div>'
             f'<div class="j-db-cols" aria-hidden="true"><span>#</span><span>Service</span><span class="a">Coverage</span><span>Status</span></div>{rows}'
             f'<div class="j-db-foot"><span><i class="fas fa-star"></i> {RATING} on Google &middot; {REVIEWS} reviews</span><span><i class="fas fa-tag"></i> Roadside from $69 &middot; Towing from $75</span></div></div>')
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="Jim Towing on {n}">{bi(i)}</a>' for i, n, u in SOC)
    brand = (f'<div class="j-fbrand rv rv-d1"><div class="j-fb-top"><img src="{LOGO_SM["full"]}" alt="Jim Towing Ltd. logo" width="240" height="224" loading="lazy">'
             f'<p>24/7 towing &amp; roadside assistance for Calgary and surrounding Alberta communities.</p></div>'
             f'<a class="j-fb-phone" href="{TEL}"><small>24/7 dispatch line</small>{PHONE}</a>'
             f'<div class="j-fb-meta"><a href="mailto:{EMAIL}"><i class="fas fa-envelope"></i>{EMAIL}</a><span><i class="fas fa-clock"></i>Open 24 hours, 7 days</span></div>'
             f'<div class="j-soc">{soc}</div>{FMAP}</div>')
    links = ''.join(f'<a href="{u}">{t}</a>' for t, u in [('Home', PAGES['home']), ('Services', PAGES['services']), ('Service Areas', PAGES['areas']), ('Pricing', PAGES['pricing']), ('About', PAGES['about']), ('Contact', PAGES['contact'])])
    road = '<div class="j-froad" aria-hidden="true"><div class="j-froad-line"></div><i class="fas fa-truck-pickup j-froad-truck"></i></div>'
    f = C([
        RAW(road),
        C([RAW(f'<div class="j-fmain">{board}{brand}</div>')], 'j-in'),
        C([RAW(f'<div class="j-fbottom"><nav aria-label="Footer">{links}</nav><span>&copy; <span class="j-year">2026</span> Jim Towing Ltd. &middot; Calgary, Alberta</span></div>'
                 f'<div class="j-credit">Designed &amp; developed by <a href="https://hafizahsanali.com/" target="_blank" rel="noopener">Hafiz Ahsan Ali</a><span>&middot;</span>Powered by <a href="https://devixpert.com/" target="_blank" rel="noopener">DeviXpert</a></div>')], 'j-in'),
    ], 'j-footer', tag='footer')
    floats = RAW(f'''<a class="j-fab" href="{TEL}" aria-label="Call Jim Towing 24/7 at {PHONE}"><span><i class="fas fa-phone-alt"></i></span>Call 24/7</a>
<button class="j-totop" aria-label="Back to top"><svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22"/></svg><i class="fas fa-arrow-up"></i></button>
<nav class="j-mbar" aria-label="Quick contact"><a class="call" href="{TEL}"><i class="fas fa-phone-alt"></i>Call Now</a><a href="{PAGES['contact']}#request"><i class="fas fa-paper-plane"></i>Get a Quote</a></nav>''')
    return [C([f, floats], 'j-root')]

# ---------------- shared sections ----------------
def marquee(items=None):
    items = items or ['24/7 Emergency Towing', 'Flatbed Towing', 'Roadside Assistance', 'Long-Distance Transport', 'Battery Jump-Starts', 'Emergency Fuel Delivery', 'Calgary & Area']
    s = ''.join(f'<a href="{surl(sl)}"><i class="fas fa-{ic}" aria-hidden="true"></i>{t}</a>' for sl, t, ic, *_ in SVC)
    return C([RAW(f'<nav class="j-marq-in" aria-label="Our services">{s}<span class="j-marq-dup" aria-hidden="true">{s.replace("<a ", "<a tabindex=" + chr(34) + "-1" + chr(34) + " ")}</span></nav>')], 'j-marq')

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
    badge = RAW(f'<a class="j-gbadge" href="{MAPS}" target="_blank" rel="noopener"><span class="g">{bi("google")}</span><b>{RATING}</b><span>{stars()}<small>Based on {REVIEWS} Google reviews</small></span></a>')
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
    figs = ''.join(f'<figure><img src="{iu(k, "ml")}" data-full="{iu(k, "large")}" alt="{esc(ia(k))}" loading="lazy" decoding="async" width="768" height="1024"></figure>' for k in keys)
    return C([C([head('Our work', title, 'Real jobs, real trucks, real Calgary roads — from downtown pickups to winter recoveries and motorcycle transport.', True)], 'j-in j-col'),
              RAW(f'<div class="j-gal"><div class="j-gal-in">{figs}</div></div>')], 'j-sec ' + cls, tag='section')

def steps(items, title='How Jim Towing ' + hl('Works'), eyebrow='Simple process', light=False, lead=None):
    st = ''.join(f'<div class="j-step" data-n="{i + 1:02d}"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(items))
    road = f'<div class="j-road{" j-light" if light else ""}"><div class="j-road-line"><div class="j-road-fill"></div></div><i class="fas fa-truck-pickup j-truck" aria-hidden="true"></i><div class="j-steps">{st}</div></div>'
    return sec([head(eyebrow, title, lead), RAW(road, 'rv')], ('j-paper' if light else 'j-dark j-grain'))

FACT_IC = [('price', 'tag'), ('roadside', 'tools'), ('towing', 'truck-pickup'), ('flatbed', 'truck-loading'), ('long', 'route'), ('confirmed', 'check-circle'),
           ('best', 'car-side'), ('method', 'truck-loading'), ('route', 'route'), ('hour', 'clock'), ('area', 'map-marked-alt'), ('where', 'map-marker-alt'),
           ('nearby', 'map-signs'), ('calgary', 'city'), ('based', 'map-pin'), ('rating', 'star'), ('email', 'envelope'), ('service', 'truck-pickup')]
def _fic(label):
    k = label.lower()
    return next((i for w, i in FACT_IC if w in k), 'info-circle')
def ticket_html(facts):
    import re as _re
    rows, price = '', ''
    for k, v in facts:
        if k.lower() == 'phone': continue
        if k.lower() in ('starting price', 'price'):
            m = _re.search(r'\$\d+', v)
            rest = _re.sub(r'^\s*(From\s*)?\$\d+\s*', '', v).strip(' —-()')
            price = (f'<div class="j-tk-price"><span>Starting<br>from</span><b>{m.group(0)}</b><small>{(rest[:1].upper() + rest[1:]) if rest else "Price confirmed before dispatch"}</small></div>' if m
                     else f'<div class="j-tk-price"><span>Pricing</span><small class="j-tk-price-q">{v}</small></div>')
            continue
        rows += f'<li><i class="fas fa-{_fic(k)}" aria-hidden="true"></i><div><span>{k}</span><b>{v}</b></div></li>'
    return (f'<aside class="j-ticket" aria-label="Key facts"><div class="j-tk-head"><span class="j-tk-ic"><i class="fas fa-clipboard-list"></i></span><div><small>At a glance</small><h2>Key facts</h2></div>'
            f'<span class="j-tk-live"><span class="j-dot"></span>Online 24/7</span></div><ul class="j-tk-rows">{rows}</ul>{price}'
            f'<a class="j-tk-call" href="{TEL}"><span class="ic"><i class="fas fa-phone-alt"></i></span><span><small>Tap to call · 24/7 dispatch</small><b>{PHONE}</b></span><i class="fas fa-arrow-right" aria-hidden="true"></i></a></aside>')

def hero_img(k):
    m = M[str(IMG[k])]
    return RAW(f'<img src="{m.get("h640", m["ml"])}" srcset="{m.get("h640", m["ml"])} 640w, {m["1536"]} {m["w1536"]}w" sizes="100vw" width="640" height="853" alt="{esc(m["alt"])}" fetchpriority="high" decoding="async">', 'j-hero-bg')

def page_hero(crumb, h1, lead, facts, img=None, extra=None):
    ticket = RAW(ticket_html(facts), 'j-ticket-w j-up j-up2')
    bg = hero_img(img) if img else None
    cr = f'<nav class="j-crumb" aria-label="Breadcrumb"><a href="{SITE}/">Home</a><span>/</span>' + ''.join(f'<a href="{u}">{t}</a><span>/</span>' for t, u in crumb[:-1]) + f'<em>{crumb[-1][0]}</em></nav>'
    return C([bg, C([C([RAW(cr), H(h1, 'h1', 'j-splitw'), P(lead, 'j-lead j-up j-up2'), BTNS(CALL(), QUOTE(), cls='j-up j-up3'), extra], 'j-phero-copy j-col'), ticket], 'j-in', fd='row')], 'j-phero', tag='section')

def wrap(els): return [C(els, 'j-root')]
