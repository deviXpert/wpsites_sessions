"""Snapshot of the live site before the redesign -> ../backup/"""
import json, os, wp
B = os.path.join(os.path.dirname(__file__), '..', 'backup'); os.makedirs(B, exist_ok=True)
def save(n, d): json.dump(d, open(os.path.join(B, n + '.json'), 'w'), indent=1); print(n, len(d) if isinstance(d, list) else 'obj')
save('pages', wp.all('wp/v2/pages?context=edit&status=any'))
save('posts', wp.all('wp/v2/posts?context=edit&status=any'))
save('elementor_library', wp.all('wp/v2/elementor_library?context=edit&status=any'))
save('menus', wp.all('wp/v2/menus?context=edit'))
save('menu-items', wp.all('wp/v2/menu-items?context=edit'))
save('settings', wp.req('wp/v2/settings'))
save('plugins', wp.req('wp/v2/plugins'))
save('themes', wp.req('wp/v2/themes'))
save('media', wp.all('wp/v2/media?context=edit'))
save('blocks', wp.all('wp/v2/blocks?context=edit'))
