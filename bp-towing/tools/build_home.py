from lib import *
import html as H_
P = 26
def PTH(eid, cls='bp-h2', anim='fadeInUp'):
    """pt-heading / heading -> [eyebrow?, heading] preserving title, subtitle and tag"""
    s = S(P, eid)
    tag = s.get('title_tag') or s.get('header_size') or 'h2'
    out = []
    if s.get('subtitle', '').strip(): out.append(W('heading', 'bp-h bp-eyebrow', title=s['subtitle'].strip(), header_size='div', _animation=anim))
    out.append(W('heading', 'bp-h ' + cls, title=s['title'], header_size=tag, _animation=anim, _animation_delay=80))
    return out

def build():
    seed('home')
    secs = []
    # 1 HERO --------------------------------------------------------------
    hero_copy = C(PTH('5c73063', 'bp-h1') + [
        T(S(P, 'dc756be', 'editor'), 'bp-lead', _animation='fadeInUp', _animation_delay=160),
        W('icon-list', 'bp-ticks', icon_list=S(P, 'd3d1cd7', 'icon_list'), _animation='fadeInUp', _animation_delay=220),
        C([BTN(S(P, '5c7ed88', 'text'), S(P, '5c7ed88', 'link')['url'], 'bp-btn', icon='arrow-right'),
           BTN(S(P, '1e36f75', 'text'), S(P, '1e36f75', 'link')['url'], 'bp-btn bp-btn-glass')],
          'bp-btns', row=True, animation='fadeInUp', animation_delay=300),
    ], 'bp-hero-copy')
    form = C([W('heading', 'bp-h bp-h3', title=S(P, '5a84d55', 'title').strip(), header_size='p'),
              FORM(P, '6906ce6', widths=[100, 50, 50, 100, 33, 33, 33, 100])],
             'bp-hero-side bp-formcard bp-glass bp-spot bp-on-dark', animation='fadeInRight', animation_delay=200)
    secs.append(SEC([hero_copy, form, HTML('<div class="bp-scrollcue" aria-hidden="true"></div>')], 'bp-hero', row=True,
                    background_background='slideshow',
                    background_slideshow_gallery=[{'id': i, 'url': MEDIA[i]['source_url']} for i in (4297, 4470, 4289, 4333, 4298)],
                    background_slideshow_ken_burns='yes', background_slideshow_ken_burns_zoom_direction='in',
                    background_slideshow_slide_duration=6000, background_slideshow_transition='fade',
                    background_slideshow_transition_duration=1400, background_slideshow_lazyload='', background_size='cover', background_position='center center'))
    # 2 TICKER ------------------------------------------------------------
    names = re.findall(r'<span>(.*?)</span>', S(P, 'cdf6e5b', 'html'))
    names = names[:len(names) // 2] if len(names) % 2 == 0 and names[:len(names)//2] == names[len(names)//2:] else names
    AH = ' aria-hidden="true"'
    sp = lambda hidden: ''.join('<span' + (AH if hidden else '') + '>' + n + '</span>' for n in names)
    tk = f'<div class="bp-tk"><div class="bp-tk-track">{sp(0)}{sp(1)}</div></div>'
    secs.append(SEC([HTML(tk)], 'bp-ticker', boxed=False))
    # 3 ABOUT -------------------------------------------------------------
    about_media = C([IMG(4452, 'bp-media bp-media-tall', size='large'),
                     C([IMG(2276, 'bp-logo-badge', size='medium')], 'bp-badge bp-glass-light')],
                    'bp-f1 bp-frame', animation='fadeInLeft')
    about_copy = C([HTML('<span class="bp-kicker"></span>')] + PTH('eabff14') +
                   [T(S(P, 'af15d06', 'editor'), 'bp-t', _animation='fadeInUp', _animation_delay=150)], 'bp-f1')
    secs.append(SEC([about_media, about_copy], 'bp-sec bp-light', row=True, css_classes='bp bp-sec bp-light bp-row bp-g64 bp-center'))
    # 4 SERVICES ----------------------------------------------------------
    svc_imgs = {'29f82cc': 4370, 'c792899': 1096, '04e3578': 1184, '755654d': 4392, '186a1e6': 1114,
                'd7b8a39': 3153, '388fda9': 1151, '09c783e': 3163, '9e033c5': 4289}
    cards = [ANIM(C([IMAGEBOX(P, k, image=v)], 'bp-cardwrap'), 'fadeInUp', (i % 3) * 120) for i, (k, v) in enumerate(svc_imgs.items())]
    secs.append(SEC([C(PTH('1298a72') + [T(S(P, '58b8602', 'editor'), 'bp-lead')], 'bp-head-c'),
                     C(cards, 'bp-grid-3')], 'bp-sec bp-dark bp-aura bp-gridbg bp-svc'))
    # 5 AREAS -------------------------------------------------------------
    vid = src(P, '7584d21'); vid['id'] = rid(); vid['settings'] = clean(vid['settings']); vid['settings'].update(show_image_overlay='yes', image_overlay=img(4433), image_overlay_size='large', play_icon=ICO('play'), lightbox='')
    secs.append(SEC([C(PTH('0f11619') + [T(S(P, 'aa1f97a', 'editor'), 'bp-t bp-list bp-list-pin')], 'bp-f1'),
                     C([vid], 'bp-f1 bp-video bp-glass-light', animation='zoomIn')],
                    'bp-sec bp-soft', row=True, css_classes='bp bp-sec bp-soft bp-row bp-g64 bp-center'))
    # 6 STATS (shared template) --------------------------------------------
    secs.append(SEC([W('template', '', template_id=STATS_ID)], '', boxed=False))
    # 7 ONE-CALL ------------------------------------------------------------
    rows = [ANIM(C([ICONBOX(P, k, cls='bp-feat-row', position='left')], 'bp-step'), 'fadeInUp', i * 120) for i, k in enumerate(['993c492', '53c0d6f', 'bd7f73b'])]
    chip = C([W('icon', '', selected_icon=S(P, k, 'selected_icon'), view='default') for k in ('993c492', '53c0d6f', 'bd7f73b')],
             'bp-oc-chip bp-glass-light', row=True, css_classes='bp-oc-chip bp-glass-light bp-row bp-keep')
    oc_media = C([IMG(4333, 'bp-media', size='large'), chip], 'bp-oc-media', animation='fadeInLeft')
    secs.append(SEC([oc_media, C(PTH('400b5c6') + [C(rows, 'bp-oc-rows')], 'bp-oc-copy')],
                    'bp-sec bp-onecall', row=True, css_classes='bp bp-sec bp-onecall bp-light bp-row bp-g64 bp-center'))
    # 8 WHY -----------------------------------------------------------------
    why_img = IMG(4366, 'bp-media bp-media-tall', size='large', motion_fx_motion_fx_scrolling='yes', motion_fx_translateY_effect='yes',
                  motion_fx_translateY_speed={'unit': 'px', 'size': 2}, motion_fx_devices=['desktop', 'tablet'])
    secs.append(SEC([C(PTH('ab14914') + [T(S(P, '8abc9df', 'editor'), 'bp-t bp-list')], 'bp-f1'),
                     C([why_img], 'bp-frame', animation='fadeInRight', _element_width='initial', css_classes='bp-frame bp-col bp-why-media')],
                    'bp-sec bp-light', row=True, css_classes='bp bp-sec bp-light bp-row bp-g64 bp-center'))
    # 9 BRANDS --------------------------------------------------------------
    brands = [C([W('image', '', image=it['image'], image_size='full')], 'bp-brand') for it in S(P, '061f5b1', 'items')]
    secs.append(SEC([C(PTH('9c5bd54', 'bp-h3'), 'bp-head-c bp-head-tight'), C(brands, 'bp-brands bp-wrap', row=True)], 'bp-sec-sm bp-dark bp-gridbg'))
    # 10 WORK ---------------------------------------------------------------
    secs.append(SEC([C(PTH('2dee8f1'), 'bp-head-c'), CAROUSEL(S(P, 'f36e0d0', 'carousel'))], 'bp-sec bp-soft'))
    # 11 REVIEWS ------------------------------------------------------------
    secs.append(SEC([C(PTH('3dc466b'), 'bp-head-c'), W('shortcode', 'bp-reviews', shortcode=S(P, '0b9e778', 'shortcode'))], 'bp-sec bp-light'))
    # 12 CTA ----------------------------------------------------------------
    b = S(P, '7677ada')
    secs.append(SEC([W('heading', 'bp-h', title=S(P, 'f4e8e77', 'title'), header_size='h2', _animation='zoomIn'),
                     T(S(P, '86ec476', 'editor'), 'bp-t', _animation='fadeInUp', _animation_delay=120),
                     BTN(b['text'], b['link']['url'], 'bp-btn bp-btn-white bp-btn-xl bp-pulse', icon='phone-alt', _animation='fadeInUp', _animation_delay=220)],
                    'bp-sec bp-cta'))
    # 13 CONTACT ------------------------------------------------------------
    secs.append(SEC([C(PTH('e1ed6b4') + [T(S(P, '0b4b953', 'editor'), 'bp-t')], 'bp-f1 bp-on-dark'),
                     C([FORM(P, 'cd50244', widths=[100, 50, 50, 100, 100])], 'bp-f1 bp-formcard bp-glass bp-spot', animation='fadeInRight')],
                    'bp-sec bp-contact bp-dark', row=True, css_classes='bp bp-sec bp-contact bp-dark bp-row bp-g64 bp-center',
                    background_background='classic', background_image=img(4414), background_size='cover', background_position='center center'))
    # 14 FAQ ----------------------------------------------------------------
    secs.append(SEC([C([HTML('<span class="bp-kicker"></span>')] + PTH('480a468'), 'bp-faq-side bp-f1'),
                     C([ACCORDION(P, 'e6e7e02')], 'bp-faq-main', css_classes='bp-faq-main bp-col', _flex_size='grow')],
                    'bp-sec bp-soft', row=True, css_classes='bp bp-sec bp-soft bp-row bp-g64 bp-faqwrap'))
    return secs

def stats_template():
    seed('stats')
    t = tree(3399)
    icons = [e['settings']['selected_icon'] for e in find(3399, lambda e: e.get('widgetType') == 'icon')]
    cnts = [e['settings'] for e in find(3399, lambda e: e.get('widgetType') == 'counter')]
    num = lambda c: W('heading', 'bp-h bp-num', header_size='div', title=f'<span class="bp-count" data-to="{int(c["ending_number"])}">{int(c["ending_number"])}</span><span class="bp-suf">{c.get("suffix", "")}</span>')
    cards = [ANIM(C([W('icon', '', selected_icon=ic, view='default'),
                     C([num(c), W('heading', 'bp-h bp-num-l', title=c['title'].strip(), header_size='div')], 'bp-statx')],
                    'bp-stat bp-glass bp-spot', row=True, css_classes='bp-stat bp-glass bp-spot bp-row bp-keep bp-center'), 'fadeInUp', i * 120)
             for i, (ic, c) in enumerate(zip(icons, cnts))]
    return [SEC([C(cards, 'bp-grid-3')], 'bp-sec-sm bp-stats bp-dark', background_background='classic', background_image=img(4298),
                background_size='cover', background_position='center center',
                background_motion_fx_motion_fx_scrolling='yes', background_motion_fx_translateY_effect='yes',
                background_motion_fx_translateY_speed={'unit': 'px', 'size': 4}, background_motion_fx_devices=['desktop', 'tablet'])]

STATS_ID = None
if __name__ == '__main__':
    import sys
    STATS_ID = 0
    d = build(); print(len(d), 'sections', len(json.dumps(d)), 'bytes')
