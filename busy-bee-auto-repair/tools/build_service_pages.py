"""The 11 service pages (URLs, copy and SEO from design/content-seo.md), built in the /services/ design language:
hero (inner header floats over it) → page sections → why-us strip → request form → FAQ (FAQPage schema) → related services →
location → reviews.  Every page links to 2–3 related services, the services hub and the booking popup.
Usage: python3 build_service_pages.py [key …]   (no args = all pages)"""
import json, sys
import el, wp
from build_globals import tpl
import build_home as home
import build_services as svc
from common import *
from sitemap import SERVICE_PAGES
from service_content import PAGES

DK2 = svc.DK2
META = {k: dict(label=l, url=u, icon=ic, summary=sm, photo=ph) for k, l, u, ic, sm, ph in SERVICE_PAGES}


def wrap(name, kids, **kw):
    kw.setdefault('pad', (60, 32))
    kw.setdefault('pad_mobile', (40, 22))
    return C(name, kids, tag='section', w=cu('min(1300px, 100%)'), mar=(0, 'auto'), cls='bb-sys ' + kw.pop('cls', ''), **kw)


def sec_list(head, em, items):
    cards = [C(t, [ICON('check', 18, color=DK2, bg=YEL, box=32, radius=8, name='Tick', w='auto'),
                   C('Text', [H(t, 'h3', DK2, S(15, 800, 21, tt='uppercase'), name='Title')] +
                     ([H(d, 'p', '#667074', S(13, 400, 20), mar=(6, 0, 0, 0), name='Text')] if d else []), w='auto', grow=True,
                     cls='bb-shrink')],
               d='row', ai='flex-start', gap=14, pad=20, bg=PAPER, radius=10, border=(1, '#E4E7E3'), cls='bb-svc-item')
             for t, d in items]
    return wrap(head, [svc.title(head, em),
                       C('Grid', cards, grid='repeat(3, minmax(0, 1fr))', grid_tablet='repeat(2, minmax(0, 1fr))', grid_mobile='1fr',
                         rows='auto', rows_tablet='auto', rows_mobile='auto', gap=14)])


def sec_signs(head, items, photo, ic='triangle-alert'):
    left = C('Photo', [
        IMG(photo, w=pct(100), h=cu('100%'), fit='cover', alt='', name='Photo', cls='bb-sm-card-img'),
        C('Copy', [H('KNOW THE SIGNS' if ic != 'check' else 'WHAT YOU GET', 'p', YEL, S(11, 800, 16.5, 1.76), name='Eyebrow'),
                   H(head, 'h2', PAPER, S(34, 850, 1.08, -1.2, 'uppercase', size_m=28, ls_m=-0.8), mar=(12, 0, 0, 0), name='Title')],
          z=1),
    ], jc='flex-end', minh=380, minh_mobile=260, pad=34, pad_mobile=26, radius=12, ov=True, bg='#172024', cls='bb-sm-book-photo')
    lst = C('Checklist', [
        C(t[:30], [ICON('check' if ic == 'check' else 'circle-alert', 20, color=DK2 if ic == 'check' else '#B42318', name='Icon',
                        w='auto'),
                   H(t, 'p', DK2, S(15, 600, 23), name='Text', cls='bb-shrink')],
          d='row', ai='flex-start', gap=14, pad=(16, 0), border=(dims(0, 0, 1, 0), '#DCE0D0'))
        for t in items] + [BTN('Book an inspection', '#book', S(13, 800, 19.5), color=DK2, bg=YEL, ic='arrow-up-right', ic_size=16,
                               pad=(14, 22), radius=6, mar=(24, 0, 0, 0), name='Book')],
        pad=(30, 34), pad_mobile=(20, 22), bg='#F3F3E7', radius=12, jc='center')
    return wrap(head, [C('Grid', [left, lst], grid='0.9fr 1.1fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto',
                         rows_mobile='auto', gap=20)])


def sec_steps(head, em, items):
    def step(i, t, p):
        return C(t, [H(f'{i:02d}', 'span', '#939C98', S(12, 800, 18, 1.44), name='Number'),
                     H(t, 'h3', DK2, S(17, 800, 24, tt='uppercase'), mar=(10, 0, 10, 0), name='Title'),
                     H(p, 'p', '#667074', S(13, 400, 21), name='Text')], pad=(20, 0, 0, 0), border=(dims(2, 0, 0, 0), YEL))
    n = len(items)
    return wrap(head, [svc.title(head, em),
                       C('Steps', [step(i + 1, *s) for i, s in enumerate(items)], grid=f'repeat({n}, minmax(0, 1fr))',
                         grid_tablet='repeat(2, minmax(0, 1fr))', grid_mobile='1fr', rows='auto', rows_tablet='auto',
                         rows_mobile='auto', gap=24)])


def sec_text(head, paras, photo):
    return wrap(head, [C('Grid', [
        C('Copy', [H(head, 'h2', DK2, S(34, 850, 1.08, -1.2, 'uppercase', size_m=28, ls_m=-0.8), name='Title')] +
          [T(f'<p>{p}</p>', '#4B5558', S(15, 400, 26), mar=(16, 0, 0, 0), name='Text') for p in paras] +
          [C('Actions', [svc.yellow_btn('Call ' + PHONE, TEL, ic='phone', name='Call'),
                         BTN('Book online', '#book', S(13, 800, 19.5), color=DK2, bg='rgba(0,0,0,0)', pad=(14, 22), radius=6,
                             border=(1, DK2), hover_bg=DK2, hover_color=PAPER, name='Book')],
             d='row', wrap='wrap', gap=12, mar=(24, 0, 0, 0))],
          jc='center', pad=(10, 0)),
        IMG(photo, w=pct(100), h=cu('100%'), fit='cover', alt='', radius=12, name='Photo', cls='bb-fill-img'),
    ], grid='1fr 1fr', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto', rows_mobile='auto', gap=40, gap_mobile=24,
        ai='stretch')])


def sec_callout(head, text):
    return wrap(head, [C('Callout', [
        ICON('shield-check', 30, color=DK2, name='Icon', w='auto', cls='bb-sw16'),
        C('Copy', [H(head, 'h2', DK2, S(26, 850, 1.15, -0.8, 'uppercase', size_m=22), name='Title'),
                   T(f'<p>{text}</p>', DK2, S(15, 400, 25), mar=(10, 0, 0, 0), name='Text')], w='auto', grow=True, cls='bb-shrink'),
    ], d='row', d_mobile='column', ai='flex-start', gap=22, pad=(32, 36), pad_mobile=26, bg=YEL, radius=12)], pad=(30, 32),
        pad_mobile=(24, 22))


def sec_prices(head, rows):
    items = [{'_id': el.uid(), 'title': t, 'price': p, 'item_description': d, 'link': {'url': '#book'}} for t, p, d in rows]
    pl = W('price-list', 'Prices', price_list=items, heading_color=DK2, price_color=DK2, description_color='#667074',
           separator_style='dotted', separator_weight=px(2), separator_color='#C9CFC6', **{('heading_' + k): v for k, v in
                                                                                         S(17, 800, 24, tt='uppercase').items()},
           **{('price_' + k): v for k, v in S(20, 850, 26).items()}, **{('description_' + k): v for k, v in S(13, 400, 20).items()},
           cls='bb-price-list')
    return wrap(head, [C('Box', [H(head, 'h2', DK2, S(30, 850, 1.1, -1, 'uppercase', size_m=24), mar=(0, 0, 20, 0), name='Title'), pl,
                                 T('<p>Final pricing depends on your vehicle. You always approve the estimate before work starts.</p>',
                                   '#667074', S(12, 400, 19), mar=(14, 0, 0, 0), name='Note')],
                         pad=(32, 36), pad_mobile=24, bg=PAPER, radius=12, border=(1, '#E4E7E3'), w=cu('min(820px, 100%)'),
                         mar=(0, 'auto'))])


def related(keys):
    cards = [svc.card(META[k]['label'], META[k]['icon'], META[k]['summary'], META[k]['photo'], href=META[k]['url']) for k in keys]
    return wrap('Related services', [svc.title('Related', 'services'),
                                     C('Grid', cards, grid=f'repeat({len(cards)}, minmax(0, 1fr))', grid_tablet='1fr', grid_mobile='1fr',
                                       rows='auto', rows_tablet='auto', rows_mobile='auto', gap=20),
                                     H('See all car repair services in Calgary ↗︎', 'p', DK2, S(13, 800, 20), href='/services/',
                                       align='center', mar=(24, 0, 0, 0), name='All services', cls='bb-underline-link')])


def aside(offer):
    ic, title, body = offer
    g = home.google_card()
    a = C('Aside', [g, C('Cards', [home.mini_card('Offer', ic, title, body, True),
                                   home.mini_card('Certified', 'shield-check', 'Certified techs',
                                                  'Parts &amp; labour warranty on most repairs', False)], d='row', gap=12, ai='stretch')],
          gap=12, cls='bb-aside')
    a['settings'].update({'width': px(280), 'width_tablet': cu('min(400px, 100%)'), 'width_mobile': pct(100)})
    return a


def build(key):
    c, m = PAGES[key], META[key]
    el.seed('svc-' + key)
    kinds = {'list': lambda s: sec_list(*s[1:]), 'signs': lambda s: sec_signs(s[1], s[2], c['photos'][-1], *s[3:]),
             'steps': lambda s: sec_steps(*s[1:]), 'text': lambda s: sec_text(*s[1:]), 'callout': lambda s: sec_callout(*s[1:]),
             'prices': lambda s: sec_prices(*s[1:])}
    hero = svc.hero(h1=c['h1'], intro=c['intro'], eyebrow=c['eyebrow'], slides=[(p, '') for p in c['photos'][:1]],
                    actions=[svc.yellow_btn(c['cta'], '#book', name='Primary CTA'),
                             BTN('Call ' + PHONE, TEL, S(13, 800, 19.5), color=PAPER, bg='rgba(0,0,0,0)', ic='phone', ic_pos='before',
                                 ic_size=16, pad=(14, 22), radius=6, border=(1, 'rgba(255,255,255,0.5)'), hover_bg=PAPER, hover_color=DK2,
                                 name='Call')],
                    aside=aside(c['offer']), select=False)
    body = [hero, C('Spacer', [], minh=24)]
    body += [kinds[s[0]](s) for s in c['sections']]
    body += [tpl('reasons'), tpl('booking'),
             svc.faq(c['faqs'], eyebrow=m['label'].upper().replace('&', '&amp;') + ' FAQS', heading='Questions?<br><em>Clear answers.</em>'),
             related(c['related']), tpl('location'), tpl('reviews')]
    return el.book_popup(body, json.load(open('ids.json'))['popup_book'])


def publish(key):
    c, m = PAGES[key], META[key]
    ids = json.load(open('ids.json'))
    k = 'page_' + key
    slug = m['url'].strip('/')
    if k not in ids:
        d = wp.post('wp/v2/pages', {'title': m['label'], 'slug': slug, 'status': 'publish',
                                    'template': 'elementor_header_footer'})
        ids[k] = d['id']
        json.dump(ids, open('ids.json', 'w'), indent=1)
    pid = ids[k]
    el.save('pages', pid, build(key), page_settings=svc.PAGE_SETTINGS,
            extra={'template': 'elementor_header_footer', 'title': seo_page_title(c['seo_title']), 'slug': slug, 'parent': 0,
                   'excerpt': c['meta']})
    el.regen(pid)
    print(key, pid, wp.get(f'wp/v2/pages/{pid}?_fields=link')['link'])


def seo_page_title(t):
    """Yoast renders "<page title> - Busy Bee Auto Repair"; the doc's SEO title minus its brand suffix gets that close to the
    doc (exact titles + meta descriptions go in via Yoast → Tools → Bulk editor, list in HANDOFF.md)."""
    return t.rsplit(' | Busy Bee', 1)[0]


if __name__ == '__main__':
    for key in (sys.argv[1:] or [k for k, *_ in SERVICE_PAGES]):
        publish(key)
