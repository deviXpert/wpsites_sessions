"""Charging cables range (client, 22 Nov 2026): 32A 7.4kW Type 2 to Type 2 cable in 5/10/15/20m.
Creates the 'Charging cables' category, adds 15m/20m to the Cable length attribute, the variable product,
menu items (main: Cables; footer: Charging cables) and a cross-sell from Fox Untethered (needs your own cable).
Specs beyond the client's product title stay out until the client sends the cable's datasheet.
Run: EVTRON_WP_USER=<admin login> python3 build_wc_cables.py"""
import json

import wp
from build_wc_products import find, term, product, att_len

C = json.load(open('created.json'))
M = json.load(open('media.json'))
W = 'wc/v3/'

if 'render_cable' not in M:
    M['render_cable'] = wp.upload('../assets/renders/type2-cable-render.webp', 'Type 2 to Type 2 EV charging cable', 'Type 2 to Type 2 EV charging cable')['id']
    json.dump(M, open('media.json', 'w'), indent=1)

cat = term('products/categories', 'Charging cables', 'charging-cables', description='Type 2 EV charging cables.')
for n, s in [('15 metres', '15m'), ('20 metres', '20m')]:
    term(f"products/attributes/{att_len['id']}/terms", n, s)

LENS = [('5 metres', '113.99', '5M'), ('10 metres', '152.99', '10M'), ('15 metres', '259.99', '15M'), ('20 metres', '313.99', '20M')]
desc = ('<p>A Type 2 to Type 2 charging cable rated at 32A, for charging at up to 7.4kW on a single-phase supply. Use it with untethered home chargers '
        'and public chargers that have a Type 2 socket.</p>'
        '<ul><li>Type 2 connector at both ends</li><li>Rated at 32A, up to 7.4kW single-phase</li><li>Four lengths: 5, 10, 15 or 20 metres</li></ul>'
        '<p>Not sure which length you need? Measure from the charger or socket to your car’s charging port, allowing a little slack. Email sales@evtron.co.uk and we’ll help.</p>')
cab = product('type-2-ev-charging-cable', {
    'name': '32A 7.4kW Type 2 to Type 2 EV Charging Cable', 'type': 'variable', 'status': 'publish', 'sku': 'EVT-CAB-T2T2-32A', 'tax_status': 'none',
    'categories': [{'id': cat['id']}], 'images': [{'id': M['render_cable']}], 'description': desc,
    'short_description': '<p>Type 2 to Type 2 charging cable, rated at 32A for up to 7.4kW single-phase charging. Available in 5, 10, 15 and 20 metres.</p>',
    'attributes': [{'id': att_len['id'], 'variation': True, 'visible': True, 'options': [l for l, _, _ in LENS]}],
    'default_attributes': [{'id': att_len['id'], 'option': '5 metres'}]})
have = {v['sku']: v['id'] for v in find(f"products/{cab['id']}/variations")}
batch = {'create': [], 'update': []}
for l, price, ls in LENS:
    sku = f'EVT-CAB-T2T2-32A-{ls}'
    v = {'sku': sku, 'regular_price': price, 'tax_status': 'none', 'attributes': [{'id': att_len['id'], 'option': l}]}
    (batch['update'].append({'id': have[sku], **v}) if sku in have else batch['create'].append(v))
r = wp.req(f"{W}products/{cab['id']}/variations/batch", 'POST', batch)
print('cable', cab['id'], cab['permalink'], len(r.get('create', [])), 'created', len(r.get('update', [])), 'updated')
wp.req(f"{W}products/{C['wc_foxu']}", 'PUT', {'cross_sell_ids': [cab['id']], 'upsell_ids': [cab['id']]})

# Menus: main "Cables" after Chargers; footer chargers group gets the cable too
url = cab['permalink']
existing = {(it['menus'], it['url']) for m in (18, 19) for it in wp.all(f'wp/v2/menu-items?menus={m}')}
if (18, url) not in existing:
    wp.req('wp/v2/menu-items', 'POST', {'title': 'Cables', 'url': url, 'menus': 18, 'menu_order': 5, 'status': 'publish', 'type': 'custom'})
if (19, url) not in existing:
    wp.req('wp/v2/menu-items', 'POST', {'title': 'Type 2 charging cable', 'url': url, 'menus': 19, 'menu_order': 9, 'status': 'publish', 'type': 'custom'})
order = {'Chargers': 1, 'Cables': 5, 'Installation': 6, 'FAQs': 7, 'About': 8, 'Contact': 9}
for it in wp.all('wp/v2/menu-items?menus=18'):
    t = it['title']['rendered']
    if it['parent'] == 0 and t in order:
        wp.req(f"wp/v2/menu-items/{it['id']}", 'POST', {'menu_order': order[t]})
C.update({'wc_cat_cables': cat['id'], 'wc_cable': cab['id']})
json.dump(C, open('created.json', 'w'), indent=1)
print([(it['title']['rendered'], it['parent']) for it in sorted(wp.all('wp/v2/menu-items?menus=18'), key=lambda x: x['menu_order'])])
