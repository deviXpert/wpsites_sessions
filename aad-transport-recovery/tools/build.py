import json, random, copy, sys, os
sys.path.insert(0, os.path.dirname(__file__))
B = os.path.join(os.path.dirname(__file__), 'wp-backup')
P = {p['id']: p for p in json.load(open(f'{B}/pages.json'))}
L = {t['id']: t for t in json.load(open(f'{B}/elementor_library.json'))}
U = 'https://maroon-raven-160825.hostingersite.com'
UP = U + '/wp-content/uploads/2026/09/'
PHONE, TEL = '07771 004242', 'tel:07771004242'

random.seed(7)
def rid(): return '%07x' % random.getrandbits(28)
def C(els, cls='', **s):
    st = {'content_width': s.pop('cw', 'full'), 'padding': s.pop('pad', z()), 'flex_gap': {'unit': 'px', 'size': s.pop('gap', 0), 'column': str(s.get('_g', 0)), 'row': '0', 'isLinked': True}}
    fd, fw = s.get('flex_direction', 'column'), s.get('flex_wrap', '')
    extra = ('x-dr' if fd == 'row' else 'x-dc') + (' x-wrap' if fw == 'wrap' else '') + (' x-bx' if st['content_width'] == 'boxed' else '') + ' e-no-lazyload'
    st['css_classes'] = (cls + ' ' + extra).strip()
    st.update(s)
    return {'id': rid(), 'elType': 'container', 'isInner': False, 'settings': st, 'elements': els}
def z(): return {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
def W(t, cls='', **s):
    if cls: s['_css_classes'] = cls
    return {'id': rid(), 'elType': 'widget', 'widgetType': t, 'isInner': False, 'settings': s, 'elements': []}
def H(t, tag='h2', cls=''): return W('heading', 'x-h ' + cls, title=t, header_size=tag)
def T(html, cls=''): return W('text-editor', 'x-t ' + cls, editor=html)
def BTN(t, url, cls='x-btn'):
    ic, al = ('phone-alt', 'row') if 'Call' in t else ('arrow-right', 'row-reverse') if 'Learn' in t else ('file-signature', 'row')
    return W('button', cls, text=t, link={'url': url, 'is_external': '', 'nofollow': ''}, selected_icon=ICO(ic), icon_align=al, icon_indent={'unit': 'px', 'size': 10})
def ICO(v): return {'value': 'fas fa-' + v, 'library': 'fa-solid'}
def RAW(h): return W('html', '', html=h)

home = json.loads(P[25]['meta']['_elementor_data'])
def find(n, pred, out):
    for e in n:
        if pred(e): out.append(e)
        find(e.get('elements', []), pred, out)
    return out
def one(t): return find(home, lambda e: e.get('widgetType') == t, [])[0]
form = copy.deepcopy(one('form')['settings'])
for f in form['form_fields']:
    if f.get('field_type') == 'select': f['field_options'] = 'Please choose a service|\nOther / Not sure'  # full list filled in by link_pages.py
form.update(selected_button_icon={'value': 'fas fa-paper-plane', 'library': 'fa-solid'}, button_icon_align='row-reverse', button_icon_indent={'unit': 'px', 'size': 10})
faq = copy.deepcopy(one('accordion')['settings'])
gmap = copy.deepcopy(one('google_maps')['settings'])
for k in ('_margin', '_border_radius'): gmap.pop(k, None)
faq['faq_schema'] = 'yes'
faq['selected_icon'] = ICO('plus'); faq['selected_active_icon'] = ICO('minus')
imgboxes = [e['settings'] for e in find(home, lambda e: e.get('widgetType') == 'image-box', [])]
services, why = imgboxes[:16], imgboxes[16:]
lists = [e['settings']['editor'] for e in find(home, lambda e: e.get('widgetType') == 'text-editor', []) if e['settings']['editor'].startswith('<ul>')]
def te(sub): return [e['settings']['editor'] for e in find(home, lambda e: e.get('widgetType') == 'text-editor', []) if sub in e['settings']['editor']][0]

CSS = open(os.path.join(os.path.dirname(__file__), 'redesign.css')).read()
JS = open(os.path.join(os.path.dirname(__file__), 'redesign.js')).read()
LD = json.dumps({'@context': 'https://schema.org', '@type': 'AutomotiveBusiness', 'additionalType': 'https://schema.org/TowingService', 'name': 'AAD Transport & Recovery', 'url': U + '/', 'telephone': '+447771004242', 'email': 'general@aadtransportrecovery.co.uk', 'image': U + '/wp-content/uploads/2026/09/A.A.D-Logo-TP.webp', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Walsall Rd', 'addressLocality': 'Birmingham', 'addressRegion': 'West Midlands', 'postalCode': 'B42 1TQ', 'addressCountry': 'GB'}, 'openingHoursSpecification': {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '00:00', 'closes': '23:59'}, 'areaServed': ['Birmingham', 'West Midlands', 'Erdington', 'Perry Barr', 'Aston', 'Sutton Coldfield', 'Solihull', 'West Bromwich', 'Walsall', 'Dudley']})
ASSETS = RAW(f'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><script type="application/ld+json">{LD}</script><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Figtree:wght@400;500;600;700&display=swap"><style>{CSS}</style><script>{JS}</script>')

# ---------- HEADER ----------
hdr_nav = copy.deepcopy(find(json.loads(L[241]['meta']['_elementor_data']), lambda e: e.get('widgetType') == 'nav-menu', [])[0]['settings'])
for k in list(hdr_nav):
    if k.startswith(('menu_typography_font_size_', 'menu_typography_line_height_')): hdr_nav.pop(k)
hdr_nav.update(menu_typography_font_family='Figtree', dropdown_typography_font_family='Figtree', pointer='underline', animation_line='grow', __globals__={}, color_menu_item='#011D5E', color_menu_item_hover='#FE6402',
               pointer_color_menu_item_hover='#FE6402', color_menu_item_active='#FE6402', pointer_color_menu_item_active='#FE6402',
               dropdown='tablet', toggle_color='#011D5E', background_color_dropdown_item='#FFFFFF', color_dropdown_item='#011D5E',
               color_dropdown_item_hover='#FE6402', background_color_dropdown_item_hover='#FFF4EC', _css_classes='x-nav')
# Service menu (mega menu, mobile drawer and footer all read from this): (group, [(label, slug, icon, blurb)])
MENU = [
    ('Vehicle Recovery', [
        ('Emergency Breakdown Recovery', 'emergency-breakdown-recovery-birmingham', 'exclamation-triangle', 'Fast 24/7 roadside rescue'),
        ('Accident Recovery', 'accident-recovery-birmingham', 'car-crash', 'Damaged &amp; non-drivable vehicles'),
        ('Flatbed Recovery', 'flatbed-recovery-birmingham', 'truck-loading', 'Safe transport for non-runners'),
        ('Wheel-Lift Recovery', 'wheel-lift-recovery-birmingham', 'truck-pickup', 'Quick towing for cars &amp; vans'),
        ('Heavy-Duty Recovery', 'heavy-duty-recovery-birmingham', 'truck-moving', 'Heavy &amp; commercial vehicles'),
        ('Motorcycle Recovery', 'motorcycle-recovery-birmingham', 'motorcycle', 'Motorbike breakdowns &amp; accidents'),
        ('RV &amp; Trailer Recovery', 'rv-trailer-recovery-birmingham', 'caravan', 'Motorhomes, caravans &amp; trailers')]),
    ('Towing &amp; Transport', [
        ('Towing Service', 'towing-service-birmingham', 'truck', '24/7 vehicle towing'),
        ('Commercial Vehicle Towing', 'commercial-vehicle-towing-birmingham', 'shipping-fast', 'Vans &amp; business vehicles'),
        ('Long-Distance Recovery', 'long-distance-recovery-birmingham', 'route', 'Recovery &amp; transport UK-wide'),
        ('Vehicle Transport', 'vehicle-transport-birmingham', 'car-side', 'Garage moves &amp; car transport')]),
    ('Roadside Assistance', [
        ('Roadside Assistance', 'roadside-assistance-birmingham', 'tools', 'Breakdown help at the roadside'),
        ('Flat Battery Service', 'flat-battery-service-birmingham', 'car-battery', 'Jump starts &amp; battery help'),
        ('Flat Tyre Services', 'flat-tyre-services-birmingham', 'circle-notch', 'Punctures &amp; tyre problems'),
        ('Fuel Delivery', 'fuel-delivery-services-birmingham', 'gas-pump', 'Out of fuel? We can help'),
        ('Car Lockout Service', 'car-lockout-service-birmingham', 'key', 'Locked out of your vehicle')]),
]
TOP = [('Home', U + '/'), ('Services', U + '/services/'), ('About Us', U + '/about-us/'), ('Contact Us', U + '/contact/')]
def mega_html():
    item = lambda t, s, i, d: f'<a class="x-mm-item" href="{U}/{s}/"><span class="x-mm-ic"><i class="fas fa-{i}" aria-hidden="true"></i></span><span class="x-mm-tx"><span class="x-mm-tt">{t}</span><span class="x-mm-ds">{d}</span></span></a>'
    groups = ''.join(f'<div class="x-mm-col"><p class="x-mm-gh">{g}</p>{"".join(item(*x) for x in xs)}</div>' for g, xs in MENU)
    promo = (f'<div class="x-mm-promo"><p class="x-mm-pk">24/7 Recovery</p><p class="x-mm-pt">Broken Down Right Now?</p><p class="x-mm-pd">Operators are standing by day and night across Birmingham &amp; the West Midlands.</p>'
             f'<a class="x-mm-call" href="{TEL}"><i class="fas fa-phone-alt" aria-hidden="true"></i> {PHONE}</a><a class="x-mm-all" href="{U}/services/">View All Services <i class="fas fa-arrow-right" aria-hidden="true"></i></a></div>')
    links = ''.join(
        f'<li class="x-mm-has"><a class="x-mm-link" href="{u}" aria-haspopup="true" aria-expanded="false">{t} <i class="fas fa-chevron-down" aria-hidden="true"></i></a>'
        f'<div class="x-mm-panel"><div class="x-mm-grid">{groups}{promo}</div></div></li>' if t == 'Services' else f'<li><a class="x-mm-link" href="{u}">{t}</a></li>' for t, u in TOP)
    dwl = lambda t, s, i, d: f'<a href="{U}/{s}/"><i class="fas fa-{i}" aria-hidden="true"></i>{t}</a>'
    # mobile drawer (moved to <body> by redesign.js so the header's backdrop-filter can't trap it)
    acc = ''.join(f'<div class="x-dw-grp"><button class="x-dw-acc" type="button" aria-expanded="false">{g}<i class="fas fa-chevron-down" aria-hidden="true"></i></button>'
                  f'<div class="x-dw-sub"><div class="x-dw-subin">{"".join(dwl(*x) for x in xs)}</div></div></div>' for g, xs in MENU)
    drawer = (f'<div class="x-dw" id="x-dw" role="dialog" aria-modal="true" aria-label="Menu" hidden><div class="x-dw-bg" data-x-close></div><div class="x-dw-pane">'
              f'<div class="x-dw-top"><span class="x-dw-ttl">Menu</span><button class="x-dw-x" type="button" data-x-close aria-label="Close menu"><i class="fas fa-times" aria-hidden="true"></i></button></div>'
              f'<nav class="x-dw-nav" aria-label="Mobile"><a class="x-dw-main" href="{U}/">Home</a><p class="x-dw-lbl">Our Services</p>{acc}'
              f'<a class="x-dw-main" href="{U}/services/">All Services</a><a class="x-dw-main" href="{U}/about-us/">About Us</a><a class="x-dw-main" href="{U}/contact/">Contact Us</a></nav>'
              f'<div class="x-dw-cta"><a class="x-dw-call" href="{TEL}"><i class="fas fa-phone-alt" aria-hidden="true"></i> Call {PHONE}</a><a class="x-dw-quote" href="{U}/contact/"><i class="fas fa-file-signature" aria-hidden="true"></i> Get a Free Quote</a></div></div></div>')
    burger = '<button class="x-burger" type="button" aria-label="Open menu" aria-controls="x-dw" aria-expanded="false"><span></span><span></span><span></span></button>'
    return f'<nav class="x-mm" aria-label="Main"><ul class="x-mm-list">{links}</ul></nav>{burger}{drawer}'

def header():
    top = C([
        W('icon-list', 'x-live', icon_list=[{'_id': rid(), 'text': 'Live dispatch — operators standing by, 24 hours a day', 'selected_icon': ICO('circle')}], view='inline'),
        W('icon-list', 'x-topphone', icon_list=[{'_id': rid(), 'text': '(077)-710-04242', 'selected_icon': ICO('phone-alt'), 'link': {'url': TEL}}], view='inline'),
    ], 'x-topbar', flex_direction='row', flex_justify_content='space-between', flex_align_items='center', cw='boxed')
    main = C([
        W('theme-site-logo', 'x-logo', __dynamic__={'image': '[elementor-tag id="" name="site-logo" settings="%7B%7D"]'}, align='start', width={'unit': 'px', 'size': 150}),
        W('html', 'x-navwrap', html=mega_html()),
        BTN('Get a Free Quote', TEL, 'x-btn x-btn-sm x-hdr-cta'),
    ], 'x-mainbar', flex_direction='row', flex_justify_content='space-between', flex_align_items='center', flex_wrap='nowrap', cw='boxed')
    return C([top, main], 'x-header', flex_direction='column')

# ---------- FOOTER ----------
def flinks(items): return W('icon-list', 'x-flinks', icon_list=[{'_id': rid(), 'text': t, 'selected_icon': {'value': '', 'library': ''}, 'link': {'url': u}} for t, u in items])
def footer():
    fl = lambda xs: flinks([(t.replace('&amp;', '&'), f'{U}/{s}/') for t, s, i, d in xs])
    cols = C([
        C([W('theme-site-logo', 'x-logo x-flogo', __dynamic__={'image': '[elementor-tag id="" name="site-logo" settings="%7B%7D"]'}, align='start', width={'unit': 'px', 'size': 150}),
           T('<p>24/7 breakdown recovery, car recovery and towing services across Birmingham and the West Midlands.</p>', 'x-fabout'),
           W('icon-list', 'x-flinks x-fcontact', icon_list=[
            {'_id': rid(), 'text': PHONE, 'selected_icon': ICO('phone-alt'), 'link': {'url': TEL}},
            {'_id': rid(), 'text': 'general@aadtransportrecovery.co.uk', 'selected_icon': ICO('envelope'), 'link': {'url': 'mailto:general@aadtransportrecovery.co.uk'}},
            {'_id': rid(), 'text': 'Walsall Rd, Birmingham, B42 1TQ', 'selected_icon': ICO('map-marker-alt')},
            {'_id': rid(), 'text': 'Open 24 hours, 7 days a week', 'selected_icon': ICO('clock')}])], 'x-fcol x-fcol-brand', flex_direction='column'),
        *[C([H(g.replace('&amp;', '&'), 'p', 'x-fhead'), fl(xs)], 'x-fcol', flex_direction='column') for g, xs in MENU],
        C([H('Company', 'p', 'x-fhead'), flinks([('Home', U + '/'), ('All Services', U + '/services/'), ('About Us', U + '/about-us/'), ('Contact Us', U + '/contact/')]),
           BTN('Get a Free Quote', U + '/contact/', 'x-btn x-btn-sm x-fquote')], 'x-fcol', flex_direction='column'),
    ], 'x-fgrid', flex_direction='row', flex_wrap='wrap', cw='boxed')
    bottom = C([T('<p>&copy; 2026 AAD Transport &amp; Recovery. All rights reserved.</p>', 'x-fcopy'),
                T(f'<p><a href="{U}/privacy-policy/">Privacy Policy</a><a href="{U}/cookie-policy/">Cookie Policy</a></p>', 'x-flegal')],
               'x-fbottom', flex_direction='row', flex_justify_content='space-between', flex_align_items='center', flex_wrap='wrap', cw='boxed')
    return C([cols, bottom], 'x-footer', flex_direction='column')

# ---------- HOME ----------
def eyebrow(t): return T(f'<p>{t}</p>', 'x-eyebrow')
def sec(els, cls, **kw): return C(els, 'x-sec ' + cls, flex_direction='column', cw='boxed', **kw)

hero = C([
    C([
        T('<p><span class="x-dot"></span> 24/7 Emergency Recovery · Birmingham</p>', 'x-badge rv'),
        H('24/7 Breakdown Recovery Birmingham: <span class="x-hl">Fast, Reliable Car Recovery</span> You Can Trust', 'h1', 'x-hero-title rv'),
        T('<p>Broken down, involved in an accident, or need a vehicle towed across the country? AAD Transport &amp; Recovery provides breakdown recovery and car recovery across Birmingham, getting you and your vehicle moving day or night, rain or shine.</p>', 'x-hero-lead rv'),
        C([BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-pulse'), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost')], 'x-btnrow rv', flex_direction='row', flex_wrap='wrap'),
        C([W('icon-box', 'x-chip', selected_icon=ICO(i), title_text=t, description_text=d, position='left', title_size='p') for i, t, d in (('clock', 'Availability', '24/7, 365 days'), ('bolt', 'Fast Response', 'Birmingham &amp; West Midlands'), ('shield-alt', 'Fully Insured', 'Experienced operators'))], 'x-chips rv', flex_direction='row', flex_wrap='wrap'),
    ], 'x-hero-copy', flex_direction='column'),
    C([
        T('<p><strong>Get A Free <span class="x-hl">Quote</span></strong></p>', 'x-card-title'),
        T("<p>Tell us what's happened — we'll call you back within minutes.</p>", 'x-card-sub'),
        W('form', 'x-form', **form),
    ], 'x-hero-card rv rv-right', flex_direction='column', _element_id='contact-form'),
], 'x-hero', flex_direction='row', cw='boxed', background_background='classic', background_image={'url': UP + 'IMG_20250802_011544_427-scaled.webp', 'id': ''}, background_size='cover', background_position='center center')

glance = sec([C([eyebrow('AT A GLANCE'), T(te('provides 24/7 breakdown recovery in Birmingham, including'), 'x-glance-text')], 'x-glance rv', flex_direction='row')], 'x-sec-glance')

def split(img, title, body, rev=False, extra=None):
    copy_ = [H(title, 'h2', 'x-title'), T(body, 'x-body')] + ([extra] if extra else [])
    return sec([C([
        C([W('image', 'x-media', image={'url': img, 'id': {'AAD-TRANSPORT_20260429_165834_226.webp':12,'AAD-TRANSPORT_20250731_144034_770.webp':13}.get(img.rsplit('/',1)[-1], '')}, image_size='full')], 'x-media-wrap rv ' + ('rv-right' if rev else 'rv-left')),
        C(copy_, 'x-split-copy rv', flex_direction='column'),
    ], 'x-split' + (' x-split-rev' if rev else ''), flex_direction='row')], 'x-sec-split')

s1 = split(UP + 'AAD-TRANSPORT_20260429_165834_226.webp', '24/7 Breakdown Recovery <span class="x-hl">Birmingham</span>', te('A breakdown never happens'))
s2 = split(UP + 'AAD-TRANSPORT_20250731_144034_770.webp', 'Car Recovery Birmingham <span class="x-hl">You Can Rely On</span>', te('When you search for car recovery'), True, BTN('Get A Quote', '#contact-form'))

SI = json.load(open(os.path.join(os.path.dirname(__file__), 'svc_imgs.json')))
SLINK = {**{t.replace('&amp;', '&'): f'{U}/{s}/' for _, xs in MENU for t, s, _, _ in xs}, 'Birmingham Towing': U + '/towing-service-birmingham/', 'Battery Services': U + '/flat-battery-service-birmingham/', 'Tyre & Flat Tyre Services': U + '/flat-tyre-services-birmingham/'}
cards = []
for i, s in enumerate(services):
    cards.append(C([
        W('image', 'x-sc-bg', image={'url': SI[i][1], 'id': SI[i][0]}, image_size='full'),
        RAW(f'<span class="x-sc-num">{i + 1:02d}</span>'),
        C([H(s['title_text'], 'h3', 'x-sc-title'), T('<p>' + s['description_text'].strip() + '</p>', 'x-sc-text'),
           W('button', 'x-sc-go', text='', link={'url': SLINK.get(s['title_text'], '#contact-form'), 'custom_attributes': 'aria-label|' + ('Learn more about ' if s['title_text'] in SLINK else 'Get a quote for ') + s['title_text']}, selected_icon=ICO('arrow-right'))], 'x-sc-body', flex_direction='column'),
    ], f'x-sc rv rv-d{i % 4}', flex_direction='column'))
cards.append(C([
    RAW('<span class="x-sc-num x-sc-num-q"><i class="fas fa-question"></i></span>'),
    C([H('Not Sure What You Need?', 'h3', 'x-sc-title'),
       T("<p>Tell us what's happened and we'll advise the safest, most suitable recovery option — day or night.</p>", 'x-sc-text'),
       BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-white x-btn-sm')], 'x-sc-body', flex_direction='column'),
], 'x-sc x-sc-cta rv', flex_direction='column'))
svc = sec([eyebrow('WHAT WE DO'), H('Our Breakdown Recovery &amp; <span class="x-hl">Roadside Services</span>', 'h2', 'x-title rv'), T(te("Whatever's happened to your vehicle, we provide"), 'x-lead rv'),
           C(cards, 'x-grid x-grid-sc', flex_direction='row', flex_wrap='wrap')], 'x-sec-svc')

reasons = sec([C([
    C([eyebrow('COMMON CALL-OUTS'), H('Common Reasons Drivers <span class="x-hl">Call Us For Recovery</span>', 'h2', 'x-title'), T(te('No two breakdowns are the same'), 'x-body'),
       T(te("If you're not sure exactly"), 'x-note')], 'x-reasons-intro rv', flex_direction='column'),
    C([T(lists[0], 'x-checks'), T(lists[1], 'x-checks')], 'x-reasons-lists rv rv-right', flex_direction='row'),
], 'x-reasons', flex_direction='row')], 'x-sec-reasons')

wicons = ['clock', 'tachometer-alt', 'shield-alt', 'pound-sign', 'truck-pickup', 'map-marked-alt', 'globe-europe', 'comments']
whyc = [W('icon-box', f'x-wcard rv rv-d{i % 4}', selected_icon=ICO(wicons[i]), title_text=s['title_text'], description_text=s['description_text'], title_size='h3') for i, s in enumerate(why)]
whys = C([C([eyebrow('WHY US'), H('Why Choose <span class="x-hl">AAD Transport &amp; Recovery?</span>', 'h2', 'x-title rv'),
             T('<p>Choosing the right recovery company matters when your vehicle is off the road and you need someone you can trust to sort it out properly.</p>', 'x-lead rv'),
             C(whyc, 'x-grid x-grid-4', flex_direction='row', flex_wrap='wrap')], 'x-sec', flex_direction='column', cw='boxed')], 'x-dark', flex_direction='column')

areas = ['Erdington', 'Perry Barr', 'Aston', 'Sutton Coldfield', 'Solihull', 'West Bromwich', 'Walsall', 'Walsall', 'Dudley']
area = sec([C([
    C([eyebrow('COVERAGE'), H('Breakdown Recovery Across <span class="x-hl">Birmingham &amp; Beyond</span>', 'h2', 'x-title'),
       T('<p>We provide breakdown recovery, car recovery and towing services throughout Birmingham, plus nationwide long-distance recovery when your vehicle needs to travel further.</p>', 'x-body'),
       C([H(a, 'p', 'x-area') for a in areas], 'x-areas', flex_direction='row', flex_wrap='wrap')], 'x-area-copy rv', flex_direction='column'),
    C([W('google_maps', 'x-map', **gmap)], 'x-map-wrap rv rv-right'),
], 'x-split', flex_direction='row')], 'x-sec-area')

steps = [('01', 'Call us', 'on 07771 004242 with your location and a brief description of the problem.immediately'),
         ('02', 'We assess the job', "and tell you which vehicle we're sending and an estimated arrival time."),
         ('03', 'We arrive and recover your vehicle', "safely, whether that's a quick wheel-lift tow or full flatbed transport."),
         ('04', 'We take you and your vehicle', 'to your chosen destination — garage, home, or elsewhere.')]
how = sec([eyebrow('HOW IT WORKS'), H('If You Break Down <span class="x-hl">Somewhere Busy:</span>', 'h2', 'x-title rv'),
           C([C([H(n, 'p', 'x-step-n'), H(t, 'h3', 'x-step-t'), T(f'<p>{d}</p>', 'x-step-d')], f'x-step rv rv-d{i}', flex_direction='column') for i, (n, t, d) in enumerate(steps)], 'x-steps', flex_direction='row')], 'x-sec-how')

reviews = sec([eyebrow('REVIEWS'), H('What Our <span class="x-hl">Customers Say</span>', 'h2', 'x-title rv'),
               T('<p>Real Google reviews from drivers we have helped across Birmingham and the West Midlands.</p>', 'x-lead rv'),
               C([W('shortcode', 'x-reviews-sc', shortcode='[trustindex no-registration=google]')], 'x-reviews rv')], 'x-sec-reviews')

faqs = sec([C([
    C([eyebrow('FAQs'), H('Frequently Asked <span class="x-hl">Questions</span>', 'h2', 'x-title'), T('<p>Still have a question? Call us any time — day or night.</p>', 'x-body'), BTN('Call Now: ' + PHONE, TEL)], 'x-faq-intro rv', flex_direction='column'),
    C([W('accordion', 'x-faq', **faq)], 'x-faq-wrap rv rv-right'),
], 'x-split x-split-faq', flex_direction='row')], 'x-sec-faq')

cta = sec([C([
    C([H("Stuck On The Road? <span class=\"x-hl\">We're Ready When You Are.</span>", 'h2', 'x-cta-title'),
       T("<p>Don't wait it out — call AAD Transport &amp; Recovery now for fast, reliable breakdown recovery anywhere in Birmingham, 24 hours a day.</p>", 'x-cta-text')], 'x-cta-copy', flex_direction='column'),
    C([BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-white'), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost')], 'x-btnrow', flex_direction='row', flex_wrap='wrap'),
], 'x-cta rv', flex_direction='row')], 'x-sec-cta')

sticky = RAW(f'<a class="x-float-call" href="{TEL}" aria-label="Call {PHONE}"><i class="fas fa-phone-alt"></i><span>Call 24/7</span></a>')
body = [hero, glance, s1, s2, svc, reasons, whys, area, how, reviews, faqs, cta]
header_el, footer_el = header(), footer()
wrap = lambda els: [C([ASSETS] + els, 'x-root', flex_direction='column')]
json.dump({'home': wrap([header_el] + body + [footer_el, sticky]), 'header': wrap([header_el]), 'footer': [C([RAW(ASSETS['settings']['html'].split('</script>',1)[1])] + [footer_el, sticky], 'x-root', flex_direction='column')],
           'home_body': wrap(body)}, open(os.path.join(os.path.dirname(__file__), 'built.json'), 'w'))
print('ok')
