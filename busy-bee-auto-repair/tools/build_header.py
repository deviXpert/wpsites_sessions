"""Busy Bee header → Theme Builder header template (post 79, condition: entire site).
Desktop/tablet: dark top bar + floating pill nav.  Mobile (<768): favicon disc, address, call + menu toggle.
The whole header is absolutely positioned over the hero, as in the design."""
import json
import el
from common import *

HEADER_ID = 79


def topbar():
    item = lambda ic, txt, href, **kw: ILIST([(ic, txt, href)], inline=True, t=M(11, 700, 16.5), color=PAPER, ic_color=BEE,
                                             ic_size=12, gap_=8, name='Top bar – ' + txt, w='auto', **kw)
    return C('Top bar', [
        item('phone', PHONE, TEL),
        item('map-pin', '324 41 Ave NE, Calgary', MAPS),
        item('clock-3', 'Mon to Fri, 9 AM to 6 PM', None, hide='t'),
    ], d='row', jc='center', ai='center', gap=28, minh=36, pad=(0, 16), bg=INK, z=20)


def nav():
    logo = IMG('busy-bee-auto-repair-logo', w=146, w_tablet=None, href='/', alt='Busy Bee Auto Repair', name='Logo', cls='bb-logo',
               width_tablet=px(112))
    import build_inner
    menu = build_inner.mega_menu()
    menu['settings']['_css_classes'] += ' bb-mega-home'
    book = BTN('Book now', BOOK, M(15, 800, 20, size_t=14, lh_t=20), color=INK, bg=BEE, ic='arrow-up-right', ic_gap=12,
               pad=(7, 7, 7, 22), radius=PILL, border=(1, BEE), sh=SH_BEE, hover_bg=INK, hover_color=PAPER, hover_border=INK,
               name='Book now', cls='bb-booknow')
    book['settings']['icon_size'] = px(16)
    return C('Nav pill', [logo, menu, book], d='row', jc='space-between', ai='center', gap=16,
             w=cu('min(1440px, 100vw - 64px)'), w_tablet=cu('calc(100vw - 48px)'), minh=70, pad=(8, 20), pad_tablet=(12, 20),
             mar=(20, 'auto', 0, 'auto'), bg=PAPER, radius=PILL, border=(1, ink(0.05)), cls='bb-nav', tag='nav')


def mobile_header():
    fav = C('Home disc', [IMG('busy-bee-favicon', w=32, alt='Busy Bee Auto Repair', href='/', name='Favicon')],
            ai='center', jc='center', w=44, minh=44, bg=wht(0.9), radius=PILL, shadow=SH_SM, cls='bb-mfav')
    addr = ILIST([('map-pin', '324 41 Ave NE<br>Calgary', MAPS)], t=M(10, 700, 12.5, tt='uppercase'), color=PAPER, ic_color=PAPER,
                 ic_size=16, gap_=8, name='Address', align='center', grow=True, cls='bb-maddr')
    call = ICON('phone', size=16, color=PAPER, bg=INK, box=40, href=TEL, name='Call', cls='bb-mcall')
    import build_inner
    menu = build_inner.mega_menu()
    menu['settings']['_css_classes'] += ' bb-mega-home bb-mmenu'
    right = C('Actions', [call, menu], d='row', ai='center', gap=4, w='auto')
    return C('Mobile header', [fav, addr, right], d='row', ai='center', gap=8, minh=80, pad=(0, 16), cls='bb-mhead', hide='dt')


def build():
    el.seed('header')
    root = C('Header', [
        C('Desktop header', [topbar(), nav()], hide='m'),
        mobile_header(),
    ], tag='header', cls='bb-header', pos={'x': 0, 'y': 0}, z=50, w=pct(100))
    return el.book_popup([root], json.load(open('ids.json'))['popup_book'])


if __name__ == '__main__':
    data = build()
    el.save('elementor_library', HEADER_ID, data, extra={'title': 'Busy Bee – Header'})
    el.regen(HEADER_ID)
