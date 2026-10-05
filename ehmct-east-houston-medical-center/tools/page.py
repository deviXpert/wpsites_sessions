from el import *
from hf import PHONE, TEL, EMAIL, ADDR1, ADDR2, MAPS, header, footer

WHITE = {'ehwhite'}
SEC_PAD = dict(padding=dims(104, 20, 104, 20), padding_tablet=dims(76, 24, 76, 24), padding_mobile=dims(56, 16, 56, 16))

def section(title, children, anchor=None, boxed=True, **s):
    base = dict(content_width='boxed' if boxed else 'full', flex_direction='column',
                flex_align_items='center', flex_gap=gap(18))
    base.update(SEC_PAD); base.update(s)
    if anchor: base['_element_id'] = anchor
    return C(title, children, inner=False, **base)

# ================= 1. HERO =================
def pill(t):
    return BTN(t, '', 'Hero – Pill ' + t, style='outline-light', icon_=None, border_radius=dims(999),
               text_padding=dims(9, 20), background_color='rgba(7,23,46,0.22)', hover_animation='',
               button_background_hover_color='rgba(7,23,46,0.22)', hover_color='#FFFFFF', button_hover_border_color='rgba(255,255,255,0.8)',
               custom_css='selector .elementor-button{cursor:default}',
               typography_typography='custom', typography_font_family='Poppins', typography_font_weight='600',
               typography_font_size=px(12.3), typography_text_transform='uppercase',
               _element_width_mobile='initial', _element_custom_width_mobile=px(47, '%'), align_mobile='justify')

def hero_slide(n):
    tag = 'h1' if n == 1 else 'h2'
    return C('Hero – Slide %d' % n, [
        H('When Minutes Matter,<br>We’re Here for You.', 'p', 'ehh4', 'ehwhite', name='Hero – Kicker',
          _element_width='initial', _element_custom_width=px(100, '%')),
        H('Expert Emergency<br>Care <span>24/7</span>', tag, 'ehh1', 'ehwhite', name='Hero – Title',
          _element_width='initial', _element_custom_width=px(100, '%'), _margin=dims(4, 0, 10, 0)),
        pill('Same-Day Care'), pill('No Appointment'), pill('All Ages'), pill('Expert Care'),
    ], flex_direction='row', flex_wrap='wrap', flex_align_content='flex-end', flex_align_items='center',
       flex_justify_content='flex-start', flex_gap=gap(10, 12),
       min_height=px(844), min_height_tablet=px(760), min_height_mobile=px(700),
       padding=dims(120, 58, 205, 58), padding_tablet=dims(120, 36, 190, 36), padding_mobile=dims(110, 20, 150, 20),
       background_background='classic', background_image=img(['ehmc-hero-hospital-building', 'ehmc-hero-building-2', 'ehmc-hero-reception-3'][n - 1]),
       background_position='center center', background_size='cover', background_repeat='no-repeat',
       background_overlay_background='gradient', background_overlay_color='rgba(2,16,34,0.9)',
       background_overlay_color_stop=px(0, '%'), background_overlay_color_b='rgba(3,19,39,0.05)',
       background_overlay_color_b_stop=px(100, '%'), background_overlay_gradient_angle=px(90, 'deg'),
       background_overlay_gradient_angle_mobile=px(180, 'deg'),
       border_radius=dims(46), border_radius_mobile=dims(24),
       custom_css='@media(min-width:1025px){selector{padding-left:max(58px,calc((100% - 1440px)/2 - 0px)) !important;padding-right:max(58px,calc((100% - 1440px)/2)) !important}}')

hero_carousel = W('nested-carousel', 'Hero – Slider',
    carousel_items=[{'_id': uid(), 'slide_title': 'Slide #%d' % i} for i in (1, 2, 3)],
    slides_to_show='1', slides_to_show_tablet='1', slides_to_show_mobile='1', slides_to_scroll='1',
    autoplay='yes', autoplay_speed=6000, pause_on_hover='yes', pause_on_interaction='yes', infinite='',
    speed=600, arrows='', pagination='bullets', image_spacing_custom=px(0),
    dots_position='inside', dots_size=px(10), dots_color_inactive='rgba(255,255,255,0.7)',
    custom_css=('selector .swiper-pagination{position:absolute;bottom:auto !important;top:335px !important;width:auto !important;'
                'left:max(89px,calc((100% - 1440px)/2 + 31px)) !important;text-align:left;z-index:3}'
                'selector .swiper-pagination-bullet{margin:0 6px 0 0 !important;opacity:1;transition:width .3s}'
                'selector .swiper-pagination-bullet-active{width:24px !important;border-radius:6px;border:2px solid #fff}'
                '@media(max-width:1024px){selector .swiper-pagination{left:67px !important;top:300px !important}}'
                '@media(max-width:767px){selector .swiper-pagination{left:51px !important;top:237px !important}}'),
    g={'dots_color': col('secondary')})
hero_carousel['elements'] = [hero_slide(i) for i in (1, 2, 3)]

def avatar(k, first=False):
    return W('image', 'Hero – Patient Avatar', image=img(k), image_size='full',
             width=px(82), width_tablet=px(70), width_mobile=px(52), height=px(82), height_tablet=px(70), height_mobile=px(52), object_fit='cover',
             image_border_radius=dims(50, u='%'), image_box_shadow_box_shadow_type='yes',
             image_box_shadow_box_shadow=shadow(6, 16, 'rgba(7,26,49,0.16)'),
             _element_width='auto', _margin=dims(0, 0, 0, 62 if first else -31), _margin_tablet=dims(0, 0, 0, 30 if first else -29),
             _margin_mobile=dims(0, 0, 0, 6 if first else -22))
trust = C('Hero – Trust Tab', [
    W('image', 'Hero – Trust Icon', image=img('ehmc-icon-users'), image_size='full', width=px(44), width_mobile=px(34), _element_width='auto'),
    T('<p>Trusted by thousands in our community for fast care at our emergency clinic in Houston.</p>', 'ehlabel', 'accent', name='Hero – Trust Note',
      typography_font_weight='700', typography_font_size=px(14), typography_font_size_mobile=px(12), typography_line_height=px(1.5, 'em'),
      _element_width='initial', _element_custom_width=px(206), _element_custom_width_mobile=px(170),
      g={'text_color': col('accent')}, custom_css='selector p{margin:0;color:#0C1D3C}'),
    avatar('ehmc-patient-avatar-1-figma', True), avatar('ehmc-patient-avatar-2-figma'), avatar('ehmc-patient-avatar-3-figma'),
], flex_direction='row', flex_align_items='center', flex_justify_content='flex-start', flex_gap=gap(18), flex_gap_mobile=gap(10),
   flex_wrap='nowrap', width=px(626), width_tablet=px(560), width_mobile=px(100, '%'), min_height=px(142),
   padding=dims(32, 34, 28, 26), padding_mobile=dims(18, 12, 18, 12),
   background_background='classic', background_color='#FFFFFF', border_radius=dims(0, 48, 0, 42), border_radius_mobile=dims(0),
   custom_css='@media(min-width:1025px){selector{padding-left:max(26px,calc((100% - 1440px)/2)) !important;width:calc(600px + max(26px,calc((100% - 1440px)/2))) !important}}')
wait = W('icon-box', 'Hero – Average Wait Time Card', selected_icon=icon('far fa-clock', 'fa-regular'), view='default',
         position='left', position_mobile='inline-start', text_align_mobile='left', title_text='Average Wait Time', description_text='Under 15 Minutes', title_size='p',
         link={'url': '#contact', 'is_external': '', 'nofollow': ''},
         icon_size=px(28), icon_space=px(20), content_vertical_alignment='middle',
         title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_weight='600',
         title_typography_font_size=px(12), title_bottom_space=px(4),
         description_typography_typography='custom', description_typography_font_family='Poppins',
         description_typography_font_weight='700', description_typography_font_size=px(20),
         _background_background='classic', _background_color='rgba(41,58,110,0.88)',
         _border_border='solid', _border_width=dims(1), _border_color='rgba(255,255,255,0.2)', _border_radius=dims(16),
         _padding=dims(26, 60, 26, 26), _padding_mobile=dims(20, 60, 20, 20),
         _element_width='initial', _element_custom_width=px(410), _element_width_mobile='inherit',
         _margin=dims(0, 28, 34, 0), _margin_mobile=dims(0, 0, 14, 0),
         _background_hover_background='classic', _background_hover_color='rgba(41,58,110,1)',
         custom_css='@media(min-width:1025px){selector{margin-right:max(28px,calc((100% - 1440px)/2)) !important}}'
                    ' selector .elementor-icon-box-wrapper{position:relative}'
                    ' selector .elementor-icon-box-wrapper::after{content:"";position:absolute;right:-36px;top:50%;width:32px;height:32px;margin-top:-16px;border:1px solid rgba(255,255,255,.7);border-radius:50%;'
                    'background:#fff;-webkit-mask:none}'
                    ' selector .elementor-icon-box-wrapper::before{content:"";position:absolute;right:-27px;top:50%;width:14px;height:14px;margin-top:-7px;background:#fff;z-index:2;'
                    '-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22black%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cpath d=%22M5 12h14M13 6l6 6-6 6%22/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22black%22 stroke-width=%222%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22%3E%3Cpath d=%22M5 12h14M13 6l6 6-6 6%22/%3E%3C/svg%3E") center/contain no-repeat}'
                    ' selector .elementor-icon-box-wrapper::after{background:transparent}',
         g={'primary_color': col('secondary'), 'title_color': col('ehmuted'), 'description_color': col('ehwhite')})
hero_bottom = C('Hero – Bottom Bar', [trust, wait], flex_direction='row', flex_direction_mobile='column-reverse',
                flex_justify_content='space-between', flex_align_items='flex-end', flex_align_items_mobile='stretch',
                flex_gap=gap(0), padding=dims(0), padding_mobile=dims(0, 14, 0, 14), margin=dims(-142, 0, 0, 0), margin_mobile=dims(-110, 0, 0, 0), z_index=5)
hero = C('Hero', [hero_carousel, hero_bottom], inner=False, flex_gap=gap(0), padding=dims(8), padding_mobile=dims(8, 8, 0, 8))

# ================= 2. STATS =================
def stat(num, label, ic, pink=False, last=False):
    s = dict(selected_icon=icon(ic, 'fa-regular' if ic.startswith('far') else 'fa-solid'), view='stacked', shape='circle',
             position='left', position_mobile='inline-start', text_align_mobile='left', title_text=num, description_text=label, title_size='p', icon_size=px(16), icon_padding=px(0.9, 'em'),
             icon_space=px(14), content_vertical_alignment='middle', title_bottom_space=px(2),
             _flex_size='grow', _element_width='initial', _element_custom_width=px(22, '%'),
             _element_custom_width_tablet=px(46, '%'), _element_custom_width_mobile=px(100, '%'),
             _padding=dims(20, 18), _padding_mobile=dims(22, 20),
             title_typography_font_size_mobile=px(22), description_typography_font_size_mobile=px(13),
             g={'primary_color': col('ehpink' if pink else 'ehlight'), 'secondary_color': col('secondary' if pink else 'primary'),
                'title_typography_typography': typ('ehstat'), 'title_color': col('primary'),
                'description_typography_typography': typ('ehsmall'), 'description_color': col('text')})
    if not last:
        s.update(_border_border='solid', _border_width=dims(0, 1, 0, 0), _border_width_tablet=dims(0),
                 _border_color='#DFE5ED')
    return W('icon-box', 'Stats – ' + label, **s)
stats = section('Stats', [C('Stats – Card', [
    stat('24/7', 'Open', 'far fa-clock'), stat('99%', 'Satisfied Patients', 'fas fa-user-friends'),
    stat('10+', 'Years of Healing Excellence', 'fas fa-shield-alt'), stat('25,231+', 'Healthy Patients', 'far fa-heart', True, True)],
    flex_direction='row', flex_wrap='wrap', flex_gap=gap(0), flex_align_items='center',
    padding=dims(6), padding_mobile=dims(0), overflow='hidden',
    custom_css='@media(max-width:767px){selector > .elementor-widget:nth-child(even){background:var(--e-global-color-ehsurf)} selector > .elementor-widget{border:0 !important}}', background_background='classic', background_color='#FFFFFF',
    border_border='solid', border_width=dims(1), border_color='#DFE5ED', border_radius=dims(16),
    box_shadow_box_shadow_type='yes', box_shadow_box_shadow=CARD_SHADOW)],
    padding=dims(24, 20, 0, 20), padding_tablet=dims(24, 24, 0, 24), padding_mobile=dims(20, 16, 0, 16))

# ================= 3. CONDITIONS =================
CONDS = [('Chest Pain & Heart Concerns', 'Prompt evaluation for chest pain and possible heart emergencies.', 'condition-chest-pain-heart'),
         ('Abdominal Pain', 'Evaluation for sudden, severe, or persistent abdominal pain.', 'condition-abdominal-pain'),
         ('Breathing Difficulties', 'Urgent care for shortness of breath and breathing problems.', 'condition-breathing-difficulties'),
         ('Broken Bones & Fractures', 'On-site imaging and treatment for fractures and orthopedic injuries.', 'condition-broken-bones'),
         ('Allergic Reactions', 'Prompt treatment for severe or worsening allergic reactions.', 'condition-allergic-reactions'),
         ('High Fever', 'Evaluation and treatment for high or persistent fever.', 'condition-high-fever'),
         ('Severe Bleeding', 'Immediate care for uncontrolled bleeding and serious wounds.', 'condition-severe-bleeding'),
         ('Major Injuries & Trauma', 'Emergency evaluation and stabilization for serious injuries.', 'condition-major-injuries-trauma')]
# layout: 4 tab cards left, image centre, 4 right; tablet: image on top, 2-col cards; mobile: 4 cards, image, 4 cards (Figma mobile)
_rows = ''.join('selector .e-n-tab-title:nth-child(%d){grid-column:%d;grid-row:%d}' % (i + 1, 1 if i < 4 else 3, i % 4 + 1) for i in range(8))
_trows = ''.join('selector .e-n-tab-title:nth-child(%d){grid-column:%d;grid-row:%d}' % (i + 1, 1 + i % 2, 2 + i // 2) for i in range(8))
_mrows = ''.join('selector .e-n-tab-title:nth-child(%d){grid-column:1;grid-row:%d}' % (i + 1, i + 1 if i < 4 else i + 2) for i in range(8))
COND_CSS = ('selector .e-n-tabs{display:grid !important;grid-template-columns:1fr 29% 1fr;gap:20px}'
            'selector .e-n-tabs-heading{display:contents !important}'
            'selector .e-n-tabs-content{grid-column:2;grid-row:1 / span 4;display:block}'
            'selector .e-n-tab-title{flex-direction:column;justify-content:center;align-items:center;text-align:center;white-space:normal;'
            'background:#fff !important;border:1px solid var(--e-global-color-ehborder) !important;border-radius:16px !important;padding:26px 22px !important;'
            'cursor:pointer;transition:border-color .2s,background .2s,box-shadow .2s;min-height:138px;box-shadow:none !important}'
            'selector .e-n-tab-title:hover,selector .e-n-tab-title[aria-selected=true]{border-color:var(--e-global-color-primary) !important;'
            'background:var(--e-global-color-ehsurf) !important;box-shadow:0 15px 35px rgba(12,30,58,.12) !important}'
            'selector .e-n-tab-title-text{display:block;color:var(--e-global-color-primary) !important;font:600 18px/1.3 Poppins,sans-serif;letter-spacing:-.6px}'
            'selector .ehmc-cdesc{display:block;margin-top:8px;color:var(--e-global-color-text);font:400 13.4px/1.6 Poppins,sans-serif;letter-spacing:0}'
            'selector .e-n-tabs-content img{width:100%;height:616px;object-fit:cover;border-radius:16px;box-shadow:0 15px 35px rgba(12,30,58,.12)}'
            + _rows +
            '@media(max-width:1024px){selector .e-n-tabs{grid-template-columns:1fr 1fr}selector .e-n-tabs-content{grid-column:1 / span 2;grid-row:1}'
            + _trows + 'selector .e-n-tabs-content img{height:420px}}'
            '@media(max-width:767px){selector .e-n-tabs{grid-template-columns:1fr;gap:16px}selector .e-n-tabs-content{grid-column:1;grid-row:5}'
            + _mrows + 'selector .e-n-tabs-content img{height:auto;aspect-ratio:343/608}}')

cond_tabs = W('nested-tabs', 'Conditions – Tabs',
    tabs=[{'_id': uid(), 'tab_title': '%s<span class="ehmc-cdesc">%s</span>' % (t, d)} for t, d, _ in CONDS],
    tabs_direction='block-start', breakpoint_selector='none', custom_css=COND_CSS)
cond_tabs['elements'] = [C('Conditions – %s Image' % t, [
    W('image', 'Conditions – %s Illustration' % t, image=img(k), image_size='full', width=px(100, '%'))], padding=dims(0))
    for t, _, k in CONDS]

conditions = section('Conditions We Treat', section_head(
    'Immediate Treatment', 'Conditions <span>We Treat</span>',
    'From sudden illness to injuries, our team provides Houston immediate care 24/7 for a wide range of conditions.') + [
    C('Conditions – Grid', [cond_tabs], width=px(100, '%'), padding=dims(0), margin=dims(26, 0, 12, 0)),
    BTN('View All Conditions', '#conditions', 'Conditions – View All Button', align='center'),
], anchor='conditions', padding=dims(126, 20, 60, 20), padding_tablet=dims(80, 24, 50, 24), padding_mobile=dims(60, 16, 40, 16))

# ================= 4. TEAM =================
def doc(name, role, key, thumb, grow, wt, extra='', bg_key=None):
    tag = W('image-box', 'Team – %s Name Tag' % name, image=img(thumb), image_size='full', position='left', position_mobile='inline-start',
            text_align='left', text_align_mobile='left', title_text=name + extra, description_text=role, title_size='h3',
            image_space=px(9), content_vertical_alignment='middle', title_bottom_space=px(0),
            title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_weight='600',
            title_typography_font_size=px(14), title_typography_line_height=px(1.6, 'em'), description_typography_typography='custom',
            description_typography_font_family='Poppins', description_typography_font_size=px(12), description_typography_line_height=px(1.6, 'em'),
            _background_background='classic', _background_color='#FFFFFF', _border_border='solid', _border_width=dims(1),
            _border_color='rgba(41,58,110,0.5)', _border_radius=dims(5), _padding=dims(5, 8, 5, 3), _padding_mobile=dims(5, 8, 5, 3),
            _element_width='initial', _element_custom_width=px(100, '%'),
            custom_css='selector .elementor-image-box-img{width:51px !important;flex:0 0 51px} selector .elementor-image-box-img img{width:51px;height:46px;object-fit:cover;border-radius:2px} selector .elementor-image-box-title small{font-weight:400;font-size:11px;color:var(--e-global-color-text)} selector .elementor-image-box-wrapper{display:flex !important;align-items:center;text-align:left !important} selector .elementor-image-box-img{margin:0 9px 0 0 !important} selector .elementor-image-box-title{white-space:nowrap}',
            g={'title_color': col('accent'), 'description_color': col('accent')})
    # name tag floats over the bottom of the photo
    tag['settings'].update(_position='absolute', _offset_orientation_h='start', _offset_x=px(15),
                           _offset_orientation_v='end', _offset_y_end=px(10), _z_index=2)
    tag['settings']['custom_css'] += ' selector{width:calc(100% - 30px) !important;max-width:none !important}'
    photo = W('image', 'Team – %s Photo' % name, image=img(bg_key or key), image_size='full',
              width=px(100, '%'), height=px(365), height_tablet=px(365 if wt < 100 else 420), height_mobile=px(360),
              object_fit='cover', object_position='center center', image_border_radius=dims(10),
              _element_width='initial', _element_custom_width=px(100, '%'))
    return C('Team – ' + name, [photo, tag], flex_gap=gap(0), padding=dims(0), border_radius=dims(10), overflow='hidden',
             width=px(1), width_tablet=px(wt, '%'), width_mobile=px(100, '%'),
             _flex_size='custom', _flex_grow=grow, _flex_shrink=1, _flex_size_tablet='grow' if wt < 100 else 'none', _flex_size_mobile='none')

statcard = C('Team – 250+ Specialists Card', [
    H('250+', 'p', 'ehh2', 'ehwhite', 'center', name='Team – 250+', typography_font_size=px(96), typography_font_size_tablet=px(80),
      typography_font_size_mobile=px(64), typography_font_style='italic', typography_line_height=px(1.5, 'em'), typography_letter_spacing=px(0)),
    H('Medical Specialists', 'p', 'ehh2', 'ehwhite', 'center', name='Team – Specialists Label', typography_font_size=px(36),
      typography_font_size_mobile=px(26), typography_font_weight='400', typography_letter_spacing=px(0), typography_line_height=px(1.5, 'em'),
      _margin=dims(-6, 0, 0, 0)),
    BTN('Book Appointment', '#contact', 'Team – Book Appointment', align='center', text_padding=dims(13, 25), _margin=dims(24, 0, 0, 0)),
], flex_justify_content='center', flex_align_items='center', flex_gap=gap(0), min_height=px(365), padding=dims(40, 24),
   background_background='classic', background_color='#293A6E', border_radius=dims(10),
   width=px(1), width_tablet=px(100, '%'), width_mobile=px(100, '%'),
   _flex_size='custom', _flex_grow=582, _flex_shrink=1, _flex_size_tablet='none', _flex_size_mobile='none')

def half(c, last_mobile=False):
    if last_mobile: c['settings']['_flex_order_mobile'] = 'end'
    # equal halves regardless of image intrinsic width
    c['settings'].update(width=px(50, '%'), _flex_size='custom', _flex_grow=0, _flex_shrink=1)
    c['settings']['custom_css'] = c['settings'].get('custom_css', '') + ' selector{min-width:0}'
    return c

row = lambda name, kids, g=20: C('Team – ' + name, kids, flex_direction='row', flex_wrap='nowrap', flex_wrap_tablet='wrap',
                                 flex_gap=gap(g, 20), width=px(100, '%'), padding=dims(0))
team = section('Meet Our Medical Team', section_head(
    '24+ Experienced Physicians', 'Meet Our Medical Team',
    'At EHMCT, our experienced staff are committed to providing excellence in urgent care.') + [
    C('Team – Grid', [
        row('Row 1', [doc('Dr. Adriano Goffi', 'ER Physician', 'dr-adriano-goffi', 'dr-goffi-thumb', 282, 48, ' <small>(Director)</small>'),
                      doc('Dr. Darshan Anandu', 'Gastroenterologist', 'dr-darshan-anandu', 'dr-anandu-thumb', 282, 48),
                      doc('Dr. Shariq Khan', 'ER Physician', 'dr-shariq-khan', 'dr-khan-thumb', 582, 100)]),
        row('Row 2', [half(statcard, last_mobile=True),
                      half(doc('Dr. Moses Wilcox', 'Urologist', 'dr-moses-wilcox', 'dr-wilcox-thumb', 582, 100, bg_key='dr-moses-wilcox-crop'))]),
    ], flex_gap=gap(20), width=px(100, '%'), padding=dims(0), margin=dims(26, 0, 0, 0)),
], anchor='team', padding=dims(80, 20, 60, 20))

# ================= 5. DEPARTMENTS =================
DEPTS = [('Emergency Care', 'Immediate emergency treatment, available 24/7.', '24/7 evaluation and treatment for urgent medical emergencies, with an experienced team ready day and night.', 'dept-emergency-care'),
         ('Diagnostic Imaging', 'On-site imaging for fast diagnostic evaluation.', 'CT scans, X-rays, and ultrasound are available on-site to support fast, accurate emergency diagnosis.', 'dept-diagnostic-imaging'),
         ('Laboratory Services', 'On-site testing to support timely medical decisions.', 'On-site testing delivers rapid, accurate results that help our physicians make timely treatment decisions.', 'dept-laboratory-services'),
         ('Trauma Care', 'Focused care for serious injuries and emergencies.', 'Specialized evaluation, stabilization, and treatment for serious injuries in a fully equipped emergency setting.', 'dept-trauma-care'),
         ('Cardiac Care', 'Prompt evaluation and care for heart-related emergencies.', 'Rapid testing and advanced treatment for chest pain, irregular heartbeat, and other urgent cardiac concerns.', 'dept-cardiac-care'),
         ('Pediatric Emergency', 'Specialized care for children with urgent medical needs.', 'Family-centered emergency care for infants, children, and adolescents in a calm, supportive environment.', 'dept-pediatric-emergency')]

SVG = {  # simple line icons for the flip-box back (white stroke on the navy circle)
 'Emergency Care': '<path d="M7 18v-6a5 5 0 0 1 10 0v6"/><path d="M5 21h14"/><path d="M12 3v1M4.5 6.5l.7.7M19.5 6.5l-.7.7"/>',
 'Diagnostic Imaging': '<rect x="4" y="4" width="16" height="16" rx="3"/><circle cx="12" cy="12" r="4"/>',
 'Laboratory Services': '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3"/><path d="M7.5 15h9"/>',
 'Trauma Care': '<circle cx="12" cy="5" r="2"/><path d="M12 7v7M8 10h8M10 21l2-7 2 7"/>',
 'Cardiac Care': '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
 'Pediatric Emergency': '<circle cx="12" cy="5.5" r="2.5"/><path d="M12 8v6M9 11h6M10 20l2-6 2 6"/>'}
FLIP_CSS = (
 'selector .elementor-flip-box__front .elementor-flip-box__layer__overlay{background:linear-gradient(180deg,rgba(41,58,110,0) 35%,rgba(41,58,110,.9) 100%) !important}'
 'selector .elementor-flip-box__back{border:1px solid var(--e-global-color-ehborder)}'
 'selector .ehmc-ic{width:32px;height:32px;border-radius:50%;background:var(--e-global-color-primary);display:flex;align-items:center;justify-content:center;margin-bottom:18px}'
  'selector .ehmc-lbl{display:block;color:var(--e-global-color-secondary);font:700 10px/1.4 Poppins,sans-serif;letter-spacing:.3px;text-transform:uppercase;margin-bottom:8px}'
 'selector .ehmc-t{display:block;color:var(--e-global-color-primary);font:700 24px/1.05 Gelasio,Georgia,serif;margin-bottom:12px}'
 'selector .ehmc-hint{display:block;color:var(--e-global-color-primary);font:600 11px/1.4 Poppins,sans-serif;margin-top:14px}')

def flip(t, front, back, key):
    back_html = ('<span class="ehmc-ic" aria-hidden="true"></span>'
                 '<span class="ehmc-lbl">Department</span><span class="ehmc-t">%s</span>%s'
                 '<span class="ehmc-hint">Move away or tap to turn</span>') % (t, back)
    from urllib.parse import quote
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="1.9" '
           'stroke-linecap="round" stroke-linejoin="round">%s</svg>') % SVG[t]
    icon_css = ('selector .ehmc-ic::before{content:"";width:17px;height:17px;background:#fff;'
                '-webkit-mask:url("data:image/svg+xml,%s") center/contain no-repeat;mask:url("data:image/svg+xml,%s") center/contain no-repeat}') % (quote(svg), quote(svg))
    return W('flip-box', 'Departments – %s Flip Box' % t,
             graphic_element='none', title_text_a=t, description_text_a=front,
             graphic_element_b='none', title_text_b='', description_text_b=back_html,
             button_text='', height=px(379), height_mobile=px(360), border_radius=px(16),
             flip_effect='flip', flip_direction='left', flip_3d='yes',
             background_a_background='classic', background_a_image=img(key), background_a_size='cover',
             background_a_position='center center', background_overlay_a='rgba(41,58,110,0.5)',
             background_b_background='classic', background_b_color='#FFFFFF',
             padding_a=dims(24, 22), alignment_a='left', vertical_position_a='bottom',
             padding_b=dims(28, 22), alignment_b='left', vertical_position_b='middle',
             title_spacing_a=px(8),
             description_typography_a_typography='custom', description_typography_a_font_family='Poppins',
             description_typography_a_font_weight='600', description_typography_a_font_size=px(12),
             description_typography_b_typography='custom', description_typography_b_font_family='Poppins',
             description_typography_b_font_size=px(12), description_typography_b_line_height=px(1.7, 'em'),
             custom_css=FLIP_CSS + icon_css,
             g={'title_typography_a_typography': typ('ehserif'), 'title_color_a': col('ehwhite'), 'description_color_a': col('ehwhite'),
                'description_color_b': col('text')})

dept_carousel = W('nested-carousel', 'Departments – Carousel',
    carousel_items=[{'_id': uid(), 'slide_title': d[0]} for d in DEPTS],
    slides_to_show='4', slides_to_show_tablet='2', slides_to_show_mobile='1', slides_to_scroll='1',
    autoplay='', infinite='yes', speed=500, arrows='yes', pagination='', image_spacing_custom=px(18),
    arrows_position='inside', arrow_size=px(14), _element_width='initial', _element_custom_width=px(100, '%'),
    _margin=dims(56, 0, 0, 0),
    custom_css='selector .elementor-swiper-button{top:-56px !important;bottom:auto;transform:none;width:38px;height:38px;border-radius:50%;'
               'border:1px solid var(--e-global-color-ehborder);background:#fff;display:flex;align-items:center;justify-content:center;transition:.2s}'
               'selector .elementor-swiper-button-prev{left:auto !important;right:48px !important;inset-inline-start:auto !important}'
               'selector .elementor-swiper-button-next{right:0 !important;inset-inline-end:0 !important}'
               'selector .elementor-swiper-button:hover{background:var(--e-global-color-ehlight);border-color:var(--e-global-color-primary)}',
    g={'arrow_normal_color': col('primary'), 'arrow_hover_color': col('primary')})
dept_carousel['elements'] = [C('Departments – Slide ' + d[0], [flip(*d)], padding=dims(0)) for d in DEPTS]
dept_carousel['settings']['hide_mobile'] = 'hidden-mobile'
dept_list = C('Departments – Mobile List', [dict(flip(*d), id=uid()) for d in DEPTS], flex_gap=gap(20), flex_align_items='center',
              padding=dims(0), width=px(100, '%'), hide_desktop='hidden-desktop', hide_tablet='hidden-tablet',
              custom_css='selector .elementor-widget-flip-box{width:285px;max-width:100%}')
departments = section('Care Under One Roof', section_head(
    'Our Departments', 'Care Under <span>One Roof</span>',
    'Advanced technology and experienced professionals, ready to deliver comprehensive urgent care centers 24 hours a day.') + [
    dept_carousel, dept_list, BTN('Explore Departments', '#departments', 'Departments – Explore Button', align='center', _margin=dims(20, 0, 0, 0)),
], anchor='departments', padding=dims(80, 20, 90, 20))

# ================= 6. REVIEWS =================
REV = [('The staff was incredible—fast, kind, and professional. I felt safe and well cared for during a very scary situation.', 'Sarah'),
       ('Short wait time, excellent care, and everyone was so compassionate. Highly recommend this ER.', 'Michael'),
       ('They treated my son with such patience and care. Truly grateful for the amazing team.', 'Jennifer')]
reviews_left = C('Reviews – Intro', [
    EYEBROW('Patient Reviews', align='left'),
    H('Trusted by<br>Houston<br>Families', 'h2', 'ehh2', 'primary', 'left', name='Reviews – Title',
      _element_width='initial', _element_custom_width=px(100, '%')),
    T('<p>Real stories. Real care. Real people.</p>', name='Reviews – Tagline', _element_width='initial', _element_custom_width=px(100, '%')),
    H('4.9<small style="font-size:20px;font-weight:600"> / 5</small>', 'p', 'ehh2', 'primary', name='Reviews – Rating Score',
      typography_font_size=px(48), typography_letter_spacing=px(-1), _element_width='auto'),
    W('star-rating', 'Reviews – Stars', rating_scale='5', rating=5, star_style='star_unicode', unmarked_star_style='outline',
      title='Based on 1,200+ reviews', icon_size=px(16), icon_space=px(3), title_gap=px(8), _element_width='auto',
      title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_size=px(12),
      g={'stars_color': col('secondary'), 'title_color': col('text')}),
], flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(14, 12),
   width=px(34, '%'), width_tablet=px(100, '%'))
reviews_widget = W('shortcode', 'Reviews – Google Reviews (Trustindex)', shortcode='[trustindex no-registration=google]',
    _flex_size='grow', _element_width='initial', _element_custom_width=px(60, '%'), _element_custom_width_tablet=px(100, '%'))
reviews = section('Trusted by Houston Families', [reviews_left, reviews_widget], anchor='reviews',
                  flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(40, 30),
                  padding=dims(86, 20, 86, 20), background_background='classic', background_color='#EDF3FA',
                  g={'background_color': col('ehlight')})

# ================= 7. LOCATIONS =================
def loc(city, a1, a2, phone, tel, maps_addr, directions):
    return C('Locations – %s Card' % city, [
        W('icon-box', 'Locations – %s Title' % city, selected_icon=icon('fas fa-map-marker-alt'), view='stacked', shape='circle',
          position='left', position_mobile='inline-start', text_align_mobile='left', title_text=city, description_text='', title_size='h3', icon_size=px(16), icon_padding=px(0.9, 'em'),
          icon_space=px(14), content_vertical_alignment='middle', title_typography_font_size=px(24),
          g={'primary_color': col('ehpink'), 'secondary_color': col('secondary'), 'title_color': col('primary'),
             'title_typography_typography': typ('ehh3')}),
        T('<p><strong style="color:#293A6E;font-size:16px">East Houston Medical Center</strong></p><p>%s<br>%s</p>'
          '<p><strong><a href="%s">☎ %s</a></strong></p>' % (a1, a2, tel, phone), 'ehsmall', name='Locations – %s Address' % city,
          typography_font_size=px(14)),
        W('google_maps', 'Locations – %s Map (placeholder embed)' % city, address=maps_addr, zoom=px(13), height=px(200),
          _border_radius=dims(8), _border_border='solid', _border_width=dims(1), _border_color='#DFE5ED',
          custom_css='selector iframe{border-radius:8px}'),
        BTN('Get Direction', directions, 'Locations – %s Directions Link' % city, style='text', icon_=ARROW,
            background_color='rgba(0,0,0,0)', text_padding=dims(4, 0), button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(0, 0, 'rgba(0,0,0,0)'), button_background_hover_color='rgba(0,0,0,0)',
            hover_animation='', typography_typography='custom', typography_font_family='Poppins',
            typography_font_weight='600', typography_font_size=px(14),
            g={'button_text_color': col('primary'), 'hover_color': col('secondary')}),
    ], flex_gap=gap(12), padding=dims(24), padding_mobile=dims(18), background_background='classic', background_color='#F6F8FB',
       border_border='solid', border_width=dims(1), border_color='#DFE5ED', border_radius=dims(10),
       border_hover_border='solid', border_hover_width=dims(1), border_hover_color='#293A6E',
       box_shadow_hover_box_shadow_type='yes', box_shadow_hover_box_shadow=CARD_SHADOW,
       width=px(48, '%'), width_mobile=px(100, '%'), _flex_size='grow')

locations = section('Locations', section_head('Our Locations', 'Find an East Houston Medical Center <span>Near You</span>') + [
    C('Locations – Cards', [
        loc('Houston', '15149 Wallisville Rd,', 'Houston TX, 77049', PHONE, TEL, '15149 Wallisville Rd, Houston, TX 77049', MAPS),
        loc('Baytown', 'Coming soon', 'Baytown TX', PHONE, TEL, '1601 Garth Rd, Baytown, TX 77530',
            'https://www.google.com/maps/dir/?api=1&destination=1601+Garth+Rd+Baytown+TX+77530'),
    ], flex_direction='row', flex_wrap='wrap', flex_gap=gap(20), width=px(100, '%'), padding=dims(0),
       margin=dims(26, 0, 0, 0)),
], anchor='locations', padding=dims(90, 20, 90, 20))
# section title width
locations['elements'][1]['settings'].update(_element_width='initial', _element_custom_width=px(780),
                                            _element_custom_width_tablet=px(100, '%'))

# ================= 8. FAQ =================
FAQ = [('Do I need an appointment?', 'No. Walk-ins are welcome 24 hours a day, seven days a week for emergency and urgent medical needs.'),
       ('Are you open on holidays?', 'Yes. Our emergency room is open 24/7, 365 days a year — including weekends and all holidays.'),
       ('What insurance do you accept?', 'We accept most major insurance plans. Please call us at %s to confirm your coverage — we will never delay emergency care because of insurance.' % PHONE),
       ('How quickly will I be seen?', 'Our average wait time is under 15 minutes. Patients with life-threatening conditions are always seen first.'),
       ('When should I visit an emergency room?', 'Come in for chest pain, trouble breathing, severe bleeding, high fever, serious injuries, or any symptom that feels urgent. If it is life-threatening, call 911.')]
faq_acc = W('nested-accordion', 'FAQ – Accordion',
    items=[{'_id': uid(), 'item_title': q} for q, _ in FAQ], default_state='expanded', max_items_expended='one',
    accordion_item_title_icon=icon('fas fa-plus'), accordion_item_title_icon_active=icon('fas fa-times'),
    accordion_item_title_position_horizontal='stretch', accordion_item_title_icon_position='end',
    accordion_item_title_space_between=px(0), accordion_item_title_distance_from_content=px(0),
    accordion_background_normal_background='classic', accordion_background_normal_color='#FFFFFF',
    accordion_border_normal_border='solid', accordion_border_normal_width=dims(0, 0, 1, 0),
    accordion_border_normal_color='#DFE5ED', accordion_border_hover_border='solid',
    accordion_border_hover_width=dims(0, 0, 1, 0), accordion_border_hover_color='#DFE5ED',
    accordion_border_active_border='solid', accordion_border_active_width=dims(0, 0, 0, 0),
    accordion_border_active_color='#DFE5ED', accordion_padding=dims(20, 6, 20, 0),
    content_border_border='solid', content_border_width=dims(0, 0, 1, 0), content_border_color='#DFE5ED',
    content_padding=dims(0, 6, 20, 0),
    title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_weight='600',
    title_typography_font_size=px(16), icon_size=px(10),
    custom_css='selector .e-n-accordion-item-title-icon{width:24px;height:24px;border:1px solid #E5C8CB;border-radius:50%;justify-content:center;align-items:center}',
    g={'title_normal_color': col('primary'), 'title_hover_color': col('secondary'), 'title_active_color': col('primary'),
       'icon_color': col('secondary'), 'icon_active_color': col('secondary')})
faq_acc['elements'] = [C('FAQ – Answer: ' + q, [T('<p>%s</p>' % a, name='FAQ – Answer Text')], padding=dims(0)) for q, a in FAQ]
faq = section('FAQ', [
    W('image', 'FAQ – Image', image=img('ehmc-faq-emergency-nurse'), image_size='full', width=px(100, '%'),
      height=px(520), height_tablet=px(420), height_mobile=px(280), object_fit='cover', image_border_radius=dims(16),
      _element_width='initial', _element_custom_width=px(40, '%'), _element_custom_width_tablet=px(100, '%')),
    C('FAQ – Content', [
        EYEBROW('FAQ', align='left'),
        H('Frequently Asked<br>Questions', 'h2', 'ehh2', 'primary', 'left', name='FAQ – Title'),
        T('<p>Get quick answers about our emergency care and emergency room services.</p>', name='FAQ – Intro'),
        faq_acc,
    ], flex_gap=gap(12), _flex_size='grow', width=px(55, '%'), width_tablet=px(100, '%')),
], anchor='faq', flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(28, 36),
   padding=dims(100, 20, 100, 20))

# ================= 9. CTA / CONTACT =================
def perk(t, d, ic):
    return W('icon-box', 'Contact – ' + t, selected_icon=icon(ic, 'fa-regular' if ic.startswith('far') else 'fa-solid'),
             view='default', position='left', position_mobile='inline-start', text_align_mobile='left', title_text=t, description_text=d, title_size='p', icon_size=px(18), icon_space=px(10),
             title_bottom_space=px(2), _element_width='initial', _element_custom_width=px(30, '%'),
             _element_custom_width_mobile=px(100, '%'), _flex_size='grow',
             title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_weight='700',
             title_typography_font_size=px(12.8), description_typography_typography='custom',
             description_typography_font_family='Poppins', description_typography_font_size=px(11),
             g={'primary_color': col('ehmuted'), 'title_color': col('ehwhite'), 'description_color': col('ehmuted')})

form = W('form', 'Contact – Request a Call Form', form_name='Request a Call',
    form_fields=[
        {'_id': uid(), 'custom_id': 'name', 'field_type': 'text', 'field_label': 'Full Name', 'placeholder': '', 'required': 'true', 'width': '50', 'width_mobile': '100'},
        {'_id': uid(), 'custom_id': 'phone', 'field_type': 'tel', 'field_label': 'Phone Number', 'placeholder': '', 'required': 'true', 'width': '50', 'width_mobile': '100'},
        {'_id': uid(), 'custom_id': 'email', 'field_type': 'email', 'field_label': 'Email Address', 'placeholder': '', 'required': 'true', 'width': '100'},
        {'_id': uid(), 'custom_id': 'message', 'field_type': 'textarea', 'field_label': 'How Can We Help?', 'placeholder': '', 'rows': 3, 'width': '100'},
    ],
    show_labels='yes', input_size='md', button_text='Request a Call', button_size='md', button_width='100',
    selected_button_icon=ARROW, button_icon_align='row-reverse', button_icon_indent=px(10),
    submit_actions=['email', 'collect_submissions'], email_subject='New "Request a Call" from EHMC website',
    success_message='Thank you! Our team will call you back shortly.',
    column_gap=px(14), row_gap=px(16), label_spacing=px(8), field_border_radius=dims(10), field_border_width=dims(1),
    button_border_radius=dims(10), button_text_padding=dims(15, 20),
    button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(12, 28, 'rgba(158,63,66,0.26)'),
    g={'label_color': col('primary'), 'field_text_color': col('accent'), 'field_background_color': col('ehsurf'),
       'field_border_color': col('ehborder'), 'button_background_color': col('secondary'),
       'button_background_hover_color': col('ehreddk'), 'button_text_color': col('ehwhite'),
       'label_typography_typography': typ('ehlabel'), 'button_typography_typography': typ('ehbtn')})
form['settings']['label_typography_font_size'] = px(12)

contact = section('Need Emergency Care Now', [
    C('Contact – Intro', [
        EYEBROW('Get in Touch', align='left'),
        H('Need Emergency Care Now?', 'h2', 'ehh2', 'ehwhite', 'left', name='Contact – Title',
          _element_width='initial', _element_custom_width=px(100, '%')),
        T('<p>We’re open 24/7 and ready when you need us.</p>', color='ehmuted', name='Contact – Tagline',
          _element_width='initial', _element_custom_width=px(100, '%'), _margin=dims(0, 0, 8, 0)),
        dict(BTN(PHONE, TEL, 'Contact – Call Button', icon_=icon('fas fa-phone-alt')), ),
        BTN('Get Directions', MAPS, 'Contact – Directions Button', style='outline-light', is_external='on'),
        W('divider', 'Contact – Divider', weight=px(1), color='rgba(255,255,255,0.2)', gap=px(6), _element_width='initial', _element_custom_width=px(100, '%')),
        perk('Open 24/7', '365 days a year', 'far fa-clock'),
        perk('Convenient Location', 'Houston, Texas', 'fas fa-map-marker-alt'),
        perk('Walk-Ins Welcome', 'No appointment', 'fas fa-walking'),
    ], flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_gap=gap(14, 16),
       width=px(52, '%'), width_tablet=px(100, '%'), _flex_size='grow'),
    C('Contact – Form Card', [
        H('Request a Call', 'h3', 'ehh3', 'primary', name='Contact – Form Title', typography_font_size=px(20),
          typography_font_weight='700'),
        T('<p>We’ll get back to you as soon as possible. Do not use this form for life-threatening emergencies.</p>',
          'ehsmall', name='Contact – Form Note', typography_font_size=px(13.1), _margin=dims(-6, 0, 6, 0)),
        form,
    ], flex_gap=gap(12), padding=dims(26, 26, 30, 26), padding_mobile=dims(22, 18, 24, 18),
       background_background='classic', background_color='#FFFFFF', border_radius=dims(16),
       box_shadow_box_shadow_type='yes', box_shadow_box_shadow=shadow(24, 70, 'rgba(4,38,72,0.22)'),
       width=px(40, '%'), width_tablet=px(100, '%')),
], anchor='contact', flex_direction='row', flex_wrap='wrap', flex_align_items='center', flex_justify_content='space-between',
   flex_gap=gap(40), background_background='gradient', background_color='#293A6E', background_color_b='#495D98',
   background_gradient_angle=px(135, 'deg'))
contact['elements'][0]['elements'][3]['settings']['icon_align'] = 'row'
contact['elements'][0]['elements'][4]['settings']['link']['is_external'] = 'on'

PAGE = [hero, stats, conditions, team, departments, reviews, locations, faq, contact]

if __name__ == '__main__':
    import sys
    print('containers/widgets:', count(PAGE))
    common = {'template': 'elementor_header_footer'}
    ps = {'hide_title': 'yes'}
    if 'page' in sys.argv:
        put(32, PAGE, {'_elementor_page_settings': ps}, dict(common)); regen(32)
    if 'qa' in sys.argv:
        put(int(sys.argv[-1]), [header] + PAGE + [footer], {'_elementor_page_settings': ps}, {'template': 'elementor_canvas'}); regen(int(sys.argv[-1]))
