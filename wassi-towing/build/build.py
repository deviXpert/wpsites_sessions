"""Build Elementor JSON for the Wassi Towing header, footer, call band and Home page.

Run:  python3 build.py   -> writes out/*.json (Elementor template export format)
Values come straight from design/html/home.html (+ the stranded-mode state).
"""
import os, re
from lib import *

OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
HANDOFF = os.path.join(HERE, '..', 'handoff', 'Wassi_Towing_Website_Handoff')

def pill(*children, bg, pad=(8, 14), gap_=8, radius=999, **s):
    s.setdefault('_flex_align_self', 'flex-start')
    return con(*children, dir='row', flex_align_items='center', flex_gap=gap(gap_),
               padding=box(pad[0], pad[1]), border_radius=box(radius), width=px('auto'),
               width_mobile=px('auto'), background_background='classic', background_color=bg, **s)

def span(label, color, size, weight=400, family=INTER, lh=1.4, **s):
    return heading(label, 'span', color, **typo(family, weight, size, lh), **s)

# =============================================================================
# HEADER (Theme Builder > Header)
# =============================================================================
def header():
    strip = section(
        con(
            icon('alert', NAVY, 18, 2.2),
            heading(f'Stuck right now? A real person answers: <a href="{PHONE_HREF}"><strong>[PHONE]</strong></a>',
                    'span', NAVY, **typo(INTER, 600, 14, 1.35, size_m=13)),
            dir='row', flex_align_items='center', flex_gap=gap(8), width=px('auto'), width_mobile=px('auto'),
            _flex_size='custom', _flex_grow=0, _flex_shrink=1),
        button("I'm stuck right now", '#', bg=NAVY, color=WHITE, font=INTER, weight=700, size=14,
               height=36, padx=14, radius=999, attrs='data-wt-stranded|open',
               _flex_size='none'),
        bg=ORANGE, pt=8, pb=8, dir='row', flex_wrap='wrap', flex_justify_content='space-between',
        flex_align_items='center', flex_gap=gap(10), flex_wrap_mobile='nowrap', flex_gap_mobile=gap(10, 12),
        padding_mobile=box(8, 16))

    nav = widget('nav-menu',
        menu='primary', layout='horizontal', align_items='center', pointer='underline', animation_line='none',
        dropdown='mobile', toggle='burger', full_width='stretch', text_align='aside',
        _css_classes='wt-nav',
        **typo(INTER, 500, 15, 1.2, prefix='menu_typography'),
        color_menu_item=ON_DARK, color_menu_item_hover=WHITE, color_menu_item_active=WHITE,
        pointer_color_menu_item_hover=ORANGE, pointer_color_menu_item_active=ORANGE,
        pointer_width=px(2), padding_horizontal_menu_item=px(2), padding_vertical_menu_item=px(8),
        menu_space_between=px(28),
        color_dropdown_item=ON_DARK, background_color_dropdown_item=NAVY,
        color_dropdown_item_hover=WHITE, background_color_dropdown_item_hover=NAVY2,
        color_dropdown_item_active=WHITE, background_color_dropdown_item_active=NAVY2,
        **typo(INTER, 600, 17, 1.2, prefix='dropdown_typography'),
        padding_horizontal_dropdown_item=px(20), padding_vertical_dropdown_item=px(16),
        dropdown_top_distance=px(16),
        toggle_color=WHITE, toggle_background_color='rgba(0,0,0,0)', toggle_size=px(28),
        toggle_border_width=px(0), toggle_border_radius=px(10),
        _flex_size='none')

    actions = con(
        button('Get my quote', '/#quote', color=WHITE, weight=700, size=15, height=48, padx=22,
               border_w=1.5, border_c='rgba(255,255,255,0.35)'),
        button('Call [PHONE]', PHONE_HREF, bg=ORANGE, color=NAVY, weight=800, size=15, height=48, padx=20,
               icon_name='phone', icon_sw=2.4, icon_px=20),
        dir='row', flex_wrap='wrap', flex_gap=gap(10), width=px('auto'),
        hide_mobile='hidden-mobile')

    bar = section(
        image('WassiTowing_horizontal_reversed.svg', width=px(194), link='/', alt='Wassi Towing Ltd. home',
              _element_width='auto', width_mobile=px(160)),
        nav, actions,
        bg=NAVY, pt=16, pb=16, dir='row', flex_wrap='wrap', flex_justify_content='space-between',
        flex_align_items='center', flex_gap=gap(16, 28), flex_wrap_mobile='nowrap',
        padding_mobile=box(12, 16),
        sticky='top', sticky_on=['desktop', 'tablet', 'mobile'], sticky_effects_offset=0, z_index=100)
    return [strip, bar]

# =============================================================================
# CALL BAND (saved as its own template, inserted with the Template widget)
# =============================================================================
def callband():
    hazard = lambda: con(min_height=px(14), css_classes='wt-hazard')
    inner = con(
        con(
            h2('Stuck right now?', NAVY, size='clamp(2rem, 4vw, 3rem)', lh=1, ls=0),
            body('A real person picks up and stays with you until help arrives.', NAVY, 18, 1.5),
            flex_gap=gap(6), width=px(620), _flex_size='custom', _flex_grow=0, _flex_shrink=1),
        con(
            button('[PHONE]', PHONE_HREF, color=NAVY, font=MONT, weight=900, size=30, height=40, padx=0,
                   icon_name='phone', icon_sw=2.4, icon_gap=14, classes='wt-bigphone',
                   typography_font_style='italic',
                   typography_font_size=px('clamp(2rem, 4.4vw, 3.4rem)'),
                   typography_line_height=px(1, 'em'), text_padding=box(0),
                   button_background_hover_color='rgba(0,0,0,0)'),
            button('Or text us your location', SMS_HREF, bg=NAVY, color=WHITE, weight=800, size=16, height=52,
                   padx=22, icon_name='pin', icon_sw=2.4, icon_px=20, attrs='data-wt-sms-location|'),
            flex_align_items='flex-start', flex_gap=gap(12), width=px('auto')),
        content_width='boxed', boxed_width=px(1152), padding=box(56, 24), padding_mobile=box(48, 20),
        flex_direction='row', flex_wrap='wrap', flex_justify_content='space-between',
        flex_align_items='center', flex_gap=gap(28))
    return [full(hazard(), inner, hazard(), background_background='classic', background_color=ORANGE)]

# =============================================================================
# STRANDED MODE overlay (lives in the footer template so every page has it)
# =============================================================================
def stranded():
    def big(label, url, bg, color, weight, size, height, ic, isz, attrs='', bw=None, bc=None):
        return button(label, url, bg=bg, color=color, weight=weight, size=size, height=height, padx=24,
                      radius=20, icon_name=ic, icon_sw=2.6 if ic == 'phone' else 2.4, icon_px=isz,
                      icon_gap=14, attrs=attrs, border_w=bw, border_c=bc, full_width=True,
                      content_align='center')
    checks = []
    for t in ['Hazard lights on', 'Off the road or as far right as you can',
              'Everyone out on the side away from traffic, if safe',
              'Engine off if the exhaust may be blocked by snow']:
        checks.append(con(
            con(css_classes='wt-box', width=px(30), width_mobile=px(30), min_height=px(30),
                border_border='solid', border_width=box(2), border_color='#5A6B88', border_radius=box(9),
                _flex_size='none'),
            span(t, WHITE, 17, 400, lh=1.4),
            dir='row', flex_align_items='center', flex_gap=gap(14), min_height=px(56),
            padding=box(6, 4), border_border='solid', border_width=box(0, 0, 1, 0), border_color='#22324D',
            css_classes='wt-check', _attributes='role|button\ntabindex|0\naria-pressed|false'))
    inner = con(
        con(
            pill(icon('alert', ORANGE, 16, 2.4), span('STRANDED MODE', ORANGE, 14, 700), bg='#3A1A08'),
            button('Exit', '#', color=WHITE, font=INTER, weight=600, size=14, height=44, padx=16, radius=12,
                   border_w=1.5, border_c='#3A4A66', attrs='data-wt-stranded|close'),
            dir='row', flex_justify_content='space-between', flex_align_items='center', flex_gap=gap(16)),
        h2("You're not alone.<br><span style=\"color:#FF6B00\">Let's get you safe first.</span>", WHITE,
           size='clamp(2.2rem, 5vw, 3.6rem)', lh=1.02, ls=0),
        con(
            big('Call a driver now', PHONE_HREF, ORANGE, NAVY, 900, 26, 92, 'phone', 30),
            big('Text my exact location', SMS_HREF, WHITE, NAVY, 800, 22, 80, 'pin', 28,
                attrs='data-wt-sms-location|'),
            big("I'm safe, give me a quote", '#quote', None, WHITE, 700, 19, 72, 'check', 26,
                attrs='data-wt-stranded|close', bw=2, bc='#3A4A66'),
            flex_gap=gap(14)),
        con(span('While you wait: tap each one as you go', WHITE, 18, 800, MONT), *checks,
            background_background='classic', background_color='#13203A', border_radius=box(20),
            padding=box(24), padding_mobile=box(20, 18), flex_gap=gap(6)),
        heading("If anyone is hurt or you're in danger, call 911 first.", 'p', '#FFD7D9',
                **typo(INTER, 600, 16, 1.5), _padding=box(16, 18), _background_background='classic',
                _background_color='#3A0F12', _border_radius=box(14)),
        content_width='boxed', boxed_width=px(712), padding=box(56, 24, 72, 24), padding_mobile=box(32, 20, 48, 20),
        flex_gap=gap(28), flex_gap_mobile=gap(22))
    return full(inner, _element_id='wt-stranded', css_classes='wt-stranded',
                background_background='classic', background_color=INK)

# =============================================================================
# FOOTER (Theme Builder > Footer)
# =============================================================================
def footer():
    def col(title, items, links=True):
        lst = []
        for it in items:
            label, url = it if isinstance(it, tuple) else (it, None)
            d = {'_id': uid(), 'text': label, 'selected_icon': {'value': '', 'library': ''}}
            if url:
                d['link'] = {'url': url, 'is_external': '', 'nofollow': ''}
            lst.append(d)
        return con(
            heading(title, 'span', ORANGE, **typo(MONT, 800, 13, 1.3, 0.12, transform='uppercase')),
            widget('icon-list', icon_list=lst, space_between=px(10), text_color=ON_DARK,
                   text_color_hover=WHITE, text_indent=px(0), **typo(INTER, 400, 14, 1.45, prefix='icon_typography')),
            flex_gap=gap(10), width=px('auto'), css_classes='wt-fcol')
    S = SERVICE_URL
    top = con(
        con(image('WassiTowing_horizontal_reversed.svg', width=px(194), link='/', _element_width='auto'),
            body('Towing, roadside and recovery across every quadrant of Calgary.', ON_DARK, 15, 1.6),
            button('Call [PHONE]', PHONE_HREF, bg=ORANGE, color=NAVY, weight=800, size=15, height=48, padx=20,
                   icon_name='phone', icon_sw=2.4, icon_px=20),
            flex_gap=gap(16), width=px(320), _flex_size='custom', _flex_grow=0, _flex_shrink=1),
        col('Services', [('Flatbed &amp; Wheel-Lift Towing', S['flatbed']), ('Roadside Rescue', S['roadside']),
                         ('Tire Rescue', S['tire']), ('Fuel Drop', S['fuel']), ('Battery Boost', S['battery']),
                         ('Ditch &amp; Snow Recovery', S['winch']), ('Trailer &amp; Equipment Hauling', S['hauling']),
                         ('Motorcycle Transport', S['moto']), ('Prestige &amp; Low-Clearance Towing', S['exotic'])]),
        col('Company', [('Home', '/'), ('About', '/about/'), ('FAQs', '/faqs/'), ('Services', '/services/')]),
        col('Contact', [('Call [PHONE]', PHONE_HREF), ('Text [SMS NUMBER]', SMS_HREF), ('[EMAIL]', 'mailto:[EMAIL]'),
                        'Hours: [24/7, confirm]', 'All of Calgary: NW, NE, SW, SE']),
        dir='row', flex_wrap='wrap', flex_justify_content='space-between', flex_gap=gap(40),
        flex_gap_mobile=gap(32))
    bottom = con(
        text('<p>© 2026 Wassi Towing Ltd. · <a href="/privacy-policy/">Privacy</a> · <a href="/terms/">Terms</a></p>',
             '#9AA6B8', link_color='#9AA6B8', link_hover_color=WHITE, **typo(INTER, 400, 13, 1.5),
             _element_width='auto'),
        span('If anyone is hurt or in danger, call 911 first.', '#9AA6B8', 13),
        dir='row', flex_wrap='wrap', flex_justify_content='space-between', flex_gap=gap(12),
        padding=box(20, 0, 0, 0), border_border='solid', border_width=box(1, 0, 0, 0), border_color='#22324D')
    foot = section(top, bottom, bg=INK, pt=64, pb=28, flex_gap=gap(40), pt_m=48, pb_m=96)
    sticky = html(open(os.path.join(HANDOFF, 'interactions', 'mobile-sticky-bar.html')).read()
                  .replace('href="/#quote"', 'href="/#quote"'))
    return [foot, stranded(), full(sticky)]

# =============================================================================
# HOME PAGE
# =============================================================================
def quote_widget():
    src = open(os.path.join(HANDOFF, 'interactions', 'quote-widget.html')).read()
    pin = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#101D32" '
           'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.5-7-12a7 7 0 0 1 '
           '14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>')
    src = src.replace('data-wtq-geo>Use my location</button>', f'data-wtq-geo>{pin}<span>Use my location</span></button>')
    src = src.replace('btn.textContent="Finding you…";', 'btn.lastChild.textContent="Finding you…";')
    src = src.replace('btn.textContent="Use my location"; go(2);', 'btn.lastChild.textContent="Use my location"; go(2);')
    src = src.replace('btn.textContent="Use my location"; $("#wtq-addr")', 'btn.lastChild.textContent="Use my location"; $("#wtq-addr")')
    src = src.replace('class="wtq-btn wtq-outline" data-wtq-next', 'class="wtq-btn wtq-outline wtq-next" data-wtq-next')
    # match home.html exactly: 56px/16px primary, 48px/Inter next, 17px question
    src = src.replace('</style>', '.wtq{box-sizing:border-box;width:100%}'
        '.wtq-pane[data-wtq-pane="1"] .wtq-primary{min-height:56px;font-size:16px;gap:10px}'
        '.wtq-next{min-height:48px;border-radius:12px;font:700 15px Inter,sans-serif}'
        '.wtq-q{color:#101D32}.wtq-label input{box-sizing:border-box;width:100%}'
        '.wtq-label input:focus{outline:2px solid #FF6B00;outline-offset:1px}'
        '@media(max-width:767px){.wtq{padding:22px;border-radius:20px}}</style>')
    return src

def home():
    S = SERVICE_URL
    # ---------------- 1. HERO ----------------
    trust = con(*[con(icon(n, ORANGE, 16, 2.2), span(t, '#D4DCE7', 14),
                      dir='row', flex_align_items='center', flex_gap=gap(6), width=px('auto'), width_mobile=px('auto'))
                  for n, t in [('tag', 'Upfront pricing'), ('shield', 'Licensed &amp; insured'),
                               ('map', 'Every corner of Calgary covered')]],
                dir='row', flex_wrap='wrap', flex_gap=gap(10, 22))
    hero_left = con(
        pill(icon('map', ORANGE, 16, 2.2),
             heading('Towing &amp; Roadside Assistance in Calgary', 'h1', WHITE, **typo(INTER, 700, 14, 1.3, 0.02)),
             bg=NAVY2),
        heading("Stuck? Breathe.<br><span style=\"color:#FF6B00\">We're already on our way.</span>", 'p', WHITE,
                **typo(MONT, 900, 'clamp(2.6rem, 5.6vw, 4.6rem)', 0.98, -0.015, style='italic')),
        body('Flat deck towing, battery boosts, flat tire changes, fuel delivery and winch-outs across Calgary. '
             'You get an upfront price and a live arrival time before the truck leaves the yard.',
             '#D4DCE7', 19, 1.55, _element_width='initial', _element_custom_width=px(540),
             typography_font_size_mobile=px(17)),
        con(button('Call now', PHONE_HREF, bg=ORANGE, color=NAVY, weight=800, size=18, height=60, padx=28,
                   icon_name='phone', icon_sw=2.4, icon_px=20),
            button("I'm stuck right now", '#', color=WHITE, weight=700, size=17, height=60, padx=22,
                   border_w=1.5, border_c='rgba(255,255,255,0.35)', icon_name='alert', icon_sw=2.2, icon_px=20,
                   attrs='data-wt-stranded|open'),
            dir='row', flex_wrap='wrap', flex_gap=gap(12)),
        trust,
        flex_gap=gap(24), width=px(480), _flex_size='custom', _flex_grow=1, _flex_shrink=1)
    hero = section(
        image('hero-road.svg', width=px(640), opacity=px(0.16), _position='absolute',
              _offset_orientation_h='end', _offset_x_end=px(-40), _offset_orientation_v='end',
              _offset_y_end=px(-30), _z_index=0, _element_width='auto', css_classes='',
              _css_classes='wt-deco'),
        hero_left,
        html(quote_widget(), _element_id='', _css_classes='wt-quote-col',
             **flex_item(380, 1, 1)),
        bg=NAVY, pt=72, pb=80, pt_m=40, pb_m=56, dir='row', flex_wrap='wrap', flex_align_items='center',
        flex_gap=gap(48), flex_gap_mobile=gap(36), overflow='hidden')

    # ---------------- 2. DISPATCH BOARD ----------------
    rows = []
    for ic, problem, svc, key in [
            ('battery', "My car won't start", 'Battery Boost', 'battery'),
            ('tire', "I've got a flat", 'Tire Rescue', 'tire'),
            ('fuel', 'I ran out of gas', 'Fuel Drop', 'fuel'),
            ('key', "I'm locked out", 'Roadside Rescue', 'roadside'),
            ('winch', "I'm stuck in snow, mud or a ditch", 'Ditch &amp; Snow Recovery', 'winch'),
            ('truck', 'My car needs to go to a shop', 'Flatbed &amp; Wheel-Lift Towing', 'flatbed'),
            ('bike', 'I need to move a bike', 'Motorcycle Transport', 'moto'),
            ('prestige', 'My car is low, rare or valuable', 'Prestige &amp; Low-Clearance Towing', 'exotic'),
            ('trailer', 'I need to move a trailer or equipment', 'Trailer &amp; Equipment Hauling', 'hauling')]:
        rows.append(con(
            con(icon(ic, ORANGE, 24, 2), span(problem, WHITE, 18, 700, lh=1.35, typography_font_size_mobile=px(17)),
                dir='row', flex_align_items='center', flex_gap=gap(14), width=px(280),
                _flex_size='custom', _flex_grow=2, _flex_shrink=1),
            span(svc, ORANGE, 16, 800, MONT, 1.3, **flex_item(240, 2, 1)),
            span('[X] min', '#9FB0C8', 14, 600, **flex_item(120, 1, 1)),
            icon('arrow', NAVY, 18, 2.6, view='stacked', shape='circle', primary_color=ORANGE,
                 secondary_color=NAVY, icon_padding=px(11), _flex_size='none'),
            dir='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(14, 20),
            padding=box(18, 6), border_border='dashed', border_width=box(0, 0, 1, 0), border_color='#2A3A57',
            html_tag='a', link={'url': S[key], 'is_external': '', 'nofollow': ''},
            background_hover_background='classic', background_hover_color='rgba(255,255,255,0.03)',
            css_classes='wt-drow'))
    th = lambda t, b, g: span(t, '#7F92AE', 12, 700, lh=1.4, typography_letter_spacing=px(0.12, 'em'),
                              **flex_item(b, g, 1))
    board = con(
        con(con(eyebrow('WHAT HAPPENED?', ORANGE),
                h2("Tell us what's wrong. We'll send the right truck.", WHITE),
                flex_gap=gap(10), width=px(640), _flex_size='custom', _flex_grow=0, _flex_shrink=1),
            pill(con(width=px(8), width_mobile=px(8), min_height=px(8), border_radius=box(99),
                     background_background='classic', background_color='#3DDC84'),
                 span('Dispatch board', '#CFE0F5', 13, 600), bg='#13203A', _flex_align_self='flex-end'),
            dir='row', flex_wrap='wrap', flex_justify_content='space-between', flex_align_items='flex-end',
            flex_gap=gap(16), padding=box(0, 0, 22, 0)),
        con(th('YOUR PROBLEM', 280, 2), th('WE SEND', 240, 2), th('TYPICAL ARRIVAL', 120, 1),
            con(width=px(40), _flex_size='none'),
            dir='row', flex_wrap='wrap', flex_gap=gap(14, 20), padding=box(10, 6),
            border_border='solid', border_width=box(2, 0, 1, 0), border_color='#2A3A57',
            css_classes='wt-thead', hide_mobile='hidden-mobile'),
        *rows,
        background_background='classic', background_color=INK, border_radius=box(28),
        padding=box(36, 32, 20, 32), padding_mobile=box(28, 18, 12, 18),
        **shadow(0, 30, 60, -30, 'rgba(11,20,36,0.6)'))
    dispatch = section(board, bg=BG, pt_m=56, pb_m=56)

    # ---------------- 3. INTRO / SEO COPY ----------------
    links = [('flatbed towing', 'flatbed'), ('roadside assistance and car lockouts', 'roadside'),
             ('flat tire changes', 'tire'), ('fuel delivery', 'fuel'), ('battery boosts', 'battery'),
             ('winch-out recovery', 'winch'), ('local hauling', 'hauling'), ('motorcycle towing', 'moto'),
             ('exotic car towing', 'exotic')]
    L = {k: f'<a href="{S[v]}">{k}</a>' for k, v in links}
    p3 = (f'<p>Our services include {L["flatbed towing"]}, accident towing, {L["roadside assistance and car lockouts"]}, '
          f'{L["flat tire changes"]}, {L["fuel delivery"]}, {L["battery boosts"]}, {L["winch-out recovery"]}, '
          f'{L["local hauling"]}, {L["motorcycle towing"]} and {L["exotic car towing"]}.</p>')
    badge = lambda t: heading(t, 'span', WHITE, **typo(MONT, 800, 14, 1.3), _padding=box(6, 12),
                              _background_background='classic', _background_color=NAVY, _border_radius=box(8),
                              _element_width='auto')
    intro = section(
        heading('CALGARY', 'div', '#F1F3F6', **typo(MONT, 900, 220, 1, -0.03, style='italic', size_m=150),
                _position='absolute', _offset_orientation_h='start', _offset_x=px(-20),
                _offset_orientation_v='end', _offset_y_end=px(-40), _z_index=0, _element_width='auto',
                _css_classes='wt-nowrap wt-deco'),
        con(eyebrow('TOWING IN CALGARY'),
            heading('Every quadrant.<br>One call.', 'p', NAVY,
                    **typo(MONT, 900, 'clamp(2rem, 3.6vw, 3rem)', 1.05, style='italic'),
                    _padding=box(0, 0, 0, 22), _border_border='solid', _border_width=box(0, 0, 0, 6),
                    _border_color=ORANGE),
            con(badge('NW'), badge('NE'), badge('SW'), badge('SE'), dir='row', flex_gap=gap(8)),
            flex_gap=gap(22), width=px(340), _flex_size='custom', _flex_grow=1, _flex_shrink=1),
        con(h2('A new kind of tow truck company in Calgary'),
            body('Wassi Towing Ltd. is a Calgary towing and roadside assistance company that covers every quadrant '
                 'of the city: NW, NE, SW, SE, Downtown and the Beltline. Whether you need a tow truck after a '
                 'breakdown on Deerfoot Trail, a battery boost on a minus-30 morning or a winch-out from a snowbank '
                 'on Stoney Trail, one call gets the right truck moving.', typography_font_size_mobile=px(17)),
            body("We run flat deck (flatbed) tow trucks and wheel-lift units, so your car, SUV, EV or motorcycle is "
                 "moved the safe way for its drivetrain and clearance. Every job starts with an upfront price you "
                 "approve, and you get a text with your driver's name and a live tracking link.",
                 typography_font_size_mobile=px(17)),
            text(p3, MUTED, link_color=ORANGE_TXT, link_hover_color=NAVY, _css_classes='wt-links',
                 **typo(INTER, 400, 18, 1.7, size_m=17)),
            flex_gap=gap(18), width=px(520), _flex_size='custom', _flex_grow=2, _flex_shrink=1),
        bg=WHITE, pt=88, pb=120, pt_m=56, pb_m=96, dir='row', flex_wrap='wrap', flex_gap=gap(56),
        flex_gap_mobile=gap(32), overflow='hidden')

    # ---------------- 4. HOW IT WORKS ----------------
    steps = []
    for n, ic, t, d in [('01', 'pin', 'Tell us where you are', 'Call, text your location or use the quote tool.'),
                        ('02', 'tag', 'Get your price and arrival time', 'You approve it before we dispatch. No surprises.'),
                        ('03', 'map', 'Track your driver', "A live link shows the truck on the map and your driver's name."),
                        ('04', 'check', 'Back on the road', 'Fixed on the spot, or delivered wherever you choose.')]:
        steps.append(con(
            con(con(span(n, ORANGE, 34, 900, MONT, 1, typography_font_style='italic'),
                    icon(ic, NAVY, 28, 2.2),
                    dir='row', flex_justify_content='space-between', flex_align_items='center'),
                heading(t, 'h3', NAVY, **typo(MONT, 800, 19, 1.25)),
                body(d, MUTED, 15, 1.55),
                background_background='classic', background_color=WHITE, border_radius=box(18),
                border_border='solid', border_width=box(8, 0, 0, 0), border_color=ORANGE,
                padding=box(22), flex_gap=gap(10), **shadow(0, 20, 40, -24, 'rgba(0,0,0,0.6)')),
            con(width=px(8), width_mobile=px(8), min_height=px(56), css_classes='wt-pole'),
            flex_align_items='center'))
    grid = con(*steps, container_type='grid',
               grid_columns_grid={'unit': 'custom', 'size': 'repeat(auto-fit, minmax(230px, 1fr))', 'sizes': []},
               grid_columns_grid_tablet={'unit': 'custom', 'size': 'repeat(auto-fit, minmax(230px, 1fr))', 'sizes': []},
               grid_columns_grid_mobile={'unit': 'fr', 'size': 1, 'sizes': []},
               grid_rows_grid={'unit': 'custom', 'size': 'auto', 'sizes': []},
               grid_rows_grid_tablet={'unit': 'custom', 'size': 'auto', 'sizes': []},
               grid_rows_grid_mobile={'unit': 'custom', 'size': 'auto', 'sizes': []},
               grid_gaps=gap(24), grid_align_items='end')
    how = full(
        con(con(eyebrow('HOW IT WORKS', ORANGE),
                h2('From “uh-oh” to “all good” in four steps', WHITE),
                flex_gap=gap(12), width=px(720), _flex_size='custom', _flex_grow=0, _flex_shrink=1),
            grid,
            content_width='boxed', boxed_width=px(1152), padding=box(88, 24, 0, 24),
            padding_mobile=box(56, 20, 0, 20), flex_gap=gap(40)),
        con(con(width=px(100, '%'), width_mobile=px(100, '%'), min_height=px(8), css_classes='wt-road-dash',
                position='absolute', _offset_orientation_h='start', _offset_x=px(0),
                _offset_orientation_v='start', _offset_y=px(56)),
            con(icon('truck', NAVY, 30, 2.4),
                width=px(86), width_mobile=px(86), min_height=px(44), border_radius=box(10),
                background_background='classic', background_color=ORANGE, flex_justify_content='center',
                flex_align_items='center', position='absolute', _offset_orientation_h='start',
                _offset_x=px(6, '%'), _offset_orientation_v='start', _offset_y=px(18), css_classes='wt-truck'),
            min_height=px(120), background_background='classic', background_color='#1B2433',
            border_border='solid', border_width=box(4, 0, 0, 0), border_color='#2C3A52'),
        background_background='classic', background_color=NAVY)

    # ---------------- 5. WHY WASSI BENTO ----------------
    tile = dict(border_radius=box(24), padding=box(30), padding_mobile=box(24), flex_gap=gap(12))
    bento = con(
        con(con(icon('tag', NAVY, 40, 2.2),
                eyebrow('UPFRONT PRICES', NAVY),
                heading('The price we quote is the price you pay', 'h3', NAVY,
                        **typo(MONT, 900, 'clamp(1.8rem, 3.2vw, 2.6rem)', 1.05, style='italic')),
                body('Your quote includes the call-out, hook-up and the distance we discussed. If anything changes on '
                     'site, the driver tells you the new price before doing the work.', NAVY, 17, 1.6,
                     _element_width='initial', _element_custom_width=px(560)),
                flex_gap=gap(12)),
            button('Get my quote', '#quote', bg=NAVY, color=WHITE, weight=800, size=16, height=52, padx=22,
                   icon_name='arrow', icon_sw=2.6, icon_px=18, icon_end=True),
            width=px(480), _flex_size='custom', _flex_grow=2, _flex_shrink=1, min_height=px(340),
            min_height_mobile=px(0), flex_justify_content='space-between',
            background_background='classic', background_color=ORANGE, **tile),
        con(con(eyebrow('LIVE ARRIVAL TRACKING', ORANGE),
                heading("Watch your driver, don't wonder", 'h3', WHITE, **typo(MONT, 800, 22, 1.25)),
                flex_gap=gap(12)),
            con(con(span('Your driver', WHITE, 14, 600), span('[X] min away', ORANGE, 14, 600),
                    dir='row', flex_justify_content='space-between'),
                con(con(width=px(64, '%'), width_mobile=px(64, '%'), min_height=px(8), border_radius=box(99),
                        background_background='classic', background_color=ORANGE),
                    min_height=px(8), border_radius=box(99), background_background='classic',
                    background_color='#2A3A57'),
                con(icon('truck', '#9FB0C8', 16, 2), span('Flatbed · Plate [PLATE]', '#9FB0C8', 13),
                    dir='row', flex_align_items='center', flex_gap=gap(8)),
                background_background='classic', background_color='#13203A', border_radius=box(16),
                padding=box(16), flex_gap=gap(10)),
            width=px(280), _flex_size='custom', _flex_grow=1, _flex_shrink=1, min_height=px(340),
            min_height_mobile=px(0), flex_justify_content='space-between',
            background_background='classic', background_color=NAVY, **tile),
        con(icon('shield', ORANGE_TXT, 36, 2),
            heading('Damage-free gear', 'h3', NAVY, **typo(MONT, 800, 21, 1.25)),
            body('Flatbeds, soft straps and wheel-lifts matched to your vehicle. Photos at every pickup.', MUTED, 16, 1.55),
            width=px(280), _flex_size='custom', _flex_grow=1, _flex_shrink=1,
            background_background='classic', background_color=BG, **tile),
        con(con(icon('user', ORANGE_TXT, 34, 2),
                heading('Real people answer', 'h3', NAVY, **typo(MONT, 800, 21, 1.25)),
                body('A dispatcher, not a phone menu, [24/7, confirm].', MUTED, 16, 1.55),
                flex_gap=gap(8), width=px(420), _flex_size='custom', _flex_grow=0, _flex_shrink=1),
            heading('[PHONE]', 'span', NAVY, link=PHONE_HREF,
                    **typo(MONT, 900, 30, 1.2, style='italic')),
            dir='row', flex_wrap='wrap', flex_justify_content='space-between', flex_align_items='center',
            width=px(480), _flex_size='custom', _flex_grow=2, _flex_shrink=1,
            background_background='classic', background_color=WHITE,
            border_border='solid', border_width=box(2), border_color=NAVY, **tile),
        dir='row', flex_wrap='wrap', flex_gap=gap(16))
    why = section(
        con(eyebrow('WHY WASSI'), h2('Built for Calgary roads and Calgary winters'),
            flex_gap=gap(12), width=px(720), _flex_size='custom', _flex_grow=0, _flex_shrink=1),
        bento, bg=WHITE, pt_m=56, pb_m=56, flex_gap=gap(32))

    # ---------------- 6. SERVICE AREA ----------------
    chip = lambda t: con(icon('check', NAVY, 16, 2.4), span(t, NAVY, 15, 600),
                         dir='row', flex_align_items='center', flex_gap=gap(8), min_height=px(42),
                         padding=box(0, 16), border_radius=box(999), background_background='classic',
                         background_color=WHITE, border_border='solid', border_width=box(1), border_color=LINE,
                         width=px('auto'), width_mobile=px('auto'))
    area = section(
        con(eyebrow('SERVICE AREA'), h2('One city. Every quadrant.'),
            body("From downtown parkades and Beltline side streets to Deerfoot, Stoney Trail and Crowchild shoulders, "
                 "and the newest communities at the city's edge. If you're inside Calgary, we come to you.",
                 MUTED, 18, 1.6, typography_font_size_mobile=px(17)),
            con(*[chip(t) for t in ['NW Calgary', 'NE Calgary', 'SW Calgary', 'SE Calgary', 'Downtown &amp; Beltline']],
                dir='row', flex_wrap='wrap', flex_gap=gap(10)),
            flex_gap=gap(18), width=px(420), _flex_size='custom', _flex_grow=1, _flex_shrink=1),
        con(html(open(os.path.join(HERE, 'calgary-map.svg')).read().replace('<svg ', '<svg style="max-width:520px;display:block;margin:0 auto" ', 1)),
            width=px(420), _flex_size='custom', _flex_grow=1, _flex_shrink=1, flex_justify_content='center'),
        bg=BG, pt_m=56, pb_m=56, dir='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(48),
        flex_gap_mobile=gap(32))

    # ---------------- 7. LAUNCH PLEDGE ----------------
    pledge_rows = [con(
        con(icon('check', ORANGE_TXT, 18, 3), width=px(28), width_mobile=px(28), min_height=px(28),
            border_border='solid', border_width=box(2), border_color=NAVY, border_radius=box(6),
            flex_justify_content='center', flex_align_items='center', _flex_size='none'),
        span(t, NAVY, 17, 400, lh=1.5, typography_font_size_mobile=px(16)),
        dir='row', flex_align_items='flex-start', flex_gap=gap(14), padding=box(14, 0),
        border_border='solid', border_width=box(0, 0, 1, 0), border_color=LINE)
        for t in ['The price you approve is the price you pay',
                  "A live tracking link and your driver's name before arrival",
                  'Photos of your vehicle at pickup',
                  'Running late on our estimate? We tell you before you ask']]
    card = con(
        con(heading('NEW IN<br>CALGARY<br>2026', 'div', ORANGE_TXT, align='center',
                    **typo(MONT, 900, 13, 1.2, 0.06)),
            width=px(118), width_mobile=px(96), min_height=px(118), min_height_mobile=px(96),
            border_radius=box(999), border_border='solid', border_width=box(3), border_color=ORANGE,
            background_background='classic', background_color=WHITE, flex_justify_content='center',
            flex_align_items='center', position='absolute', _offset_orientation_h='end', _offset_x_end=px(-18),
            _offset_x_end_mobile=px(-6), _offset_orientation_v='start', _offset_y=px(-26), z_index=2,
            _transform_rotate_popover='transform', _transform_rotateZ_effect=px(12, 'deg'),
            css_classes='wt-stamp'),
        eyebrow('OUR LAUNCH PLEDGE', ls=0.16),
        h2('New on Calgary roads. Built the right way from day one.', size='clamp(1.8rem, 3.4vw, 2.5rem)',
           lh=1.08, ls=0, _margin=box(10, 0, 8, 0), _element_width='initial',
           _element_custom_width=px('calc(100% - 90px)'), _element_width_mobile='initial',
           _element_custom_width_mobile=px('calc(100% - 70px)')),
        body("We haven't earned your review yet. Here's what we promise every customer while we do.",
             MUTED, 17, 1.6, _margin=box(0, 0, 8, 0), typography_font_size_mobile=px(16)),
        con(*pledge_rows),
        con(con(heading('[Founder name]', 'span', NAVY, **typo(MONT, 700, 26, 1.3, style='italic'),
                        _padding=box(0, 30, 4, 0), _border_border='solid', _border_width=box(0, 0, 2, 0),
                        _border_color=NAVY, _element_width='auto'),
                span('Founder, Wassi Towing Ltd.', MUTED, 13),
                flex_gap=gap(4), width=px('auto')),
            image('symbol-navy.svg', width=px(111), _element_width='auto', alt=''),
            dir='row', flex_wrap='wrap', flex_justify_content='space-between', flex_align_items='flex-end',
            flex_gap=gap(16), margin=box(28, 0, 0, 0)),
        width=px(760), background_background='classic', background_color=WHITE, border_radius=box(10),
        padding=box(48, 44, 40, 44), padding_mobile=box(40, 22, 32, 22),
        _transform_rotate_popover='transform', _transform_rotateZ_effect=px(-1, 'deg'),
        **shadow(0, 30, 60, -28, 'rgba(16,29,50,0.45)'))
    pledge = section(card, bg='#FFF3E8', pt=96, pb=96, pt_m=64, pb_m=64, dir='row',
                     flex_justify_content='center', css_classes='wt-dots')

    # ---------------- 8. CALL BAND (global template) ----------------
    band = full(widget('template', template_id='{{CALLBAND_ID}}'))
    return [hero, dispatch, intro, how, why, area, pledge, band]


if __name__ == '__main__':
    save('out/header.json', header(), 'Wassi Header', 'header')
    save('out/callband.json', callband(), 'Wassi Call Band', 'container')
    foot = footer()
    save('out/footer.json', foot, 'Wassi Footer', 'footer')
    save('out/home.json', home(), 'Home', 'page',
         {'template': 'elementor_header_footer', 'hide_title': 'yes'})
    print('icons:', len(os.listdir(os.path.join(HERE, 'icons'))))
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))
