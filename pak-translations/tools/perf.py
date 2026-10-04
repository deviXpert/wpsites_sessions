"""Site-wide performance settings (PageSpeed). Safe to re-run.
- Kit 26951: global typography font families cleared (Elementor no longer enqueues Google Fonts; pt.css sets fonts),
  custom CSS = fonts.css (@font-face + metric-matched fallbacks, prints in <head>).
- Elementor options via elementor/v1/settings (see SETTINGS).  Original kit settings: wp-backup/kit-26951-page-settings.json
usage: python3 perf.py"""
import os, wp
D = os.path.dirname(os.path.abspath(__file__))
KIT = 26951
SETTINGS = {
    'elementor_font_display': 'swap',
    'elementor_css_print_method': 'internal',   # inline Elementor CSS in <head> instead of separate files
    'elementor_experiment-e_font_icon_svg': 'active',   # icons as inline SVG: no Font Awesome / eicons CSS + font files
    'elementor_optimized_image_loading': '1',           # lazy-load below-the-fold images, correct fetchpriority
    'elementor_experiment-e_lazyload': 'active',        # lazy-load background images
}

ps = wp.req(f'wp/v2/elementor_library/{KIT}?context=edit')['meta']['_elementor_page_settings']
for grp in ('system_typography', 'custom_typography'):
    for t in ps.get(grp, []): t.pop('typography_font_family', None)
ps['custom_css'] = open(os.path.join(D, 'fonts.css')).read()
print('kit', wp.req(f'wp/v2/elementor_library/{KIT}', 'POST', {'meta': {'_elementor_page_settings': ps}}).get('id'))
for k, v in SETTINGS.items():
    print(k, wp.req(f'elementor/v1/settings/{k}', 'POST', {'value': v}).get('success'))
print('cache clear', wp.req('elementor/v1/cache', 'DELETE'))
