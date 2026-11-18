"""Build the EVTRON homepage (Direction A "Spec Sheet") with native Elementor V4 elements.
Run: EVTRON_WP_USER=<admin login> python3 build_home.py   (rebuilds the page content in place)"""
import json, urllib.parse, wp

C = json.load(open('created.json'))
M = json.load(open('media.json'))
PID = C['home']
SITE = 'https://evtron.co.uk'

xml, cfg, st, cl = [], {}, {}, {}


def el(tag, cid, conf=None, style=None, classes=None, children=None):
    if conf: cfg[cid] = conf
    if style: st[cid] = style
    if classes: cl[cid] = classes
    inner = ''.join(children or [])
    return f'<{tag} configuration-id="{cid}">{inner}</{tag}>'


def div(cid, children, style=None, classes=None, tag='div'):
    return el('e-div-block', cid, {'tag': tag} if tag != 'div' else None, 'padding: 0; ' + (style or ''), classes, children)


def p(cid, text, classes=None, style=None):
    return el('e-paragraph', cid, {'paragraph': text, 'tag': 'p'}, 'margin: 0; ' + (style or ''), classes)


def h(cid, text, tag='h2', classes=None, style=None):
    return el('e-heading', cid, {'title': text, 'tag': tag}, 'margin: 0; ' + (style or ''), classes)


def btn(cid, text, url, kind='primary', style=None):
    return el('e-button', cid, {'text': text, 'link': {'destination': SITE + url}}, style, ['ev-btn-' + kind])


def img(cid, mid, style=None):
    return el('e-image', cid, {'image': {'src': {'id': mid}, 'size': 'large'}}, style)


# ---------- 1. Hero ----------
facts = [('7kW', 'Single-phase home charging'), ('Type 2', 'Fits most UK EVs and plug-in hybrids'), ('3', 'Chargers, one clear price each')]
fact_cells = [div(f'Fact {i+1}', [p(f'Fact {i+1} value', v, style='font-family: var(--ev-mono); font-weight: 500; font-size: 24px; line-height: 1.1; color: var(--ev-text);'),
                                  p(f'Fact {i+1} text', k, ['ev-small'], 'margin-top: 4px;')],
                  'background-color: var(--ev-ink); padding: 16px;') for i, (v, k) in enumerate(facts)]

lines = [('EVTRON Tethered · Mythos Black', '£1,295', False), ('Cable 7.5m', 'Included', True),
         ('Standard installation', 'Included', True), ('Load balancing CT clamp', 'Included', True)]
line_rows = [div(f'Line {i+1}', [p(f'Line {i+1} item', a, ['ev-body'], 'font-size: 14px;'),
                                 p(f'Line {i+1} value', b, style='font-family: var(--ev-mono); font-size: 14px; white-space: nowrap; color: ' + ('var(--ev-accent)' if inc else 'var(--ev-text)') + ';')],
                 'display: flex; justify-content: space-between; gap: 16px; padding-top: 10px; padding-bottom: 10px; border-bottom: 1px dashed var(--ev-divider);')
             for i, (a, b, inc) in enumerate(lines)]

hero = div('Hero', [div('Hero grid', [
    div('Hero copy', [
        p('Hero eyebrow', 'Home EV chargers · supplied and fitted', ['ev-label']),
        h('Hero title', 'Fast. Smart. Effortless.', 'h1', ['ev-h-display'], 'margin-top: 14px;'),
        p('Hero title line 2', 'One price, fully installed.', ['ev-h-display'], 'font-weight: 300; color: var(--ev-muted);'),
        p('Hero lead', 'Three carefully chosen home chargers. Pick one, see exactly what the price includes, and pay in full or spread the cost.', ['ev-lead'], 'margin-top: 24px;'),
        div('Hero buttons', [btn('Hero CTA', 'Compare the chargers', '/ev-chargers/'), btn('Hero CTA 2', "What's included", '/installation/', 'ghost')],
            'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px;'),
        div('Hero facts', fact_cells, 'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; margin-top: 40px; background-color: var(--ev-divider); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); overflow: hidden; @media(--mobile){ grid-template-columns: 1fr; }'),
    ], 'display: flex; flex-direction: column;'),
    div('Price receipt', [
        div('Receipt head', [p('Receipt title', 'Your installed price', style='color: var(--ev-text); font-weight: 600; font-size: 15px;'), p('Receipt live', 'Live', ['ev-label'])],
            'display: flex; justify-content: space-between; align-items: center; gap: 12px;'),
        div('Receipt controls', [], 'display: flex; flex-direction: column; gap: 14px; margin-top: 16px;'),
        div('Receipt lines', line_rows, 'display: flex; flex-direction: column; margin-top: 16px; border-top: 1px dashed var(--ev-control);'),
        div('Receipt total', [p('Total label', 'Total, fully installed', ['ev-body']), p('Total value', '£1,295', ['ev-price'])],
            'display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-top: 16px;'),
        p('Receipt note', 'Includes a standard installation [definition to be confirmed]. Prices are proposed and will be confirmed before launch.', ['ev-small'], 'margin-top: 10px; font-size: 12.5px;'),
        btn('Receipt CTA', 'View EVTRON Tethered', '/ev-chargers/evtron-tethered-ev-charger/', 'primary', 'width: 100%; margin-top: 18px;'),
        p('Receipt instalments', 'Pay in full, or spread the cost with Klarna or PayPal Pay in 3 (subject to approval).', ['ev-small'], 'margin-top: 12px; text-align: center; font-size: 12.5px;'),
    ], 'background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); padding: 24px;', tag='aside'),
], 'display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 56px; align-items: start; padding-top: 88px; padding-bottom: 96px; @media(--tablet){ grid-template-columns: 1fr; gap: 40px; padding-top: 56px; padding-bottom: 72px; }',
    ['ev-container'])], 'background-color: var(--ev-ink);', tag='section')

# ---------- 2. Chargers ----------
PRODUCTS = [
    ('evtron', 'EVTRON Tethered', '£1,295', M['placeholder-evtron-tethered'], '/ev-chargers/evtron-tethered-ev-charger/',
     ['TETHERED', '4 FINISHES'], [('Power', '7kW'), ('Connection', 'Tethered Type 2'), ('Cable', '7.5m'), ('Weather rating', 'IP65'), ('Solar surplus', 'No')],
     'Black · Red · Grey · Green'),
    ('foxt', 'Fox Tethered', '£995', M['placeholder-fox-tethered'], '/ev-chargers/fox-tethered-solar-ev-charger/',
     ['TETHERED', 'SOLAR-READY'], [('Power', '7.3kW'), ('Connection', 'Tethered Type 2'), ('Cable', '5m'), ('Weather rating', 'IP55 · IK08'), ('Solar surplus', 'Yes')],
     'Black · Blue · Purple · Pink'),
    ('foxu', 'Fox Untethered', '£945', M['placeholder-fox-untethered'], '/ev-chargers/fox-untethered-solar-ev-charger/',
     ['UNTETHERED', 'SOLAR-READY'], [('Power', '7.3kW'), ('Connection', 'Type 2 socket'), ('Cable', 'Use your own'), ('Weather rating', 'IP55 · IK08'), ('Solar surplus', 'Yes')],
     'White'),
]
cards = []
for key, name, price, mid, url, tags, specs, colours in PRODUCTS:
    spec_rows = [div(f'{name} spec {i+1}', [p(f'{name} spec {i+1} k', k, ['ev-label']), p(f'{name} spec {i+1} v', v, style='font-family: var(--ev-mono); font-size: 14px; color: ' + ('var(--ev-accent)' if v == 'Yes' else 'var(--ev-text)') + ';')],
                     'display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding-top: 9px; padding-bottom: 9px; border-bottom: 1px solid var(--ev-divider);')
                 for i, (k, v) in enumerate(specs)]
    cards.append(div(f'{name} card', [
        img(f'{name} image', mid, 'width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 8px;'),
        h(f'{name} name', name, 'h3', ['ev-h3'], 'margin-top: 18px;'),
        p(f'{name} tags', '  ·  '.join(tags), ['ev-label'], 'margin-top: 8px;' + (' color: var(--ev-accent);' if 'SOLAR-READY' in tags else '')),
        div(f'{name} specs', spec_rows, 'display: flex; flex-direction: column; margin-top: 16px; border-top: 1px solid var(--ev-divider);'),
        p(f'{name} colours', 'Finishes: ' + colours, ['ev-small'], 'margin-top: 12px;'),
        div(f'{name} foot', [p(f'{name} price', price, style='font-family: var(--ev-mono); font-weight: 500; font-size: 24px; color: var(--ev-text);'),
                             btn(f'{name} view', 'View charger', url, 'ghost')],
            'display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: auto; padding-top: 18px;'),
    ], 'display: flex; flex-direction: column; gap: 0; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); padding: 20px;', tag='article'))

chargers = div('Chargers', [div('Chargers inner', [
    div('Chargers head', [h('Chargers title', 'Three chargers. Every number on the table.', 'h2', ['ev-h2']),
                          p('Chargers intro', 'Each price includes a standard installation. Specifications show verified figures only; anything still being confirmed with the supplier stays off this page until it is.', ['ev-body'], 'max-width: 56ch;')],
        'display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: end; @media(--tablet){ grid-template-columns: 1fr; gap: 12px; }'),
    div('Charger cards', cards, 'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin-top: 36px; @media(--tablet){ grid-template-columns: 1fr; }'),
    p('Chargers note', 'Prices shown are proposed and will be confirmed before launch. Product images are placeholders.', ['ev-small'], 'margin-top: 16px;'),
], classes=['ev-container'])], classes=['ev-section'], tag='section')

# ---------- 3. What's included ----------
def checklist(cid, items, mark):
    rows = [div(f'{cid} {i+1}', [p(f'{cid} {i+1} mark', mark, style='font-family: var(--ev-mono); color: ' + ('var(--ev-accent)' if mark == '✓' else 'var(--ev-muted)') + '; width: 24px; flex-shrink: 0;'),
                                 p(f'{cid} {i+1} text', t, ['ev-body'])],
                'display: flex; gap: 10px; padding-top: 14px; padding-bottom: 14px; border-bottom: 1px solid var(--ev-divider);') for i, t in enumerate(items)]
    return div(cid, rows, 'display: flex; flex-direction: column; border-top: 1px solid var(--ev-divider);')

steps = [('01', 'Order online', 'Choose your charger, finish and cable, then pay in full or in instalments.'),
         ('02', 'Quick check', 'Send a few photos so we can confirm a standard installation.'),
         ('03', 'Installation day', 'Fitted, tested and certified by a qualified electrician.'),
         ('04', 'Charge off-peak', 'Schedule charging for your tariff’s cheaper hours.')]
step_cells = [div(f'Step {n}', [p(f'Step {n} number', n, style='font-family: var(--ev-mono); color: var(--ev-accent); font-size: 13px;'),
                                h(f'Step {n} title', t, 'h3', ['ev-h3'], 'margin-top: 10px;'),
                                p(f'Step {n} text', d, ['ev-body'], 'margin-top: 6px; font-size: 15px;')],
                  'background-color: var(--ev-ink); padding: 24px;') for n, t, d in steps]

included = div('Included', [div('Included inner', [
    div('Included head', [h('Included title', 'What “fully installed” means', 'h2', ['ev-h2']),
                          p('Included intro', 'Know before you pay. If your home needs more than a standard installation, we tell you the cost first and you decide.', ['ev-body'], 'max-width: 56ch;')],
        'display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: end; @media(--tablet){ grid-template-columns: 1fr; gap: 12px; }'),
    div('Included cols', [
        div('Included col', [p('Included label', 'Included in the price', ['ev-label'], 'margin-bottom: 12px;'),
                             checklist('Included list', ['Supply of your chosen charger', 'Wall mounting on an exterior wall [to be confirmed]', 'Cable run up to [X]m from your consumer unit [to be confirmed]',
                                                         'Protection fitted to UK wiring regulations (BS 7671)', 'Testing, certification and network operator notification [to be confirmed]', 'App set-up and a walkthrough'], '✓')]),
        div('Extra col', [p('Extra label', 'Might cost extra (always quoted first)', ['ev-label'], 'margin-bottom: 12px;'),
                          checklist('Extra list', ['Longer cable runs', 'Consumer unit upgrade', 'Groundworks or trenching', 'Charging post instead of a wall mount'], '+')]),
    ], 'display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 36px; @media(--mobile){ grid-template-columns: 1fr; }'),
    div('Steps', step_cells, 'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; margin-top: 40px; background-color: var(--ev-divider); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); overflow: hidden; @media(--tablet){ grid-template-columns: 1fr 1fr; } @media(--mobile){ grid-template-columns: 1fr; }'),
], classes=['ev-container'])], classes=['ev-section'], tag='section')

# ---------- 4. Cost to charge ----------
costs = div('Costs', [div('Costs inner', [
    div('Costs head', [h('Costs title', 'What a charge costs at home', 'h2', ['ev-h2']),
                       p('Costs intro', 'Use your own numbers. We don’t assume a tariff: check your bill for your off-peak rate.', ['ev-body'], 'max-width: 56ch;')],
        'display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: end; @media(--tablet){ grid-template-columns: 1fr; gap: 12px; }'),
    div('Calculator', [
        div('Calculator inputs', [p('Calc fallback', 'Example: a 60 kWh battery charged from 20% to 80% uses 36 kWh. At 8.5p per kWh that is about £3.06, and takes about 5 hours 9 minutes on a 7kW charger.', ['ev-body'])],
            'display: flex; flex-direction: column; gap: 18px;'),
        div('Calculator result', [p('Calc label', 'Estimated cost', ['ev-label']),
                                  p('Calc cost', '£3.06', style='font-family: var(--ev-mono); font-weight: 500; font-size: clamp(40px, 6vw, 56px); line-height: 1; color: var(--ev-text); margin-top: 10px;'),
                                  p('Calc time', 'About 5 h 9 min on a 7kW charger', ['ev-body'], 'margin-top: 10px;'),
                                  p('Calc note', 'Estimate only. Ignores charging losses (typically a few percent) and assumes the full 7kW is available. Example values, not a quote.', ['ev-small'], 'margin-top: 12px;')],
            'display: flex; flex-direction: column;'),
    ], 'display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 36px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); padding: 32px; @media(--tablet){ grid-template-columns: 1fr; padding: 24px; }'),
], classes=['ev-container'])], classes=['ev-section'], tag='section')

# ---------- 5. FAQs ----------
FAQ = [('Will it work with my car?', 'All three chargers use Type 2, which most battery-electric and plug-in hybrid cars sold in the UK use. If you’re unsure, check the charging port on your car or its handbook.'),
       ('Tethered or untethered: what’s the difference?', 'A tethered charger has the cable permanently attached, so you just plug in. An untethered charger has a socket, and you use your own Type 2 cable.'),
       ('Can I charge from my solar panels?', 'The two Fox chargers can use surplus solar power to charge your car. What you need for this depends on your inverter; we’ll confirm the requirements before you order.'),
       ('Am I eligible for a government grant?', 'The OZEV chargepoint grant (75% of the cost, up to £500) is for people who rent, or own and live in a flat, with private off-street parking. People who own a house aren’t eligible. The scheme runs until 31 March 2027 (source: gov.uk).'),
       ('Can I pay in instalments?', 'Yes, once our payment accounts are approved you’ll be able to pay in full, or spread the cost with Klarna or PayPal Pay in 3, subject to status.')]
items = []
for i, (q, a) in enumerate(FAQ):
    items.append(el('e-accordion-item', f'FAQ {i+1}', None, 'border-bottom: 1px solid var(--ev-divider);', None, [
        el('e-accordion-item-header', f'FAQ {i+1} header', None, 'padding: 20px 0; gap: 16px;', None, [
            el('e-accordion-item-title', f'FAQ {i+1} title', None, None, None, [p(f'FAQ {i+1} question', q, style='color: var(--ev-text); font-weight: 600; font-size: 17px;')]),
            el('e-accordion-item-icon', f'FAQ {i+1} icon', None, 'width: 24px; color: var(--ev-accent);')]),
        el('e-accordion-item-content', f'FAQ {i+1} content', None, 'padding: 0 0 20px 0;', None, [p(f'FAQ {i+1} answer', a, ['ev-body'], 'max-width: 68ch;')])]))
faqs = div('FAQs', [div('FAQs inner', [
    h('FAQs title', 'Questions people ask first', 'h2', ['ev-h2']),
    el('e-accordion', 'FAQ list', {'default_state': 'all_collapsed', 'max_expanded': 'multiple', 'show_icon': True, 'faq_schema': True}, 'margin-top: 28px; border-top: 1px solid var(--ev-divider);', None, items),
    btn('FAQs more', 'See all FAQs', '/faqs/', 'ghost', 'margin-top: 28px;'),
], 'display: flex; flex-direction: column; align-items: flex-start;', ['ev-container'])], classes=['ev-section'], tag='section')

# ---------- 6. Closing CTA ----------
closing = div('Closing', [div('Closing inner', [
    div('Closing copy', [h('Closing title', 'One price. Fitted. No surprises.', 'h2', ['ev-h2']),
                         p('Closing text', 'Compare the three chargers side by side and choose the one that suits your home.', ['ev-lead'], 'margin-top: 14px;')]),
    btn('Closing CTA', 'Compare the chargers', '/ev-chargers/'),
], 'display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 24px;', ['ev-container'])], classes=['ev-section'], tag='section')

X = div('Home', [hero, chargers, included, costs, faqs, closing], 'background-color: var(--ev-ink);', tag='main')

if __name__ == '__main__':
    r = wp.ability('elementor/build-composition', {'post_id': PID, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('success', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:8])
    if r.get('resolved_xml'):
        open('home_resolved.xml', 'w').write(r['resolved_xml'])
    print(wp.ability('elementor/update-page-settings', {'post_id': PID, 'settings': {'template': 'elementor_header_footer', 'hide_title': 'yes'}}).get('success'))
    print(wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': PID}), 'DELETE').get('status'))
