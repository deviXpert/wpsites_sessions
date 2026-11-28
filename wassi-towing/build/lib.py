"""Helpers that emit native Elementor (4.x) container/widget JSON.

Everything here maps 1:1 to controls you can see in the Elementor panel.
Icons/images are referenced by local file name and resolved to media-library
IDs/URLs at deploy time via media.json (see deploy.py).
"""
import json, os, random, string

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_PATHS = json.load(open(os.path.join(HERE, 'icon_paths.json')))
try:
    MEDIA = json.load(open(os.path.join(HERE, 'media.json')))
except FileNotFoundError:
    MEDIA = {}

# ---- brand tokens -----------------------------------------------------------
NAVY, INK, NAVY2 = '#101D32', '#0B1424', '#1A2B47'
ORANGE, ORANGE_TXT, ORANGE_TINT = '#FF6B00', '#B84D00', '#FFF1E6'
BG, LINE, MUTED, ON_DARK, WHITE = '#F5F6F8', '#E2E6EC', '#5A6577', '#C5CEDB', '#FFFFFF'
MONT, INTER = 'Montserrat', 'Inter'

PHONE_HREF = 'tel:+10000000000'      # [PHONE]
SMS_HREF = 'sms:+10000000000'        # [SMS NUMBER]

SERVICE_URL = {
    'flatbed': '/services/flatbed-towing/',
    'roadside': '/services/roadside-assistance/',
    'tire': '/services/flat-tire-change/',
    'fuel': '/services/fuel-delivery/',
    'battery': '/services/battery-boost/',
    'winch': '/services/winch-out/',
    'hauling': '/services/local-hauling/',
    'moto': '/services/motorcycle-towing/',
    'exotic': '/services/exotic-car-towing/',
}

_used = set()
def uid():
    while True:
        i = ''.join(random.choice('0123456789abcdef') for _ in range(7))
        if i not in _used:
            _used.add(i)
            return i

# ---- value helpers ----------------------------------------------------------
def px(v, unit='px'):
    if isinstance(v, str):
        return {'unit': 'custom', 'size': v, 'sizes': []}
    return {'unit': unit, 'size': v, 'sizes': []}

def box(t, r=None, b=None, l=None, unit='px'):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l),
            'isLinked': len({t, r, b, l}) == 1}

def gap(row, col=None):
    col = row if col is None else col
    return {'unit': 'px', 'row': str(row), 'column': str(col), 'size': col, 'isLinked': row == col}

def typo(family=None, weight=None, size=None, lh=None, ls=None, style=None, transform=None,
         prefix='typography', size_m=None, size_t=None, lh_unit='em', decoration=None):
    s = {f'{prefix}_typography': 'custom'}
    if family: s[f'{prefix}_font_family'] = family
    if weight: s[f'{prefix}_font_weight'] = str(weight)
    if size is not None: s[f'{prefix}_font_size'] = px(size)
    if size_t is not None: s[f'{prefix}_font_size_tablet'] = px(size_t)
    if size_m is not None: s[f'{prefix}_font_size_mobile'] = px(size_m)
    if lh is not None: s[f'{prefix}_line_height'] = px(lh, lh_unit)
    if ls is not None: s[f'{prefix}_letter_spacing'] = px(ls, 'em')
    if style: s[f'{prefix}_font_style'] = style
    if transform: s[f'{prefix}_text_transform'] = transform
    if decoration: s[f'{prefix}_text_decoration'] = decoration
    return s

def shadow(h, v, blur, spread, color, key='box_shadow'):
    return {f'{key}_box_shadow_type': 'yes',
            f'{key}_box_shadow': {'horizontal': h, 'vertical': v, 'blur': blur, 'spread': spread, 'color': color}}

def border(width, color, style='solid', radius=None, prefix='border'):
    s = {f'{prefix}_border': style, f'{prefix}_width': width if isinstance(width, dict) else box(width),
         f'{prefix}_color': color}
    if radius is not None:
        s[f'{prefix}_radius' if prefix == 'border' else f'{prefix}_radius'] = radius if isinstance(radius, dict) else box(radius)
    return s

def media(name):
    m = MEDIA.get(name)
    if m:
        return {'url': m['url'], 'id': m['id'], 'source': 'library'}
    return {'url': f'https://wassitowing.ca/wp-content/uploads/wt/{name}', 'id': '', 'source': 'library'}

def icon_value(name, sw=2):
    fname = f'{name}-{str(sw).replace(".", "_")}.svg'
    write_icon(name, sw, fname)
    return {'value': media(fname), 'library': 'svg'}

def write_icon(name, sw, fname):
    path = os.path.join(HERE, 'icons', fname)
    if os.path.exists(path):
        return
    inner = ICON_PATHS[name]
    import re
    # explicit fill="none" on every shape so Elementor's svg{fill:color} rule
    # can't flood-fill stroke icons; stroke follows the icon colour control.
    inner = re.sub(r'<(path|circle|rect|line|polyline|polygon)\b', r'<\1 fill="none"', inner)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')
    open(path, 'w').write(svg)

# ---- elements -----------------------------------------------------------------
def con(*children, dir='column', **s):
    """Inner flex container (full width content, zero default padding/gap)."""
    base = {'content_width': 'full', 'flex_direction': dir, 'padding': box(0), 'flex_gap': gap(0)}
    base.update(s)
    return {'id': uid(), 'elType': 'container', 'isInner': True, 'settings': base,
            'elements': [c for c in children if c]}

def section(*children, bg=None, pt=88, pb=88, pt_m=None, pb_m=None, dir='column', **s):
    """Top-level boxed container: 1200px incl. 24px side padding."""
    base = {'content_width': 'boxed', 'boxed_width': px(1152), 'flex_direction': dir,
            'padding': box(pt, 24, pb, 24), 'flex_gap': gap(0)}
    if pt_m is not None or pb_m is not None:
        base['padding_mobile'] = box(pt if pt_m is None else pt_m, 20, pb if pb_m is None else pb_m, 20)
    if bg:
        base.update({'background_background': 'classic', 'background_color': bg})
    base.update(s)
    return {'id': uid(), 'elType': 'container', 'isInner': False, 'settings': base,
            'elements': [c for c in children if c]}

def full(*children, dir='column', **s):
    """Top-level full-bleed container."""
    base = {'content_width': 'full', 'flex_direction': dir, 'padding': box(0), 'flex_gap': gap(0)}
    base.update(s)
    return {'id': uid(), 'elType': 'container', 'isInner': False, 'settings': base,
            'elements': [c for c in children if c]}

def widget(wtype, **s):
    return {'id': uid(), 'elType': 'widget', 'widgetType': wtype, 'settings': s, 'elements': []}

def flex_item(basis=None, grow=None, shrink=None, widget_=True, mobile_full=False):
    """Flex sizing equivalent to CSS `flex: grow shrink basis`."""
    s = {}
    if grow is not None or shrink is not None:
        s['_flex_size'] = 'custom'
        s['_flex_grow'] = grow if grow is not None else 0
        s['_flex_shrink'] = shrink if shrink is not None else 1
    if basis is not None:
        if widget_:
            s['_element_width'] = 'initial'
            s['_element_custom_width'] = px(basis)
            if mobile_full:
                s['_element_width_mobile'] = 'inherit'
        else:
            s['width'] = px(basis)
    return s

def heading(text, tag='h2', color=NAVY, link=None, **s):
    d = {'title': text, 'header_size': tag, 'title_color': color}
    if link:
        d['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    d.update(s)
    return widget('heading', **d)

def text(html, color=MUTED, **s):
    d = {'editor': html, 'text_color': color, 'paragraph_spacing': px(0)}
    d.update(s)
    return widget('text-editor', **d)

def icon(name, color, size, sw=2, **s):
    d = {'selected_icon': icon_value(name, sw), 'view': 'default', 'primary_color': color,
         'size': px(size), '_element_width': 'auto'}
    d.update(s)
    return widget('icon', **d)

def button(label, url, *, bg=None, color=NAVY, font=MONT, weight=800, size=15, height=48, padx=20,
           radius=14, icon_name=None, icon_sw=2.4, icon_px=None, icon_gap=10, icon_end=False,
           border_w=None, border_c=None, attrs=None, classes='', full_width=False, **s):
    lh = round(size * 1.2)
    content_h = max(lh, icon_px or 0)
    bw = border_w or 0
    pady = round((height - content_h - 2 * bw) / 2, 2)
    d = {'text': label,
         'link': {'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': attrs or ''},
         'button_text_color': color, 'hover_color': color,
         'border_radius': box(radius), 'text_padding': box(pady, padx, pady, padx)}
    d.update(typo(font, weight, size, lh, lh_unit='px'))
    if bg:
        d.update({'background_background': 'classic', 'background_color': bg,
                  'button_background_hover_background': 'classic', 'button_background_hover_color': bg})
    else:
        d.update({'background_background': 'classic', 'background_color': 'rgba(0,0,0,0)',
                  'button_background_hover_background': 'classic', 'button_background_hover_color': 'rgba(255,255,255,0.06)'})
    if bw:
        d.update({'border_border': 'solid', 'border_width': box(bw), 'border_color': border_c,
                  'button_hover_border_color': border_c})
    if icon_name:
        d['selected_icon'] = icon_value(icon_name, icon_sw)
        d['icon_align'] = 'row-reverse' if icon_end else 'row'
        d['icon_indent'] = px(icon_gap)
        if icon_px and icon_px != size:
            classes = (classes + f' wt-i{icon_px}').strip()
    if classes:
        d['_css_classes'] = classes
    if full_width:
        d['align'] = 'justify'
    d.update(s)
    return widget('button', **d)

def image(name, width=None, link=None, alt='', **s):
    d = {'image': media(name), 'image_size': 'full'}
    if width:
        d['width'] = px(width)
    if link:
        d['link_to'] = 'custom'
        d['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    d.update(s)
    return widget('image', **d)

def html(code, **s):
    return widget('html', html=code, **s)

def eyebrow(label, color=ORANGE_TXT, ls=0.14, tag='span'):
    return heading(label, tag, color, **typo(MONT, 800, 13, 1.3, ls, transform='uppercase'))

def h2(label, color=NAVY, tag='h2', size='clamp(1.9rem, 3.4vw, 2.8rem)', lh=1.08, ls=-0.01, **s):
    return heading(label, tag, color, **typo(MONT, 900, size, lh, ls, style='italic'), **s)

def body(label, color=MUTED, size=18, lh=1.7, tag='p', **s):
    return heading(label, tag, color, **typo(INTER, 400, size, lh), **s)

def save(path, content, title, ttype='page', page_settings=None):
    data = {'version': '0.4', 'title': title, 'type': ttype, 'content': content,
            'page_settings': page_settings or {}}
    json.dump(data, open(os.path.join(HERE, path), 'w'), indent=1)
