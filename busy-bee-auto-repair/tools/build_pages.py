"""About Us (/about-us/) and Contact Us (/contact-us/) – copy from design/content-seo.md, built in the /services/ design language.
Usage: python3 build_pages.py [about|contact]"""
import json, sys
import el, wp
from build_globals import tpl
import build_home as home
import build_services as svc
import build_service_pages as sp
from common import *
from sitemap import SERVICE_PAGES

DK2 = svc.DK2


# ---------------------------------------------------------------- About
def about():
    el.seed('about')
    hero = svc.hero(h1='About Busy Bee Auto Repair &amp; <em>Tire Shop</em>',
                    intro='Busy Bee Auto Repair & Tire Shop is a family-owned garage in NE Calgary. We started with a simple idea: treat '
                          'every customer’s car like it belongs to our own family. That means honest diagnosis, fair prices, and work '
                          'we’re proud to put our name on.',
                    eyebrow='FAMILY-OWNED · NE CALGARY', slides=[('busy-bee-auto-repair-storefront-calgary', '')],
                    actions=[svc.yellow_btn('Book an appointment', '#book', name='Book'), svc.wa_btn()], select=False)
    diff = [('message-square', 'Straight answers', 'We explain what’s wrong, what’s urgent, and what can wait.'),
            ('clipboard-check', 'No surprise bills', 'You approve every repair and price before we start.'),
            ('shield-check', 'Certified technicians', 'Experienced mechanics who work on all makes and models.'),
            ('scan-search', 'Modern equipment', 'Advanced diagnostic tools that find problems fast.'),
            ('wrench', 'Quality parts', 'Reliable parts backed by warranty.')]
    different = sp.wrap('What makes us different', [
        svc.title('What makes us', 'different'),
        C('Grid', [C(t, [ICON(ic, 28, color=DK2, bg='#FFF5A8', box=52, radius=12, name='Icon', w='auto', cls='bb-sw16'),
                         H(t, 'h3', DK2, S(15, 800, 22.5, tt='uppercase'), mar=(16, 0, 8, 0), name='Title'),
                         H(d, 'p', '#667074', S(13, 400, 20.8), name='Text')], pad=(20, 0, 0, 0), border=(dims(2, 0, 0, 0), YEL))
                   for ic, t, d in diff],
          grid='repeat(5, minmax(0, 1fr))', grid_tablet='repeat(3, minmax(0, 1fr))', grid_mobile='1fr', rows='auto', rows_tablet='auto',
          rows_mobile='auto', gap=24)])
    story = sp.sec_text('Our story', [
        'Busy Bee is run by a local family, not a chain. Our name is on every job, and our reputation in NE Calgary depends on '
        'getting it right the first time.',
        'Our technicians work on domestic, Asian and European cars, SUVs and light trucks every day, from Mobil 1 oil changes and '
        'seasonal tire swaps to check engine lights other shops couldn’t solve. You get a clear diagnosis, an honest quote, and the '
        'work done right.'], 'busy-bee-repair-bay-calgary')
    calgary = sp.sec_callout('Built for Calgary driving',
                             'Cold starts, chinooks, potholes, and road salt are hard on a car. We know what fails here and why, and '
                             'we’ll tell you what can wait.')
    cards = tpl('services_grid')
    body = [hero, C('Spacer', [], minh=24), different, story, calgary, tpl('reviews'), cards, tpl('booking'),
            tpl('location')]
    return el.book_popup(body, json.load(open('ids.json'))['popup_book'])


# ---------------------------------------------------------------- Contact
def contact():
    el.seed('contact')
    quick = [('phone', 'Call the shop', PHONE, TEL), ('navigation', 'Get directions', '324 41 Ave NE, Calgary', MAPS),
             ('mail', 'Email us', EMAIL, 'mailto:' + EMAIL), ('whatsapp', 'WhatsApp', 'Message the shop', svc.WA)]
    social = [('facebook', FACEBOOK), ('instagram', INSTAGRAM)]
    actions = C('Quick actions', [
        C(t, [ICON(ic, 22, color=DK2, bg=YEL, box=44, radius=12, name='Icon', w='auto'),
              C('Text', [H(t, 'span', '#C6CDD0', S(11, 700, 16.5, 0.88, 'uppercase'), name='Label'),
                         H(v, 'span', PAPER, S(15, 800, 21), name='Value', cls='bb-break')], w='auto', grow=True, cls='bb-shrink')],
          d='row', ai='center', gap=14, pad=18, radius=12, bg='rgba(255,255,255,0.06)', border=(1, 'rgba(255,255,255,0.18)'), href=h,
          cls='bb-quick')
        for ic, t, v, h in quick], grid='repeat(4, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))', grid_mobile='1fr',
        rows='auto', rows_tablet='auto', rows_mobile='auto', gap=12, mar=(0, 0, 40, 0))
    hero = svc.hero(h1='Contact Busy Bee Auto Repair in <em>Calgary</em>',
                    intro='Ready to book, need a quote, or have a question about your car? Call, email, or send the form below and '
                          'we’ll get back to you quickly.',
                    eyebrow='CONTACT · NE CALGARY', slides=[('busy-bee-auto-repair-storefront-calgary', '')],
                    actions=[svc.yellow_btn('Call ' + PHONE, TEL, ic='phone', name='Call'),
                             BTN('Get directions', MAPS, S(13, 800, 19.5), color=PAPER, bg='rgba(0,0,0,0)', ic='navigation',
                                 ic_pos='before', ic_size=16, pad=(14, 22), radius=6, border=(1, 'rgba(255,255,255,0.5)'),
                                 hover_bg=PAPER, hover_color=DK2, name='Directions')],
                    aside=False, select=False, trust=None)
    hero['elements'][-1]['elements'].insert(-1, actions)
    hours = W('price-list', 'Hours', price_list=[
        {'_id': el.uid(), 'title': d, 'price': h, 'item_description': '', 'link': {'url': ''}}
        for d, h in [('Monday to Friday', '9 AM to 6 PM'), ('Saturday', 'Closed'), ('Sunday', 'Closed')]],
        heading_color=DK2, price_color=DK2, separator_style='dotted', separator_weight=px(2), separator_color='#C9CFC6',
        **{('heading_' + k): v for k, v in S(15, 700, 22).items()}, **{('price_' + k): v for k, v in S(15, 800, 22).items()},
        cls='bb-price-list')
    visit = C('Visit', [
        H('VISIT OUR SHOP', 'p', DK2, S(11, 800, 16.5, 1.76), name='Eyebrow'),
        H('Busy Bee Auto Repair &amp; Tire Shop', 'h2', DK2, S(30, 850, 1.1, -1, 'uppercase', size_m=24), mar=(12, 0, 18, 0),
          name='Title'),
        ILIST([('map-pin', '324 41 Ave NE, Calgary, AB T2E 2N3', MAPS), ('phone', PHONE, TEL), ('mail', EMAIL, 'mailto:' + EMAIL)],
              t=S(15, 600, 24), color=DK2, ic_color=DK2, ic_size=18, gap_=12, space=14, name='NAP', cls='bb-break'),
        H('Hours', 'h3', DK2, S(18, 800, 24, tt='uppercase'), mar=(28, 0, 12, 0), name='Hours title'), hours,
        H('Follow us', 'h3', DK2, S(18, 800, 24, tt='uppercase'), mar=(28, 0, 10, 0), name='Follow title'),
        C('Social', [ICON(ic, 18, color=DK2, bg=PAPER, box=40, radius=20, href=u, name=ic.title(), w='auto') for ic, u in social],
          d='row', gap=10),
        H('Getting here', 'h3', DK2, S(18, 800, 24, tt='uppercase'), mar=(28, 0, 10, 0), name='Getting here'),
        T('<p>We’re in NE Calgary off 41 Avenue NE, a few minutes from Deerfoot Trail and Edmonton Trail. Appointments and walk-ins '
          'welcome.</p>', '#4B5558', S(14, 400, 23), name='Directions'),
    ], pad=(32, 34), pad_mobile=24, bg='#F3F3E7', radius=12)
    gmap = W('google_maps', 'Map', address='Busy Bee Auto Repair, 324 41 Ave NE, Calgary, AB T2E 2N3', zoom={'unit': 'px', 'size': 15},
             height=px(560), height_mobile=px(320), cls='bb-sm-map')
    info = sp.wrap('Visit', [C('Grid', [visit, gmap], grid='1fr 1fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto',
                                 rows_tablet='auto', rows_mobile='auto', gap=24)], id_='visit')
    body = [hero, info, booking_form(), tpl('faq')]
    return el.book_popup(body, json.load(open('ids.json'))['popup_book'])


def booking_form():
    F = home.form_field
    reasons = '\n'.join(['Select a reason|'] + [l for _, l, *_ in SERVICE_PAGES] + ['Not sure — help me diagnose it', 'Quote request',
                                                                                     'Other'])
    fields = [F('name', 'text', 'Name', 'Your name', '50', True), F('phone', 'tel', 'Phone', '(403) 555-0123', '50', True),
              F('email', 'email', 'Email (for confirmations)', 'you@example.com', '50'),
              F('reason', 'select', 'Reason for visit', '', '50', True, field_options=reasons),
              F('date', 'date', 'Preferred date', '', '50'), F('time', 'time', 'Preferred time', '', '50'),
              F('details', 'textarea', 'Repair details', 'Vehicle make, model and year, plus what you’ve noticed', '100', rows=4)]
    for f in fields:
        if f['width'] == '50':
            f['width_mobile'] = '100'
    form = W('form', 'Appointment form', form_name='Contact page – appointment request', form_fields=fields, input_size='md',
             show_labels='yes', button_text='Request my appointment', button_size='md', button_width='100',
             selected_button_icon=icon('arrow-up-right'), button_icon_align='row-reverse', button_icon_indent=px(12),
             submit_actions=['email'], email_to=EMAIL, email_subject='Appointment request – [field id="reason"] – busybeeautorepair website',
             email_content='[all-fields]', email_reply_to='email', email_from_name='Busy Bee website',
             success_message="Thanks! We'll call you back within business hours to confirm your appointment.",
             column_gap=px(16), row_gap=px(16), label_spacing=px(6), label_color=DK2,
             **{('label_' + k): v for k, v in S(12, 700, 18).items()}, field_text_color=DK2,
             **{('field_' + k): v for k, v in S(15, 400, 22).items()}, field_background_color=PAPER, field_border_color='#D3D8D4',
             field_border_width=dims(1), field_border_radius=dims(6), button_background_color=YEL, button_text_color=DK2,
             button_background_hover_color='#F2DC00', button_hover_color=DK2, button_border_radius=dims(6),
             button_text_padding=dims(16, 22), **{('button_' + k): v for k, v in S(14, 800, 20).items()}, cls='bb-contact-form')
    return sp.wrap('Book an appointment', [C('Card', [
        C('Copy', [H('BOOK AN APPOINTMENT', 'p', YEL, S(11, 800, 16.5, 1.76), name='Eyebrow'),
                   H('Tell us what your vehicle <em>needs.</em>', 'h2', PAPER, S(36, 850, 1.08, -1.2, 'uppercase', size_m=28),
                     mar=(12, 0, 16, 0), name='Title', cls='bb-sm-em-yel'),
                   T('<p>Send the form and we’ll call you back within business hours to confirm a time. Prefer to talk? Call '
                     '<a href="tel:+14039305888">(403) 930-5888</a>.</p>', '#C6CDD0', S(14, 400, 23), name='Text'),
                   ILIST([('check', 'Clear estimates. Your approval first.', None), ('check', 'Walk-ins welcome Mon–Fri', None),
                          ('check', 'All makes and models', None)], t=S(14, 600, 22), color=PAPER, ic_color=YEL, ic_size=16, gap_=10,
                         space=10, mar=(20, 0, 0, 0), name='Points')], pad=36, pad_mobile=26),
        C('Form', [form], pad=36, pad_mobile=(26, 22), bg=PAPER, radius=12, mar=(10, 10, 10, 0), mar_mobile=(0, 10, 10, 10)),
    ], grid='0.8fr 1.2fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto', rows_mobile='auto', gap=0, bg=DK2,
        radius=14)], id_='book-form')


PAGES = {'about': ('About Us', 'about-us', about, 'About Busy Bee Auto Repair | Family-Owned Calgary Mechanic',
                   'Meet Busy Bee Auto Repair & Tire Shop, a family-owned NE Calgary mechanic known for honest diagnosis, fair prices, and '
                   'certified technicians.', 'AboutPage'),
         'contact': ('Contact Us', 'contact-us', contact, 'Contact Busy Bee Auto Repair | 324 41 Ave NE Calgary',
                     'Book auto repair in NE Calgary. Call (403) 930-5888 or visit us at 324 41 Ave NE, Calgary, AB T2E 2N3. Appointments '
                     'and walk-ins welcome.', 'ContactPage')}

if __name__ == '__main__':
    ids = json.load(open('ids.json'))
    for key in (sys.argv[1:] or list(PAGES)):
        label, slug, fn, seo, meta, schema = PAGES[key]
        if 'page_' + key not in ids:
            d = wp.post('wp/v2/pages', {'title': label, 'slug': slug, 'status': 'publish', 'template': 'elementor_header_footer'})
            ids['page_' + key] = d['id']
            json.dump(ids, open('ids.json', 'w'), indent=1)
        pid = ids['page_' + key]
        el.save('pages', pid, fn(), page_settings=svc.PAGE_SETTINGS,
                extra={'template': 'elementor_header_footer', 'title': sp.seo_page_title(seo), 'slug': slug, 'excerpt': meta})
        el.regen(pid)
        wp.mcp('yoast-seo/update-post-seo-data', {'post_id': pid, 'schema_page_type': schema})
        print(key, pid, wp.get(f'wp/v2/pages/{pid}?_fields=link')['link'])
