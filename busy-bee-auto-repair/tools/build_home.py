"""Busy Bee home page (post id in ids.json → 'home'), built from the ChatGPT-site design.
Run: python3 build_home.py            (writes the page + regenerates its CSS)
Every section is native Elementor containers/widgets; behaviour lives in bb.js / bb.css (Custom Code)."""
import json
import el
from common import *
from el import uid

# ---------------------------------------------------------------- data
DIAG = [  # hero diagnostic cards
    ('engine', 'cog', 'Engine', 'Timing, spark plugs, leak detection'),
    ('battery', 'battery-charging', 'Battery', 'Free testing, alternator and charging'),
    ('brakes', 'disc-3', 'Brakes', 'Pads, rotors, full inspections'),
    ('suspension', 'waves', 'Suspension', 'Shocks, struts, steering'),
    ('cooling', 'snowflake', 'Cooling', 'Radiator, water pump, thermostat'),
    ('tires', 'circle-dashed', 'Tires', 'New and used, balancing, rotations'),
]
ZONES = [(33.0, 56.5), (39.0, 55.0), (40.5, 73.5), (45.5, 50.5), (68.5, 65.0), (72.0, 73.5)]
SLIDES = [  # desktop hero slides 2..5 (slide 1 is the SUV base layer)
    ('pickup-truck-repair-calgary', 'Pickup', [('cog', 45, 40), ('disc-3', 66.8, 63), ('waves', 81.8, 64), ('circle-dashed', 94, 60)]),
    ('mercedes-repair-calgary', 'Mercedes', [('cog', 77.7, 44), ('snowflake', 93, 49), ('battery-charging', 68.1, 46)]),
    ('bmw-repair-calgary', 'BMW', [('battery-charging', 53.2, 40), ('disc-3', 39.5, 66), ('circle-dashed', 84.5, 66)]),
    ('busy-bee-repair-bay-calgary', 'At work', []),
]
VEHICLES = ['SUV', 'Pickup', 'Mercedes', 'BMW', 'At work']


def abs_fill(name, children=(), **kw):
    return C(name, children, pos={'x': 0, 'y': 0}, w=pct(100), minh=cu('100%'), **kw)


# ================================================================ HERO (≥768px)
def hero_badge(mobile=False):
    disc = C('Scan disc', [IMG('computer-diagnostics-indicator', w=18, name='Diagnostic indicator', alt='')],
             ai='center', jc='center', w=32, minh=32, bg=SOFT, radius=PILL, cls='bb-scan-glow')
    txt = H('Computer diagnostics <span aria-hidden="true">•</span> All makes and models', 'div', INK,
            M(11, 800, 11, 0.44, 'uppercase', size_m=9, lh_m=9, ls_m=0.36), name='Badge text', cls='bb-nowrap' if not mobile else 'bb-wrap')
    return C('Badge', [disc, txt], d='row', ai='center', gap=10, w='auto', pad=(6, 16, 6, 6), bg=PAPER, radius=PILL,
             border=(1, ink(0.1)), shadow=shadow(0, 8, 22, -12, ink(0.55)), cls='bb-badge')


def h1(tag='h1'):
    return H('Auto repair in<br>Calgary you can<br>actually <span class="bb-type" data-word="trust">trust</span>', tag, PAPER,
             M(60, 800, 1.02, tt='uppercase', size_t=48, size_m=36), name='Hero title', mar=(24, 0, 0, 0), mar_mobile=(20, 0, 0, 0),
             w=650, w_tablet='full', cls='bb-h1')


HERO_P = ('Busy Bee Auto Repair &amp; Tire Shop is a family-owned auto repair shop in NE Calgary. Our certified mechanics fix all '
          'makes and models, from a quick oil change to a check engine light nobody else could solve. You get a clear diagnosis, '
          'an honest quote, and the work done right the first time.')


def whatsapp_btn():
    return BTN('WhatsApp us', WHATSAPP, S(13, 750, 16.9), color=PAPER, bg='#128C50', ic='whatsapp', ic_pos='before', ic_gap=9,
               ic_size=22, pad=(12, 19), radius=30, border=(1, '#128C50'), hover_bg='#096D3C', hover_color=PAPER, name='WhatsApp us',
               cls='bb-wa')


def google_card():
    top = C('Top', [H('Google reviews', 'div', ink(0.55), M(10, 800, 15, tt='uppercase'), name='Label'),
                    IMG('google-g-mark-hero', w=28, alt='Google', name='Google mark')], d='row', jc='space-between', ai='center', gap=8)
    stars = T('<span class="bb-gstars"><span>★</span><span>★</span><span>★</span><span>★</span><span>★</span></span>', None,
              S(18, 400, 28), name='Stars')
    score = C('Score', [H('4.8', 'div', INK, M(48, 800, 48), name='Rating'),
                        C('Stars col', [stars, T('<p>Google customer rating</p>', ink(0.7), M(11, 400, 16.5), name='Caption')],
                          w='auto')], d='row', ai='center', gap=12, mar=(12, 0, 0, 0))
    bar = C('Rating bar', [C('Fill', [], w=pct(96), minh=6, radius=PILL, cls='bb-gbar')], minh=6, bg=GREY, radius=PILL, mar=(12, 0))
    return C('Google card', [top, score, bar, T('<p>Honest pricing, quality workmanship and transparent communication.</p>', ink(0.65),
                                                M(12, 400, 19.5), name='Note')],
             pad=20, bg=PAPER, radius=18, border=(1, ink(0.05)), shadow=SH_LG)


def mini_card(name, ic, title, body, yellow):
    ibox = ICON(ic, 16, color=BEE if yellow else INK, bg=INK if yellow else SOFT, box=36, radius=10,
                border=None if yellow else (1, ink(0.1)), name='Icon', w='auto')
    return C(name, [ibox, H(title, 'h2', INK, M(14, 800, 17.5, tt='uppercase'), mar=(12, 0, 0, 0), name='Title'),
                    T(f'<p>{body}</p>', INK if yellow else ink(0.7), M(12, 400, 16.5), mar=(8, 0, 0, 0), name='Text')],
             pad=16, bg=BEE if yellow else PAPER, radius=18, border=None if yellow else (1, ink(0.05)), shadow=SH_LG,
             w=cu('calc(50% - 6px)'))


def aside():
    return C('Reviews aside', [
        google_card(),
        C('Cards', [mini_card('Walk-ins', 'calendar-days', 'Walk-ins welcome', 'Monday to Friday<br>9 AM to 6 PM', True),
                    mini_card('Certified', 'shield-check', 'Certified techs', 'Parts &amp; labour warranty on most repairs', False)],
          d='row', gap=12, ai='stretch'),
    ], gap=12, cls='bb-aside')


def diag_card(slug, ic, title, detail):
    head = C('Head', [ICON(ic, 20, color=INK, bg=BEE, box=28, name='Icon', w='auto'),
                      H(title, 'h3', INK, M(12, 800, 16, tt='uppercase'), name='Title')], d='row', ai='center', gap=8)
    link_row = C('See service', [H('See service', 'span', INK, M(9, 800, 13.5, tt='uppercase'), name='Label'),
                                 ICON('arrow-up-right', 12, color=PAPER, bg=INK, box=24, name='Arrow', w='auto')],
                 d='row', jc='space-between', ai='center', pad=(8, 0, 0, 0), mar=(0, 0, 0, 0), href=SVC[slug],
                 border=(dims(1, 0, 0, 0), ink(0.1)), cls='bb-dlink')
    return C('Card – ' + title, [head, T(f'<p>{detail}</p>', ink(0.65), M(11, 400, 15.125), mar=(8, 0, 12, 0), name='Detail', grow=True),
                                 link_row],
             pad=12, bg=PAPER, radius=14, border=(1, ink(0.05)), minh=144, tag='article', cls='bb-dcard')


def diag_block(mobile=False):
    label = C('Scan label', [
        C('Dot', [], w=6, minh=6, bg=BEE, radius=PILL),
        H('Multi-point diagnostic scan · <span class="bb-vname">SUV</span>', 'p', PAPER, M(9, 800, 13.5, tt='uppercase'), name='Label',
          w='auto'),
        C('Line', [], minh=1, bg=wht(0.25), grow=True, w=cu('auto')),
    ], d='row', ai='center', gap=12, mar=(0, 0, 12, 0))
    grid = C('Diagnostic cards', [diag_card(*d) for d in DIAG], grid='repeat(6, minmax(0, 1fr))', grid_tablet='repeat(3, minmax(0, 1fr))',
             grid_mobile='repeat(2, minmax(0, 1fr))', gap=8, rows='auto', rows_tablet='auto', rows_mobile='auto')
    return C('Diagnostics', [label, grid])


def vehicle_buttons(names, mobile=False, labels=None):
    btns = []
    for i, n in enumerate(names):
        b = BTN(n, '#', M(9, 800, 13.5, tt='uppercase'), color=INK, bg=PAPER, pad=(8.25, 12 if mobile else 16), radius=PILL,
                border=(1, '#E2E8F0'), sh=SH_SM, name='Vehicle – ' + n, cls='bb-vbtn' + (' is-active' if i == 0 else ''),
                attrs={'data-slide': i, 'data-label': (labels or names)[i]})
        b['settings']['button_text_color'] = INK
        btns.append(b)
    return C('Vehicle buttons', btns, d='row', jc='flex-end', gap=8, wrap='wrap', mar=(0, 0, 20, 0) if not mobile else (20, 0),
             cls='bb-vbtns')


def zone(x, y):
    return C('Zone', [C('Dot', [], w=8, minh=8, bg=INK, radius=PILL)], ai='center', jc='center', w=64, minh=64, radius=PILL,
             border=(2, BEE), pos={'x': pct(x), 'y': pct(y)}, cls='bb-zone')


def point(ic, x, y, size=48, icon_size=20):
    return ICON(ic, icon_size, color=INK, bg=BEE, box=size, pos={'x': pct(x), 'y': pct(y)}, name='Point', cls='bb-pt', w='auto')


def hero_desktop():
    base = abs_fill('Slide 1 – SUV', [zone(*z) for z in ZONES] + [
        C('Ground line', [], pos={'x': 0, 'y': pct(8), 'v': 'end'}, w=pct(100), minh=1,
          border=(dims(0, 0, 1, 0), wht(0.25), 'dashed'), cls='bb-fade'),
        H('Multi-point diagnostic scan', 'div', ink(0.7), M(10, 600, 15, tt='uppercase'), name='Scan tag', pad=(4, 8),
          pos={'x': 16, 'y': 16, 'v': 'end'}, z=20, w='auto', cls='bb-fade bb-scanlabel',
          _background_background='classic', _background_color=wht(0.9), _border_border='solid', _border_width=dims(1),
          _border_color=ink(0.4)),
    ], bgimg='busy-bee-auto-repair-calgary-workshop-hero', cls='bb-slide bb-slide-1 is-active', attrs={'data-slide': 0})
    slides = [base]
    for i, (key, name, pts) in enumerate(SLIDES, start=1):
        slides.append(abs_fill(f'Slide {i + 1} – {name}', [point(*p) for p in pts], bgimg=key, z=10,
                               cls=f'bb-slide bb-slide-n bb-slide-{i + 1}', attrs={'data-slide': i}))

    left = C('Hero copy', [
        hero_badge(),
        h1(),
        T(f'<p>{HERO_P}</p>', wht(0.9), M(16, 400, 26), mar=(16, 0, 0, 0), w=510, w_tablet='full', name='Intro'),
        C('Actions', [
            BTN('Book an Appointment', BOOK, M(14, 700, 20), color=PAPER, bg=INK, ic='calendar-days', ic_pos='before', ic_gap=12,
                ic_size=16, radius=PILL, border=(1, INK), name='Book an Appointment', cls='bb-btn-disc bb-disc-bee bb-ring'),
            BTN('Call ' + PHONE, TEL, M(14, 700, 20), color=INK, bg=PAPER, ic='phone', ic_pos='before', ic_gap=12, ic_size=16,
                radius=PILL, border=(1, ink(0.1)), sh=SH_SM, name='Call', cls='bb-btn-disc bb-disc-ink'),
            whatsapp_btn(),
        ], d='row', wrap='wrap', gap=12, mar=(24, 0, 0, 0)),
        C('Family', [IMG('busy-bee-customer-avatars', w=75, h=36, fit='contain', alt='', name='Avatars'),
                     T('<p><strong>Family-owned in NE Calgary.</strong><br>Walk-ins welcome, every make and model.</p>', PAPER,
                       M(12, 400, 16.5), name='Text')], d='row', ai='center', gap=12, mar=(20, 0, 0, 0)),
    ], cls='bb-hero-copy')

    content = C('Hero content', [
        C('Hero grid', [left, aside()], grid='minmax(0,1fr) 260px', gap=(80, 80), gap_tablet=(40, 40), ai='start', rows='auto',
          pad=(40, 0), minh=490, minh_tablet=470),
        vehicle_buttons(VEHICLES),
        diag_block(),
    ], w=cu('min(1152px, 100%)'), mar=(0, 'auto'), pad=(0, 24, 24, 24), z=20)

    return C('Hero', slides + [content], tag='section', cls='bb-hero', ov=True, pad=(126, 0, 0, 0), bg=PAPER, hide='m',
             id_='top')


# ================================================================ HERO (mobile, <768px)
MSLIDES = [  # key, button label, scan label, points (icon, left %, top %, service)
    ('busy-bee-auto-repair-calgary-workshop-hero-mobile', 'SUV', 'SUV',
     [('snowflake', 15.7, 56.3, 'cooling'), ('cog', 24.9, 53.2, 'engine'), ('battery-charging', 33.1, 57.5, 'battery'),
      ('disc-3', 37.2, 62.6, 'brakes'), ('waves', 67.5, 58, 'suspension'), ('circle-dashed', 83, 60.8, 'tires')]),
    ('pickup-truck-repair-calgary', 'Pickup', 'Pickup truck',
     [('cog', 28, 52, 'engine'), ('disc-3', 49, 60, 'brakes'), ('waves', 68, 57, 'suspension'), ('circle-dashed', 71, 59, 'tires')]),
    ('mercedes-repair-calgary', 'Mercedes', 'Mercedes sports car',
     [('cog', 75, 53, 'engine'), ('snowflake', 85, 55, 'cooling'), ('battery-charging', 40, 51, 'battery')]),
    ('bmw-repair-calgary', 'BMW', 'BMW sedan',
     [('battery-charging', 52, 52, 'battery'), ('disc-3', 36, 59, 'brakes'), ('circle-dashed', 67, 59, 'tires')]),
]


def hero_mobile():
    vh = dict(pos={'x': 0, 'y': 0}, w=pct(100), minh=cu('100svh'))
    slides = []
    for i, (key, _, _, _) in enumerate(MSLIDES):
        if i == 0:
            kids = [IMG(key, w=pct(100), h=cu('100%'), fit='cover', alt='Silver SUV inside a clean mechanic shop', name='Photo',
                        cls='bb-mslide-photo')]
        else:
            kids = [IMG(key, w=pct(100), h=cu('100%'), fit='cover', alt='', name='Blurred backdrop', cls='bb-mslide-photo bb-mslide-blur'),
                    IMG(key, w=cu('min(125%, 600px)'), alt='', name='Vehicle', cls='bb-mslide-focus')]
        slides.append(C(f'Mobile slide {i + 1}', kids, ov=True, cls='bb-slide' + (' is-active bb-slide-1' if i == 0 else ' bb-slide-n'),
                        attrs={'data-slide': i}, **vh))
    overlays = [C('Overlay – base', [], cls='bb-mov bb-mov-1', **vh), C('Overlay – vehicles', [], cls='bb-mov bb-mov-2', **vh)]
    pts = []
    for i, (_, _, _, points) in enumerate(MSLIDES):
        pts.append(C(f'Points – slide {i + 1}', [
            ICON(ic, 16, color=INK, bg=BEE, box=36, href=SVC[svc], pos={'x': pct(x), 'y': pct(y)}, name='Point – ' + svc,
                 cls='bb-pt bb-mpt' + ('' if i else ' bb-pt-scan'), w='auto')
            for ic, x, y, svc in points], cls='bb-pts' + (' is-active' if i == 0 else ''), attrs={'data-slide': i}, **vh))
    copy = C('Mobile hero copy', [
        hero_badge(mobile=True),
        h1('div'),
        T(f'<p>{HERO_P}</p>', PAPER, M(14, 400, 22.75), mar=(16, 0, 0, 0), w=384, name='Intro'),
        C('Actions', [
            BTN('Book an Appointment', BOOK, S(14, 700, 20), color=PAPER, bg=INK, ic='calendar-days', ic_pos='before', ic_size=16,
                pad=(13, 16), radius=PILL, border=(1, INK), sh=SH_INK, name='Book an Appointment'),
            BTN('Call ' + PHONE, TEL, S(14, 500, 20), color=INK, bg=PAPER, ic='phone', ic_pos='before', ic_size=16, pad=(13, 16),
                radius=PILL, border=(1, ink(0.1)), sh=SH_SM, name='Call'),
            whatsapp_btn(),
        ], d='column', ai='flex-start', gap=8, mar=(20, 0, 0, 0)),
        SPACER(160),
        C('Family', [IMG('busy-bee-customer-avatars', w=75, h=36, fit='contain', alt='', name='Avatars'),
                     T('<p><strong>Family-owned in NE Calgary.</strong><br>Walk-ins welcome, every make and model.</p>', INK,
                       M(12, 400, 16.5), name='Text')], d='row', ai='center', gap=12, pad=(8, 12), bg=wht(0.9), radius=PILL,
          mar=(0, 0, 20, 0)),
        aside(),
        vehicle_buttons([m[1] for m in MSLIDES], mobile=True, labels=[m[2] for m in MSLIDES]),
        diag_block(mobile=True),
    ], pad=(96, 20, 24, 20), z=20)
    return C('Hero (mobile)', slides + overlays + [copy, C('Points', pts, cls='bb-pts-layer', z=10, **vh)], tag='section',
             cls='bb-mhero', bg=PITCH, ov=True, hide='dt')


# ================================================================ SUPPLIERS MARQUEE
SUPPLIERS = [('napa-auto-parts', 'NAPA Auto Parts', 40, 28), ('lordco-auto-parts', 'Lordco Auto Parts', 52, 36),
             ('partsource', 'PartSource', 40, 28), ('auto-value-auto-parts', 'Auto Value Auto Parts', 40, 28)]


def suppliers():
    def group(dup):
        return C('Logos' + (' (loop copy)' if dup else ''), [
            IMG(k, h=h, alt='' if dup else alt, name=alt, cls='bb-logoimg', height_mobile=px(hm), w=None,
                width=cu('auto')) for k, alt, h, hm in SUPPLIERS],
            d='row', ai='center', gap=80, gap_mobile=48, w='auto', attrs={'aria-hidden': 'true'} if dup else None)
    track = C('Track', [group(False), group(True)], d='row', ai='center', gap=80, gap_mobile=48, pad=(0, 80, 0, 0),
              pad_mobile=(0, 48, 0, 0), w=cu('max-content'), cls='bb-marquee-track')
    return C('Suppliers', [
        H('Quality parts from proven suppliers', 'p', ink(0.45), M(11, 700, 16.5, 3.52, 'uppercase'), align='center',
          mar=(0, 0, 24, 0), name='Title'),
        C('Marquee', [track], ov=True, cls='bb-marquee'),
    ], tag='section', pad=(40, 0), pad_mobile=(32, 0), bg=PAPER, border=(dims(1, 0, 1, 0), ink(0.1)), cls='bb-suppliers')


# ================================================================ SERVICES
SERVICES = [  # slug, category, eyebrow, title, description, price, badge, icon, photo
    ('oil-change', 'Maintenance', 'Routine care', 'Mobil 1 synthetic oil change', 'Mobil 1 synthetic oil changes from $75, with a free inspection.', 'From $75', 'Same day', 'droplets', 'mobil-1-synthetic-oil-change-calgary'),
    ('brakes', 'Repair', 'Safety system', 'Brake repair &amp; replacement', 'Pads, rotors, calipers, and brake fluid service.', 'Quote after inspection', None, 'disc-3', 'brake-repair-calgary'),
    ('diagnostics', 'Repair', 'Fault finding', 'Computer diagnostics &amp; electrical', 'Warning lights, wiring, starters, and sensors.', 'Quote after scan', None, 'circle-gauge', 'computer-diagnostics-calgary'),
    ('battery', 'Maintenance', 'Starting &amp; charging', 'Battery &amp; alternator service', 'Free battery testing and charging system checks.', 'Free battery test', 'Free', 'battery-charging', 'battery-alternator-service-calgary'),
    ('engine', 'Repair', 'Powertrain', 'Engine maintenance &amp; repair', 'Check engine lights, misfires, leaks, timing belts, and more.', 'Quote after inspection', None, 'settings-2', 'engine-repair-audi-calgary'),
    ('cooling', 'Maintenance', 'Temperature control', 'Cooling system &amp; radiator', 'Radiators, water pumps, thermostats, and coolant flushes.', 'Quote after inspection', None, 'snowflake', 'computer-diagnostics-calgary'),
    ('suspension', 'Repair', 'Ride &amp; handling', 'Suspension &amp; steering repair', 'Shocks, struts, ball joints, tie rods, and bearings.', 'Quote after inspection', None, 'waves', 'brake-repair-calgary'),
    ('transmission', 'Repair', 'Driveline', 'Transmission repair', 'Fluid service, diagnosis, and repair.', 'Quote after inspection', None, 'unplug', 'busy-bee-repair-bay-calgary'),
]


def eyebrow_dot(text, color=ink(0.5), dot=BEE):
    return C('Eyebrow', [C('Dot', [], w=8, minh=8, bg=dot, radius=PILL),
                         H(text, 'p', color, M(11, 800, 16.5, 2.64, 'uppercase'), name='Eyebrow')],
             d='row', ai='center', gap=8)


def filter_btn(label, active):
    return BTN(label, '#services', M(14, 700, 20), color=PAPER if active else INK, bg=INK if active else PAPER, pad=(11, 20),
               radius=PILL, border=(1, INK if active else ink(0.15)), sh=SH_SM, name='Filter – ' + label,
               cls='bb-filter' + (' is-active' if active else ''), attrs={'data-filter': label})


def feature_card():
    checks = ['Tire repair up to 16 in · $84', 'Seasonal tire swaps', 'Wheel alignment', 'Balancing &amp; rotation',
              'New &amp; used tires', 'Winter &amp; all-season tires']
    top = C('Top', [
        C('Label', [ICON('gauge', 28, color=INK, bg=BEE, box=56, radius=18, name='Icon', w='auto'),
                    H('Most booked', 'span', BEE, M(12, 800, 16, 0.6, 'uppercase'), name='Most booked')], d='row', ai='center', gap=12,
          w='auto'),
        H('Winter tire season is here', 'span', BEE, M(12, 700, 16), name='Pill', pad=(8, 12), w='auto',
          _background_background='classic', _background_color='rgba(247,215,16,0.15)', _border_radius=dims(PILL)),
    ], d='row', wrap='wrap', jc='space-between', ai='center', gap=16)
    lst = C('Checks', [ILIST([('check', c, None)], t=M(14, 400, 24), color=PAPER, ic_color=BEE, ic_size=20, gap_=8,
                             name='Check', cls='bb-check') for c in checks],
            grid='repeat(2, minmax(0, 1fr))', grid_mobile='1fr', gap=(20, 16), rows='auto', rows_mobile='auto', mar=(32, 0))
    btns = C('Buttons', [
        BTN('Book a tire swap', BOOK, M(14, 700, 20), color=INK, bg=BEE, ic='arrow-right', ic_size=16, pad=(12, 20), radius=PILL,
            border=(1, ink(0.2)), sh=SH_BEE, name='Book a tire swap', w_mobile=pct(100), align_mobile='justify'),
        BTN('Tire services', SVC['tires'], M(14, 700, 20), color=PAPER, bg='rgba(0,0,0,0)', pad=(11, 20), radius=PILL,
            border=(1, wht(0.25)), sh=SH_SM, name='Tire services', w_mobile=pct(100), align_mobile='justify'),
    ], d='row', d_mobile='column', wrap='wrap', gap=12, pad=(8, 0, 0, 0), mar=(0, 0, 0, 0), cls='bb-push-bottom')
    return C('Feature – Tires', [
        ICON('circle-dot', 320, color=BEE, name='Decorative ring', hide='d', pos={'x': -64, 'y': -64, 'h': 'end', 'v': 'end'},
             cls='bb-feature-ring', w='auto', z=0),
        top,
        H('Tires, wheels &amp; alignment', 'h3', PAPER, M(36, 800, 45, tt='uppercase', size_m=30, lh_m=37.5), mar=(32, 0, 0, 0),
          name='Title'),
        T('<p>New and used tires, installation, repair, rotation, and balancing. Wheel alignment for straighter tracking and longer tire life.</p>',
          '#E3E7E8', M(16, 400, 28, size_m=14), mar=(16, 0, 0, 0), name='Text'),
        lst, btns,
    ], tag='article', pad=40, pad_mobile=32, bg='#192024', radius=28, ov=True, bgimg='winter-tire-change-calgary', bgpos='58% center',
        cls='bb-svc-feature', grid_column='2', grid_column_tablet='1', grid_row='2', grid_row_tablet='1', attrs={'data-cat': 'Tires'})


def service_card(slug, cat, eyebrow, title, desc, price, badge, ic, photo):
    top = [ICON(ic, 24, color=INK, bg='#F3D832', box=52, radius=18, name='Icon', w='auto', cls='bb-svc-icon', size_mobile=px(24))]
    if badge:
        top.append(H(badge, 'span', BEE, M(12, 700, 16), name='Badge', pad=(4, 12), w='auto', hide='m',
                     _background_background='classic', _background_color=INK, _border_radius=dims(PILL)))
    return C('Service – ' + slug, [
        IMG(photo, w=pct(100), h=190, fit='cover', posn='center 38%', alt='', name='Photo', hide='tm',
            pos={'x': 0, 'y': 0}, cls='bb-svc-photo', z=0),
        C('Top', top, d='row', jc='space-between', ai='center', gap=8, pos={'x': 18, 'y': 15}, w=cu('calc(100% - 36px)'), z=1,
          cls='bb-svc-top'),
        C('Body', [
            H(eyebrow, 'p', '#F6DA4F', M(10, 800, 20, 0.5, 'uppercase'), mar=(20, 0, 0, 0), name='Eyebrow', hide='m', cls='bb-svc-eyebrow'),
            H(title, 'h3', PAPER, M(20, 800, 27.5, tt='uppercase', size_m=16, lh_m=22), mar=(8, 0, 0, 0), mar_mobile=(0, 0, 0, 0),
              name='Title', cls='bb-svc-title'),
            T(f'<p>{desc}</p>', '#E0E5E6', M(14, 400, 24), mar=(12, 0, 0, 0), mar_mobile=(4, 0, 0, 0), name='Text', cls='bb-svc-text'),
            H(price, 'p', INK, M(14, 800, 20), mar=(4, 0, 0, 0), name='Price (mobile)', hide='dt'),
        ], z=1, grow=True, cls='bb-svc-body', w_mobile=cu('auto')),
        C('Footer', [H(price, 'span', PAPER, M(14, 800, 20), name='Price', cls='bb-svc-price'),
                     ICON('arrow-right', 20, color=BEE, bg=INK, box=44, name='Arrow', w='auto')],
          d='row', jc='space-between', ai='center', gap=8, pad=(16, 0, 0, 0), mar=(24, 0, 0, 0), hide='m', z=1,
          border=(dims(1, 0, 0, 0), 'rgba(255,255,255,0.19)'), cls='bb-svc-foot'),
        ICON('chevron-right', 20, color=INK, name='Chevron', hide='dt', w='auto'),
    ], href=SVC[slug], pad=(155, 28, 28, 28), pad_tablet=28, pad_mobile=16, d_mobile='row', ai_mobile='center', gap_mobile=16,
        bg='#192024', radius=22, radius_mobile=18, border=(1, 'rgba(255,255,255,0.082)'), shadow=shadow(0, 8, 25, 0, 'rgba(21,33,38,0.07)'),
        minh=420, minh_tablet=0, ov=True, cls='bb-svc-card', attrs={'data-cat': cat})


def services():
    head = C('Head', [
        C('Intro', [eyebrow_dot('Services · NE Calgary'),
                    H('Car Repair Services in Calgary', 'h2', INK, M(48, 800, 1.05, tt='uppercase', size_m=28), mar=(12, 0, 0, 0),
                      name='Title'),
                    T('<p>Whatever your vehicle needs, our Calgary auto shop handles it under one roof.</p>', ink(0.6),
                      M(16, 400, 28, size_m=14), mar=(16, 0, 0, 0), w=576, w_mobile='full', name='Intro')],
          w=672, w_tablet=pct(100)),
        H('View all services ↗︎', 'span', INK, M(14, 700, 20, deco='underline'), href='#services', name='View all services',
          w=96, w_tablet='auto', cls='bb-underline'),
        C('Filters', [filter_btn(x, x == 'All') for x in ('All', 'Maintenance', 'Repair', 'Tires')], d='row', gap=8, w='auto',
          cls='bb-filters'),
    ], d='row', d_tablet='column', jc='space-between', ai='flex-end', ai_tablet='flex-start', gap=28, cls='bb-svc-head')
    grid = C('Service grid', [feature_card()] + [service_card(*sv) for sv in SERVICES],
             grid='repeat(4, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))', grid_mobile='1fr', gap=20, rows='auto',
             rows_tablet='auto', rows_mobile='auto', flow='row dense', mar=(32, 0, 0, 0), cls='bb-svc-grid')
    trust = C('Promise bar', [
        C('Items', [ILIST([(i, t, None)], t=M(14, 600, 24), color=INK, ic_color=INK, ic_size=24, gap_=12, name=t, w='auto')
                    for i, t in (('clipboard-check', 'Estimate approved before any work'),
                                 ('shield-check', 'Parts &amp; labour warranty on most repairs'),
                                 ('timer-reset', 'Oil, tires &amp; batteries often done same day'))],
          d='row', d_mobile='column', gap=24, gap_mobile=20, w='auto', w_tablet=pct(100)),
        BTN('Book a service', BOOK, M(14, 700, 20), color=INK, bg=BEE, ic='calendar-check', ic_pos='before', ic_size=20, pad=(12, 20),
            radius=PILL, border=(1, ink(0.2)), sh=SH_BEE, name='Book a service', w_tablet=pct(100), align_tablet='justify',
            cls='bb-nowrap'),
    ], d='row', d_tablet='column', jc='space-between', ai='center', ai_tablet='stretch', gap=24, pad=(24, 32), mar=(32, 0, 0, 0),
        bg=PAPER, radius=22, border=(1, ink(0.1)))
    return C('Services', [C('Inner', [head, grid, trust], w=cu('min(1152px, 100%)'), mar=(0, 'auto'))],
             tag='section', id_='services', pad=(112, 32), pad_mobile=(40, 20), bg='#FCFCFD', cls='bb-services')


# ================================================================ RIBBON + WINTER OFFERS
def ribbon():
    def group(dup):
        return C('Group', [
            IMG('busy-bee-auto-repair-logo', w=116, h=42, fit='contain', alt='' if dup else 'Busy Bee Auto Repair', name='Logo',
                cls='bb-ribbon-logo'),
            H('Calgary, get winter-ready.', 'span', PAPER, S(15, 650, 22.5), name='Text', cls='bb-nowrap'),
            C('Dot', [], w=5, minh=5, bg=YEL, radius=PILL),
            H('Seasonal tire changes · Balancing · Tire checks', 'span', PAPER, S(15, 650, 22.5), name='Text', cls='bb-nowrap'),
            BTN('Call ' + PHONE + ' ↗︎', TEL, S(14, 750, 21), color='#1B2225', bg=YEL, pad=(12, 22), radius=30, border=(1, YEL),
                name='Call', cls='bb-nowrap'),
        ], d='row', ai='center', gap=40, pad=(0, 64, 0, 0), w=cu('max-content'), attrs={'aria-hidden': 'true'} if dup else None)
    return C('Winter ribbon', [C('Track', [group(False), group(True)], d='row', w=cu('max-content'), cls='bb-ribbon-track')],
             pad=(18, 0), bg='#1B2225', ov=True, cls='bb-ribbon')


OFFERS = [
    ('winter-tire-change-calgary', 'tires', 'CALGARY · WINTER READY', 'New season.<br>Right tires.', None, None, 'Book your tire change'),
    ('mobil-1-synthetic-oil-change-calgary', 'oil', 'MOBIL 1 SYNTHETIC OIL CHANGE', 'FROM $75', 'Includes a complimentary vehicle inspection',
     'Starting price · vehicle-dependent', 'Book an oil change'),
    ('battery-alternator-service-calgary', 'battery', 'BATTERY TESTING', 'FREE', 'Battery test + charging-system check',
     'Repairs and replacement parts extra', 'Get your battery checked'),
]


def popup_link(popup_id):
    """Elementor Pro 'Popup' dynamic link (opens the popup and makes Elementor print it on the page)."""
    import urllib.parse
    st = urllib.parse.quote(json.dumps({'popup': str(popup_id)}, separators=(',', ':')))
    return {'link': f'[elementor-tag id="{uid()}" name="popup" settings="{st}"]'}


def cta_chip(text, dark_text=True, line=False, size=12, pad=(12, 16), ic_size=17, mar=(19, 0, 0, 0)):
    """Button-looking label used inside clickable cards (cards are links already, so no nested anchors)."""
    return C('CTA', [H(text, 'span', '#172024' if dark_text else PAPER, S(size, 750, 1.5), name='Label'),
                     ICON('arrow-up-right', ic_size, color='#172024' if dark_text else PAPER, name='Arrow', w='auto')],
             d='row', ai='center', gap=10, w='auto', mar=mar, pad=(10, 0, 0, 0) if line else pad,
             bg=None if line else YEL, radius=0 if line else 4, cls='bb-offer-cta-line' if line else 'bb-offer-cta')


def offer_post(img_key, theme, tag, title, benefit, terms, cta, popup_id):
    tires = theme == 'tires'
    copy = [H(tag, 'small', YEL, S(8 if tires else 11, 750, 12 if tires else 16.5, 0.8 if tires else 1.32), mar=(0, 0, 10, 0),
              name='Tag')]
    if tires:
        copy.append(H(title, 'strong', PAPER, S(33.84, 800, 34.855, -1.5228, size_t=27, lh_t=27.81, ls_t=-1.215), name='Title'))
        copy.append(cta_chip(cta, dark_text=False, line=True, size=10))
    else:
        copy += [H(title, 'strong', YEL, S(63.36, 900, 66.528, -3.8016, size_m=40, lh_m=42, ls_m=-2.4), name='Title'),
                 H(benefit, 'span', PAPER, S(16, 750, 21.6), mar=(12, 0, 0, 0), w=260, name='Benefit'),
                 H(terms, 'span', 'rgba(255,255,255,0.8)', S(10, 400, 15), mar=(10, 0, 0, 0), name='Terms'),
                 cta_chip(cta)]
    card = C('Offer – ' + theme, [
        IMG('busy-bee-auto-repair-logo', w=90, h=35, fit='contain', alt='Busy Bee Auto Repair', name='Logo', pos={'x': 18, 'y': 18},
            cls='bb-offer-logo'),
        C('Copy', copy, ai='flex-start', pos={'x': 22 if tires else 26, 'y': 22 if tires else 26, 'v': 'end',
                                              **({'x_tablet': 16, 'y_tablet': 16} if tires else {})},
          w=cu('calc(100% - 44px)' if tires else 'calc(100% - 52px)'), z=1),
    ], tag='a', bg='#182124' if tires else '#101719', bgimg=img_key, bgpos='center center' if tires else 'center 25%',
        radius=6, ov=True, cls=f'bb-offer bb-offer-{theme}', attrs={'aria-label': 'View promotion: ' + title.replace('<br>', ' ')})
    card['settings']['link'] = link('#')
    card['settings']['__dynamic__'] = popup_link(popup_id)
    return card


def winter():
    banner = C('Winter banner', [
        C('Copy', [
            H('BUSY BEE · CALGARY TIRE CHANGE SEASON', 'span', YEL, S(10, 750, 24, 1.5, lh_m=21), name='Tag'),
            H('Winter roads. Meet your match.', 'h2', PAPER, S(cu('clamp(28px, 3vw, 44px)'), 400, 1.08, cu('-0.04em'), 'uppercase'),
              mar=(14, 0, 12, 0), w=540, w_mobile='full', name='Title'),
            T('<p>Seasonal tire changes, balancing and checks for the months ahead.</p>', '#E1E4E5', S(13, 400, 20.8), w=410,
              w_mobile='full', name='Text'),
        ], w='auto', w_tablet=pct(100), z=1),
        BTN('Book your tire change', TEL, S(13, 750, 19.5), color='#172024', bg=YEL, ic='arrow-up-right', ic_size=18, ic_gap=16,
            pad=(15, 21), radius=5, name='Book your tire change'),
    ], d='row', d_tablet='column', jc='space-between', ai='flex-end', ai_tablet='flex-start', gap=24, pad=(36, 40), minh=220,
        bg='#161D1F', bgimg='winter-tire-change-calgary', bgpos='50% 60%', radius=8, ov=True, cls='bb-winter-banner')
    head = C('Heading', [H('REAL SERVICES. CLEAR VALUE.', 'p', '#1B2225', S(10, 750, 15, 1.5), name='Label'),
                         H('Explore our service offers', 'span', '#687174', S(12, 400, 18), name='Note', hide='m')],
             d='row', jc='space-between', ai='center', mar=(34, 0, 18, 0))
    ids = json.load(open('ids.json'))
    pids = [ids['popup_tires'], ids['popup_oil'], ids['popup_battery']]
    posts = C('Offers', [offer_post(*o, pids[i]) for i, o in enumerate(OFFERS)], grid='repeat(3, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))',
              grid_mobile='1fr', gap=22, rows='auto', rows_tablet='auto', rows_mobile='auto', cls='bb-offers')
    return C('Winter ready', [banner, head, posts], tag='section', id_='winter-ready', pad=(52, 32, 70, 32), pad_tablet=(30, 20),
             w=cu('min(1504px, 100%)'), mar=(0, 'auto'), bg=PAPER, cls='bb-winter bb-sys', attrs={'data-popup': pids[0]})


# ================================================================ BRANDS
BRAND_LOGOS = [('audi-logo', 'Audi'), ('bmw-logo', 'BMW'), ('mercedes-benz-logo', 'Mercedes-Benz'), ('porsche-logo', 'Porsche'),
               ('toyota-logo', 'Toyota'), ('ford-logo', 'Ford'), ('gmc-logo', 'GMC'), ('hyundai-logo', 'Hyundai'), ('dodge-logo', 'Dodge')]
ALL_BRANDS = ['Acura', 'Alfa Romeo', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Dodge', 'Fiat', 'Ford', 'Genesis',
              'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jeep', 'Kia', 'Land Rover', 'Lexus', 'Lincoln', 'Mazda', 'Mercedes-Benz',
              'Mitsubishi', 'Nissan', 'Porsche', 'RAM', 'Skoda', 'Smart', 'Subaru', 'Suzuki', 'Toyota', 'Volkswagen', 'Volvo']
DK = '#1B2225'


def section_eyebrow(text, color=DK, mar=(0, 0, 0, 0)):
    return H(text, 'p', color, S(10, 800, 15, 2, 'uppercase'), name='Eyebrow', mar=mar)


def brands():
    intro = C('Intro', [
        C('Left', [section_eyebrow('Domestic &amp; import specialists'),
                   H('Your car.<br>Our expertise.', 'h2', DK, S(cu('clamp(36px, 4vw, 52px)'), 800, 1.06, cu('-0.045em'), 'uppercase'),
                     mar=(25, 0, 0, 0), name='Title')], w='auto'),
        C('Right', [T('<p>Our mechanics work on domestic, Asian, and European vehicles every day.</p>', '#748085', S(14, 400, 26.6),
                      name='Text'),
                    ILIST([('arrow-right', 'Talk to our team', TEL)], t=S(12, 800, 18), color=DK, ic_color=DK, ic_size=18, gap_=12,
                          mar=(20, 0, 0, 0), name='Talk to our team', cls='bb-icon-after')],
          w=380, w_mobile=pct(100), mar_mobile=(22, 0, 0, 0)),
    ], d='row', d_mobile='column', jc='space-between', ai='flex-end', ai_mobile='flex-start', gap=50, gap_mobile=0, mar=(0, 0, 42, 0))
    cells = [C('Brand – ' + n, [IMG(k, w=115, h=62, fit='contain', alt=n + ' logo', name='Logo', width_mobile=px(75),
                                    height_mobile=px(48)),
                                H(n, 'span', '#7B8588', S(10, 600, 1.5, 0.6, size_m=9), name='Name')],
               ai='center', jc='center', gap=16, minh=155, minh_mobile=120, bg='#FBFCFB', cls='bb-brand-cell')
             for k, n in BRAND_LOGOS]
    gallery = C('Brand gallery', cells, grid='repeat(3, minmax(0, 1fr))', gap=0, rows='auto', radius=20, border=(1, '#E8EBEA'), ov=True,
                cls='bb-brand-gallery')
    alllist = ILIST([('arrow-up-right', b, None) for b in ALL_BRANDS], t=S(12, 400, 18), color=DK, ic_color=DK, ic_size=13, gap_=8,
                    mar=(32, 0), name='All brands', cls='bb-allbrands')
    bottom = C('Bottom', [
        ILIST([('badge-check', 'All makes. All models. One trusted shop.', None)], t=S(11, 400, 16.5), color='#343F42',
              ic_color='#343F42', ic_size=18, gap_=8, name='Promise'),
        H('Dealer-sourced parts available', 'span', '#7B8588', S(11, 400, 16.5), name='Note'),
    ], d='row', d_mobile='column', jc='space-between', ai_mobile='flex-start', gap=20, gap_mobile=12)
    return C('Vehicle brands', [C('Wrap', [intro, gallery, alllist, bottom], w=cu('min(1152px, 100%)'), mar=(0, 'auto'))],
             tag='section', id_='vehicle-brands', pad=(90, 32, 60, 32), pad_mobile=(56, 20), bg=PAPER, cls='bb-brands bb-sys')


# ================================================================ SYMPTOM CHECKER
def form_field(fid, ftype, label, ph='', width='100', required=False, **extra):
    f = {'_id': fid, 'custom_id': fid, 'field_type': ftype, 'field_label': label, 'placeholder': ph, 'width': width,
         'width_tablet': width, 'width_mobile': width,
         'required': 'true' if required else ''}
    f.update(extra)
    return f


def checker():
    head = C('Heading', [
        C('Left', [H('BUSY BEE / SYMPTOM CHECKER', 'p', DK, S(10, 800, 15, 1.6), mar=(0, 0, 22, 0), name='Eyebrow'),
                   H('Know your car.<br><span class="bb-muted">Understand the signs.</span>', 'h2', DK,
                     S(48, 700, 1.12, -2.16, size_m=36, ls_m=-1.62), name='Title')], w='auto'),
        T('<p>Tell us what’s happening. We’ll help you understand the possible causes and your next step.</p>', '#717779',
          S(14, 400, 25.2), w=315, mar_mobile=(20, 0, 0, 0), name='Intro'),
    ], d='row', d_mobile='column', jc='space-between', ai='flex-end', ai_mobile='flex-start', gap=60, gap_mobile=0, mar=(0, 0, 45, 0))
    studio = C('Vehicle studio', [
        C('Top', [H('YOUR VEHICLE', 'span', '#7D8587', S(9, 700, 13.5, 1.08), name='Label'),
                  H('01 / OVERVIEW', 'span', '#7D8587', S(9, 700, 13.5, 1.08), name='Step')], d='row', jc='space-between'),
        H('Let’s meet your car.', 'h3', DK, S(32, 700, 48, -1.12), mar=(34, 0, 0, 0), name='Vehicle title', cls='bb-veh-title'),
        H('<span class="bb-veh-year">Year</span><span class="bb-sep"> / </span><span class="bb-veh-km">Mileage</span>', 'p', '#7B8385',
          S(12, 400, 18), mar=(8, 0, 0, 0), name='Spec', cls='bb-veh-spec'),
        IMG('honda-civic-symptom-checker', w=cu('calc(100% + 60px)'), fit='contain', alt='Illustrative white Honda Civic studio render',
            name='Car render', mar=(12, -30, 0, -30), cls='bb-veh-img'),
        C('Caption', [H('HONDA CIVIC · ILLUSTRATIVE PREVIEW', 'span', '#8A9294', S(8, 400, 12, 0.32), name='Caption'),
                      H('Vehicle image matching coming next', 'span', '#8A9294', S(8, 400, 12, 0.32), name='Note')],
          d='row', wrap='wrap', jc='space-between', gap=10, mar=(8, 0, 0, 0)),
        C('Bottom', [ICON('shield-check', 19, color='#6B7476', name='Shield', w='auto'),
                     T('<p>Your description is the starting point.<br><strong>A technician confirms the diagnosis.</strong></p>',
                       '#6B7476', S(11, 400, 19.8), name='Text', cls='bb-strong-dark')],
          d='row', ai='center', gap=12, pad=(32, 0, 0, 0), cls='bb-push-bottom'),
    ], pad=30, pad_mobile=24, bg='#F6F7F7', ov=True, cls='bb-studio')
    fields = [
        form_field('make', 'text', 'Make', 'e.g. Honda', '50'),
        form_field('model', 'text', 'Model', 'e.g. Civic', '50'),
        form_field('year', 'text', 'Year', 'e.g. 2022', '50'),
        form_field('mileage', 'text', 'Mileage (km)', 'e.g. 65,000', '50'),
        form_field('issue', 'textarea', 'Describe the issue',
                   'What do you hear or feel? When does it happen? Any warning lights? Tell us as much as you can.', '100', True, rows=4),
        form_field('chips', 'html', '', '', '100',
                   field_html='<div class="bb-chips"><button type="button" data-add="Unusual noise">Unusual noise +</button>'
                              '<button type="button" data-add="Warning light">Warning light +</button>'
                              '<button type="button" data-add="Trouble starting">Trouble starting +</button>'
                              '<button type="button" data-add="Vibration">Vibration +</button></div>'),
    ]
    form = W('form', 'Symptom form', form_name='Symptom check', form_fields=fields, input_size='sm', show_labels='yes',
             button_text='Check my symptoms', button_size='sm', button_width='100', selected_button_icon=icon('arrow-right'),
             button_icon_align='row-reverse', submit_actions=['email'], email_to=EMAIL,
             email_subject='Symptom check from busybeeautorepair website', email_content='[all-fields]',
             email_from_name='Busy Bee website', success_message='Thanks! A Busy Bee technician will review this and call you back. '
             'Need it sooner? Call (403) 930-5888.', column_gap=px(14), row_gap=px(19), label_spacing=px(8),
             label_color='#41494B', **{('label_' + k): v for k, v in S(11, 600, 16.5).items()},
             field_text_color=DK, **{('field_' + k): v for k, v in S(12, 400, 18).items()},
             field_background_color=PAPER, field_border_color='#DCE1E2', field_border_width=dims(1), field_border_radius=dims(6),
             button_background_color=YEL, button_text_color='#151C1E', button_background_hover_color='#F2DC00',
             button_hover_color='#151C1E', button_border_radius=dims(7), button_text_padding=dims(17, 20),
             **{('button_' + k): v for k, v in S(13, 800, 19.5).items()}, cls='bb-checker-form')
    panel = C('Form panel', [
        H('02 / THE DETAILS', 'span', '#8B9395', S(9, 700, 24, 1.08), name='Step'),
        H('What’s going on?', 'h3', DK, S(26, 700, 39, -0.91), mar=(12, 0, 27, 0), name='Title'),
        form,
    ], pad=34, pad_mobile=24, bg=PAPER, border=(dims(0, 0, 0, 1), '#E4E7E7'), cls='bb-form-panel')
    grid = C('Checker grid', [studio, panel], grid='1.2fr 1fr', grid_mobile='1fr', rows='auto', rows_mobile='auto', gap=0,
             radius=18, border=(1, '#E4E7E7'), ov=True)
    return C('Symptom check', [C('Wrap', [head, grid], w=cu('min(1240px, 100%)'), mar=(0, 'auto'))],
             tag='section', id_='symptom-check', pad=(90, 32), pad_mobile=(50, 20), bg=PAPER, cls='bb-checker bb-sys')


# ================================================================ WHY BUSY BEE
def why():
    P = lambda x, y, w, h: dict(pos={'x': pct(x), 'y': pct(y)}, w=pct(w), minh=cu(f'{h}%'))
    spine = C('Spine', [H('Why Busy Bee', 'span', '#141615', S(64, 900, 64, -4, 'uppercase', size_m=38, lh_m=38, ls_m=-2),
                          name='Vertical title', cls='bb-vertical')], ai='center', jc='center', ov=True, cls='bb-why-spine',
                **P(2.33, 3.28, 14.69, 70.16))
    heading = C('Heading', [
        H('Why Calgary Drivers Choose Our Mechanics', 'h2', '#141615', S(28, 800, 31.64, -1, 'uppercase', size_m=27, lh_m=28.35,
                                                                             ls_m=-1.4), w=560, w_mobile='full', name='Title'),
        T('<p>Family-owned, locally run. Our name is on every job, and our reputation depends on getting it right.</p>', '#333333',
          S(13, 400, 19.5, size_m=14, lh_m=22.4), mar=(18, 0, 0, 0), w=500, w_mobile='full', name='Text'),
    ], pad=(25, 22, 10, 12), pad_mobile=24, cls='bb-why-heading', **P(17, 3.28, 52.93, 31.8))
    diag = C('Diagnosis', [
        ICON('arrow-up-right', 25, color='#141615', name='Arrow', pos={'x': 14, 'y': 14, 'h': 'end'}, cls='bb-why-arrow', w='auto'),
        H("Honest diagnosis first. We find the real cause before we replace anything, so you don't pay for parts you didn't need.",
          'h3', '#141615', S(26, 750, 1.23, -0.6, 'uppercase', size_m=22, lh_m=27.5, ls_m=-0.8), name='Title', cls='bb-why-diag-title'),
        BTN('Book appointment', BOOK, S(13, 700, 19.5), color='#141615', bg='rgba(0,0,0,0)', ic='arrow-right', ic_size=18, ic_gap=25,
            pad=(9, 16), radius=30, border=(1, '#141615'), hover_bg='#141615', hover_color=YEL, name='Book appointment',
            pos={'x': 30, 'y': 20, 'v': 'end'}, cls='bb-why-btn'),
    ], pad=(87, 30, 22, 30), pad_mobile=24, cls='bb-why-diag', **P(18.18, 24.92, 51.75, 48.52))
    quotes = C('Quotes', [
        IMG('brake-repair-calgary', w=pct(100), h=cu('100%'), fit='cover', alt='Technician inspecting a vehicle brake system',
            name='Photo', cls='bb-why-quotes-img'),
        H('Clear, upfront quotes.<span>You approve every repair and price before we start. No surprises at pickup.</span>', 'h3',
          '#141615', S(cu('1.35cqw'), 800, 1.25, tt='uppercase', size_m=18, lh_m=25.2), name='Title', cls='bb-why-quotes-title'),
    ], pad=(18, 24), pad_mobile=23, bg=PAPER, radius=36.192, radius_mobile=24, ov=True, cls='bb-why-quotes', **P(27.04, 75.41, 42.89, 21.31))
    fix = C('Fix', [
        IMG('computer-diagnostics-calgary', w=pct(100), h=cu('100%'), fit='cover', posn='center 30%', alt='Technician diagnosing a vehicle',
            name='Photo', cls='bb-why-fix-img'),
        H('Finds the real problem and fixes it right the first time.', 'h3', PAPER, S(17, 700, 20.4, -0.4176, 'uppercase', size_m=21,
                                                                                         lh_m=26.25, ls_m=0), name='Title', z=1),
    ], d='row', ai='flex-end', pad=18, pad_mobile=22, bg='#242927', radius=36.192, radius_mobile=24, ov=True, cls='bb-why-fix',
        **P(2.33, 75.41, 23.31, 21.31))
    makes = C('Makes', [
        IMG('engine-repair-audi-calgary', w=pct(100), h=cu('100%'), fit='cover', posn='43% center',
            alt='Mechanic working on a vehicle in a workshop', name='Photo', cls='bb-why-makes-img'),
        C('Copy', [ICON('car-front', 32, color=PAPER, name='Car', w='auto'),
                   H('ALL MAKES', 'h3', PAPER, S(32, 850, 48, -1), mar=(15, 0, 0, 0), mar_mobile=(18, 0, 0, 0), name='Title'),
                   T('<p>Cars · SUVs · Trucks</p>', '#DDDDDD', S(13, 400, 19.5), mar=(5, 0, 0, 0), name='Text')],
          pos={'x': 25, 'y': 25, 'v': 'end'}, w='auto', z=1, cls='bb-why-makes-copy'),
    ], bg='#343A38', radius=36.192, radius_mobile=24, ov=True, cls='bb-why-makes', **P(71.33, 3.28, 26.34, 93.44))
    board = C('Why board', [spine, heading, diag, quotes, fix, makes], minh=680, radius=36, bg='#050505', cls='bb-why-board')
    return C('Why Busy Bee', [board], tag='section', id_='why-busy-bee', pad=(72, 24), pad_mobile=(40, 24), bg=PAPER,
             cls='bb-why bb-sys')


# ================================================================ REVIEWS
REVIEWS_DATA = [
    ('Fair pricing, honest work, and zero feeling of being taken advantage of.', 'Allyson R.', 'General repair', 'AR'),
    ('The techs listened, ran a quick diagnostic, and pinpointed a worn lift pump. They replaced the part same day. Prices were transparent.',
     'Rai S.', 'Computer diagnostics', 'RS'),
    ('They did an excellent job with my oil change: fast, professional, and friendly.', 'Armanjot K.', 'Oil change', 'AK'),
    ('Despite not having an appointment, they helped me last minute with my car battery issue.', 'Ruby S.', 'Battery service', 'RS'),
    ('They quickly diagnosed the issue and explained everything clearly, at a very reasonable price.', 'Kultar S.', 'Computer diagnostics',
     'KS'),
]
GTOP = ['#4285F4', '#EA4335', '#FBBC05', '#34A853']


def review_card(i, quote, name, service, initials):
    blue = i % 2 == 0
    return C('Review – ' + name, [
        C('Top', [H('★★★★★', 'span', '#FBBC05', S(19, 400, 28.5, 3), name='Stars'),
                  IMG('google-g-mark', w=28, alt='Google', name='Google mark')], d='row', jc='space-between', ai='center',
          mar=(0, 0, 24, 0)),
        T(f'<p>“{quote}”</p>', ink(0.65), M(14, 400, 24), name='Quote'),
        C('Author', [H(initials, 'div', '#1967D2' if blue else '#C5221F', M(10, 700, 15), align='center', name='Initials',
                       w=32, cls='bb-avatar', _background_background='classic', _background_color='#E8F0FE' if blue else '#FCE8E6',
                       _border_radius=dims(PILL)),
                     C('Name', [H(name, 'p', INK, M(14, 600, 20), name='Name'), H(service, 'p', ink(0.45), M(12, 400, 16), name='Service')],
                       w='auto')],
          d='row', ai='center', gap=12, pad=(40, 0, 0, 0), cls='bb-push-bottom'),
    ], tag='figure', pad=24, bg=PAPER, radius=16, minh=285, border=(dims(3, 1, 1, 1), '#E5E8EC'),
        shadow=shadow(0, 8, 24, 0, 'rgba(32,33,36,0.024)'), cls=f'bb-review bb-reveal bb-gtop-{i % 4}')


def summary_card():
    return C('Rating summary', [
        H('★★★★★', 'span', INK, S(16, 400, 16, 2), name='Stars'),
        H('4.8', 'p', INK, M(48, 600, 48), mar=(20, 0, 0, 0), name='Rating'),
        T('<p>Rated by local drivers on Google for honest pricing and clear answers.</p>', ink(0.7), M(14, 400, 24), mar=(12, 0, 0, 0),
          name='Text'),
        BTN('Book your visit', BOOK, M(12, 600, 16), color=PAPER, bg=INK, ic='arrow-right', ic_size=14, ic_gap=12, pad=(6, 6, 6, 16),
            radius=PILL, name='Book your visit', cls='bb-visit-btn bb-push-bottom'),
    ], tag='figure', pad=24, bg=PAPER, radius=16, minh=279, border=(dims(3, 1, 1, 1), '#E5E8EC'),
        shadow=shadow(0, 8, 24, 0, 'rgba(32,33,36,0.024)'), cls='bb-review bb-review-summary bb-reveal bb-gtop-1')


def reviews():
    head = C('Head', [
        C('Pill', [IMG('google-g-mark', w=28, alt='Google', name='Google mark'),
                   H('Service you can trust', 'span', '#555555', M(11, 600, 16.5, 0.88, 'uppercase'), name='Label')],
          d='row', ai='center', gap=12, pad=(10, 32), bg=PAPER, radius=PILL, border=(1, '#E8EAED'), w='auto', mar=(0, 'auto')),
        H('What our customers say', 'h2', INK, M(48, 800, 1.05, tt='uppercase', size_m=28), align='center', mar=(12, 0, 0, 0),
          name='Title'),
        T('<p>4.8 stars on Google from Calgary drivers.</p>', ink(0.6), M(16, 400, 24, size_m=14), align='center', mar=(16, 0, 0, 0),
          name='Intro'),
    ], w=cu('min(672px, 100%)'), mar=(0, 'auto'), cls='bb-reveal')
    track = C('Review track', [review_card(i, *r) for i, r in enumerate(REVIEWS_DATA[:4])] + [review_card(4, *REVIEWS_DATA[4]),
                                                                                             summary_card()],
              d='row', gap=12, pad=(0, 0, 12, 0), mar=(56, 0, 0, 0), mar_mobile=(32, 0, 0, 0), cls='bb-review-track', ai='flex-start')
    nav = C('Review nav', [
        ICON('arrow-left', 14, color=INK, bg='rgba(229,232,234,0.45)', box=28, name='Previous', cls='bb-rev-prev', w='auto',
             href='#reviews'),
        ICON('arrow-right', 14, color=INK, bg='rgba(229,232,234,0.45)', box=28, name='Next', cls='bb-rev-next', w='auto',
             href='#reviews'),
        H('Read all Google reviews', 'span', INK, M(10, 800, 15, 1.6, 'uppercase'), href=REVIEWS, mar=(0, 0, 0, 8),
          name='Read all reviews', cls='bb-greviews-link'),
    ], d='row', ai='center', gap=8, mar=(40, 0, 0, 0), mar_mobile=(24, 0, 0, 0))
    return C('Reviews', [head, track, nav], tag='section', id_='reviews', pad=(65, 64, 112, 64), pad_tablet=(65, 40, 112, 40),
             pad_mobile=(65, 20, 40, 20), bg=PAPER, cls='bb-reviews')


# ================================================================ HOW IT WORKS
def stage(n, inner, connector=True):
    kids = [H(f'0 {n}', 'span', '#7A8284', S(12, 800, 18, 2), name='Number', pos={'x': 15, 'y': 15}, w='auto'), inner]
    return C('Stage', kids, ai='center', jc='center', minh=235, radius=13, ov=True, cls='bb-stage')


def process_card(n, title, text, inner, last=False):
    kids = [stage(n, inner)]
    if not last:
        kids.append(ICON('arrow-right', 20, color='#929B9E', name='Connector', pos={'x': -24, 'y': 114, 'h': 'end'}, z=2,
                         cls='bb-connector', w='auto'))
    kids += [H(title, 'h3', DK, S(18, 800, 23.4, -0.54, 'uppercase'), mar=(24, 14, 12, 14), name='Title',
               cls='bb-proc-title'),
             T(f'<p>{text}</p>', '#596569', S(13, 400, 24.05), mar=(0, 14), name='Text')]
    return C('Step ' + str(n), kids, pad=(10, 10, 28, 10), bg=PAPER, radius=20, border=(1, '#E8E9E9'), cls='bb-proc-card')


def stage_book():
    cal = ''.join(f'<i{" class=\"sel\"" if d == 10 else ""}>{d}</i>' for d in range(1, 15))
    return C('Your visit', [
        H('YOUR VISIT', 'span', DK, S(9, 700, 13.5, 1), name='Label'),
        H(cal, 'div', DK, S(9, 400, 13.5), name='Mini calendar', cls='bb-cal'),
        ICON('car-front', 38, color=DK, name='Car', cls='bb-stage-book-car', w='auto', pos={'x': -25, 'y': -15, 'h': 'end', 'v': 'end'}),
    ], ai='center', pad=14, w=145, cls='bb-stage-book')


def stage_scan():
    return C('Scan', [
        ICON('car-front', 100, color='#293236', name='Car', w='auto', cls='bb-scan-car'),
        C('Scan line', [], w=135, minh=2, cls='bb-scan-line', pos={'x': pct(50), 'y': 48}),
        ILIST([('scan-search', 'DIAGNOSTIC CHECK', None)], t=S(8, 400, 12, 0.5), color=DK, ic_color=DK, ic_size=16, gap_=6,
              name='Label'),
        H('<i></i><i></i><i></i>', 'div', DK, S(8, 400, 5), name='Meters', cls='bb-meters'),
    ], ai='center', gap=12, w='auto', cls='bb-stage-scan')


def stage_approval():
    return C('Estimate', [
        ICON('clipboard-check', 43, color=DK, name='Clipboard', w='auto'),
        H('REPAIR ESTIMATE', 'span', DK, S(9, 700, 13.5, 1), name='Label', mar=(9, 0, 0, 0)),
        H('<i></i><i></i><i></i>', 'div', DK, S(8, 400, 4), name='Lines', cls='bb-est-lines'),
        ILIST([('check', 'YOU APPROVE', None)], t=S(8, 800, 12), color=DK, ic_color=DK, ic_size=20, gap_=6, name='You approve',
              cls='bb-approve-pill', mar=(14, 0, 0, 0)),
    ], pad=16, w=150, cls='bb-stage-approval')


def stage_drive():
    return C('Drive', [
        ICON('shield-check', 29, color=DK, bg=YEL, box=45, name='Shield', w='auto', cls='bb-drive-shield'),
        ICON('car-front', 94, color=DK, name='Car', w='auto', cls='bb-drive-car'),
        C('Road', [], w=155, minh=2, mar=(5, 0, 0, 0), cls='bb-road'),
        H('READY FOR THE ROAD', 'span', DK, S(8, 400, 12, 1), mar=(17, 0, 0, 0), name='Label'),
    ], ai='center', w='auto', cls='bb-stage-drive')


def process():
    head = C('Heading', [
        C('Left', [section_eyebrow('The Busy Bee way'),
                   H('Good repairs.<br>No surprises.', 'h2', DK, S(cu('clamp(36px, 4vw, 52px)'), 800, 1.06, cu('-0.045em'), 'uppercase'),
                     mar=(25, 0, 0, 0), name='Title'),
                   T('<p>Auto repair in NE Calgary made simple. From brake repairs and oil changes to vehicle diagnostics, Busy Bee Auto '
                     'Repair explains what your car needs, provides a clear estimate, and gets your approval before work begins.</p>',
                     '#687276', S(14, 400, 25.2), mar=(22, 0, 0, 0), w=640, w_mobile='full', name='Intro')], w='auto', cls='bb-shrink'),
        T('<p>From the first conversation to the drive home, you’re in control. Clear answers. Honest estimates. Work you can trust.</p>',
          '#6C777B', S(14, 400, 26.6), w=340, w_mobile='full', mar_mobile=(22, 0, 0, 0), name='Aside', cls='bb-noshrink'),
    ], d='row', d_mobile='column', jc='space-between', ai='flex-end', ai_mobile='flex-start', gap=50, gap_mobile=0, mar=(0, 0, 42, 0))
    grid = C('Steps', [
        process_card(1, 'Book or walk in', 'Book auto repair in NE Calgary online, call (403) 930-5888, or walk into Busy Bee at 324 41 Ave NE. '
                     'Share your vehicle’s make, model and symptoms so our team can plan the right first check.', stage_book()),
        process_card(2, 'We diagnose and explain', 'Our mechanics inspect your vehicle and investigate warning lights, unusual noises or '
                     'performance concerns. We explain the findings and provide a clear repair estimate before any work begins.',
                     stage_scan()),
        process_card(3, 'You approve', 'Review the recommended repairs and quoted price with our team. Ask about the work your car needs '
                     'and approve the estimate before we start. You stay in control of your auto repair decisions.', stage_approval()),
        process_card(4, 'Drive away covered', 'Collect your vehicle after the agreed repairs are complete. We explain the work performed '
                     'and any recommended next steps. Most repairs include a parts and labour warranty; ask our team about coverage '
                     'for your job.', stage_drive(), last=True),
    ], grid='repeat(4, minmax(0, 1fr))', grid_tablet='minmax(169px, 1fr) minmax(141px, 1fr) minmax(174px, 1fr) minmax(179px, 1fr)', grid_mobile='minmax(174px, 1fr) minmax(179px, 1fr)', gap=24,
        rows='auto', rows_tablet='auto', rows_mobile='auto', cls='bb-proc-grid')
    note = C('Note', [
        ILIST([('shield-check', 'Your approval comes before every repair.', None)], t=S(11, 400, 16.5, lh_m=17.6), color='#6C777B',
              ic_color='#6C777B', ic_size=18, gap_=9, name='Note'),
        ILIST([('arrow-right', 'Let’s get you booked', BOOK)], t=S(11, 800, 16.5, lh_m=17.6), color=DK, ic_color=DK, ic_size=16, gap_=8,
              name='Book link', cls='bb-icon-after', w_mobile=pct(100)),
    ], d='row', wrap='wrap', jc='space-between', ai='center', gap=9, mar=(28, 0, 0, 0))
    return C('How it works', [C('Wrap', [head, grid, note], w=cu('min(1152px, 100%)'), mar=(0, 'auto'))], tag='section',
             id_='how-it-works', pad=(90, 32), bg=PAPER, cls='bb-process bb-sys')


# ================================================================ PRICING
PRICES = [
    ('battery-charging', 'Battery testing', 'Free', 'Free battery testing plus a full charging system check — especially wise before a Calgary cold snap.',
     ['Free battery testing', 'Full charging system checks', 'Long-term warranty options'], False),
    ('droplets', 'Mobil 1 synthetic oil change', 'From $75', 'Premium Mobil 1 synthetic oil with a complimentary vehicle inspection.',
     ['Premium Mobil 1 synthetic oil', 'Complimentary vehicle inspection', 'Often done the same day'], True),
    ('wrench', 'Wheels &amp; tires', 'From $84', 'Tire repair up to 16 inches, wheel balancing, rotations, and new and used tires.',
     ['Tire repair (up to 16″) — $84', 'Balancing and rotations', 'Honest advice on repair vs. replace'], False),
]


def price_card(i, ic, label, price, desc, items, popular):
    kids = []
    if popular:
        kids.append(ILIST([('star', 'Popular', None)], t=M(10, 800, 15), color=PAPER, ic_color=PAPER, ic_size=12, gap_=4,
                          name='Popular', pos={'x': 0, 'y': 0, 'h': 'end'}, cls='bb-popular', w='auto', pad=(4, 10),
                          _background_background='classic', _background_color=INK,
                          _border_radius=dims(0, 8, 0, 10)))
    kids += [
        ICON(ic, 20 if popular else 19, color=INK, bg=BEE, box=40 if popular else 38, name='Icon', align='center'),
        H(label, 'p', ink(0.5), M(12, 800, 16, tt='uppercase'), align='center', mar=(20, 0, 0, 0), name='Label'),
        H(price, 'h3', INK, M(30, 800, 37.5, tt='uppercase', size_m=24, lh_m=30), align='center', mar=(24, 0, 0, 0), name='Price'),
        T(f'<p>{desc}</p>', ink(0.45), M(12, 400, 20), align='center', mar=(8, 0, 0, 0), name='Description'),
        ILIST([('check', x, None) for x in items], t=M(14, 500, 20), color=INK, ic_color='#020618', ic_size=16 if popular else 15,
              gap_=8, space=12, name='Includes', pad=(20, 0, 0, 0), mar=(24, 0, 28, 0), cls='bb-price-list',
              _border_border='solid', _border_width=dims(1, 0, 0, 0), _border_color=ink(0.1)),
        BTN('Get your estimate', BOOK, M(14, 700, 20), color=PAPER if popular else INK, bg=INK if popular else PAPER,
            pad=(12 if popular else 10.5, 16), radius=PILL if popular else 8, border=(1, INK if popular else '#E2E8F0'),
            sh=SH_INK if popular else SH_SM, align='justify', name='Get your estimate', cls='bb-push-bottom'),
        T('<p>You always approve before work starts.</p>', ink(0.4), M(10, 400, 16), align='center', mar=(16, 0, 0, 0), name='Note'),
    ]
    return C('Price – ' + label, kids, pad=28, bg=PAPER, radius=10, border=(2, INK) if popular else (1, ink(0.1)),
             shadow=shadow(0, 20, 25, -5, 'rgba(0,0,0,0.1)') if popular else None, minh=540 if popular else 470,
             minh_mobile=470 if popular else None, tag='article', z=20 if popular else 10,
             cls='bb-price' + (' bb-price-pop' if popular else f' bb-price-side bb-price-{"first" if i == 0 else "last"}'))


def pricing():
    head = C('Head', [
        H('Straightforward Pricing', 'h2', INK, M(48, 800, 1.05, tt='uppercase', size_m=28), align='center', name='Title'),
        T('<p>Most repairs are quoted after a quick diagnosis, because the right price depends on your vehicle. Here are our published '
          'starting prices.</p>', ink(0.55), M(16, 400, 28, size_m=14), align='center', mar=(16, 0, 0, 0),
          w=cu('min(672px, 100%)'), name='Intro'),
    ], w=cu('min(768px, 100%)'), mar=(0, 'auto'), ai='center')
    toggle = C('Approval toggle', [
        C('Switch', [C('Knob', [], w=16, minh=16, bg=PAPER, radius=PILL)], d='row', jc='flex-end', ai='center', w=36, minh=20, pad=2,
          bg=INK, radius=PILL),
        H('You approve the estimate before work starts', 'p', INK, M(14, 700, 20), name='Label'),
    ], d='row', jc='center', ai='center', gap=10, mar=(32, 0, 48, 0))
    cards = C('Price cards', [price_card(i, *p) for i, p in enumerate(PRICES)], grid='repeat(3, minmax(0, 1fr))', grid_mobile='1fr',
              gap=0, gap_mobile=16, rows='auto', rows_mobile='auto', ai='center', cls='bb-price-grid')
    return C('Pricing', [C('Wrap', [head, toggle, cards,
                                    T('<p>Final pricing depends on your vehicle\'s make, model and condition. You always approve the '
                                      'estimate before work starts.</p>', ink(0.5), M(12, 400, 24), align='center', mar=(32, 0, 0, 0),
                                      name='Footnote')],
                                   w=cu('min(1024px, 100%)'), mar=(0, 'auto'))],
             tag='section', id_='pricing', pad=(112, 32), pad_mobile=(40, 20), bg=PAPER, cls='bb-pricing')


# ================================================================ FAQ
FAQS = [
    ('Do you work on all makes and models?', 'Yes. We service domestic, Asian, and European cars, SUVs, and light trucks.'),
    ('Do I need an appointment?', 'Appointments get you in fastest, but walk-ins are welcome.'),
    ('How much does a diagnostic cost?', "It depends on the issue. We'll quote the diagnostic upfront and always ask before doing any repairs."),
    ('Do your repairs come with a warranty?', "Yes. Parts and labour are covered, and we'll explain the terms for your specific repair."),
    ('Where are you located?', '324 41 Ave NE, Calgary, AB T2E 2N3.'),
]


def faq():
    left = C('Intro', [
        H('Questions, answered', 'p', ink(0.5), M(11, 800, 16.5, 2.64, 'uppercase'), name='Eyebrow'),
        H('Frequently Asked Questions', 'h2', INK, M(48, 800, 1.05, tt='uppercase', size_m=28), mar=(12, 0, 0, 0), name='Title'),
        T("<p>If you have a different question, call the shop and we'll help you plan the next step.</p>", ink(0.65),
          M(16, 400, 28, size_m=14), mar=(16, 0, 0, 0), name='Intro'),
        BTN(PHONE, TEL, M(14, 500, 20), color=INK, bg=BEE, ic='phone', ic_pos='before', ic_size=16, pad=(18, 28), radius=8,
            border=(1, ink(0.2)), sh=SH_BEE, mar=(32, 0, 0, 0), name='Call'),
    ])
    toggle = W('toggle', 'FAQ', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in FAQS],
               selected_icon=icon('chevron-down'), selected_active_icon=icon('chevron-down'), icon_align='right', title_html_tag='h3',
               faq_schema='yes', border_width=px(0), space_between=px(0), title_color=INK, tab_active_color=INK, icon_color=INK,
               icon_active_color=INK, title_padding=dims(20, 0), content_padding=dims(0, 40, 20, 0), content_color=ink(0.65),
               **{('title_' + k): v for k, v in M(18, 800, 28, tt='uppercase', size_m=16, lh_m=24).items()},
               **{('content_' + k): v for k, v in M(14, 400, 28).items()}, cls='bb-faq')
    return C('FAQ', [C('Grid', [left, C('Questions', [toggle], border=(dims(1, 0, 0, 0), ink(0.15)))], grid='minmax(min-content, 0.8fr) 1.2fr',
                       grid_mobile='1fr', gap=48, gap_mobile=24, rows='auto', rows_mobile='auto', w=cu('min(1152px, 100%)'), mar=(0, 'auto'))],
             tag='section', id_='faq', pad=(112, 32), pad_mobile=(40, 20), bg=PAPER, cls='bb-faq-section')


# ================================================================ BOOK
REASONS = ['Scheduled maintenance', 'Oil change', 'Tire change', 'Brake issue', 'Noise complaint', 'Check engine or dash warning light',
           'Battery or starting issue', 'Repair estimate or diagnostic', 'Other']


def book():
    head = C('Head', [
        ICON('sparkles', 28, color=BEE, name='Sparkles', w='auto', cls='bb-sparkles'),
        H('Need a Mechanic in Calgary Today?', 'h2', INK, M(48, 800, 1.05, tt='uppercase', size_m=30), mar=(12, 0, 0, 0), name='Title'),
        T("<p>Call (403) 930-5888 or book online. We'll get you back on the road safely, without the runaround.</p>", ink(0.65),
          M(16, 400, 24, size_m=14), mar=(16, 0, 0, 0), w=576, w_mobile='full', name='Intro'),
    ], mar=(0, 0, 40, 0), mar_mobile=(0, 0, 32, 0))
    left = C('Promo', [
        C('Top', [
            IMG('busy-bee-auto-repair-logo', w=101, h=36, fit='contain', alt='Busy Bee Auto Repair', name='Logo', align='left'),
            C('Calls', [
                BTN(PHONE, TEL, M(12, 600, 16), color=PAPER, bg=INK, ic='phone', ic_pos='before', ic_size=14, pad=(8, 16), radius=8,
                    name='Phone', cls='bb-ic-bee'),
                BTN('Call the shop', TEL, M(12, 600, 16), color=INK, bg='rgba(0,0,0,0)', pad=(8, 16), radius=8, border=(1, ink(0.25)),
                    hover_bg=INK, hover_color=PAPER, name='Call the shop'),
            ], d='row', wrap='wrap', ai='center', gap=8, mar=(24, 0, 0, 0)),
            T('<p>Book online in under a minute. We call back to confirm your appointment.</p>', ink(0.7), M(12, 400, 20),
              mar=(20, 0, 0, 0), w=320, name='Text'),
        ]),
        H('Every repair <span>starts with a plan.</span>', 'p', INK, M(48, 600, 1.02, size_m=36), mar=(40, 0, 0, 0), name='Tagline',
          cls='bb-tagline'),
        ILIST([('map-pin', '324 41 Ave NE, Calgary, AB T2E 2N3', MAPS)], t=M(12, 400, 20), color=ink(0.7), ic_color=ink(0.7),
              ic_size=16, gap_=8, mar=(32, 0, 0, 0), name='Address'),
    ], jc='space-between', pad=32, pad_mobile=24, grad=(BEE, 0, 'rgba(229,232,234,0.4)', 100, 180), cls='bb-book-promo')
    fields = [{'_id': 'reason', 'custom_id': 'reason', 'field_type': 'radio', 'field_label': 'Reason for your visit',
               'field_options': '\n'.join(REASONS), 'inline_list': 'elementor-subgroup-inline', 'width': '100', 'required': ''},
              form_field('name', 'text', 'Name', 'Name', '50', True),
              form_field('phone', 'tel', 'Phone number', 'Phone number', '50', True),
              form_field('vehicle', 'text', 'Vehicle make and model', 'Vehicle make and model', '100'),
              form_field('details', 'textarea', 'Briefly describe repair details', 'Briefly describe repair details', '100', rows=3),
              {'_id': 'hp', 'custom_id': 'hp', 'field_type': 'honeypot', 'field_label': '', 'width': '100'}]
    form = W('form', 'Booking form', form_name='Appointment request', form_fields=fields, input_size='sm', show_labels='yes',
             button_text='Request my appointment', button_size='sm', button_width='100', submit_actions=['email'], email_to=EMAIL,
             email_subject='New appointment request – busybeeautorepair website', email_content='[all-fields]',
             email_from_name='Busy Bee website', email_reply_to='',
             success_message="Thanks! We'll call you back within business hours to confirm your appointment.",
             column_gap=px(20), row_gap=px(0), field_text_color=PAPER, **{('field_' + k): v for k, v in M(14, 400, 20).items()},
             field_background_color='rgba(0,0,0,0)', field_border_color=wht(0.25), field_border_width=dims(0, 0, 1, 0),
             field_border_radius=dims(0), button_background_color=BEE, button_text_color=INK, button_background_hover_color='#E9CB0A',
             button_hover_color=INK, button_border_radius=dims(8), button_text_padding=dims(14, 16),
             **{('button_' + k): v for k, v in M(14, 700, 20).items()}, label_color=wht(0.6),
             **{('label_' + k): v for k, v in M(11, 700, 16.5, 1.54, 'uppercase').items()}, cls='bb-book-form')
    right = C('Form side', [
        H('<span>Book your visit.</span> Tell us what your vehicle needs.', 'h3', PAPER, M(30, 600, 36, tt='uppercase', size_m=24, lh_m=32),
          name='Title', cls='bb-book-title'),
        form,
        T('<p>We usually call back within business hours. Walk-ins welcome Monday to Friday, 9 AM to 6 PM.</p>', wht(0.45),
          M(11, 400, 20), mar=(12, 0, 0, 0), name='Note'),
    ], pad=32, pad_mobile=24, bg=INK)
    card = C('Booking card', [left, right], grid='0.9fr 1.1fr', grid_mobile='1fr', rows='auto', rows_mobile='auto', gap=0, radius=18,
             ov=True, shadow=shadow(0, 24, 60, -30, 'rgba(23,23,23,0.6)'))
    return C('Book', [C('Wrap', [head, card], w=cu('min(1152px, 100%)'), mar=(0, 'auto'))], tag='section', id_='book', pad=(56, 32),
             pad_mobile=(40, 20), bg=PAPER, cls='bb-book')


# ================================================================ PAGE
def build():
    el.seed('home')
    return [hero_mobile(), hero_desktop(), suppliers(), services(), ribbon(), winter(), brands(), checker(), why(), reviews(), process(), pricing(),
            faq(), book()]


PAGE_SETTINGS = {'hide_title': 'yes', 'template': 'elementor_header_footer'}

if __name__ == '__main__':
    ids = json.load(open('ids.json'))
    pid = ids['home']
    el.save('pages', pid, build(), page_settings=PAGE_SETTINGS, extra={'template': 'elementor_header_footer'})
    el.regen(pid)
