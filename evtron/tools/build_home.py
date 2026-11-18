"""Build the EVTRON homepage (Direction A "Spec Sheet") with native Elementor V4 elements.
Run: EVTRON_WP_USER=<admin login> python3 build_home.py   (rebuilds the page content in place)

Layout rules (professional rhythm):
- Sections: class ev-section (vertical padding clamp(80px, 9vw, 128px)); inner wrapper ev-container (max 1440px, 32/16px gutters).
- Section heading block: ev-section-head (max 720px, 56px below). Never set local padding on elements carrying these classes.
- 8px spacing scale for gaps inside components (8/12/16/24/32/48)."""
import json, urllib.parse, wp

C = json.load(open('created.json'))
M = json.load(open('media.json'))
PID = C['home']
SITE = 'https://evtron.co.uk'
cfg, st, cl = {}, {}, {}


def el(tag, cid, conf=None, style=None, classes=None, children=None):
    if conf: cfg[cid] = conf
    if style: st[cid] = style
    if classes: cl[cid] = classes
    return f'<{tag} configuration-id="{cid}">{"".join(children or [])}</{tag}>'


def div(cid, children, style='', classes=None, tag='div'):
    # Reset Elementor's default 10px div padding ONLY on plain layout wrappers (no class) so classes keep control.
    base = '' if classes else 'padding: 0; '
    return el('e-div-block', cid, {'tag': tag} if tag != 'div' else None, (base + style).strip() or None, classes, children)


def p(cid, text, classes=None, style=''):
    return el('e-paragraph', cid, {'paragraph': text, 'tag': 'p'}, 'margin: 0; ' + style, classes)


def h(cid, text, tag='h2', classes=None, style=''):
    return el('e-heading', cid, {'title': text, 'tag': tag}, 'margin: 0; ' + style, classes)


def btn(cid, text, url, kind='primary', style=None):
    return el('e-button', cid, {'text': text, 'link': {'destination': SITE + url}}, style, ['ev-btn-' + kind])


def img(cid, mid, style=None):
    return el('e-image', cid, {'image': {'src': {'id': mid}, 'size': 'large'}}, style)


def section(cid, children, extra=None):
    return div(cid, [div(cid + ' inner', children, classes=['ev-container'])], classes=['ev-section'] + (extra or []), tag='section')


def head(cid, title, intro=None):
    kids = [h(cid + ' title', title, 'h2', ['ev-h2'])]
    if intro: kids.append(p(cid + ' intro', intro, ['ev-lead']))
    return div(cid, kids, classes=['ev-section-head'])


MONO = 'font-family: var(--ev-mono); '

# ---------- 1. Hero ----------
line_rows = [div(f'Line {i+1}', [p(f'Line {i+1} item', a, ['ev-body'], 'font-size: 14px;'),
                                 p(f'Line {i+1} value', b, None, MONO + 'font-size: 14px; white-space: nowrap; color: ' + ('var(--ev-accent)' if inc else 'var(--ev-text)') + ';')],
                 'display: flex; justify-content: space-between; gap: 16px; padding-top: 12px; padding-bottom: 12px; border-bottom: 1px dashed var(--ev-divider);')
             for i, (a, b, inc) in enumerate([('EVTRON Tethered · Mythos Black', '£1,295', False), ('Cable 7.5m', 'Included', True),
                                               ('Standard installation', 'Included', True), ('Load balancing CT clamp', 'Included', True)])]

hero = div('Hero', [div('Hero grid', [
    div('Hero copy', [
        p('Hero eyebrow', 'Home EV chargers · supplied and fitted', ['ev-label']),
        h('Hero title', 'Fast. Smart. Effortless.', 'h1', ['ev-h-display'], 'margin-top: 24px;'),
        p('Hero title line 2', 'One price, fully installed.', ['ev-h-display'], 'font-weight: 300; color: var(--ev-muted);'),
        p('Hero lead', 'Three carefully chosen home chargers. See exactly what the price includes, then pay in full or spread the cost.', ['ev-lead'], 'margin-top: 32px; max-width: 46ch;'),
        div('Hero buttons', [btn('Hero CTA', 'Compare the chargers', '/ev-chargers/'), btn('Hero CTA 2', 'How installation works', '/installation/', 'ghost')],
            'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 40px;'),
        p('Hero facts', '7kW home charging  ·  Type 2  ·  Pay in full or in instalments', ['ev-label'], 'margin-top: 40px; letter-spacing: 0.06em;'),
    ], 'display: flex; flex-direction: column; justify-content: center;'),
    div('Price receipt', [
        div('Receipt head', [p('Receipt title', 'Your installed price', None, 'color: var(--ev-text); font-weight: 600; font-size: 16px;'), p('Receipt live', 'Live', ['ev-label'])],
            'display: flex; justify-content: space-between; align-items: center; gap: 12px;'),
        div('Receipt controls', [], 'display: flex; flex-direction: column; gap: 16px; margin-top: 20px;'),
        div('Receipt lines', line_rows, 'display: flex; flex-direction: column; margin-top: 20px; border-top: 1px dashed var(--ev-control);'),
        div('Receipt total', [p('Total label', 'Total, fully installed', ['ev-body']), p('Total value', '£1,295', ['ev-price'])],
            'display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-top: 20px;'),
        btn('Receipt CTA', 'View EVTRON Tethered', '/ev-chargers/evtron-tethered-ev-charger/', 'primary', 'width: 100%; margin-top: 24px;'),
        p('Receipt instalments', 'Pay in full, or spread the cost with Klarna or PayPal Pay in 3.', ['ev-small'], 'margin-top: 12px; text-align: center;'),
    ], 'background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); padding: 32px; @media(--mobile){ padding: 20px; }', tag='aside'),
], 'display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr); gap: 80px; align-items: center; padding-top: 104px; padding-bottom: 120px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 48px; padding-top: 64px; padding-bottom: 80px; }',
    ['ev-container'])], 'background-color: var(--ev-ink); border-bottom: 1px solid var(--ev-divider);', tag='section')

# ---------- 2. Chargers ----------
PRODUCTS = [
    ('EVTRON Tethered', '£1,295', M['placeholder-evtron-tethered'], '/ev-chargers/evtron-tethered-ev-charger/', '7kW  ·  Tethered Type 2  ·  7.5m cable',
     'Our own design in four finishes, with a long tethered cable.', None),
    ('Fox Tethered', '£995', M['placeholder-fox-tethered'], '/ev-chargers/fox-tethered-solar-ev-charger/', '7.3kW  ·  Tethered Type 2  ·  5m cable',
     'Charges from your solar panels’ surplus. Four colours.', 'Solar-ready'),
    ('Fox Untethered', '£945', M['placeholder-fox-untethered'], '/ev-chargers/fox-untethered-solar-ev-charger/', '7.3kW  ·  Type 2 socket  ·  Your own cable',
     'A tidy socket for your own cable. Solar-ready.', 'Solar-ready'),
]
cards = []
for name, price, mid, url, spec, blurb, tag in PRODUCTS:
    top = [img(f'{name} image', mid, 'width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 6px;')]
    meta = [h(f'{name} name', name, 'h3', ['ev-h3'])]
    if tag:
        meta.append(p(f'{name} tag', tag, ['ev-label'], 'color: var(--ev-accent);'))
    cards.append(div(f'{name} card', top + [
        div(f'{name} meta', meta, 'display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-top: 24px;'),
        p(f'{name} blurb', blurb, ['ev-body'], 'margin-top: 8px;'),
        p(f'{name} spec', spec, None, MONO + 'font-size: 13px; color: var(--ev-muted); margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--ev-divider);'),
        div(f'{name} foot', [p(f'{name} price', price, None, MONO + 'font-weight: 500; font-size: 24px; color: var(--ev-text);'),
                             btn(f'{name} view', 'View charger', url, 'ghost')],
            'display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: auto; padding-top: 24px;'),
    ], classes=['ev-card'], tag='article'))

chargers = section('Chargers', [
    head('Chargers head', 'Three chargers. One clear price each.', 'Every price includes a standard installation. Compare them side by side, or let the receipt above do the maths.'),
    div('Charger cards', cards, 'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); gap: 16px; }'),
])

# ---------- 3. How it works ----------
steps = [('01', 'Order online', 'Choose your charger, finish and cable. Pay in full or in instalments.'),
         ('02', 'Quick home check', 'Send a few photos so we can confirm a standard installation.'),
         ('03', 'Installation day', 'Fitted, tested and certified by a qualified electrician.'),
         ('04', 'Charge off-peak', 'Schedule charging for your tariff’s cheaper hours.')]
step_cells = [div(f'Step {n}', [p(f'Step {n} number', n, None, MONO + 'color: var(--ev-accent); font-size: 13px;'),
                                h(f'Step {n} title', t, 'h3', ['ev-h3'], 'margin-top: 24px;'),
                                p(f'Step {n} text', d, ['ev-body'], 'margin-top: 8px;')],
                  'padding-top: 24px; border-top: 1px solid var(--ev-control);') for n, t, d in steps]

def checklist(cid, items, mark):
    rows = [div(f'{cid} {i+1}', [p(f'{cid} {i+1} mark', mark, None, MONO + 'color: ' + ('var(--ev-accent)' if mark == '✓' else 'var(--ev-muted)') + '; width: 20px; flex-shrink: 0;'),
                                 p(f'{cid} {i+1} text', t, ['ev-body'])], 'display: flex; gap: 12px;') for i, t in enumerate(items)]
    return div(cid, rows, 'display: flex; flex-direction: column; gap: 14px;')

how = section('How', [
    head('How head', 'How it works', 'From order to first charge in four steps. If your home needs more than a standard installation, we tell you the cost first and you decide.'),
    div('Steps', step_cells, 'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 40px 32px; } @media(--mobile){ grid-template-columns: minmax(0, 1fr); gap: 32px; }'),
    div('Price includes', [
        div('Included col', [p('Included label', 'Included in the price', ['ev-label']),
                             checklist('Included list', ['Your chosen charger, supplied and fitted', 'Safety protection to UK wiring regulations', 'Testing and certification', 'App set-up and a walkthrough'], '✓')],
            'display: flex; flex-direction: column; gap: 20px;'),
        div('Extra col', [p('Extra label', 'May cost extra (always quoted first)', ['ev-label']),
                          checklist('Extra list', ['Longer cable runs', 'Consumer unit upgrade', 'Groundworks or trenching', 'A charging post instead of a wall mount'], '+')],
            'display: flex; flex-direction: column; gap: 20px;'),
    ], 'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 48px; margin-top: 80px; padding: 40px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); @media(--mobile){ grid-template-columns: minmax(0, 1fr); gap: 32px; padding: 24px; margin-top: 56px; }'),
], ['ev-divider-top'])

# ---------- 4. Cost to charge ----------
costs = section('Costs', [
    head('Costs head', 'What a charge costs at home', 'Use your own numbers. We don’t assume a tariff: check your bill for your off-peak rate.'),
    div('Calculator', [
        div('Calculator inputs', [p('Calc fallback', 'Example: a 60 kWh battery charged from 20% to 80% uses 36 kWh. At 8.5p per kWh that is about £3.06, and takes about 5 hours 9 minutes on a 7kW charger.', ['ev-body'])],
            'display: flex; flex-direction: column; gap: 24px;'),
        div('Calculator result', [p('Calc label', 'Estimated cost', ['ev-label']),
                                  p('Calc cost', '£3.06', None, MONO + 'font-weight: 500; font-size: clamp(44px, 6vw, 64px); line-height: 1; color: var(--ev-text); margin-top: 16px;'),
                                  p('Calc time', 'About 5 h 9 min on a 7kW charger', ['ev-body'], 'margin-top: 12px;'),
                                  p('Calc note', 'Estimate only. Ignores charging losses and assumes the full 7kW is available.', ['ev-small'], 'margin-top: 24px;')],
            'display: flex; flex-direction: column; justify-content: center; padding-left: 48px; border-left: 1px solid var(--ev-divider); @media(--tablet){ padding-left: 0; border-left: 0; padding-top: 32px; border-top: 1px solid var(--ev-divider); }'),
    ], 'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 48px; padding: 40px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; } @media(--mobile){ padding: 24px; }'),
], ['ev-divider-top'])

# ---------- 5. FAQs (two columns) ----------
FAQ = [('Will it work with my car?', 'All three chargers use Type 2, which most battery-electric and plug-in hybrid cars sold in the UK use. If you’re unsure, check the charging port on your car or its handbook.'),
       ('Tethered or untethered: what’s the difference?', 'A tethered charger has the cable permanently attached, so you just plug in. An untethered charger has a socket, and you use your own Type 2 cable.'),
       ('Can I charge from my solar panels?', 'The two Fox chargers can use surplus solar power to charge your car. What you need depends on your inverter, and we’ll confirm it before you order.'),
       ('Am I eligible for a government grant?', 'The OZEV chargepoint grant (75% of the cost, up to £500) is for people who rent, or own and live in a flat, with private off-street parking. People who own a house aren’t eligible. The scheme runs until 31 March 2027 (source: gov.uk).'),
       ('Can I pay in instalments?', 'Yes. You can pay in full, or spread the cost with Klarna or PayPal Pay in 3, subject to status.')]
items = []
for i, (q, a) in enumerate(FAQ):
    items.append(el('e-accordion-item', f'FAQ {i+1}', None, 'border-bottom: 1px solid var(--ev-divider);', None, [
        el('e-accordion-item-header', f'FAQ {i+1} header', None, 'padding-top: 24px; padding-bottom: 24px; padding-left: 0; padding-right: 0; gap: 24px;', None, [
            el('e-accordion-item-title', f'FAQ {i+1} title', None, None, None, [p(f'FAQ {i+1} question', q, None, 'color: var(--ev-text); font-weight: 600; font-size: 18px; line-height: 1.4;')]),
            el('e-accordion-item-icon', f'FAQ {i+1} icon', None, 'width: 24px; color: var(--ev-accent);')]),
        el('e-accordion-item-content', f'FAQ {i+1} content', None, 'padding-top: 0; padding-bottom: 24px; padding-left: 0; padding-right: 40px;', None, [p(f'FAQ {i+1} answer', a, ['ev-body'], 'max-width: 64ch;')])]))
faqs = section('FAQs', [div('FAQ grid', [
    div('FAQ side', [h('FAQs title', 'Questions people ask first', 'h2', ['ev-h2']),
                     p('FAQs intro', 'Straight answers before you choose. More detail on the full FAQs page.', ['ev-lead'], 'margin-top: 16px;'),
                     btn('FAQs more', 'See all FAQs', '/faqs/', 'ghost', 'margin-top: 32px;')],
        'display: flex; flex-direction: column; align-items: flex-start;'),
    el('e-accordion', 'FAQ list', {'default_state': 'all_collapsed', 'max_expanded': 'multiple', 'show_icon': True, 'faq_schema': True}, 'border-top: 1px solid var(--ev-divider);', None, items),
], 'display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 80px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 40px; }')],
    ['ev-divider-top'])

# ---------- 6. Closing CTA ----------
closing = section('Closing', [div('Closing panel', [
    div('Closing copy', [h('Closing title', 'One price. Fitted. No surprises.', 'h2', ['ev-h2']),
                         p('Closing text', 'Compare the three chargers side by side and choose the one that suits your home.', ['ev-lead'], 'margin-top: 16px;')],
        'max-width: 640px;'),
    btn('Closing CTA', 'Compare the chargers', '/ev-chargers/'),
], 'display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 32px; padding: 56px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); @media(--mobile){ padding: 32px 24px; }')],
    ['ev-divider-top'])

X = div('Home', [hero, chargers, how, costs, faqs, closing], 'background-color: var(--ev-ink);', tag='main')

if __name__ == '__main__':
    r = wp.ability('elementor/build-composition', {'post_id': PID, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('success', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:8])
    if r.get('resolved_xml'):
        open('home_resolved.xml', 'w').write(r['resolved_xml'])
    print(wp.ability('elementor/update-page-settings', {'post_id': PID, 'settings': {'template': 'elementor_header_footer', 'hide_title': 'yes'}}).get('success'))
    print(wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': PID}), 'DELETE').get('status'))
