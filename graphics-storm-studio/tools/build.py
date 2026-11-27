"""Builds every template/page of the redesign from native Elementor widgets.
python3 build.py            -> writes ../templates/*.json (importable) only
python3 build.py --push     -> also pushes header/footer/CTA/pages to the site as DRAFTS"""
import json, os, sys, urllib.parse
import el
from el import (C, ROW, COL, GRID, SECTION, GLASS, H, EYEBROW, P, BTN, ICONBOX, ICONLIST, COUNTER, IMG, FAQ,
                FORM, TEMPLATE, W, px, dims, gap, col, typ, ico, link, section_head)
import content as K

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'templates')

# ------------------------------------------------------------------ infographics (animated SVG in native Image widgets)
import gfx
def _media():
    try: return json.load(open(os.path.join(HERE, 'created.json'))).get('media', {})
    except Exception: return {}
INFO_ALT = {'gss-growth-engine.svg': 'Infographic: website development, SEO, social media marketing and graphic design working together as one growth engine to deliver more leads and revenue',
            'gss-website-development.svg': 'Infographic: responsive website built for desktop and mobile with a 98 PageSpeed score',
            'gss-seo-services.svg': 'Infographic: your website climbing to the number one Google result with organic traffic up 214 percent',
            'gss-social-media-marketing.svg': 'Infographic: social media post gaining likes, followers and leads with growing reach and engagement',
            'gss-graphic-design.svg': 'Infographic: logo being designed with the pen tool, brand colour palette and typography',
            'gss-about.svg': 'Infographic: one connected Graphics Storm Studio team with 5+ years, 130+ clients and 180+ websites',
            'gss-services-funnel.svg': 'Infographic: digital marketing funnel – attract with social media and design, rank with SEO, convert with your website, grow with more leads',
            'gss-our-work.svg': 'Infographic: laptop and phone showcasing website, brand identity and SEO projects with results',
            'gss-contact.svg': 'Infographic: your enquiry is sent to our team, who reply within one business day',
            'gss-privacy.svg': 'Infographic: shield and padlock protecting your personal data',
            'gss-terms.svg': 'Infographic: service agreement checklist with clear scope, ownership of work, honest results and support'}
def INFO(name, label):
    m = _media().get(name)
    img = {'url': m['url'], 'id': m['id'], 'alt': INFO_ALT[name], 'source': 'library'} if m else {'url': el.PLACEHOLDER, 'id': '', 'alt': INFO_ALT[name], 'source': 'library'}
    return W('image', f'Infographic – {label} (animated SVG)', image=img, image_size='full', width=px(100, '%'), align='center',
             caption_source='none', image_border_radius=dims(18))

def info_panel(name, label):
    return GLASS(f'Infographic Panel – {label}', [INFO(name, label)], strong=True, pad=(20, 16, 12), radius=24)

def growth_engine_section(bg='a'):
    return SECTION('Growth Engine', [ROW('Engine Row', [
        COL('Engine Copy', [EYEBROW('One team · one strategy'),
                            H('Four Services. One <span>Growth Engine.</span>', 'h2', name='Engine Title'),
                            P('Your website, SEO, social media and branding should not work in silos. We plan them together, so every channel feeds the next – and every click has a better chance of becoming a customer.', 'gslead', name='Engine Text'),
                            ICONLIST(['Website converts the traffic SEO and social bring in', 'SEO compounds free, high-intent visitors every month',
                                      'Social media builds awareness, trust and retargeting audiences', 'Design keeps your brand consistent and memorable everywhere'],
                                     name='Engine Checklist'),
                            BTN('Get a Free Growth Plan', K.URL['contact'])], w=42, wt=100, gap_=22),
        COL('Engine Visual', [info_panel('gss-growth-engine.svg', 'Growth Engine')], w=58, wt=100)],
        gap_=56, stack='tablet', align='center')], bg=bg)

# ------------------------------------------------------------------ shared blocks
LOGO = {'id': 5904, 'url': 'https://graphicsstormstudio.com/wp-content/uploads/2026/11/graphics-storm-studio-logo.webp',
        'alt': 'Graphics Storm Studio – digital marketing agency', 'source': 'library'}

def logo(w=180, wm=150):
    """Brand logo (Image widget, links home). Transparent WebP made from the client's logo – brand/gss-logo.webp."""
    return W('image', 'Logo', image=LOGO, image_size='full', width=px(w), width_tablet=px(w), width_mobile=px(wm),
             link_to='custom', link=link('/'), align='left', _element_width='auto', _flex_size='none')

def cta_band():
    """Saved template 'GS – CTA Band' (embedded everywhere via the Template widget)."""
    el.seed('cta')
    inner = GLASS('CTA Panel', [
        EYEBROW('Free strategy call', 'center'),
        H('Ready to Grow Your Business <span>Online?</span>', 'h2', align='center', name='CTA Title'),
        P('Book a free, no-obligation strategy call. We will review your website, SEO and social media and show you exactly where your next customers will come from.',
          'gslead', align='center', maxw=680, name='CTA Text'),
        ROW('CTA Buttons', [BTN('Get a Free Proposal', K.URL['contact']),
                            BTN('Chat on WhatsApp', K.WHATSAPP, 'ghost', 'fab fa-whatsapp', ext=True)],
            gap_=14, justify='center', align='center', flex_wrap='wrap', flex_direction_mobile='column', flex_align_items_mobile='stretch'),
    ], strong=True, pad=(64, 48, 32), radius=28, flex_align_items='center', flex_gap=gap(18))
    inner['settings']['background_background'] = 'gradient'
    inner['settings']['background_color'] = 'rgba(124,92,255,0.22)'
    inner['settings']['background_color_b'] = 'rgba(6,132,196,0.18)'
    inner['settings']['background_gradient_angle'] = {'unit': 'deg', 'size': 135, 'sizes': []}
    inner['settings']['__globals__'].pop('background_color', None)
    return [SECTION('CTA Band', [inner], pad=(40, 32, 24), tag='section')]

def FORM_HEAD(title, sub):
    return C('Form Header', [EYEBROW('Free proposal · no obligation'), H(title, 'h3', 'gsh3', name='Form Title'),
                             P(sub, 'gssmall', 'text', name='Form Intro')], flex_gap=gap(8),
             padding=dims(0, 0, 18, 0), border_border='solid', border_width=dims(0, 0, 1, 0), g=dict(border_color=col('gsline')))

def FORM_TRUST():
    return ICONLIST([('No obligation', 'fas fa-check-circle'), ('Reply in 1 business day', 'fas fa-clock'), ('100% confidential', 'fas fa-lock')],
                    inline=True, t='gssmall', name='Form Trust Row', space_between=px(20), icon_size=px(13))

def PRIVACY_NOTE():
    return P('We only use your details to reply to your enquiry – see our <a href="/privacy-policy/">Privacy Policy</a>.',
             'gssmall', 'gsmuted', name='Privacy Note')

def cta(ids):
    return TEMPLATE(ids['cta'], 'CTA Band (saved template)') if ids and ids.get('cta') else cta_band()[0]

def page_hero(eyebrow, h1, lead, buttons=True, extra=None, info=None):
    """Two-column hero: copy left, animated infographic (glass panel) right; stacks on tablet/mobile."""
    kids = [EYEBROW(eyebrow), H(h1, 'h1', 'gsh1', name='H1 – Page Title'), P(lead, 'gslead', name='Lead')]
    if buttons:
        kids.append(ROW('Hero Buttons', [BTN('Get a Free Proposal', K.URL['contact']), BTN('Call ' + K.PHONE_DISPLAY, K.PHONE_TEL, 'ghost', 'fas fa-phone-alt')],
                        gap_=14, flex_wrap='wrap', flex_direction_mobile='column', flex_align_items_mobile='stretch'))
    if extra: kids += extra
    copy = COL('Hero Copy', kids, w=50, wt=100, gap_=20, animation='fadeInUp', animation_duration='fast')
    visual = COL('Hero Visual', [info_panel(*info)], w=50, wt=100)
    return SECTION('Page Hero', [ROW('Hero Row', [copy, visual], gap_=56, stack='tablet', align='center')], bg='a', pad=(88, 72, 48))

def service_cards(items=K.SERVICES_GRID, tag='h3'):
    return GRID('Services Grid', [GLASS(f'Service Card – {t}', [ICONBOX(i, t, d, u, tag=tag),
                    BTN('Learn more', u, 'link', 'fas fa-arrow-right', name='Card Link', size='sm',
                        background_color='rgba(0,0,0,0)', button_background_hover_color='rgba(0,0,0,0)', text_padding=dims(0),
                        g=dict(button_text_color=col('accent'), hover_color=col('gswhite')))], hover=True, flex_justify_content='space-between')
                 for i, t, d, u in items], 3, 2, 1)

def stats_band():
    return GLASS('Stats Panel', [GRID('Counters', [COL(f'Stat – {t}', [COUNTER(n, t)], gap_=4, flex_align_items='center') for n, t in K.STATS], 4, 2, 2, 32)],
                 strong=True, pad=(48, 40, 28), radius=24)

def process():
    return GRID('Process Steps', [GLASS(f'Step {n}', [H(n, 'p', 'gsstat', 'accent', name='Step Number', grad=False, _css_classes='gs-grad'),
                                                      H(t, 'h3', 'gsh3', name='Step Title'), P(d, name='Step Text')], hover=True)
                                  for n, t, d in K.PROCESS], 4, 2, 1)

def testimonials():
    slides = [{'_id': el.uid(), 'content': q, 'name': n, 'title': r} for n, r, q in K.TESTIMONIALS]
    return W('testimonial-carousel', 'Testimonials Carousel', slides=slides, skin='default', layout='image_above',
             alignment='left', slides_per_view='3', slides_per_view_tablet='2', slides_per_view_mobile='1',
             slides_to_scroll='1', space_between=px(24), autoplay='yes', autoplay_speed=6000, loop='yes',
             pause_on_hover='yes', pagination='bullets', show_arrows='', speed=600,
             slide_background_color='rgba(255,255,255,0.06)', slide_border_size=dims(1), slide_border_radius=px(20),
             slide_border_color='rgba(255,255,255,0.14)', slide_padding=dims(32, 28),
             _css_classes='gs-glass-slides',
             g=dict(content_color=col('text'), content_typography_typography=typ('gsbody'),
                    name_color=col('gswhite'), name_typography_typography=typ('gsh4'),
                    title_color=col('accent'), title_typography_typography=typ('gssmall'),
                    pagination_color=col('accent')))

def logos_strip():
    return C('Client Logos', [P('Trusted by growing brands across the USA, Canada & beyond', 'gssmall', 'gsmuted', 'center', name='Logos Label'),
              GRID('Logo Row', [IMG(f'client-logo-{i}.svg', '240×96, transparent SVG/PNG, white or light version', f'Client logo {i}', radius=0,
                                    width=px(140), opacity=px(0.75, ''), align='center')
                                for i in range(1, 6)], 5, 3, 2, 32, flex_align_items='center')],
             flex_direction='column', flex_gap=gap(24),
             hide_desktop='hidden-desktop', hide_tablet='hidden-tablet', hide_mobile='hidden-mobile')  # hidden until real client logos are uploaded

# ------------------------------------------------------------------ header / footer
def header():
    el.seed('header')
    nav = W('nav-menu', 'Main Menu', menu='gss-main', layout='horizontal', align_items='center', pointer='underline',
            animation_line='fade', submenu_icon=ico('fas fa-chevron-down'), dropdown='tablet', full_width='stretch',
            text_align='aside', toggle='burger', toggle_align='right', padding_horizontal_menu_item=px(14),
            padding_vertical_menu_item=px(10), pointer_width=px(2), dropdown_border_radius=dims(14),
            padding_horizontal_dropdown_item=px(20), padding_vertical_dropdown_item=px(12), dropdown_top_distance=px(14),
            toggle_size=px(22), toggle_border_width=px(1), toggle_border_radius=px(12),
            background_color_dropdown_item='#0E1738', toggle_background_color='rgba(255,255,255,0.10)',
            g=dict(menu_typography_typography=typ('gsnav'), color_menu_item=col('gswhite'), color_menu_item_hover=col('accent'),
                   pointer_color_menu_item_hover=col('accent'), color_menu_item_active=col('accent'), pointer_color_menu_item_active=col('accent'),
                   color_dropdown_item=col('text'), color_dropdown_item_hover=col('gswhite'),
                   background_color_dropdown_item_hover=col('primary'), dropdown_typography_typography=typ('gsnav'),
                   toggle_color=col('gswhite')))
    bar = C('Header Bar', [logo(), C('Nav + CTA', [nav, BTN('Free Consultation', K.URL['contact'], icon=None, name='Header CTA', size='sm',
                                                          hide_mobile='hidden-mobile')],
                                    flex_direction='row', flex_align_items='center', flex_gap=gap(18), flex_justify_content='flex-end',
                                    width=px(100, '%'), flex_grow=1)],
            content_width='boxed', flex_direction='row', flex_align_items='center', flex_justify_content='space-between',
            flex_wrap='nowrap', padding=dims(14, 24), padding_mobile=dims(12, 16), flex_gap=gap(24))
    root = C('Header – Sticky Glass', [bar], html_tag='header', css_classes='gs-glass-header',
             sticky='top', sticky_on=['desktop', 'tablet', 'mobile'], sticky_effects_offset=60,
             background_background='classic', g=dict(background_color=col('gstransparent')), z_index=99)
    return [root]

def footer():
    el.seed('footer')
    head = lambda t: H(t, 'h2', 'gsh4', name=f'Footer Title – {t}')
    brand = COL('Footer Brand', [logo(200, 180), P('A design-led digital marketing agency helping businesses grow with websites, SEO, social media marketing and graphic design.', 'gssmall', name='Footer About'),
                                 W('social-icons', 'Social Icons', social_icon_list=[
                                     {'_id': el.uid(), 'social_icon': ico('fab fa-instagram', 'fa-brands'), 'link': link(K.INSTAGRAM, True), 'item_icon_color': 'default'},
                                     {'_id': el.uid(), 'social_icon': ico('fab fa-whatsapp', 'fa-brands'), 'link': link(K.WHATSAPP, True), 'item_icon_color': 'default'},
                                     {'_id': el.uid(), 'social_icon': ico('fab fa-facebook-f', 'fa-brands'), 'link': link('#facebook-url-here', True), 'item_icon_color': 'default'},
                                     {'_id': el.uid(), 'social_icon': ico('fab fa-linkedin-in', 'fa-brands'), 'link': link('#linkedin-url-here', True), 'item_icon_color': 'default'}],
                                   shape='circle', align='left', icon_color='custom', icon_size=px(16), icon_padding=px(0.75, 'em'), icon_spacing=px(10),
                                   border_border='solid', border_width=dims(1), hover_animation='float',
                                   g=dict(icon_primary_color=col('gsglass2'), icon_secondary_color=col('gswhite'), border_color=col('gsline'),
                                          hover_primary_color=col('secondary'), hover_secondary_color=col('gswhite')))],
                 w=29, wt=100, gap_=18)
    quick = COL('Footer Links', [head('Company'), ICONLIST(['Home', 'About Us', 'Our Work', 'Contact Us', 'Free Consultation'], icon='fas fa-angle-right',
                                                         t='gssmall', name='Company Links', icolor='primary',
                                                         links=[K.URL['home'], K.URL['about'], K.URL['work'], K.URL['contact'], K.URL['contact']], space_between=px(10))], w=16, wt=30, gap_=16)
    svc = COL('Footer Services', [head('Services'), ICONLIST(['Website Development', 'SEO Services', 'Social Media Marketing', 'Graphic Design', 'Logo & Branding'],
                                                         icon='fas fa-angle-right', t='gssmall', name='Service Links', icolor='primary',
                                                         links=[K.URL['web'], K.URL['seo'], K.URL['smm'], K.URL['design'], K.URL['design']], space_between=px(10))], w=21, wt=30, gap_=16)
    contact = COL('Footer Contact', [head('Get in touch'), ICONLIST([(K.EMAIL, 'fas fa-envelope'), (K.PHONE_DISPLAY, 'fas fa-phone-alt')]
                                                                  + [(a, 'fas fa-map-marker-alt') for _, a in K.OFFICES], t='gssmall', name='Contact List',
                                                                  links=['mailto:' + K.EMAIL, K.PHONE_TEL, None, None], space_between=px(12))], w=24, wt=30, gap_=16)
    top = ROW('Footer Columns', [brand, quick, svc, contact], gap_=40, stack='mobile', flex_wrap='wrap', flex_wrap_tablet='wrap', flex_gap_tablet=gap(32))
    year_tag = '[elementor-tag id="%s" name="current-date-time" settings="%s"]' % (el.uid(), urllib.parse.quote(json.dumps(
        {'date_format': 'custom', 'time_format': '', 'custom_format': 'Y', 'before': '© ', 'after': ' Graphics Storm Studio. All rights reserved.'})))
    copy = H('© Graphics Storm Studio. All rights reserved.', 'p', 'gssmall', 'gsmuted', name='Copyright (dynamic year)')
    copy['settings']['__dynamic__'] = {'title': year_tag}
    bottom = ROW('Footer Bottom', [copy, ICONLIST(['Privacy Policy', 'Terms of Service'], inline=True, icon='fas fa-circle', t='gssmall', color='gsmuted',
                                                   name='Legal Links', links=['/privacy-policy/', '/terms-of-service/'], icon_size=px(4), space_between=px(20))],
                 justify='space-between', align='center', gap_=12, border_border='solid', border_width=dims(1, 0, 0, 0),
                 padding=dims(24, 0, 0, 0), g=dict(border_color=col('gsline')), flex_align_items_mobile='flex-start')
    root = SECTION('Footer', [top, bottom], tag='footer', pad=(80, 64, 48), gap_=48, bg='c')
    return [root]

# ------------------------------------------------------------------ pages
def home(ids=None):
    el.seed('home')
    hero_copy = COL('Hero Copy', [
        EYEBROW('Digital Marketing Agency · USA & Canada'),
        H('Grow Faster With a Digital Marketing Agency That <span>Delivers Results</span>', 'h1', 'gsh1', name='H1 – Hero'),
        P('Graphics Storm Studio builds high-converting websites, ranks you on Google with proven SEO services and grows your audience with social media marketing and standout graphic design – all from one dedicated team.', 'gslead', name='Hero Lead'),
        ROW('Hero Buttons', [BTN('Get a Free Proposal', '#free-proposal'), BTN('View Our Work', K.URL['work'], 'ghost', 'fas fa-play-circle')],
            gap_=14, flex_wrap='wrap', flex_direction_mobile='column', flex_align_items_mobile='stretch'),
        ICONLIST([('130+ happy clients', 'fas fa-star'), ('5+ years experience', 'fas fa-award'), ('USA & Canada offices', 'fas fa-globe-americas')],
                 inline=True, t='gssmall', name='Trust Row'),
    ], w=55, wt=100, gap_=24, animation='fadeInUp', animation_duration='fast')
    hero_visual = COL('Hero Visual', [info_panel('gss-growth-engine.svg', 'Growth Engine')], w=45, wt=100)
    hero = SECTION('Hero', [ROW('Hero Row', [hero_copy, hero_visual], gap_=56, stack='tablet', align='center')],
                   bg='a', pad=(88, 72, 48), gap_=64)
    hero['elements'][0]['elements'].append(logos_strip())
    proposal = SECTION('Free Proposal', [ROW('Proposal Row', [
        COL('Proposal Copy', [EYEBROW('Free proposal'), H('Get Your Free <span>Growth Proposal</span>', 'h2', name='Proposal Title'),
                              P('Tell us what you need and we will reply within 1 business day with a clear plan, timeline and price – no obligation.', 'gslead', name='Proposal Text'),
                              ICONLIST(['A quick audit of your website, SEO and social media', 'Recommended services for your goals and budget',
                                        'Fixed, transparent pricing before any work starts'], name='Proposal Checklist')], w=45, wt=100, gap_=20),
        COL('Proposal Form', [GLASS('Lead Form Panel', [
            FORM_HEAD('Tell us about your project', 'Takes 60 seconds. We reply with a tailored plan, timeline and price.'),
            FORM('Home Lead Form', ('name', 'email', 'phone', 'service', 'message_short'), 'Get My Free Proposal', 'Home Lead'),
            FORM_TRUST(), PRIVACY_NOTE()], strong=True, pad=(36, 28, 22), radius=24, flex_gap=gap(18))], w=55, wt=100)],
        gap_=56, stack='tablet', align='center')], anchor='free-proposal', bg='c')

    services = SECTION('Services', [section_head('What we do', 'Digital Marketing Services Built to <span>Grow Your Business</span>',
                                                 'From website development and SEO services to social media marketing and graphic design – everything you need to attract, convert and keep customers.'),
                                    service_cards()], anchor='services', bg='b')

    why = SECTION('Why Choose Us', [ROW('Why Row', [
        COL('Why Copy', [EYEBROW('Why Graphics Storm Studio'),
                         H('The Digital Marketing Partner That Treats Your Growth <span>Like Its Own</span>', 'h2', name='Why Title'),
                         P('No more wasted budget, missed deadlines or confusing reports. We combine premium design with data-driven marketing to give you a clear plan, a dedicated team and results you can measure.', 'gslead', name='Why Text'),
                         ICONLIST(['Personalised campaigns for your goals and budget', 'Reach your ideal audience faster', 'Low cost, high return marketing', 'Honest monthly reporting – no jargon'], name='Why Checklist'),
                         BTN('About Our Agency', K.URL['about'], 'ghost')], w=45, wt=100, gap_=22),
        COL('Why Cards', [GRID('Why Grid', [GLASS(f'Why – {t}', [ICONBOX(i, t, d)], hover=True, pad=(28, 24, 22)) for i, t, d in K.WHY], 2, 2, 1, 20)], w=55, wt=100)],
        gap_=56, stack='tablet', align='center'), stats_band()], bg='c', gap_=72)

    proc = SECTION('Process', [section_head('How we work', 'A Simple 4-Step Process to <span>Predictable Growth</span>',
                                            'Transparent from day one – you always know what we are doing, why, and what it achieved.'), process()], bg='a')

    testi = SECTION('Testimonials', [section_head('Client reviews', 'What Our Clients <span>Say About Us</span>'), testimonials()], bg='b')

    faq = SECTION('FAQ', [ROW('FAQ Row', [
        COL('FAQ Intro', [EYEBROW('FAQ'), H('Digital Marketing <span>Questions, Answered</span>', 'h2', name='FAQ Title'),
                          P('Can’t find what you are looking for? Our team is happy to help.', 'gslead', name='FAQ Text'),
                          BTN('Ask Us Anything', K.URL['contact'], 'ghost', 'fas fa-comments')], w=38, wt=100, gap_=20),
        COL('FAQ List', [FAQ(K.HOME_FAQ)], w=62, wt=100)], gap_=56, stack='tablet')], bg='c')

    return [hero, proposal, services, why, proc, testi, faq, cta(ids)]

def about(ids=None):
    el.seed('about'); A = K.ABOUT
    hero = page_hero('About us', A['h1'], A['lead'], info=('gss-about.svg', 'About'))
    story = SECTION('Our Story', [ROW('Story Row', [
        COL('Story Image', [IMG('about-team.webp', '1000×1100, team at work', 'Graphics Storm Studio team working together', radius=24)], w=45, wt=100),
        COL('Story Copy', [EYEBROW('Our story'), H(A['story_h2'], 'h2', name='Story Title'), P(A['story'], name='Story Text'),
                           GRID('Timeline', [GLASS(f'Timeline – {t}', [ICONBOX(i, t, d, tag='h3', icon_size=px(20), icon_padding=px(12))], pad=(22, 20, 18)) for i, t, d in A['timeline']], 1, 1, 1, 14)],
            w=55, wt=100, gap_=20)], gap_=56, stack='tablet', align='center'), stats_band()], bg='b', gap_=72)
    ceo = SECTION('CEO Message', [GLASS('CEO Quote', [
        W('icon', 'Quote Icon', selected_icon=ico('fas fa-quote-left'), size=px(36), g=dict(primary_color=col('secondary'))),
        H(A['ceo_quote'], 'p', 'gsh3', name='Quote', _css_classes=''),
        ROW('CEO', [IMG('ceo-portrait.webp', '400×400 square headshot', A['ceo'], radius=999, width=px(64), name='📷 PLACEHOLDER – ceo-portrait.webp (400×400)'),
                    C('CEO Name', [H(A['ceo'], 'p', 'gsh4', name='CEO Name'), P(A['ceo_role'], 'gssmall', 'accent', name='CEO Role')], flex_gap=gap(2))],
            gap_=16, align='center', flex_direction_mobile='row')], strong=True, pad=(56, 40, 28), radius=28, flex_gap=gap(22))], bg='a')
    values = SECTION('Values', [section_head('Our values', 'What You Can <span>Always Expect</span>'),
                                GRID('Values Grid', [GLASS(f'Value – {t}', [ICONBOX(i, t, d)], hover=True) for i, t, d in A['values']], 3, 2, 1)], bg='c')
    team = SECTION('Team', [section_head('Our team', 'Meet the People Behind <span>Your Growth</span>'),
                            GRID('Team Grid', [GLASS(f'Team – {n}', [IMG(f'team-{n.split()[0].lower()}.webp', '600×600 square headshot', f'{n}, {r} at Graphics Storm Studio', radius=16),
                                                                    H(n, 'h3', 'gsh4', name='Name'), P(r, 'gssmall', 'accent', name='Role')], pad=(16, 16, 16), hover=True, flex_gap=gap(10))
                                               for n, r in A['team']], 5, 3, 2, 20)], bg='b')
    return [hero, story, ceo, values, cta(ids)]   # team section removed at client request (no team photos)

def service(key, ids=None):
    el.seed('svc-' + key); S = K.SERVICE_PAGES[key]
    hero = SECTION('Service Hero', [ROW('Hero Row', [
        COL('Hero Copy', [EYEBROW(S['eyebrow']), H(S['h1'], 'h1', 'gsh1', name='H1 – Service'), P(S['lead'], 'gslead', name='Lead'),
                          ROW('Hero Buttons', [BTN('Get a Free Quote', '#service-quote'), BTN('Call ' + K.PHONE_DISPLAY, K.PHONE_TEL, 'ghost', 'fas fa-phone-alt')],
                              gap_=14, flex_wrap='wrap', flex_direction_mobile='column', flex_align_items_mobile='stretch')], w=56, wt=100, gap_=22,
            animation='fadeInUp', animation_duration='fast'),
        COL('Hero Visual', [info_panel(S['info'], S['title'])], w=44, wt=100)], gap_=56, stack='tablet', align='center')], bg='a', pad=(88, 72, 48))
    benefits = SECTION('Benefits', [section_head('Why it matters', f'Why Invest in Professional <span>{S["title"]}</span>?'),
                                    ROW('Benefits Row', [COL('Included', [GLASS('What’s Included', [H('What’s included', 'h3', 'gsh3', name='Included Title'), ICONLIST(S['included'], name='Included List')],
                                                                                  strong=True, pad=(32, 28, 24), radius=24)], w=50, wt=100),
                                                         COL('Benefits List', [GLASS(f'Benefit – {t}', [ICONBOX(i, t, d, position='left', position_mobile='top', icon_size=px(22), icon_padding=px(14))], hover=True, pad=(24, 22, 20)) for i, t, d in S['benefits']], w=50, wt=100, gap_=18)],
                                        gap_=40, stack='tablet', align='center')], bg='b')
    features = SECTION('Features', [section_head('Our services', f'{S["title"]} Services <span>We Offer</span>',
                                                 'Everything you need, delivered by specialists – pick a single service or a complete package.'),
                                    GRID('Features Grid', [GLASS(f'Feature – {t}', [ICONBOX(i, t, d)], hover=True) for i, t, d in S['features']], 3, 2, 1)], bg='c')
    proc = SECTION('Process', [section_head('Our process', 'How We <span>Work With You</span>'), process()], bg='a')
    quote = SECTION('Quote Form', [ROW('Quote Row', [
        COL('FAQ', [EYEBROW('FAQ'), H(f'{S["title"]} <span>FAQs</span>', 'h2', name='FAQ Title'), FAQ(S['faq'])], w=55, wt=100, gap_=20),
        COL('Quote Form Col', [GLASS('Quote Form Panel', [FORM_HEAD(f'Get a free {S["title"].lower()} quote', 'Share a few details and we will send a tailored proposal within 1 business day.'),
                                                           FORM('Service Quote Form', ('name', 'email', 'phone', 'budget', 'message'), 'Request My Free Quote', f'{S["title"]} Quote'),
                                                           FORM_TRUST(), PRIVACY_NOTE()],
                                     strong=True, pad=(36, 28, 22), radius=24, flex_gap=gap(18))], w=45, wt=100, _element_id='service-quote')],
        gap_=48, stack='tablet')], bg='b')
    return [hero, benefits, features, proc, quote, cta(ids)]

def services_hub(ids=None):
    el.seed('services-hub')
    return [page_hero('Our services', 'Digital Marketing Services That <span>Drive Growth</span>',
                      'Website development, SEO services, social media marketing and graphic design – one expert team, one clear strategy, measurable results.',
                      info=('gss-services-funnel.svg', 'Marketing Funnel')),
            SECTION('Services', [service_cards(tag='h2')], bg='b'),
            growth_engine_section('a'),
            SECTION('Process', [section_head('How we work', 'A Simple 4-Step <span>Process</span>'), process(), stats_band()], bg='c', gap_=56),
            cta(ids)]

def work(ids=None):
    el.seed('work')
    cats = [('Website Development', 'fas fa-laptop-code'), ('Brand Identity', 'fas fa-bezier-curve'), ('Social Media Marketing', 'fas fa-hashtag'),
            ('SEO', 'fas fa-search-dollar'), ('Graphic Design', 'fas fa-pen-nib'), ('Website Development', 'fas fa-laptop-code')]
    cards = [GLASS(f'Project {i}', [IMG(f'project-{i}.webp', '1200×900 (4:3) screenshot / mockup', f'[Project {i} name] – {c} project by Graphics Storm Studio', radius=14),
                                    EYEBROW(c, name='Category'), H(f'[Project {i} name]', 'h2', 'gsh3', name='Project Title'),
                                    P('[One-line result, e.g. “New website + SEO: 3× more enquiries in 6 months”]', 'gssmall', name='Project Result')],
                   hover=True, pad=(16, 16, 14), flex_gap=gap(12)) for i, (c, _) in enumerate(cats, 1)]
    return [page_hero('Our work', 'Websites, Brands & Campaigns That <span>Get Results</span>',
                      'A selection of recent website development, branding, social media and SEO projects for growing businesses.',
                      info=('gss-our-work.svg', 'Our Work')),
            SECTION('Portfolio', [ICONLIST([c for c in ['Websites', 'Branding', 'Social Media', 'SEO', 'Graphic Design']], inline=True, icon='fas fa-circle',
                                           t='gsnav', name='Categories (add anchors or Loop Grid filter later)', icon_size=px(6)),
                                  GRID('Projects Grid', cards, 3, 2, 1)], bg='b', gap_=32,
                    hide_desktop='hidden-desktop', hide_tablet='hidden-tablet', hide_mobile='hidden-mobile'),  # hidden until real projects are added
            SECTION('Testimonials', [section_head('Client reviews', 'Trusted by <span>Growing Brands</span>'), testimonials()], bg='c'),
            cta(ids)]

def contact(ids=None):
    el.seed('contact')
    info = [('fas fa-envelope', 'Email us', K.EMAIL, 'mailto:' + K.EMAIL), ('fas fa-phone-alt', 'Call us', K.PHONE_DISPLAY, K.PHONE_TEL),
            ('fab fa-whatsapp', 'WhatsApp', 'Chat with our team', K.WHATSAPP)] + \
           [('fas fa-map-marker-alt', f'{c} office', a, None) for c, a in K.OFFICES]
    cards = [GLASS(f'Info – {t}', [ICONBOX(i, t, d, u, tag='h2', icon_size=px(20), icon_padding=px(12), position='left',
                                           position_mobile='left', title_typography_typography='', g=dict(title_typography_typography=typ('gsh4')))],
                   pad=(20, 20, 16), hover=bool(u)) for i, t, d, u in info]
    return [page_hero('Contact us', 'Let’s Talk About <span>Growing Your Business</span>',
                      'Tell us about your project and get a free, no-obligation proposal. We reply within 1 business day.', buttons=False,
                      info=('gss-contact.svg', 'Contact')),
            SECTION('Contact', [ROW('Contact Row', [
                COL('Contact Info', [H('Get in touch', 'h2', 'gsh3', name='Info Title'),
                                     P('Prefer to talk? Call, email or WhatsApp us – or visit one of our offices.', name='Info Text')] + cards, w=40, wt=100, gap_=16),
                COL('Contact Form', [GLASS('Contact Form Panel', [FORM_HEAD('Request a free proposal', 'Tell us a little about your business and goals – we reply within 1 business day.'),
                                                                  FORM('Contact Form', ('name', 'email', 'phone', 'company', 'service', 'budget', 'message'),
                                                                       'Send My Request', 'Contact Page'),
                                                                  FORM_TRUST(), PRIVACY_NOTE()],
                                           strong=True, pad=(40, 28, 22), radius=24, flex_gap=gap(18))], w=60, wt=100)], gap_=40, stack='tablet')], bg='b'),
            SECTION('FAQ', [section_head('FAQ', 'Before You <span>Get in Touch</span>'), FAQ(K.HOME_FAQ[1:4])], bg='c')]

def legal_page(kind, ids=None):
    import legal as L
    el.seed('legal-' + kind)
    if kind == 'privacy':
        secs, h1, lead, info = L.PRIVACY, 'Privacy <span>Policy</span>', 'How Graphics Storm Studio collects, uses and protects your personal information – in plain English.', ('gss-privacy.svg', 'Privacy')
    else:
        secs, h1, lead, info = L.TERMS, 'Terms of <span>Service</span>', 'The terms that apply when you use our website and work with Graphics Storm Studio on websites, SEO, social media and design.', ('gss-terms.svg', 'Terms')
    hero = page_hero('Legal · Last updated ' + L.UPDATED, h1, lead, buttons=False, info=info)
    toc = GLASS('Table of Contents', [H('On this page', 'p', 'gsh4', name='TOC Title'),
                                      ICONLIST([t for _, t, _ in secs], icon='fas fa-angle-right', t='gssmall', icolor='accent', name='TOC Links',
                                               links=['#' + a for a, _, _ in secs], space_between=px(8))],
                pad=(24, 20, 20), radius=20, sticky='top', sticky_on=['desktop'], sticky_offset=110, sticky_parent='yes')
    body = [GLASS(f'Legal – {t}', [H(f'{n}. {t}', 'h2', 'gsh3', name='Section Title'), P(html, name='Section Text')],
                  pad=(32, 28, 22), radius=20, _element_id=a) for n, (a, t, html) in enumerate(secs, 1)]
    note = P('This document is provided for general information and does not create any rights beyond those stated. Questions? Email <a href="mailto:info@graphicsstormstudio.com">info@graphicsstormstudio.com</a>.',
             'gssmall', 'gsmuted', name='Footnote')
    main = SECTION('Legal Content', [ROW('Legal Row', [COL('TOC Column', [toc], w=30, wt=100), COL('Content Column', body + [note], w=70, wt=100, gap_=20)],
                                         gap_=40, stack='tablet', align='flex-start')], bg='b', pad=(72, 56, 40))
    return [hero, main, cta(ids)]

LEGAL = {'privacy': ('Privacy Policy', 'privacy-policy'), 'terms': ('Terms of Service', 'terms-of-service')}

PAGES = {  # key: (builder, title, original page id to replace at launch, slug)
 'home': (home, 'Home – Redesign', 21, None), 'about': (about, 'About Us – Redesign', 2738, None),
 'web': (lambda ids: service('web', ids), 'Website Development – Redesign', 5429, None),
 'seo': (lambda ids: service('seo', ids), 'Search Engine Optimization – Redesign', 5607, None),
 'smm': (lambda ids: service('smm', ids), 'Social Media Marketing – Redesign', 5516, None),
 'design': (lambda ids: service('design', ids), 'Graphics Designing – Redesign', 5562, None),
 'services': (services_hub, 'Services – Redesign', 4213, None),
 'work': (work, 'Our Work – Redesign', 4569, None), 'contact': (contact, 'Contact Us – Redesign', 2802, None),
}

def export():
    os.makedirs(OUT, exist_ok=True)
    files = {'gs-header.json': el.template_json('GS – Header (Sticky Glass)', 'header', el.finalize(header())),
             'gs-footer.json': el.template_json('GS – Footer', 'footer', el.finalize(footer())),
             'gs-cta-band.json': el.template_json('GS – CTA Band', 'section', el.finalize(cta_band())),
             'gs-section-title.json': el.template_json('GS – Section Title', 'section', el.finalize([C('Section Title Block', [section_head('Eyebrow text', 'Section Title With <span>Highlight</span>', 'Optional intro paragraph.')], content_width='boxed')])),
             'gs-service-card.json': el.template_json('GS – Service Card', 'section', el.finalize([GLASS('Service Card', [ICONBOX('fas fa-star', 'Service name', 'Short description.', '#')], hover=True)])),
             'gs-home.json': el.template_json('GS – Homepage', 'page', el.finalize(home()), {'template': 'elementor_header_footer', 'hide_title': 'yes'}),
             'gs-service-page.json': el.template_json('GS – Service Page Template', 'page', el.finalize(service('web')), {'template': 'elementor_header_footer', 'hide_title': 'yes'}),
             'gs-about.json': el.template_json('GS – About Us', 'page', el.finalize(about()), {'template': 'elementor_header_footer', 'hide_title': 'yes'}),
             'gs-our-work.json': el.template_json('GS – Our Work', 'page', el.finalize(work()), {'template': 'elementor_header_footer', 'hide_title': 'yes'}),
             'gs-contact.json': el.template_json('GS – Contact Us', 'page', el.finalize(contact()), {'template': 'elementor_header_footer', 'hide_title': 'yes'})}
    for n, d in files.items():
        json.dump(d, open(os.path.join(OUT, n), 'w'), ensure_ascii=False, indent=1)
        print('wrote', n, el.count(d['content']))

def menu():
    """New nav menu 'GSS Main' (old 'Main Menu' kept untouched). Items point at the ORIGINAL pages,
    whose URLs stay the same at launch."""
    import wp, push as P_
    if P_.IDS.get('menu'): return P_.IDS['menu']
    m = wp.req('wp/v2/menus', 'POST', {'name': 'GSS Main', 'slug': 'gss-main'})
    mid = m['id']; P_.IDS['menu'] = mid; P_._save()
    def add(title, page_id, parent=0, order=0):
        r = wp.req('wp/v2/menu-items', 'POST', {'title': title, 'menus': mid, 'parent': parent, 'menu_order': order,
                                                'object': 'page', 'object_id': page_id, 'type': 'post_type', 'status': 'publish'})
        return r['id']
    add('Home', 21, 0, 1); add('About Us', 2738, 0, 2)
    sv = add('Services', 4213, 0, 3)
    for i, (t, pid) in enumerate([('Website Development', 5429), ('Search Engine Optimization', 5607),
                                  ('Social Media Marketing', 5516), ('Graphic Design', 5562)], 1):
        add(t, pid, sv, 3 + i)
    add('Our Work', 4569, 0, 8); add('Contact Us', 2802, 0, 9)
    print('menu', mid); return mid

def push():
    import push as P_
    ids = P_.IDS
    menu()
    P_.part('header', 'header', 'GS – Header (Sticky Glass)', header())
    P_.part('footer', 'footer', 'GS – Footer', footer())
    P_.part('cta', 'section', 'GS – CTA Band', cta_band())
    for k, (fn, title, _, slug) in PAGES.items():
        P_.page(k, title, fn(ids))
    # Preview: show the new header/footer only on the redesign drafts (live pages unaffected)
    conds = [f'include/singular/page/{ids[k]}' for k in PAGES]
    print(json.dumps(__import__('wp').ability('elementor/manage-site-parts', {'operations': [
        {'action': 'update', 'post_id': ids['header'], 'conditions': conds},
        {'action': 'update', 'post_id': ids['footer'], 'conditions': conds}]}))[:400])

if __name__ == '__main__':
    export()
    if '--push' in sys.argv: push()
