"""Busy Bee offer popups (Elementor Pro popup templates). Opened by the offer cards on the home page and, for the
winter-tires popup, automatically once per session after scrolling 650px on screens ≥901px (bb.js)."""
import json
import el
from common import *

POPUPS = [  # key, image, theme, tag, title, benefit, detail, cta
    ('popup_tires', 'winter-tire-change-calgary', 'tires', 'CALGARY · WINTER READY', 'New season.<br>Right tires.', None,
     'Seasonal tire changes, balancing and tire checks. Get your car ready for the road ahead.', 'Book your tire change'),
    ('popup_oil', 'mobil-1-synthetic-oil-change-calgary', 'oil', 'MOBIL 1 SYNTHETIC OIL CHANGE', 'FROM $75',
     'Includes a complimentary vehicle inspection',
     'Mobil 1 synthetic oil change with a complimentary vehicle inspection. Final pricing depends on your vehicle. Confirm your '
     'quote with our team before booking.', 'Book an oil change'),
    ('popup_battery', 'battery-alternator-service-calgary', 'battery', 'BATTERY TESTING', 'FREE', 'Battery test + charging-system check',
     'Free battery testing and a charging-system check. Find out how your battery is performing before colder Calgary mornings. '
     'Any recommended repairs are quoted separately.', 'Get your battery checked'),
]

SETTINGS = {
    'width': px(520), 'width_mobile': cu('calc(100vw - 32px)'), 'height_type': 'auto', 'content_position': 'center',
    'horizontal_position': 'center', 'vertical_position': 'center', 'overlay': 'yes',
    'overlay_background_background': 'classic', 'overlay_background_color': 'rgba(0,0,0,0.8)',
    'close_button': 'yes', 'close_button_position': 'inside', 'close_button_vertical': pct(2.3), 'close_button_horizontal': pct(2.3),
    'close_button_color': '#182124', 'close_button_background_color': '#FFFFFF', 'icon_size': px(16),
    'entrance_animation': 'fadeIn', 'entrance_animation_duration': px(0.2, 'px'), 'border_radius': dims(10),
    'background_background': 'classic', 'background_color': '#182124', 'padding': dims(0),
    'box_shadow_box_shadow_type': 'yes', 'box_shadow_box_shadow': shadow(0, 10, 15, -3, 'rgba(0,0,0,0.1)'),
    'prevent_scroll': 'yes', 'avoid_multiple_popups': 'yes',
}


def popup(key, img_key, theme, tag, title, benefit, detail, cta):
    tires = theme == 'tires'
    copy = [H(tag, 'small', YEL, S(10 if tires else 11, 750, 15 if tires else 16.5, 1 if tires else 1.32), mar=(0, 0, 10, 0), name='Tag')]
    if tires:
        copy.append(H(title, 'h2', PAPER, S(48, 800, 1.02, -2.16, 'uppercase', size_m=34, ls_m=-1.53), name='Title'))
    else:
        copy += [H(title, 'h2', YEL, S(88, 900, 88, -5.28, size_m=64, lh_m=64, ls_m=-3.84), name='Title'),
                 H(benefit, 'span', PAPER, S(20, 750, 27, size_m=16, lh_m=21.6), mar=(12, 0, 0, 0), w=350, name='Benefit')]
    copy += [T(f'<p>{detail}</p>', PAPER, S(13, 400, 20.8, size_m=11, lh_m=17.6), mar=(14, 0, 0, 0), w=370, name='Detail'),
             BTN(cta, TEL, S(12, 750, 18), color='#172024' if not tires else '#182124', bg=YEL, ic='arrow-up-right', ic_size=18,
                 ic_gap=10, pad=(13, 17) if tires else (12, 16), radius=4, mar=(20, 0, 0, 0), mar_mobile=(12, 0, 0, 0), name='CTA')]
    side = 32 if tires else 26
    return [C('Offer', [
        IMG('busy-bee-auto-repair-logo', w=115, h=44, fit='contain', alt='Busy Bee Auto Repair', name='Logo', pos={'x': 32, 'y': 26},
            cls='bb-offer-logo', width_mobile=px(90), height_mobile=px(34)),
        C('Copy', copy, ai='flex-start', pos={'x': side, 'y': 30 if tires else 26, 'v': 'end'}, w=cu(f'calc(100% - {side * 2}px)'), z=1),
    ], bgimg=img_key, bgpos='center center' if tires else 'center 25%', bg='#182124', ov=True,
        cls=f'bb-offer bb-popup-card bb-offer-{theme}')]


if __name__ == '__main__':
    ids = json.load(open('ids.json'))
    for p in POPUPS:
        el.seed(p[0])
        el.save('elementor_library', ids[p[0]], popup(*p), page_settings=SETTINGS,
                )
        el.regen(ids[p[0]])
