"""WooCommerce catalogue (client info + 19 Nov feedback). Idempotent: finds by slug/SKU before creating.
- EV-Tron Tethered: variable product, Colour x Cable length (5m / 7.5m free upgrade / 10m +£80), base £595.
- Add-ons (hidden from the catalogue, bought via the configurator): 5-year warranty, CT clamp, black post, steel post.
- Fox ESS Tethered / Untethered: partner brand, published 21 Nov 2026 (general product template).
Prices are what the client gave; the client is not VAT registered, so products are tax_status none for now.
Run: EVTRON_WP_USER=<admin login> python3 build_wc_products.py"""
import json

import wp

C = json.load(open('created.json'))
M = json.load(open('media.json'))
W = 'wc/v3/'


def find(path, **q):
    qs = '&'.join(f'{k}={v}' for k, v in q.items())
    r = wp.req(f'{W}{path}?{qs}&per_page=100')
    return r if isinstance(r, list) else []


def term(path, name, slug, **extra):
    hit = [t for t in find(path) if t['slug'] == slug]
    return hit[0] if hit else wp.req(W + path, 'POST', {'name': name, 'slug': slug, **extra})


cat_ev = term('products/categories', 'EV chargers', 'ev-chargers', description='Home EV chargers, supplied and fitted.')
cat_acc = term('products/categories', 'Accessories', 'accessories')
att_col = term('products/attributes', 'Colour', 'pa_colour', type='select', order_by='menu_order')
att_len = term('products/attributes', 'Cable length', 'pa_cable-length', type='select', order_by='menu_order')
for n, s in [('Mythos Black', 'mythos-black'), ('Space Grey', 'space-grey'), ('Midnight Green', 'midnight-green'), ('Crimson Red', 'crimson-red'),
             ('Black', 'black'), ('Blue', 'blue'), ('Purple', 'purple'), ('Pink', 'pink'), ('White', 'white')]:
    term(f"products/attributes/{att_col['id']}/terms", n, s)
for n, s in [('5 metres', '5m'), ('7.5 metres', '7-5m'), ('10 metres', '10m')]:
    term(f"products/attributes/{att_len['id']}/terms", n, s)

ASTRA = [{'key': 'ast-site-content-layout', 'value': 'full-width-container'}, {'key': 'site-sidebar-layout', 'value': 'no-sidebar'},
         {'key': 'site-content-style', 'value': 'unboxed'}]


def product(slug, data):
    hit = [p for p in find('products', slug=slug, status='any')]
    if hit:
        return wp.req(f"{W}products/{hit[0]['id']}", 'PUT', data)
    return wp.req(W + 'products', 'POST', {'slug': slug, **data})


# ---------- Add-ons ----------
ADDONS = [('evtron-extended-warranty-5-years', 'EV-Tron extended warranty (5 years in total)', 'EVT-WAR-5Y', '89.99', True,
           'Extends the standard 3-year EV-Tron warranty by 2 years, to 5 years in total. Bought with an EV-Tron charger.'),
          ('ct-clamp', 'CT clamp', 'EVT-ACC-CT', '15', False, 'Current transformer clamp that measures your home’s demand, for load balancing.'),
          ('black-charging-post', 'Black charging post', 'EVT-ACC-POST-BLK', '200', False, 'Free-standing black post for drives without a suitable wall.'),
          ('steel-charging-post', 'Steel charging post', 'EVT-ACC-POST-STL', '280', False, 'Free-standing brushed steel post for drives without a suitable wall.')]
addon_ids = []
for slug, name, sku, price, virtual, desc in ADDONS:
    r = product(slug, {'name': name, 'type': 'simple', 'status': 'publish', 'sku': sku, 'regular_price': price, 'virtual': virtual,
                       'catalog_visibility': 'hidden', 'tax_status': 'none', 'categories': [{'id': cat_acc['id']}], 'short_description': desc})
    addon_ids.append(r['id']); print('addon', r['id'], name)

# ---------- EV-Tron Tethered ----------
COLS = [('Mythos Black', 'render_evtron', 'BLK'), ('Space Grey', 'render_evtron_grey', 'GRY'), ('Midnight Green', 'render_evtron_green', 'GRN'), ('Crimson Red', 'render_evtron_red', 'RED')]
LENS = [('5 metres', '595', '5M'), ('7.5 metres', '595', '7M5'), ('10 metres', '675', '10M')]
desc = ('<p>EV-Tron Tethered is our own 7kW smart home charger, with a tethered Type 2 cable and four finishes: Mythos Black, Space Grey, Midnight Green and Crimson Red.</p>'
        '<p>Control it from your phone over Wi-Fi or Bluetooth, schedule charging for cheaper off-peak hours, tap an RFID card to start, and adjust the charging current to suit your home. '
        'It is IP65 rated for indoor or outdoor installation, with built-in over- and under-voltage, over-current, 30mA leakage and over-temperature protection.</p>'
        '<p>Installed by qualified electricians after a free remote survey.</p>')
evt = product('evtron-tethered-ev-charger', {
    'name': 'EV-Tron Tethered 7kW Home EV Charger', 'type': 'variable', 'status': 'publish', 'sku': 'EVT-EMS3-70-C', 'tax_status': 'none',
    'categories': [{'id': cat_ev['id']}], 'short_description': '<p>7kW smart home charger with a tethered Type 2 cable. App control over Wi-Fi and Bluetooth, scheduling, RFID and IP65.</p>',
    'description': desc, 'weight': '3.5', 'dimensions': {'length': '27.4', 'width': '20.4', 'height': ''},
    'images': [{'id': M[k]} for _, k, _ in COLS],
    'attributes': [{'id': att_col['id'], 'variation': True, 'visible': True, 'options': [c for c, _, _ in COLS]},
                   {'id': att_len['id'], 'variation': True, 'visible': True, 'options': [l for l, _, _ in LENS]}],
    'default_attributes': [{'id': att_col['id'], 'option': 'Mythos Black'}, {'id': att_len['id'], 'option': '7.5 metres'}],
    'cross_sell_ids': addon_ids, 'meta_data': ASTRA})
print('evtron', evt['id'], evt.get('permalink'))
have = {v['sku']: v['id'] for v in find(f"products/{evt['id']}/variations")}
batch = {'create': [], 'update': []}
for c, k, cs in COLS:
    for l, price, ls in LENS:
        sku = f'EVT-EMS3-70-C-{cs}-{ls}'
        v = {'sku': sku, 'regular_price': price, 'tax_status': 'none', 'image': {'id': M[k]}, 'weight': '3.5',
             'attributes': [{'id': att_col['id'], 'option': c}, {'id': att_len['id'], 'option': l}]}
        (batch['update'].append({'id': have[sku], **v}) if sku in have else batch['create'].append(v))
r = wp.req(f"{W}products/{evt['id']}/variations/batch", 'POST', batch)
print('variations', len(r.get('create', [])), 'created', len(r.get('update', [])), 'updated')

# ---------- Fox ESS (partner brand) ----------
fox_note = '<p>Fox ESS is an independent brand, supplied and installed by EV-Tron. Solar charging depends on the model and your solar system.</p>'
foxt = product('fox-tethered-solar-ev-charger', {
    'name': 'Fox ESS Tethered Solar EV Charger', 'type': 'variable', 'status': 'publish', 'tax_status': 'none', 'categories': [{'id': cat_ev['id']}],
    'short_description': '<p>Solar-compatible 7kW tethered Type 2 charger from Fox ESS, an independent brand we supply and install. Price includes a standard installation.</p>',
    'images': [{'id': M['render_foxt']}], 'meta_data': ASTRA,
    'attributes': [{'id': att_col['id'], 'variation': True, 'visible': True, 'options': ['Black', 'Blue', 'Purple', 'Pink']}],
    'default_attributes': [{'id': att_col['id'], 'option': 'Black'}]})
have = {v['sku']: v['id'] for v in find(f"products/{foxt['id']}/variations")}
batch = {'create': [], 'update': []}
for c in ['Black', 'Blue', 'Purple', 'Pink']:
    sku = 'FOX-L-TETH-' + c[:3].upper()
    v = {'sku': sku, 'regular_price': '995', 'tax_status': 'none', 'attributes': [{'id': att_col['id'], 'option': c}]}
    (batch['update'].append({'id': have[sku], **v}) if sku in have else batch['create'].append(v))
wp.req(f"{W}products/{foxt['id']}/variations/batch", 'POST', batch)
foxu = product('fox-untethered-solar-ev-charger', {
    'name': 'Fox ESS Untethered Solar EV Charger', 'type': 'simple', 'status': 'publish', 'sku': 'FOX-A-UNTETH-WHT', 'regular_price': '945', 'tax_status': 'none',
    'categories': [{'id': cat_ev['id']}], 'images': [{'id': M['render_foxu']}], 'meta_data': ASTRA,
    'short_description': '<p>Solar-compatible 7kW untethered Type 2 socket charger from Fox ESS, an independent brand we supply and install. In white. Price includes a standard installation.</p>'})
print('fox', foxt['id'], foxu['id'])

C.update({'wc_cat_ev': cat_ev['id'], 'wc_cat_acc': cat_acc['id'], 'wc_evtron': evt['id'], 'wc_foxt': foxt['id'], 'wc_foxu': foxu['id'], 'wc_addons': addon_ids})
json.dump(C, open('created.json', 'w'), indent=1)
