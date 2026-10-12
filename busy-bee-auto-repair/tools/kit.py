"""Busy Bee Elementor kit (active kit = post 17). Writes the FULL settings set through MCP so kit CSS regenerates.
Backup of the original AutoWorks kit: wp-backup/kit_17_autoworks.json"""
import json, wp
from el import px, dims

KIT_ID = 17
INK, BEE, PAPER, PITCH = '#1A2024', '#F7D710', '#FFFFFF', '#010101'

colors_sys = [
    {'_id': 'primary', 'title': 'Ink', 'color': INK},
    {'_id': 'secondary', 'title': 'Bee', 'color': BEE},
    {'_id': 'text', 'title': 'Body text', 'color': '#020618'},
    {'_id': 'accent', 'title': 'Bright yellow', 'color': '#FFE600'},
]
colors_custom = [
    {'_id': 'bbpaper', 'title': 'Paper', 'color': PAPER},
    {'_id': 'bbpitch', 'title': 'Pitch', 'color': PITCH},
    {'_id': 'bbsoft', 'title': 'Bee soft', 'color': '#FCF5DB'},
    {'_id': 'bbgrey', 'title': 'Line grey', 'color': '#E5E8EA'},
    {'_id': 'bbdark', 'title': 'Dark', 'color': '#1B2225'},
    {'_id': 'bbcard', 'title': 'Card dark', 'color': '#192024'},
    {'_id': 'bbwa', 'title': 'WhatsApp', 'color': '#128C50'},
]
# System typography carries no font family on purpose: widgets either set Manrope explicitly or inherit the
# design's system font stack from <body> (set in the "Busy Bee – Styles" custom code).
typo_sys = [
    {'_id': 'primary', 'title': 'Primary'}, {'_id': 'secondary', 'title': 'Secondary'},
    {'_id': 'text', 'title': 'Text'}, {'_id': 'accent', 'title': 'Accent'},
]
typo_custom = [
    {'_id': 'bbdisplay', 'title': 'Display (Manrope 800)', 'typography_typography': 'custom', 'typography_font_family': 'Manrope', 'typography_font_weight': '800', 'typography_text_transform': 'uppercase'},
    {'_id': 'bbbody', 'title': 'Body (Manrope 400)', 'typography_typography': 'custom', 'typography_font_family': 'Manrope', 'typography_font_weight': '400'},
]

settings = {
    'system_colors': colors_sys, 'custom_colors': colors_custom,
    'system_typography': typo_sys, 'custom_typography': typo_custom,
    'default_generic_fonts': 'Sans-serif',
    'site_name': 'Busy Bee Auto Repair',
    'site_description': 'Auto repair in NE Calgary',
    'default_page_template': 'elementor_header_footer',
    'page_title_selector': 'h1.entry-title',
    'viewport_md': 768, 'viewport_lg': 1024, 'viewport_mobile': 767, 'viewport_tablet': 1023,
    'container_width': px(1152),
    'container_padding': dims(0),
    'space_between_widgets': {'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px', 'size': 0},
    'body_background_background': 'classic', 'body_background_color': PAPER,
    'body_color': '#020618',
    'lightbox_enable_counter': 'yes',
    'colors_enable_styleguide_preview': 'yes',
    'activeItemIndex': 1,
}

if __name__ == '__main__':
    r = wp.post(f'wp/v2/elementor_library/{KIT_ID}', {'meta': {'_elementor_page_settings': settings}})
    print('rest', r.get('id'))
    print(json.dumps(wp.mcp('elementor/update-page-settings', {'post_id': KIT_ID, 'settings': settings}))[:200])
    g = wp.get('elementor/v1/globals')
    print({k: v['value'] for k, v in g['colors'].items()})
