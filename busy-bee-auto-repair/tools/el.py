"""Helpers that emit classic Elementor (flexbox/grid container + native widget) JSON for Busy Bee.

Conventions
- Values are written the way Elementor stores them, so everything stays editable in the editor.
- Responsive variants: pass `x_tablet=` / `x_mobile=` kwargs (same key + suffix).
- Element IDs are deterministic per build (random seeded by page slug) so Elementor's per-post CSS stays valid.
"""
import json, os, random

import wp

HERE = os.path.dirname(os.path.abspath(__file__))
MEDIA = json.load(open(os.path.join(HERE, 'media.json')))
_ICONS_FILE = os.path.join(HERE, 'icons.json')
ICONS = json.load(open(_ICONS_FILE)) if os.path.exists(_ICONS_FILE) else {}

RNG = random.Random(1)


def seed(s):
    RNG.seed(s)


def uid():
    return '%07x' % RNG.getrandbits(28)


# ---------------------------------------------------------------- value helpers
def px(v, u='px'):
    return {'unit': u, 'size': v, 'sizes': []}


def pct(v):
    return px(v, '%')


def cu(v):
    """Elementor 'custom' unit (any CSS value, e.g. clamp())."""
    return {'unit': 'custom', 'size': v, 'sizes': []}


def dims(t, r=None, b=None, l=None, u='px'):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    if any(isinstance(v, str) and not v.lstrip('-').replace('.', '').isdigit() for v in (t, r, b, l)):
        u = 'custom'
        t, r, b, l = [v if isinstance(v, str) else f'{v}px' if v else '0' for v in (t, r, b, l)]
    return {'unit': u, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l),
            'isLinked': len({str(t), str(r), str(b), str(l)}) == 1}


def gap(col, row=None, u='px'):
    row = col if row is None else row
    return {'column': str(col), 'row': str(row), 'isLinked': col == row, 'unit': u, 'size': col}


def shadow(x, y, blur, spread, color):
    return {'horizontal': x, 'vertical': y, 'blur': blur, 'spread': spread, 'color': color}


def img(key):
    m = MEDIA[key]
    return {'id': m['id'], 'url': m['url'], 'source': 'library', 'alt': ''}


def link(url, external=False):
    return {'url': url, 'is_external': 'on' if external else '', 'nofollow': '', 'custom_attributes': ''}


USED_ICONS = set()
LIST_ICON_COLORS = set()


def icon(name, fallback=None):
    """Lucide icon uploaded as SVG (icons.json) or a Font Awesome fallback."""
    USED_ICONS.add(name)
    if name in ICONS:
        m = ICONS[name]
        return {'value': {'id': m['id'], 'url': m['url']}, 'library': 'svg'}
    fa = fallback or FA.get(name, 'fas fa-circle')
    return {'value': fa, 'library': 'fa-solid' if fa.startswith('fas') else ('fa-brands' if fa.startswith('fab') else 'fa-regular')}


FA = {
    'phone': 'fas fa-phone', 'map-pin': 'fas fa-map-marker-alt', 'clock-3': 'far fa-clock', 'arrow-up-right': 'fas fa-arrow-right',
    'arrow-right': 'fas fa-arrow-right', 'arrow-left': 'fas fa-arrow-left', 'calendar-days': 'far fa-calendar-alt',
    'calendar-check': 'far fa-calendar-check', 'shield-check': 'fas fa-shield-alt', 'cog': 'fas fa-cog', 'battery-charging': 'fas fa-car-battery',
    'disc-3': 'fas fa-compact-disc', 'waves': 'fas fa-water', 'snowflake': 'far fa-snowflake', 'circle-dashed': 'far fa-circle',
    'gauge': 'fas fa-tachometer-alt', 'droplets': 'fas fa-tint', 'circle-gauge': 'fas fa-tachometer-alt', 'settings-2': 'fas fa-sliders-h',
    'unplug': 'fas fa-plug', 'check': 'fas fa-check', 'clipboard-check': 'fas fa-clipboard-check', 'timer-reset': 'fas fa-stopwatch',
    'badge-check': 'fas fa-check-circle', 'car-front': 'fas fa-car', 'scan-search': 'fas fa-search', 'star': 'fas fa-star',
    'wrench': 'fas fa-wrench', 'chevron-down': 'fas fa-chevron-down', 'sparkles': 'fas fa-magic', 'navigation': 'fas fa-location-arrow',
    'instagram': 'fab fa-instagram', 'mail': 'far fa-envelope', 'menu': 'fas fa-bars', 'x': 'fas fa-times', 'whatsapp': 'fab fa-whatsapp',
    'google': 'fab fa-google', 'chevron-right': 'fas fa-chevron-right', 'circle-dot': 'far fa-dot-circle',
}

# ---------------------------------------------------------------- typography
SYS = None  # sentinel: inherit the body (system) font stack, no font-family output


def typo(prefix='typography', ff='Manrope', size=None, weight=None, lh=None, ls=None, tt=None, size_t=None, size_m=None,
         lh_t=None, lh_m=None, ls_t=None, ls_m=None, style=None, deco=None):
    s = {prefix + '_typography': 'custom'}
    if ff:
        s[prefix + '_font_family'] = ff
    if size is not None:
        s[prefix + '_font_size'] = size if isinstance(size, dict) else px(size)
    if size_t is not None:
        s[prefix + '_font_size_tablet'] = size_t if isinstance(size_t, dict) else px(size_t)
    if size_m is not None:
        s[prefix + '_font_size_mobile'] = size_m if isinstance(size_m, dict) else px(size_m)
    if weight is not None:
        s[prefix + '_font_weight'] = str(weight)
    for k, v in (('', lh), ('_tablet', lh_t), ('_mobile', lh_m)):
        if v is not None:
            s[prefix + '_line_height' + k] = v if isinstance(v, dict) else (px(v) if v > 4 else px(v, 'em'))
    for k, v in (('', ls), ('_tablet', ls_t), ('_mobile', ls_m)):
        if v is not None:
            s[prefix + '_letter_spacing' + k] = v if isinstance(v, dict) else px(v)
    if tt:
        s[prefix + '_text_transform'] = tt
    if style:
        s[prefix + '_font_style'] = style
    if deco:
        s[prefix + '_text_decoration'] = deco
    return s


# ---------------------------------------------------------------- elements
def _common(s, kw, widget=False):
    """Map short kwargs shared by containers and widgets to Elementor advanced settings
    (widgets prefix most advanced controls with an underscore, containers don't)."""
    m = {
        'cls': '_css_classes' if widget else 'css_classes', 'id_': '_element_id',
    }
    for k, v in list(kw.items()):
        if k in m:
            s[m[k]] = v
            kw.pop(k)
    # absolute positioning: pos=('abs', x, y, unit, orientation_h, orientation_v)
    pos = kw.pop('pos', None)
    if pos:
        for k2, v2 in list(pos.items()):
            if k2 in ('x_mobile', 'y_mobile', 'x_tablet', 'y_tablet'):
                axis, suf = k2.split('_')
                key = ('_offset_x' if axis == 'x' else '_offset_y') + ('_end' if pos.get('h' if axis == 'x' else 'v', 'start') == 'end' else '')
                s[key + '_' + suf] = v2 if isinstance(v2, dict) else px(v2)
        s['_position' if widget else 'position'] = 'absolute' if pos.get('mode', 'abs') == 'abs' else 'fixed'
        if 'x' in pos:
            s['_offset_orientation_h'] = pos.get('h', 'start')
            s['_offset_x' if pos.get('h', 'start') == 'start' else '_offset_x_end'] = pos['x'] if isinstance(pos['x'], dict) else px(pos['x'])
        if 'y' in pos:
            s['_offset_orientation_v'] = pos.get('v', 'start')
            s['_offset_y' if pos.get('v', 'start') == 'start' else '_offset_y_end'] = pos['y'] if isinstance(pos['y'], dict) else px(pos['y'])
    z = kw.pop('z', None)
    if z is not None:
        s['_z_index' if widget else 'z_index'] = z
    hide = kw.pop('hide', None)  # e.g. 'm' / 'dt' / 'd'
    if hide:
        if 'd' in hide:
            s['hide_desktop'] = 'hidden-desktop'
        if 't' in hide:
            s['hide_tablet'] = 'hidden-tablet'
        if 'm' in hide:
            s['hide_mobile'] = 'hidden-mobile'
    attrs = kw.pop('attrs', None)
    if attrs:
        s['_attributes'] = '\n'.join(f'{k}|{v}' for k, v in attrs.items())
    s.update(kw)
    return s


def C(cname, children=(), /, **kw):
    """Container. Short kwargs: d (direction), grid (columns string), gap, pad, mar, w, minh, bg, radius, border,
    shadow, ov (overflow hidden), jc, ai, wrap, tag, href, boxed (content width px)."""
    s = {'_title': cname}
    boxed = kw.pop('boxed', None)
    if boxed:
        s['content_width'] = 'boxed'
        s['boxed_width'] = px(boxed) if not isinstance(boxed, dict) else boxed
    else:
        s['content_width'] = 'full'
    grid = kw.pop('grid', None)
    if grid is not None:
        s['container_type'] = 'grid'
        s['grid_columns_grid'] = cu(grid) if isinstance(grid, str) else px(grid, 'fr')
        rows = kw.pop('rows', None)
        s['grid_rows_grid'] = cu(rows) if isinstance(rows, str) else px(rows or 1, 'fr')
        for suf in ('_tablet', '_mobile'):
            g2 = kw.pop('grid' + suf, None)
            if g2 is not None:
                s['grid_columns_grid' + suf] = cu(g2) if isinstance(g2, str) else px(g2, 'fr')
            r2 = kw.pop('rows' + suf, None)
            if r2 is not None:
                s['grid_rows_grid' + suf] = cu(r2) if isinstance(r2, str) else px(r2, 'fr')
        # Elementor defaults grids to 1 column / 1 row on tablet & mobile – inherit the desktop grid unless overridden
        for suf in ('_tablet', '_mobile'):
            s.setdefault('grid_columns_grid' + suf, s['grid_columns_grid'] if suf == '_tablet' else s.get('grid_columns_grid_tablet', s['grid_columns_grid']))
            s.setdefault('grid_rows_grid' + suf, s['grid_rows_grid'] if suf == '_tablet' else s.get('grid_rows_grid_tablet', s['grid_rows_grid']))
        g = kw.pop('gap', None)
        if g is not None:
            s['grid_gaps'] = gap(*g) if isinstance(g, tuple) else gap(g)
        for suf in ('_tablet', '_mobile'):
            g2 = kw.pop('gap' + suf, None)
            if g2 is not None:
                s['grid_gaps' + suf] = gap(*g2) if isinstance(g2, tuple) else gap(g2)
        ai = kw.pop('ai', None)
        if ai:
            s['grid_align_items'] = ai
        jc = kw.pop('jc', None)
        if jc:
            s['grid_justify_items'] = jc
        flow = kw.pop('flow', None)
        if flow:
            s['grid_auto_flow'] = flow
    else:
        s['container_type'] = 'flex'
        s['flex_direction'] = kw.pop('d', 'column')
        for suf in ('_tablet', '_mobile'):
            v = kw.pop('d' + suf, None)
            if v:
                s['flex_direction' + suf] = v
        for short, key in (('jc', 'flex_justify_content'), ('ai', 'flex_align_items'), ('wrap', 'flex_wrap'), ('ac', 'flex_align_content')):
            for suf in ('', '_tablet', '_mobile'):
                v = kw.pop(short + suf, None)
                if v:
                    s[key + suf] = v
        for suf in ('', '_tablet', '_mobile'):
            g = kw.pop('gap' + suf, None)
            if g is not None:
                s['flex_gap' + suf] = gap(*g) if isinstance(g, tuple) else gap(g)
        if 'flex_gap' not in s:
            s['flex_gap'] = gap(0)
        # Elementor wraps flex containers on small screens by default; the design never relies on that
        for suf in ('', '_tablet', '_mobile'):
            s.setdefault('flex_wrap' + suf, s.get('flex_wrap', 'nowrap') if suf else 'nowrap')
    for suf in ('', '_tablet', '_mobile'):
        for short, key in (('pad', 'padding'), ('mar', 'margin')):
            v = kw.pop(short + suf, None)
            if v is not None:
                s[key + suf] = v if isinstance(v, dict) else (dims(*v) if isinstance(v, tuple) else dims(v))
        w = kw.pop('w' + suf, None)
        if w is not None:
            s['width' + suf] = w if isinstance(w, dict) else (cu('fit-content') if w == 'auto' else cu(f'min({w}px, 100%)'))
        mh = kw.pop('minh' + suf, None)
        if mh is not None:
            s['min_height' + suf] = mh if isinstance(mh, dict) else px(mh)
        r = kw.pop('radius' + suf, None)
        if r is not None:
            s['border_radius' + suf] = r if isinstance(r, dict) else (dims(*r) if isinstance(r, tuple) else dims(r))
    # Elementor forces --width:100% on every flex container below 768px; keep explicit desktop widths unless overridden
    if 'width' in s and 'width_mobile' not in s:
        s['width_mobile'] = s.get('width_tablet', s['width'])
    if 'width' in s and 'width_tablet' not in s and s['width'].get('unit') == 'custom':
        s['width_tablet'] = s['width']
    bg = kw.pop('bg', None)
    if bg:
        s['background_background'] = 'classic'
        s['background_color'] = bg
    bgi = kw.pop('bgimg', None)
    if bgi:
        s['background_background'] = 'classic'
        s['background_image'] = img(bgi) if isinstance(bgi, str) else bgi
        s['background_size'] = kw.pop('bgsize', 'cover')
        s['background_position'] = kw.pop('bgpos', 'center center')
        s['background_repeat'] = 'no-repeat'
    grad = kw.pop('grad', None)  # (c1, s1, c2, s2, angle) or ('radial', c1, s1, c2, s2, pos)
    if grad:
        s['background_background'] = 'gradient'
        if grad[0] == 'radial':
            _, c1, s1, c2, s2, posn = grad
            s.update(background_gradient_type='radial', background_gradient_position=posn)
        else:
            c1, s1, c2, s2, ang = grad
            s.update(background_gradient_type='linear', background_gradient_angle=px(ang, 'deg'))
        s.update(background_color=c1, background_color_stop=pct(s1), background_color_b=c2, background_color_b_stop=pct(s2))
    ov_ = kw.pop('overlay', None)  # (c1, s1, c2, s2, angle) gradient overlay or a color
    if ov_:
        if isinstance(ov_, str):
            s.update(background_overlay_background='classic', background_overlay_color=ov_)
        else:
            c1, s1, c2, s2, ang = ov_
            s.update(background_overlay_background='gradient', background_overlay_color=c1, background_overlay_color_stop=pct(s1),
                     background_overlay_color_b=c2, background_overlay_color_b_stop=pct(s2),
                     background_overlay_gradient_type='linear', background_overlay_gradient_angle=px(ang, 'deg'))
    b = kw.pop('border', None)  # (width, color[, style]) or dict of per-side widths
    if b:
        s['border_border'] = b[2] if len(b) > 2 else 'solid'
        s['border_width'] = b[0] if isinstance(b[0], dict) else dims(b[0])
        s['border_color'] = b[1]
    sh = kw.pop('shadow', None)
    if sh:
        s['box_shadow_box_shadow_type'] = 'yes'
        s['box_shadow_box_shadow'] = sh
    if kw.pop('ov', False):
        s['overflow'] = 'hidden'
    tag = kw.pop('tag', None)
    if tag:
        s['html_tag'] = tag
    href = kw.pop('href', None)
    if href:
        s['html_tag'] = 'a'
        s['link'] = link(href)
    grow = kw.pop('grow', None)
    if grow is not None:
        s['_flex_size'] = 'grow' if grow else 'none'
    _common(s, kw)
    return {'id': uid(), 'elType': 'container', 'isInner': False, 'settings': s, 'elements': list(children)}


def W(wtype, wname, /, **kw):
    s = {'_title': wname}
    for suf in ('', '_tablet', '_mobile'):
        for short, key in (('mar', '_margin'), ('pad', '_padding')):
            v = kw.pop(short + suf, None)
            if v is not None:
                s[key + suf] = v if isinstance(v, dict) else (dims(*v) if isinstance(v, tuple) else dims(v))
        w = kw.pop('w' + suf, None)
        if w is not None:
            if w == 'auto':
                s['_element_width' + suf] = 'auto'
            elif w == 'full':
                s['_element_width' + suf] = 'initial'
                s['_element_custom_width' + suf] = pct(100)
            else:
                s['_element_width' + suf] = 'initial'
                s['_element_custom_width' + suf] = w if isinstance(w, dict) else px(w)
    grow = kw.pop('grow', None)
    if grow is not None:
        s['_flex_size'] = 'grow' if grow else 'none'
    _common(s, kw, widget=True)
    return {'id': uid(), 'elType': 'widget', 'widgetType': wtype, 'settings': s, 'elements': []}


def H(text, tag='h2', color=None, t=None, align=None, href=None, **kw):
    s = dict(title=text, header_size=tag)
    if color:
        s['title_color'] = color
    if t:
        s.update(t)
    if align:
        s['align'] = align
    if href:
        s['link'] = link(href)
    return W('heading', kw.pop('name', 'Heading'), **s, **kw)


def T(html, color=None, t=None, align=None, **kw):
    s = dict(editor=html)
    if color:
        s['text_color'] = color
    if t:
        s.update(t)
    if align:
        s['align'] = align
    return W('text-editor', kw.pop('name', 'Text'), **s, **kw)


def BTN(text, href='#', t=None, color=None, bg=None, ic=None, ic_pos='after', ic_size=None, ic_gap=8, pad=None, radius=None,
        border=None, sh=None, hover_bg=None, hover_color=None, hover_border=None, align=None, h=None, **kw):
    s = dict(text=text, link=link(href), size='sm')
    if t:
        s.update(t)
    if color:
        s['button_text_color'] = color
    if bg:
        s['background_color'] = bg
        s['background_background'] = 'classic' if not bg.startswith('linear') else 'gradient'
    if ic:
        s['selected_icon'] = icon(ic) if isinstance(ic, str) else ic
        s['icon_align'] = 'row-reverse' if ic_pos == 'after' else 'row'
        s['icon_indent'] = px(ic_gap)
    if ic_size:
        s['icon_size'] = px(ic_size)
    if pad is not None:
        s['text_padding'] = pad if isinstance(pad, dict) else (dims(*pad) if isinstance(pad, tuple) else dims(pad))
    if radius is not None:
        s['border_radius'] = radius if isinstance(radius, dict) else (dims(*radius) if isinstance(radius, tuple) else dims(radius))
    if border:
        s['border_border'] = 'solid'
        s['border_width'] = dims(border[0])
        s['border_color'] = border[1]
    else:
        s['border_border'] = 'none'
    if sh:
        s['button_box_shadow_box_shadow_type'] = 'yes'
        s['button_box_shadow_box_shadow'] = sh
    if hover_bg:
        s['button_background_hover_color'] = hover_bg
        s['button_background_hover_background'] = 'classic'
    if hover_color:
        s['hover_color'] = hover_color
    if hover_border:
        s['button_hover_border_color'] = hover_border
    if align:
        s['align'] = align
    return W('button', kw.pop('name', 'Button – ' + text[:30]), **s, **kw)


def IMG(key, w=None, h=None, fit=None, posn=None, alt=None, radius=None, href=None, size='full', **kw):
    s = dict(image=img(key) if isinstance(key, str) else key, image_size=size)
    if w is not None:
        s['width'] = w if isinstance(w, dict) else px(w)
    if h is not None:
        s['height'] = h if isinstance(h, dict) else px(h)
    if fit:
        s['object-fit'] = fit
    if posn:
        s['object-position'] = posn
    if radius is not None:
        s['image_border_radius'] = dims(radius) if not isinstance(radius, dict) else radius
    if href:
        s['link_to'] = 'custom'
        s['link'] = link(href)
    if alt is not None:
        s['image']['alt'] = alt
    return W('image', kw.pop('name', 'Image'), **s, **kw)


def ICON(ic, /, size=16, color=None, bg=None, box=None, radius=None, href=None, view='default', border=None, **kw):
    """Icon widget. box=N renders a circle/rounded square of N px (stacked view)."""
    s = dict(selected_icon=icon(ic), size=px(size))
    if box:
        s['view'] = 'stacked'
        s['shape'] = 'circle'
        s['icon_padding'] = px((box - size) / 2)
        if bg:
            s['secondary_color'] = color or '#1A2024'
            s['primary_color'] = bg
        if radius is not None:
            s['shape'] = 'square' if radius == 0 else 'rounded'
            s['border_radius'] = dims(radius)
        if border:  # the icon widget has no border for the stacked view – drawn by bb.css
            kw['cls'] = (kw.get('cls', '') + ' bb-ibord').strip()
    else:
        s['view'] = view
        if color:
            s['primary_color'] = color
    if href:
        s['link'] = link(href)
    s.setdefault('align', kw.pop('align', 'left'))
    return W('icon', kw.pop('name', 'Icon – ' + ic), **s, **kw)


def ILIST(items, inline=False, t=None, color=None, ic_color=None, ic_size=14, space=None, gap_=8, align=None, **kw):
    """Icon list: items = [(icon_name, text, href|None)]."""
    li = []
    for it in items:
        ic, txt = it[0], it[1]
        d = {'_id': uid(), 'text': txt, 'selected_icon': icon(ic) if ic else {'value': '', 'library': ''}}
        if len(it) > 2 and it[2]:
            d['link'] = link(it[2])
        li.append(d)
    s = dict(icon_list=li, icon_size=px(ic_size), text_indent=px(gap_))
    if inline:
        s['view'] = 'inline'
    if t:
        s.update({('icon_' + k if k.startswith('typography') else k): v for k, v in t.items()})
    if color:
        s['text_color'] = color
    if ic_color:
        s['icon_color'] = ic_color
        # Elementor colours list icons via `fill`; Lucide icons are stroked, so bb.css maps this class to `stroke`
        key = ''.join(ch for ch in ic_color if ch.isalnum()).lower()
        LIST_ICON_COLORS.add((key, ic_color))
        kw['cls'] = (kw.get('cls', '') + ' bb-icc-' + key).strip()
    if space is not None:
        s['space_between'] = px(space)
    if align:
        s['icon_align'] = align
    return W('icon-list', kw.pop('name', 'Icon List'), **s, **kw)


def SPACER(h, **kw):
    return W('spacer', 'Spacer', space=px(h), **kw)


def DIV(**kw):
    return W('divider', kw.pop('name', 'Divider'), **kw)


# ---------------------------------------------------------------- persistence
def count(els):
    c = w = 0
    for e in els:
        if e['elType'] == 'container':
            c += 1
        else:
            w += 1
        a, b = count(e['elements'])
        c += a
        w += b
    return c, w


def _fix_inner(els, inner=False):
    for e in els:
        if e['elType'] == 'container':
            e['isInner'] = inner
            _fix_inner(e['elements'], True)


def save(kind, post_id, elements, page_settings=None, extra=None):
    """kind: 'pages' or 'elementor_library'."""
    _fix_inner(elements)
    meta = {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder'}
    if kind == 'pages':  # Astra: full-width, no title, no sidebar
        meta.update({'ast-site-content-layout': 'full-width-container', 'site-content-style': 'unboxed',
                     'site-sidebar-layout': 'no-sidebar', 'site-post-title': 'disabled', 'ast-breadcrumbs-content': 'disabled',
                     'ast-featured-img': 'disabled'})
    if page_settings is not None:
        meta['_elementor_page_settings'] = page_settings
    body = {'meta': meta}
    body.update(extra or {})
    d = wp.post(f'wp/v2/{kind}/{post_id}', body)
    if 'id' not in d:
        raise SystemExit(f'save {post_id} failed: {str(d)[:500]}')
    c, w = count(elements)
    print(f'saved {kind}/{post_id}: {c} containers, {w} widgets')
    return d


def regen(post_id):
    """Ask Elementor to rebuild the document's CSS (MCP update-page-settings triggers a proper document save)."""
    return wp.mcp('elementor/update-page-settings', {'post_id': post_id, 'settings': {}})
