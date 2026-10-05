from el import *

PHONE = '(832) 400-2396'; TEL = 'tel:+18324002396'
EMAIL = 'info@ehmct.com'
ADDR1, ADDR2 = '15149 Wallisville Rd', 'Houston, TX 77049'
MAPS = 'https://www.google.com/maps/dir/?api=1&destination=15149+Wallisville+Rd+Houston+TX+77049'

# ---------------- HEADER ----------------
logo = W('image', 'Header – Logo', image=img('ehmc-logo'), image_size='full',
         width=px(190), width_mobile=px(150),
         link_to='custom', link={'url': '/', 'is_external': '', 'nofollow': ''})
nav = W('nav-menu', 'Header – Menu', menu='ehmc-primary', layout='horizontal', align_items='right',
        pointer='none', dropdown='mobile', toggle='burger', full_width='stretch',
        menu_typography_typography='custom', menu_typography_font_family='Poppins', menu_typography_font_weight='700',
        menu_typography_font_size=px(14.4), padding_horizontal_menu_item=px(18),
        g={'color_menu_item': col('accent'), 'color_menu_item_hover': col('secondary'),
           'color_dropdown_item': col('primary'), 'color_dropdown_item_hover': col('secondary'),
           'toggle_color': col('primary')},
        background_color_dropdown_item='#FFFFFF', background_color_dropdown_item_hover='#F6F8FB',
        dropdown_border_radius=dims(12), dropdown_top_distance=px(18),
        _flex_size='grow', _flex_size_mobile='none')
pill = C('Header – Logo & Nav Pill', [logo, nav], flex_direction='row', flex_align_items='center',
         flex_justify_content='space-between', flex_gap=gap(20),
         width=px(63, '%'), width_tablet=px(75, '%'), width_mobile=px(100, '%'),
         padding=dims(10, 26, 10, 18), padding_mobile=dims(8, 14, 8, 14),
         background_background='classic', background_color='#FFFFFF',
         border_radius=dims(18), box_shadow_box_shadow_type='yes', box_shadow_box_shadow=shadow(6, 16, 'rgba(7,26,49,0.16)'))
checkin = BTN('Check-In Now', '#contact', 'Header – Check-In', style='outline-light',
              icon_=icon('fas fa-arrow-right'), border_radius=dims(999), text_padding=dims(8, 8, 8, 22), icon_indent=px(12),
              background_color='rgba(255,255,255,0.12)', typography_font_size=px(14.4),
              custom_css='selector .elementor-button-icon{width:30px;height:30px;border:1px solid rgba(255,255,255,.8);border-radius:50%;display:inline-flex;align-items:center;justify-content:center} selector .elementor-button-icon svg{width:12px} selector .elementor-button-content-wrapper{align-items:center}',
              hide_tablet='hidden-tablet', hide_mobile='hidden-mobile')
call = BTN('Call Now', TEL, 'Header – Call Now', icon_=icon('fas fa-phone-alt'),
           border_radius=dims(999), text_padding=dims(16, 30), text_padding_mobile=dims(12, 18),
           border_border='solid', border_width=dims(3), border_color='#FFFFFF', hide_mobile='hidden-mobile')
call['settings']['icon_align'] = 'row'
header = C('Header', [pill, checkin, call], inner=False,
           content_width='full',
           flex_direction='row', flex_align_items='center', flex_justify_content='space-between', flex_gap=gap(16),
           flex_wrap_mobile='wrap',
           padding=dims(26, 36, 0, 36), padding_tablet=dims(22, 24, 0, 24), padding_mobile=dims(14, 14, 0, 14),
           position='absolute', _position='absolute', z_index=50,
           width=px(100, '%'), css_classes='ehmc-header',
           custom_css='@media(min-width:1025px){selector{padding-left:max(36px,calc((100% - 1440px)/2)) !important;padding-right:max(36px,calc((100% - 1440px)/2)) !important}}')

# ---------------- FOOTER ----------------
def fcol(title, items, name):
    return C('Footer – ' + name, [
        H(title, 'h4', 'ehh3', 'primary', name='Footer – %s Title' % name,
          typography_font_size=px(15.7)),
        W('icon-list', 'Footer – %s Links' % name,
          icon_list=[dict(_id=uid(), text=t, **({'link': {'url': u, 'is_external': '', 'nofollow': ''}} if u else {}),
                          selected_icon={'value': '', 'library': ''}) for t, u in items],
          space_between=px(6), icon_size=px(0), text_indent=px(0),
          g={'text_color': col('text'), 'text_color_hover': col('secondary'), 'icon_typography_typography': typ('ehsmall')}),
    ], flex_gap=gap(14), width=px(20, '%'), width_tablet=px(46, '%'), width_mobile=px(100, '%'))

brand = C('Footer – Brand', [
    W('image', 'Footer – Logo', image=img('ehmc-logo'), image_size='full', width=px(210), align='left'),
    T('<p>Expert emergency care and compassionate treatment, available when Houston needs it most.</p>',
      'ehsmall', name='Footer – Blurb'),
], flex_gap=gap(18), width=px(32, '%'), width_tablet=px(100, '%'))

footer_row = C('Footer – Columns', [
    brand,
    fcol('Contact', [(ADDR1 + ', ' + ADDR2, MAPS), (PHONE, TEL), (EMAIL, 'mailto:' + EMAIL), ('Open 24/7', '')], 'Contact'),
    fcol('Quick Links', [('Conditions', '/#conditions'), ('Physicians', '/#team'), ('Departments', '/#departments'), ('Reviews', '/#reviews')], 'Quick Links'),
    fcol('Emergency Care', [('Diagnostic Imaging', '/#departments'), ('Trauma Care', '/#departments'), ('Cardiac Care', '/#departments'), ('Pediatric Emergency', '/#departments')], 'Emergency Care'),
], content_width='boxed', flex_direction='row', flex_wrap='wrap',
   flex_justify_content='space-between', flex_gap=gap(30, 36), padding=dims(52, 20, 44, 20))

warning = T('<p>A medical emergency can be life-threatening. If you are experiencing a serious emergency, call 911 immediately.</p>',
            'eheye', 'ehwhite', 'center', name='Footer – 911 Warning Bar',
            typography_letter_spacing=px(0.3), typography_font_size=px(11.7),
            _background_background='classic', _background_color='#9F3135', _padding=dims(16, 20), _padding_mobile=dims(14, 16),
            g={'typography_typography': typ('eheye'), 'text_color': col('ehwhite'), '_background_color': col('secondary')})
footer = C('Footer', [footer_row, warning], inner=False, flex_gap=gap(0), padding=dims(0),
           border_border='solid', border_width=dims(4, 0, 0, 0), border_color='#293A6E',
           background_background='classic', background_color='#FFFFFF')

if __name__ == '__main__':
    for pid, el in ((33, header), (34, footer)):
        print(count([el]))
        put(pid, [el], post_extra={'_type': 'lib'})
