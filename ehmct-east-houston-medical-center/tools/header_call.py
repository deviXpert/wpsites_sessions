"""Header 33 (live patch):
- desktop Call button shows the number
- mobile-only actions row under the logo pill, per Figma Mobile view: "View Our ER" (glass pill + arrow circle)
  and "Call Now" (red pill, 5px white border). Replaces the earlier in-pill mobile Call Now button.
"""
from patch import fetch, save, find, titled
from el import W, C, px, dims, icon, gap

ARROW = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' "
         "stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12h14M13 6l6 6-6 6'/%3E%3C/svg%3E")
PHONE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' "
         "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 "
         "19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6"
         "l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z'/%3E%3C/svg%3E")


def actions_row():
    view = W('button', 'Header – View Our ER (Mobile)', text='View Our ER',
             link={'url': '/#locations', 'is_external': '', 'nofollow': '', 'custom_attributes': ''},
             border_radius=dims(999), text_padding=dims(0), button_text_color='#FFFFFF', background_color='rgba(12,37,67,0.14)',
             typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
             typography_font_size=px(10.63), typography_line_height=px(17),
             custom_css='selector .elementor-button{display:inline-flex;align-items:center;gap:8.2px;height:39.9px;padding:0 4.45px 0 15.5px;'
                        'border:.74px solid rgba(255,255,255,.75);-webkit-backdrop-filter:blur(7.4px);backdrop-filter:blur(7.4px);white-space:nowrap}'
                        'selector .elementor-button-content-wrapper{align-items:center;gap:8.2px}'
                        'selector .elementor-button-content-wrapper::after{content:"";width:31px;height:31px;box-sizing:border-box;border-radius:50%;'
                        'border:.74px solid rgba(255,255,255,.72);background:url("' + ARROW + '") center/14.8px no-repeat}')
    call = W('button', 'Header – Call Now (Mobile)', text='Call Now',
             link={'url': 'tel:+18324002396', 'is_external': '', 'nofollow': '', 'custom_attributes': ''},
             border_radius=dims(999), text_padding=dims(0), button_text_color='#FFFFFF', background_color='#BE2424',
             button_background_hover_color='#9F3135', hover_color='#FFFFFF',
             typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
             typography_font_size=px(13.22), typography_line_height=px(21.17),
             custom_css='selector .elementor-button{display:inline-flex;align-items:center;height:48px;box-sizing:border-box;'
                        'padding:7.86px 19.94px 8.38px;border:5.17px solid #FFFFFF;box-shadow:0 8.86px 23.63px rgba(75,5,22,.25);white-space:nowrap}'
                        'selector .elementor-button-content-wrapper{align-items:center;gap:8.86px}'
                        'selector .elementor-button-content-wrapper::before{content:"";width:18.5px;height:18.5px;background:url("' + PHONE + '") center/contain no-repeat}')
    return C('Header – Mobile Actions', [view, call], flex_direction='row', flex_justify_content='center',
             flex_align_items='center', flex_gap=gap(13.9), flex_wrap='nowrap', width=px(100, '%'), padding=dims(0),
             hide_desktop='hidden-desktop', hide_tablet='hidden-tablet')


doc = fetch(33, 'elementor_library')
d = doc['data']
find(d, titled('Header – Call Now'))['settings']['text'] = 'Call (832) 400-2396'

pill = find(d, titled('Header – Logo & Nav Pill'))
pill['elements'] = [e for e in pill['elements'] if e['settings'].get('_title') != 'Header – Call Now (Mobile)']

top = find(d, titled('Header'))
top['elements'] = [e for e in top['elements'] if e['settings'].get('_title') != 'Header – Mobile Actions']
pill_i = top['elements'].index(pill)
top['elements'].insert(pill_i + 1, actions_row())
# Figma: pill ends at y=83, buttons row starts at y=90 -> 7px row gap on mobile
top['settings']['flex_gap_mobile'] = {'column': '16', 'row': '7', 'isLinked': False, 'unit': 'px', 'size': 16}
save(doc)
