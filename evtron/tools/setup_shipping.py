"""WooCommerce delivery (client, 23 Nov 2026): free UK delivery on chargers.
Cable delivery charge not given yet, so cables also ship free until the client sets a price (change the 'cables' class cost then).
Idempotent. Run: EVTRON_WP_USER=<admin login> python3 setup_shipping.py"""
import json

import wp

W = 'wc/v3/'
C = json.load(open('created.json'))

wp.req(W + 'settings/general/woocommerce_ship_to_countries', 'PUT', {'value': ''})          # ship to all selling countries (GB)
zone = next((z for z in wp.req(W + 'shipping/zones') if z['name'] == 'United Kingdom'), None) or wp.req(W + 'shipping/zones', 'POST', {'name': 'United Kingdom', 'order': 0})
wp.req(f"{W}shipping/zones/{zone['id']}/locations", 'PUT', [{'code': 'GB', 'type': 'country'}])
methods = wp.req(f"{W}shipping/zones/{zone['id']}/methods")
if not any(m['method_id'] == 'free_shipping' for m in methods):
    wp.req(f"{W}shipping/zones/{zone['id']}/methods", 'POST', {'method_id': 'free_shipping', 'settings': {'title': 'Free UK delivery', 'requires': ''}})
print('zone', zone['id'], [(m['method_id'], m['title'], m['enabled']) for m in wp.req(f"{W}shipping/zones/{zone['id']}/methods")])
