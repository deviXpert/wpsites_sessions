"""Helpers that emit classic Elementor (Flexbox Container) JSON using ONLY native widgets,
the Site Settings globals (kit 17) and the gs-* utility classes from templates/gs-global.css."""
import json, random, hashlib

_rng = random.Random(1)
def seed(s):
    """Stable element IDs per document (keeps Elementor's generated CSS valid between rebuilds)."""
    _rng.seed(int(hashlib.md5(s.encode()).hexdigest()[:8], 16))
def uid(): return '%07x' % _rng.getrandbits(28)

# ---------- value helpers ----------
def px(v, u='px'): return {'unit': u, 'size': v, 'sizes': []}
def dims(t, r=None, b=None, l=None, u='px'):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': u, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len({t, r, b, l}) == 1}
def gap(v, row=None):
    row = v if row is None else row
    return {'column': str(v), 'row': str(row), 'isLinked': v == row, 'unit': 'px', 'size': v}
def col(i): return 'globals/colors?id=' + i
def typ(i): return 'globals/typography?id=' + i
def ico(v, lib='fa-solid'): return {'value': v, 'library': lib}
def link(url, ext=False):
    """External links open in a new tab with rel=noopener noreferrer (security)."""
    return {'url': url, 'is_external': 'on' if ext else '', 'nofollow': '', 'custom_attributes': 'rel|noopener noreferrer' if ext else ''}
def shadow(y, blur, color, x=0, spread=0): return {'horizontal': x, 'vertical': y, 'blur': blur, 'spread': spread, 'color': color}

PLACEHOLDER = '/wp-content/plugins/elementor/assets/images/placeholder.png'
SHADOW_CARD = shadow(20, 50, 'rgba(2,6,23,0.45)')
SHADOW_HOVER = shadow(28, 60, 'rgba(6,132,196,0.28)')

def _g(s):
    g = s.pop('g', None)
    if g: s.setdefault('__globals__', {}).update(g)
    return s

# ---------- containers ----------
def C(title, children, /, **s):
    """Flex container. Defaults: full width, column. Pass Elementor container settings as kwargs."""
    s = _g(s); s['_title'] = title
    s.setdefault('content_width', 'full')
    s.setdefault('padding', dims(0))   # cancel Elementor's 10px default container padding (keeps edges aligned)
    return {'id': uid(), 'elType': 'container', 'isInner': False, 'settings': s, 'elements': children}

def ROW(title, children, gap_=24, wrap=False, stack='mobile', align='stretch', justify=None, **s):
    """Horizontal container that stacks on mobile (or tablet)."""
    s.update(flex_direction='row', flex_gap=gap(gap_), flex_align_items=align)
    if justify: s['flex_justify_content'] = justify
    if wrap: s['flex_wrap'] = 'wrap'
    s['flex_direction_mobile'] = 'column'
    if stack == 'tablet': s['flex_direction_tablet'] = 'column'
    return C(title, children, **s)

def COL(title, children, w=None, wt=None, wm=100, gap_=20, **s):
    """Column child of a ROW with width in % per device."""
    s.setdefault('flex_direction', 'column'); s.setdefault('flex_gap', gap(gap_))
    if w is not None:
        s['width'] = px(w, '%')
        if wt is not None: s['width_tablet'] = px(wt, '%')
        s['width_mobile'] = px(wm, '%')
    return C(title, children, **s)

def GRID(title, children, cols=3, cols_t=2, cols_m=1, gap_=24, **s):
    """Native CSS Grid container (Elementor Container → Grid)."""
    s.update(container_type='grid',
             grid_columns_grid={'unit': 'fr', 'size': cols, 'sizes': []},
             grid_columns_grid_tablet={'unit': 'fr', 'size': cols_t, 'sizes': []},
             grid_columns_grid_mobile={'unit': 'fr', 'size': cols_m, 'sizes': []},
             grid_rows_grid={'unit': 'fr', 'size': 1, 'sizes': []},
             grid_auto_flow='row', grid_gaps=gap(gap_))
    return C(title, children, **s)

def BG_SECTION(variant='a'):
    """Native radial-gradient 'blob' backgrounds (no images, no CSS): bg + overlay."""
    v = {
      'a': ('rgba(124,92,255,0.30)', 'top left', 'rgba(6,132,196,0.28)', 'bottom right'),
      'b': ('rgba(6,132,196,0.30)', 'top right', 'rgba(124,92,255,0.22)', 'bottom left'),
      'c': ('rgba(93,176,216,0.18)', 'center center', 'rgba(124,92,255,0.18)', 'top right'),
    }[variant]
    return dict(background_background='gradient', background_color=v[0], background_color_stop=px(0, '%'),
                background_color_b='#070B1F', background_color_b_stop=px(55, '%'),
                background_gradient_type='radial', background_gradient_position=v[1],
                background_overlay_background='gradient', background_overlay_color=v[2],
                background_overlay_color_stop=px(0, '%'), background_overlay_color_b='rgba(7,11,31,0)',
                background_overlay_color_b_stop=px(50, '%'), background_overlay_gradient_type='radial',
                background_overlay_gradient_position=v[3], background_overlay_opacity=px(1, ''))

def SECTION(title, children, anchor=None, bg=None, pad=(112, 88, 64), tag='section', gap_=48, **s):
    """Top-level page section: full-width outer + boxed inner (width from Site Settings)."""
    outer = dict(content_width='full', html_tag=tag, flex_direction='column',
                 padding=dims(pad[0], 0, pad[0], 0), padding_tablet=dims(pad[1], 0, pad[1], 0), padding_mobile=dims(pad[2], 0, pad[2], 0))
    if bg: outer.update(BG_SECTION(bg) if isinstance(bg, str) else bg)
    if anchor: outer['_element_id'] = anchor
    outer.update(s)
    inner = C(title + ' – Inner', children, content_width='boxed', flex_direction='column', flex_gap=gap(gap_),
              padding=dims(0, 24), padding_mobile=dims(0, 16))
    inner['isInner'] = True
    return C(title, [inner], **outer)

def GLASS(title, children, strong=False, pad=(32, 28, 24), radius=20, hover=False, cls='', **s):
    """Glass card. Fill/border/radius/shadow are native controls; .gs-glass adds only the blur."""
    s.setdefault('flex_direction', 'column'); s.setdefault('flex_gap', gap(16))
    s.update(background_background='classic',
             border_border='solid', border_width=dims(1), border_radius=dims(radius),
             box_shadow_box_shadow_type='yes', box_shadow_box_shadow=SHADOW_CARD,
             padding=dims(pad[0]), padding_tablet=dims(pad[1]), padding_mobile=dims(pad[2]),
             css_classes=(('gs-glass--strong' if strong else 'gs-glass') + (' ' + cls if cls else '')).strip())
    s.setdefault('g', {}).update(background_color=col('gsglass2' if strong else 'gsglass'), border_color=col('gsline'))
    if hover:
        s.update(_transform_translateY_popover_hover='transform', _transform_translateY_effect_hover=px(-6),
                 _transform_transition_hover=px(300, 'ms'),
                 border_hover_border='solid', border_hover_width=dims(1), border_hover_transition=px(0.3, 's'),
                 box_shadow_hover_box_shadow_type='yes', box_shadow_hover_box_shadow=SHADOW_HOVER)
        s['g']['border_hover_color'] = col('accent')
    return C(title, children, **s)

# ---------- widgets ----------
def W(wtype, title, /, **s):
    s = _g(s); s['_title'] = title
    return {'id': uid(), 'elType': 'widget', 'widgetType': wtype, 'settings': s, 'elements': []}

def H(text, tag='h2', t='gsh2', color='gswhite', align=None, grad=None, name=None, **s):
    """Heading. Words wrapped in <span> get the brand gradient via .gs-grad."""
    s.setdefault('g', {}).update(typography_typography=typ(t), title_color=col(color))
    if align: s.update(align=align)
    if grad is None: grad = '<span>' in text
    if grad: s['_css_classes'] = (s.get('_css_classes', '') + ' gs-grad').strip()
    return W('heading', name or f'{tag.upper()} – {text[:40]}', title=text, header_size=tag, **s)

def EYEBROW(text, align=None, name=None):
    return H(text, 'p', 'gseyebrow', 'accent', align, False, name or f'Eyebrow – {text}')

def P(html, t='gsbody', color='text', align=None, name='Text', maxw=None, **s):
    s.setdefault('g', {}).update(typography_typography=typ(t), text_color=col(color))
    if align: s['align'] = align
    if maxw:
        s.update(_element_width='initial', _element_custom_width=px(maxw), _element_custom_width_tablet=px(100, '%'))
    if not html.lstrip().startswith('<'): html = f'<p>{html}</p>'
    return W('text-editor', name, editor=html, **s)

def BTN(text, url, style='primary', icon='fas fa-arrow-right', align=None, name=None, ext=False, size='md', **s):
    """primary = global violet pill (Site Settings → Buttons). ghost = glass outline pill."""
    b = dict(text=text, link=link(url, ext), size=size, hover_animation='float')
    if icon: b.update(selected_icon=ico(icon), icon_align='row-reverse', icon_indent=px(10))
    if style == 'ghost':
        b.update(border_border='solid', border_width=dims(1))
        b['g'] = dict(background_color=col('gsglass2'), border_color=col('gsline'), button_text_color=col('gswhite'),
                      button_background_hover_color=col('gswhite'), hover_color=col('gsnavy'))
    if style in ('primary', 'ghost') and size == 'md':
        b['align_mobile'] = 'justify'   # full-width, easy-to-tap buttons on phones
    if style in ('ghost', 'link'):  # cancel the global violet glow shadow
        b.update(button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(0, 0, 'rgba(0,0,0,0)'))
    if align: b['align'] = align
    b.update(s)
    return W('button', name or f'Button – {text}', **b)

def ICONBOX(icon, title, desc, url=None, tag='h3', name=None, **s):
    """Service / feature card content (put inside GLASS)."""
    b = dict(selected_icon=ico(icon), view='stacked', shape='rounded', title_text=title, description_text=desc,
             title_size=tag, position='top', text_align='left', icon_size=px(26), icon_padding=px(16),
             border_radius=dims(14), icon_space=px(20), title_bottom_space=px(10))
    b['position_mobile'] = 'top'
    if url: b['link'] = link(url)
    b['g'] = dict(primary_color=col('gsglass2'), secondary_color=col('accent'),
                  title_color=col('gswhite'), title_typography_typography=typ('gsh3'),
                  description_color=col('text'), description_typography_typography=typ('gsbody'))
    b.update(s)
    return W('icon-box', name or f'Icon Box – {title}', **b)

def ICONLIST(items, inline=False, icon='fas fa-check-circle', t='gsbody', color='text', icolor='accent', name='Icon List', links=None, **s):
    lst = []
    for i, it in enumerate(items):
        txt, ic = (it if isinstance(it, tuple) else (it, icon))
        d = {'_id': uid(), 'text': txt, 'selected_icon': ico(ic, 'fa-brands' if ic.startswith('fab') else 'fa-solid')}
        if links and links[i]: d['link'] = link(links[i])
        lst.append(d)
    b = dict(icon_list=lst, view='inline' if inline else 'traditional', icon_size=px(16), text_indent=px(10),
             space_between=px(12 if not inline else 28))
    b['g'] = dict(icon_color=col(icolor), text_color=col(color), icon_typography_typography=typ(t), text_color_hover=col('gswhite'))
    b.update(s)
    return W('icon-list', name, **b)

def COUNTER(n, title, suffix='+', name=None):
    return W('counter', name or f'Counter – {title}', starting_number=0, ending_number=n, suffix=suffix, title=title,
             duration=1600, thousand_separator='yes', title_tag='p', number_alignment='start', title_horizontal_alignment='start',
             g=dict(number_color=col('gswhite'), typography_number_typography=typ('gsstat'),
                    title_color=col('text'), typography_title_typography=typ('gsbody')))

def IMG(label, size, alt, name=None, radius=18, **s):
    """Labelled image placeholder – replace in Media Library later (see docs/06-checklist.md)."""
    return W('image', name or f'📷 PLACEHOLDER – {label} ({size})', image={'url': PLACEHOLDER, 'id': '', 'alt': alt, 'source': 'library'},
             image_size='large', image_border_radius=dims(radius), caption_source='none', **s)

def DIVIDER(name='Divider'):
    return W('divider', name, style='solid', weight=px(1), gap=px(4), g=dict(color=col('gsline')))

def SPACER(h=24): return W('spacer', 'Spacer', space=px(h))

def FAQ(items, name='FAQ – Accordion'):
    """Nested Accordion with FAQ Schema (structured data for Google) – native setting."""
    its, kids = [], []
    for q, a in items:
        its.append({'_id': uid(), 'item_title': q})
        kids.append(C(f'FAQ – {q[:30]}', [P(a, name='Answer')], padding=dims(4, 22, 20, 22)))
    for k in kids: k['isInner'] = True
    w = W('nested-accordion', name, items=its, faq_schema='yes', title_tag='h3', default_state='expanded',
          max_items_expended='one', accordion_item_title_space_between=px(14), accordion_item_title_distance_from_content=px(0),
          accordion_background_normal_background='classic', accordion_border_normal_border='solid',
          accordion_border_normal_width=dims(1), accordion_border_radius=dims(16), accordion_padding=dims(20, 22),
          accordion_background_hover_background='classic', accordion_background_active_background='classic',
          content_background_background='classic', icon_size=px(14),
          content_border_border='solid', content_border_width=dims(0, 1, 1, 1), content_border_radius=dims(0, 0, 16, 16), title_text_shadow_text_shadow_type='',
          icon_section_icon=ico('fas fa-plus'), icon_section_active_icon=ico('fas fa-minus'),
          g=dict(accordion_background_normal_color=col('gsglass'), accordion_background_hover_color=col('gsglass2'),
                 accordion_background_active_color=col('gsglass2'), accordion_border_normal_color=col('gsline'),
                 title_typography_typography=typ('gsh4'), normal_title_color=col('gswhite'),
                 hover_title_color=col('accent'), active_title_color=col('accent'),
                 icon_color=col('accent'), icon_active_color=col('accent'), content_border_color=col('gsline')))
    w['elements'] = kids
    w['elType'] = 'widget'
    return w

def TEMPLATE(template_id, name):
    """Embed a saved template (single source of truth, e.g. the CTA band)."""
    return W('template', name, template_id=str(template_id))

def FORM(name='Lead Form', fields=('name', 'email', 'phone', 'services', 'message'), button='Get My Free Proposal',
         form_name='Website Lead', email_to='info@graphicsstormstudio.com'):
    """Elementor Pro Form – inherits Site Settings → Form Fields + Buttons. Honeypot = bot protection."""
    F = {
     'name': dict(field_type='text', field_label='Full name', placeholder='Your full name', required='true', width='50', custom_id='name', autocomplete='name'),
     'email': dict(field_type='email', field_label='Email', placeholder='you@company.com', required='true', width='50', custom_id='email'),
     'phone': dict(field_type='tel', field_label='Phone / WhatsApp', placeholder='+1 (555) 000-0000', width='50', custom_id='phone'),
     'company': dict(field_type='text', field_label='Website (optional)', placeholder='https://', width='50', custom_id='website'),
     'budget': dict(field_type='select', field_label='Monthly budget', field_options='Select a range\nUnder $1,000\n$1,000 – $3,000\n$3,000 – $10,000\n$10,000+', width='50', custom_id='budget'),
     'services': dict(field_type='checkbox', field_label='Services you need', inline_list='elementor-subgroup-inline',
                      field_options='Website Development\nSEO\nSocial Media Marketing\nGraphic Design\nLogo & Branding\nPaid Ads', width='100', custom_id='services'),
     'message': dict(field_type='textarea', field_label='Project details', placeholder='Tell us about your goals…', rows='4', width='100', custom_id='message'),
    }
    lst = []
    for f in fields:
        d = dict(F[f]); d['_id'] = uid(); lst.append(d)
    lst.append({'_id': uid(), 'custom_id': 'hp', 'field_type': 'honeypot', 'field_label': '', 'width': '100'})
    return W('form', name, form_name=form_name, form_fields=lst, show_labels='yes', mark_required='yes',
             input_size='md', button_text=button, button_size='md', button_width='100',
             selected_button_icon=ico('fas fa-paper-plane'), button_icon_align='row-reverse', button_icon_indent=px(10),
             submit_actions=['email', 'collect_submissions'], email_to=email_to,
             email_subject='New enquiry from graphicsstormstudio.com', email_content='[all-fields]',
             email_from_name='Graphics Storm Studio Website', email_reply_to='email',
             success_message='Thank you! We received your request and will reply within 1 business day.',
             error_message='Something went wrong – please email info@graphicsstormstudio.com.',
             required_field_message='This field is required.', invalid_message='Please check this field.',
             column_gap=px(16), row_gap=px(16), label_spacing=px(8), _css_classes='gs-form',
             button_border_radius=dims(999),
             g=dict(label_color=col('text'), label_typography_typography=typ('gssmall'),
                    field_text_color=col('gswhite'), field_background_color=col('gsglass'), field_border_color=col('gsline'),
                    button_background_color=col('secondary'), button_background_hover_color=col('gsvioletdk'),
                    button_text_color=col('gswhite'), button_typography_typography=typ('gsbtn')),
             field_border_radius=dims(12), field_border_width=dims(1))

def section_head(eyebrow, title, intro=None, align='center', tag='h2', maxw=720):
    kids = [EYEBROW(eyebrow, align), H(title, tag, 'gsh2' if tag == 'h2' else 'gsh1', align=align, name='Section Title')]
    if intro: kids.append(P(intro, 'gslead', align=align, name='Section Intro', maxw=maxw))
    return C('Section Head', kids, flex_direction='column', flex_gap=gap(14),
             flex_align_items='center' if align == 'center' else 'flex-start')

def count(els):
    c = w = 0
    for e in els:
        if e['elType'] == 'container': c += 1
        else: w += 1
        a, b = count(e['elements']); c += a; w += b
    return c, w

def template_json(title, ttype, content, page_settings=None):
    """Elementor 'Saved Templates → Import' file format."""
    return {'title': title, 'type': ttype, 'version': '0.4', 'page_settings': page_settings or {}, 'content': content}

def finalize(els, top=True):
    for e in els:
        if e['elType'] == 'container': e['isInner'] = not top
        finalize(e['elements'], False)
    return els
