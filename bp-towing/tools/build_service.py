"""Service pages: convert each original 14-section page into the new design, widget by widget, in original order.
Only native Elementor / Elementor Pro widgets are emitted (no pt-* theme addon widgets)."""
from lib import *

SVC = {573: 'roadside', 1012: 'jumpstart', 1049: 'fuel', 1057: 'tire', 1069: 'winch', 1075: 'auto', 2732: 'hauling', 2741: 'moto', 2752: 'special'}
# hero background + in-content images (in original order of image widgets)
IMGS = {
    573: (4370, [4367, 4373, 1151]),
    1012: (1184, [1182, 3160, 4374, 1151]),
    1049: (1109, [1114, 4367, 4373, 1118]),
    1057: (1096, [646, 645, 3160, 1151]),
    1069: (2269, [1205, 3153, 3156, 3151]),
    1075: (4297, [4333, 4298, 4366]),
    2732: (4415, [3163, 3164, 3162, 3524]),
    2741: (4289, [4164, 4375, 4293, 4163]),
    2752: (4470, [4471, 4433, 3159, 3148]),
}

def widgets(e, out):
    if e['elType'] == 'widget': out.append(e)
    for c in e.get('elements', []): widgets(c, out)
    return out

class Conv:
    def __init__(self, pid):
        self.p = pid; self.imgs = list(IMGS[pid][1])
    def img(self, orig):
        return self.imgs.pop(0) if self.imgs else orig['settings']['image'].get('id')
    def one(self, e, ctx=''):
        """original widget -> list of new widgets"""
        t, s = e.get('widgetType'), e.get('settings') or {}
        if t == 'pt-heading':
            out = []
            if (s.get('subtitle') or '').strip(): out.append(W('heading', 'bp-h bp-eyebrow', title=s['subtitle'].strip(), header_size='div', _animation='fadeInUp'))
            out.append(W('heading', 'bp-h bp-h2', title=s['title'], header_size=s.get('title_tag') or 'h2', _animation='fadeInUp', _animation_delay=80))
            return out
        if t == 'heading':
            tag = s.get('header_size') or 'h2'
            cls = 'bp-h1' if tag == 'h1' else 'bp-h2'
            return [W('heading', 'bp-h ' + cls, title=s['title'], header_size=tag, _animation='fadeInUp')]
        if t == 'text-editor':
            ed = s.get('editor', '')
            cls = ('bp-lead' if ctx == 'hero' else 'bp-t') + (' bp-list' + (' bp-list-pin' if ctx == 'areas' else '') if '<ul' in ed and ctx not in ('hero', 'faq') else '')
            return [T(ed, cls)]
        if t in ('pt-button', 'button'):
            url = (s.get('link') or {}).get('url', '')
            tel = url.startswith('tel:')
            cls = 'bp-btn' + (' bp-btn-glass' if ctx == 'hero' and tel else '') + (' bp-btn-white bp-btn-xl bp-pulse' if ctx == 'cta' else '')
            return [BTN(s.get('text', ''), url, cls, icon='phone-alt' if tel and '📱' not in s.get('text', '') else ('arrow-right' if not tel else None))]
        if t == 'image':
            return [IMG(self.img(e), 'bp-media bp-media-wide', size='large')]
        if t == 'video':
            v = copy.deepcopy(e); v['id'] = rid(); v['settings'] = clean(v['settings']); v['settings'].update(show_image_overlay='yes', image_overlay=img(IMGS[self.p][0]), image_overlay_size='large', play_icon=ICO('play'), lightbox='')
            return [v]
        if t == 'icon-box':
            return [ANIM(C([ICONBOX(self.p, e['id'])], 'bp-cardwrap'), 'fadeInUp', 0)]
        if t == 'global':
            tid = int(e.get('templateID') or 0)
            return [FORM(tid, tree(tid)[0]['id'], widths=[100, 50, 50, 100, 100], cls='bp-form')]
        if t == 'form':
            return [FORM(self.p, e['id'], widths=[100, 50, 50, 100, 100], cls='bp-form')]
        if t == 'html':
            return []  # ticker handled separately
        x = copy.deepcopy(e); x['id'] = rid(); return [x]

    def build(self):
        p = self.p; seed(SVC[p]); secs = []
        tops = tree(p)
        hero_bg = IMGS[p][0]
        faq_head = None
        for i, top in enumerate(tops):
            ws = widgets(top, [])
            types = [w.get('widgetType') for w in ws]
            # --- shared templates
            if types == ['template']:
                tid = int(ws[0]['settings']['template_id'])
                if tid == 3399:
                    secs.append(SEC([W('template', '', template_id=STATS_ID)], '', boxed=False))
                elif tid == 3418:
                    s = find(3418, lambda e: e.get('widgetType') in ('pt-heading', 'image-carousel'))
                    secs.append(SEC([C(self.one(s[0]), 'bp-head-c'), CAROUSEL(s[1]['settings']['carousel'])], 'bp-sec bp-soft'))
                elif tid == 3427:
                    s = find(3427, lambda e: e.get('widgetType') in ('pt-heading', 'shortcode'))
                    secs.append(SEC([C(self.one(s[0]), 'bp-head-c'), W('shortcode', 'bp-reviews', shortcode=s[1]['settings']['shortcode'])], 'bp-sec bp-light'))
                else:
                    secs.append(SEC([W('template', '', template_id=tid)], '', boxed=False))
                continue
            if 'html' in types:  # ticker
                names = re.findall(r'<span>(.*?)</span>', ws[types.index('html')]['settings']['html'])
                half = len(names) // 2
                if names[:half] == names[half:]: names = names[:half]
                AH = ' aria-hidden="true"'
                sp = lambda h: ''.join('<span' + (AH if h else '') + '>' + n + '</span>' for n in names)
                secs.append(SEC([HTML(f'<div class="bp-tk"><div class="bp-tk-track">{sp(0)}{sp(1)}</div></div>')], 'bp-ticker', boxed=False))
                continue
            if i == 0:  # hero
                form = [w for w in ws if w.get('widgetType') in ('global', 'form')]
                copy_ws = [w for w in ws if w not in form]
                body, btns = [], []
                for w in copy_ws:
                    (btns if w.get('widgetType') in ('pt-button', 'button') else body).extend(self.one(w, 'hero'))
                kids = [C(body + ([C(btns, 'bp-btns', row=True, animation='fadeInUp', animation_delay=200)] if btns else []), 'bp-hero-copy')]
                if form: kids.append(C(self.one(form[0], 'hero'), 'bp-hero-side bp-formcard bp-glass bp-spot bp-on-dark', animation='fadeInRight', animation_delay=150))
                secs.append(SEC(kids, 'bp-hero bp-hero-svc', row=True, background_background='slideshow',
                                background_slideshow_gallery=[{'id': hero_bg, 'url': MEDIA[hero_bg]['source_url']}],
                                background_slideshow_ken_burns='yes', background_slideshow_ken_burns_zoom_direction='in',
                                background_slideshow_slide_duration=9000, background_slideshow_loop='yes', background_size='cover', background_position='center center'))
                continue
            if 'nested-accordion' in types:
                acc = ws[types.index('nested-accordion')]
                side = [HTML('<span class="bp-kicker"></span>')] + (faq_head or [])
                for w in ws:
                    if w.get('widgetType') not in ('nested-accordion',) and not self._inside(acc, w): side += self.one(w)
                secs.append(SEC([C(side, 'bp-faq-side bp-f1'), C([ACCORDION(p, acc['id'])], 'bp-faq-main')],
                                'bp-sec bp-soft', row=True, css_classes='bp bp-sec bp-soft bp-row bp-g64 bp-faqwrap'))
                faq_head = None
                continue
            if types in (['pt-heading'], ['heading']) and i + 1 < len(tops) and 'nested-accordion' in [w.get('widgetType') for w in widgets(tops[i + 1], [])]:
                faq_head = self.one(ws[0]); continue
            if types.count('icon-box') >= 3:  # features
                head, cards = [], []
                for w in ws:
                    if w.get('widgetType') == 'icon-box':
                        c = self.one(w)[0]; c['settings']['animation_delay'] = (len(cards) % 3) * 120; cards.append(c)
                    else: head += self.one(w)
                secs.append(SEC([C(head, 'bp-head-c'), C(cards, 'bp-grid-3')], 'bp-sec bp-dark bp-aura bp-gridbg'))
                continue
            if 'form' in types or 'global' in types:  # contact
                txt, frm = [], []
                for w in ws: (frm if w.get('widgetType') in ('form', 'global') else txt).extend(self.one(w))
                secs.append(SEC([C(txt, 'bp-f1 bp-on-dark'), C(frm, 'bp-f1 bp-formcard bp-glass bp-spot', animation='fadeInRight')],
                                'bp-sec bp-contact bp-dark', row=True, css_classes='bp bp-sec bp-contact bp-dark bp-row bp-g64 bp-center',
                                background_background='classic', background_image=img(4414), background_size='cover', background_position='center center'))
                continue
            if 'image' not in types and 'video' not in types:  # CTA band (heading + text + button)
                kids = []
                for w in ws: kids += self.one(w, 'cta')
                for k in kids:
                    if k['widgetType'] == 'heading': k['settings']['_css_classes'] = 'bp-h'
                secs.append(SEC(kids, 'bp-sec bp-cta'))
                continue
            # split text / media sections, alternating sides & surfaces
            n_split = sum(1 for s in secs if 'bp-split' in s['settings']['css_classes'])
            areas = any('Service Area' in (w['settings'].get('title') or '') for w in ws)
            ctx = 'areas' if areas else ''
            txt, media = [], []
            for w in ws:
                (media if w.get('widgetType') in ('image', 'video') else txt).extend(self.one(w, ctx))
            tbtns = [x for x in txt if x['widgetType'] == 'button']
            txt = [x for x in txt if x['widgetType'] != 'button'] + ([C(tbtns, 'bp-btns', row=True)] if tbtns else [])
            vid = media and media[0]['widgetType'] == 'video'
            mcol = C(media, ('bp-video bp-glass-light' if vid else 'bp-frame') + ' bp-split-media', animation='fadeInRight' if n_split % 2 == 0 else 'fadeInLeft')
            tcol = C([HTML('<span class="bp-kicker"></span>')] + txt, 'bp-f1')
            surface = 'bp-light' if n_split % 2 == 0 else 'bp-soft'
            kids = [tcol, mcol] if n_split % 2 == 0 else [mcol, tcol]
            secs.append(SEC(kids, '', row=True, css_classes=f'bp bp-sec {surface} bp-split bp-row bp-g64 bp-center'))
        return secs

    @staticmethod
    def _inside(parent, w):
        found = []
        widgets(parent, found)
        return w in found

STATS_ID = None
def build(pid):
    return Conv(pid).build()
