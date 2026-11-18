"""EV-Tron V3 "Simple" homepage (/home-v3/): product-first, few words, two clear actions (Buy now / Book a free survey).
Learns from Hypervolt's buying patterns (product first, colours, one price, short process, trust strip) without copying its design.
Run: EVTRON_WP_USER=<admin login> python3 build_v3.py"""
import json, urllib.parse, wp
from build_home import el, div, p, h, btn, img, section, head, icon, icon_tile, checklist, cfg, st, cl, MONO, SITE

C = json.load(open('created.json'))
M = json.load(open('media.json'))
cfg.clear(); st.clear(); cl.clear()


def gtile(cid, value):
    """Green icon tile for V3 cards."""
    return div(cid, [icon(cid + ' svg', value, 20, 'var(--ev-accent)')],
               'width: 48px; height: 48px; min-width: 48px; max-width: 48px; flex: 0 0 48px; display: flex; align-items: center; justify-content: center; border-radius: 12px; background-color: rgba(59,227,127,0.10); border: 1px solid rgba(59,227,127,0.30);')


BUY_EVT = '/ev-chargers/evtron-tethered-ev-charger/'
BOOK = '/get-a-quote/'

# ---------- 1. Hero: one product, one price, two actions ----------
SW = [('Mythos Black', '#1B1D21'), ('Space Grey', '#6E737A'), ('Midnight Green', '#1E4A3A'), ('Crimson Red', '#5A1418')]
swatches = div('Hero swatches', [div(f'Swatch {i}', [], f'width: 34px; min-width: 34px; max-width: 34px; height: 34px; flex: 0 0 34px; border-radius: 999px; background-color: {c}; border: 2px solid var(--ev-control);')
                                 for i, (_, c) in enumerate(SW)], 'display: flex; gap: 12px; justify-content: center;')
trust = [('fa-solid fa-screwdriver-wrench', 'Installation included'), ('fa-solid fa-mobile-screen', 'Free remote survey'),
         ('fa-solid fa-sterling-sign', 'Pay in full or in 3'), ('fa-solid fa-shield', '3-year warranty')]
strip = div('Trust strip', [div(f'Strip {i}', [icon(f'Strip {i} svg', ic, 16, 'var(--ev-accent)'), p(f'Strip {i} t', t, None, 'font-size: 14px; font-weight: 500; color: var(--ev-text);')],
                                'display: flex; align-items: center; gap: 10px; justify-content: center;') for i, (ic, t) in enumerate(trust)],
            'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; padding-top: 24px; padding-bottom: 24px; border-top: 1px solid var(--ev-divider); border-bottom: 1px solid var(--ev-divider); margin-top: 72px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); justify-items: start; margin-top: 48px; }')

hero = div('V3 hero', [div('V3 hero inner', [
    div('Hero head', [
        p('Hero eyebrow', 'Home EV charger · supplied and fitted', ['ev-label'], 'color: var(--ev-accent);'),
        h('Hero title', 'Meet EV-Tron.', 'h1', ['ev-h-display'], 'margin-top: 16px; text-align: center;'),
        p('Hero sub', 'Fast. Smart. Effortless. A 7kW smart charger, fitted for one clear price.', ['ev-lead'], 'margin-top: 16px; text-align: center; max-width: 40ch;'),
    ], 'display: flex; flex-direction: column; align-items: center;'),
    div('Hero product', [img('Hero image', M['render_evtron'], 'width: 100%; max-width: 320px; height: auto; margin-left: auto; margin-right: auto;')],
        'margin-top: 32px; display: flex; justify-content: center;'),
    div('Hero choose', [swatches, p('Swatch name', 'Mythos Black', None, MONO + 'font-size: 13px; color: var(--ev-muted); text-align: center; margin-top: 12px; letter-spacing: 0.06em; text-transform: uppercase;')],
        'margin-top: 8px;'),
    div('Hero buy', [
        div('Hero price', [p('Price v', '£1,295', ['ev-price'], 'text-align: center;'), p('Price n', 'fully installed · or pay in 3', ['ev-small'], 'text-align: center; margin-top: 8px;')]),
        div('Hero CTAs', [btn('Buy now', 'Buy now', BUY_EVT, 'primary', 'min-width: 200px;'), btn('Book survey', 'Book a free survey', BOOK, 'ghost', 'min-width: 200px;')],
            'display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 24px;'),
    ], 'margin-top: 32px;'),
    strip,
], 'display: flex; flex-direction: column; align-items: center; padding-top: 96px; padding-bottom: 72px; @media(--mobile){ padding-top: 48px; }', ['ev-container'])],
    'background-color: var(--ev-ink);', tag='section')

# ---------- 2. Choose your charger: three simple cards ----------
CARDS = [('EV-Tron Tethered', M['render_evtron'], '7kW · up to 32A · Type 2 · 7.5m cable. Wi-Fi and Bluetooth app. Four colours.', '£1,295', BUY_EVT, None),
         ('Fox Tethered', M['render_foxt'], '7.3kW · Type 2 tethered. Solar-compatible. Black, blue, purple or pink.', '£995', '/ev-chargers/fox-tethered-solar-ev-charger/', 'Solar-compatible'),
         ('Fox Untethered', M['render_foxu'], '7.3kW · Type 2 socket, use your own cable. Solar-compatible. White.', '£945', '/ev-chargers/fox-untethered-solar-ev-charger/', 'Lowest price')]
cards = [div(f'{n} card', [
    img(f'{n} img', mid, 'width: 100%; height: auto; aspect-ratio: 1 / 1; object-fit: contain; background-color: var(--ev-ink); border-radius: 8px;'),
    div(f'{n} title row', [h(f'{n} name', n, 'h3', ['ev-h3'])] + ([p(f'{n} tag', tag, ['ev-label'], 'color: var(--ev-accent); white-space: nowrap;')] if tag else []),
        'display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-top: 20px;'),
    p(f'{n} blurb', blurb, ['ev-body'], 'margin-top: 8px;'),
    p(f'{n} price', price, None, MONO + 'font-weight: 500; font-size: 26px; color: var(--ev-text); margin-top: 20px;'),
    p(f'{n} pn', 'fully installed', ['ev-small'], 'margin-top: 4px;'),
    div(f'{n} btns', [btn(f'{n} buy', 'Buy now', url, 'primary', 'flex: 1 1 0;'), btn(f'{n} more', 'Details', url, 'ghost', 'flex: 1 1 0;')],
        'display: flex; gap: 10px; margin-top: auto; padding-top: 24px;'),
], classes=['ev-card'], tag='article') for n, mid, blurb, price, url, tag in CARDS]
choose = section('V3 choose', [
    head('Choose head', 'Choose your charger', 'Every price includes a standard installation.'),
    div('V3 cards', cards, 'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
], ['ev-divider-top'])

# ---------- 3. How it works: three steps ----------
STEPS = [('fa-solid fa-cart-shopping', 'Buy online or book a survey', 'Order your charger, or book a free survey first if you’re not sure.'),
         ('fa-regular fa-camera', 'Free remote check', 'Share a few photos or a quick video call. No home visit needed.'),
         ('fa-solid fa-plug-circle-check', 'Installed and certified', 'Most standard installs within 10 days of survey approval, and as little as 48 to 96 hours in selected areas. Fitted, tested and certified.')]
steps = section('V3 steps', [
    head('Steps head', 'Three simple steps'),
    div('V3 step grid', [div(f'V3 step {i}', [gtile(f'V3 step {i} icon', ic), p(f'V3 step {i} n', f'Step {i+1}', ['ev-label'], 'margin-top: 20px;'),
                                              h(f'V3 step {i} t', t, 'h3', ['ev-h3'], 'margin-top: 6px;'), p(f'V3 step {i} d', d, ['ev-body'], 'margin-top: 8px;')], classes=['ev-card'])
                         for i, (ic, t, d) in enumerate(STEPS)],
        'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
], ['ev-divider-top'])

# ---------- 4. What's included (full package from the client) ----------
PKG = ['Your charger in your chosen colour', 'Up to 10 metres of supply cable', 'Wall mounting and standard drilling through external walls',
       'Connection to your existing electrical supply', 'Dedicated EV consumer unit with surge protection', 'Electrical protection and earthing arrangements',
       'Dynamic load balancing and CT clamp', 'PEN fault protection appropriate to your installation', 'DNO applications and notifications',
       'Testing, commissioning and electrical installation certificate', 'App set-up, demonstration and English operating manual', 'Post-installation customer support']
EXTRAS = [('Extra supply cable beyond 10m', '£15 per metre'), ('Black charging post', '£200'), ('Steel charging post', '£280'), ('Non-standard installations', 'Quoted first')]
SUIT = ['Suitable off-street parking', 'A suitable wall or post location', 'An electrical check (done remotely)', 'Any property permissions you need']
extras_rows = [div(f'Extra {i}', [p(f'Extra {i} k', k, ['ev-body']), p(f'Extra {i} v', v, None, MONO + 'font-size: 14px; color: var(--ev-text); white-space: nowrap;')],
                   'display: flex; justify-content: space-between; gap: 16px; padding-top: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--ev-divider);') for i, (k, v) in enumerate(EXTRAS)]
included = section('V3 included', [
    head('Inc head', 'What’s included in the price', 'A standard installation covers everything most homes need. Anything extra is agreed with you before work starts.'),
    div('Inc grid', [
        div('Inc list card', [p('Inc list label', 'Included as standard', ['ev-label'], 'color: var(--ev-accent); margin-bottom: 18px;'),
                              div('Inc cols', [checklist('Inc list A', PKG[:6], '✓'), checklist('Inc list B', PKG[6:], '✓')],
                                  'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 28px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }')],
            classes=['ev-card']),
        div('Inc side', [
            div('Extras card', [p('Extras label', 'Optional extras', ['ev-label'], 'margin-bottom: 6px;'), div('Extras rows', extras_rows),
                                p('Extras note', 'Groundworks and excavation aren’t offered.', ['ev-small'], 'margin-top: 14px;')], classes=['ev-card']),
            div('Suit card', [p('Suit label', 'Is my home suitable?', ['ev-label'], 'margin-bottom: 14px;'), checklist('Suit list', SUIT, '+'),
                              btn('Inc CTA', 'Book a free survey', BOOK, 'primary', 'margin-top: 22px;')], classes=['ev-card']),
        ], 'display: flex; flex-direction: column; gap: 20px;'),
    ], 'display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 20px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }'),
], ['ev-divider-top'])

# ---------- 4b. EV-Tron at a glance (specs from the client) ----------
SPECS = [('Power', '7kW single-phase'), ('Current', 'Up to 32A, adjustable'), ('Connector', 'Type 2, tethered'), ('Cable', '7.5m'),
         ('Weather', 'IP65, indoor or outdoor'), ('Connectivity', 'Wi-Fi and Bluetooth'), ('Access', 'RFID card or app'), ('Status', 'LED indicators'),
         ('Load balancing', 'Built in, CT clamp included'), ('Protection', 'Over/under-voltage, overcurrent, earth leakage, over-temperature')]
specs = section('V3 specs', [div('Spec grid wrap', [
    div('Spec copy', [h('Spec title', 'EV-Tron at a glance', 'h2', ['ev-h2']),
                      p('Spec lead', 'Smart scheduling, real-time charging information and the protection you’d expect, in four premium finishes.', ['ev-lead'], 'margin-top: 16px;'),
                      img('Spec image', M['render_evtron'], 'width: 100%; max-width: 260px; height: auto; margin-top: 32px; @media(--tablet){ display: none; }')],
        'display: flex; flex-direction: column; align-items: flex-start;'),
    div('Spec table', [div(f'Spec {i}', [p(f'Spec {i} k', k, ['ev-label']), p(f'Spec {i} v', v, None, 'font-size: 15.5px; color: var(--ev-text); font-weight: 500; text-align: right; max-width: 32ch;')],
                           'display: flex; justify-content: space-between; align-items: baseline; gap: 20px; padding-top: 16px; padding-bottom: 16px; border-bottom: 1px solid var(--ev-divider);')
                       for i, (k, v) in enumerate(SPECS)], 'border-top: 1px solid var(--ev-divider);'),
], 'display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 56px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; }')],
    ['ev-divider-top'])

# ---------- 4c. Warranty, payment and peace of mind ----------
PEACE = [('fa-solid fa-shield', 'Warranty', '3 years included. Extend to 5 years for £89.99.', 'Claims are handled directly by EV-Tron, with manufacturer support where needed.'),
         ('fa-regular fa-credit-card', 'Pay your way', 'Card, Apple Pay, Google Pay or PayPal.', 'Or spread the cost with Klarna or PayPal Pay in 3, subject to approval.'),
         ('fa-solid fa-rotate-left', 'Fair refunds', 'Full refund if your home isn’t suitable after our remote check.', 'As long as no chargeable work has been agreed. Non-standard work is always explained first.'),
         ('fa-solid fa-headset', 'One point of contact', 'Installation, technical help and aftercare, all through EV-Tron.', 'Monday to Saturday, 8:30am to 6:30pm · sales@evtron.co.uk')]
peace = section('V3 peace', [
    head('Peace head', 'Buy with confidence'),
    div('Peace grid', [div(f'Peace {i}', [gtile(f'Peace {i} icon', ic), h(f'Peace {i} t', t, 'h3', ['ev-h3'], 'margin-top: 18px;'), p(f'Peace {i} d', d, ['ev-body'], 'margin-top: 6px;'),
                                          p(f'Peace {i} more', more, ['ev-small'], 'margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--ev-divider); color: var(--ev-accent);')], classes=['ev-card'])
                       for i, (ic, t, d, more) in enumerate(PEACE)],
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
], ['ev-divider-top'])

# ---------- 5. Key features ----------
FEAT = [('fa-solid fa-wifi', 'Smart app', 'Wi-Fi and Bluetooth. Schedule cheaper off-peak charging.', 'See live voltage, current, power, temperature, time and energy added.'),
        ('fa-solid fa-gauge-high', 'Load balancing', 'Protects your home supply automatically.', 'A CT clamp reads your home’s demand and lowers charging when needed.'),
        ('fa-solid fa-shield-halved', 'Protected install', 'Surge and PEN fault protection as standard.', 'Plus over/under-voltage, overcurrent, earth leakage and temperature protection.'),
        ('fa-solid fa-cloud-rain', 'Weatherproof', 'IP65 rated for outdoor walls (EV-Tron).', 'Suitable indoors or outdoors, subject to a suitable location.')]
features = section('V3 features', [
    head('Feat head', 'Why EV-Tron'),
    div('Feat grid', [div(f'Feat {i}', [gtile(f'Feat {i} icon', ic), h(f'Feat {i} t', t, 'h3', ['ev-h3'], 'margin-top: 18px;'), p(f'Feat {i} d', d, ['ev-body'], 'margin-top: 6px;'),
                                        p(f'Feat {i} more', more, ['ev-small'], 'margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--ev-divider); color: var(--ev-accent);')], classes=['ev-card'])
                      for i, (ic, t, d, more) in enumerate(FEAT)],
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
], ['ev-divider-top'])

# ---------- 5b. About (client copy) ----------
about = section('V3 about', [div('About wrap', [
    p('About eyebrow', 'Driven by innovation', ['ev-label'], 'color: var(--ev-accent);'),
    h('About title', 'The future of electric driving starts at home.', 'h2', ['ev-h2'], 'margin-top: 16px; max-width: 22ch;'),
    p('About text', 'Our mission is to make home EV charging smarter, simpler and more accessible. We combine innovative technology, premium contemporary design and professional installation, with a network of qualified electricians covering England, and the rest of the UK to follow.', ['ev-lead'], 'margin-top: 18px; max-width: 62ch;'),
    div('About values', [p(f'Value {i}', v, None, MONO + 'font-size: 12px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ev-body); padding: 8px 14px; border: 1px solid var(--ev-control); border-radius: 999px;')
                         for i, v in enumerate(['Intelligent technology', 'Premium design', 'Transparent pricing', 'Fast installation', 'Professional workmanship', 'Exceptional aftercare'])],
        'display: flex; flex-wrap: wrap; gap: 10px; margin-top: 28px;'),
], 'display: flex; flex-direction: column; align-items: flex-start;')], ['ev-divider-top'])

# ---------- 6. FAQ (short, one open at a time) ----------
FAQ = [('Will it work with my car?', 'Yes, if your car uses Type 2, which most UK electric and plug-in hybrid cars do.'),
       ('How long does installation take?', 'Most standard installs happen within 10 days of your survey being approved, and in as little as 48 to 96 hours in selected areas.'),
       ('Do I need a home visit?', 'Usually not. We check your home remotely using photos or a video call.'),
       ('Can I pay in instalments?', 'Yes. Pay in full, or spread the cost with Klarna or PayPal Pay in 3, subject to status.'),
       ('Where do you install?', 'Across England, with the rest of the UK coming soon.'),
       ('What if my home isn’t suitable?', 'If our remote check shows your home isn’t suitable and no chargeable work has been agreed, you get a full refund.'),
       ('What warranty do I get?', '3 years as standard, or 5 years in total with the £89.99 extension. Warranty claims are handled directly by EV-Tron.'),
       ('Can I charge from solar panels?', 'The two Fox chargers are solar-compatible, depending on the model and your system. EV-Tron Tethered doesn’t support solar-surplus charging.'),
       ('Do you do groundworks?', 'No. We don’t offer groundworks or excavation, so the charger needs a suitable wall or post location near your parking.')]
items = []
for i, (q, a) in enumerate(FAQ):
    items.append(el('e-accordion-item', f'Q {i}', None, 'border-bottom: 1px solid var(--ev-divider); border-radius: var(--ev-r-md);', None, [
        el('e-accordion-item-header', f'Q {i} h', None, 'padding-top: 22px; padding-bottom: 22px; padding-left: 24px; padding-right: 24px; gap: 24px; @media(--mobile){ padding-left: 16px; padding-right: 16px; gap: 16px; }', None, [
            el('e-accordion-item-title', f'Q {i} t', None, None, None, [div(f'Q {i} row', [
                p(f'Q {i} n', f'{i+1:02d}', None, MONO + 'font-size: 13px; color: var(--ev-muted); width: 32px; flex-shrink: 0; padding-top: 3px;'),
                p(f'Q {i} q', q, None, 'color: var(--ev-text); font-weight: 600; font-size: 17px; line-height: 1.4; @media(--mobile){ font-size: 16px; }')],
                'display: flex; align-items: flex-start; gap: 16px;')]),
            el('e-accordion-item-icon', f'Q {i} i', None, 'width: 32px; height: 32px; min-width: 32px; max-width: 32px; flex: 0 0 32px; display: flex; align-items: center; justify-content: center; padding: 0; border: 1px solid var(--ev-control); border-radius: 999px; color: var(--ev-text);', None,
               [icon(f'Q {i} plus', 'fa-solid fa-plus', 12, 'var(--ev-text)')])]),
        el('e-accordion-item-content', f'Q {i} c', None, 'padding-top: 0; padding-bottom: 26px; padding-left: 72px; padding-right: 64px; @media(--mobile){ padding-left: 16px; padding-right: 16px; }', None,
           [p(f'Q {i} a', a, ['ev-body'], 'max-width: 62ch;')])]))
faq = section('V3 faq', [div('FAQ grid', [
    div('FAQ side', [p('FAQ eyebrow', 'FAQs', ['ev-label'], 'color: var(--ev-accent);'),
                     h('FAQ title', 'Quick answers', 'h2', ['ev-h2'], 'margin-top: 16px;'),
                     p('FAQ intro', 'Straight answers before you buy. Open one at a time.', ['ev-lead'], 'margin-top: 16px;'),
                     div('Help card', [p('Help title', 'Still have a question?', None, 'color: var(--ev-text); font-weight: 600; font-size: 17px;'),
                                       p('Help text', 'We’re here Monday to Saturday, 8:30am to 6:30pm. Email us any time.', ['ev-small'], 'margin-top: 8px;'),
                                       p('Help email', '<a href="mailto:sales@evtron.co.uk">sales@evtron.co.uk</a>', None, MONO + 'font-size: 14px; color: var(--ev-accent); margin-top: 16px;'),
                                       div('Help buttons', [btn('Help book', 'Book a free survey', BOOK, 'primary'), btn('Help faqs', 'All FAQs', '/faqs/', 'ghost')],
                                           'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px;')],
                         'margin-top: 40px; padding: 24px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md);')],
        'display: flex; flex-direction: column; position: sticky; top: 120px; @media(--tablet){ position: static; }'),
    el('e-accordion', 'V3 FAQ list', {'default_state': 'first_expanded', 'max_expanded': 'one', 'show_icon': True, 'icon_rotation': 45, 'faq_schema': True}, 'display: flex; flex-direction: column; gap: 8px;', None, items),
], 'display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 80px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 40px; }')],
    ['ev-divider-top'])

# ---------- 7. Final band ----------
final = section('V3 final', [div('Final panel', [
    h('Final title', 'Ready to charge at home?', 'h2', ['ev-h2'], 'text-align: center;'),
    p('Final text', 'Buy now, or book a free survey and we’ll confirm everything first.', ['ev-lead'], 'margin-top: 14px; text-align: center;'),
    p('Final meta', 'Covering England · Monday to Saturday, 8:30am to 6:30pm · sales@evtron.co.uk', None, MONO + 'font-size: 12px; letter-spacing: 0.04em; color: var(--ev-muted); margin-top: 28px; text-align: center;'),
    div('Final CTAs', [btn('Final buy', 'Buy now', '/ev-chargers/', 'primary', 'min-width: 200px;'), btn('Final book', 'Book a free survey', BOOK, 'ghost', 'min-width: 200px;')],
        'display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 28px;'),
], 'display: flex; flex-direction: column; align-items: center; padding: 64px 32px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); @media(--mobile){ padding: 40px 20px; }')],
    ['ev-divider-top'])

X = div('Home V3', [hero, choose, steps, included, specs, features, peace, about, faq, final], 'background-color: var(--ev-ink);', ['ev-plain'], tag='main')

if __name__ == '__main__':
    pid = C.get('home_v3')
    if not pid:
        pg = wp.req('wp/v2/pages', 'POST', {'title': 'Home V3 (simple)', 'slug': 'home-v3', 'status': 'publish',
                                            'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': '[]',
                                                     'ast-site-content-layout': 'full-width-container', 'site-content-style': 'unboxed', 'site-sidebar-layout': 'no-sidebar'}})
        pid = pg['id']; C['home_v3'] = pid; json.dump(C, open('created.json', 'w'), indent=1)
        print('created', pid, pg.get('link'))
        wp.ability('elementor/update-page-settings', {'post_id': pid, 'settings': {'template': 'elementor_header_footer', 'hide_title': 'yes'}})
    r = wp.ability('elementor/build-composition', {'post_id': pid, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('v3', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:6])
    print(wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': pid}), 'DELETE').get('status'))
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
