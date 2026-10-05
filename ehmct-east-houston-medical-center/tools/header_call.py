"""Header 33: phone number on the desktop Call button + a mobile-only Call Now button inside the logo pill (live patch)."""
from patch import fetch, save, find, titled
from el import W, px, dims, icon, col, shadow
import mobile_hero as mh

doc = fetch(33, 'elementor_library')
d = doc['data']
call = find(d, titled('Header – Call Now'))
call['settings']['text'] = 'Call (832) 400-2396'

pill = find(d, titled('Header – Logo & Nav Pill'))
pill['settings']['flex_gap_mobile'] = {'column': '8', 'row': '8', 'isLinked': True, 'unit': 'px', 'size': 8}
if not any(e['settings'].get('_title') == 'Header – Call Now (Mobile)' for e in pill['elements']):
    btn = W('button', 'Header – Call Now (Mobile)', text='Call Now',
            link={'url': 'tel:+18324002396', 'is_external': '', 'nofollow': '', 'custom_attributes': ''},
            selected_icon=icon('fas fa-phone-alt'), icon_indent=px(6), border_radius=dims(999), text_padding=dims(9, 14),
            typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
            typography_font_size=px(13), typography_line_height=px(16),
            button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(6, 14, 'rgba(158,63,66,0.30)'),
            hide_desktop='hidden-desktop', hide_tablet='hidden-tablet', _flex_size='none',
            custom_css='selector{margin-left:auto}selector .elementor-button{white-space:nowrap}'
                       '@media(max-width:389px){selector .elementor-button-text{display:none}'
                       'selector .elementor-button{padding:10px !important;width:34px;height:34px;justify-content:center}'
                       'selector .elementor-button-icon{margin:0 !important}}',
            g={'background_color': col('secondary'), 'button_text_color': col('ehwhite'),
               'button_background_hover_color': col('ehreddk'), 'hover_color': col('ehwhite')})
    logo_i = next(i for i, e in enumerate(pill['elements']) if e['settings'].get('_title') == 'Header – Logo')
    pill['elements'].insert(logo_i + 1, btn)
save(doc)
