"""Helpers that emit classic Elementor (flexbox/grid container + native widget) JSON for the Quality Waterproofing site.
Styling uses native widget controls + Global Colors / Global Fonts from the kit (kit.py). No per-widget custom CSS.
The only extra CSS lives in the Elementor Custom Code snippet (see snippet.py)."""
import json, random, os, subprocess, zlib
import wp

D = os.path.dirname(os.path.abspath(__file__))
MEDIA = json.load(open(os.path.join(D, 'media.json')))
PAGES = json.load(open(os.path.join(D, 'pages.json')))
U = wp.U
PHONE, TEL = '(437) 264-2664', 'tel:+14372642664'
EMAIL = 'waterproofingquality@gmail.com'
TAGLINE = "Our company will help protect your home's basement from water damage"

def seed(s): random.seed(zlib.crc32(s.encode()))  # stable element IDs per page
def uid(): return '%07x' % random.getrandbits(28)
def px(v, u='px'): return {'unit': u, 'size': v, 'sizes': []}
def dims(t, r=None, b=None, l=None, u='px'):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': u, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len({t, r, b, l}) == 1}
def gap(c, r=None):
    r = c if r is None else r
    return {'column': str(c), 'row': str(r), 'isLinked': c == r, 'unit': 'px', 'size': c}
def col(i): return 'globals/colors?id=' + i
def typ(i): return 'globals/typography?id=' + i
def ico(v, lib='fa-solid'): return {'value': v, 'library': lib}
def img(k, size=None): m = MEDIA[k]; return {'id': m['id'], 'url': m['url'], 'source': 'library', 'size': ''}
def link(u, ext=False): return {'url': u, 'is_external': 'on' if ext else '', 'nofollow': ''}
def page_url(slug): return U + '/' + ('' if slug == 'home' else slug + '/')
def shadow(y, blur, color, x=0, spread=0): return {'horizontal': x, 'vertical': y, 'blur': blur, 'spread': spread, 'color': color}

def _g(s):
    g = s.pop('g', None)
    if g: s['__globals__'] = {**s.get('__globals__', {}), **g}
    return s

def C(children, title='Container', inner=True, **s):
    """Flex container (column by default). Use row=True for a row; grid=N for a CSS grid of N columns."""
    row = s.pop('row', False); grid = s.pop('grid', None)
    s.setdefault('content_width', 'full')
    if inner: s.setdefault('padding', dims(0))  # no default 10px inset on nested containers
    if grid:
        t, m = s.pop('grid_t', min(grid, 2)), s.pop('grid_m', 1)
        for k, v in dict(container_type='grid', grid_columns_grid=px(grid, 'fr'), grid_columns_grid_tablet=px(t, 'fr'), grid_columns_grid_mobile=px(m, 'fr'),
                         grid_rows_grid=px(1, 'fr'), grid_rows_grid_tablet=px(1, 'fr'), grid_rows_grid_mobile=px(1, 'fr'), grid_auto_flow='row').items():
            s.setdefault(k, v)
        s.setdefault('grid_gaps', gap(24))
    else:
        s.setdefault('flex_direction', 'row' if row else 'column')
        if row: s.setdefault('flex_direction_mobile', 'column')
    s['_title'] = title
    return {'id': uid(), 'elType': 'container', 'isInner': inner, 'settings': _g(s), 'elements': children}

def SECTION(children, title, bg='white', pad=(100, 90, 64), **s):
    """Top-level section: full-width outer + boxed inner content width (kit container width)."""
    bgs = {'white': col('qwwhite'), 'cream': col('qwcream'), 'light': col('qwlight'), 'ink': col('primary'), 'ink2': col('qwink2')}
    s.setdefault('g', {})
    if bg in bgs:
        s['background_background'] = 'classic'; s['g']['background_color'] = bgs[bg]
    if bg in ('ink', 'ink2'): s['css_classes'] = (s.get('css_classes', '') + ' qw-dark').strip()
    d, t, m = pad
    s.setdefault('padding', dims(d, 20)); s.setdefault('padding_tablet', dims(t, 20)); s.setdefault('padding_mobile', dims(m, 16))
    s.setdefault('html_tag', 'section')
    s.setdefault('flex_gap', gap(20))
    return C(children, title, inner=False, content_width='boxed', **s)

def W(t, _name, /, **s):
    s['_title'] = _name
    return {'id': uid(), 'elType': 'widget', 'widgetType': t, 'settings': _g(s), 'elements': []}

# ---------- text ----------
def H(text, tag='h2', typo='qwh2', color='primary', align=None, **s):
    s.setdefault('g', {}).update(typography_typography=typ(typo), title_color=col(color))
    if align: s['align'] = align
    return W('heading', 'Heading: ' + text.split('<')[0][:40], title=text, header_size=tag, **s)

def EYE(text, color='qwgolddk', align=None, **s):
    """Small serif eyebrow above section titles (not a heading tag)."""
    s.setdefault('g', {}).update(typography_typography=typ('qweye'), title_color=col(color))
    if align: s['align'] = align
    return W('heading', 'Eyebrow: ' + text[:30], title=text, header_size='p', **s)

def T(html, color='text', typo='qwbody', align=None, **s):
    if not html.lstrip().startswith('<'): html = '<p>' + html + '</p>'
    s.setdefault('g', {}).update(typography_typography=typ(typo), text_color=col(color))
    if align: s['align'] = align
    return W('text-editor', 'Text', editor=html, **s)

def LINE(color='secondary', width=64, align='left'):
    return W('divider', 'Gold Line', style='solid', weight=px(3), width=px(width), align=align, gap=px(2), g={'color': col(color)})

def HEAD(eyebrow, title, intro=None, align='left', dark=False, tag='h2', maxw=760):
    a = None if align == 'left' else align
    out = [EYE(eyebrow, color='secondary' if dark else 'qwgolddk', align=a), H(title, tag, color='qwwhite' if dark else 'primary', align=a)]
    if intro:
        out.append(T(intro, color='qwmuted' if dark else 'text', typo='qwlead', align=a,
                     _element_width='initial', _element_custom_width=px(maxw), _element_custom_width_tablet=px(100, '%')))
    if align == 'center':
        return [C(out, 'Section Head', flex_align_items='center', flex_gap=gap(14))]
    return [C(out, 'Section Head', flex_gap=gap(14))]

# ---------- buttons ----------
def BTN(text, url, style='gold', icon='fas fa-arrow-right', align=None, size='md', **s):
    base = dict(text=text, link=link(url), border_radius=dims(4), text_padding=dims(17, 30) if size == 'md' else dims(13, 22),
                icon_indent=px(10), hover_animation='grow' if style == 'gold' else '', selected_icon=ico(icon), icon_align='row-reverse' if 'arrow' in icon else 'row')
    g = {'typography_typography': typ('qwbtn')}
    if style == 'gold':
        g.update(background_color=col('secondary'), button_text_color=col('primary'), button_background_hover_color=col('qwgoldlt'), hover_color=col('primary'))
        base.update(button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(10, 26, 'rgba(201,162,75,0.30)'))
    elif style == 'ghost':  # on dark backgrounds
        base.update(background_color='rgba(255,255,255,0.04)', border_border='solid', border_width=dims(1), border_color='rgba(255,255,255,0.45)', button_hover_border_color='#C9A24B')
        g.update(button_text_color=col('qwwhite'), hover_color=col('secondary'))
    elif style == 'ink':
        g.update(background_color=col('primary'), button_text_color=col('qwwhite'), button_background_hover_color=col('accent'), hover_color=col('qwwhite'))
    elif style == 'outline':  # on light backgrounds
        base.update(background_color='rgba(0,0,0,0)', border_border='solid', border_width=dims(1.5), button_hover_border_color='#0E1420')
        g.update(button_text_color=col('primary'), border_color=col('primary'), button_background_hover_color=col('primary'), hover_color=col('qwwhite'))
    if align: base['align'] = align
    base.update(s); base.setdefault('g', {}).update(g)
    return W('button', 'Button: ' + text[:30], **base)

def CTA_BTNS(dark=True, align=None, quote_url='#estimate'):
    mob = dict(align_mobile='justify', _element_width_mobile='inherit', text_padding_mobile=dims(16, 20))
    return C([BTN('Get a Free Estimate', quote_url, 'gold', 'fas fa-clipboard-check', **mob),
              BTN('Call ' + PHONE, TEL, 'ghost' if dark else 'outline', 'fas fa-phone-alt', **mob)], 'Buttons', row=True, flex_wrap='wrap',
             flex_gap=gap(14), flex_direction_mobile='row', flex_justify_content=align or 'flex-start', flex_justify_content_mobile='flex-start')

# ---------- lists & boxes ----------
def ILIST(items, color='text', icon_color='secondary', inline=False, icon='fas fa-check-circle', size=17, typo='qwbody', gapv=12, **s):
    lst = []
    for it in items:
        if isinstance(it, tuple):
            t, i, u = (it + (None,))[:3]
        else:
            t, i, u = it, icon, None
        e = {'_id': uid(), 'text': t, 'selected_icon': ico(i)}
        if u: e['link'] = link(u)
        lst.append(e)
    s.setdefault('g', {}).update(icon_color=col(icon_color), text_color=col(color), icon_typography_typography=typ(typo))
    return W('icon-list', 'Icon List', icon_list=lst, view='inline' if inline else 'traditional', icon_size=px(size), text_indent=px(10),
             space_between=px(gapv), **s)

def IBOX(icon, title, desc, dark=False, pos='top', view='stacked', align='left', link_url=None, tag='h3', icon_size=None, **s):
    g = {'title_typography_typography': typ('qwh3'), 'description_typography_typography': typ('qwbody'),
         'title_color': col('qwwhite' if dark else 'primary'), 'description_color': col('qwmuted' if dark else 'text')}
    if view == 'stacked': g.update(primary_color=col('secondary'), secondary_color=col('primary'))
    else: g.update(primary_color=col('secondary'))
    s.setdefault('g', {}).update(g)
    if link_url: s['link'] = link(link_url)
    return W('icon-box', 'Icon Box: ' + title[:30], selected_icon=ico(icon), title_text=title, description_text=desc, position=pos, view=view,
             shape='square', icon_size=icon_size or px(24 if view == 'stacked' else 34), icon_padding=px(16), icon_space=px(18), title_bottom_space=px(10),
             text_align=align, title_size=tag, border_radius=dims(4), **s)

def CARD(children, dark=False, title='Card', pad=34, **s):
    s.setdefault('g', {})['background_color'] = col('qwink2' if dark else 'qwwhite')
    st = dict(background_background='classic', padding=dims(pad), padding_mobile=dims(26), border_radius=dims(6), flex_gap=gap(14))
    if not dark:
        st['css_classes'] = 'qw-light'
        st.update(border_border='solid', border_width=dims(1), border_color='#E3E6EC',
                  box_shadow_box_shadow_type='yes', box_shadow_box_shadow=shadow(18, 40, 'rgba(14,20,32,0.07)'))
    else:
        st.update(border_border='solid', border_width=dims(1), border_color='#2A3448')
    st.update(s)
    return C(children, title, **st)

def IMG(k, h=None, radius=6, size='large', hm=None, **s):
    st = dict(image=img(k), image_size=size, image_border_radius=dims(radius), width=px(100, '%'))
    if h:
        st.update(height=px(h), height_mobile=px(hm or int(h * 0.75)))
        # Elementor's control id is 'object-fit' (hyphen) – set every breakpoint so photos crop instead of squashing
        st.update({'object-fit': 'cover', 'object-fit_tablet': 'cover', 'object-fit_mobile': 'cover', 'object-position': 'center center'})
    st.update(s)
    return W('image', 'Image: ' + k, **st)

def SERVICE_CARD(k, title, desc, url, label='Learn More', h=440):
    """Pro Call-to-Action widget, cover skin: photo card with overlay + button."""
    return W('call-to-action', 'Service Card: ' + title, skin='cover', bg_image=img(k), bg_image_size='large',
             title=title, title_tag='h3', description=desc, button=label, link=link(url), link_click='button',
             alignment='left', vertical_position='bottom', **{'min-height': px(h), 'min-height_mobile': px(int(h*0.8))},
             transformation='zoom-in', effect_duration=900, content_animation='',
             overlay_color='rgba(14,20,32,0.55)', overlay_color_hover='rgba(14,20,32,0.80)',
             title_color='#FFFFFF', description_color='#D8DEE8', button_text_color='#0E1420', button_background_color='#C9A24B',
             button_border_color='#C9A24B', button_border_width=px(1), button_border_radius=px(4), button_hover_background_color='#E8CC84',
             button_hover_text_color='#0E1420', button_hover_border_color='#E8CC84',
             padding=dims(30), button_size='sm',
             g={'title_typography_typography': typ('qwh3'), 'description_typography_typography': typ('qwsmall'), 'button_typography_typography': typ('qwbtn')})

def STEPS(steps, dark=True):
    cards = []
    for i, (t, d) in enumerate(steps, 1):
        cards.append(CARD([
            H(f'{i:02d}', 'div', 'qwstat', 'secondary'),
            H(t, 'h3', 'qwh3', 'qwwhite' if dark else 'primary'),
            T(d, 'qwmuted' if dark else 'text', 'qwsmall'),
        ], dark=dark, title='Step ' + str(i), pad=30))
    return C(cards, 'Steps Grid', grid=len(steps) if len(steps) <= 4 else 3, grid_t=2, grid_gaps=gap(22))

def COUNTER(n, suffix, title, dark=True):
    return W('counter', 'Counter: ' + title, starting_number=0, ending_number=n, suffix=suffix, title=title, duration=1800,
             g={'number_color': col('secondary'), 'title_color': col('qwmuted' if dark else 'text'),
                'typography_number_typography': typ('qwstat'), 'typography_title_typography': typ('qwsmall')})

def FAQ(items):
    return W('accordion', 'FAQ Accordion', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': a} for q, a in items],  # no <p>: its margin left a gap under answers
             faq_schema='yes', selected_icon=ico('fas fa-plus'), selected_active_icon=ico('fas fa-minus'), title_html_tag='h3', icon_align='right',
             border_width=px(1), border_color='#E3E6EC', title_padding=dims(22, 28), title_padding_mobile=dims(18, 20), content_padding=dims(0, 28, 24, 28), content_padding_mobile=dims(0, 20, 20, 20),
             g={'title_color': col('primary'), 'tab_active_color': col('qwgolddk'), 'icon_color': col('secondary'), 'icon_active_color': col('qwgolddk'),
                'title_background': col('qwwhite'), 'content_background_color': col('qwwhite'), 'content_color': col('text'),
                'title_typography_typography': typ('qwh3'), 'content_typography_typography': typ('qwbody')})

def FORM(name='Free Estimate Request', compact=False, service_default=None):
    opts = 'Exterior Waterproofing\nInterior Waterproofing\nSump Pump Installation\nFoundation Crack Repair\nInterlocking\nNot sure – need an inspection'
    fields = [
        {'_id': uid(), 'custom_id': 'name', 'field_type': 'text', 'field_label': 'Full Name', 'placeholder': 'Your name', 'required': 'true', 'width': '50', 'width_mobile': '100'},
        {'_id': uid(), 'custom_id': 'phone', 'field_type': 'tel', 'field_label': 'Phone', 'placeholder': '(___) ___-____', 'required': 'true', 'width': '50', 'width_mobile': '100'},
        {'_id': uid(), 'custom_id': 'email', 'field_type': 'email', 'field_label': 'Email', 'placeholder': 'you@email.com', 'required': 'true', 'width': '100'},
        {'_id': uid(), 'custom_id': 'city', 'field_type': 'select', 'field_label': 'Your City', 'field_options': 'Toronto\nMississauga\nBrampton\nSt. Catharines\nNorth Bay\nOther city', 'width': '50', 'width_mobile': '100'},
        {'_id': uid(), 'custom_id': 'service', 'field_type': 'select', 'field_label': 'Service Needed', 'field_options': opts, 'width': '50', 'width_mobile': '100'},
    ]
    if not compact:
        fields.append({'_id': uid(), 'custom_id': 'message', 'field_type': 'textarea', 'field_label': 'Tell Us About the Problem', 'placeholder': 'Where is the water coming in? When did it start?', 'rows': 3, 'width': '100'})
    return W('form', 'Form: ' + name, form_name=name, form_fields=fields, input_size='md', show_labels='yes', mark_required='yes',
             button_text='Request My Free Estimate', button_size='md', button_width='100', selected_button_icon=ico('fas fa-paper-plane'), button_icon_align='row-reverse', button_icon_indent=px(10),
             submit_actions=['save-to-database', 'email'], email_subject='New estimate request – Quality Waterproofing website',
             success_message="Thanks! We've received your request and will call you shortly to book your free estimate.",
             column_gap=px(14), row_gap=px(14), label_spacing=px(6), button_border_radius=dims(4),
             g={'button_background_color': col('secondary'), 'button_text_color': col('primary'), 'button_background_hover_color': col('qwgoldlt'), 'button_hover_color': col('primary'),
                'button_typography_typography': typ('qwbtn'), 'label_color': col('primary'), 'label_typography_typography': typ('qwsmall')})

def SPACER(h): return W('spacer', 'Spacer', space=px(h))

# ---------- write / regenerate ----------
def put(post_id, elements, kind='pages', extra=None, settings=None):
    body = {'meta': {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page' if kind == 'pages' else extra.pop('_ttype')}}
    if settings is not None: body['meta']['_elementor_page_settings'] = settings
    if extra: body.update(extra)
    d = wp.req(f'wp/v2/{kind}/{post_id}', 'POST', body)
    print(post_id, 'saved' if 'id' in d else d)
    return d

def mcp(ability, params):
    r = subprocess.run([D + '/mcp.sh', ability, json.dumps(params)], capture_output=True, text=True)
    return r.stdout

def clear_cache(): print('clear-cache', mcp('elementor/clear-cache', {})[:120])

def cols(spec): return {'unit': 'custom', 'size': spec, 'sizes': []}
