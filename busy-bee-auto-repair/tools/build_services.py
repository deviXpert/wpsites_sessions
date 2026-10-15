"""Busy Bee /services/ page (design: busy-bee-auto-repair-preview…/services).  Elementor Canvas template – the page carries its
the global inner header (mega menu) floats over the hero; the global inner footer closes the page.  Reviews + suppliers reuse the home-page builders."""
import json
import el
import build_home as home
from common import *
from el import uid
from sitemap import SERVICE_PAGES

SIDE = 'max(32px, 50vw - 650px)'          # hero side padding from the design
DK2 = '#192124'
LINE = '#DCE0DD'
WA = 'https://wa.me/14039305888?text=' + 'Hi%20Busy%20Bee%2C%20I%27d%20like%20to%20ask%20about%20service%20for%20my%20vehicle.'

REASONS = [('wrench', 'Practical expertise'), ('clipboard-check', 'Clear estimates'), ('scan-search', 'Careful diagnostics'),
           ('clock-3', 'Walk-ins welcome'), ('settings', 'Parts options explained'), ('shield-check', 'Warranty on most repairs'),
           ('sparkles', 'Care for your vehicle')]
STEPS = [('calendar-check', 'Book your visit', 'Call or send your service request.'),
         ('message-square', 'Describe the issue', 'Tell us what changed and when.'),
         ('scan-search', 'We inspect', 'We investigate the symptoms.'),
         ('clipboard-check', 'You approve', 'Review the findings and estimate.'),
         ('car-front', 'Back on the road', 'Collect your car after agreed repairs.')]
FAQS = [
    ('What auto repair services do you offer?', 'We offer diagnostics, engine repairs, brakes, oil changes, suspension and steering repairs, '
     'tires, battery and charging-system checks, cooling-system repairs and transmission service. Call to discuss the work your '
     'vehicle needs.'),
    ('Do I need an appointment?', 'Call ahead to arrange your visit. Walk-ins are welcome during business hours; timing depends on the '
     'work required and workshop availability.'),
    ('Will I get a price before repairs begin?', 'Yes. We explain our findings and provide an estimate for your approval before '
     'starting the agreed repairs.'),
    ('Do you work on my make and model?', 'We work on domestic, Asian and European vehicles. For imported, electric or hybrid variants, '
     'call first so we can confirm the equipment and service required.'),
    ('Do repairs include a warranty?', 'Most repairs include a parts and labour warranty. Ask our team about the coverage and conditions '
     'for your specific job.'),
    ('Where is Busy Bee located?', 'Find us at 324 41 Ave NE, Calgary, AB T2E 2N3. We are open Monday to Friday, 9 AM to 6 PM.'),
]


def yellow_btn(text, href, ic='arrow-up-right', **kw):
    return BTN(text, href, S(13, 800, 19.5), color=DK2, bg=YEL, ic=ic, ic_size=18, ic_gap=15, pad=(14, 22), radius=6,
               hover_bg='#F2DC00', hover_color=DK2, **kw)


def wa_btn(**kw):
    return BTN('WhatsApp us', WA, S(13, 750, 16.9), color=PAPER, bg='#128C50', ic='whatsapp', ic_pos='before', ic_size=22, ic_gap=9,
               pad=(12, 19), radius=30, border=(1, '#128C50'), hover_bg='#096D3C', hover_color=PAPER, name='WhatsApp us',
               cls='bb-wa', **kw)


def title(text, em, name='Section title', mar=(0, 0, 30, 0)):
    line = lambda: C('Line', [], minh=1, bg=LINE, w='auto', cls='bb-sm-line')
    return C(name, [line(), H(f'{text} <em>{em}</em>', 'h2', DK2, S(30, 850, 45, -1.05, 'uppercase', size_m=24, lh_m=36, ls_m=-0.84),
                              align='center', name='Title', cls='bb-sm-h2'), line()],
             d='row', ai='center', gap=24, mar=mar, cls='bb-sm-title')


# ---------------------------------------------------------------- hero
HERO_SLIDES = [('busy-bee-repair-bay-calgary', 'Mechanic servicing a car in the Busy Bee workshop'),
               ('busy-bee-service-bays-calgary', 'Tire, engine and diagnostic work bays')]
TRUST = [('wrench', 'Hands-on repair'), ('clipboard-check', 'Upfront estimates'), ('shield-check', 'Warranty on most repairs'),
         ('map-pin', 'Local Calgary workshop')]


def hero(h1='Car repair &amp; maintenance services in <em>Calgary.</em>',
         intro='From routine oil changes to complex engine and electrical repairs, Busy Bee Auto Repair handles it all at one NE '
               'Calgary shop. Choose a service below to see what’s included, common warning signs, and how we work.',
         eyebrow='YOUR LOCAL WORKSHOP · NE CALGARY', slides=HERO_SLIDES, actions=None, aside=None, trust=TRUST, select=True):
    """Dark photo hero shared by every inner page.  The global inner header (pill + mega menu) floats over its top."""
    slides_ = [IMG(k, w=pct(100), h=cu('100%'), fit='cover', posn='center 40%', alt=alt, name='Slide ' + str(i + 1),
                   cls='bb-sm-slide' + (' is-active' if i == 0 else ''))
               for i, (k, alt) in enumerate(slides)]
    intro_ = C('Intro', [
        H(eyebrow, 'p', YEL, S(10, 800, 15, 1.6), name='Eyebrow'),
        H(h1, 'h1', PAPER, S(cu('clamp(34px, 4.4vw, 64px)'), 800, 1.05, cu('-0.03em'), 'uppercase'), mar=(20, 0, 20, 0), name='Title',
          cls='bb-sm-h1'),
        T(f'<p>{intro}</p>', '#EEF0F1', S(16, 400, 28, size_m=15, lh_m=26), w=560, w_mobile='full', name='Text'),
        C('Actions', actions or [yellow_btn('Request a service', '#service-book', name='Request a service'), wa_btn()],
          d='row', wrap='wrap', ai='center', gap=12, mar=(24, 0, 0, 0)),
    ], pad=(65, 0, 60, 0), pad_mobile=(48, 0, 36, 0), w=cu('min(680px, 100%)'), cls='bb-sm-intro')
    if aside is None:
        aside = home.aside()
        aside['settings'].update({'width': px(280), 'width_tablet': cu('min(400px, 100%)'), 'width_mobile': pct(100)})
    layout = C('Layout', [intro_, aside] if aside else [intro_], grid='minmax(0, 1fr) 280px' if aside else '1fr', grid_tablet='1fr',
               grid_mobile='1fr', rows='auto', rows_tablet='auto', rows_mobile='auto', ai='center', gap=65, gap_tablet=0,
               cls='bb-sm-layout')
    kids = [layout]
    if select and len(slides) > 1:
        kids.append(C('Photo select', [
            BTN(t, '#', S(11, 400, 16.5), color=PAPER, bg='rgba(23,32,36,0.44)', pad=(8, 16), radius=25,
                border=(1, 'rgba(255,255,255,0.5)'), name=t, cls='bb-sm-sel' + (' is-active' if i == 0 else ''), attrs={'data-slide': i})
            for i, t in enumerate(['Workshop', 'Service bays'][:len(slides)])], d='row', jc='flex-end', gap=8, pad=(0, 0, 25, 0),
            mar_mobile=(24, 0, 0, 0)))
    if trust:
        kids.append(C('Trust strip', [
            C(t, [ICON(ic, 24, color=YEL, name='Icon', w='auto'), H(t, 'span', PAPER, S(12, 700, 18), name='Label')],
              d='row', ai='center', gap=15, pad=23, cls='bb-sm-trust-item') for ic, t in trust
        ], grid=f'repeat({len(trust)}, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))', grid_mobile='repeat(2, minmax(0, 1fr))',
            rows='auto', rows_tablet='auto', rows_mobile='auto', gap=0, bg=DK2, radius=8, border=(1, 'rgba(255,255,255,0.19)'),
            mar=(0, 0, -24, 0), z=2, cls='bb-sm-trust'))
    else:
        kids.append(C('Spacer', [], minh=24))
    inner = C('Hero inner', kids, w=cu('min(1300px, 100%)'), mar=(0, 'auto'), z=1)
    return C('Hero', slides_ + [inner], tag='section', pad=(126, 0, 0, 0), pad_mobile=(84, 0, 0, 0), bg='#11191D',
             cls='bb-sm-hero bb-sys')


# ---------------------------------------------------------------- services grid
def card(value, ic, blurb, photo, href='#service-book'):
    return C(value, [
        IMG(photo, w=pct(100), h=cu('100%'), fit='cover', alt='', name='Photo', cls='bb-sm-card-img'),
        C('Copy', [
            ICON(ic, 24, color=YEL, name='Icon', w='auto'),
            H(value.replace('&', '&amp;'), 'h3', PAPER, S(22, 800, 1.1, tt='uppercase'), mar=(12, 0, 8, 0), w=320, name='Title'),
            H(blurb, 'p', '#E0E5E7', S(12, 400, 18), name='Blurb'),
            C('Explore', [H('Explore service', 'span', PAPER, S(11, 750, 16.5), name='Label'),
                          ICON('arrow-up-right', 16, color=YEL, name='Arrow', w='auto')], d='row', ai='center', gap=12, mar=(15, 0, 0, 0)),
        ], pos={'x': 23, 'y': 23, 'v': 'end'}, w=cu('calc(100% - 46px)'), z=1),
    ], minh=280, bg='#172024', radius=8, ov=True, href=href, cls='bb-sm-card',
        attrs=None if href.startswith('/') else {'data-service': value})


def cta_card():
    return C('Not sure card', [
        ICON('scan-search', 28, color=DK2, name='Icon', w='auto'),
        H('Not sure what’s wrong?', 'h3', DK2, S(22, 800, 1.1, tt='uppercase'), mar=(12, 0, 8, 0), name='Title'),
        H('Describe the symptom and we’ll find the real cause before any repair.', 'p', DK2, S(13, 400, 20), name='Text'),
        C('Explore', [H('Request a diagnostic', 'span', DK2, S(11, 800, 16.5), name='Label'),
                      ICON('arrow-up-right', 16, color=DK2, name='Arrow', w='auto')], d='row', ai='center', gap=12, mar=(15, 0, 0, 0)),
    ], jc='flex-end', minh=280, pad=23, bg=YEL, radius=8, href='#service-book', cls='bb-sm-card-cta')


def page_cards():
    return [card(l, ic, sm, ph, href=u) for _, l, u, ic, sm, ph in SERVICE_PAGES] + [cta_card()]


def services_grid():
    return C('Our services', [title('Our automotive', 'services'),
                              C('Grid', page_cards(), grid='repeat(3, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))',
                                grid_mobile='1fr', rows='auto', rows_tablet='auto', rows_mobile='auto', gap=20)],
             tag='section', id_='our-services', pad=(66, 32, 60, 32), pad_mobile=(64, 22, 40, 22), w=cu('min(1300px, 100%)'),
             mar=(0, 'auto'), cls='bb-sys')


# ---------------------------------------------------------------- brands marquee
def brands():
    logos = dict((name, key) for key, name in home.BRAND_LOGOS)

    def cell(b):
        if b in logos:
            return C(b, [IMG(logos[b], w=90, h=40, fit='contain', alt=b, name='Logo'),
                         H(b, 'span', '#273034', S(11, 800, 16.5), align='center', name='Name')],
                     ai='center', jc='center', gap=12, w=150, minh=83, cls='bb-sm-brand')
        return C(b, [H(b, 'span', '#273034', S(18, 800, 27), align='center', name='Name')], ai='center', jc='center', w=150, minh=83, cls='bb-sm-brand')
    group = C('Brand group', [cell(b) for b in home.ALL_BRANDS], d='row', gap=20, pad=(0, 20, 0, 0), w=cu('max-content'))
    return C('Brands', [
        C('Title wrap', [title('All makes.', 'Expert care.', mar=(0, 0, 0, 0))], w=cu('min(1236px, 100%)'), mar=(0, 'auto'),
          pad=(0, 24)),
        C('Window', [C('Track', [group], d='row', w=cu('max-content'), cls='bb-sm-brand-track')], pad=(24, 0), bg=PAPER,
          border=(dims(1, 0, 1, 0), '#E4E7E3'), ov=True, mar=(30, 0, 0, 0), cls='bb-sm-brand-window'),
    ], tag='section', id_='service-brands', pad=(65, 0, 40, 0), ov=True, cls='bb-sys')


# ---------------------------------------------------------------- reasons
def reasons():
    return C('Why drivers choose us', [
        title('Why drivers', 'choose us'),
        C('Grid', [C(t, [ICON(ic, 34, color=DK2, name='Icon', w='auto', align='center', cls='bb-sw16'),
                         H(t, 'h3', DK2, S(12, 750, 1.4, tt='uppercase'), align='center', mar=(15, 0, 0, 0), name='Title')],
                     ai='center', pad=18, border=(dims(0, 1, 0, 0), LINE), cls='bb-sm-reason') for ic, t in REASONS],
          grid='repeat(7, minmax(0, 1fr))', grid_tablet='repeat(3, minmax(0, 1fr))', grid_mobile='repeat(3, minmax(0, 1fr))',
          rows='auto', rows_tablet='auto', rows_mobile='auto', gap=0),
    ], tag='section', pad=(10, 32, 60, 32), pad_mobile=(10, 22, 40, 22), w=cu('min(1300px, 100%)'), mar=(0, 'auto'), cls='bb-sys')


# ---------------------------------------------------------------- request form (opens WhatsApp)
def book(heading='Need your car checked <em>today?</em>', photo_key='engine-repair-audi-calgary', preset=''):
    photo = C('Photo', [
        IMG(photo_key, w=pct(100), h=cu('100%'), fit='cover', alt='', name='Photo', cls='bb-sm-card-img'),
        C('Copy', [
            H('LET’S GET IT SORTED', 'p', PAPER, S(13, 800, 22.1, 2.08), name='Eyebrow'),
            H(heading, 'h2', PAPER, S(40, 850, 1.06, -1.6, 'uppercase'), mar=(14, 0, 20, 0), w=348,
              name='Title', cls='bb-sm-em-yel'),
            T('<p>Tell us what’s happening. We’ll confirm availability and the next step.</p>', PAPER, S(13, 400, 22.1), w=330,
              name='Text'),
            ILIST([('check', 'Clear estimates. Your approval first.', None)], t=S(13, 400, 22.1), color=PAPER, ic_color=PAPER, ic_size=16,
                  gap_=8, mar=(18, 0, 0, 0), name='Check'),
        ], z=1),
    ], jc='flex-end', minh=500, minh_mobile=360, pad=42, pad_mobile=(42, 28), ov=True, cls='bb-sm-book-photo')
    opts = '\n'.join(['Select a service|'] + [l for _, l, *_ in SERVICE_PAGES] + ['Not sure — help me diagnose it'])
    F = home.form_field
    fields = [F('name', 'text', 'Name', '', '50', True), F('phone', 'tel', 'Phone', '', '50', True),
              F('vehicle', 'text', 'Vehicle make, model and year', 'e.g. 2020 Honda Civic', '100'),
              F('service', 'select', 'Service needed', '', '100', field_options=opts, field_value=preset),
              F('issue', 'textarea', 'Tell us about the issue', '', '100', rows=2)]
    for f in fields:
        if f['width'] == '50':
            f['width_mobile'] = '100'
    form = W('form', 'Request form', form_name='Service request (WhatsApp)', form_fields=fields, input_size='sm', show_labels='yes',
             button_text='Continue in WhatsApp', button_size='sm', button_width='100', selected_button_icon=icon('arrow-up-right'),
             button_icon_align='row-reverse', button_icon_indent=px(15), submit_actions=[], success_message='Opening WhatsApp…',
             column_gap=px(15), row_gap=px(12), label_spacing=px(6), label_color=PAPER,
             **{('label_' + k): v for k, v in S(11, 650, 16.5).items()},
             field_text_color=PAPER, **{('field_' + k): v for k, v in S(13, 400, 19.5).items()},
             field_background_color='rgba(255,255,255,0.03)', field_border_color='rgba(255,255,255,0.25)', field_border_width=dims(1),
             field_border_radius=dims(5), button_background_color=YEL, button_text_color=DK2, button_background_hover_color='#F2DC00',
             button_hover_color=DK2, button_border_radius=dims(6), button_text_padding=dims(14, 22),
             **{('button_' + k): v for k, v in S(13, 800, 19.5).items()}, mar=(20, 0, 0, 0), cls='bb-sm-form')
    right = C('Form side', [
        H('Request your service', 'h2', PAPER, S(25, 850, 26.5, -1, 'uppercase'), name='Title'),
        form,
        T('<p>Opens a message for you to send. The shop confirms your appointment.</p>', '#C6CDD0', S(10, 400, 16), mar=(12, 0, 0, 0),
          name='Note'),
    ], pad=32, pad_mobile=(32, 28))
    return C('Request', [C('Card', [photo, right], grid='1fr 1fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto',
                           rows_mobile='auto', gap=0, bg=DK2, radius=12, ov=True)],
             tag='section', id_='service-book', pad=(0, 32), pad_tablet=(0, 24), pad_mobile=(0, 24), w=cu('min(1300px, 100%)'),
             mar=(0, 'auto'), cls='bb-sys')


# ---------------------------------------------------------------- how it works
def steps():
    def step(i, ic, t, p):
        kids = [ICON(ic, 28, color='#172024', bg='#FFF5A8', box=52, radius=12, name='Icon', w='auto', cls='bb-sw16'),
                H(f'{i:02d}', 'span', '#939C98', S(12, 800, 18, 1.44), mar=(15, 0, 0, 0), name='Number'),
                H(t, 'h3', DK2, S(15, 800, 22.5, tt='uppercase'), mar=(12, 0, 12, 0), name='Title'),
                H(p, 'p', '#667074', S(12, 400, 19.2), name='Text')]
        if i < 5:
            kids.append(ICON('arrow-right', 20, color='#929D9D', name='Arrow', pos={'x': -20, 'y': 34, 'h': 'end'}, hide='tm', w='auto'))
        return C(t, kids, pad=(20, 0, 0, 0), border=(dims(2, 0, 0, 0), YEL))
    return C('How it works', [
        title('How it', 'works'),
        C('Steps', [step(i + 1, *s) for i, s in enumerate(STEPS)], grid='repeat(5, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))',
          grid_mobile='1fr', rows='auto', rows_tablet='auto', rows_mobile='auto', gap=24),
    ], tag='section', pad=(60, 32), pad_mobile=(40, 22), w=cu('min(1300px, 100%)'), mar=(0, 'auto'), cls='bb-sys')


# ---------------------------------------------------------------- FAQ + location
def faq(faqs=FAQS, eyebrow='BEFORE YOUR VISIT', heading='Questions?<br><em>Clear answers.</em>', id_='service-faq'):
    left = C('Intro', [
        H(eyebrow, 'p', DK2, S(10, 800, 15, 1.6), name='Eyebrow'),
        H(heading, 'h2', DK2, S(40, 850, 1.06, -1.6, 'uppercase'), mar=(14, 0, 20, 0), name='Title'),
        ILIST([('phone', PHONE, TEL)], t=S(14, 750, 21), color=DK2, ic_color=DK2, ic_size=18, gap_=10, name='Phone'),
    ])
    toggle = W('accordion', 'FAQ', tabs=[{'_id': uid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faqs],
               selected_icon=icon('caret-right', 'fas fa-caret-right'), selected_active_icon=icon('caret-down', 'fas fa-caret-down'),
               icon_align='left', icon_space=px(8), title_html_tag='h3', faq_schema='yes', border_width=px(0), space_between=px(0),
               title_color=DK2, tab_active_color=DK2, icon_color=DK2, icon_active_color=DK2, title_padding=dims(19, 0),
               content_padding=dims(0, 0, 19, 0), content_color='#596367',
               **{('title_' + k): v for k, v in S(15, 750, 22.5).items()}, **{('content_' + k): v for k, v in S(13, 400, 23.4).items()},
               cls='bb-sm-faq')
    return C('FAQ', [left, toggle], grid='0.85fr 1.3fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto',
             rows_mobile='auto', gap=60, gap_tablet=24, tag='section', id_=id_, pad=(60, 32), pad_mobile=(40, 22),
             w=cu('min(1300px, 100%)'), mar=(0, 'auto'), cls='bb-sys')


def location():
    card_ = C('Card', [
        H('FIND BUSY BEE', 'p', DK2, S(14, 800, 25.2, 2.24), name='Eyebrow'),
        H('Your neighbourhood<br><em>repair shop.</em>', 'h2', DK2, S(40, 850, 1.06, -1.6, 'uppercase', size_m=34), mar=(14, 0, 20, 0),
          name='Title'),
        T('<p>324 41 Ave NE<br>Calgary, AB T2E 2N3</p><p>Monday–Friday · 9 AM–6 PM</p>', DK2, S(14, 400, 25.2), name='Address',
          cls='bb-sm-addr'),
        C('Actions', [yellow_btn('Get directions', MAPS, name='Get directions'), wa_btn()], d='row', wrap='wrap', ai='center', gap=12,
          mar=(14, 0, 0, 0)),
    ], pad=30, bg='#F3F3E7', radius=8)
    gmap = W('google_maps', 'Map', address='324 41 Ave NE, Calgary, AB T2E 2N3', zoom={'unit': 'px', 'size': 15}, height=px(390),
             cls='bb-sm-map')
    return C('Location', [card_, gmap], grid='1fr 1fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto',
             rows_mobile='auto', gap=35, tag='section', id_='service-location', pad=(60, 32), pad_mobile=(40, 22),
             w=cu('min(1300px, 100%)'), mar=(0, 'auto'), cls='bb-sys')


def build():
    el.seed('services')
    return el.book_popup([hero(), services_grid(), brands(), reasons(), book(), steps(), faq(), location(), home.reviews(),
                          home.suppliers()], json.load(open('ids.json'))['popup_book'])


PAGE_SETTINGS = {'hide_title': 'yes', 'template': 'elementor_header_footer', 'background_background': 'classic',
                 'background_color': '#FBFCFA'}

if __name__ == '__main__':
    import wp
    ids = json.load(open('ids.json'))
    if 'services' not in ids:
        d = wp.post('wp/v2/pages', {'title': 'Services', 'slug': 'services', 'status': 'publish', 'template': 'elementor_header_footer'})
        ids['services'] = d['id']
        json.dump(ids, open('ids.json', 'w'), indent=1)
    el.save('pages', ids['services'], build(), page_settings=PAGE_SETTINGS,
            extra={'template': 'elementor_header_footer', 'title': 'Services',
                   'excerpt': 'Auto repair services in NE Calgary: diagnostics, engine, brakes, oil changes, suspension, tires, '
                              'battery, cooling and transmission repair.'})
    el.regen(ids['services'])
