"""About us page (/about/) in the V2 glass style, from the client's copy (docs/client-about.md).
Only the client's mission and values plus facts already agreed (coverage, hours, survey, contact). No invented team, dates or stats.
Run: EVTRON_WP_USER=<admin login> python3 build_about.py"""
import json
import urllib.parse

import wp
import build_v2 as B
from build_home import el, div, p, h, cfg, st, cl, MONO

C = json.load(open('created.json'))
cfg.clear(); st.clear(); cl.clear()
chip, v2head, v2sec, itile, vbtn = B.chip, B.v2head, B.v2sec, B.itile, B.vbtn
PRODUCT = '/ev-chargers/evtron-tethered-ev-charger/'

hero = div('AB hero', [div('AB hero inner', [
    div('AB hero copy', [
        chip('AB chip', '● About EV-Tron'),
        h('AB title', 'Driven by innovation.', 'h1', ['v2-display'], 'margin-top: 28px; font-size: clamp(48px, 6.4vw, 104px);'),
        p('AB sub', 'The future of electric driving starts at home.', ['v2-display'], 'font-weight: 300; color: #A3FFC1; margin-top: 14px; font-size: clamp(26px, 3vw, 46px); line-height: 1.1; letter-spacing: -0.03em;'),
        p('AB lead', 'At EV-Tron, we make home EV charging smarter, simpler and more accessible, with a premium charger you can buy online or have fitted by a qualified electrician.', ['v2-lead'], 'margin-top: 28px; max-width: 60ch;'),
    ], 'display: flex; flex-direction: column; align-items: flex-start; max-width: 980px;'),
], classes=['ev-container'])], classes=['v2-hero'], tag='section')

mission = v2sec('AB mission', [div('AB m grid', [
    div('AB m label', [chip('AB m chip', 'Our mission')], 'display: flex; flex-direction: column; align-items: flex-start;'),
    div('AB m body', [
        h('AB m title', 'Smarter, simpler, more accessible home charging.', 'h2', ['v2-h2']),
        p('AB m p1', 'By combining innovative technology, premium contemporary design and professional installation, we provide charging solutions designed around modern lifestyles.', ['v2-lead'], 'margin-top: 24px;'),
        p('AB m p2', 'Through our network of qualified electricians, we aim to deliver nationwide installation coverage, fast turnaround times and a seamless customer experience. Today we cover England.', ['v2-body'], 'margin-top: 18px; font-size: 17px;'),
        p('AB m p3', 'From choosing your charger to installation and ongoing aftercare, we’re committed to making every step straightforward and hassle-free.', ['v2-body'], 'margin-top: 14px; font-size: 17px;'),
    ]),
], 'display: grid; grid-template-columns: minmax(0, 0.45fr) minmax(0, 1.55fr); gap: 56px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 20px; }')])

VALUES = [('fa-solid fa-microchip', 'Innovation and intelligent technology', 'App control over Wi-Fi and Bluetooth, smart scheduling and built-in protection.'),
          ('fa-solid fa-gem', 'Premium quality and contemporary design', 'A charger in four finishes, designed to look at home on your wall.'),
          ('fa-solid fa-sterling-sign', 'Transparent pricing', 'Prices published online, and any extra work agreed before it starts.'),
          ('fa-solid fa-bolt', 'Fast and convenient installation', 'A free remote survey, then most installs within 10 days of survey approval.'),
          ('fa-solid fa-screwdriver-wrench', 'Professional workmanship', 'Qualified electricians who test and certify every installation.'),
          ('fa-solid fa-headset', 'Customer service and aftercare', 'One point of contact, from your first question to support after installation.')]
values = v2sec('AB values', [
    v2head('AB v head', 'What we stand for', 'Six values behind every charger we supply.', None, center=True),
    div('AB v grid', [div(f'AV {i}', [
        div(f'AV {i} top', [itile(f'AV {i} icon', ic), p(f'AV {i} n', f'0{i + 1}', None, MONO + 'font-size: 13px; color: rgba(163,255,193,0.55); letter-spacing: 0.08em;')],
            'display: flex; justify-content: space-between; align-items: center; width: 100%;'),
        h(f'AV {i} t', t, 'h3', ['v2-h3'], 'margin-top: 22px;'),
        p(f'AV {i} d', d, ['v2-body'], 'margin-top: 8px;'),
    ], classes=['v2-card' if i % 2 == 0 else 'v2-solid']) for i, (ic, t, d) in enumerate(VALUES)],
        'display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; @media(--tablet){ grid-template-columns: repeat(2, minmax(0, 1fr)); } @media(--mobile){ grid-template-columns: minmax(0, 1fr); }'),
])

FACTS = [('Coverage', 'England, with UK-wide expansion planned'), ('Survey', 'Free and remote, by phone, photos or video'),
         ('Opening hours', 'Monday to Saturday, 8:30am to 6:30pm'), ('Get in touch', 'sales@evtron.co.uk · info@evtron.co.uk')]
facts = v2sec('AB facts', [div('AB f grid', [
    div('AB f copy', [chip('AB f chip', 'Get started'),
                      h('AB f title', 'Buy online, or let us fit it.', 'h2', ['v2-h2'], 'margin-top: 20px;'),
                      p('AB f lead', 'Choose your finish and options online, or ask us to supply and install it after a free remote survey.', ['v2-lead'], 'margin-top: 16px;'),
                      div('AB f btns', [vbtn('AB f buy', 'Buy now', PRODUCT + '#configure'), vbtn('AB f install', 'Request installation', PRODUCT + '#details', 'glass')],
                          'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px;')],
        'display: flex; flex-direction: column; align-items: flex-start;'),
    div('AB f list', [div(f'AF {i}', [p(f'AF {i} k', k, ['v2-label']), p(f'AF {i} v', v, None, 'font-size: 17px; color: #F5FFF8; font-weight: 600; margin-top: 8px;')],
                          'padding: 22px 0; border-bottom: 1px solid rgba(190,255,215,0.12);') for i, (k, v) in enumerate(FACTS)],
        'padding: 12px 32px; @media(--mobile){ padding: 8px 20px; }', ['v2-glass']),
], 'display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 56px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; }')])

X = div('About', [hero, mission, values, facts], 'background-color: #07110E;', tag='main')


def ensure_page():
    if 'about' not in C:
        hit = [x for x in wp.req('wp/v2/pages?slug=about&status=publish,draft') or []]
        C['about'] = hit[0]['id'] if hit else wp.req('wp/v2/pages', 'POST', {'title': 'About us', 'slug': 'about', 'status': 'publish', 'template': 'elementor_header_footer'})['id']
    wp.req(f"wp/v2/pages/{C['about']}", 'POST', {'status': 'publish', 'template': 'elementor_header_footer',
                                                'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_page_settings': {'hide_title': 'yes'},
                                                         'site-sidebar-layout': 'no-sidebar', 'ast-site-content-layout': 'full-width-container', 'site-content-style': 'unboxed'}})
    json.dump(C, open('created.json', 'w'), indent=1)
    return C['about']


if __name__ == '__main__':
    pid = ensure_page()
    r = wp.ability('elementor/build-composition', {'post_id': pid, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('build', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:6])
    print('publish', wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': pid}), 'DELETE').get('status'))
    r = wp.ability('elementor/manage-site-parts', {'operations': [{'action': 'update', 'post_id': 145, 'conditions': [
        'include/singular/front_page', 'include/singular/page/141', f"include/singular/product/{C['wc_evtron']}", f'include/singular/page/{pid}']}]})
    print('v2 styles on', r['results'][0].get('conditions'))
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
    print(wp.req(f'wp/v2/pages/{pid}')['link'])
