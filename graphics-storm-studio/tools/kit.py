"""Graphics Storm Studio – Elementor Site Settings (Default Kit, post 17).
Run:  python3 kit.py          -> merges these settings into the live kit
      python3 kit.py --dry    -> only writes ../templates/site-settings.json
Every value here maps 1:1 to a field in Elementor → Site Settings (see docs/01-design-spec.md)."""
import json, os, sys
import wp

KIT_ID = 17
HERE = os.path.dirname(os.path.abspath(__file__))
def px(v, u='px'): return {'unit': u, 'size': v, 'sizes': []}
def dims(t, r=None, b=None, l=None, u='px'):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': u, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len({t, r, b, l}) == 1}
def C(i, t, c): return {'_id': i, 'title': t, 'color': c}
def typo(_id, title, fam, w, size=None, lh=None, ls=None, tr=None, t=None, m=None, lhu='em'):
    d = {'_id': _id, 'title': title, 'typography_typography': 'custom', 'typography_font_family': fam, 'typography_font_weight': str(w)}
    if size: d['typography_font_size'] = px(size)
    if t: d['typography_font_size_tablet'] = px(t)
    if m: d['typography_font_size_mobile'] = px(m)
    if lh is not None: d['typography_line_height'] = px(lh, lhu)
    if ls is not None: d['typography_letter_spacing'] = px(ls)
    if tr: d['typography_text_transform'] = tr
    return d

HEAD, BODY = 'Sora', 'Inter'
NAVY, NAVY2, BLUE, SKY, VIOLET, VIOLET_DK = '#070B1F', '#0E1738', '#0684C4', '#5DB0D8', '#7052FF', '#5B3BE0'
WHITE, TEXT, MUTED = '#FFFFFF', '#C9D3E8', '#93A1BF'

S = {
 'system_colors': [C('primary', 'Brand Blue', BLUE), C('secondary', 'Accent Violet (CTA)', VIOLET),
                   C('text', 'Body Text', TEXT), C('accent', 'Light Blue', SKY)],
 'custom_colors': [
   C('gsnavy', 'Navy – Page Background', NAVY), C('gsnavy2', 'Navy – Raised Surface', NAVY2),
   C('gswhite', 'White – Headings', WHITE), C('gsmuted', 'Muted Text', MUTED),
   C('gsvioletdk', 'Violet – Hover', VIOLET_DK),
   C('gsglass', 'Glass Fill (6% white)', '#FFFFFF0F'), C('gsglass2', 'Glass Fill Strong (10% white)', '#FFFFFF1A'),
   C('gsline', 'Glass Border (14% white)', '#FFFFFF24'),
   C('gsvioletglow', 'Violet Glow (blob)', '#7C5CFF59'), C('gsblueglow', 'Blue Glow (blob)', '#0684C44D'),
   C('gstransparent', 'Transparent', '#070B1F00'),
   C('gsgold', 'Star Gold (ratings)', '#FFC857'),
 ],
 'system_typography': [typo('primary', 'Headings', HEAD, 700), typo('secondary', 'Subheadings', HEAD, 600),
                       typo('text', 'Body', BODY, 400, 17, 1.7, None, None, 16, 16), typo('accent', 'Buttons', HEAD, 600, 16, 1.2)],
 'custom_typography': [
   typo('gsh1', 'H1 – Hero', HEAD, 700, 64, 1.08, -1.5, None, 48, 38),
   typo('gsh2', 'H2 – Section Title', HEAD, 700, 46, 1.15, -1, None, 38, 30),
   typo('gsh3', 'H3 – Card / Sub Title', HEAD, 600, 24, 1.3, -0.3, None, 22, 20),
   typo('gsh4', 'H4 – Small Title', HEAD, 600, 19, 1.4, None, None, 18, 18),
   typo('gseyebrow', 'Eyebrow / Kicker', BODY, 600, 13, 1.5, 2, 'uppercase'),
   typo('gslead', 'Lead Paragraph', BODY, 400, 19, 1.65, None, None, 18, 17),
   typo('gsbody', 'Body', BODY, 400, 17, 1.7, None, None, 16, 16),
   typo('gssmall', 'Small / Meta', BODY, 400, 14, 1.6),
   typo('gsbtn', 'Button', HEAD, 600, 16, 1.2),
   typo('gsnav', 'Navigation', BODY, 500, 15, 1.4),
   typo('gsstat', 'Stat Number', HEAD, 700, 52, 1, -1, None, 44, 38),
 ],
 'default_generic_fonts': 'Sans-serif',
 # Typography tab
 'body_color': TEXT, 'body_typography_typography': 'custom', 'body_typography_font_family': BODY,
 'body_typography_font_size': px(17), 'body_typography_font_size_mobile': px(16), 'body_typography_font_weight': '400',
 'body_typography_line_height': px(1.7, 'em'), 'paragraph_spacing': px(16),
 'link_normal_color': SKY, 'link_hover_color': WHITE,
 # Buttons tab (primary = violet pill)
 'button_typography_typography': 'custom', 'button_typography_font_family': HEAD, 'button_typography_font_weight': '600',
 'button_typography_font_size': px(16), 'button_typography_line_height': px(1.2, 'em'),
 'button_text_color': WHITE, 'button_background_background': 'classic', 'button_background_color': VIOLET,
 'button_hover_text_color': WHITE, 'button_hover_background_background': 'classic', 'button_hover_background_color': VIOLET_DK,
 'button_border_radius': dims(999), 'button_padding': dims(16, 30),
 'button_box_shadow_box_shadow_type': 'yes',
 'button_box_shadow_box_shadow': {'horizontal': 0, 'vertical': 12, 'blur': 30, 'spread': 0, 'color': 'rgba(112,82,255,0.35)'},
 # Form Fields tab (dark glass inputs)
 'form_label_typography_typography': 'custom', 'form_label_typography_font_family': BODY, 'form_label_typography_font_weight': '500',
 'form_label_typography_font_size': px(14), 'form_label_color': '#DCE4F5',
 'form_field_typography_typography': 'custom', 'form_field_typography_font_family': BODY, 'form_field_typography_font_size': px(16),
 'form_field_text_color': WHITE, 'form_field_background_color': 'rgba(255,255,255,0.06)',
 'form_field_border_border': 'solid', 'form_field_border_width': dims(1), 'form_field_border_color': 'rgba(255,255,255,0.18)',
 'form_field_border_radius': dims(12), 'form_field_padding': dims(14, 16),
 'form_field_focus_text_color': WHITE, 'form_field_focus_background_color': 'rgba(255,255,255,0.10)',
 'form_field_focus_border_border': 'solid', 'form_field_focus_border_width': dims(1), 'form_field_focus_border_color': SKY,
 # Background
 'body_background_background': 'classic', 'body_background_color': NAVY,
 # Layout tab
 'container_width': px(1240), 'container_padding': dims(0, 24), 'container_padding_mobile': dims(0, 16),
 'space_between_widgets': {'column': '20', 'row': '20', 'isLinked': True, 'unit': 'px', 'size': 20},
 'page_title_selector': 'h1.entry-title', 'default_page_template': 'elementor_header_footer',
 'viewport_tablet': 1024, 'viewport_mobile': 767, 'viewport_md': 768, 'viewport_lg': 1025,
 # Site identity
 'site_name': 'Graphics Storm Studio', 'site_description': 'Digital Marketing Agency',
 'site_logo': {'id': 5904, 'url': 'https://graphicsstormstudio.com/wp-content/uploads/2026/11/graphics-storm-studio-logo.webp'},
 # Lightbox off (we have no galleries needing it)
 'global_image_lightbox': '',
}
H_SIZES = {1: ('gsh1', 700), 2: ('gsh2', 700), 3: ('gsh3', 600), 4: ('gsh4', 600), 5: (None, 600), 6: (None, 600)}
for n, (_, w) in H_SIZES.items():
    S[f'h{n}_color'] = WHITE
    S[f'h{n}_typography_typography'] = 'custom'; S[f'h{n}_typography_font_family'] = HEAD; S[f'h{n}_typography_font_weight'] = str(w)
for n, (sz, t, m, lh) in {1: (64, 48, 38, 1.08), 2: (46, 38, 30, 1.15), 3: (24, 22, 20, 1.3), 4: (19, 18, 18, 1.4), 5: (17, 17, 16, 1.4), 6: (15, 15, 15, 1.4)}.items():
    S[f'h{n}_typography_font_size'] = px(sz); S[f'h{n}_typography_font_size_tablet'] = px(t); S[f'h{n}_typography_font_size_mobile'] = px(m)
    S[f'h{n}_typography_line_height'] = px(lh, 'em')

S['custom_css'] = open(os.path.join(HERE, '..', 'templates', 'gs-global.css')).read()

if __name__ == '__main__':
    json.dump(S, open(os.path.join(HERE, '..', 'templates', 'site-settings.json'), 'w'), indent=1)
    if '--dry' in sys.argv: raise SystemExit('dry run: wrote templates/site-settings.json')
    cur = wp.req(f'wp/v2/elementor_library/{KIT_ID}?context=edit')['meta']['_elementor_page_settings'] or {}
    legacy = [dict(c, title='Legacy – ' + c['title'].replace('Legacy – ', '')) for c in cur.get('custom_colors', []) if not c['_id'].startswith('gs')]
    new = dict(cur); new.update(S)
    new['custom_colors'] = S['custom_colors'] + legacy   # keep old colours (renamed) until old pages are deleted
    new.pop('activeItemIndex', None)
    # Save through Elementor's document API (merges + regenerates the kit CSS file)
    r = wp.ability('elementor/update-page-settings', {'post_id': KIT_ID, 'settings': new})
    print('kit saved:', str(r)[:300])
