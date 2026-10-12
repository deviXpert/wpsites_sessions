"""Create/refresh the Busy Bee nav menus (idempotent). Records menu slugs/ids in ids.json."""
import json, wp

MENUS = {
    'bb-desktop': ('Busy Bee – Desktop', [('Services', '/#services'), ('Pricing', '/#pricing'), ('Brands', '/#vehicle-brands'),
                                          ('Why us', '/#why-busy-bee'), ('Reviews', '/#reviews'), ('FAQ', '/#faq')]),
    'bb-mobile': ('Busy Bee – Mobile', [('Services', '/#services'), ('Pricing', '/#pricing'), ('Why us', '/#why-busy-bee'),
                                        ('Reviews', '/#reviews'), ('FAQ', '/#faq'), ('Book appointment', '/#book', 'bb-menu-cta')]),
}

if __name__ == '__main__':
    ids = json.load(open('ids.json'))
    existing = {m['slug']: m for m in wp.get('wp/v2/menus')}
    for slug, (name, items) in MENUS.items():
        m = existing.get(slug) or wp.post('wp/v2/menus', {'name': name, 'slug': slug})
        mid = m['id']
        for it in wp.get(f'wp/v2/menu-items?menus={mid}&per_page=100'):
            wp.req('DELETE', f'wp/v2/menu-items/{it["id"]}?force=true')
        for i, it in enumerate(items):
            body = {'title': it[0], 'url': it[1], 'type': 'custom', 'menus': mid, 'menu_order': i + 1, 'status': 'publish'}
            if len(it) > 2:
                body['classes'] = [it[2]]
            wp.post('wp/v2/menu-items', body)
        ids['menu_' + slug] = mid
        print(slug, mid, len(items))
    json.dump(ids, open('ids.json', 'w'), indent=1)
