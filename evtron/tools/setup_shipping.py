"""WooCommerce delivery (client, 23 Nov 2026): chargers delivered free; cables £4.95.
UK zone with one Flat rate method: base £0, 'Cables' shipping class £4.95, charged once per order ('order' type = most expensive class).
Idempotent. Run: EVTRON_WP_USER=<admin login> python3 setup_shipping.py"""
import json

import wp

W = 'wc/v3/'
C = json.load(open('created.json'))
CABLE_DELIVERY = '4.95'

wp.req(W + 'settings/general/woocommerce_ship_to_countries', 'PUT', {'value': ''})
cls = next((c for c in wp.req(W + 'products/shipping_classes') if c['slug'] == 'cables'), None) \
    or wp.req(W + 'products/shipping_classes', 'POST', {'name': 'Cables', 'slug': 'cables', 'description': 'Charging cables: £4.95 delivery'})
wp.req(f"{W}products/{C['wc_cable']}", 'PUT', {'shipping_class': 'cables'})
for v in wp.req(f"{W}products/{C['wc_cable']}/variations?per_page=50"):
    wp.req(f"{W}products/{C['wc_cable']}/variations/{v['id']}", 'PUT', {'shipping_class': 'cables'})

zone = next((z for z in wp.req(W + 'shipping/zones') if z['name'] == 'United Kingdom'), None) or wp.req(W + 'shipping/zones', 'POST', {'name': 'United Kingdom', 'order': 0})
wp.req(f"{W}shipping/zones/{zone['id']}/locations", 'PUT', [{'code': 'GB', 'type': 'country'}])
methods = wp.req(f"{W}shipping/zones/{zone['id']}/methods")
for m in methods:
    if m['method_id'] == 'free_shipping':
        wp.req(f"{W}shipping/zones/{zone['id']}/methods/{m['instance_id']}?force=true", 'DELETE')
flat = next((m for m in methods if m['method_id'] == 'flat_rate'), None)
settings = {'title': 'UK delivery', 'tax_status': 'none', 'cost': '0', f"class_cost_{cls['id']}": CABLE_DELIVERY, 'no_class_cost': '0', 'type': 'order'}
if flat:
    wp.req(f"{W}shipping/zones/{zone['id']}/methods/{flat['instance_id']}", 'PUT', {'settings': settings, 'enabled': True})
else:
    wp.req(f"{W}shipping/zones/{zone['id']}/methods", 'POST', {'method_id': 'flat_rate', 'settings': settings})
print('zone', zone['id'], 'class', cls['id'], [(m['method_id'], m['title'], m['enabled']) for m in wp.req(f"{W}shipping/zones/{zone['id']}/methods")])
