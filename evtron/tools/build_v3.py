"""EV-Tron V3 "Simple" homepage (/home-v3/): product-first, few words, two clear actions (Buy now / Book a free survey).
Learns from Hypervolt's buying patterns (product first, colours, one price, short process, trust strip) without copying its design.
Run: EVTRON_WP_USER=<admin login> python3 build_v3.py"""
import json, urllib.parse, wp
from build_home import el, div, p, h, btn, img, section, head, icon, icon_tile, checklist, cfg, st, cl, MONO, SITE

C = json.load(open('created.json'))
M = json.load(open('media.json'))
cfg.clear(); st.clear(); cl.clear()

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
CARDS = [('EV-Tron Tethered', M['render_evtron'], 'Our own design. Four colours, 7.5m cable, smart app.', '£1,295', BUY_EVT, None),
         ('Fox Tethered', M['render_foxt'], 'Solar-compatible. Cable attached. Four colours.', '£995', '/ev-chargers/fox-tethered-solar-ev-charger/', 'Solar-compatible'),
         ('Fox Untethered', M['render_foxu'], 'Solar-compatible socket. Use your own cable.', '£945', '/ev-chargers/fox-untethered-solar-ev-charger/', 'Lowest price')]
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
         ('fa-solid fa-plug-circle-check', 'Installed and certified', 'A qualified electrician fits, tests and certifies your charger.')]
steps = section('V3 steps', [
    head('Steps head', 'Three simple steps'),
    div('V3 step grid', [div(f'V3 step {i}', [icon_tile(f'V3 step {i} icon', ic), p(f'V3 step {i} n', f'Step {i+1}', ['ev-label'], 'margin-top: 20px;'),
                                              h(f'V3 step {i} t', t, 'h3', ['ev-h3'], 'margin-top: 6px;'), p(f'V3 step {i} d', d, ['ev-body'], 'margin-top: 8px;')], classes=['ev-card'])
                         for i, (ic, t, d) in enumerate(STEPS)],
        'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
], ['ev-divider-top'])

# ---------- 4. What's included ----------
included = section('V3 included', [div('Inc grid', [
    div('Inc copy', [h('Inc title', 'What’s included in the price', 'h2', ['ev-h2']),
                     p('Inc lead', 'A standard installation covers everything most homes need.', ['ev-lead'], 'margin-top: 16px;'),
                     p('Inc extras', 'Extras, only if needed: extra cable £15 per metre beyond 10m · charging post from £200. Always agreed before work starts.', ['ev-small'], 'margin-top: 24px; max-width: 46ch;'),
                     btn('Inc CTA', 'Book a free survey', BOOK, 'ghost', 'margin-top: 32px;')],
        'display: flex; flex-direction: column; align-items: flex-start;'),
    div('Inc list wrap', [checklist('Inc list', ['Your charger in your chosen colour', 'Up to 10 metres of supply cable', 'Dedicated EV consumer unit with surge protection',
                                                 'Dynamic load balancing and CT clamp', 'DNO notification and electrical certificate', 'Testing, app set-up and a demonstration'], '✓')],
        classes=['ev-card']),
], 'display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 56px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; }')],
    ['ev-divider-top'])

# ---------- 5. Key features ----------
FEAT = [('fa-solid fa-wifi', 'Smart app', 'Wi-Fi and Bluetooth. Schedule cheaper charging.'),
        ('fa-solid fa-gauge-high', 'Load balancing', 'Protects your home supply automatically.'),
        ('fa-solid fa-shield-halved', 'Protected install', 'Surge and PEN fault protection as standard.'),
        ('fa-solid fa-cloud-rain', 'Weatherproof', 'IP65 rated for outdoor walls (EV-Tron).')]
features = section('V3 features', [
    head('Feat head', 'Why EV-Tron'),
    div('Feat grid', [div(f'Feat {i}', [icon_tile(f'Feat {i} icon', ic), h(f'Feat {i} t', t, 'h3', ['ev-h3'], 'margin-top: 18px;'), p(f'Feat {i} d', d, ['ev-body'], 'margin-top: 6px;')])
                      for i, (ic, t, d) in enumerate(FEAT)],
        'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); gap: 28px; }'),
], ['ev-divider-top'])

# ---------- 6. FAQ (short, one open at a time) ----------
FAQ = [('Will it work with my car?', 'Yes, if your car uses Type 2, which most UK electric and plug-in hybrid cars do.'),
       ('How long does installation take?', 'Most standard installs happen within 10 days of your survey being approved, and in as little as 48 to 96 hours in selected areas.'),
       ('Do I need a home visit?', 'Usually not. We check your home remotely using photos or a video call.'),
       ('Can I pay in instalments?', 'Yes. Pay in full, or spread the cost with Klarna or PayPal Pay in 3, subject to status.'),
       ('Where do you install?', 'Across England, with the rest of the UK coming soon.')]
items = [el('e-accordion-item', f'Q {i}', None, 'border-bottom: 1px solid var(--ev-divider);', None, [
    el('e-accordion-item-header', f'Q {i} h', None, 'padding: 22px 0; gap: 16px;', None, [
        el('e-accordion-item-title', f'Q {i} t', None, None, None, [p(f'Q {i} q', q, None, 'color: var(--ev-text); font-weight: 600; font-size: 17px;')]),
        el('e-accordion-item-icon', f'Q {i} i', None, 'width: 20px; color: var(--ev-accent);', None, [icon(f'Q {i} plus', 'fa-solid fa-plus', 12, 'var(--ev-accent)')])]),
    el('e-accordion-item-content', f'Q {i} c', None, 'padding: 0 0 22px 0;', None, [p(f'Q {i} a', a, ['ev-body'], 'max-width: 64ch;')])]) for i, (q, a) in enumerate(FAQ)]
faq = section('V3 faq', [
    head('FAQ head', 'Quick answers'),
    el('e-accordion', 'V3 FAQ list', {'default_state': 'all_collapsed', 'max_expanded': 'one', 'show_icon': True, 'icon_rotation': 45, 'faq_schema': True}, 'border-top: 1px solid var(--ev-divider); max-width: 860px;', None, items),
], ['ev-divider-top'])

# ---------- 7. Final band ----------
final = section('V3 final', [div('Final panel', [
    h('Final title', 'Ready to charge at home?', 'h2', ['ev-h2'], 'text-align: center;'),
    p('Final text', 'Buy now, or book a free survey and we’ll confirm everything first.', ['ev-lead'], 'margin-top: 14px; text-align: center;'),
    div('Final CTAs', [btn('Final buy', 'Buy now', '/ev-chargers/', 'primary', 'min-width: 200px;'), btn('Final book', 'Book a free survey', BOOK, 'ghost', 'min-width: 200px;')],
        'display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 28px;'),
], 'display: flex; flex-direction: column; align-items: center; padding: 64px 32px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); @media(--mobile){ padding: 40px 20px; }')],
    ['ev-divider-top'])

X = div('Home V3', [hero, choose, steps, included, features, faq, final], 'background-color: var(--ev-ink);', ['ev-plain'], tag='main')

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
