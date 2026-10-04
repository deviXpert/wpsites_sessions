"""Publish the redesign LIVE: site-wide header/footer templates + every page body into its ORIGINAL page ID (URLs unchanged) + Yoast meta.
usage: python3 golive.py [page names...]   (no args = templates + all pages)"""
import json, sys, importlib, wp
from lib import header, footer
PAGES = {'home': 39107, 'about': 611, 'services': 673, 'languages': 633, 'samples': 988, 'career': 693, 'contact': 706, 'order': 319}
HOME_SEO = ('Professional & Certified Translation Services | Pak Translations',
            'PhD-led translation company: certified document translation, localization, transcription, subtitling & interpreting in 120+ languages. Free quote.',
            'professional translation services')
names = sys.argv[1:] or list(PAGES)
if not sys.argv[1:]:
    print('header', wp.req('wp/v2/elementor_library/33', 'POST', {'meta': {'_elementor_data': json.dumps([header()]), '_elementor_edit_mode': 'builder'}}).get('id'))
    print('footer', wp.req('wp/v2/elementor_library/37', 'POST', {'meta': {'_elementor_data': json.dumps([footer()]), '_elementor_edit_mode': 'builder'}}).get('id'))
    print('header conditions', wp.req('elementor/v1/site-editor/templates-conditions/33', 'POST', {'conditions': [{'type': 'include', 'name': 'general', 'sub_name': '', 'sub_id': ''}]}))
seo = []
for n in names:
    mod = importlib.import_module(n)
    r = wp.req(f'wp/v2/pages/{PAGES[n]}', 'POST', {'template': 'elementor_header_footer', 'status': 'publish',
        'meta': {'_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page', '_elementor_data': json.dumps(mod.build()),
                 'ast-site-content-layout': 'full-width-container', 'site-content-layout': 'page-builder', 'site-sidebar-layout': 'no-sidebar',
                 'site-content-style': 'unboxed', 'site-sidebar-style': 'unboxed', 'site-post-title': 'disabled'}})
    print(n, r.get('id'), r.get('link'), r.get('_err') or '')
    t, d, k = HOME_SEO if n == 'home' else mod.SEO
    seo.append({'id': PAGES[n], 'seo_title': t, 'meta_description': d, 'focus_keyphrase': k})
r = wp.req('yoast/v1/bulk_editor/update_search', 'POST', {'items': seo})
print('yoast', [x.get('success') for x in r.get('results', [])] or r)
for n in names: wp.req(f'wp/v2/pages/{PAGES[n]}', 'POST', {'status': 'publish'})   # re-save so Yoast refreshes indexables
print('cache clear', wp.req('elementor/v1/cache', 'DELETE'))
