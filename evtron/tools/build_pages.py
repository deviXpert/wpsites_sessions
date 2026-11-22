"""Site pages in the V2 glass style: Installation, FAQs, Contact, Warranty, Grants + legal pages.
Facts only from docs/client-answers.md, docs/client-about.md and the client's 19 Nov feedback. Nothing invented.
Legal pages render docs/legal/<slug>.md when it exists (headings with '#'/'##', paragraphs, '- ' bullets);
until then they show an honest 'being finalised' notice.
Run: EVTRON_WP_USER=<admin login> python3 build_pages.py [slug ...]"""
import json
import os
import sys
import urllib.parse

import wp
import build_v2 as B
from build_home import el, div, p, h, cfg, st, cl, MONO

C = json.load(open('created.json'))
chip, v2head, v2sec, itile, vbtn = B.chip, B.v2head, B.v2sec, B.itile, B.vbtn
PRODUCT = '/ev-chargers/evtron-tethered-ev-charger/'
TICK = lambda cid: el('e-svg', cid, {'svg': {'value': 'fa-solid fa-check', 'library': 'fa-solid'}}, 'width: 14px; height: 14px; color: #55E68B;')
INPUT = 'width: 100%; min-height: 50px; padding: 12px 16px; border-radius: 12px; border: 1px solid #6A7688; background-color: rgba(7,17,14,0.6); color: #F5FFF8; font-size: 15px;'
LABEL = 'font-size: 13px; color: #C9D6CE; font-weight: 500;'


# ---------------- shared building blocks ----------------
def ticks(cid, items, size='15.5px'):
    return div(cid, [div(f'{cid} {i}', [TICK(f'{cid} {i} t'), p(f'{cid} {i} p', t, None, f'font-size: {size}; color: #DCE8E0; line-height: 1.5;')],
                         'display: flex; gap: 10px; align-items: flex-start;') for i, t in enumerate(items)], 'display: flex; flex-direction: column; gap: 12px;')


def hero(cid, chip_text, title, lead, side=None):
    copy = div(cid + ' copy', [chip(cid + ' chip', chip_text),
                               h(cid + ' title', title, 'h1', ['v2-display'], 'margin-top: 26px; font-size: clamp(42px, 5.4vw, 84px);'),
                               p(cid + ' lead', lead, ['v2-lead'], 'margin-top: 24px; max-width: 58ch;')],
               'display: flex; flex-direction: column; align-items: flex-start;')
    inner = div(cid + ' grid', [copy, side], 'display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); gap: 56px; align-items: end; '
                '@media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; }') if side else copy
    return div(cid, [div(cid + ' inner', [inner], classes=['ev-container'])], classes=['v2-hero'], tag='section')


def facts_panel(cid, rows):
    return div(cid, [div(f'{cid} {i}', [p(f'{cid} {i} k', k, ['v2-label']), p(f'{cid} {i} v', v, None, 'font-size: 16px; color: #F5FFF8; font-weight: 600; margin-top: 6px;')],
                         'padding: 16px 0;' + ('' if i == len(rows) - 1 else ' border-bottom: 1px solid rgba(190,255,215,0.12);')) for i, (k, v) in enumerate(rows)],
               'padding: 12px 28px; @media(--mobile){ padding: 8px 20px; }', ['v2-glass'])


def field(cid, fid, label, ftype='text', required=True, placeholder='', full=False):
    return div(cid, [el('e-form-label', cid + ' l', {'text': label + (' *' if required else ''), 'input-id': fid}, LABEL),
                     el('e-form-input', cid + ' i', {'type': ftype, 'required': required, 'placeholder': placeholder, '_cssid': fid}, INPUT)],
               'display: flex; flex-direction: column; gap: 8px; width: 100%;' + (' grid-column: 1 / -1;' if full else ''))


def select(cid, fid, label, name, options):
    return div(cid, [el('e-form-label', cid + ' l', {'text': label, 'input-id': fid}, LABEL),
                     el('e-form-select', cid + ' s', {'name': name, 'options': [{'key': o, 'value': o} for o in options]}, INPUT)],
               'display: flex; flex-direction: column; gap: 8px; width: 100%;')


def textarea(cid, label, placeholder, required=False):
    return div(cid, [el('e-form-label', cid + ' l', {'text': label + (' *' if required else '')}, LABEL),
                     el('e-form-textarea', cid + ' t', {'rows': 4, 'placeholder': placeholder, 'required': required}, INPUT)],
               'display: flex; flex-direction: column; gap: 8px; width: 100%; grid-column: 1 / -1;')


def form(cid, name, to, subject, fields, submit, success, consent):
    return el('e-form', cid, {'form-name': name, 'actions-after-submit': ['collect-submissions', 'email'],
                              'email': {'to': [to], 'subject': subject, 'from-name': 'EV-Tron website', 'send-as': 'html'}},
              'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }', ['v2-form'], fields + [
        div(cid + ' consent', [el('e-form-checkbox', cid + ' cc', {'name': 'consent', 'value': 'yes', 'required': True}, 'width: 20px; height: 20px; flex: 0 0 20px; margin-top: 2px; accent-color: #55E68B;'),
                               el('e-form-label', cid + ' cl', {'text': consent + ' *'}, 'font-size: 13.5px; color: #C9D6CE; line-height: 1.5;')],
            'display: flex; gap: 12px; align-items: flex-start; grid-column: 1 / -1;'),
        div(cid + ' submit row', [el('e-form-submit-button', cid + ' submit', {'text': submit},
                                     'min-height: 54px; padding: 0 32px; border-radius: 999px; border: 0; font-weight: 600; font-size: 16px; color: #06150C; background-color: #55E68B; cursor: pointer;', ['v2-btn-primary'])],
            'grid-column: 1 / -1;'),
        el('e-form-success-message', cid + ' ok', None, 'grid-column: 1 / -1; padding: 18px; border-radius: 14px; background-color: rgba(85,230,139,0.12); color: #DFFBEA; font-size: 15px; text-align: left;', None,
           [p(cid + ' ok p', success, None, 'color: #DFFBEA;')]),
        el('e-form-error-message', cid + ' err', None, 'grid-column: 1 / -1; padding: 18px; border-radius: 14px; background-color: rgba(229,72,77,0.14); color: #FFD9DA; font-size: 15px; text-align: left;', None,
           [p(cid + ' err p', 'Sorry, something went wrong. Please try again, or email ' + to + '.', None, 'color: #FFD9DA;')]),
    ])


def accordion(cid, qa):
    items = [el('e-accordion-item', f'{cid} {i}', None, 'border-radius: 16px;', None, [
        el('e-accordion-item-header', f'{cid} {i} h', None, 'padding: 22px 24px; gap: 20px; @media(--mobile){ padding: 18px 16px; }', None, [
            el('e-accordion-item-title', f'{cid} {i} tt', None, None, None, [p(f'{cid} {i} q', q, None, 'color: #F5FFF8; font-weight: 600; font-size: 17px; line-height: 1.4;')]),
            el('e-accordion-item-icon', f'{cid} {i} ic', None, 'width: 32px; height: 32px; min-width: 32px; flex: 0 0 32px; display: flex; align-items: center; justify-content: center; padding: 0; '
               'border: 1px solid rgba(190,255,215,0.24); border-radius: 999px; color: #A3FFC1;', None,
               [el('e-svg', f'{cid} {i} plus', {'svg': {'value': 'fa-solid fa-plus', 'library': 'fa-solid'}}, 'width: 12px; height: 12px;')])]),
        el('e-accordion-item-content', f'{cid} {i} c', None, 'padding: 0 24px 24px; @media(--mobile){ padding: 0 16px 20px; }', None, [p(f'{cid} {i} a', a, ['v2-body'], 'max-width: 68ch;')])])
        for i, (q, a) in enumerate(qa)]
    return el('e-accordion', cid, {'default_state': 'all_collapsed', 'max_expanded': 'one', 'show_icon': True, 'icon_rotation': 45, 'faq_schema': True},
              'display: flex; flex-direction: column; gap: 10px;', None, items)


def cta_band(cid, title, lead, buttons):
    return v2sec(cid, [div(cid + ' card', [
        div(cid + ' copy', [h(cid + ' t', title, 'h2', ['v2-h2']), p(cid + ' l', lead, ['v2-lead'], 'margin-top: 14px;')]),
        div(cid + ' btns', [vbtn(f'{cid} b{i}', t, u, k) for i, (t, u, k) in enumerate(buttons)], 'display: flex; flex-wrap: wrap; gap: 12px; width: auto; flex: 0 0 auto;'),
    ], 'display: flex; justify-content: space-between; align-items: center; gap: 32px; padding: 48px; @media(--tablet){ flex-direction: column; align-items: flex-start; } @media(--mobile){ padding: 28px; }', ['v2-card'])])


def step_cards(cid, steps):
    return div(cid, [
        div(cid + ' line', [div(cid + ' fill', [], 'width: 0; height: 100%; border-radius: 999px; background-color: #55E68B;')],
            'position: absolute; left: 32px; right: 32px; width: auto; top: 14px; height: 2px; border-radius: 999px; background-color: rgba(190,255,215,0.14); @media(--tablet){ display: none; }'),
        div(cid + ' grid', [div(f'{cid} {i}', [
            p(f'{cid} {i} n', f'0{i + 1}', None, MONO + 'font-size: 56px; line-height: 1; font-weight: 500; letter-spacing: -0.04em; color: rgba(163,255,193,0.18);'),
            itile(f'{cid} {i} icon', ic), h(f'{cid} {i} t', t, 'h3', ['v2-h3'], 'margin-top: 20px;'), p(f'{cid} {i} d', d, ['v2-body'], 'margin-top: 8px;')],
            'gap: 0;', ['v2-card', 'v2-step']) for i, (ic, t, d) in enumerate(steps)],
            f'display: grid; grid-template-columns: repeat({len(steps)}, minmax(0, 1fr)); gap: 16px; @media(--tablet){{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} @media(--mobile){{ grid-template-columns: minmax(0, 1fr); }}'),
    ], 'padding-top: 44px; @media(--tablet){ padding-top: 0; }', ['v2-proc'])


# ---------------- facts (client answers) ----------------
INCLUDED = ['Charger in your chosen finish', 'Up to 10m of supply cable', 'Wall mounting and standard drilling', 'Connection to your existing supply',
            'Dedicated EV consumer unit with surge protection', 'Electrical protection and earthing', 'PEN fault protection appropriate to your installation',
            'DNO application or notification', 'Testing and commissioning', 'Electrical installation certificate', 'App set-up and a demonstration',
            'English operating manual', 'Support after installation']
HOURS = 'Monday to Saturday, 8:30am to 6:30pm'


def page_installation():
    side = facts_panel('IN facts', [('Survey', 'Free and remote'), ('Turnaround', 'Most installs within 10 days of survey approval'), ('Coverage', 'Nationwide'), ('Hours', HOURS)])
    return [
        hero('IN hero', 'Installation', 'Professional installation, made simple.',
             'Every installation starts with a free remote survey. A qualified electrician then fits, tests and certifies your charger, and sets up the app with you.', side),
        v2sec('IN process', [v2head('IN p head', 'How it works', 'Four steps from request to first charge.', 'No home visit, no hassle.', center=True),
                             step_cards('IN steps', [('fa-solid fa-phone', 'Get in touch', 'Order online or request a callback. We’ll talk through your home, your car and the best spot for your charger.'),
                                                     ('fa-solid fa-mobile-screen', 'Free remote survey', 'Send photos or a short video, or talk us through it by phone. No home visit, no hassle.'),
                                                     ('fa-solid fa-file-invoice', 'Your quote and date', 'We confirm your installation, agree any extras with you, and book a time that suits you with our trusted installer.'),
                                                     ('fa-solid fa-truck-fast', 'Delivered and installed', 'Your EV-Tron is delivered to your installer ahead of the day. They fit, test and certify it, then show you how it works.')])]),
        v2sec('IN incl', [div('IN incl grid', [
            div('IN incl side', [chip('IN i chip', 'What’s included'), h('IN i t', 'A standard installation covers it all.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                                 p('IN i l', 'Anything non-standard is quoted and agreed with you before work starts.', ['v2-lead'], 'margin-top: 16px;')],
                'display: flex; flex-direction: column; align-items: flex-start;'),
            div('IN incl card', [div('IN incl cols', [ticks('IN a', INCLUDED[:7]), ticks('IN b', INCLUDED[7:])],
                                     'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 32px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }')],
                'padding: 36px; @media(--mobile){ padding: 22px; }', ['v2-card']),
        ], 'display: grid; grid-template-columns: minmax(0, 0.75fr) minmax(0, 1.25fr); gap: 48px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 24px; }')]),
        v2sec('IN suit', [
            v2head('IN s head', 'Is my home suitable?', 'Four things we check.', 'We confirm all of these during your free remote survey.'),
            div('IN s grid', [div(f'IS {i}', [itile(f'IS {i} icon', ic), h(f'IS {i} t', t, 'h3', ['v2-h3'], 'margin-top: 20px;'), p(f'IS {i} d', d, ['v2-body'], 'margin-top: 8px;')], classes=['v2-solid'])
                              for i, (ic, t, d) in enumerate([('fa-solid fa-car', 'Off-street parking', 'A driveway or private parking space where the charger and your car can sit side by side.'),
                                                             ('fa-solid fa-plug-circle-bolt', 'Electrical assessment', 'We check your supply, fuse board and earthing can support a 7kW charger safely.'),
                                                             ('fa-solid fa-file-signature', 'Permissions', 'If you rent or live in a flat, you may need permission from your landlord or freeholder.'),
                                                             ('fa-solid fa-location-dot', 'A suitable location', 'A wall or post position near your parking, within reach of the charging cable.')])],
                'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
            div('IN extras', [div(f'IX {i}', [p(f'IX {i} k', k, None, 'font-size: 15px; color: #DCE8E0;'), p(f'IX {i} v', v, None, MONO + 'font-size: 13.5px; color: #A3FFC1; text-align: right;')],
                                  'display: flex; justify-content: space-between; gap: 16px; padding: 16px 0; border-bottom: 1px solid rgba(190,255,215,0.10);')
                              for i, (k, v) in enumerate([('Supply cable beyond 10m', '£15 per metre'), ('Black charging post', '£200'), ('Steel charging post', '£280'),
                                                          ('Non-standard work', 'Quoted first'), ('Groundworks and excavation', 'Not offered')])],
                'margin-top: 24px; padding: 8px 28px; @media(--mobile){ padding: 8px 18px; }', ['v2-glass']),
        ]),
        v2sec('IN form', [div('IN form grid', [
            div('IN form copy', [chip('IN f chip', 'Request installation'), h('IN f t', 'Let’s get you charging at home.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                                 p('IN f l', 'Leave your details and our sales team will call to arrange your free remote survey and quote.', ['v2-lead'], 'margin-top: 16px;'),
                                 div('IN f ticks', [ticks('IN f t2', ['No payment until you approve your quote', HOURS, 'Prefer email? sales@evtron.co.uk'], '14.5px')], 'margin-top: 28px;')],
                'display: flex; flex-direction: column; align-items: flex-start;'),
            div('IN form card', [form('Install form', 'EV-Tron installation request', 'sales@evtron.co.uk', 'New installation request (Installation page)', [
                field('IF name', 'in-name', 'Full name'), field('IF phone', 'in-phone', 'Phone number', 'tel'),
                field('IF email', 'in-email', 'Email address', 'email'), field('IF postcode', 'in-postcode', 'Postcode'),
                select('IF finish', 'in-finish', 'Finish (if you know)', 'finish', ['Not sure yet', 'Mythos Black', 'Space Grey', 'Midnight Green', 'Crimson Red']),
                select('IF time', 'in-time', 'Best time to call', 'best-time', ['Any time', 'Morning (8:30 to 12:00)', 'Afternoon (12:00 to 17:00)', 'Early evening (17:00 to 18:30)']),
                textarea('IF notes', 'Anything we should know?', 'For example, where you’d like the charger and how far it is from your fuse box.')],
                'Request my callback', 'Thank you. A member of our sales team will call you to arrange your free remote survey.',
                'I agree to EV-Tron contacting me about this request. We’ll only use your details for this request.')],
                'padding: 32px; @media(--mobile){ padding: 20px; }', ['v2-card']),
        ], 'display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 48px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 28px; }')]),
    ]


FAQS = [
    ('The charger', [
        ('Will EV-Tron work with my car?', 'EV-Tron uses a Type 2 connector, which most electric and plug-in hybrid cars sold in the UK use. If you’re not sure, check your car’s charging port or handbook.'),
        ('How fast does it charge?', 'Up to 7kW on a single-phase home supply, at up to 32A. How many miles that adds per hour depends on your car.'),
        ('Can it be installed outdoors?', 'Yes. EV-Tron is IP65 rated against dust and water jets, and works from −20°C to +50°C.'),
        ('Which colours are available?', 'Four finishes, all the same price: Mythos Black, Space Grey, Midnight Green and Crimson Red.'),
        ('Which cable lengths can I choose?', 'The charging cable comes in 5 metres as standard. 7.5 metres is a free upgrade, and 10 metres is £80 extra.'),
        ('Does it work with solar panels?', 'Yes. EV-Tron is solar compatible, so you can use more of your own solar energy and lower your electricity bills. Our Fox ESS chargers are solar compatible too.')]),
    ('App and smart features', [
        ('Can I control it from my phone?', 'Yes. Over Wi-Fi or Bluetooth you can start and stop charging, set a schedule and see live data such as power, current and energy. We set it all up with you.'),
        ('Can I charge at off-peak times?', 'Yes. Set a charging schedule in the app to match your tariff’s cheaper hours.'),
        ('What is load balancing?', 'With the optional CT clamp (£15), the charger watches your home’s electricity use and adjusts charging so your supply isn’t overloaded.'),
        ('Can I start charging without my phone?', 'Yes. Use plug and charge, or tap the RFID card supplied with the charger.')]),
    ('Buying', [
        ('Can I buy the charger without installation?', 'Yes. Choose Charger only in the configurator and check out online. It will need to be installed by a qualified electrician.'),
        ('How do I get it installed by EV-Tron?', 'Choose Supply and install, or request installation on our Installation page. We’ll call you, run a free remote survey and send your quote.'),
        ('How can I pay?', 'Online by card, Apple Pay, Google Pay or PayPal. Pay-later options are planned, subject to approval.'),
        ('Is there a free gift?', 'Supply and install orders currently unlock a free handheld vacuum cleaner. Full offer terms will be published before launch.')]),
    ('Installation', [
        ('Do I need a home visit first?', 'No home visit and no hassle. We start with a free remote survey by phone, photos or video, and agree everything with you before installation.'),
        ('How soon can it be installed?', 'Most installations happen within 10 days of survey approval, and in some areas in as little as 48 to 96 hours, subject to availability.'),
        ('Where do you install?', 'Nationwide, through our network of trusted installers.'),
        ('Is my home suitable?', 'You’ll need off-street parking, a suitable location for the charger, an electrical supply that can support it, and any permissions needed if you rent or live in a flat. We don’t offer groundworks or excavation.'),
        ('Who installs the charger?', 'Qualified electricians from our installation network. Every installation is tested, certified and notified to your network operator.')]),
    ('Warranty and aftercare', [
        ('What warranty do I get?', 'Every EV-Tron comes with a 3-year warranty. Upgrade to 5 years for extra peace of mind, for only £89.99 when you order.'),
        ('Who do I contact if something goes wrong?', 'Us. EV-Tron is your single point of contact for installation, technical help and warranty. Email info@evtron.co.uk.'),
        ('Do I get a manual?', 'Yes. Every charger comes with an English user manual, and your installer will show you how to use the charger and the app.')]),
]


def page_faqs():
    groups = []
    for gi, (g, qa) in enumerate(FAQS):
        groups.append(div(f'FQ g{gi}', [
            div(f'FQ g{gi} side', [p(f'FQ g{gi} n', f'0{gi + 1}', None, MONO + 'font-size: 13px; color: #55E68B; letter-spacing: 0.08em;'),
                                   h(f'FQ g{gi} t', g, 'h2', ['v2-h3'], 'margin-top: 10px; font-size: clamp(22px, 2.2vw, 30px);')],
                'display: flex; flex-direction: column; align-items: flex-start; position: sticky; top: 140px; @media(--tablet){ position: relative; top: 0; }'),
            accordion(f'FQ acc{gi}', qa),
        ], 'display: grid; grid-template-columns: minmax(0, 0.55fr) minmax(0, 1.45fr); gap: 48px; align-items: start; padding-top: 48px; padding-bottom: 48px; '
           + ('' if gi == 0 else 'border-top: 1px solid rgba(190,255,215,0.10); ') + '@media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 18px; }'))
    return [
        hero('FQ hero', 'FAQs', 'Questions, answered.', 'Everything people ask us about EV-Tron, buying online, installation and aftercare.'),
        v2sec('FQ list', groups),
        cta_band('FQ cta', 'Still have a question?', 'Email us or send a message, and we’ll get back to you.', [('Contact us', '/contact/', 'primary'), ('Request installation', '/installation/#request', 'glass')]),
    ]


def page_contact():
    methods = [('fa-solid fa-cart-shopping', 'Buying and installation', 'sales@evtron.co.uk', 'Orders, quotes and installation requests.'),
               ('fa-solid fa-envelope', 'Everything else', 'info@evtron.co.uk', 'Questions, support, warranty and aftercare.'),
               ('fa-regular fa-clock', 'Opening hours', HOURS, 'We reply as soon as we can during these hours.'),
               ('fa-solid fa-location-dot', 'Coverage', 'Nationwide', 'Installations by our trusted installer network.')]
    return [
        hero('CT hero', 'Contact', 'Talk to EV-Tron.', 'Questions about the charger, your order or installation? Send us a message and we’ll get back to you.'),
        v2sec('CT main', [div('CT grid', [
            div('CT methods', [div(f'CM {i}', [itile(f'CM {i} icon', ic),
                                               div(f'CM {i} txt', [p(f'CM {i} k', k, ['v2-label']), p(f'CM {i} v', v, None, 'font-size: 17px; color: #F5FFF8; font-weight: 600; margin-top: 6px;'),
                                                                   p(f'CM {i} d', d, ['v2-body'], 'margin-top: 4px; font-size: 14.5px;')])],
                                   'display: flex; gap: 16px; align-items: flex-start; padding: 22px;', ['v2-solid']) for i, (ic, k, v, d) in enumerate(methods)],
                'display: flex; flex-direction: column; gap: 12px;'),
            div('CT form card', [h('CT f t', 'Send us a message', 'h2', ['v2-h3'], 'font-size: 24px; margin-bottom: 20px;'),
                                 form('Contact form', 'EV-Tron contact', 'info@evtron.co.uk', 'New message from the EV-Tron website', [
                                     field('CF name', 'ct-name', 'Full name'), field('CF email', 'ct-email', 'Email address', 'email'),
                                     field('CF phone', 'ct-phone', 'Phone number', 'tel', required=False),
                                     select('CF topic', 'ct-topic', 'What’s it about?', 'topic', ['Buying a charger', 'Installation', 'An existing order', 'Warranty or support', 'Something else']),
                                     textarea('CF msg', 'Your message', 'How can we help?', required=True)],
                                     'Send message', 'Thank you. Your message has been sent and we’ll get back to you soon.',
                                     'I agree to EV-Tron using my details to reply to this message.')],
                'padding: 32px; @media(--mobile){ padding: 20px; }', ['v2-card']),
        ], 'display: grid; grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr); gap: 24px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }')]),
        v2sec('CT links', [div('CT l grid', [div(f'CL {i}', [h(f'CL {i} t', t, 'h3', ['v2-h3']), p(f'CL {i} d', d, ['v2-body'], 'margin-top: 8px;'),
                                                              vbtn(f'CL {i} b', b, u, 'glass', 'margin-top: 20px;')], 'align-items: flex-start;', ['v2-card'])
                                             for i, (t, d, b, u) in enumerate([('FAQs', 'Quick answers about the charger, buying and installation.', 'Read FAQs', '/faqs/'),
                                                                               ('Installation', 'How our free remote survey and installation work.', 'How it works', '/installation/'),
                                                                               ('Warranty', 'What your warranty covers and how to get help.', 'Warranty', '/warranty/')])],
            'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }')]),
    ]


def page_warranty():
    cover = div('WA cover', [
        div('WA std', [p('WA s k', 'Standard', ['v2-label']), p('WA s n', '3 years', ['v2-num'], 'font-size: clamp(44px, 5vw, 72px); margin-top: 12px;'),
                       p('WA s d', 'Included with every EV-Tron charger.', ['v2-body'], 'margin-top: 10px;')], 'padding: 36px;', ['v2-solid']),
        div('WA ext', [p('WA e k', 'Extended', ['v2-label']), p('WA e n', '5 years', ['v2-num'], 'font-size: clamp(44px, 5vw, 72px); margin-top: 12px; color: #A3FFC1;'),
                       p('WA e d', 'Upgrade for extra peace of mind, for only £89.99 when you order.', ['v2-body'], 'margin-top: 10px;'),
                       vbtn('WA e b', 'Configure your charger', PRODUCT + '#configure', 'primary', 'margin-top: 24px;')], 'padding: 36px; align-items: flex-start;', ['v2-card']),
    ], 'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }')
    return [
        hero('WA hero', 'Warranty', 'Covered, with one number to call.', '3-year warranty included, handled directly by us. Upgrade to 5 years for extra peace of mind, for only £89.99.'),
        v2sec('WA cover sec', [v2head('WA c head', 'Your cover', 'Choose 3 or 5 years.', None), cover]),
        v2sec('WA claim', [v2head('WA cl head', 'Getting help', 'If something isn’t right.', 'We’re your single point of contact for technical help and warranty claims.', center=True),
                           step_cards('WA steps', [('fa-solid fa-envelope', 'Get in touch', 'Email info@evtron.co.uk with your order number and a short description.'),
                                                   ('fa-solid fa-camera', 'We diagnose it', 'Photos or a short video help us find the cause quickly, often remotely.'),
                                                   ('fa-solid fa-screwdriver-wrench', 'We put it right', 'Depending on what’s needed, we fix it remotely, repair it or replace it.')])]),
        v2sec('WA terms', [div('WA t card', [itile('WA t icon', 'fa-solid fa-file-lines'),
                                             div('WA t txt', [h('WA t t', 'Full warranty terms', 'h3', ['v2-h3']),
                                                              p('WA t d', 'Our full warranty terms, including what is and isn’t covered, are being finalised and will be published on this page before launch.', ['v2-body'], 'margin-top: 8px;')])],
                                   'display: flex; gap: 20px; align-items: flex-start; padding: 32px;', ['v2-glass'])]),
    ]


def page_grants():
    return [
        hero('GR hero', 'Grants', 'EV charger grants.', 'Government funding for home chargers is available to some households in the UK. Here’s where EV-Tron stands.'),
        v2sec('GR status', [div('GR card', [itile('GR icon', 'fa-solid fa-circle-info'),
                                            div('GR txt', [h('GR t', 'Not available through us yet', 'h2', ['v2-h3'], 'font-size: 26px;'),
                                                           p('GR p1', 'We don’t currently offer grant-funded installations. Once our charger and installer approvals are confirmed, we’ll explain here who could be eligible and how to apply.', ['v2-body'], 'margin-top: 10px; font-size: 16.5px;'),
                                                           p('GR p2', 'Until then, our prices are what you pay, with nothing to claim back.', ['v2-body'], 'margin-top: 10px; font-size: 16.5px;')])],
                                  'display: flex; gap: 20px; align-items: flex-start; padding: 36px; @media(--mobile){ flex-direction: column; padding: 24px; }', ['v2-glass'])]),
        cta_band('GR cta', 'Ready without a grant?', 'Buy EV-Tron online, or have it fitted after a free remote survey.', [('Buy now', PRODUCT + '#configure', 'primary'), ('Request installation', '/installation/#request', 'glass')]),
    ]


LEGAL = {'terms': 'Terms and conditions', 'privacy-policy': 'Privacy policy', 'cookie-policy': 'Cookie policy', 'cancellations-returns': 'Cancellations and returns'}


def page_legal(slug):
    title = LEGAL[slug]
    src = f'../docs/legal/{slug}.md'
    if os.path.exists(src):
        blocks, n = [], 0
        for raw in open(src).read().split('\n\n'):
            t = raw.strip()
            if not t: continue
            n += 1
            if t.startswith('#'):
                blocks.append(h(f'LG b{n}', t.lstrip('#').strip(), 'h2', ['v2-h3'], 'margin-top: 32px; font-size: 22px;'))
            elif all(l.strip().startswith('- ') for l in t.splitlines()):
                blocks.append(ticks(f'LG b{n}', [l.strip()[2:] for l in t.splitlines()], '16px'))
            else:
                blocks.append(p(f'LG b{n}', ' '.join(t.splitlines()), ['v2-body'], 'margin-top: 14px; font-size: 16.5px; line-height: 1.75;'))
        body = div('LG body', blocks, 'padding: 40px; max-width: 900px; @media(--mobile){ padding: 22px; }', ['v2-glass'])
    else:
        body = div('LG body', [itile('LG icon', 'fa-solid fa-file-lines'),
                               div('LG txt', [h('LG t', 'Being finalised', 'h2', ['v2-h3'], 'font-size: 24px;'),
                                              p('LG p', f'Our {title.lower()} will be published on this page before we start taking orders. If you have a question in the meantime, email info@evtron.co.uk.',
                                                ['v2-body'], 'margin-top: 10px; font-size: 16.5px;')])],
                   'display: flex; gap: 20px; align-items: flex-start; padding: 36px; max-width: 900px; @media(--mobile){ flex-direction: column; padding: 24px; }', ['v2-glass'])
    return [hero('LG hero', 'Legal', title + '.', 'EV-Tron · evtron.co.uk'), v2sec('LG sec', [body])]


PAGES = {'installation': ('Installation', page_installation), 'faqs': ('FAQs', page_faqs), 'contact': ('Contact', page_contact),
         'warranty': ('Warranty', page_warranty)}   # Grants page removed (client, 22 Nov 2026)
PAGES.update({s: (t, (lambda s=s: page_legal(s))) for s, t in LEGAL.items()})
META = {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_page_settings': {'hide_title': 'yes'},
        'site-sidebar-layout': 'no-sidebar', 'ast-site-content-layout': 'full-width-container', 'site-content-style': 'unboxed'}


def ensure(slug, title):
    pages = C.setdefault('pages', {})
    if slug not in pages:
        pages[slug] = wp.req('wp/v2/pages', 'POST', {'title': title, 'slug': slug, 'status': 'publish', 'template': 'elementor_header_footer'})['id']
    wp.req(f'wp/v2/pages/{pages[slug]}', 'POST', {'status': 'publish', 'template': 'elementor_header_footer', 'meta': META})
    json.dump(C, open('created.json', 'w'), indent=1)
    return pages[slug]


if __name__ == '__main__':
    for slug in (sys.argv[1:] or PAGES):
        title, fn = PAGES[slug]
        cfg.clear(); st.clear(); cl.clear()
        X = div(title, fn(), 'background-color: #07110E;', tag='main')
        pid = ensure(slug, title)
        r = wp.ability('elementor/build-composition', {'post_id': pid, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
        pub = wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': pid}), 'DELETE').get('status')
        print(slug, pid, r.get('success'), pub, [w for w in (r.get('warnings') or []) if 'not linked' not in w][:4])
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
