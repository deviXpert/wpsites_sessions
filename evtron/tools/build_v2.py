"""EV-Tron V2 (emerald glassmorphism) homepage: /home-v2/.
Stage 1 = new hero only; the remaining sections are V1's, appended unchanged until each is redesigned.
Run: EVTRON_WP_USER=<admin login> python3 build_v2.py"""
import json, urllib.parse, wp
from build_home import el, div, p, h, cfg, st, cl, MONO, SITE

C = json.load(open('created.json'))
M = json.load(open('media.json'))
PID = C['home_v2']
cfg.clear(); st.clear(); cl.clear()
PRICE = '£595'                                   # client 19 Nov: charger price shown is £595
PRODUCT = '/ev-chargers/evtron-tethered-ev-charger/'
HERO_COLOURS = [('render_evtron', 'Mythos Black', '#1B1D21'), ('render_evtron_grey', 'Space Grey', '#7A8088'), ('render_evtron_green', 'Midnight Green', '#1E4A3A')]


def vbtn(cid, text, url, kind='primary', style=None):
    return el('e-button', cid, {'text': text, 'link': {'destination': SITE + url}}, style, ['v2-btn-' + kind])


def chip(cid, text, style=''):
    return p(cid, text, ['v2-chip'], style)


# ---------- Floating information panels around the product ----------
float_status = div('Float status', [
    p('Status label', 'Live status', ['v2-label']),
    div('Status row', [div('Status led', [], 'width: 10px; min-width: 10px; max-width: 10px; height: 10px; border-radius: 999px; background-color: #55E68B; flex: 0 0 10px;'),
                       p('Status text', 'Charging · 7kW', None, MONO + 'font-size: 15px; color: #F5FFF8;')],
        'display: flex; align-items: center; gap: 10px; margin-top: 8px;'),
    div('Status track', [div('Status fill', [], 'width: 64%; height: 100%; border-radius: 999px; background-color: #55E68B;')],
        'width: 180px; max-width: 180px; height: 4px; margin-top: 12px; border-radius: 999px; background-color: rgba(255,255,255,0.10); overflow: hidden;'),
], 'width: max-content; left: 0; top: 10%; @media(--mobile){ top: 2%; left: 0; }', ['v2-float'])

float_price = div('Float price', [
    p('Price label', 'EV-Tron charger', ['v2-label']),
    p('Price value', PRICE, None, MONO + 'font-weight: 500; font-size: 34px; line-height: 1; color: #F5FFF8; margin-top: 8px;'),
    p('Price note', 'Choose cable and extras next', None, 'font-size: 13px; color: #A1B5A8; margin-top: 6px;'),
], 'width: max-content; right: 0; top: 44%; @media(--mobile){ top: auto; bottom: 14%; right: 0; }', ['v2-float'])

float_sched = div('Float schedule', [
    p('Sched label', 'Smart scheduling', ['v2-label']),
    p('Sched text', 'Avoids peak hours by default', None, 'font-size: 14px; color: #F5FFF8; margin-top: 8px; font-weight: 600;'),
    div('Sched bars', [div(f'Bar {i}', [], f'width: 8px; min-width: 8px; max-width: 8px; flex: 0 0 8px; height: {hgt}px; border-radius: 3px; background-color: {"#55E68B" if g else "rgba(255,255,255,0.14)"};')
                       for i, (hgt, g) in enumerate([(14, 1), (22, 1), (10, 0), (8, 0), (18, 1), (26, 1), (12, 0), (20, 1)])],
        'display: flex; align-items: flex-end; gap: 5px; margin-top: 12px; height: 26px;'),
], 'width: max-content; left: 0; top: 58%; @media(--mobile){ display: none; }', ['v2-float'])

visual = div('Hero visual', [
    div('Visual halo', [], 'position: absolute; left: 50%; top: 50%; width: 78%; aspect-ratio: 1; transform: translate(-50%, -50%); border-radius: 999px; border: 1px solid rgba(190,255,215,0.10);'),
    div('Hero stack', [el('e-image', f'Hero product {i}', {'image': {'src': {'id': M[k]}, 'size': 'full'}},
                          'display: block; width: 100%; height: auto;' + ('' if i == 0 else ' position: absolute; left: 0; top: 0;'))
                       for i, (k, n, _) in enumerate(HERO_COLOURS)], classes=['v2-stack']),
    div('Hero swatches', [div(f'Hero sw {i}', [div(f'Hero sw dot {i}', [], f'width: 12px; min-width: 12px; height: 12px; border-radius: 999px; background-color: {c}; border: 1px solid rgba(255,255,255,0.35);'),
                                               p(f'Hero sw name {i}', n, None, 'font-size: 12.5px; color: #C9D6CE; white-space: nowrap;')],
                              'display: flex; align-items: center; gap: 8px; width: auto; flex: 0 0 auto; padding: 7px 12px; border-radius: 999px; border: 1px solid rgba(190,255,215,0.14); background-color: rgba(7,17,14,0.45);')
                          for i, (_, n, c) in enumerate(HERO_COLOURS)],
        'display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; position: relative; z-index: 2; margin-top: 4px;', ['v2-swatches']),
    float_status, float_price, float_sched,
], 'position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 620px; @media(--tablet){ min-height: 600px; max-width: 640px; width: 100%; margin-left: auto; margin-right: auto; } @media(--mobile){ min-height: 460px; }')

copy = div('Hero copy', [
    chip('Hero chip', '● Home EV charging · supplied and fitted'),
    h('Hero title', 'Fast. Smart. Effortless.', 'h1', ['v2-display'], 'margin-top: 28px; font-size: clamp(44px, 5.6vw, 88px);'),
    p('Hero subtitle', 'Three finishes. Pick yours.', ['v2-display'], 'font-weight: 300; color: #A3FFC1; margin-top: 10px; font-size: clamp(30px, 3.4vw, 54px); line-height: 1.05; letter-spacing: -0.035em;'),
    p('Hero lead', 'A premium 7kW smart charger in Mythos Black, Space Grey or Midnight Green. Installation by a qualified electrician is included, starting with a free remote survey.', ['v2-lead'], 'margin-top: 28px;'),
    div('Hero CTAs', [vbtn('CTA primary', 'Buy now', PRODUCT + '#configure'), vbtn('CTA glass', 'Explore EV-Tron', PRODUCT, 'glass')],
        'display: flex; flex-wrap: wrap; gap: 14px; margin-top: 40px;'),
    div('Hero chips', [chip('Chip 1', '7kW home charging'), chip('Chip 2', 'Type 2'), chip('Chip 3', 'Wi-Fi + Bluetooth')],
        'display: flex; flex-wrap: wrap; gap: 10px; margin-top: 40px;'),
], 'display: flex; flex-direction: column; align-items: flex-start; position: relative; z-index: 2;')

rail_items = [('Power', '7kW single-phase'), ('Connector', 'Type 2'), ('Installation', 'Included'), ('Survey', 'Free and remote')]
rail = div('Spec rail', [div(f'Rail {i}', [p(f'Rail {i} k', k, ['v2-label']), p(f'Rail {i} v', v, None, 'font-size: 15.5px; font-weight: 600; color: #F5FFF8; margin-top: 6px;')],
                             'padding: 22px 24px; ' + ('' if i == 0 else 'border-left: 1px solid rgba(190,255,215,0.12); @media(--mobile){ border-left: 0; border-top: 1px solid rgba(190,255,215,0.12); }'))
                         for i, (k, v) in enumerate(rail_items)],
           'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-top: 56px; padding: 0; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }', ['v2-glass'])

hero = div('V2 hero', [div('V2 hero inner', [
    div('V2 hero grid', [copy, visual],
        'display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 24px; }'),
    rail,
], classes=['ev-container'])], classes=['v2-hero'], tag='section')

# ================= Shared helpers for V2 sections =================
def v2head(cid, chip_text, title, lead=None, center=False):
    kids = [chip(cid + ' chip', chip_text), h(cid + ' title', title, 'h2', ['v2-h2'], 'margin-top: 20px;')]
    if lead: kids.append(p(cid + ' lead', lead, ['v2-lead'], 'margin-top: 18px;'))
    return div(cid, kids, 'display: flex; flex-direction: column; align-items: ' + ('center; text-align: center; margin-left: auto; margin-right: auto;' if center else 'flex-start;') + ' max-width: 760px; margin-bottom: 64px; @media(--mobile){ margin-bottom: 40px; }')


def v2sec(cid, children):
    return div(cid, [div(cid + ' inner', children, classes=['ev-container'])], classes=['v2-sec'], tag='section')


def icon(cid, value, size=20, color='#A3FFC1'):
    return el('e-svg', cid, {'svg': {'value': value, 'library': value.split()[0]}}, f'width: {size}px; height: {size}px; color: {color};')


def itile(cid, value):
    return div(cid, [icon(cid + ' svg', value, 20)], 'width: 48px; height: 48px; min-width: 48px; max-width: 48px; flex: 0 0 48px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background-color: rgba(85,230,139,0.10); border: 1px solid rgba(190,255,215,0.18);')


def dots(cid, colours):
    return div(cid, [div(f'{cid} {i}', [], f'width: 18px; min-width: 18px; max-width: 18px; height: 18px; flex: 0 0 18px; border-radius: 999px; background-color: {c}; border: 2px solid rgba(255,255,255,0.18);') for i, c in enumerate(colours)],
               'display: flex; gap: 8px; align-items: center;')

# ================= 2. Product showcase =================
spec = lambda cid, k, v: div(cid, [p(cid + ' k', k, ['v2-label']), p(cid + ' v', v, ['v2-num'], 'font-size: 18px; margin-top: 8px;')],
                             'padding: 16px; border-radius: 14px; background-color: rgba(7,17,14,0.55); border: 1px solid rgba(190,255,215,0.10);')
EVC = [('Mythos Black', '#1B1D21'), ('Space Grey', '#6E737A'), ('Midnight Green', '#1E4A3A'), ('Crimson Red', '#5A1418')]
featured = div('Featured EV-Tron', [
    div('Feat top', [chip('Feat chip', 'Our own design'), p('Feat meta', '7kW · Type 2 · Tethered', None, MONO + 'font-size: 12px; color: #A1B5A8; letter-spacing: 0.06em;')],
        'display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;'),
    div('Feat stage', [el('e-image', 'Feat image', {'image': {'src': {'id': M['render_evtron']}, 'size': 'full'}}, 'width: 62%; max-width: 360px; height: auto; position: relative; z-index: 1;')],
        'position: relative; display: flex; justify-content: center; padding-top: 24px; padding-bottom: 8px;'),
    h('Feat name', 'EV-Tron Tethered', 'h3', ['v2-h2'], 'font-size: clamp(30px, 3vw, 44px);'),
    div('Feat colours', [dots('Feat dots', [c for _, c in EVC]), p('Feat colour name', 'Mythos Black · Space Grey · Midnight Green · Crimson Red', None, 'font-size: 13.5px; color: #A1B5A8;')],
        'display: flex; align-items: center; gap: 14px; flex-wrap: wrap; margin-top: 14px;'),
    div('Feat specs', [spec('FS1', 'Power', '7kW'), spec('FS2', 'Current', 'Up to 32A'), spec('FS3', 'Cable', 'Up to 10m'),
                       spec('FS4', 'Weather', 'IP65'), spec('FS5', 'Connect', 'Wi-Fi + BT'), spec('FS6', 'Load balancing', 'Built in')],
        'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-top: 24px; @media(--mobile){ grid-template-columns: repeat(2, minmax(0, 1fr)); }'),
    div('Feat foot', [div('Feat price wrap', [p('Feat price', PRICE, ['v2-num'], 'font-size: 40px;'), p('Feat price note', 'Charger price · cable and extras next', None, 'font-size: 13.5px; color: #A1B5A8; margin-top: 6px;')]),
                      div('Feat btns', [vbtn('Feat explore', 'Explore', PRODUCT, 'glass'), vbtn('Feat buy', 'Buy now', PRODUCT + '#configure')], 'display: flex; gap: 10px; flex-wrap: wrap;')],
        'display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; flex-wrap: wrap; margin-top: auto; padding-top: 28px;'),
], 'grid-row: span 2; padding: 32px; @media(--tablet){ grid-row: auto; }', ['v2-card'], tag='article')


def foxcard(cid, name, mid, meta, colours, cnames, price, url, chips, note='fully installed'):
    return div(cid, [
        div(cid + ' img', [el('e-image', cid + ' image', {'image': {'src': {'id': mid}, 'size': 'large'}}, 'width: 100%; height: auto; position: relative; z-index: 1;')],
            'position: relative; flex: 0 0 38%; max-width: 38%; @media(--mobile){ flex: 0 0 auto; max-width: 70%; margin-left: auto; margin-right: auto; }'),
        div(cid + ' body', [
            div(cid + ' chips', [chip(f'{cid} chip {i}', c) for i, c in enumerate(chips)], 'display: flex; gap: 8px; flex-wrap: wrap;'),
            h(cid + ' name', name, 'h3', ['v2-h3'], 'font-size: clamp(22px, 2vw, 28px); margin-top: 16px;'),
            p(cid + ' meta', meta, None, MONO + 'font-size: 12.5px; color: #A1B5A8; margin-top: 8px; letter-spacing: 0.04em;'),
            div(cid + ' colours', [dots(cid + ' dots', colours), p(cid + ' cn', cnames, None, 'font-size: 13px; color: #A1B5A8;')], 'display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-top: 14px;'),
            div(cid + ' foot', [div(cid + ' pw', [p(cid + ' price', price, ['v2-num'], 'font-size: 30px;'), p(cid + ' pn', note, None, 'font-size: 12.5px; color: #A1B5A8; margin-top: 4px;')]),
                                div(cid + ' btns', [vbtn(cid + ' explore', 'Explore', url, 'glass', 'min-height: 44px; padding: 0 18px;'), vbtn(cid + ' buy', 'Buy', url + '#buy', 'primary', 'min-height: 44px; padding: 0 18px;')], 'display: flex; gap: 8px;')],
                'display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: auto; padding-top: 20px;'),
        ], 'display: flex; flex-direction: column; flex: 1 1 auto; min-width: 0;'),
    ], 'flex-direction: row; gap: 20px; align-items: center; @media(--mobile){ flex-direction: column; align-items: stretch; }', ['v2-card'], tag='article')


showcase = v2sec('V2 range', [
    v2head('Range head', 'The range', 'EV-Tron, plus solar-ready chargers from Fox ESS.', 'EV-Tron is our own charger. Got solar panels? We also supply and install Fox ESS chargers, which can work with your solar system.'),
    div('Range grid', [featured,
        foxcard('Fox tethered', 'Fox ESS Tethered', M['render_foxt'], '7.3kW · Type 2 · Tethered', ['#1E2024', '#6FB7B5', '#9C86C9', '#D7A3AE'], 'Black · Blue · Purple · Pink', '£995', '/ev-chargers/fox-tethered-solar-ev-charger/', ['Fox ESS · partner brand', 'Solar-compatible']),
        foxcard('Fox untethered', 'Fox ESS Untethered', M['render_foxu'], '7.3kW · Type 2 socket · Untethered', ['#ECEDEA'], 'White', '£945', '/ev-chargers/fox-untethered-solar-ev-charger/', ['Fox ESS · partner brand', 'Solar-compatible'])],
        'display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 20px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }'),
    p('Range note', 'Fox ESS is an independent brand, supplied and installed by EV-Tron. Solar charging depends on the model and your system.', None, MONO + 'font-size: 11px; color: rgba(161,181,168,0.75); margin-top: 18px; letter-spacing: 0.04em;'),
])

# ================= 3. Benefits Bento =================
bars = div('Sched chart', [div(f'SB {i}', [], f'flex: 1 1 0; min-width: 0; height: {hh}%; border-radius: 4px 4px 2px 2px; background-color: {"#55E68B" if g else "rgba(255,255,255,0.10)"};')
                           for i, (hh, g) in enumerate([(70, 1), (82, 1), (90, 1), (76, 1), (40, 0), (30, 0), (22, 0), (18, 0), (20, 0), (26, 0), (30, 0), (34, 0), (28, 0), (24, 0), (22, 0), (30, 0), (46, 0), (60, 0), (64, 0), (52, 0), (40, 0), (34, 0), (58, 1), (66, 1)])],
            'display: flex; align-items: flex-end; gap: 5px; height: 150px; margin-top: auto; padding-top: 28px;')
loadviz = div('Load viz', [
    div('LV home', [p('LV home k', 'Home', ['v2-label']), div('LV home bar', [div('LV home fill', [], 'width: 58%; height: 100%; border-radius: 999px; background-color: rgba(163,255,193,0.55);')], 'height: 10px; border-radius: 999px; background-color: rgba(255,255,255,0.08); margin-top: 8px;')]),
    div('LV car', [p('LV car k', 'Charger adjusts', ['v2-label']), div('LV car bar', [div('LV car fill', [], 'width: 36%; height: 100%; border-radius: 999px; background-color: #55E68B;')], 'height: 10px; border-radius: 999px; background-color: rgba(255,255,255,0.08); margin-top: 8px;')], 'margin-top: 14px;'),
], 'margin-top: auto; padding-top: 24px;')

def tile(cid, kids, extra='', glass=True):
    return div(cid, kids, extra, ['v2-card' if glass else 'v2-solid'])

bento = v2sec('V2 benefits', [
    v2head('Ben head', 'Why EV-Tron', 'Everything a great home charger should be.', 'Smart where it matters, protected where it counts, and installed properly.'),
    div('Bento', [
        tile('B schedule', [itile('B sched icon', 'fa-regular fa-clock'), h('B sched t', 'Smart scheduling', 'h3', ['v2-h3'], 'margin-top: 20px;'),
                            p('B sched d', 'Set charging for your tariff’s cheaper hours in the app. UK smart chargers also avoid peak times by default.', ['v2-body'], 'margin-top: 8px; max-width: 42ch;'), bars],
             'grid-column: span 2; grid-row: span 2; @media(--tablet){ grid-row: auto; } @media(--mobile){ grid-column: auto; }'),
        tile('B power', [p('B power n', '7kW', ['v2-num'], 'font-size: clamp(48px, 5vw, 72px); color: #A3FFC1;'), p('B power d', 'Up to 32A single-phase home charging', ['v2-body'], 'margin-top: 12px;')], 'justify-content: flex-end; min-height: 220px;', glass=False),
        tile('B app', [itile('B app icon', 'fa-solid fa-wifi'), h('B app t', 'Wi-Fi and Bluetooth', 'h3', ['v2-h3'], 'margin-top: 20px;'), p('B app d', 'Start, stop and monitor charging from your phone.', ['v2-body'], 'margin-top: 8px;')]),
        tile('B safety', [itile('B safe icon', 'fa-solid fa-shield-halved'), h('B safe t', 'Protected installation', 'h3', ['v2-h3'], 'margin-top: 20px;'), p('B safe d', 'A dedicated EV consumer unit with surge protection, and PEN fault protection appropriate to your home.', ['v2-body'], 'margin-top: 8px;')], glass=False),
        tile('B ip', [p('B ip n', 'IP65', ['v2-num'], 'font-size: clamp(44px, 4.4vw, 64px);'), p('B ip d', 'Weather-sealed for outdoor installation (EV-Tron).', ['v2-body'], 'margin-top: 12px;')], 'justify-content: flex-end;'),
        tile('B load', [itile('B load icon', 'fa-solid fa-gauge-high'), h('B load t', 'Load balancing, included', 'h3', ['v2-h3'], 'margin-top: 20px;'),
                        p('B load d', 'A CT clamp watches your home’s demand and adjusts charging, so your supply isn’t overloaded.', ['v2-body'], 'margin-top: 8px; max-width: 46ch;'), loadviz],
             'grid-column: span 2; @media(--mobile){ grid-column: auto; }', glass=False),
        tile('B rfid', [itile('B rfid icon', 'fa-solid fa-id-card'), h('B rfid t', 'RFID access', 'h3', ['v2-h3'], 'margin-top: 20px;'), p('B rfid d', 'Tap a card to start or stop a session.', ['v2-body'], 'margin-top: 8px;')]),
        tile('B fast', [p('B fast n', '48–96h', ['v2-num'], 'font-size: clamp(36px, 3.6vw, 52px);'), p('B fast d', 'Installation in as little as 48 to 96 hours in selected areas.', ['v2-body'], 'margin-top: 12px;')], 'justify-content: flex-end;', glass=False),
    ], 'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); gap: 14px; }'),
])

# ================= 4. Technology =================
app_row = lambda cid, k, v: div(cid, [p(cid + ' k', k, None, 'font-size: 13px; color: #A1B5A8;'), p(cid + ' v', v, None, MONO + 'font-size: 13px; color: #F5FFF8;')],
                                'display: flex; justify-content: space-between; padding-top: 10px; padding-bottom: 10px; border-bottom: 1px solid rgba(190,255,215,0.08);')
phone = div('Phone', [
    div('Phone notch', [], 'width: 90px; height: 6px; border-radius: 999px; background-color: rgba(255,255,255,0.14); margin-left: auto; margin-right: auto;'),
    p('App title', 'Driveway charger', None, 'font-weight: 600; color: #F5FFF8; margin-top: 22px; font-size: 15px;'),
    p('App state', '● Connected · charging', None, MONO + 'font-size: 11.5px; color: #55E68B; margin-top: 4px;'),
    div('App ring', [p('App kwh', '18.6', ['v2-num'], 'font-size: 46px;'), p('App kwh l', 'kWh added', None, 'font-size: 12px; color: #A1B5A8; margin-top: 6px;')],
        'width: 190px; height: 190px; margin: 26px auto 22px; border-radius: 999px; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 10px solid rgba(85,230,139,0.85); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);'),
    app_row('AR1', 'Power', '7.0 kW'), app_row('AR2', 'Time', '2h 39m'), app_row('AR3', 'Current', '32 A'),
    div('App btn', [p('App btn t', 'Stop charging', None, 'font-weight: 600; font-size: 14px; color: #06150C;')], 'margin-top: 18px; padding: 12px; border-radius: 999px; background-color: #55E68B; text-align: center;'),
], 'position: relative; z-index: 2; width: 300px; max-width: 100%; margin-left: auto; margin-right: auto; padding: 22px 22px 26px; border-radius: 40px; background-color: rgba(7,17,14,0.72); border: 1px solid rgba(190,255,215,0.22);')
tf = lambda cid, kids, pos: div(cid, kids, 'width: max-content; max-width: 240px; ' + pos, ['v2-float'])
tech_visual = div('Tech visual', [
    phone,
    tf('TF schedule', [p('TFS l', 'Schedule', ['v2-label']), p('TFS v', 'Off-peak window', None, 'font-weight: 600; color: #F5FFF8; margin-top: 6px; font-size: 14px;'), p('TFS t', 'Set your own times', None, 'font-size: 12.5px; color: #A1B5A8; margin-top: 4px;')], 'left: 0; top: 12%; @media(--mobile){ display: none; }'),
    tf('TF load', [p('TFL l', 'Load balancing', ['v2-label']), p('TFL v', '● Active', None, MONO + 'font-size: 14px; color: #55E68B; margin-top: 6px;')], 'right: 0; top: 30%; @media(--mobile){ display: none; }'),
    tf('TF rfid', [p('TFR l', 'Access', ['v2-label']), p('TFR v', 'RFID card or app', None, 'font-weight: 600; color: #F5FFF8; margin-top: 6px; font-size: 14px;')], 'left: 4%; bottom: 10%; @media(--mobile){ display: none; }'),
], 'position: relative; display: flex; align-items: center; justify-content: center; min-height: 640px; @media(--mobile){ min-height: auto; }')
tech = v2sec('V2 tech', [div('Tech grid', [
    div('Tech copy', [
        chip('Tech chip', 'Smart app'),
        h('Tech title', 'Your charger, in your pocket.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
        p('Tech lead', 'See what’s happening in real time, schedule charging for cheaper hours, and adjust the charging current to suit your home.', ['v2-lead'], 'margin-top: 18px;'),
        div('Tech list', [div(f'TL {i}', [itile(f'TL {i} icon', ic), div(f'TL {i} txt', [h(f'TL {i} t', t, 'h3', ['v2-h3'], 'font-size: 17px;'), p(f'TL {i} d', d, ['v2-body'], 'margin-top: 4px; font-size: 14.5px;')])],
                              'display: flex; gap: 16px; align-items: flex-start;')
                          for i, (ic, t, d) in enumerate([('fa-solid fa-chart-line', 'Real-time monitoring', 'Power, current, time and energy for every session.'),
                                                          ('fa-regular fa-clock', 'Scheduled charging', 'Charge when your electricity is cheapest.'),
                                                          ('fa-solid fa-sliders', 'Adjustable current', 'Set the charging current to suit your supply.')])],
            'display: flex; flex-direction: column; gap: 22px; margin-top: 36px;'),
    ], 'display: flex; flex-direction: column; align-items: flex-start;'),
    tech_visual,
], 'display: grid; grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr); gap: 56px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 40px; }')])

# ================= 5. The process (replaces V1 "How it works") =================
STEPS = [('fa-solid fa-sliders', 'Choose and order', 'Pick your colour, cable length and any extras online. We’ll call you to confirm the details.', 'Online, in a few clicks'),
         ('fa-solid fa-mobile-screen', 'Free remote survey', 'Send photos or a short video, or talk us through it by phone. We confirm your installation and agree any extras first.', 'Phone, photos or video'),
         ('fa-solid fa-bolt', 'Installed and ready', 'A qualified electrician fits, tests and certifies your charger, then sets up the app with you.', 'Installed within 10 days of survey approval')]
process = v2sec('V2 process', [
    v2head('Proc head', 'The process', 'From order to first charge, in three steps.', 'No home visit needed to get started. We check everything remotely, then a qualified electrician fits your charger.', center=True),
    div('Proc track', [
        div('Proc line', [div('Proc fill', [], 'width: 0; height: 100%; border-radius: 999px; background-color: #55E68B;')],
            'position: absolute; left: 32px; right: 32px; width: auto; top: 14px; height: 2px; border-radius: 999px; background-color: rgba(190,255,215,0.14); @media(--tablet){ display: none; }'),
        div('Proc grid', [div(f'Step {i}', [
            p(f'Step {i} n', f'0{i + 1}', None, MONO + 'font-size: 64px; line-height: 1; font-weight: 500; letter-spacing: -0.04em; color: rgba(163,255,193,0.18);'),
            itile(f'Step {i} icon', ic),
            h(f'Step {i} t', t, 'h3', ['v2-h3'], 'margin-top: 20px;'),
            p(f'Step {i} d', d, ['v2-body'], 'margin-top: 8px;'),
            p(f'Step {i} m', m, None, MONO + 'font-size: 12px; letter-spacing: 0.04em; color: #A3FFC1; margin-top: auto; padding-top: 24px;'),
        ], 'gap: 0;', ['v2-card', 'v2-step']) for i, (ic, t, d, m) in enumerate(STEPS)],
            'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }'),
    ], 'padding-top: 44px; @media(--tablet){ padding-top: 0; }', ['v2-proc']),
])

# ================= 7. Trust =================
facts = [('fa-solid fa-mobile-screen', 'Free remote survey', 'By phone, photos or video, so there are no unnecessary home visits.'),
         ('fa-solid fa-sterling-sign', 'Clear pricing', 'Your options are priced up front, and any extra work is agreed before it starts.'),
         ('fa-solid fa-screwdriver-wrench', 'Qualified electricians', 'Our network of experienced, qualified electricians fits every charger.'),
         ('fa-solid fa-file-circle-check', 'Certified on completion', 'Electrical installation certificate and DNO notification handled for you.'),
         ('fa-solid fa-headset', 'One point of contact', 'Installation, technical help and aftercare all go through EV-Tron.'),
         ('fa-solid fa-shield', '3-year warranty', 'Extendable to 5 years for £89.99. Full terms published before launch.')]
trust = v2sec('V2 trust', [div('Trust grid', [
    div('Trust statement', [chip('Trust chip', 'Honest by design'),
                            h('Trust title', 'Straightforward from order to aftercare.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                            p('Trust lead', 'We publish our prices, spell out what’s included, and agree any extras with you first.', ['v2-lead'], 'margin-top: 18px;'),
                            div('Trust meta', [p('TM1', 'Covering England · UK-wide expansion planned', None, MONO + 'font-size: 12px; color: #A3FFC1; letter-spacing: 0.04em;'),
                                               p('TM2', 'Monday to Saturday · 8:30am to 6:30pm', None, MONO + 'font-size: 12px; color: #A1B5A8; letter-spacing: 0.04em; margin-top: 8px;')],
                                'margin-top: auto; padding-top: 40px; border-top: 1px solid rgba(190,255,215,0.12);')],
        'justify-content: flex-start; padding: 40px; @media(--mobile){ padding: 24px; }', ['v2-card']),
    div('Trust facts', [div(f'Fact {i}', [itile(f'Fact {i} icon', ic), h(f'Fact {i} t', t, 'h3', ['v2-h3'], 'margin-top: 18px; font-size: 18px;'), p(f'Fact {i} d', d, ['v2-body'], 'margin-top: 6px; font-size: 14.5px;')], classes=['v2-solid'])
                        for i, (ic, t, d) in enumerate(facts)],
        'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
], 'display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 20px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); }')])

X = div('Home V2', [hero, showcase, bento, tech, process, trust], 'background-color: #07110E;', tag='main')

if __name__ == '__main__':
    r = wp.ability('elementor/build-composition', {'post_id': PID, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('hero', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:6])
    print(wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': PID}), 'DELETE').get('status'))
    # Append V1's remaining sections (unchanged for now) into the V2 <main>, after the new hero
    v1 = json.loads(wp.req('wp/v2/pages/95?context=edit')['meta']['_elementor_data'])
    v2 = json.loads(wp.req(f'wp/v2/pages/{PID}?context=edit')['meta']['_elementor_data'])
    new = v2[0]['elements']            # hero, showcase, bento, tech, process, trust
    v1s = v1[0]['elements']            # 0 hero, 1 chargers, 2 how (replaced by process), 3 costs, 4 faqs, 5 closing
    v2[0]['elements'] = new[:5] + [v1s[3], new[5], v1s[4], v1s[5]]
    raw = json.dumps(v2)
    for a, b in [('with the reasons and the installed price', 'with the reasons and the price')]:   # copy tweaks for kept V1 sections
        raw = raw.replace(a, b)
    print('assembled', len(v2[0]['elements']), wp.req(f'wp/v2/pages/{PID}', 'POST', {'meta': {'_elementor_data': raw}}).get('id'))
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
