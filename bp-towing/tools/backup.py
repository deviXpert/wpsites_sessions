import wp, json, os
os.makedirs('wp-backup', exist_ok=True)
def save(n, d): json.dump(d, open(f'wp-backup/{n}.json', 'w'), indent=1)
save('pages', wp.all('wp/v2/pages?context=edit&status=publish,draft,private,pending'))
save('posts', wp.all('wp/v2/posts?context=edit&status=publish,draft,private'))
save('elementor_library', wp.all('wp/v2/elementor_library?context=edit&status=publish,draft,private'))
save('media', wp.all('wp/v2/media?context=edit'))
for k in ['menus', 'menu-items', 'settings', 'plugins', 'themes', 'templates', 'template-parts']:
    save(k, wp.all(f'wp/v2/{k}?context=edit') if k not in ('settings',) else wp.req('wp/v2/settings'))
