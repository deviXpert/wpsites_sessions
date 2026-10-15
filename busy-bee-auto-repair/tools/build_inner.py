"""Shared site chrome pieces: the native Elementor Pro Mega Menu (used by the site header, template 79) and the phone-only
sticky Call bar (used by the site footer, template 74).  Running this file applies header 79 / footer 74 to the entire site."""
import json
import el
import wp
from common import *
from el import uid
from sitemap import SERVICE_PAGES, PAGES, URL

DK2 = '#192124'


# ---------------------------------------------------------------- mega menu (native Elementor Pro "Menu" widget)
def service_link(label, url, ic, summary):
    return C(label, [ICON(ic, 20, color=DK2, bg='#FFF5A8', box=40, radius=10, name='Icon', w='auto', cls='bb-sw16'),
                     C('Text', [H(label.replace('&', '&amp;'), 'span', DK2, S(14, 800, 20), name='Name'),
                                H(summary, 'span', '#667074', S(12, 400, 17), mar=(3, 0, 0, 0), name='Summary')], w='auto', grow=True,
                       cls='bb-shrink')],
             d='row', ai='flex-start', gap=12, pad=10, radius=10, href=url, cls='bb-mega-link')


def mega_panel():
    links = C('Service links', [service_link(l, u, ic, s) for _, l, u, ic, s, _ in SERVICE_PAGES],
              grid='repeat(3, minmax(0, 1fr))', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto',
              rows_mobile='auto', gap=4)
    feature = C('Help card', [
        H('NOT SURE WHAT’S WRONG?', 'p', YEL, S(10, 800, 15, 1.6), name='Eyebrow'),
        H('Book a diagnostic and get a clear answer.', 'p', PAPER, S(20, 800, 24, -0.4, 'uppercase'), mar=(10, 0, 14, 0), name='Title'),
        BTN('Book appointment', '#book', S(13, 800, 19.5), color=DK2, bg=YEL, ic='arrow-up-right', ic_size=16, pad=(12, 18), radius=6,
            name='Book'),
        H(PHONE, 'p', PAPER, S(14, 750, 21), href=TEL, mar=(14, 0, 0, 0), name='Phone'),
        H('All services ↗︎', 'p', YEL, S(12, 750, 18), href=URL['services'], mar=(18, 0, 0, 0), name='All services'),
    ], pad=24, bg=DK2, radius=12, hide='tm')
    return C('Services mega panel', [links, feature], grid='minmax(0, 1fr) 260px', grid_tablet='1fr', grid_mobile='1fr', rows='auto',
             rows_tablet='auto', rows_mobile='auto', gap=16, pad=16, pad_tablet=(4, 0), pad_mobile=(4, 0), bg=PAPER, radius=16,
             cls='bb-mega-panel')


def mega_menu(dark=False):
    items = [('Home', URL['home'], False), ('Services', URL['services'], True), ('About', URL['about'], False),
             ('Blog', URL['blog'], False), ('Contact', URL['contact'], False)]
    kids = []
    for title, url, drop in items:
        kids.append({'id': uid(), 'elType': 'container', 'isInner': True, 'elements': [mega_panel()] if drop else [],
                     'settings': {'content_width': 'full', '_title': title + ' dropdown'}})
    return {'id': uid(), 'elType': 'widget', 'widgetType': 'mega-menu', 'elements': kids, 'settings': {
        '_title': 'Main menu (mega)', 'menu_name': 'Main menu',
        'menu_items': [{'_id': uid(), 'item_title': t, 'item_link': {'url': u, 'is_external': '', 'nofollow': ''},
                        'item_dropdown_content': 'yes' if d else ''} for t, u, d in items],
        'open_on': 'hover', 'content_width': 'fit_to_content', 'content_horizontal_position': 'center', 'breakpoint_selector': 'tablet', 'item_layout': 'horizontal',
        'menu_toggle_icon_normal': icon('menu'), 'menu_toggle_icon_active': icon('x'),
        'menu_item_icon': icon('chevron-down'), 'menu_item_icon_active': icon('chevron-down'),
        '_css_classes': 'bb-mega' + (' bb-mega-dark' if dark else ''), '_flex_size': 'none'}}


# ---------------------------------------------------------------- phone call bar (lives in the site footer, template 74)
def callbar():
    """Phone-only sticky Call / Book bar (the SEO doc asks for a sticky tap-to-call button on mobile)."""
    return C('Mobile call bar', [
        BTN('Call ' + PHONE, TEL, S(14, 800, 20), color=DK2, bg=YEL, ic='phone', ic_pos='before', ic_size=16, pad=(14, 16), radius=30,
            name='Call', cls='bb-cb-call'),
        BTN('Book now', '#book', S(14, 800, 20), color=DK2, bg=PAPER, ic='calendar-days', ic_pos='before', ic_size=16, pad=(14, 16),
            radius=30, name='Book', cls='bb-cb-book'),
    ], d='row', gap=8, hide='dt', cls='bb-callbar')


def ensure_template(key, title, ttype):
    ids = json.load(open('ids.json'))
    if key not in ids:
        d = wp.post('wp/v2/elementor_library', {'title': title, 'status': 'publish',
                                                 'meta': {'_elementor_template_type': ttype, '_elementor_edit_mode': 'builder'}})
        ids[key] = d['id']
        json.dump(ids, open('ids.json', 'w'), indent=1)
    return ids[key]


def set_conditions(tid, conds):
    wp.req('PUT', f'elementor/v1/site-editor/templates-conditions/{tid}',
           {'conditions': [dict(type=t, name=n, sub_name=s, sub_id='') for t, n, s in conds]})


if __name__ == '__main__':
    # The site uses the home header (79) and footer (74) everywhere; retire the earlier inner header/footer templates.
    ids = json.load(open('ids.json'))
    for k in ('inner_header', 'inner_footer'):
        if k in ids:
            wp.req('DELETE', f"wp/v2/elementor_library/{ids.pop(k)}?force=true")
    json.dump(ids, open('ids.json', 'w'), indent=1)
    for t in (79, 74):
        set_conditions(t, [('include', 'general', '')])
