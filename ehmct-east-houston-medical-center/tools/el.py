"""Helpers that emit classic Elementor (flexbox container) JSON."""
import json, random, os, subprocess

# Safety: only ever write to the EHMC site
_EXPECTED = os.environ.get('EHMC_EXPECTED_HOST', 'hotpink-lobster-615998.hostingersite.com')
if _EXPECTED not in os.environ.get('WP_URL', ''):
    raise SystemExit('Refusing to run: WP_URL is not ' + _EXPECTED)

MEDIA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media.json')))

def uid():
    return '%07x' % random.getrandbits(28)

def px(v, u='px'):
    return {'unit': u, 'size': v, 'sizes': []}

def dims(t, r=None, b=None, l=None, u='px'):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': u, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len({t, r, b, l}) == 1}

def gap(v, row=None):
    row = v if row is None else row
    return {'column': str(v), 'row': str(row), 'isLinked': v == row, 'unit': 'px', 'size': v}

def img(key):
    m = MEDIA[key]; return {'id': m['id'], 'url': m['url'], 'source': 'library'}

def icon(v, lib='fa-solid'):
    return {'value': v, 'library': lib}

def col(i): return 'globals/colors?id=' + i
def typ(i): return 'globals/typography?id=' + i

def shadow(y, blur, color, x=0, spread=0):
    return {'horizontal': x, 'vertical': y, 'blur': blur, 'spread': spread, 'color': color}

CARD_SHADOW = shadow(15, 35, 'rgba(12,30,58,0.12)')

TOK = {  # mirrors the kit's custom typography, used when a widget needs a local tweak
 'ehh1': ('Poppins', '700', 74, 0.92, -4, 'uppercase', 56, 40), 'ehh2': ('Poppins', '700', 56, 1.1, -2, None, 42, 32),
 'ehh4': ('Poppins', '700', 24, 1.35, None, None, 20, 18), 'ehh3': ('Poppins', '600', 18, 1.3, -0.6, None, 17, 17), 'ehserif': ('Gelasio', '700', 25, 1.05, None, None, 23, 22),
 'eheye': ('Poppins', '700', 12, 1.6, 2.4, 'uppercase', None, None), 'ehbody': ('Poppins', '400', 16, 1.65, None, None, None, 15),
 'ehsmall': ('Poppins', '400', 13.4, 1.6, None, None, None, None), 'ehlabel': ('Poppins', '600', 14, 1.5, None, None, None, None),
 'ehstat': ('Poppins', '600', 24, 1.1, None, None, None, None), 'ehbtn': ('Poppins', '700', 16, 1.2, None, None, None, None)}

def apply_typo(s, token, prefix='typography'):
    """Use the global token unless local typography overrides were passed; then inline the token as custom."""
    local = [k for k in s if k.startswith(prefix + '_') and k != prefix + '_typography']
    if not local:
        s.setdefault('g', {})[prefix + '_typography'] = typ(token); return s
    f, w, size, lh, ls, tr, t, m = TOK[token]
    base = {prefix + '_typography': 'custom', prefix + '_font_family': f, prefix + '_font_weight': w,
            prefix + '_font_size': px(size), prefix + '_line_height': px(lh, 'em')}
    if ls is not None: base[prefix + '_letter_spacing'] = px(ls)
    if tr: base[prefix + '_text_transform'] = tr
    if t: base[prefix + '_font_size_tablet'] = px(t)
    if m: base[prefix + '_font_size_mobile'] = px(m)
    base.update(s); s.clear(); s.update(base)
    return s

def _split_globals(s):
    g = s.pop('g', None)
    if g: s['__globals__'] = g
    return s

def C(title, children, /, inner=True, **s):
    """Flex container. Pass settings as kwargs; g={} for globals."""
    s = _split_globals(s)
    s['_title'] = title
    s.setdefault('content_width', 'full')
    return {'id': uid(), 'elType': 'container', 'isInner': inner, 'settings': s, 'elements': children}

def W(wtype, title, /, **s):
    s = _split_globals(s)
    s['_title'] = title
    return {'id': uid(), 'elType': 'widget', 'widgetType': wtype, 'settings': s, 'elements': []}

def H(title_html, tag='h2', typo='ehh2', color='primary', align=None, name=None, **s):
    apply_typo(s, typo); s.setdefault('g', {})
    if color: s['g']['title_color'] = col(color)
    if align: s['align'] = align
    if '<span' in title_html:
        # accent word uses the global red via Pro custom CSS
        s['custom_css'] = 'selector .elementor-heading-title span{color:var(--e-global-color-secondary);}'
    return W('heading', name or ('Heading – ' + title_html[:30]), title=title_html, header_size=tag, **s)

def T(html, typo='ehbody', color='text', align=None, name='Text', **s):
    apply_typo(s, typo); s.setdefault('g', {})
    if color: s['g']['text_color'] = col(color)
    if align: s['align'] = align
    return W('text-editor', name, editor=html, **s)

def EYEBROW(text, align='center', color='secondary', name=None):
    return W('divider', name or ('Eyebrow – ' + text), look='line_text', text=text, html_tag='span',
             width=px(len(text) * 9.6 + 80), align=align, text_align='left',
             weight=px(1.5), gap=px(2), text_spacing=px(12), style='solid',
             g={'color': col(color), 'text_color': col(color), 'typography_typography': typ('eheye')})

ARROW = icon('fas fa-arrow-right')

def BTN(text, url='#', name=None, style='primary', icon_=ARROW, align=None, **s):
    apply_typo(s, 'ehbtn'); s.setdefault('g', {})
    base = dict(text=text, link={'url': url, 'is_external': '', 'nofollow': ''},
                border_radius=dims(10), text_padding=dims(15, 26), icon_indent=px(10),
                hover_animation='float')
    if icon_:
        base.update(selected_icon=icon_, icon_align='row-reverse')
    if style == 'primary':
        s['g'].update({'background_color': col('secondary'), 'button_text_color': col('ehwhite'),
                       'button_background_hover_color': col('ehreddk'), 'hover_color': col('ehwhite')})
        base.update(button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(12, 28, 'rgba(158,63,66,0.26)'))
    elif style == 'outline-light':
        base.update(background_color='rgba(255,255,255,0.06)', border_border='solid', border_width=dims(1.5),
                    border_color='rgba(255,255,255,0.8)', button_background_hover_color='#FFFFFF', hover_color='#293A6E',
                    button_text_color='#FFFFFF', button_hover_border_color='#FFFFFF')
    if align: base['align'] = align
    base.update(s)
    return W('button', name or ('Button – ' + text), **base)

def section_head(eyebrow, title_html, sub=None, h='h2', maxw=760):
    items = [EYEBROW(eyebrow), H(title_html, h, align='center', name='Section Title')]
    if sub:
        items.append(T('<p>' + sub + '</p>', align='center', name='Section Intro',
                       _element_width='initial', _element_custom_width=px(maxw), _element_custom_width_tablet=px(100, '%')))
    return items

def put(post_id, elements, extra_meta=None, post_extra=None):
    meta = {'_elementor_data': json.dumps(elements), '_elementor_edit_mode': 'builder',
            '_elementor_version': '3.30.0', '_elementor_pro_version': '3.30.0'}
    meta.update(extra_meta or {})
    body = {'meta': {k: v for k, v in meta.items() if k.startswith('_elementor_data') or k in ('_elementor_edit_mode', '_elementor_page_settings', '_elementor_template_type')}}
    body.update(post_extra or {})
    path = 'pages' if (post_extra or {}).get('_type') != 'lib' else 'elementor_library'
    body.pop('_type', None)
    open('' + os.path.dirname(os.path.abspath(__file__)) + '/payload.json', 'w').write(json.dumps(body))
    r = subprocess.run(['curl', '-sS', '-X', 'POST', '-u', os.environ['WP_USER'] + ':' + os.environ['WP_APP_PASSWORD'],
                        '-H', 'Content-Type: application/json', '--data-binary',
                        '@' + os.path.dirname(os.path.abspath(__file__)) + '/payload.json',
                        os.environ['WP_URL'] + '/wp-json/wp/v2/' + path + '/' + str(post_id)], capture_output=True, text=True)
    d = json.loads(r.stdout)
    ok = 'id' in d
    print(post_id, 'saved' if ok else d)
    return d

def count(els):
    c = w = 0
    for e in els:
        if e['elType'] == 'container': c += 1
        else: w += 1
        a, b = count(e['elements']); c += a; w += b
    return c, w

def regen(post_id):
    """Save through Elementor's document API so it regenerates the post CSS."""
    d = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([d + '/mcp.sh', 'elementor/update-page-settings', json.dumps({'post_id': post_id, 'settings': {'hide_title': 'yes'}})],
                       capture_output=True, text=True)
    print(post_id, 'regen', '"success":true' in r.stdout)
