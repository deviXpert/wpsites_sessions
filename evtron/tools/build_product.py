"""EV-Tron Tethered single-product template (Theme Builder, type product) for WooCommerce product EV-Tron Tethered (V2 glass style).
Sections: hero buy box, configurator (colour, cable, warranty, accessories) + details form (sales callback),
features, specifications, installation, FAQs. Behaviour lives in design/custom-code/07-product.html.
Facts come from docs/client-answers.md, the client's 19 Nov feedback and the supplier manual (EMS3-70-C).
Run: EVTRON_WP_USER=<admin login> python3 build_product.py"""
import json
import urllib.parse

import wp
import build_v2 as B                      # reuse V2 helpers (vbtn, chip, v2head, v2sec, itile, icon)
from build_home import el, div, p, h, cfg, st, cl, MONO

C = json.load(open('created.json'))
M = json.load(open('media.json'))
cfg.clear(); st.clear(); cl.clear()
chip, v2head, v2sec, itile, icon = B.chip, B.v2head, B.v2sec, B.itile, B.icon


def vbtn(cid, text, url, kind='primary', style=None):
    """In-page anchors stay relative (#configure) so they work at any product URL."""
    return el('e-button', cid, {'text': text, 'link': {'destination': url if url.startswith('#') else B.SITE + url}}, style, ['v2-btn-' + kind])

PRICE = '£595'
COLOURS = [('render_evtron', 'Mythos Black', '#1B1D21'), ('render_evtron_grey', 'Space Grey', '#7A8088'),
           ('render_evtron_green', 'Midnight Green', '#1E4A3A'), ('render_evtron_red', 'Crimson Red', '#7A1A20')]
CLASSES = ['pp-hero', 'pp-stage', 'pp-swatches', 'pp-group', 'pp-opt', 'pp-summary', 'pp-lines', 'pp-total', 'pp-details', 'pp-unlock', 'pp-multi', 'pp-specs']

TICK = lambda cid: el('e-svg', cid, {'svg': {'value': 'fa-solid fa-check', 'library': 'fa-solid'}}, 'width: 14px; height: 14px; color: #55E68B;')


def ticks(cid, items, size='15px'):
    return div(cid, [div(f'{cid} {i}', [TICK(f'{cid} {i} t'), p(f'{cid} {i} p', t, None, f'font-size: {size}; color: #DCE8E0; line-height: 1.45;')],
                         'display: flex; gap: 10px; align-items: flex-start;') for i, t in enumerate(items)],
               'display: flex; flex-direction: column; gap: 12px;')


def stage(cid, width='100%'):
    imgs = [el('e-image', f'{cid} {i}', {'image': {'src': {'id': M[k]}, 'size': 'full'}},
               'display: block; width: 100%; height: auto;' + ('' if i == 0 else ' position: absolute; left: 0; top: 0;'))
            for i, (k, _, _) in enumerate(COLOURS)]
    return div(cid, imgs, f'position: relative; width: {width}; margin-left: auto; margin-right: auto;', ['pp-stage'])


def swatches(cid):
    return div(cid, [div(f'{cid} {i}', [], f'width: 34px; height: 34px; min-width: 34px; flex: 0 0 34px; border-radius: 999px; background-color: {c}; border: 2px solid rgba(255,255,255,0.22);')
                     for i, (_, _, c) in enumerate(COLOURS)], 'display: flex; gap: 12px; align-items: center;', ['pp-swatches'])


# ================= 1. Hero buy box =================
hero = div('PP hero', [div('PP hero inner', [div('PP hero grid', [
    div('PP visual', [stage('PP stage', '78%'),
                      div('PP visual note', [p('PP vn', 'Illustration · 7kW · Type 2 · tethered', None, MONO + 'font-size: 11.5px; letter-spacing: 0.06em; color: #A1B5A8;')],
                          'display: flex; justify-content: center; margin-top: 8px;')],
        'position: relative; padding: 32px; @media(--mobile){ padding: 16px; }', ['v2-glass']),
    div('PP buy', [
        p('PP crumbs', 'EV chargers  /  EV-Tron Tethered', None, MONO + 'font-size: 12px; letter-spacing: 0.06em; color: #A1B5A8;'),
        chip('PP chip', 'Our own design'),
        h('PP title', 'EV-Tron Tethered', 'h1', ['v2-h2'], 'margin-top: 18px; font-size: clamp(40px, 4.6vw, 68px);'),
        p('PP sub', '7kW smart home charger with a tethered Type 2 cable.', ['v2-lead'], 'margin-top: 12px;'),
        div('PP price row', [p('PP price', PRICE, ['v2-num'], 'font-size: 44px; line-height: 1;'),
                             p('PP price note', 'Charger price. Installation available, quoted after a free remote survey', None, 'font-size: 14px; color: #A1B5A8;')],
            'display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap; margin-top: 28px;'),
        div('PP colour', [p('PP colour k', 'Colour', ['v2-label']), p('PP colour name', 'Mythos Black', None, 'font-size: 15px; color: #F5FFF8; font-weight: 600;')],
            'display: flex; gap: 12px; align-items: baseline; margin-top: 28px;'),
        div('PP sw wrap', [swatches('PP swatches')], 'margin-top: 12px;'),
        div('PP points', [ticks('PP ticks', ['Up to 7kW, 32A single-phase charging', 'App control over Wi-Fi and Bluetooth', 'Tethered Type 2 cable, up to 10 metres', 'IP65 rated for outdoor installation'])], 'margin-top: 28px;'),
        div('PP ctas', [vbtn('PP buy btn', 'Configure and buy', '#configure'),
                        vbtn('PP specs btn', 'See specifications', '#specs', 'glass')],
            'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px;'),
        div('PP assure', [p(f'PP as {i}', t, None, MONO + 'font-size: 11.5px; letter-spacing: 0.04em; color: #A3FFC1;') for i, t in
                          enumerate(['Free remote survey', 'Qualified electricians', 'Installed within 10 days of survey approval'])],
            'display: flex; flex-wrap: wrap; gap: 8px 22px; margin-top: 28px; padding-top: 22px; border-top: 1px solid rgba(190,255,215,0.12);'),
    ], 'display: flex; flex-direction: column; align-items: flex-start;'),
], 'display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr); gap: 56px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; }')],
    classes=['ev-container'])], 'padding-top: 180px; padding-bottom: 96px; @media(--tablet){ padding-top: 190px; } @media(--mobile){ padding-top: 170px; padding-bottom: 64px; }', ['pp-hero'], tag='section')


# ================= 2. Configurator =================
def option(cid, title, price, note=None, badge=None, swatch=None):
    kids = []
    if swatch: kids.append(div(cid + ' sw', [], f'width: 28px; height: 28px; min-width: 28px; flex: 0 0 28px; border-radius: 999px; background-color: {swatch}; border: 2px solid rgba(255,255,255,0.22);'))
    body = [p(cid + ' t', title, None, 'font-size: 16px; font-weight: 600; color: #F5FFF8;')]
    if note: body.append(p(cid + ' n', note, None, 'font-size: 13px; color: #A1B5A8; margin-top: 4px;'))
    kids.append(div(cid + ' body', body, 'flex: 1 1 0; width: auto; min-width: 0;'))
    right = []
    if badge: right.append(p(cid + ' b', badge, None, MONO + 'font-size: 10.5px; letter-spacing: 0.08em; text-transform: uppercase; color: #06150C; background-color: #55E68B; padding: 4px 8px; border-radius: 999px; white-space: nowrap;'))
    right.append(p(cid + ' p', price, None, MONO + 'font-size: 14px; color: #A3FFC1; white-space: nowrap;'))
    kids.append(div(cid + ' right', right, 'display: flex; flex-direction: column; align-items: flex-end; gap: 6px; flex: 0 0 auto; width: auto;'))
    return div(cid, kids, 'display: flex; align-items: center; gap: 14px; padding: 18px 20px; border-radius: 16px; border: 1px solid rgba(190,255,215,0.14); background-color: rgba(255,255,255,0.025); cursor: pointer;', ['pp-opt'])


def group(cid, n, title, sub, options, cols=1, multi=False):
    return div(cid, [
        div(cid + ' head', [p(cid + ' n', n, None, MONO + 'font-size: 12px; color: #55E68B; letter-spacing: 0.08em;'),
                            h(cid + ' t', title, 'h3', ['v2-h3'], 'font-size: 22px;')], 'display: flex; align-items: baseline; gap: 12px;'),
        p(cid + ' sub', sub, ['v2-body'], 'margin-top: 6px; font-size: 14.5px;'),
        div(cid + ' opts', options, f'display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 10px; margin-top: 18px; @media(--mobile){{ grid-template-columns: minmax(0, 1fr); }}'),
    ], 'padding-top: 32px; padding-bottom: 32px; border-bottom: 1px solid rgba(190,255,215,0.10);', ['pp-group'] + (['pp-multi'] if multi else []))


groups = div('Cfg steps', [
    group('G colour', '01', 'Colour', 'All four finishes are the same price.', [option(f'O col {i}', n, 'Included', swatch=c) for i, (_, n, c) in enumerate(COLOURS)], cols=2),
    group('G cable', '02', 'Cable length', 'Measure from where the charger will go to your car’s charging port.',
          [option('O cab 0', '5 metres', 'Included', 'Standard length'),
           option('O cab 1', '7.5 metres', 'Free', 'Free upgrade, unlocked for you', 'Unlocked'),
           option('O cab 2', '10 metres', '+£80', 'For longer driveways')]),
    group('G warranty', '03', 'Warranty', 'Every EV-Tron comes with a 3-year warranty.',
          [option('O war 0', '3-year warranty', 'Included', 'Standard cover'),
           option('O war 1', '5-year warranty', '+£89.99', 'Extend your cover by 2 years')]),
    group('G acc', '04', 'Accessories', 'Optional. Choose one charging post at most.',
          [option('O acc 0', 'CT clamp', '+£15', 'Measures your home’s demand for load balancing'),
           option('O acc 1', 'Black charging post', '+£200', 'Free-standing post for drives without a wall'),
           option('O acc 2', 'Steel charging post', '+£280', 'Brushed steel free-standing post')], multi=True),
    group('G install', '05', 'Installation', 'Buy the charger on its own, or let us supply and fit it.',
          [option('O ins 0', 'Charger only', 'Buy online', 'Checkout now. Delivered to you for your own electrician to fit'),
           option('O ins 1', 'Supply and install', 'Quote', 'We call you, run a free remote survey and quote for fitting')], cols=2),
], 'display: flex; flex-direction: column;')

summary = div('Cfg summary', [
    p('Sum k', 'Your EV-Tron', ['v2-label']),
    stage('Sum stage', '62%'),
    div('Sum lines', [], 'display: flex; flex-direction: column; gap: 10px; margin-top: 8px;', ['pp-lines']),
    div('Sum total row', [p('Sum total k', 'Total', None, 'font-size: 15px; color: #A1B5A8;'), p('Sum total', PRICE, ['v2-num'], 'font-size: 34px;', )],
        'display: flex; justify-content: space-between; align-items: baseline; margin-top: 18px; padding-top: 18px; border-top: 1px solid rgba(190,255,215,0.14);'),
    vbtn('Sum continue', 'Add to basket', '#details', 'primary', 'width: 100%; justify-content: center; margin-top: 20px;'),
    p('Sum note', 'Secure checkout. Prefer it fitted? Choose Supply and install.', None, 'font-size: 12.5px; color: #A1B5A8; margin-top: 12px; text-align: center;'),
], 'position: sticky; top: 120px; padding: 28px; @media(--tablet){ position: relative; top: 0; }', ['v2-glass', 'pp-summary'])

configure = div('PP configure', [div('PP configure inner', [
    v2head('Cfg head', 'Build your order', 'Make it yours.', 'Pick a finish, choose your cable and extras, then buy online or ask us to fit it. Your total updates as you go.'),
    div('Cfg grid', [groups, summary],
        'display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); gap: 48px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 24px; }'),
], classes=['ev-container'])], classes=['v2-sec'], tag='section')


# ================= 3. Details (unlock + callback form) =================
def field(cid, label, ftype='text', required=True, placeholder='', readonly=False):
    return div(cid, [el('e-form-label', cid + ' l', {'text': label + (' *' if required else ''), 'input-id': 'pp-' + cid.split()[-1]}, 'font-size: 13px; color: #C9D6CE; font-weight: 500;'),
                     el('e-form-input', cid + ' i', {'type': ftype, 'required': required, 'placeholder': placeholder, 'readonly': readonly, '_cssid': 'pp-' + cid.split()[-1]},
                        'width: 100%; min-height: 50px; padding: 12px 16px; border-radius: 12px; border: 1px solid #6A7688; background-color: rgba(7,17,14,0.6); color: #F5FFF8; font-size: 15px;')],
               'display: flex; flex-direction: column; gap: 8px; width: 100%;')


form = el('e-form', 'Order form', {
    'form-name': 'EV-Tron installation request',
    'actions-after-submit': ['collect-submissions', 'email'],
    'email': {'to': ['sales@evtron.co.uk'], 'subject': 'New EV-Tron supply and install request', 'from-name': 'EV-Tron website', 'send-as': 'html'},
}, 'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }', None, [
    div('F selection', [el('e-form-label', 'F selection l', {'text': 'Your selection', 'input-id': 'pp-selection'}, 'font-size: 13px; color: #C9D6CE; font-weight: 500;'),
                        el('e-form-textarea', 'F selection t', {'rows': 3, 'readonly': True, 'resizable': False},
                           'width: 100%; padding: 12px 16px; border-radius: 12px; font-size: 13px; line-height: 1.6;')],
        'display: flex; flex-direction: column; gap: 8px; width: 100%; grid-column: 1 / -1;'),
    field('F name', 'Full name'), field('F phone', 'Phone number', 'tel'),
    field('F email', 'Email address', 'email'), field('F postcode', 'Postcode'),
    div('F time', [el('e-form-label', 'F time l', {'text': 'Best time to call', 'input-id': 'pp-time'}, 'font-size: 13px; color: #C9D6CE; font-weight: 500;'),
                   el('e-form-select', 'F time s', {'name': 'best-time', 'options': [{'key': t, 'value': t} for t in ['Any time', 'Morning (8:30 to 12:00)', 'Afternoon (12:00 to 17:00)', 'Early evening (17:00 to 18:30)']]},
                      'width: 100%; min-height: 50px; padding: 12px 16px; border-radius: 12px; border: 1px solid #6A7688; background-color: rgba(7,17,14,0.6); color: #F5FFF8; font-size: 15px;')],
        'display: flex; flex-direction: column; gap: 8px; width: 100%;'),
    div('F notes', [el('e-form-label', 'F notes l', {'text': 'Anything we should know?', 'input-id': 'pp-notes'}, 'font-size: 13px; color: #C9D6CE; font-weight: 500;'),
                    el('e-form-textarea', 'F notes t', {'rows': 3, 'placeholder': 'For example, where you’d like the charger and how far it is from your fuse box.'},
                       'width: 100%; padding: 12px 16px; border-radius: 12px; border: 1px solid #6A7688; background-color: rgba(7,17,14,0.6); color: #F5FFF8; font-size: 15px;')],
        'display: flex; flex-direction: column; gap: 8px; width: 100%; grid-column: 1 / -1;'),
    div('F consent', [el('e-form-checkbox', 'F consent c', {'name': 'consent', 'value': 'yes', 'required': True}, 'width: 20px; height: 20px; flex: 0 0 20px; margin-top: 2px; accent-color: #55E68B;'),
                      el('e-form-label', 'F consent l', {'text': 'I agree to EV-Tron contacting me about this order. We’ll only use your details for this request. *', 'input-id': 'pp-consent'}, 'font-size: 13.5px; color: #C9D6CE; line-height: 1.5;')],
        'display: flex; gap: 12px; align-items: flex-start; grid-column: 1 / -1;'),
    div('F submit row', [el('e-form-submit-button', 'F submit', {'text': 'Request my callback'}, 'min-height: 54px; padding: 0 32px; border-radius: 999px; border: 0; font-weight: 600; font-size: 16px; color: #06150C; background-color: #55E68B; cursor: pointer;', ['v2-btn-primary'])],
        'grid-column: 1 / -1;'),
    el('e-form-success-message', 'F success', None, 'grid-column: 1 / -1; padding: 18px; border-radius: 14px; background-color: rgba(85,230,139,0.12); color: #DFFBEA; font-size: 15px; text-align: left;', None,
       [p('F success p', 'Thank you. A member of our sales team will call you to confirm your order and book your free remote survey.', None, 'color: #DFFBEA;')]),
    el('e-form-error-message', 'F error', None, 'grid-column: 1 / -1; padding: 18px; border-radius: 14px; background-color: rgba(229,72,77,0.14); color: #FFD9DA; font-size: 15px; text-align: left;', None,
       [p('F error p', 'Sorry, something went wrong. Please try again, or email sales@evtron.co.uk.', None, 'color: #FFD9DA;')]),
])

details = div('PP details', [div('PP details inner', [
    div('Unlock', [
        div('Unlock tile', [icon('Unlock icon', 'fa-solid fa-gift', 26, '#06150C')], 'width: 64px; height: 64px; min-width: 64px; flex: 0 0 64px; border-radius: 18px; display: flex; align-items: center; justify-content: center; background-color: #55E68B;'),
        div('Unlock text', [p('Unlock k', 'Offer unlocked', ['v2-label']),
                            h('Unlock t', 'You’ve just unlocked a free handheld vacuum cleaner.', 'h3', ['v2-h3'], 'font-size: clamp(20px, 2vw, 26px); margin-top: 6px;'),
                            p('Unlock d', 'Added to your order at no cost. [PLACEHOLDER: offer terms and product photo]', ['v2-body'], 'margin-top: 6px; font-size: 14px;')]),
    ], 'display: flex; gap: 20px; align-items: center; padding: 24px 28px; @media(--mobile){ flex-direction: column; align-items: flex-start; }', ['v2-glass', 'pp-unlock']),
    div('Details grid', [
        div('Details copy', [chip('Det chip', 'Last step'),
                             h('Det title', 'Where should we call you?', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                             p('Det lead', 'Leave your details and our sales team will call to talk through your installation, arrange your free remote survey and confirm your quote.', ['v2-lead'], 'margin-top: 16px;'),
                             div('Det ticks', [ticks('Det t', ['No payment taken until you approve your quote', 'Monday to Saturday, 8:30am to 6:30pm', 'Prefer email? sales@evtron.co.uk'], '14.5px')], 'margin-top: 28px;')],
            'display: flex; flex-direction: column; align-items: flex-start;'),
        div('Details form', [form], 'padding: 32px; @media(--mobile){ padding: 20px; }', ['v2-card']),
    ], 'display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 48px; align-items: start; margin-top: 40px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 28px; }'),
], classes=['ev-container'])], 'padding-top: 24px; padding-bottom: 120px;', ['pp-details'], tag='section')


# ================= 4. Features =================
FEATS = [('fa-solid fa-wifi', 'App control', 'Start, stop and monitor charging from your phone over Wi-Fi or Bluetooth, using the WeGoodCharger app.'),
         ('fa-regular fa-clock', 'Scheduled charging', 'Set charging to run in your tariff’s cheaper off-peak hours.'),
         ('fa-solid fa-id-card', 'RFID card', 'Tap the supplied RFID card to start or stop a session.'),
         ('fa-solid fa-sliders', 'Adjustable current', 'Set the charging current to suit your car and your home’s supply.'),
         ('fa-solid fa-cloud-rain', 'IP65 rated', 'Sealed against dust and water jets, for indoor or outdoor installation.'),
         ('fa-solid fa-shield-halved', 'Built-in protection', 'Over- and under-voltage, over-current, 30mA leakage and over-temperature protection.')]
features = v2sec('PP features', [
    v2head('Feat head', 'Features', 'Smart where it matters.', 'Everything you need from a home charger, without the clutter.'),
    div('Feat grid', [div(f'PF {i}', [itile(f'PF {i} icon', ic), h(f'PF {i} t', t, 'h3', ['v2-h3'], 'margin-top: 20px;'), p(f'PF {i} d', d, ['v2-body'], 'margin-top: 8px;')], classes=['v2-solid'])
                      for i, (ic, t, d) in enumerate(FEATS)],
        'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
])

# ================= 5. Specifications =================
SPECS = [('Model', 'EMS3-70-C'), ('Rated power', '7kW'), ('Rated current', '32A, adjustable'), ('Supply', 'Single-phase'),
         ('Connector', 'Type 2, tethered'), ('Cable length', '5m, 7.5m or 10m'), ('Start methods', 'Plug and charge, RFID card, app'),
         ('Connectivity', 'Wi-Fi and Bluetooth'), ('Ingress protection', 'IP65'), ('Operating temperature', '−20°C to +50°C'),
         ('Unit size', '274 × 204 mm'), ('Leakage protection', '30mA'), ('Standards', 'EN 62196-2, EN 61851-1, EN 62752'),
         ('Finishes', 'Mythos Black, Space Grey, Midnight Green, Crimson Red'), ('Warranty', '3 years, extendable to 5')]
specs = v2sec('PP specs', [div('Spec grid', [
    div('Spec side', [chip('Spec chip', 'Specifications'), h('Spec title', 'The technical detail.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                      p('Spec lead', 'From the manufacturer’s data for model EMS3-70-C.', ['v2-lead'], 'margin-top: 16px;')],
        'display: flex; flex-direction: column; align-items: flex-start; position: sticky; top: 140px; @media(--tablet){ position: relative; top: 0; }'),
    div('Spec table', [div(f'SR {i}', [p(f'SR {i} k', k, None, 'font-size: 14.5px; color: #A1B5A8;'), p(f'SR {i} v', v, None, MONO + 'font-size: 14px; color: #F5FFF8; text-align: right;')],
                           'display: flex; justify-content: space-between; gap: 24px; padding: 16px 0; border-bottom: 1px solid rgba(190,255,215,0.10);')
                       for i, (k, v) in enumerate(SPECS)], 'padding: 12px 32px; @media(--mobile){ padding: 8px 20px; }', ['v2-glass', 'pp-specs']),
], 'display: grid; grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr); gap: 56px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 28px; }')])

# ================= 6. Installation =================
INCL = ['Wall mounting and standard drilling', 'Connection to your existing supply', 'Dedicated EV consumer unit with surge protection',
        'Electrical protection and earthing', 'PEN fault protection appropriate to your installation', 'DNO application or notification',
        'Testing and commissioning', 'Electrical installation certificate', 'App set-up and a demonstration', 'English operating manual', 'Support after installation']
install = v2sec('PP install', [
    v2head('Inst head', 'Installation', 'What a standard installation covers.', 'Fitted by qualified electricians after a free remote survey. Anything non-standard is quoted and agreed before work starts.', center=True),
    div('Inst grid', [
        div('Inst list', [div('Inst cols', [ticks('Inst a', INCL[:6]), ticks('Inst b', INCL[6:])],
                              'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 32px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }')],
            'padding: 36px; @media(--mobile){ padding: 22px; }', ['v2-card']),
        div('Inst extras', [p('Ext k', 'Good to know', ['v2-label']),
                            div('Ext rows', [div(f'ER {i}', [p(f'ER {i} k', k, None, 'font-size: 14.5px; color: #DCE8E0;'), p(f'ER {i} v', v, None, MONO + 'font-size: 13.5px; color: #A3FFC1; text-align: right;')],
                                                 'display: flex; justify-content: space-between; gap: 16px; padding: 14px 0; border-bottom: 1px solid rgba(190,255,215,0.10);')
                                             for i, (k, v) in enumerate([('Cable beyond 10m', '£15 per metre'), ('Non-standard work', 'Quoted first'), ('Groundworks', 'Not offered'), ('Coverage', 'England')])],
                                'margin-top: 8px;')],
            'padding: 28px; @media(--mobile){ padding: 22px; }', ['v2-solid']),
    ], 'display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 20px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }'),
])

# ================= 7. FAQs =================
FAQ = [('Will it work with my car?', 'EV-Tron uses a Type 2 connector, which most electric and plug-in hybrid cars sold in the UK use. If you’re not sure, check your car’s charging port or handbook.'),
       ('How fast does it charge?', 'Up to 7kW. How many miles that adds per hour depends on your car, but it’s typically several times faster than a 3-pin plug.'),
       ('Can I control it from my phone?', 'Yes. The charger connects over Wi-Fi or Bluetooth to the WeGoodCharger app, so you can start, stop, schedule and monitor charging. We set it up with you on the day.'),
       ('Do I need a home visit before installation?', 'No. We start with a free remote survey by phone, photos or video. Any extra work is agreed with you before installation.'),
       ('How soon can it be installed?', 'Most installations happen within 10 days of survey approval, and in some areas in as little as 48 to 96 hours, subject to availability.'),
       ('Does it work with solar panels?', 'EV-Tron isn’t designed to charge from solar panels. If you have solar, email sales@evtron.co.uk and we’ll talk you through your options.'),
       ('What warranty do I get?', 'Every EV-Tron comes with a 3-year warranty. You can extend it to 5 years for £89.99 when you order.')]
items = []
for i, (q, a) in enumerate(FAQ):
    items.append(el('e-accordion-item', f'PQ {i}', None, 'border-radius: 16px;', None, [
        el('e-accordion-item-header', f'PQ {i} header', None, 'padding: 22px 24px; gap: 20px; @media(--mobile){ padding: 18px 16px; }', None, [
            el('e-accordion-item-title', f'PQ {i} title', None, None, None, [p(f'PQ {i} q', q, None, 'color: #F5FFF8; font-weight: 600; font-size: 17px; line-height: 1.4;')]),
            el('e-accordion-item-icon', f'PQ {i} icon', None, 'width: 32px; height: 32px; min-width: 32px; flex: 0 0 32px; display: flex; align-items: center; justify-content: center; padding: 0; border: 1px solid rgba(190,255,215,0.24); border-radius: 999px; color: #A3FFC1;', None,
               [el('e-svg', f'PQ {i} plus', {'svg': {'value': 'fa-solid fa-plus', 'library': 'fa-solid'}}, 'width: 12px; height: 12px;')])]),
        el('e-accordion-item-content', f'PQ {i} content', None, 'padding: 0 24px 24px; @media(--mobile){ padding: 0 16px 20px; }', None,
           [p(f'PQ {i} a', a, ['v2-body'], 'max-width: 66ch;')])]))
faqs = v2sec('PP faqs', [div('PQ grid', [
    div('PQ side', [chip('PQ chip', 'FAQs'), h('PQ title', 'Good questions.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                    p('PQ lead', 'Still unsure? Email sales@evtron.co.uk and we’ll help.', ['v2-lead'], 'margin-top: 16px;')],
        'display: flex; flex-direction: column; align-items: flex-start;'),
    el('e-accordion', 'PQ list', {'default_state': 'first_expanded', 'max_expanded': 'one', 'show_icon': True, 'icon_rotation': 45, 'faq_schema': True}, 'display: flex; flex-direction: column; gap: 10px;', None, items),
], 'display: grid; grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr); gap: 56px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 28px; }')])

X = div('Product EV-Tron', [hero, configure, details, features, specs, install, faqs], 'background-color: #07110E;', tag='main')


def ensure_classes():
    have = json.dumps(wp.req('wp-abilities/v1/abilities/elementor/read-resource/run?input[uri]=elementor://global-classes'))
    ops = [{'action': 'create', 'label': c, 'css': 'position: relative;'} for c in CLASSES if f'"{c}"' not in have.replace('\\"', '"')]
    if ops: print('classes', [r['status'] for r in wp.ability('elementor/manage-classes', {'operations': ops})['results']])


def ensure_template():
    """Theme Builder single-product template, assigned to the EV-Tron WooCommerce product (see build_wc_products.py)."""
    tid, pid = C['tpl_product_evtron'], C['wc_evtron']
    r = wp.ability('elementor/manage-site-parts', {'operations': [{'action': 'update', 'post_id': tid, 'conditions': [f'include/singular/product/{pid}']}]})
    print('conditions', r['results'][0].get('conditions'))
    return tid


if __name__ == '__main__':
    ensure_classes()
    pid = ensure_template()
    r = wp.ability('elementor/build-composition', {'post_id': pid, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('build', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:8])
    print('publish', wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': pid}), 'DELETE').get('status'))
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
    print(wp.req(f"wc/v3/products/{C['wc_evtron']}")['permalink'])
