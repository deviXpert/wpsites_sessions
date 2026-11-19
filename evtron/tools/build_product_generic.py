"""General single-product template (Theme Builder, type product, all products) in the V2 glass style.
Products with their own template (EV-Tron Tethered) keep it: Elementor prefers the more specific condition.
Everything product-specific is dynamic (title, price, short description, description, gallery, add to basket),
so new products need no extra build. Also writes the Fox ESS descriptions from the client's information.
Run: EVTRON_WP_USER=<admin login> python3 build_product_generic.py"""
import json
import urllib.parse

import wp
import build_v2 as B
from build_home import el, div, p, h, cfg, st, cl, MONO

C = json.load(open('created.json'))
cfg.clear(); st.clear(); cl.clear()
chip, v2sec = B.chip, B.v2sec
TAG = lambda name: {'name': name, 'settings': {}}
TICK = lambda cid: el('e-svg', cid, {'svg': {'value': 'fa-solid fa-check', 'library': 'fa-solid'}}, 'width: 14px; height: 14px; color: #55E68B;')

hero = div('GP hero', [div('GP hero inner', [div('GP grid', [
    div('GP gallery', [el('woocommerce-product-images', 'GP images', {'sale_flash': False})], 'padding: 28px; @media(--mobile){ padding: 14px; }', ['v2-glass', 'gp-gallery']),
    div('GP buy', [
        chip('GP chip', 'Supplied by EV-Tron'),
        h('GP title', TAG('woocommerce-product-title-tag'), 'h1', ['v2-h2'], 'margin-top: 18px; font-size: clamp(34px, 3.6vw, 56px);'),
        p('GP price', TAG('woocommerce-product-price-tag'), ['v2-num'], 'font-size: 40px; line-height: 1; margin-top: 24px;'),
        p('GP short', TAG('woocommerce-product-short-description-tag'), ['v2-lead'], 'margin-top: 20px; font-size: 17px;'),
        div('GP cart', [el('woocommerce-product-add-to-cart', 'GP add', {'show_quantity': False, 'layout': 'stacked'})], 'width: 100%; margin-top: 28px;', ['gp-cart']),
        div('GP assure', [div(f'GP as {i}', [TICK(f'GP as {i} t'), p(f'GP as {i} p', t, None, 'font-size: 14.5px; color: #DCE8E0;')], 'display: flex; gap: 10px; align-items: center; width: auto;')
                          for i, t in enumerate(['Free remote survey', 'Qualified electricians', 'Secure checkout'])],
            'display: flex; flex-wrap: wrap; gap: 10px 24px; margin-top: 28px; padding-top: 22px; border-top: 1px solid rgba(190,255,215,0.12); width: 100%;'),
        p('GP help', 'Questions? Email sales@evtron.co.uk', None, MONO + 'font-size: 12px; letter-spacing: 0.04em; color: #A3FFC1; margin-top: 18px;'),
    ], 'display: flex; flex-direction: column; align-items: flex-start;'),
], 'display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 56px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 32px; }')],
    classes=['ev-container'])], 'padding-top: 180px; padding-bottom: 96px; @media(--tablet){ padding-top: 190px; } @media(--mobile){ padding-top: 170px; padding-bottom: 64px; }', ['pp-hero'], tag='section')

details = v2sec('GP details', [div('GP d grid', [
    div('GP d side', [chip('GP d chip', 'Details'), h('GP d title', 'The full picture.', 'h2', ['v2-h2'], 'margin-top: 20px;')],
        'display: flex; flex-direction: column; align-items: flex-start;'),
    div('GP d body', [p('GP content', TAG('woocommerce-product-content-tag'), ['v2-body'], 'font-size: 16.5px; line-height: 1.7;')],
        'padding: 36px; @media(--mobile){ padding: 22px; }', ['v2-card', 'gp-content']),
], 'display: grid; grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr); gap: 56px; align-items: start; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 24px; }')])

X = div('Product', [hero, details], 'background-color: #07110E;', tag='main')

FOX = {
    'wc_foxt': ('<p>A 7kW tethered Type 2 home charger from Fox ESS, an independent brand we supply and install. It can charge your car from surplus solar power, depending on the model and your solar system.</p>'
                '<ul><li>7kW single-phase, tethered Type 2 cable</li><li>Solar-compatible, subject to model and system</li><li>Dynamic load balancing with CT clamp included in the installation</li>'
                '<li>Colours: black, blue, purple and pink (availability to be confirmed)</li><li>Price includes a standard installation by a qualified electrician</li></ul>'
                '<p>Not sure it suits your solar set-up? Email sales@evtron.co.uk before you order and we’ll check.</p>'),
    'wc_foxu': ('<p>A 7kW untethered Type 2 socket charger from Fox ESS, an independent brand we supply and install. You plug in your own cable, and it can charge your car from surplus solar power, depending on the model and your solar system.</p>'
                '<ul><li>7kW single-phase, Type 2 socket (use your own cable)</li><li>Solar-compatible, subject to model and system</li><li>Dynamic load balancing with CT clamp included in the installation</li>'
                '<li>Colour: white</li><li>Price includes a standard installation by a qualified electrician</li></ul>'
                '<p>Not sure it suits your solar set-up? Email sales@evtron.co.uk before you order and we’ll check.</p>'),
}

if __name__ == '__main__':
    for k, d in FOX.items():
        print('desc', wp.req(f"wc/v3/products/{C[k]}", 'PUT', {'description': d}).get('id'))
    if 'tpl_product_generic' not in C:
        r = wp.ability('elementor/manage-site-parts', {'operations': [{'action': 'create', 'type': 'product', 'title': 'Product (general)'}]})
        C['tpl_product_generic'] = r['results'][0]['id']; json.dump(C, open('created.json', 'w'), indent=1)
    tid = C['tpl_product_generic']
    ops = [{'action': 'create', 'label': c, 'css': 'position: relative;'} for c in ['gp-gallery', 'gp-cart', 'gp-content']]
    have = json.dumps(wp.req('wp-abilities/v1/abilities/elementor/read-resource/run?input[uri]=elementor://global-classes'))
    ops = [o for o in ops if o['label'] not in have]
    if ops: wp.ability('elementor/manage-classes', {'operations': ops})
    r = wp.ability('elementor/build-composition', {'post_id': tid, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('build', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w][:6])
    print('publish', wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': tid}), 'DELETE').get('status'))
    pid = C['wc_evtron']
    ops = [{'action': 'update', 'post_id': tid, 'conditions': ['include/product']},
           {'action': 'update', 'post_id': 145, 'conditions': ['include/singular/front_page', 'include/singular/page/141', 'include/product', f"include/singular/page/{C['about']}"]},
           {'action': 'update', 'post_id': C['snippet_woo'], 'conditions': ['include/singular/page/20', 'include/singular/page/21', 'include/singular/page/22', 'include/product']}]
    print([x.get('conditions') for x in wp.ability('elementor/manage-site-parts', {'operations': ops})['results']])
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
