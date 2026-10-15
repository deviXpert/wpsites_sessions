"""Busy Bee footer → Theme Builder footer template (post 74, condition: entire site)."""
import json
import el
from common import *
from el import uid
from sitemap import SERVICE_PAGES, PAGES

FOOTER_ID = 74
FOOT_SERVICES = [('Computer diagnostics &amp; electrical', 'diagnostics'), ('Engine maintenance &amp; repair', 'engine'),
                 ('Brake repair &amp; replacement', 'brakes'), ('Mobil 1 synthetic oil change', 'oil-change'),
                 ('Suspension &amp; steering repair', 'suspension'), ('Wheels, tires &amp; balancing', 'tires'),
                 ('Battery &amp; alternator service', 'battery'), ('Cooling system &amp; radiator', 'cooling'),
                 ('Transmission repair', 'transmission')]


def eyebrow(t):
    return H(t, 'p', BEE, M(10, 800, 15, 2, 'uppercase'), name='Eyebrow')


def build():
    el.seed('footer')
    cta = C('CTA row', [
        C('Copy', [eyebrow('Ready when you are'),
                   H('Need a Mechanic in Calgary Today?', 'h2', PAPER, M(60, 800, 1.05, tt='uppercase', size_m=30), mar=(16, 0, 0, 0),
                     w=768, w_tablet='full', name='Title')]),
        C('Buttons', [
            BTN('Book appointment', '/#book', M(14, 700, 20), color=INK, bg=BEE, ic='arrow-right', ic_size=16, pad=(18, 28), radius=PILL,
                border=(1, ink(0.2)), sh=SH_BEE, name='Book appointment', w_mobile=pct(100), align_mobile='justify'),
            BTN('Get directions', MAPS, M(14, 700, 20), color=PAPER, bg='rgba(0,0,0,0)', ic='navigation', ic_pos='before', ic_size=16,
                pad=(18, 28), radius=PILL, border=(1, wht(0.25)), sh=SH_SM, name='Get directions', w_mobile=pct(100),
                align_mobile='justify'),
        ], d='row', d_mobile='column', jc='flex-end', jc_tablet='flex-start', gap=12),
    ], grid='1.15fr 0.85fr', grid_tablet='1fr', rows='auto', rows_tablet='auto', ai='end', ai_tablet='start', gap=40, gap_tablet=24,
        pad=(0, 0, 56, 0), pad_mobile=(0, 0, 32, 0), border=(dims(0, 0, 1, 0), wht(0.15)))

    about = C('About', [
        IMG('busy-bee-auto-repair-logo', w=151, alt='Busy Bee Auto Repair', name='Logo', href='/', cls='bb-foot-logo', align='left'),
        T('<p>You\'ll find us at 324 41 Ave NE, close to Deerfoot Trail and easy to reach from across the city. We see drivers from NE '
          'Calgary, Downtown, Bridgeland, Renfrew, Mayland Heights, Marlborough, and Airdrie.</p>', wht(0.55), M(14, 400, 28),
          mar=(20, 0, 0, 0), w=320, name='Text'),
        C('Social', [ICON('facebook', 16, color=PAPER, href=FACEBOOK, name='Facebook', cls='bb-social', w='auto'),
                     ICON('instagram', 16, color=PAPER, href=INSTAGRAM, name='Instagram', cls='bb-social', w='auto'),
                     ICON('mail', 16, color=PAPER, href='mailto:' + EMAIL, name='Email', cls='bb-social', w='auto')],
          d='row', ai='center', gap=8, mar=(24, 0, 0, 0)),
    ])
    svc = C('Services', [
        eyebrow('Services'),
        ILIST([('arrow-right', l.replace('&', '&amp;'), u) for _, l, u, *_ in SERVICE_PAGES], t=M(14, 400, 20), color=wht(0.65),
              ic_color=BEE, ic_size=14, gap_=12, mar=(20, 0, 0, 0), name='Service links', cls='bb-foot-links'),
    ])
    company = C('Company', [
        eyebrow('Company'),
        ILIST([('arrow-right', t, u) for t, u in PAGES] + [('arrow-right', 'Book an appointment', '/#book')], t=M(14, 400, 20),
              color=wht(0.65), ic_color=BEE, ic_size=14, gap_=12, mar=(20, 0, 0, 0), name='Company links', cls='bb-foot-links bb-foot-1col'),
    ])
    contact = C('Contact', [
        eyebrow('Contact'),
        ILIST([('map-pin', '324 41 Ave NE<br>Calgary, AB T2E 2N3', MAPS)], t=M(14, 400, 24), color=wht(0.65), ic_color=BEE, ic_size=16,
              gap_=12, mar=(20, 0, 16, 0), name='Address', cls='bb-top-icon'),
        ILIST([('phone', PHONE, TEL)], t=M(14, 700, 20), color=PAPER, ic_color=BEE, ic_size=16, gap_=12, mar=(0, 0, 16, 0),
              name='Phone', cls='bb-hover-bee'),
        ILIST([('phone', PHONE2, TEL2)], t=M(14, 700, 20), color=wht(0.65), ic_color=BEE, ic_size=16, gap_=12, mar=(0, 0, 16, 0),
              name='Phone 2', cls='bb-hover-bee'),
        ILIST([('mail', EMAIL, 'mailto:' + EMAIL)], t=M(14, 400, 20), color=wht(0.65), ic_color=BEE, ic_size=16, gap_=12,
              mar=(0, 0, 16, 0), name='Email', cls='bb-top-icon bb-break'),
        ILIST([('clock-3', 'Monday–Friday<br>9:00 AM–6:00 PM<br>Weekends closed', None)], t=M(14, 400, 24), color=wht(0.65),
              ic_color=BEE, ic_size=16, gap_=12, name='Hours', cls='bb-top-icon'),
    ])
    cols = C('Columns', [about, svc, company, contact], grid='1fr 1.6fr 0.7fr 1fr', grid_tablet='repeat(2, minmax(0, 1fr))', grid_mobile='1fr',
             rows='auto', rows_tablet='auto', rows_mobile='auto', gap=48, gap_mobile=32, pad=(56, 0), pad_mobile=(32, 0),
             border=(dims(0, 0, 1, 0), wht(0.15)))

    form = W('form', 'Footer email form', form_name='Footer enquiry',
             form_fields=[{'_id': 'email', 'custom_id': 'email', 'field_type': 'email', 'field_label': 'Your email address',
                           'placeholder': 'Your email address', 'width': '100', 'required': 'true'}],
             show_labels='', input_size='md', button_text='Send email', button_size='md', button_width='',
             selected_button_icon=icon('arrow-right'), button_icon_align='row-reverse', submit_actions=['email'], email_to=EMAIL,
             email_subject='Website enquiry – please contact me about my vehicle',
             email_content='Please contact me at [field id="email"] about my vehicle.', email_reply_to='email',
             email_from_name='Busy Bee website', success_message="Thanks! We'll email you back shortly.",
             column_gap=px(8), row_gap=px(8), field_text_color=PAPER, **{('field_' + k): v for k, v in M(14, 400, 20).items()},
             field_background_color=wht(0.05), field_border_color=wht(0.2), field_border_width=dims(1), field_border_radius=dims(PILL),
             button_background_color=BEE, button_text_color=INK, button_background_hover_color='#E9CB0A', button_hover_color=INK,
             button_border_radius=dims(PILL), button_text_padding=dims(18, 28),
             **{('button_' + k): v for k, v in M(14, 700, 20).items()}, cls='bb-foot-form')
    news = C('Email row', [
        C('Copy', [H('Questions about your vehicle?', 'p', PAPER, M(24, 800, 32, size_m=20, lh_m=28), name='Title'),
                   T('<p>Enter your email and start a message to our shop.</p>', wht(0.5), M(14, 400, 20), mar=(8, 0, 0, 0), name='Text')]),
        form,
    ], grid='1fr 1.2fr', grid_mobile='1fr', rows='auto', rows_mobile='auto', ai='center', gap=24, pad=(40, 0),
        border=(dims(0, 0, 1, 0), wht(0.15)))
    legal = C('Legal', [
        H('© 2026 Busy Bee Auto Repair', 'span', wht(0.35), M(10, 400, 15, 1.6, 'uppercase'), name='Copyright'),
        H('Calgary, Alberta', 'span', wht(0.35), M(10, 400, 15, 1.6, 'uppercase'), name='City'),
        H('Design &amp; developed by <a href="https://devixpert.com/" target="_blank" rel="noopener">DeviXpert</a>', 'span', wht(0.35),
          M(10, 400, 15, 1.6, 'uppercase'), name='Credit', cls='bb-credit'),
    ], d='row', d_mobile='column', jc='space-between', ai='center', ai_mobile='flex-start', gap=12, pad=(28, 0, 0, 0))

    import build_inner
    root = C('Footer', [C('Inner', [cta, cols, news, legal], w=cu('min(1280px, 100%)'), mar=(0, 'auto'), z=1),
                        build_inner.callbar()],
             tag='footer', pad=(80, 32, 32, 32), pad_mobile=(40, 20, 96, 20), bgimg='busy-bee-auto-repair-storefront-calgary',
             bg=INK, ov=True, cls='bb-footer')
    return el.book_popup([root], json.load(open('ids.json'))['popup_book'])


if __name__ == '__main__':
    el.save('elementor_library', FOOTER_ID, build(), extra={'title': 'Busy Bee – Footer'})
    el.regen(FOOTER_ID)
