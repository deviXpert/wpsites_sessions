"""First build of the Figma pages "Condition we treat" (436:46) and "departments" (436:1016).

Same rules as inner_pages.py: refuses to overwrite a built page (`--rebuild-draft` only while still a draft),
`--qa` writes to QA draft 41. Later changes go through patch.py.
  python3 figma_pages.py conditions|departments [--qa|--rebuild-draft]
Mobile has no Figma frame: one column, banner content starts below the header's mobile action row (y=138).
"""
import json, os, sys
from el import C, W, T, EYEBROW, H, px, dims, gap, img, col, put, regen
from patch import _api

IDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inner_ids.json')

# Figma 436:986 (left->right) + 436:987 (bottom->top, lower half)
OVERLAY = ('linear-gradient(0deg,rgba(2,13,29,.62) 0%,rgba(2,13,29,0) 47%),'
           'linear-gradient(90deg,rgba(2,16,34,.9) 0%,rgba(3,19,39,.74) 32%,rgba(3,19,39,.22) 62%,rgba(3,19,39,.04) 100%)')


def banner(title_html, img_key, name):
    title = W('heading', 'Banner – Title', title=title_html, header_size='h1', align='left', align_mobile='left',
              typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
              typography_font_size=px(74), typography_font_size_tablet=px(56), typography_font_size_mobile=px(40),
              typography_line_height=px(0.912, 'em'), typography_line_height_mobile=px(1, 'em'),
              typography_letter_spacing=px(-4.08), typography_letter_spacing_tablet=px(-3), typography_letter_spacing_mobile=px(-1.5),
              typography_text_transform='uppercase', title_color='#FFFFFF',
              custom_css='selector .elementor-heading-title span{color:var(--e-global-color-secondary);}')
    content = C(name + ' – Content', [title], flex_direction='column', flex_align_items='flex-start',
                padding=dims(0, 113, 0, 113), padding_tablet=dims(0, 40, 0, 40), padding_mobile=dims(150, 20, 40, 20))
    card = C(name + ' – Image', [content], flex_direction='column', flex_justify_content='center',
             flex_justify_content_mobile='flex-start', min_height=px(729.9), min_height_tablet=px(520), min_height_mobile=px(380),
             padding=dims(0), background_background='classic', background_image=img(img_key),
             background_position='center center', background_size='cover', background_repeat='no-repeat',
             border_radius=dims(48), border_radius_mobile=dims(24), overflow='hidden',
             custom_css='selector::before{content:"";position:absolute;inset:0;background-image:' + OVERLAY + ';border-radius:inherit;z-index:0;pointer-events:none}'
                        'selector > .e-con{position:relative;z-index:1}')
    return C(name, [card], inner=False, padding=dims(10, 8, 0, 8), padding_mobile=dims(8, 8, 0, 8))


def heading_block(eyebrow, title_html, intro, intro_w):
    return [EYEBROW(eyebrow),
            H(title_html, 'h2', align='center', name='Section Title', _margin=dims(1, 0, 0, 0)),
            T('<p>' + intro + '</p>', align='center', name='Section Intro', color=None,
              text_color='#5F6D82', _margin=dims(20, 0, 0, 0),
              _element_width='initial', _element_custom_width=px(intro_w), _element_custom_width_tablet=px(100, '%'))]


def section(title, kids, top, bottom):
    return C(title, kids, inner=False, flex_direction='column', flex_align_items='center', flex_gap=gap(0),
             padding=dims(top, 20, bottom, 20), padding_tablet=dims(70, 24, 70, 24), padding_mobile=dims(56, 20, 56, 20))


def grid(title, cards, cols, col_gap, row_gap, width):
    css = ('selector{display:grid !important;grid-template-columns:repeat(%d,minmax(0,1fr));column-gap:%spx;row-gap:%spx}'
           '@media(max-width:1024px){selector{grid-template-columns:repeat(2,minmax(0,1fr))}}'
           '@media(max-width:767px){selector{grid-template-columns:1fr;row-gap:16px}}') % (cols, col_gap, row_gap)
    return C(title, cards, width=px(width), width_tablet=px(100, '%'), padding=dims(0),
             custom_css=css, margin=dims(48, 0, 0, 0))


# ---------------------------------------------------------------- Conditions (Figma 436:46)
CONDITIONS = [
    ('Chest Pain & Heart Concerns', 'Prompt evaluation for chest pain and possible heart emergencies.', '/chest-pain/'),
    ('Abdominal Pain', 'Evaluation for sudden, severe, or persistent abdominal pain', '/abdominal-pain/'),
    ('Breathing Difficulties', 'Urgent care for shortness of breath and breathing problems.', '/difficulty-breathing/'),
    ('Broken Bones & Fractures', 'On-site imaging and treatment for fractures an orthopedic injuries.', '/broken-bones/'),
    ('Allergic Reactions', 'Prompt treatment for severe or worsening allergic reactions.', '/allergic-reactions/'),
    ('High Fever', 'Evaluation and treatment for high or persistent fever.', '/high-fever/'),
    ('Severe Bleeding', 'Immediate care for uncontrolled bleeding and serious wounds.', '/severe-bleeding/'),
    ('Major Injuries & Trauma', 'Emergency evaluation and stabilization for serious injuries', '/trauma-injury/'),
]
COND_CARD_CSS = ('selector{transition:background-color .2s,border-color .2s,box-shadow .2s;text-decoration:none}'
                 'selector:hover,selector:focus-visible{background-color:#F7F9FD !important;border-color:#293A6E !important;'
                 'box-shadow:0 16px 38px rgba(17,39,77,.11)}'
                 'selector .elementor-heading-title{min-height:53.7px;display:flex;align-items:flex-start;justify-content:center}'
                 '@media(max-width:767px){selector .elementor-heading-title{min-height:0}}')


def cond_card(t, desc, url):
    title = W('heading', 'Condition – ' + t, title=t, header_size='h3', align='center', title_color='#293A6E',
              typography_typography='custom', typography_font_family='Poppins', typography_font_weight='600',
              typography_font_size=px(17.9), typography_line_height=px(26.85), typography_letter_spacing=px(-0.627))
    text = W('text-editor', 'Condition – Text', editor='<p>' + desc + '</p>', align='center', text_color='#5F6D82',
             typography_typography='custom', typography_font_family='Poppins', typography_font_weight='400',
             typography_font_size=px(14), typography_line_height=px(18.55),
             custom_css='selector p{margin:0}')
    return C('Condition Card – ' + t, [title, text], html_tag='a',
             link={'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': ''},
             flex_direction='column', flex_align_items='center', flex_gap=gap(24), flex_gap_mobile=gap(10),
             min_height=px(195), min_height_mobile=px(138), flex_justify_content_mobile='center',
             padding=dims(28.28, 28, 28.3, 28), padding_mobile=dims(26, 20, 26, 20),
             background_background='classic', background_color='#FFFFFF', border_border='solid', border_width=dims(1),
             border_color='#DFE5ED', border_radius=dims(16), custom_css=COND_CARD_CSS)


def conditions():
    s = section('Conditions We Treat', heading_block(
        'Immediate Treatment', 'Conditions <span>We Treat</span>',
        'From sudden illness to injuries, our team provides Houston immediate care 24/7 for a wide range of conditions.', 640)
        + [grid('Conditions – Grid', [cond_card(*c) for c in CONDITIONS], 4, 20, 20, 1192)], 90, 70)
    return [banner('Condition <span>We Treat</span>', 'banner_conditions', 'Conditions Banner'), s]


# ---------------------------------------------------------------- Departments (Figma 436:1016)
DEPARTMENTS = [
    ('Emergency Care', '24/7 emergency care for urgent medical conditions, injuries, and life-threatening symptoms.'),
    ('Diagnostic Imaging', 'Advanced diagnostic imaging, including X-rays, CT scans, and ultrasound for accurate diagnosis.'),
    ('Laboratory Services', 'On-site laboratory services and diagnostic testing to support fast, accurate medical decisions.'),
    ('Trauma Care', 'Expert trauma care for serious injuries, accidents, fractures, and other emergency conditions.'),
    ('Cardiac Care', 'Expert cardiac care for chest pain, heart conditions, and other cardiovascular emergencies.'),
    ('Pediatric Emergency', 'Specialized pediatric emergency care for children with injuries, illnesses, and urgent symptoms.'),
]


def dept_card(t, desc):
    title = W('heading', 'Department – ' + t, title=t, header_size='h3', title_color='#293A6E',
              typography_typography='custom', typography_font_family='Gelasio', typography_font_weight='700',
              typography_font_size=px(26), typography_font_size_mobile=px(23), typography_line_height=px(26.19))
    text = W('text-editor', 'Department – Text', editor='<p>' + desc + '</p>', text_color='#5F6D82',
             typography_typography='custom', typography_font_family='Poppins', typography_font_weight='400',
             typography_font_size=px(14), typography_line_height=px(20), custom_css='selector p{margin:0}')
    return C('Department Card – ' + t, [title, text], flex_direction='column', flex_justify_content='center',
             flex_gap=gap(16), min_height=px(200), padding=dims(28.05, 24.75, 28.05, 24.75),
             background_background='classic', background_color='#FFFFFF', border_radius=dims(16.5),
             box_shadow_box_shadow_type='yes',
             box_shadow_box_shadow={'horizontal': 0, 'vertical': 14.85, 'blur': 34.65, 'spread': 0, 'color': 'rgba(12,30,58,0.18)'})


def departments():
    s = section('Our Departments', heading_block(
        'Our Departments', 'Care Under <span>One Roof</span>',
        'Advanced technology and experienced professionals, ready to deliver comprehensive urgent care centers 24 hours a day.', 672)
        + [grid('Departments – Grid', [dept_card(*d) for d in DEPARTMENTS], 3, 23.5, 28, 1190)], 92, 73)
    return [banner('Our <span>Departments</span>', 'banner_departments', 'Departments Banner'), s]


PAGES = {
    'conditions': dict(title='Conditions We Treat', slug='conditions', build=conditions,
                       excerpt='Emergency care in Houston for chest pain, abdominal pain, breathing problems, fractures, allergic reactions, fever, bleeding and trauma.'),
    'departments': dict(title='Departments', slug='departments', build=departments,
                        excerpt='East Houston Medical Center departments: emergency care, diagnostic imaging, laboratory, trauma, cardiac and pediatric emergency care.'),
}

if __name__ == '__main__':
    pg = PAGES[sys.argv[1]]
    ids = json.load(open(IDS_FILE)) if os.path.exists(IDS_FILE) else {}
    if '--qa' in sys.argv:
        pid = 41
    elif pg['slug'] in ids:
        pid = ids[pg['slug']]
        cur = _api('GET', f'wp/v2/pages/{pid}?context=edit&_fields=status,meta')
        live = cur['meta'].get('_elementor_data')
        if live and live != '[]' and not ('--rebuild-draft' in sys.argv and cur['status'] == 'draft'):
            raise SystemExit(f'{pg["slug"]} ({pid}) already built – patch it with patch.py instead of regenerating')
    else:
        layout = {'ast-site-content-layout': 'full-width-container', 'site-content-style': 'default', 'site-sidebar-layout': 'no-sidebar'}
        r = _api('POST', 'wp/v2/pages', {'title': pg['title'], 'slug': pg['slug'], 'status': 'draft', 'excerpt': pg['excerpt'],
                                          'template': 'elementor_header_footer', 'meta': layout})
        pid = ids[pg['slug']] = r['id']
        json.dump(ids, open(IDS_FILE, 'w'), indent=1)
    put(pid, pg['build'](), post_extra={'template': 'elementor_header_footer'})
    regen(pid)
    print(pg['slug'], pid)
