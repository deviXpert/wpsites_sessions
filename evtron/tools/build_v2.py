"""EV-Tron V2 (emerald glassmorphism) homepage: /home-v2/.
Stage 1 = new hero only; the remaining sections are V1's, appended unchanged until each is redesigned.
Run: EVTRON_WP_USER=<admin login> python3 build_v2.py"""
import json, urllib.parse, wp
from build_home import el, div, p, h, cfg, st, cl, MONO, SITE

C = json.load(open('created.json'))
M = json.load(open('media.json'))
PID = C['home_v2']
cfg.clear(); st.clear(); cl.clear()


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
    p('Price label', 'Installed from', ['v2-label']),
    p('Price value', '£945', None, MONO + 'font-weight: 500; font-size: 34px; line-height: 1; color: #F5FFF8; margin-top: 8px;'),
    p('Price note', 'incl. standard installation', None, 'font-size: 13px; color: #A1B5A8; margin-top: 6px;'),
], 'width: max-content; right: 0; top: 44%; @media(--mobile){ top: auto; bottom: 14%; right: 0; }', ['v2-float'])

float_sched = div('Float schedule', [
    p('Sched label', 'Smart scheduling', ['v2-label']),
    p('Sched text', 'Avoids peak hours by default', None, 'font-size: 14px; color: #F5FFF8; margin-top: 8px; font-weight: 600;'),
    div('Sched bars', [div(f'Bar {i}', [], f'width: 8px; min-width: 8px; max-width: 8px; flex: 0 0 8px; height: {hgt}px; border-radius: 3px; background-color: {"#55E68B" if g else "rgba(255,255,255,0.14)"};')
                       for i, (hgt, g) in enumerate([(14, 1), (22, 1), (10, 0), (8, 0), (18, 1), (26, 1), (12, 0), (20, 1)])],
        'display: flex; align-items: flex-end; gap: 5px; margin-top: 12px; height: 26px;'),
], 'width: max-content; left: 2%; bottom: 10%; @media(--mobile){ display: none; }', ['v2-float'])

visual = div('Hero visual', [
    div('Visual halo', [], 'position: absolute; left: 50%; top: 50%; width: 78%; aspect-ratio: 1; transform: translate(-50%, -50%); border-radius: 999px; border: 1px solid rgba(190,255,215,0.10);'),
    el('e-image', 'Hero product', {'image': {'src': {'id': M['render_evtron']}, 'size': 'full'}},
       'position: relative; z-index: 1; width: 66%; max-width: 480px; height: auto; margin-left: auto; margin-right: auto; @media(--mobile){ width: 80%; }'),
    float_status, float_price, float_sched,
    p('Visual caption', 'Illustration · product photography to follow', None, MONO + 'position: absolute; right: 0; bottom: 0; font-size: 10.5px; letter-spacing: 0.06em; color: rgba(161,181,168,0.7); z-index: 2;'),
], 'position: relative; display: flex; align-items: center; justify-content: center; min-height: 620px; @media(--tablet){ min-height: 600px; max-width: 640px; width: 100%; margin-left: auto; margin-right: auto; } @media(--mobile){ min-height: 460px; }')

copy = div('Hero copy', [
    chip('Hero chip', '● Home EV charging · supplied and fitted'),
    h('Hero title', 'Fast. Smart. Effortless.', 'h1', ['v2-display'], 'margin-top: 28px; font-size: clamp(44px, 5.6vw, 88px);'),
    p('Hero subtitle', 'One price, fully installed.', ['v2-display'], 'font-weight: 300; color: #A3FFC1; margin-top: 10px; font-size: clamp(30px, 3.4vw, 54px); line-height: 1.05; letter-spacing: -0.035em;'),
    p('Hero lead', 'Premium home chargers, fitted by qualified electricians at one clear price. See exactly what’s included, then pay in full or spread the cost.', ['v2-lead'], 'margin-top: 28px;'),
    div('Hero CTAs', [vbtn('CTA primary', 'Choose your charger', '/ev-chargers/'), vbtn('CTA glass', 'How installation works', '/installation/', 'glass')],
        'display: flex; flex-wrap: wrap; gap: 14px; margin-top: 40px;'),
    div('Hero chips', [chip('Chip 1', '7kW home charging'), chip('Chip 2', 'Type 2'), chip('Chip 3', 'Pay in instalments')],
        'display: flex; flex-wrap: wrap; gap: 10px; margin-top: 40px;'),
], 'display: flex; flex-direction: column; align-items: flex-start; position: relative; z-index: 2;')

rail_items = [('Power', '7kW single-phase'), ('Connector', 'Type 2'), ('Installation', 'Included as standard'), ('Payment', 'In full or instalments')]
rail = div('Spec rail', [div(f'Rail {i}', [p(f'Rail {i} k', k, ['v2-label']), p(f'Rail {i} v', v, None, 'font-size: 15.5px; font-weight: 600; color: #F5FFF8; margin-top: 6px;')],
                             'padding: 22px 24px; ' + ('' if i == 0 else 'border-left: 1px solid rgba(190,255,215,0.12); @media(--mobile){ border-left: 0; border-top: 1px solid rgba(190,255,215,0.12); }'))
                         for i, (k, v) in enumerate(rail_items)],
           'display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-top: 56px; padding: 0; @media(--mobile){ grid-template-columns: minmax(0, 1fr); }', ['v2-glass'])

hero = div('V2 hero', [div('V2 hero inner', [
    div('V2 hero grid', [copy, visual],
        'display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 24px; }'),
    rail,
], classes=['ev-container'])], classes=['v2-hero'], tag='section')

X = div('Home V2', [hero], 'background-color: #07110E;', tag='main')

if __name__ == '__main__':
    r = wp.ability('elementor/build-composition', {'post_id': PID, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('hero', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:6])
    print(wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': PID}), 'DELETE').get('status'))
    # Append V1's remaining sections (unchanged for now) into the V2 <main>, after the new hero
    v1 = json.loads(wp.req('wp/v2/pages/95?context=edit')['meta']['_elementor_data'])
    v2 = json.loads(wp.req(f'wp/v2/pages/{PID}?context=edit')['meta']['_elementor_data'])
    v2[0]['elements'] = v2[0]['elements'][:1] + v1[0]['elements'][1:]
    print('appended V1 sections', len(v1[0]['elements']) - 1, wp.req(f'wp/v2/pages/{PID}', 'POST', {'meta': {'_elementor_data': json.dumps(v2)}}).get('id'))
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
