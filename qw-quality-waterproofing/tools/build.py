"""Builds every page + header/footer for the Quality Waterproofing site with native Elementor widgets.
Usage:  python3 build.py all            build + push everything
        python3 build.py home about ...  only the named parts (header, footer, home, about, services, projects, contact, <service slug>, <location slug>)
        python3 build.py --dry home      build JSON locally only (out/<name>.json)
WARNING: pushing overwrites the page's Elementor data. If the user has edited a page in the Elementor editor, fetch and patch instead."""
import sys, json, os
from el import *
from content import SERVICES, LOCATIONS

MENU_SLUG = 'qw-main-menu'
SVC_ORDER = ['exterior-waterproofing', 'interior-waterproofing', 'sump-pump-installation', 'foundation-crack-repair', 'interlocking']
LOC_ORDER = ['basement-waterproofing-toronto', 'basement-waterproofing-mississauga', 'basement-waterproofing-brampton', 'basement-waterproofing-north-bay']
FB = 'https://www.facebook.com/share/1E1EebBzXR/?mibextid=wwXIfr'
IG = 'https://www.instagram.com/qualitywaterproofinginc'

# ================= shared sections =================
def hero(eyebrow, h1, lead, bg=None, video=False, form=True, trust=None, minh=640):
    trust = trust or ['10+ Years Experience', 'Free On-Site Estimates', 'Residential & Commercial']
    left = C([
        EYE(eyebrow, color='qwgoldlt'),
        H(h1, 'h1', 'qwh1', 'qwwhite'),
        T(lead, 'qwmuted', 'qwlead'),
        CTA_BTNS(dark=True),
        ILIST(trust, color='qwwhite', inline=True, typo='qwsmall', size=15, gapv=22, _margin=dims(10, 0, 0, 0)),
    ], 'Hero Copy', flex_gap=gap(20), flex_justify_content='center')
    kids = [left]
    if form:
        kids.append(CARD([
            H('Get Your <span class="qw-hl">Free Estimate</span>', 'h2', 'qwh3', 'primary'),
            T('Tell us about the problem – we’ll call you back to book an inspection.', 'text', 'qwsmall'),
            FORM('Hero Estimate', compact=True),
        ], title='Hero Form Card', pad=32, _element_id='estimate', border_border='none',
           box_shadow_box_shadow=shadow(30, 60, 'rgba(0,0,0,0.35)'), border_radius=dims(6), flex_gap=gap(10)))
    s = dict(min_height=px(minh), min_height_mobile=px(0), flex_align_items='center', background_overlay_background='gradient',
             background_overlay_color='rgba(10,14,23,0.86)', background_overlay_color_b='rgba(10,14,23,0.40)',
             background_overlay_gradient_angle=px(90, 'deg'), background_overlay_gradient_angle_mobile=px(180, 'deg'), background_overlay_opacity=px(1))
    if video:
        s.update(background_background='video', background_video_link=MEDIA['hero_video']['url'], background_play_on_mobile='yes',
                 background_video_fallback=img(bg), background_privacy_mode='')
    else:
        s.update(background_background='classic', background_image=img(bg), background_position='center center', background_size='cover')
    inner = C(kids, 'Hero Grid', grid=2 if form else 1, grid_t=1, grid_gaps=gap(56, 36), **({'grid_columns_grid': cols('1.3fr 1fr')} if form else {}), grid_align_items='center')
    return SECTION([inner], 'Hero', bg='none', pad=(120, 90, 64), css_classes='qw-dark qw-hero', **s)

def trust_strip():
    items = [('fas fa-search-location', 'Free Inspection', 'We find the real source of the water before we quote.'),
             ('fas fa-file-signature', 'Clear Written Quotes', 'Know exactly what is included – no surprises.'),
             ('fas fa-hard-hat', '10+ Years Experience', 'Residential & commercial construction know-how.'),
             ('fas fa-broom', 'Clean, Respectful Crews', 'We protect your property and clean up every day.')]
    return SECTION([C([IBOX(i, t, d, pos='left', view='default', icon_size=px(30), tag='h3', position_mobile='top') for i, t, d in items], 'Trust Grid', grid=4, grid_t=2, grid_m=2, grid_gaps=gap(30, 26))],
                   'Trust Strip', bg='white', pad=(54, 44, 40), border_border='solid', border_width=dims(0, 0, 1, 0), border_color='#E3E6EC')

def inspection_card():
    return CARD([
            W('icon', 'Icon', selected_icon=ico('fas fa-question'), view='stacked', shape='square', size=px(22), icon_padding=px(16), align='left',
              g={'primary_color': col('secondary'), 'secondary_color': col('primary')}),
            H('Not Sure What You Need?', 'h3', 'qwh3', 'primary'),
            T('Every home is different. Book a free inspection and we’ll find the source of the water and recommend the right fix – honestly.', 'text', 'qwsmall'),
            BTN('Book Free Inspection', '#estimate', 'gold', 'fas fa-arrow-right', size='sm'),
        ], title='Inspection Card', border_width=dims(4, 1, 1, 1), border_color='#C9A24B', flex_justify_content='flex-end', min_height=px(440), min_height_mobile=px(0))

def services_grid(dark=False, intro=True, exclude=None, bg='cream'):
    cards = [SERVICE_CARD(SERVICES[s]['card'], SERVICES[s]['name'], SERVICES[s]['card_text'], page_url(s)) for s in SVC_ORDER if s != exclude]
    if not exclude:
        cards.append(inspection_card())
    head = HEAD('What We Do', 'Waterproofing & Exterior <span class="qw-hl">Services</span>',
                'From the footing to the front walk – we protect your home from water with proven methods and careful workmanship.' if intro else None,
                align='center', dark=dark)
    return SECTION(head + [C(cards, 'Services Grid', grid=3, grid_t=2, grid_gaps=gap(24), _margin=dims(26, 0, 0, 0))],
                   'Services', bg='ink' if dark else bg, flex_gap=gap(20))

def process(steps=None, title='How We Waterproof <span class="qw-hl">Your Basement</span>', eyebrow='Our Process'):
    steps = steps or [('Free Inspection', 'We inspect inside and out to find exactly where and why water is getting in.'),
                      ('Honest Recommendation', 'You get a clear, written quote for the right fix – not the most expensive one.'),
                      ('Expert Installation', 'Our experienced crew completes the work carefully, using proven materials.'),
                      ('Clean-Up & Walkthrough', 'We clean the site, walk you through the finished work and answer every question.')]
    return SECTION(HEAD(eyebrow, title, 'A straightforward, four-step process from the first call to a dry basement.', align='center')
                   + [C([STEPS(steps, dark=False)], 'Steps Wrap', _margin=dims(26, 0, 0, 0))], 'Process', bg='light', flex_gap=gap(20))

def why_us(img1='ext_worker_dig', img2='int_dmx_wall', bg='white'):
    left = C([
        C([IMG(img1, h=480, hm=300), IMG(img2, h=480, hm=300)], 'Image Pair', grid=2, grid_t=2, grid_m=2, grid_gaps=gap(16)),
        C([CARD([H('10+', 'div', 'qwstat', 'secondary'), T('Years of residential & commercial construction experience', 'text', 'qwsmall')], pad=24, title='Stat 1'),
           CARD([H('4', 'div', 'qwstat', 'secondary'), T('Service regions: Toronto & GTA, Mississauga, Brampton, North Bay', 'text', 'qwsmall')], pad=24, title='Stat 2')],
          'Stats', grid=2, grid_t=2, grid_m=2, grid_gaps=gap(16)),
    ], 'Why Media', flex_gap=gap(16))
    right = C(HEAD('Why Quality Waterproofing', 'Done Right the First Time. <span class="qw-hl">Built to Stay Dry.</span>') + [
        T('A wet basement is stressful. Our job is to make it simple: find the real cause, explain your options in plain language, and fix it properly with materials and methods that last.'),
        C([IBOX('fas fa-user-check', 'Experienced Crews', 'Waterproofing, interlock, walkouts and underpinning experience – one team that understands your whole foundation.', pos='left', view='default', icon_size=px(28)),
           IBOX('fas fa-layer-group', 'Proven Materials', 'Drainage membranes, sealants and weeping tile chosen for each wall – not a one-size-fits-all product.', pos='left', view='default', icon_size=px(28)),
           IBOX('fas fa-comments', 'Straight Answers', 'Clear written quotes and honest advice, even if the answer is a smaller job.', pos='left', view='default', icon_size=px(28))],
          'Why Points', flex_gap=gap(22), _margin=dims(8, 0, 8, 0)),
        CTA_BTNS(dark=False),
    ], 'Why Copy', flex_gap=gap(16), flex_justify_content='center')
    return SECTION([C([left, right], 'Why Grid', grid=2, grid_t=1, grid_gaps=gap(64, 44), grid_align_items='center')], 'Why Us', bg=bg)

def areas_section(city_focus=None, dark=False):
    cards = []
    for slug in LOC_ORDER:
        L = LOCATIONS[slug]
        cards.append(IBOX('fas fa-map-marker-alt', L['label'], ', '.join(L['hoods'][:5]) + ' and nearby.',
                          view='stacked', link_url=page_url(slug), tag='h3',
                          **({'_border_border': 'solid', '_border_width': dims(1), '_border_color': '#E3E6EC', '_padding': dims(28), '_border_radius': dims(6), '_background_background': 'classic', '_background_color': '#FFFFFF',
                             '_box_shadow_box_shadow_type': 'yes', '_box_shadow_box_shadow': shadow(18, 40, 'rgba(14,20,32,0.07)')})))
    head = HEAD('Service Areas', 'Proudly Serving the GTA <span class="qw-hl">& North Bay</span>',
                'Basement waterproofing, sump pumps, crack repair and interlocking for homeowners across Toronto, Mississauga, Brampton, North Bay and surrounding communities.', align='center')
    return SECTION(head + [C(cards, 'Areas Grid', grid=4, grid_t=2, grid_gaps=gap(20), _margin=dims(24, 0, 0, 0))], 'Service Areas', bg='cream', flex_gap=gap(20))

def faq_section(items, title='Frequently Asked <span class="qw-hl">Questions</span>', side_img='ext_parging'):
    left = C(HEAD('FAQ', title) + [
        T('Have a question that isn’t answered here? Call us at <a href="' + TEL + '">' + PHONE + '</a> or send us a message – we’re happy to help.'),
        IMG(side_img, h=300, hm=220),
    ], 'FAQ Intro', flex_gap=gap(16))
    return SECTION([C([left, C([FAQ(items)], 'FAQ List')], 'FAQ Grid', grid=2, grid_t=1, grid_gaps=gap(60, 36),
                      grid_columns_grid=cols('1fr 1.35fr'))], 'FAQ', bg='light')

def cta_band(title='Ready for a <span class="qw-hl-ink">Dry, Healthy</span> Basement?', text='Book your free on-site inspection today. We’ll find the source of the water and give you a clear written quote – with no pressure.'):
    copy = C([H(title, 'h2', 'qwh2', 'primary'), T(text, 'primary', 'qwlead')], 'CTA Copy', flex_gap=gap(12))
    btns = C([BTN('Get a Free Estimate', page_url('contact'), 'ink', 'fas fa-clipboard-check'),
              BTN('Call ' + PHONE, TEL, 'outline', 'fas fa-phone-alt')], 'CTA Buttons', row=True, flex_wrap='wrap', flex_gap=gap(14),
             flex_direction_mobile='row', flex_justify_content='flex-end', flex_justify_content_tablet='flex-start')
    return SECTION([C([copy, btns], 'CTA Grid', grid=2, grid_t=1, grid_gaps=gap(30), grid_align_items='center')], 'CTA Band', bg='none', pad=(76, 64, 54),
                   background_background='gradient', background_color='#E8CC84', background_color_b='#C9A24B', background_gradient_angle=px(120, 'deg'))

def split(title, paras, imgk, img2=None, eyebrow=None, rev=False, extra=None, bg='white'):
    copy = C(([EYE(eyebrow)] if eyebrow else []) + [H(title, 'h2', 'qwh2'), LINE()] + [T(p) for p in paras] + (extra or []), 'Split Copy', flex_gap=gap(16), flex_justify_content='center')
    if img2:
        media = C([IMG(imgk, h=520, hm=320), IMG(img2, h=520, hm=320, _margin=dims(60, 0, 0, 0), _margin_mobile=dims(30, 0, 0, 0))], 'Split Media', grid=2, grid_t=2, grid_m=2, grid_gaps=gap(16))
    else:
        media = C([IMG(imgk, h=540, hm=320)], 'Split Media')
    kids = [media, copy] if not rev else [copy, media]
    return SECTION([C(kids, 'Split Grid', grid=2, grid_t=1, grid_gaps=gap(64, 40), grid_align_items='center')], 'Split: ' + title.split('<')[0][:30], bg=bg)

def gallery(keys, title='Recent <span class="qw-hl">Projects</span>', eyebrow='Our Work', intro=None, cols=4, bg='white'):
    g = W('gallery', 'Gallery', gallery_type='single', gallery=[img(k) for k in keys], gallery_layout='grid', columns=cols, columns_tablet=3, columns_mobile=2,
          gap=px(12), gap_tablet=px(10), gap_mobile=px(8), aspect_ratio='1:1', thumbnail_image_size='medium_large', link_to='file', open_lightbox='yes',
          image_hover_animation='zoom-in', overlay_background='yes', background_overlay_color='rgba(14,20,32,0.45)', image_border_radius=dims(4))
    return SECTION(HEAD(eyebrow, title, intro, align='center') + [C([g], 'Gallery Wrap', _margin=dims(20, 0, 0, 0))], 'Gallery', bg=bg)

def form_section(title='Book Your <span class="qw-hl">Free Estimate</span>', text=None, eid='estimate-form'):
    text = text or 'Tell us a little about your basement or project and we’ll call you back to book a free on-site inspection anywhere in Toronto, Mississauga, Brampton or North Bay.'
    left = C(HEAD('Contact Us', title) + [T(text),
        ILIST([(PHONE, 'fas fa-phone-alt', TEL), (EMAIL, 'fas fa-envelope', 'mailto:' + EMAIL), ('Toronto · Mississauga · Brampton · North Bay', 'fas fa-map-marker-alt')],
              color='primary', typo='qwlead', size=18, gapv=16)], 'Form Copy', flex_gap=gap(18), flex_justify_content='center')
    right = CARD([FORM('Estimate Request')], title='Form Card', pad=36, _element_id=eid)
    return SECTION([C([left, right], 'Form Grid', grid=2, grid_t=1, grid_gaps=gap(60, 36), grid_align_items='center')], 'Estimate Form', bg='cream')

# ================= header / footer =================
def header():
    seed('header')
    top = C([
        ILIST([('Serving Toronto, Mississauga, Brampton & North Bay', 'fas fa-map-marker-alt')], color='qwmuted', icon_color='secondary', inline=True, typo='qwsmall', size=13),
        ILIST([(EMAIL, 'fas fa-envelope', 'mailto:' + EMAIL), (PHONE, 'fas fa-phone-alt', TEL)], color='qwmuted', icon_color='secondary', inline=True, typo='qwsmall', size=13, gapv=26,
              g={'text_color_hover': col('secondary')}),
    ], 'Top Bar', inner=False, content_width='boxed', row=True, flex_justify_content='space-between', flex_align_items='center',
        padding=dims(9, 20), background_background='classic', hide_mobile='hidden-mobile', border_border='solid', border_width=dims(0, 0, 1, 0), border_color='#2A3448',
        g={'background_color': col('qwink2')})
    nav = W('nav-menu', 'Main Menu', menu=MENU_SLUG, layout='horizontal', align_items='center', pointer='underline', animation_line='grow', submenu_icon=ico('fas fa-chevron-down'),
            dropdown='tablet', full_width='stretch', toggle='burger', text_align='aside', menu_space_between=px(6), padding_horizontal_menu_item=px(14), padding_vertical_menu_item=px(30),
            pointer_width=px(2), dropdown_border_radius=dims(4), dropdown_box_shadow_box_shadow_type='yes', dropdown_box_shadow_box_shadow=shadow(14, 34, 'rgba(14,20,32,0.14)'), dropdown_divider_border='solid', dropdown_divider_color='#EEF2F7', dropdown_divider_width=px(1), padding_horizontal_dropdown_item=px(20), padding_vertical_dropdown_item=px(13), dropdown_top_distance=px(0),
            toggle_size=px(26), toggle_border_width=px(0), toggle_border_radius=px(4), padding_vertical_dropdown_item_tablet=px(15),
            g={'menu_typography_typography': typ('qwnav'), 'dropdown_typography_typography': typ('qwnav'),
               'color_menu_item': col('primary'), 'color_menu_item_hover': col('qwgolddk'), 'pointer_color_menu_item_hover': col('secondary'),
               'color_menu_item_active': col('qwgolddk'), 'pointer_color_menu_item_active': col('secondary'),
               'color_dropdown_item': col('primary'), 'background_color_dropdown_item': col('qwwhite'), 'color_dropdown_item_hover': col('primary'),
               'background_color_dropdown_item_hover': col('secondary'), 'color_dropdown_item_active': col('primary'), 'background_color_dropdown_item_active': col('secondary'),
               'toggle_color': col('primary'), 'toggle_background_color': col('qwcream')})
    main = C([
        W('image', 'Logo', image=img('logo_light'), image_size='full', width=px(132), width_tablet=px(120), width_mobile=px(100), link_to='custom', link=link(U + '/'), align='left',
          _flex_size='none'),
        nav,
        BTN('Free Estimate', page_url('contact'), 'gold', 'fas fa-clipboard-check', size='sm', hide_mobile='hidden-mobile', _flex_size='none'),
    ], 'Main Bar', inner=False, content_width='boxed', row=True, flex_direction_mobile='row', flex_justify_content='space-between', flex_align_items='center', flex_wrap='nowrap',
        padding=dims(6, 20), padding_mobile=dims(10, 16), flex_gap=gap(20), background_background='classic', g={'background_color': col('qwwhite')},
        box_shadow_box_shadow_type='yes', box_shadow_box_shadow=shadow(6, 24, 'rgba(14,20,32,0.10)'))
    ld = {'@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness', 'name': 'Quality Waterproofing', 'url': U + '/', 'telephone': '+1-437-264-2664',
          'email': EMAIL, 'logo': MEDIA['logo']['url'], 'image': MEDIA['ext_trench_membrane']['url'], 'slogan': TAGLINE,
          'description': 'Basement waterproofing, sump pump installation, foundation crack repair and interlocking in Toronto, Mississauga, Brampton and North Bay.',
          'areaServed': [{'@type': 'City', 'name': c} for c in ('Toronto', 'Mississauga', 'Brampton', 'North Bay', 'Vaughan', 'Markham', 'Richmond Hill', 'Oakville')],
          'sameAs': [FB, IG],
          'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Waterproofing Services', 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': SERVICES[s]['name'], 'url': page_url(s)}} for s in SVC_ORDER]}}
    schema = W('html', 'Schema (LocalBusiness JSON-LD)', html='<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    return [C([top, main, schema], 'Header', inner=False, content_width='full', padding=dims(0), flex_gap=gap(0),
              sticky='top', sticky_on=['desktop', 'tablet', 'mobile'], sticky_offset=0, sticky_effects_offset=90, z_index=99)]

def footer():
    seed('footer')
    def fl(items): return ILIST(items, color='qwmuted', icon_color='secondary', typo='qwsmall', size=10, gapv=8, icon='fas fa-chevron-right', g={'text_color_hover': col('secondary')})
    def fh(t): return H(t, 'p', 'qwh3', 'qwwhite', _margin=dims(0, 0, 6, 0))
    about = C([
        IMG('logo', size='full', width=px(190), radius=0, align='left'),
        T(TAGLINE + '. Basement waterproofing, foundation crack repair, sump pumps and interlocking for homeowners in Toronto, the GTA and North Bay. Over 10 years of residential and commercial construction experience.', 'qwmuted', 'qwsmall'),
        W('social-icons', 'Social Icons', social_icon_list=[{'_id': uid(), 'social_icon': ico('fab fa-facebook-f', 'fa-brands'), 'link': link(FB, True)},
                                                           {'_id': uid(), 'social_icon': ico('fab fa-instagram', 'fa-brands'), 'link': link(IG, True)}],
          shape='square', align='left', icon_size=px(15), icon_padding=px(0.8, 'em'), icon_spacing=px(10), icon_color='custom',
          icon_primary_color='#161E2D', icon_secondary_color='#C9A24B', hover_primary_color='#C9A24B', hover_secondary_color='#0E1420', border_radius=dims(4)),
    ], 'Footer About', flex_gap=gap(18))
    svc = C([fh('Services')] + [fl([(SERVICES[s]['name'], 'fas fa-chevron-right', page_url(s)) for s in SVC_ORDER])], 'Footer Services', flex_gap=gap(10))
    areas = C([fh('Service Areas')] + [fl([('Waterproofing ' + LOCATIONS[s]['label'], 'fas fa-chevron-right', page_url(s)) for s in LOC_ORDER] + [('Projects', 'fas fa-chevron-right', page_url('projects')), ('About Us', 'fas fa-chevron-right', page_url('about-us'))])], 'Footer Areas', flex_gap=gap(10))
    contact = C([fh('Get In Touch'),
                 ILIST([(PHONE, 'fas fa-phone-alt', TEL), (EMAIL, 'fas fa-envelope', 'mailto:' + EMAIL), ('Toronto · Mississauga · Brampton · North Bay', 'fas fa-map-marker-alt')],
                       color='qwwhite', icon_color='secondary', typo='qwsmall', size=15, gapv=14),
                 BTN('Get a Free Estimate', page_url('contact'), 'gold', 'fas fa-clipboard-check', size='sm')], 'Footer Contact', flex_gap=gap(14))
    grid = C([about, svc, areas, contact], 'Footer Grid', grid=4, grid_t=2, grid_gaps=gap(40), grid_columns_grid=cols('1.5fr 1fr 1.1fr 1.2fr'))
    top = SECTION([grid], 'Footer Main', bg='primary', pad=(80, 64, 52), background_background='classic', g={'background_color': col('primary')})
    bottom = C([T('© 2026 Quality Waterproofing. All rights reserved.', 'qwmuted', 'qwsmall'),
                T('Basement Waterproofing Toronto · Mississauga · Brampton · North Bay', 'qwmuted', 'qwsmall')],
               'Footer Bottom', inner=False, content_width='boxed', row=True, flex_justify_content='space-between', flex_align_items='center', padding=dims(20, 20), padding_mobile=dims(20, 16),
               flex_wrap='wrap', background_background='classic', border_border='solid', border_width=dims(1, 0, 0, 0), border_color='#2A3448', g={'background_color': col('primary')})
    return [top, bottom]

# ================= pages =================
GEN_FAQ = [('Do you offer free estimates?', 'Yes. We provide free on-site inspections and written estimates for homeowners in Toronto, Mississauga, Brampton, North Bay and across the GTA.'),
           ('What areas do you serve?', 'We serve Toronto and the Greater Toronto Area – including Mississauga, Brampton, Etobicoke, North York, Scarborough and Vaughan – as well as North Bay and the surrounding area.'),
           ('Should I choose interior or exterior waterproofing?', 'It depends on where the water is entering, access around your home and your plans for the basement. Exterior waterproofing stops water before it reaches the wall; interior waterproofing manages it from inside with a drain and sump pump. We will explain both options during your inspection.'),
           ('Do you do residential and commercial work?', 'Yes. Our team has over 10 years of residential and commercial construction experience.'),
           ('Besides waterproofing, what else do you do?', 'We also install sump pumps, repair foundation cracks and build interlocking patios, walkways and driveways. Ask us about walkouts and underpinning too.')]

def home():
    seed('home')
    return [
        hero('Toronto · Mississauga · Brampton · North Bay', 'Basement Waterproofing & Foundation Repair in the <span class="qw-hl">GTA & North Bay</span>',
             'Wet basement? Leaking foundation crack? Quality Waterproofing keeps homes across Toronto, the GTA and North Bay dry with exterior and interior waterproofing, sump pumps, crack repair and expert interlocking.',
             bg='ext_long_trench', video=True, minh=720),
        trust_strip(),
        services_grid(),
        split('Wet Basement? We Have <span class="qw-hl">the Solutions</span>',
              ['A wet basement is a major concern for any homeowner. Leaks lead to damaged drywall and flooring, ruined belongings, mould growth and poor air quality – and they only get worse with time.',
               'Quality Waterproofing specializes in repairing wet basements and preventing future leaks. We waterproof foundations from the outside, install interior drainage and sump pump systems, seal leaking cracks and correct grading with new interlock, so water is directed away from your home for good.'],
              'ext_orange_membrane', 'int_dmx_window', eyebrow='The Problem',
              extra=[ILIST(['Water at the base of walls or the floor joint', 'Damp walls, white efflorescence or musty smells', 'Leaks after heavy rain or spring thaw', 'Cracked foundation walls'], _margin=dims(6, 0, 6, 0)),
                     BTN('Book a Free Inspection', '#estimate', 'gold', 'fas fa-arrow-right')]),
        why_us(bg='cream'),
        process(),
        gallery(['ext_trench_membrane', 'int_dmx_window', 'il_pool1', 'ext_brick_membrane', 'sump_basin', 'il_patio_steps', 'int_unfinished', 'ext_red_brick', 'crack_patch', 'il_steps', 'ext_long_trench', 'il_rear'],
                intro='Real projects completed by our crews – exterior and interior waterproofing, sump pumps, crack repairs and interlocking.'),
        areas_section(),
        faq_section(GEN_FAQ),
        cta_band(),
    ]

def services_hub():
    seed('services')
    return [hero('Our Services', 'Basement Waterproofing <span class="qw-hl">Services</span> in Toronto & the GTA',
                 'Exterior and interior waterproofing, sump pump installation, exterior foundation crack repair and interlocking – everything you need to keep water out and protect your home.',
                 bg='ext_orange_membrane', minh=560),
            services_grid(intro=True), why_us('ext_crew_trench', 'int_column'), process(), areas_section(), cta_band()]

def service_page(slug):
    seed(slug); S = SERVICES[slug]
    signs = SECTION(HEAD('Warning Signs', f'Signs You Need <span class="qw-hl">{S["name"]}</span>', align='center')
                    + [C([CARD([W('icon', 'Icon', selected_icon=ico('fas fa-exclamation-triangle'), view='stacked', shape='square', size=px(18), icon_padding=px(13), align='left',
                                  g={'primary_color': col('primary'), 'secondary_color': col('secondary')}),
                                T(s, 'primary', 'qwbody')], title='Sign', pad=26, row=True, flex_direction_mobile='row', flex_align_items='center', flex_gap=gap(16))
                          for s in S['signs']], 'Signs Grid', grid=3, grid_t=2, grid_gaps=gap(18), _margin=dims(20, 0, 0, 0))], 'Signs', bg='cream')
    benefits = SECTION(HEAD('Benefits', f'Why Choose Our <span class="qw-hl">{S["name"]}</span>', align='center')
                       + [C([IBOX(i, t, d, view='stacked') for i, t, d in S['benefits']], 'Benefits Grid', grid=3, grid_t=2, grid_gaps=gap(36, 40), _margin=dims(26, 0, 0, 0))], 'Benefits', bg='white')
    return [
        hero(S['name'] + ' · Toronto & GTA', S['h1'], S['lead'], bg=S['hero']),
        split(S['intro_h'], S['intro'], S['intro_img'], S['intro_img2'], eyebrow=S['name'], extra=[CTA_BTNS(dark=False)]),
        signs,
        process(S['steps'], f'Our {S["name"]} <span class="qw-hl">Process</span>'),
        benefits,
        gallery(S['gallery'], f'{S["name"]} <span class="qw-hl">Projects</span>', 'Project Gallery', cols=4, bg='light'),
        areas_section(),
        faq_section(S['faq'], side_img=S['gallery'][1]),
        form_section(),
        services_grid(intro=False, exclude=slug, bg='white'),
    ]

def location_page(slug):
    seed(slug); L = LOCATIONS[slug]; city = L['city']
    local = SECTION(HEAD('Local Expertise', L['local_h'].replace(city, f'<span class="qw-hl">{city}</span>'), align='center')
                    + [C([IBOX(i, t, d, view='stacked') for i, t, d in L['local']], 'Local Grid', grid=4, grid_t=2, grid_gaps=gap(30), _margin=dims(24, 0, 0, 0))], 'Local Issues', bg='white')
    svc_cards = [SERVICE_CARD(SERVICES[s]['card'], f"{SERVICES[s]['name']}", SERVICES[s]['card_text'], page_url(s)) for s in SVC_ORDER] + [inspection_card()]
    svcs = SECTION(HEAD('Services in ' + city, f'Our Services in <span class="qw-hl">{city}</span>', f'Everything you need to keep your {city} basement dry and your exterior looking great.', align='center')
                   + [C(svc_cards, 'Services Grid', grid=3, grid_t=2, grid_gaps=gap(24), _margin=dims(24, 0, 0, 0))], 'Services', bg='cream')
    hoods = SECTION([C([
        C(HEAD('Neighbourhoods', f'Areas We Serve in and Around <span class="qw-hl">{city}</span>') + [
            T(f'We provide basement waterproofing, sump pump installation, foundation crack repair and interlocking throughout {city} and nearby communities, including:'),
            C([ILIST(L['hoods'][:6], icon='fas fa-map-marker-alt'), ILIST(L['hoods'][6:], icon='fas fa-map-marker-alt')], 'Hood Lists', grid=2, grid_t=2, grid_m=2, grid_gaps=gap(20)),
            T('Don’t see your area? Call us – we likely serve it.', 'primary', 'qwsmall')], 'Hoods Copy', flex_gap=gap(16)),
        W('google_maps', 'Map', address=city + ', Ontario, Canada', zoom=px(11), height=px(440), height_mobile=px(300), _border_radius=dims(6)),
    ], 'Hoods Grid', grid=2, grid_t=1, grid_gaps=gap(56, 36), grid_align_items='center')], 'Neighbourhoods', bg='white')
    return [
        hero(f'Serving {L["label"]}', L['h1'].replace(city, f'<span class="qw-hl">{city}</span>', 1), L['lead'], bg=L['hero']),
        split(f'Trusted Waterproofing Contractor in <span class="qw-hl">{city}</span>', L['intro'], L['img'], L['img2'], eyebrow=L['label'], extra=[CTA_BTNS(dark=False)]),
        svcs, local, process(), hoods, why_us(bg='cream'), faq_section(L['faq'] + GEN_FAQ[2:4], side_img=L['img']), form_section(f'Free Estimate in <span class="qw-hl">{city}</span>'),
    ]

def about():
    seed('about')
    values = SECTION(HEAD('Our Values', 'What Every Customer <span class="qw-hl">Can Expect</span>', align='center')
                     + [C([IBOX('fas fa-search', 'Honest Diagnosis', 'We find the real cause of the water and recommend the right fix – not the most expensive one.', view='stacked'),
                           IBOX('fas fa-gem', 'Quality Workmanship', 'Careful excavation, proper materials and attention to detail on every job, big or small.', view='stacked'),
                           IBOX('fas fa-handshake', 'Respect for Your Home', 'We protect your property, keep the site safe and clean up when the work is finished.', view='stacked'),
                           IBOX('fas fa-file-invoice', 'Clear Communication', 'Written quotes, clear timelines and straight answers from the first call to the final walkthrough.', view='stacked')],
                          'Values Grid', grid=4, grid_t=2, grid_gaps=gap(30), _margin=dims(24, 0, 0, 0))], 'Values', bg='cream')
    return [
        hero('About Quality Waterproofing', 'Protecting GTA Basements With <span class="qw-hl">Quality Work</span>',
             'We are a waterproofing and exterior construction company serving Toronto, Mississauga, Brampton and North Bay, with more than 10 years of residential and commercial experience.',
             bg='ext_crew_trench', form=False, minh=520),
        split('Who <span class="qw-hl">We Are</span>',
              ['<strong>' + TAGLINE + '.</strong> That has been our focus for more than 10 years.',
               'Quality Waterproofing specializes in basement waterproofing and the exterior work that keeps a home dry and looking its best – exterior and interior waterproofing, sump pump installation, foundation crack repair and interlocking. Our team also brings experience in landscaping, walkouts, underpinning, concrete and drainage.',
               'With more than 10 years of residential and commercial construction experience, we know that every basement is different. That’s why every job starts with a proper inspection, and every recommendation comes with a clear explanation and a written quote.',
               'Our goal is simple: a dry basement, a protected foundation and a homeowner who would happily recommend us to their neighbours.'],
              'ext_worker_dig', 'il_pool2', eyebrow='Our Story', extra=[CTA_BTNS(dark=False)]),
        values, process(), services_grid(dark=False), cta_band()]

def projects():
    seed('projects')
    def g(t, keys): return {'_id': uid(), 'gallery_title': t, 'multiple_gallery': [img(k) for k in keys]}
    gal = W('gallery', 'Project Gallery', gallery_type='multiple', galleries=[
        g('Exterior Waterproofing', SERVICES['exterior-waterproofing']['gallery'] + ['ext_worker_dig', 'ext_brick_coat', 'ext_parging', 'ext_blueskin', 'ext_crew_trench', 'ext_live2']),
        g('Interior Waterproofing', SERVICES['interior-waterproofing']['gallery'] + ['int_orange']),
        g('Sump Pumps', ['sump_basin', 'sump_system', 'sump_pit']),
        g('Crack Repair', SERVICES['foundation-crack-repair']['gallery']),
        g('Interlocking', SERVICES['interlocking']['gallery'] + ['il_live_deck'])],
        show_all_galleries='yes', show_all_galleries_label='All Projects', gallery_layout='grid', columns=4, columns_tablet=3, columns_mobile=2, gap=px(12), gap_mobile=px(8),
        aspect_ratio='1:1', thumbnail_image_size='medium_large', link_to='file', open_lightbox='yes', image_hover_animation='zoom-in', overlay_background='yes',
        background_overlay_color='rgba(14,20,32,0.45)', galleries_pointer='underline', galleries_animation_line='grow', galleries_title_space_between=px(10), galleries_title_gap=px(34),
        g={'galleries_title_color_normal': col('primary'), 'galleries_title_color_hover': col('qwgolddk'), 'galleries_pointer_color_hover': col('secondary'),
           'galleries_title_color_active': col('qwgolddk'), 'galleries_pointer_color_active': col('secondary'), 'galleries_typography_typography': typ('qwnav')})
    return [hero('Our Work', 'Waterproofing & Interlocking <span class="qw-hl">Projects</span>',
                 'Browse recent projects by our crews across Toronto, the GTA and North Bay – from deep exterior excavations to finished pool patios.', bg='il_pool3', form=False, minh=480),
            SECTION(HEAD('Project Gallery', 'Real Work, <span class="qw-hl">Real Homes</span>', 'Filter by service and click any photo to view it full size.', align='center') + [C([gal], 'Gallery Wrap', _margin=dims(20, 0, 0, 0))], 'Projects', bg='white'),
            cta_band()]

def contact():
    seed('contact')
    cards = [CARD([IBOX('fas fa-phone-alt', 'Call Us', f'<a href="{TEL}">{PHONE}</a>', view='stacked', align='left')], title='Phone Card', pad=28),
             CARD([IBOX('fas fa-envelope', 'Email Us', f'<a href="mailto:{EMAIL}">{EMAIL}</a>', view='stacked', align='left')], title='Email Card', pad=28),
             CARD([IBOX('fas fa-map-marker-alt', 'Service Areas', 'Toronto & GTA · Mississauga · Brampton · North Bay', view='stacked', align='left')], title='Areas Card', pad=28)]
    left = C(HEAD('Get In Touch', 'Let’s Talk About <span class="qw-hl">Your Basement</span>', 'Call, email or send the form and we’ll get back to you quickly to book your free on-site inspection.') + cards
             + [W('social-icons', 'Social Icons', social_icon_list=[{'_id': uid(), 'social_icon': ico('fab fa-facebook-f', 'fa-brands'), 'link': link(FB, True)},
                                                                   {'_id': uid(), 'social_icon': ico('fab fa-instagram', 'fa-brands'), 'link': link(IG, True)}],
                  shape='square', align='left', icon_size=px(16), icon_padding=px(0.8, 'em'), icon_spacing=px(10), icon_color='custom', icon_primary_color='#0E1420',
                  icon_secondary_color='#C9A24B', hover_primary_color='#C9A24B', hover_secondary_color='#0E1420', border_radius=dims(4))], 'Contact Info', flex_gap=gap(16))
    right = CARD([H('Request a <span class="qw-hl">Free Estimate</span>', 'h2', 'qwh3'), T('All fields marked * are required.', 'text', 'qwsmall'), FORM('Contact Page Estimate')],
                 title='Contact Form Card', pad=40, _element_id='estimate')
    return [hero('Contact Quality Waterproofing', 'Contact Us for a <span class="qw-hl">Free Estimate</span>',
                 'Serving Toronto, Mississauga, Brampton, North Bay and the GTA. Call ' + PHONE + ' or send us a message below.', bg='int_long', form=False, minh=440),
            SECTION([C([left, right], 'Contact Grid', grid=2, grid_t=1, grid_gaps=gap(56, 40))], 'Contact', bg='white'),
            areas_section(), faq_section(GEN_FAQ[:3])]

# ================= push =================
SEO_TITLES = {'home': 'Home', 'services': 'Waterproofing Services', 'about-us': 'About Us', 'projects': 'Projects', 'contact': 'Contact Us'}
PAGE_SETTINGS = {'hide_title': 'yes'}

def build(name):
    if name == 'header': return header()
    if name == 'footer': return footer()
    if name == 'home': return home()
    if name == 'services': return services_hub()
    if name == 'about-us': return about()
    if name == 'projects': return projects()
    if name == 'contact': return contact()
    if name in SERVICES: return service_page(name)
    if name in LOCATIONS: return location_page(name)
    raise SystemExit('unknown part ' + name)

ALL = ['header', 'footer', 'home', 'services', 'about-us', 'projects', 'contact'] + SVC_ORDER + LOC_ORDER
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    names = ALL if args == ['all'] else args
    os.makedirs(os.path.join(D, 'out'), exist_ok=True)
    TPL = json.load(open(os.path.join(D, 'templates.json')))
    for n in names:
        data = build(n)
        json.dump(data, open(os.path.join(D, 'out', n + '.json'), 'w'))
        if dry: print(n, 'built', len(json.dumps(data)) // 1024, 'KB'); continue
        if n in ('header', 'footer'):
            put(TPL[n], data, 'elementor_library', extra={'_ttype': n, 'status': 'publish'})
        else:
            # keep the page's current status (pages are drafts until the client approves; only Home is public)
            extra = {'status': wp.req(f'wp/v2/pages/{PAGES[n]}?_fields=status')['status'], 'template': 'elementor_header_footer'}
            if n in SERVICES: extra['title'] = SERVICES[n]['name']
            if n in LOCATIONS: extra['title'] = LOCATIONS[n]['h1']
            put(PAGES[n], data, 'pages', extra=extra, settings=PAGE_SETTINGS)
    if not dry: clear_cache()
