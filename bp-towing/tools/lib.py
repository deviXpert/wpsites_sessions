"""Element builders + source-content helpers for the BP Towing redesign.
All copy/links come from the ORIGINAL Elementor data (wp-backup/) by element id — never retyped."""
import json, random, copy, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, 'wp-backup')
PAGES = {p['id']: p for p in json.load(open(f'{B}/pages.json'))}
POSTS = {p['id']: p for p in json.load(open(f'{B}/posts.json'))}
LIB = {t['id']: t for t in json.load(open(f'{B}/elementor_library.json'))}
MEDIA = {m['id']: m for m in json.load(open(f'{B}/media.json'))}
SITE = 'https://bptowingservice.ca'

_rng = random.Random(1)
def seed(s): global _rng; _rng = random.Random(str(s))
def rid(): return '%07x' % _rng.getrandbits(28)

# ---------- source access ----------
def tree(doc):
    src = PAGES.get(doc) or POSTS.get(doc) or LIB.get(doc)
    return json.loads(src['meta']['_elementor_data'] or '[]')
_IDX = {}
def src(doc, eid):
    """deep copy of an original element (by doc id + element id)"""
    if doc not in _IDX:
        ix = {}
        def w(e):
            ix[e['id']] = e
            for c in e.get('elements', []): w(c)
        for e in tree(doc): w(e)
        _IDX[doc] = ix
    return copy.deepcopy(_IDX[doc][eid])
def S(doc, eid, key=None):
    s = src(doc, eid)['settings']
    return s if key is None else s.get(key)
def find(doc, pred):
    out = []
    def w(e):
        if pred(e): out.append(e)
        for c in e.get('elements', []): w(c)
    for e in tree(doc): w(e)
    return copy.deepcopy(out)

# ---------- media ----------
def img(mid, size='large'):
    m = MEDIA[mid]
    return {'id': mid, 'url': m['source_url'], 'size': '', 'alt': m.get('alt_text', ''), 'source': 'library'}

# ---------- builders ----------
def C(els, cls='', boxed=False, row=False, inner=True, **s):
    st = {'content_width': 'boxed' if boxed else 'full', 'flex_direction': 'row' if row else 'column',
          'css_classes': ' '.join(x for x in [cls, 'bp-row' if row else 'bp-col'] if x)}
    if row: st['flex_wrap'] = 'nowrap'
    st.update(s)
    return {'id': rid(), 'elType': 'container', 'isInner': inner, 'settings': st, 'elements': els}
def SEC(els, cls='', boxed=True, **s):
    """top-level section"""
    c = C(els, 'bp ' + cls, boxed=boxed, inner=False, **s)
    return c
def W(t, cls='', anim=None, delay=0, **s):
    if cls: s['_css_classes'] = cls
    if anim: s['_animation'] = anim; s['_animation_delay'] = delay
    return {'id': rid(), 'elType': 'widget', 'widgetType': t, 'isInner': False, 'settings': s, 'elements': []}
def ANIM(c, anim='fadeInUp', delay=0):
    c['settings']['animation'] = anim; c['settings']['animation_delay'] = delay; return c
def ICO(v, lib='fa-solid'):
    pre = {'fa-solid': 'fas', 'fa-regular': 'far', 'fa-brands': 'fab'}[lib]
    return {'value': f'{pre} fa-{v}', 'library': lib}
def LINK(u): return {'url': u, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}
def H(title, tag='h2', cls='bp-h2', **k): return W('heading', 'bp-h ' + cls, title=title, header_size=tag, **k)
def T(html, cls='bp-t', **k): return W('text-editor', cls, editor=html, **k)
def BTN(text, url, cls='bp-btn', icon=None, **k):
    s = dict(text=text, link=LINK(url), **k)
    if icon: s.update(selected_icon=ICO(icon), icon_align='row-reverse' if icon.startswith('arrow') else 'row', icon_indent={'unit': 'px', 'size': 10})
    return W('button', cls, **s)
def IMG(mid, cls='bp-media', size='large', **k): return W('image', cls, image=img(mid), image_size=size, **k)
def HTML(h, cls='', **k): return W('html', cls, html=h, **k)
def ICONLIST(items, cls='', **k):
    """items: list of dicts with text/icon/link (link optional)"""
    lst = []
    for it in items:
        d = {'_id': rid(), 'text': it['text'], 'selected_icon': it.get('icon') or {'value': '', 'library': ''}}
        if it.get('link'): d['link'] = LINK(it['link'])
        lst.append(d)
    return W('icon-list', cls, icon_list=lst, **k)

STYLE_KEY = re.compile(r'(color|typography|border|background|padding|margin|_size$|_spacing|shadow|align|_gap|width|height|radius|hover_animation|_position$|^_)', re.I)
def clean(settings, keep=()):
    """drop styling keys from an original widget's settings so only content/function remains"""
    return {k: v for k, v in settings.items() if k in keep or not STYLE_KEY.search(k)}

def FORM(doc, eid, widths=None, cls='bp-form', btn_text=None):
    s = clean(S(doc, eid), keep=('button_width',))
    s['_css_classes'] = cls
    for i, f in enumerate(s.get('form_fields', [])):
        if widths: f['width'] = str(widths[i] if i < len(widths) else 100)
        for k in list(f):
            if k.startswith('width_'): f.pop(k)
    s['button_width'] = '100'
    s['selected_button_icon'] = ICO('paper-plane'); s['button_icon_align'] = 'row-reverse'; s['button_icon_indent'] = {'unit': 'px', 'size': 10}
    s['input_size'] = 'md'; s['button_size'] = 'md'
    w = src(doc, eid); w['settings'] = s; w['id'] = rid()
    return w

def IMAGEBOX(doc, eid, cls='bp-card bp-glass bp-spot', image=None, **k):
    o = S(doc, eid)
    s = {kk: o[kk] for kk in ('title_text', 'description_text', 'link', 'title_size') if kk in o}
    s['image'] = img(image) if image else o['image']
    s['thumbnail_size'] = 'medium_large'
    s['title_size'] = 'h3'
    s['_css_classes'] = cls
    s.update(k)
    return {'id': rid(), 'elType': 'widget', 'widgetType': 'image-box', 'isInner': False, 'settings': s, 'elements': []}

def ICONBOX(doc, eid, cls='bp-feat bp-glass bp-spot', icon=None, **k):
    o = S(doc, eid)
    s = {kk: o[kk] for kk in ('title_text', 'description_text', 'link', 'selected_icon') if kk in o}
    if icon: s['selected_icon'] = icon
    s.setdefault('selected_icon', ICO('check'))
    s['title_size'] = 'h3'; s['view'] = 'default'; s['_css_classes'] = cls; s.update(k)
    return {'id': rid(), 'elType': 'widget', 'widgetType': 'icon-box', 'isInner': False, 'settings': s, 'elements': []}

def ACCORDION(doc, eid, cls='bp-faq'):
    """rebuild nested accordion keeping item titles + inner text-editor content exactly"""
    a = src(doc, eid)
    items = a['settings']['items']
    kids = []
    for it, ch in zip(items, a['elements']):
        eds = [e for e in ch['elements'] if e['elType'] == 'widget']
        inner = []
        for e in eds:
            if e['widgetType'] == 'text-editor': inner.append(T(e['settings']['editor']))
            else:
                e = copy.deepcopy(e); e['id'] = rid(); inner.append(e)
        kids.append({'id': rid(), 'elType': 'container', 'isInner': True, 'settings': {'content_width': 'full', 'css_classes': 'bp-col'}, 'elements': inner})
    s = {'items': [{'item_title': i['item_title'], '_id': i['_id']} for i in items],
         'title_tag': a['settings'].get('title_tag', 'h3'), 'faq_schema': a['settings'].get('faq_schema', 'yes'),
         'accordion_item_title_icon': ICO('chevron-down'), 'accordion_item_title_icon_active': ICO('chevron-down'),
         'default_state': 'expanded', 'max_items_expended': 'one', '_css_classes': cls}
    return {'id': rid(), 'elType': 'widget', 'widgetType': 'nested-accordion', 'isInner': False, 'settings': s, 'elements': kids}

def CAROUSEL(ids_or_list, cls='bp-carousel', **k):
    lst = [img(i) if isinstance(i, int) else {'id': i['id'], 'url': i['url']} for i in ids_or_list]
    s = dict(carousel=lst, thumbnail_size='medium_large', slides_to_show='4', slides_to_show_tablet='2', slides_to_show_mobile='1',
             slides_to_scroll='1', navigation='both', autoplay='yes', autoplay_speed=3500, pause_on_hover='yes', infinite='yes',
             speed=700, image_stretch='yes', image_spacing='custom', image_spacing_custom={'unit': 'px', 'size': 20}, link_to='none')
    s.update(k)
    return W('image-carousel', cls, **s)

def COUNTER(n, suffix, title, **k):
    return W('counter', '', starting_number=0, ending_number=n, suffix=suffix, title=title, duration=2200, thousand_separator='', **k)

def tw(x): return json.dumps(x)
