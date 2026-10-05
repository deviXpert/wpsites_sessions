"""First build of /request-an-appointment/ (content + form fields from ehmct.com, Elementor Pro form, EHMC theme).
Refuses to overwrite once built (`--rebuild-draft` only while still a draft). Later changes: patch.py.
"""
import json, os, sys
from el import C, W, T, H, EYEBROW, px, dims, gap, col, icon, put, regen, shadow
from figma_pages import banner, IDS_FILE
from patch import _api

INTRO = ('To request an appointment using our website, please complete the form below. After you submit this information, '
         'a representative will contact you by phone within two business days. <strong>If you have an emergency dial 911.</strong>')
STATES = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
          'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
          'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
          'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
          'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
          'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
CHECKIN = 'https://portal.gorev.com/preregister.aspx?s=h%2f4vymVZJdRgfYtF7XRQTw%3d%3d&f=TY11yCMzYfJUUuhIahY6Qg%3d%3d&l=wQE4BShlAnIMHtZ%2bZ98z2Q%3d%3d'


def f(_id, label, typ='text', width='100', req=False, ph='', **kw):
    d = {'_id': _id, 'custom_id': _id, 'field_type': typ, 'field_label': label, 'placeholder': ph, 'width': width,
         'width_mobile': '100' if width in ('50', '33', '25') and _id not in ('state', 'zip') else width}
    if req: d['required'] = 'true'
    d.update(kw)
    return d


def section_label(_id, text):
    return {'_id': _id, 'custom_id': _id, 'field_type': 'html', 'width': '100',
            'field_html': '<h3 class="ehmc-form-sec">' + text + '</h3>'}


FIELDS = [
    section_label('sec_patient', 'Patient Information'),
    f('first_name', 'First Name', req=True, width='50', ph='First Name'),
    f('last_name', 'Last Name', req=True, width='50', ph='Last Name'),
    f('address1', 'Address Line 1', ph='Address Line 1'),
    f('address2', 'Address Line 2', ph='Address Line 2'),
    f('city', 'City', width='50', ph='City'),
    f('state', 'State', 'select', width='25', field_options='State|\n' + '\n'.join(STATES), width_mobile='50'),
    f('zip', 'Zip Code', width='25', ph='ZIP', width_mobile='50'),
    f('phone', 'Phone No', 'tel', req=True, width='50', ph='Your Phone Number'),
    f('email', 'Email', 'email', req=True, width='50', ph='Your Email'),
    f('dob', 'Date of Birth', 'date', req=True, width='50', ph='mm/dd/yyyy', use_native_date='yes'),
    f('contact_time', 'Preferred Contact Time (EST)', 'select', width='50',
      field_options='Choose Contact Time|\nMorning (8am-12pm)\nAfternoon (12pm-5pm)\nEvening (5pm-8pm)'),
    section_label('sec_appt', 'Appointment Information'),
    f('existing_patient', 'Existing Patient', 'radio', width='50', field_options='Yes\nNo', inline_list='elementor-subgroup-inline'),
    f('physician_gender', 'Preferred Physician Gender', 'radio', width='50', field_options='Male\nFemale',
      inline_list='elementor-subgroup-inline'),
    f('reason', 'Reason for Visit or Diagnosis', 'textarea', rows=5, ph='Briefly describe the reason for your visit'),
]

FORM_CSS = ('selector .ehmc-form-sec{margin:10px 0 0;padding-bottom:12px;border-bottom:1px solid #DFE5ED;color:#293A6E;'
            'font:700 20px/1.3 Poppins,sans-serif;letter-spacing:-.4px}'
            'selector .elementor-field-group-sec_appt .ehmc-form-sec{margin-top:18px}'
            'selector .elementor-field-subgroup .elementor-field-option label{color:#5F6D82;font:500 15px/1.4 Poppins,sans-serif}'
            'selector .elementor-field-subgroup.elementor-subgroup-inline .elementor-field-option{margin-right:22px}'
            'selector .elementor-field-type-radio input{accent-color:#9F3135;width:17px;height:17px;vertical-align:-3px;margin-right:6px}'
            'selector select.elementor-field{color:#0C1D3C}'
            'selector .elementor-field-required .elementor-field-label:after{color:#9F3135}'
            'selector .elementor-button[type=submit]{min-width:240px}'
            '@media(max-width:767px){selector .elementor-button[type=submit]{width:100%}}')


def form():
    return W('form', 'Appointment – Form', form_name='Request an Appointment', form_fields=FIELDS, show_labels='yes',
             mark_required='yes', input_size='md', button_text='Request Appointment', button_size='md', button_width='',
             selected_button_icon=icon('fas fa-arrow-right'), button_icon_align='row-reverse', button_icon_indent=px(10),
             submit_actions=['email', 'collect_submissions'],
             email_to='dev@themaddex.com', email_subject='New appointment request from EHMC website',
             email_content='[all-fields]', email_from='email@hotpink-lobster-615998.hostingersite.com',
             email_from_name='East Houston Medical Center website', email_reply_to='email',
             success_message='Thank you! A representative will contact you by phone within two business days.',
             error_message='Your submission failed because of an error.', required_field_message='This field is required.',
             invalid_message='Your submission failed because the form is invalid.',
             server_message='Your submission failed because of a server error.',
             column_gap=px(16), row_gap=px(18), label_spacing=px(8),
             field_border_radius=dims(10), field_border_width=dims(1),
             button_border_radius=dims(10), button_text_padding=dims(16, 28),
             button_box_shadow_box_shadow_type='yes', button_box_shadow_box_shadow=shadow(12, 28, 'rgba(158,63,66,0.26)'),
             label_typography_typography='custom', label_typography_font_family='Poppins', label_typography_font_weight='600',
             label_typography_font_size=px(13.5), field_typography_typography='custom', field_typography_font_family='Poppins',
             field_typography_font_size=px(15), custom_css=FORM_CSS,
             g={'label_color': col('primary'), 'field_text_color': col('accent'), 'field_background_color': col('ehsurf'),
                'field_border_color': col('ehborder'), 'button_background_color': col('secondary'),
                'button_background_hover_color': col('ehreddk'), 'button_text_color': col('ehwhite'),
                'button_typography_typography': typ_btn()})


def typ_btn():
    return 'globals/typography?id=ehbtn'


def info_row(ic, title, text, url=None):
    s = dict(selected_icon=icon(ic), view='stacked', position='inline-start', position_mobile='inline-start',
             text_align_mobile='left', title_text=title, description_text=text, title_size='p', icon_size=px(16),
             icon_padding=px(12), icon_space=px(14), content_vertical_alignment='top', title_bottom_space=px(4),
             title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_weight='700',
             title_typography_font_size=px(15), description_typography_typography='custom',
             description_typography_font_family='Poppins', description_typography_font_size=px(13.5),
             description_typography_line_height=px(1.55, 'em'),
             primary_color='rgba(255,255,255,0.12)', secondary_color='#FFFFFF', title_color='#FFFFFF',
             description_color='rgba(230,234,241,0.85)')
    if url: s['link'] = {'url': url, 'is_external': 'on' if url.startswith('http') else '', 'nofollow': ''}
    return W('icon-box', 'Appointment Info – ' + title, **s)


def side():
    call = W('button', 'Appointment – Call', text='Call (832) 400-2396',
             link={'url': 'tel:+18324002396', 'is_external': '', 'nofollow': ''}, selected_icon=icon('fas fa-phone-alt'),
             icon_indent=px(10), border_radius=dims(10), text_padding=dims(15, 22), align='justify',
             g={'background_color': col('secondary'), 'button_text_color': col('ehwhite'),
                'button_background_hover_color': col('ehreddk'), 'typography_typography': typ_btn()},
             custom_css='selector .elementor-button{white-space:nowrap}')
    checkin = W('button', 'Appointment – Check-In', text='Check-In Now',
                link={'url': CHECKIN, 'is_external': 'on', 'nofollow': ''}, selected_icon=icon('fas fa-arrow-right'),
                icon_align='row-reverse', icon_indent=px(10), border_radius=dims(10), text_padding=dims(15, 22), align='justify',
                background_color='rgba(255,255,255,0.06)', border_border='solid', border_width=dims(1.5),
                border_color='rgba(255,255,255,0.8)', button_background_hover_color='#FFFFFF', hover_color='#293A6E',
                button_text_color='#FFFFFF', g={'typography_typography': typ_btn()})
    return C('Appointment – Side Card', [
        EYEBROW('Need Care Now?', align='left', color='ehwhite'),
        W('heading', 'Appointment – Side Title', title='Walk-ins Welcome 24/7', header_size='h3', title_color='#FFFFFF',
          typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
          typography_font_size=px(26), typography_line_height=px(1.2, 'em'), typography_letter_spacing=px(-0.6)),
        W('text-editor', 'Appointment – Side Text', editor='<p>No appointment is needed for emergency care. '
          'If you have a medical emergency, dial 911 or come straight to our ER.</p>', text_color='rgba(230,234,241,0.85)',
          typography_typography='custom', typography_font_family='Poppins', typography_font_size=px(14.5),
          typography_line_height=px(1.6, 'em'), custom_css='selector p{margin:0}'),
        info_row('far fa-clock', 'Open 24/7', '365 days a year'),
        info_row('fas fa-map-marker-alt', '15149 Wallisville Rd', 'Houston, TX 77049',
                 'https://www.google.com/maps/dir/?api=1&destination=15149+Wallisville+Rd+Houston+TX+77049'),
        info_row('fas fa-phone-alt', 'Response time', 'We call you back within two business days.'),
        call, checkin],
        flex_direction='column', flex_gap=gap(18), padding=dims(36, 32), padding_mobile=dims(28, 22),
        border_radius=dims(24), border_radius_mobile=dims(20), background_background='gradient',
        background_color='#293A6E', background_color_b='#3E5596', background_gradient_angle=px(160, 'deg'),
        width=px(34, '%'), width_tablet=px(100, '%'), _flex_align_self='flex-start',
        custom_css='@media(min-width:1025px){selector{position:sticky;top:30px}}')


def page():
    intro = W('text-editor', 'Appointment – Intro', editor='<p>' + INTRO + '</p>', align='center', text_color='#5F6D82',
              typography_typography='custom', typography_font_family='Poppins', typography_font_size=px(16),
              typography_line_height=px(1.7, 'em'), _element_width='initial', _element_custom_width=px(760),
              _element_custom_width_tablet=px(100, '%'), custom_css='selector p{margin:0}selector strong{color:#9F3135}')
    head = C('Appointment – Head', [
        EYEBROW('Appointments'),
        H('You Would Like To Make <span>An Appointment</span>', 'h2', align='center', name='Section Title'),
        intro], flex_direction='column', flex_align_items='center', flex_gap=gap(14), padding=dims(0))
    form_card = C('Appointment – Form Card', [form()], padding=dims(40, 40), padding_tablet=dims(32, 28),
                  padding_mobile=dims(24, 18), background_background='classic', background_color='#FFFFFF',
                  border_border='solid', border_width=dims(1), border_color='#DFE5ED', border_radius=dims(24),
                  border_radius_mobile=dims(20), box_shadow_box_shadow_type='yes',
                  box_shadow_box_shadow=shadow(18, 50, 'rgba(16,37,74,0.10)'), width=px(66, '%'), width_tablet=px(100, '%'))
    row = C('Appointment – Row', [form_card, side()], flex_direction='row', flex_direction_tablet='column',
            flex_gap=gap(28), flex_wrap='nowrap', padding=dims(0), width=px(1240), width_tablet=px(100, '%'),
            custom_css='selector{max-width:100%}')
    sec = C('Request an Appointment', [head, row], inner=False, flex_direction='column', flex_align_items='center',
            flex_gap=gap(48), flex_gap_mobile=gap(32), padding=dims(90, 20, 100, 20), padding_tablet=dims(70, 24, 80, 24),
            padding_mobile=dims(56, 16, 64, 16))
    return [banner('Request <span>An Appointment</span>', 'banner_conditions', 'Appointment Banner'), sec]


if __name__ == '__main__':
    slug, title = 'request-an-appointment', 'Request An Appointment'
    ids = json.load(open(IDS_FILE))
    if '--qa' in sys.argv:
        pid = 41
    elif slug in ids:
        pid = ids[slug]
        cur = _api('GET', f'wp/v2/pages/{pid}?context=edit&_fields=status,meta')
        live = cur['meta'].get('_elementor_data')
        if live and live != '[]' and not ('--rebuild-draft' in sys.argv and cur['status'] == 'draft'):
            raise SystemExit(f'{slug} ({pid}) already built – patch it with patch.py instead of regenerating')
    else:
        layout = {'ast-site-content-layout': 'full-width-container', 'site-content-style': 'default', 'site-sidebar-layout': 'no-sidebar'}
        r = _api('POST', 'wp/v2/pages', {'title': title, 'slug': slug, 'status': 'draft', 'template': 'elementor_header_footer',
                                          'excerpt': 'Request an appointment at East Houston Medical Center. A representative will call you within two business days.',
                                          'meta': layout})
        pid = ids[slug] = r['id']
        json.dump(ids, open(IDS_FILE, 'w'), indent=1)
    put(pid, page(), post_extra={'template': 'elementor_header_footer'})
    regen(pid)
    print(slug, pid)
