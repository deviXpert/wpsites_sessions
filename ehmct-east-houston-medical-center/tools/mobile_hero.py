"""Mobile-only (<=767px) patch of the live home hero (32) and header (33) to match Figma "Mobile view" 266:2.

Fetches live data and only sets *_mobile keys / appends an @media(max-width:767px) block to custom CSS,
so desktop/tablet and the user's editor changes are kept. Safe to re-run (CSS blocks are replaced by marker).
usage: python3 mobile_hero.py [hero|header|all]
"""
import re, sys
from patch import fetch, save, find, titled
from el import px, dims, img, shadow, W, C, icon, col

M = '/*m-figma*/'  # marker for the appended mobile CSS block
MOBILE_IMG = 'https://hotpink-lobster-615998.hostingersite.com/wp-content/uploads/2026/10/ehmc-hero-building-mobile.webp'


def add_css(s, css):
    cur = re.sub(re.escape(M) + r'.*?' + re.escape(M), '', s.get('custom_css', ''), flags=re.S)
    s['custom_css'] = (cur + ' ' + M + '@media(max-width:767px){' + css + '}' + M).strip()


def dm(t, r, b, l, u='px'):
    return {'unit': u, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}


# Figma image crops per slide: background width and offset relative to the slide (slide = card minus 4px border)
CROPS = {'Hero – Slide 1': (1271, -249, -94), 'Hero – Slide 2': (365, -4, -4),  # slide 2 mobile image is already a 365x753 crop
         'Hero – Slide 3': (1129, -229, 0), 'Hero – Slide 4': (1129, -442, -4)}
OVERLAY = ('linear-gradient(0deg,rgba(6,40,67,.2) 0%,rgba(12,50,105,0) 112%),'
           'linear-gradient(90deg,rgba(2,16,34,.81) 0%,rgba(3,19,39,.67) 32%,rgba(3,19,39,.2) 62%,rgba(3,19,39,.04) 100%)')
ARROW_MOBILE = ('selector .elementor-icon-box-wrapper::after{right:-50.7px;width:36px;height:36px;margin-top:-18px;'
                'border:.8px solid rgba(255,255,255,.45)}'
                'selector .elementor-icon-box-wrapper::before{right:-41.2px;width:17px;height:17px;margin-top:-8.5px}')
BURGER = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23141B34' "
          "stroke-width='1.5' stroke-linecap='round'%3E%3Cpath d='M4 5h16M10 12h10M4 19h16'/%3E%3C/svg%3E")


def hero(pid=32):
    doc = fetch(pid)
    d = doc['data']
    h = find(d, titled('Hero'))
    s = h['settings']
    # the white card (Figma frame 14px from the edges, 4px white inside stroke = hero padding)
    s['padding_mobile'] = dm(19, 18, 4, 18)
    # Figma card outline: 4px white(.94) stroke over the photo -> light grey curved border around the whole card
    add_css(s, 'selector{position:relative}selector::after{content:"";position:absolute;top:15px;left:14px;right:14px;bottom:0;'
               'border:4px solid #F1F2F3;border-radius:30px;pointer-events:none;z-index:6}')

    car = find(d, titled('Hero – Slider'))
    car['settings']['custom_css'] = re.sub(r'@media\(max-width:767px\)\{selector \.swiper-pagination\{left:51px !important;top:237px !important\}\}', '',
                                           car['settings']['custom_css'])
    add_css(car['settings'],
            'selector .swiper-pagination{left:11.5px !important;top:160.2px !important;transform:none !important;line-height:0;display:flex;gap:4.8px}'
            'selector .swiper-pagination-bullet{width:10.8px !important;height:10.8px !important;margin:0 !important;'
            'box-sizing:border-box;background:rgba(255,255,255,.76) !important;border:1.8px solid rgba(255,255,255,.72) !important}'
            'selector .swiper-pagination-bullet-active{width:22.8px !important;border-radius:6px;background:#9F3135 !important}')

    for slide in car['elements']:
        ss = slide['settings']
        ss.update(padding_mobile=dm(196, 11, 0, 11.5), min_height_mobile=px(658),
                  flex_align_content_mobile='flex-start', flex_justify_content_mobile='flex-start',
                  flex_gap_mobile={'column': '9.5', 'row': '9', 'isLinked': False, 'unit': 'px', 'size': 9.5},
                  border_radius_mobile=dm(26, 26, 0, 0))
        crop = CROPS.get(ss.get('_title'))
        if crop:
            w, x, y = crop
            ss.update(background_size_mobile='initial', background_bg_width_mobile=px(w),
                      background_position_mobile='initial', background_xpos_mobile=px(x), background_ypos_mobile=px(y))
            if ss.get('_title') == 'Hero – Slide 1':  # Figma uses the clean photo (live desktop image has a baked-in gradient)
                ss['background_image_mobile'] = {'id': 968, 'url': MOBILE_IMG, 'source': 'library', 'alt': '', 'size': ''}
        add_css(ss, 'selector::before{background-image:' + OVERLAY + ' !important;opacity:1 !important}')
        for w in slide['elements']:
            t = w['settings'].get('_title', '')
            if t == 'Hero – Kicker':
                add_css(w['settings'], 'selector .elementor-heading-title{font-size:16px;line-height:24px;letter-spacing:0}')
            elif t == 'Hero – Title':
                w['settings']['_margin_mobile'] = dm(5.5, 0, 28, 0)
                add_css(w['settings'], 'selector .elementor-heading-title{font-size:40px;line-height:40px;letter-spacing:0}')
            elif t.startswith('Hero – Pill'):
                w['settings'].update(text_padding_mobile=dm(7.4, 6, 8, 6), border_width_mobile=dims(0.93),
                                     typography_font_size_mobile=px(11.38), typography_line_height_mobile=px(18))
                add_css(w['settings'], 'selector{width:calc(50% - 4.75px) !important;max-width:none}')

    bar = find(d, titled('Hero – Bottom Bar'))
    bar['settings'].update(margin_mobile=dm(-110.1, 0, 0, 0),
                           flex_gap_mobile={'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px', 'size': 0})

    card = find(d, titled('Hero – Average Wait Time Card'))
    cs = card['settings']
    cs.update(_padding_mobile=dm(25.9, 69.5, 25.9, 22), _margin_mobile=dm(0, 10.8, 18, 11.5),
              _border_radius_mobile=dims(8.16), _border_width_mobile=dims(0.8),
              icon_size_mobile=px(33), icon_space_mobile=px(18),
              title_typography_font_size_mobile=px(11.38), title_typography_line_height_mobile=px(16.3),
              title_bottom_space_mobile=px(2.4),
              description_typography_font_size_mobile=px(15.17), description_typography_line_height_mobile=px(19.6))
    add_css(cs, 'selector{width:auto !important;align-self:stretch}' + ARROW_MOBILE)

    tab = find(d, titled('Hero – Trust Tab'))
    tab['settings'].update(padding_mobile=dm(17.1, 9.5, 15, 13.9), min_height_mobile=px(87),
                           flex_gap_mobile={'column': '9.6', 'row': '9.6', 'isLinked': True, 'unit': 'px', 'size': 9.6},
                           border_radius_mobile=dm(0, 0, 26, 26))
    find(d, titled('Hero – Trust Icon'))['settings']['width_mobile'] = px(23.5)
    note = find(d, titled('Hero – Trust Note'))
    note['settings'].update(typography_font_size_mobile=px(10), typography_line_height_mobile=px(12),
                            _element_custom_width_mobile=px(174))
    add_css(note['settings'], 'selector{flex-shrink:0}selector p{letter-spacing:0;word-spacing:0}')
    avatars = find(d, titled('Hero – Patient Avatar'), many=True)
    for i, a in enumerate(avatars):
        # Figma crops (square, no baked-in ring); ring + shadow are CSS borders now
        a['settings'].update(image=img('patient_avatar_%d_v2' % (i + 1)), width_mobile=px(43.8), height_mobile=px(43.8),
                             object_fit='cover', image_border_border='solid', image_border_color='#FFFFFF',
                             image_border_width=dims(5), image_border_width_tablet=dims(4.3), image_border_width_mobile=dims(2.67),
                             image_box_shadow_box_shadow=shadow(3.2, 8.55, 'rgba(7,26,49,0.16)'),
                             _margin_mobile=dm(0, 0, 0, 0 if i == 0 else -16.5))  # -6.9 overlap minus the strip's 9.6 gap
        if i == 0:
            add_css(a['settings'], 'selector{margin-left:auto !important}')
    stats(doc)
    conditions(doc)
    save(doc)


STATS_CSS = ('selector{display:grid !important;grid-template-columns:171fr 180fr;align-items:stretch !important;box-shadow:0 18px 50px rgba(16,37,74,.11) !important}'
             'selector > .elementor-widget{width:auto !important;max-width:none !important;border:0 !important;margin:0 !important}'
             'selector > .elementor-widget:nth-child(odd){border-right:1px solid #DFE5ED !important}'
             'selector > .elementor-widget:nth-child(-n+2){border-bottom:1px solid #DFE5ED !important}'
             'selector > .elementor-widget:nth-child(even){background:#F7F9FC}'
             'selector .elementor-icon-box-title{font-size:16px !important;line-height:26px !important;font-weight:600 !important;letter-spacing:0 !important;margin-bottom:5px !important}'
             'selector .elementor-icon-box-description{font-size:10px !important;line-height:16.4px !important;font-weight:500 !important;color:#5F6D82 !important;letter-spacing:0 !important}'
             'selector .elementor-icon-box-icon{margin-top:5px}')


# Conditions tabs on mobile: accordion-like order -> active card, its image right below it, then the remaining cards
OLD_TABS_MOBILE = ('@media(max-width:767px){selector .e-n-tabs{grid-template-columns:1fr;gap:16px}selector .e-n-tabs-content{grid-column:1;grid-row:5}'
                   + ''.join('selector .e-n-tab-title:nth-child(%d){grid-column:1;grid-row:%d}' % (n, n if n < 5 else n + 1) for n in range(1, 9))
                   + 'selector .e-n-tabs-content img{height:auto;aspect-ratio:343/608}}')
TABS_CSS = ('selector .e-n-tabs{display:flex !important;flex-direction:column;gap:18px}'
            'selector .e-n-tabs-heading{display:contents !important}'
            + ''.join('selector .e-n-tab-title:nth-child(%d){order:%d}' % (n, 2 * n) for n in range(1, 9))
            + 'selector .e-n-tabs-content{order:3}'
            + ''.join('selector .e-n-tabs:has(.e-n-tab-title:nth-child(%d)[aria-selected=true]) .e-n-tabs-content{order:%d}' % (n, 2 * n + 1)
                      for n in range(1, 9))
            + 'selector .e-n-tabs-content img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:18px}')  # Figma 442:727: 353x353, r18


def conditions(doc):
    t = find(doc['data'], titled('Conditions – Tabs'))
    t['settings']['custom_css'] = t['settings']['custom_css'].replace(OLD_TABS_MOBILE, '')
    add_css(t['settings'], TABS_CSS)
    sec = find(doc['data'], titled('Conditions We Treat'))['settings']   # Figma cards/image are 353 wide at 393 -> 20px sides
    sec['padding_mobile'] = dict(sec.get('padding_mobile') or {'unit': 'px', 'top': '60', 'bottom': '40'}, right='20', left='20', isLinked=False)


def stats(doc):
    d = doc['data']
    find(d, titled('Stats'))['settings']['padding_mobile'] = dm(16, 20, 0, 20)
    card = find(d, titled('Stats – Card'))
    card['settings']['custom_css'] = card['settings'].get('custom_css', '').replace(
        '@media(max-width:767px){selector > .elementor-widget:nth-child(even){background:var(--e-global-color-ehsurf)} selector > .elementor-widget{border:0 !important}}', '')
    add_css(card['settings'], STATS_CSS)
    for w in card['elements']:
        w['settings'].update(_padding_mobile=dm(27.5, 4, 27.5, 10), icon_space_mobile=px(15), icon_size_mobile=px(22),
                             icon_padding_mobile=px(14))


def header():
    doc = fetch(33, 'elementor_library')
    d = doc['data']
    top = find(d, titled('Header'))
    top['settings']['padding_mobile'] = dm(35, 30, 0, 30)
    pill = find(d, titled('Header – Logo & Nav Pill'))
    pill['settings'].update(padding_mobile=dm(7, 9, 7, 7), border_radius_mobile=dims(999))
    add_css(pill['settings'], 'selector{background-color:rgba(255,255,255,.91);border:2px solid rgba(255,255,255,.95);'
                              '-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);min-height:48px}')
    find(d, titled('Header – Logo'))['settings']['width_mobile'] = px(164)
    menu = find(d, titled('Header – Menu'))
    menu['settings']['toggle_size_mobile'] = px(24)
    add_css(menu['settings'], 'selector .elementor-menu-toggle{width:24px;height:24px;padding:0;background:transparent;position:relative}'
                              'selector .elementor-menu-toggle:not(.elementor-active) .elementor-menu-toggle__icon--open{opacity:0}'
                              'selector .elementor-menu-toggle:not(.elementor-active)::before{content:"";position:absolute;inset:0;'
                              'background:url("' + BURGER + '") center/24px no-repeat}')
    save(doc)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('hero', 'all'): hero(int(sys.argv[2]) if len(sys.argv) > 2 else 32)
    if what in ('header', 'all'): header()
