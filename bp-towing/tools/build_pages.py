"""Remaining pages (About, Services, Contact, FAQ, Thank You, Blog) in the new design.
Every widget's content/links come from the original page data; only native Elementor/Pro widgets are emitted."""
from lib import *
import lib, wp
import build_service as bs

PAGES_MAP = {30: 'about', 32: 'services', 36: 'contact', 552: 'faq', 3928: 'thankyou', 4037: 'blog'}
CARD_IMG = [('Auto Towing', 4370), ('Flat Tire', 1096), ('Jump Start', 1184), ('Junk', 4392), ('Fuel', 1114),
            ('Winch', 3153), ('Roadside', 1151), ('Hauling', 3163), ('Motorcycle', 4289)]

def refresh(pid):
    """use the CURRENT live Elementor data as the source (not the older backup)"""
    live = wp.req(f'wp/v2/pages/{pid}?context=edit')
    lib.PAGES[pid]['meta']['_elementor_data'] = live['meta']['_elementor_data']
    lib._IDX.pop(pid, None)

class P(bs.Conv):
    def __init__(self, pid):
        self.p = pid; self.imgs = []
    def one(self, e, ctx=''):
        t = e.get('widgetType')
        if t == 'image-box':
            title = e['settings'].get('title_text', '')
            im = next((m for k, m in CARD_IMG if k.lower() in title.lower()), None)
            return [ANIM(C([IMAGEBOX(self.p, e['id'], image=im)], 'bp-cardwrap'), 'fadeInUp', 0)]
        if t == 'pt-brands':
            return [C([C([W('image', '', image=it['image'], image_size='full')], 'bp-brand') for it in e['settings']['items']],
                      'bp-brands bp-wrap', row=True)]
        if t == 'image-carousel':
            return [CAROUSEL(e['settings']['carousel'])]
        if t == 'shortcode':
            return [W('shortcode', 'bp-reviews', shortcode=e['settings']['shortcode'])]
        if t == 'icon-list':
            return [W('icon-list', 'bp-ticks bp-calllist', icon_list=e['settings']['icon_list'])]
        if t == 'loop-grid':
            x = copy.deepcopy(e); x['id'] = rid(); x['settings']['_css_classes'] = 'bp-loop'
            return [x]
        if t == 'icon-box' and ctx == 'info':
            o = e['settings']
            s = {k: o[k] for k in ('title_text', 'description_text', 'link', 'selected_icon') if k in o}
            s.update(title_size='h3', _css_classes='bp-info bp-glass-light bp-spot')
            return [{'id': rid(), 'elType': 'widget', 'widgetType': 'icon-box', 'isInner': False, 'settings': s, 'elements': []}]
        return super().one(e, ctx)

    # ---------- shared section shapes ----------
    def hero_page(self, ws, bg):
        kids = []
        for w in ws: kids += self.one(w, 'hero')
        return SEC([C(kids, 'bp-phero-copy')], 'bp-phero bp-sec', background_background='slideshow',
                   background_slideshow_gallery=[{'id': bg, 'url': MEDIA[bg]['source_url']}], background_slideshow_ken_burns='yes',
                   background_slideshow_slide_duration=9000, background_size='cover', background_position='center center')
    def cards(self, ws):
        head, cards = [], []
        for w in ws:
            if w.get('widgetType') == 'image-box':
                c = self.one(w)[0]; c['settings']['animation_delay'] = (len(cards) % 3) * 120; cards.append(c)
            else: head += self.one(w)
        return SEC([C(head, 'bp-head-c'), C(cards, 'bp-grid-3')], 'bp-sec bp-dark bp-aura bp-gridbg bp-svc')
    def centered(self, ws, cls):
        kids = []
        for w in ws: kids += self.one(w)
        head = [k for k in kids if k['widgetType'] == 'heading']
        rest = [k for k in kids if k['widgetType'] != 'heading']
        return SEC([C(head, 'bp-head-c')] + rest, cls)
    def contact(self, ws, bg=4414):
        txt, frm = [], []
        for w in ws: (frm if w.get('widgetType') in ('form', 'global', 'icon-list') else txt).extend(self.one(w))
        return SEC([C(txt, 'bp-f1 bp-on-dark'), C(frm, 'bp-f1 bp-formcard bp-glass bp-spot', animation='fadeInRight')],
                   'bp-sec bp-contact bp-dark', row=True, css_classes='bp bp-sec bp-contact bp-dark bp-row bp-g64 bp-center',
                   background_background='classic', background_image=img(bg), background_size='cover', background_position='center center')
    def cta(self, ws):
        kids = []
        for w in ws: kids += self.one(w, 'cta')
        for k in kids:
            if k['widgetType'] == 'heading': k['settings']['_css_classes'] = 'bp-h'
        return SEC(kids, 'bp-sec bp-cta')

    def build(self):
        p = self.p; seed('page-' + PAGES_MAP[p]); tops = tree(p)
        W_ = lambda i: bs.widgets(tops[i], [])
        S_ = []
        if p == 30:  # About
            hero_ws = W_(0); form_ws = W_(1)
            body, btns = [], []
            for w in hero_ws: (btns if w.get('widgetType') == 'pt-button' else body).extend(self.one(w, 'hero'))
            side = [W('heading', 'bp-h bp-h3', title=form_ws[0]['settings']['title'].strip(), header_size=form_ws[0]['settings'].get('header_size', 'p'))]
            side += [FORM(p, form_ws[1]['id'], widths=[100, 50, 50, 100, 33, 33, 33, 100])]
            S_.append(SEC([C(body + [C(btns, 'bp-btns', row=True, animation='fadeInUp', animation_delay=200)], 'bp-hero-copy'),
                           C(side, 'bp-hero-side bp-formcard bp-glass bp-spot bp-on-dark', animation='fadeInRight')],
                          'bp-hero bp-hero-svc', row=True, background_background='slideshow',
                          background_slideshow_gallery=[{'id': 4296, 'url': MEDIA[4296]['source_url']}], background_slideshow_ken_burns='yes',
                          background_slideshow_slide_duration=9000, background_size='cover', background_position='center center'))
            self.imgs = [4162]
            ws = W_(2); txt = [x for w in ws if w.get('widgetType') != 'image' for x in self.one(w)]
            med = [x for w in ws if w.get('widgetType') == 'image' for x in self.one(w)]
            S_.append(SEC([C([HTML('<span class="bp-kicker"></span>')] + txt, 'bp-f1'), C(med, 'bp-frame bp-split-media', animation='fadeInRight')],
                          '', row=True, css_classes='bp bp-sec bp-light bp-split bp-row bp-g64 bp-center'))
            S_.append(self.cards(W_(3)))
            S_.append(SEC([W('template', '', template_id=STATS_ID)], '', boxed=False))
            ws = W_(5); S_.append(SEC([C(self.one(ws[0]), 'bp-head-c bp-head-tight')] + self.one(ws[1]), 'bp-sec-sm bp-dark bp-gridbg'))
            S_.append(self.centered(W_(6), 'bp-sec bp-soft'))
            S_.append(self.centered(W_(7), 'bp-sec bp-light'))
            S_.append(self.contact(W_(8)))
        elif p == 32:  # Services
            S_.append(self.hero_page(W_(0), 4297))
            S_.append(self.cards(W_(1)))
            S_.append(self.centered(W_(2), 'bp-sec bp-soft'))
            S_.append(self.centered(W_(3), 'bp-sec bp-light'))
            S_.append(self.cta(W_(4)))
            S_.append(self.contact(W_(5)))
        elif p == 36:  # Contact
            S_.append(self.hero_page(W_(0), 4414))
            S_.append(self.contact(W_(1), bg=4370))
            info = [x for w in W_(2) for x in self.one(w, 'info')]
            for i, x in enumerate(info): x['settings'].update(_animation='fadeInUp', _animation_delay=i * 120)
            S_.append(SEC([C(info, 'bp-grid-3 bp-info-grid')], 'bp-sec bp-soft'))
        elif p == 552:  # FAQ
            S_.append(self.hero_page(W_(0), 4373))
            acc = [w for w in W_(1) if w.get('widgetType') == 'nested-accordion'][0]
            S_.append(SEC([C([ACCORDION(p, acc['id'])], 'bp-faq-solo')], 'bp-sec bp-soft'))
        elif p == 3928:  # Thank You
            kids, btns = [], []
            for w in W_(0): (btns if w.get('widgetType') == 'pt-button' else kids).extend(self.one(w, 'hero'))
            S_.append(SEC([C(kids + [C(btns, 'bp-btns bp-mid', row=True)], 'bp-ty')], 'bp-phero bp-ty-sec bp-sec',
                          background_background='slideshow', background_slideshow_gallery=[{'id': 4366, 'url': MEDIA[4366]['source_url']}],
                          background_slideshow_ken_burns='yes', background_size='cover', background_position='center center'))
        elif p == 4037:  # Blog
            S_.append(self.hero_page(W_(0), 4298))
            S_.append(SEC([x for w in W_(1) for x in self.one(w)], 'bp-sec bp-soft'))
        return S_

STATS_ID = None
def build(pid):
    if pid == 36: refresh(36)
    return P(pid).build()
