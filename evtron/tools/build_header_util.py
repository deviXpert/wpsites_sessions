"""Header utility row (client feedback 19 Nov): sales@ pill + USP row, inserted at the top of the header site part.
Also switches the header CTA to "Buy now". Phone / WhatsApp are added once the client supplies the numbers.
Idempotent: removes an existing utility row (found by its layer name) before inserting.
Run: EVTRON_WP_USER=<admin login> python3 build_header_util.py"""
import json
import urllib.parse

import wp
from build_home import el, div, p, cfg, st, cl, SITE

C = json.load(open('created.json'))
HID = C['header']
ROOT = '1f4afb1e'          # header root (tag header)
CTA = 'd509f11'            # header primary button
BUY_URL = '/ev-chargers/evtron-tethered-ev-charger/#configure'

USPS = ['Installation available', 'Free remote survey', 'Secure checkout', 'Installed within 10 days of survey approval']


def tick(cid):
    return el('e-svg', cid, {'svg': {'value': 'fa-solid fa-check', 'library': 'fa-solid'}}, 'width: 12px; height: 12px; color: #55E68B;')


def build():
    cfg.clear(); st.clear(); cl.clear()
    mail = el('e-button', 'Util mail', {'text': 'sales@evtron.co.uk', 'link': {'destination': 'mailto:sales@evtron.co.uk'}},
              'font-size: 12.5px; line-height: 1; padding: 7px 12px; min-height: 0; border-radius: 999px; border: 1px solid rgba(190,255,215,0.20); '
              'background-color: rgba(255,255,255,0.03); color: #F5FFF8; font-weight: 500; &:hover{ border-color: rgba(120,255,170,0.45); } @media(--mobile){ display: none; }')
    usps = div('Util usps', [div(f'Util usp {i}', [tick(f'Util tick {i}'), p(f'Util usp t {i}', t, None, 'font-size: 12.5px; color: #C9D6CE;')], classes=['ev-usp'])
                             for i, t in enumerate(USPS)],
               'display: flex; align-items: center; justify-content: flex-end; gap: 28px; flex: 1 1 auto; flex-wrap: nowrap; overflow: hidden; @media(--mobile){ justify-content: center; }')
    link = lambda cid, t, u: el('e-button', cid, {'text': t, 'link': {'destination': SITE + u}},
                                'font-size: 12.5px; line-height: 1; padding: 7px 4px; min-height: 0; border: 0; background-color: transparent; color: #C9D6CE; font-weight: 500; '
                                '&:hover{ color: #A3FFC1; } @media(--mobile){ display: none; }')
    left = div('Util left', [mail, link('Util installers', 'For installers', '/for-installers/'), link('Util dealers', 'For dealerships', '/for-dealerships/')],
               'display: flex; align-items: center; gap: 14px; width: auto; flex: 0 0 auto; @media(--mobile){ display: none; }')
    return div('Utility bar', [left, usps], classes=['ev-util'])


if __name__ == '__main__':
    data = json.loads(wp.req(f'wp/v2/elementor_library/{HID}?context=edit')['meta']['_elementor_data'])
    root = data[0]
    old = [e['id'] for e in root['elements'] if (e.get('editor_settings') or {}).get('title') == 'Utility bar']
    if old:
        print('delete old', wp.ability('elementor/manage-elements', {'post_id': HID, 'operations': [{'action': 'delete', 'element_id': i} for i in old]}).get('status'))
    X = build()
    r = wp.ability('elementor/build-composition', {'post_id': HID, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'parent_id': ROOT, 'mode': 'append'})
    print('build', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:4])
    pub = lambda: wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': HID}), 'DELETE').get('status')
    print('publish', pub())   # publish first: the saved meta is only current after publishing
    data = json.loads(wp.req(f'wp/v2/elementor_library/{HID}?context=edit')['meta']['_elementor_data'])
    util = next(e['id'] for e in data[0]['elements'] if (e.get('editor_settings') or {}).get('title') == 'Utility bar')
    ops = [{'action': 'move', 'element_id': util, 'new_parent_id': ROOT, 'index': 0},
           {'action': 'update', 'element_id': ROOT, 'style': 'display: flex; flex-direction: column;'},
           {'action': 'update', 'element_id': CTA, 'settings': {'text': 'Buy now', 'link': {'destination': SITE + BUY_URL}}}]
    print('ops', [r['status'] for r in wp.ability('elementor/manage-elements', {'post_id': HID, 'operations': ops})['results']])
    print('publish', pub())
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
