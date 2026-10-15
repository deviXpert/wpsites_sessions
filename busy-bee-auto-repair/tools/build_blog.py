"""Blog: /blog/ (WordPress posts page) + Elementor Theme Builder templates
  • Blog archive  – hero + native Archive Posts (cards) for the posts page and every category archive.
  • Single post   – hero with title/meta, featured image, post content, sticky service sidebar, related posts, booking CTA.
Also seeds three starter posts (each links to its matching service page, as the SEO doc asks).  Usage: python3 build_blog.py"""
import json
import el, wp
from build_globals import tpl
import build_services as svc
import build_service_pages as sp
from build_inner import ensure_template, set_conditions
from common import *
from sitemap import SERVICE_PAGES, SVC_URL

DK2 = svc.DK2
MEDIA = json.load(open('media.json'))

POSTS = [
    ('check-engine-light-calgary', 'Check Engine Light On? What It Means and What to Do', 'computer-diagnostics-calgary',
     'A check engine light can mean anything from a loose fuel cap to a misfire. Here’s how to tell how urgent it is, and what a '
     'proper diagnostic involves.',
     f'''<p>A check engine light is your car asking for help. It can mean anything from a loose fuel cap to a misfire that can damage
your catalytic converter, so the light itself tells you little. The fault codes behind it tell you a lot.</p>
<h2>Steady or flashing?</h2>
<p><strong>A steady light</strong> means the engine computer has stored a fault. It’s usually safe to keep driving for a short time,
but book a diagnosis soon. <strong>A flashing light</strong> usually means an active misfire. Reduce speed, avoid hard acceleration,
and call a mechanic – unburned fuel can overheat and ruin the catalytic converter.</p>
<h2>Common causes we see in Calgary</h2>
<ul><li>A loose or worn fuel cap (an evaporative system code)</li><li>Worn spark plugs or a failing ignition coil</li>
<li>Oxygen sensor or mass air flow sensor faults</li><li>Vacuum leaks from cracked hoses – cold winters are hard on rubber</li>
<li>Thermostat faults that stop the engine reaching temperature</li></ul>
<h2>Why a proper diagnostic matters</h2>
<p>A code reader gives a starting point, not an answer. A code for a misfire on cylinder 3 could be a plug, a coil, an injector or a
mechanical problem. Our <a href="{SVC_URL['electrical']}">car diagnostics in Calgary</a> combine computer scanning with hands-on
testing, so you pay for one correct repair instead of a series of guesses.</p>
<p>If the light came on with rough running, overheating or a loss of power, see our <a href="{SVC_URL['engine']}">engine repair
in Calgary</a> page or call us on {PHONE}.</p>'''),
    ('winter-tires-calgary-when-to-switch', 'When Should You Switch to Winter Tires in Calgary?', 'winter-tire-change-calgary',
     'The 7°C rule, tread depth for Calgary snow, and why new or good used winter tires are worth it before the first storm.',
     f'''<p>The simple rule: switch to winter tires when temperatures stay below 7°C. In Calgary that’s usually from mid-October. Below
7°C, the rubber in all-season tires hardens and loses grip, while winter compounds stay soft.</p>
<h2>Check your tread before the first snow</h2>
<p>Winter tires need tread depth to clear snow and slush. At or below 4/32" (3 mm) a tire is too worn for Calgary snow, even if it’s
still legal. Also look for cracks, bulges or cuts in the sidewall, and replace any tire more than 6 years old, whatever the
tread.</p>
<h2>New or used winter tires?</h2>
<p>Good used tires can save you hundreds. Every used tire we sell is inspected for tread depth, age, sidewall damage and repairs
before it goes on your car. Visit our <a href="{SVC_URL['tires']}">tire shop in Calgary</a> to check what we have in your size.</p>
<h2>Don’t forget alignment</h2>
<p>Potholes and curbs knock wheels out of alignment, and a car that pulls will wear new tires out early. If your steering wheel sits
off-centre, book a <a href="{SVC_URL['alignment']}">wheel alignment in Calgary</a> when your winter set goes on.</p>'''),
    ('how-often-oil-change-calgary', 'How Often Should You Change Your Oil in Calgary?', 'mobil-1-synthetic-oil-change-calgary',
     'Calgary counts as severe driving. Here’s a realistic oil change interval for synthetic oil, and what a good oil change '
     'includes.',
     f'''<p>Most modern cars on synthetic oil need a change every 8,000 to 12,000 km. But Calgary counts as “severe” driving: cold starts,
short trips and dust all break oil down faster, so many vehicles do better at the shorter end of that range.</p>
<h2>Signs you’re due</h2>
<ul><li>Your oil change reminder or maintenance light is on</li><li>The oil on the dipstick is dark and gritty</li>
<li>You hear more engine noise on cold starts</li><li>You’ve driven mostly short trips in winter</li></ul>
<h2>What a proper oil change includes</h2>
<p>Drain and refill with the correct oil grade for your engine, a new oil filter, fluid top-ups and a leak check. At Busy Bee every
oil change also includes a free multi-point inspection of brakes, tires, belts, battery and lights.</p>
<p>Our <a href="{SVC_URL['oil']}">Mobil 1 synthetic oil change in Calgary</a> starts from $75 and walk-ins are welcome. Planning
bigger service? See <a href="{SVC_URL['maintenance']}">car maintenance in Calgary</a>.</p>'''),
]


def seed_posts():
    cats = wp.get('wp/v2/categories?slug=car-care-tips')
    cat = cats[0]['id'] if cats else wp.post('wp/v2/categories', {'name': 'Car care tips', 'slug': 'car-care-tips'})['id']
    for slug, title, img, excerpt, html in POSTS:
        have = wp.get(f'wp/v2/posts?slug={slug}&status=any&_fields=id')
        body = {'title': title, 'slug': slug, 'status': 'publish', 'content': html, 'excerpt': excerpt, 'categories': [cat],
                'featured_media': MEDIA[img]['id']}
        body['content'] = ' '.join(html.split())  # one line per block: wpautop would turn source line breaks into <br>
        body['content'] = body['content'].replace('> <', '><')
        d = wp.post(f"wp/v2/posts/{have[0]['id']}", body) if have else wp.post('wp/v2/posts', body)
        print('post', d['id'], d['link'])


def blog_page():
    ids = json.load(open('ids.json'))
    if 'page_blog' not in ids:
        ids['page_blog'] = wp.post('wp/v2/pages', {'title': 'Blog', 'slug': 'blog', 'status': 'publish'})['id']
        json.dump(ids, open('ids.json', 'w'), indent=1)
    wp.post('wp/v2/settings', {'page_for_posts': ids['page_blog']})
    wp.post(f"wp/v2/pages/{ids['page_blog']}", {'title': 'Car Care Tips & Auto Repair Advice', 'slug': 'blog',
                                                'excerpt': 'Car care tips from Busy Bee Auto Repair in NE Calgary: warning lights, '
                                                           'winter tires, oil changes, brakes and more.'})
    return ids['page_blog']


def sidebar():
    rows = [C(l, [ICON(ic, 18, color=DK2, bg=YEL, box=36, radius=10, name='Icon', w='auto'),
                  H(l.replace('&', '&amp;'), 'span', PAPER, S(14, 700, 20), name='Name', cls='bb-shrink', grow=True),
                  ICON('arrow-right', 14, color=PAPER, box=28, radius=14, name='Arrow', w='auto', cls='bb-side-arrow')],
              d='row', ai='center', gap=12, pad=(9, 10), radius=12, href=u, cls='bb-side-link')
            for _, l, u, ic, *_ in SERVICE_PAGES]
    return C('Sidebar', [
        C('Services', [H('OUR SERVICES', 'p', YEL, S(11, 800, 16.5, 1.76), name='Eyebrow'),
                       H('What can we fix <em>today?</em>', 'p', PAPER, S(22, 850, 26, -0.4, 'uppercase'), mar=(8, 0, 16, 0),
                         name='Title', cls='bb-sm-em-yel')] + rows +
          [H('All services ↗︎', 'p', YEL, S(13, 800, 20), href='/services/', mar=(14, 0, 0, 10), name='All services')],
          pad=(24, 14), bg=DK2, radius=16, cls='bb-side-services'),
        C('Book card', [H('NEED A MECHANIC?', 'p', DK2, S(11, 800, 16.5, 1.76), name='Eyebrow'),
                        H('Book with Busy Bee in NE Calgary.', 'p', DK2, S(20, 850, 24, tt='uppercase'), mar=(10, 0, 16, 0),
                          name='Title'),
                        BTN('Book appointment', '#book', S(13, 800, 19.5), color=PAPER, bg=DK2, ic='arrow-up-right', ic_size=16,
                            pad=(14, 22), radius=30, name='Book'),
                        H(PHONE, 'p', DK2, S(15, 800, 22), href=TEL, mar=(14, 0, 0, 0), name='Phone')],
          pad=24, bg=YEL, radius=16, mar=(16, 0, 0, 0)),
    ], cls='bb-sticky-side')


def tag(name, settings=None):
    import urllib.parse
    st = urllib.parse.quote(json.dumps(settings or {}, separators=(',', ':')))
    return f'[elementor-tag id="{el.uid()}" name="{name}" settings="{st}"]'


def single():
    el.seed('single-post')
    hero = C('Post hero', [C('Inner', [
        W('post-info', 'Category', icon_list=[{'_id': el.uid(), 'type': 'terms', 'taxonomy': 'category', 'selected_icon': {'value': '',
                                                                                                                             'library': ''}}],
          text_color=YEL, **{('icon_typography_' + k[11:]): v for k, v in S(11, 800, 16.5, 1.76, 'uppercase').items()},
          cls='bb-post-cat'),
        W('theme-post-title', 'Title', header_size='h1', title_color=PAPER, __dynamic__={'title': tag('post-title')},
          **S(cu('clamp(32px, 4vw, 54px)'), 850, 1.06, cu('-0.035em'), 'uppercase'), mar=(14, 0, 18, 0), cls='bb-post-title'),
        W('post-info', 'Meta', icon_list=[{'_id': el.uid(), 'type': 'date', 'link': '', 'selected_icon': icon('calendar-days')},
                                          {'_id': el.uid(), 'type': 'custom', 'custom_text': 'Busy Bee Auto Repair, NE Calgary',
                                           'selected_icon': icon('map-pin')}],
          text_color='#C6CDD0', icon_color=YEL, **{('icon_typography_' + k[11:]): v for k, v in S(13, 500, 20).items()},
          cls='bb-post-meta'),
    ], w=cu('min(900px, 100%)'), mar=(0, 'auto'))], tag='section', pad=(190, 32, 80, 32), pad_mobile=(120, 22, 44, 22), bg='#11191D',
        cls='bb-sys')
    content = C('Body', [
        C('Main', [W('theme-post-featured-image', 'Featured image', image_size='large', image_border_radius=dims(12),
                     __dynamic__={'image': tag('post-featured-image')},
                     cls='bb-post-img'),
                   W('theme-post-content', 'Content', text_color='#2B3437', **{('typography_' + k[11:]): v for k, v in
                                                                               S(17, 400, 30).items()}, mar=(28, 0, 0, 0),
                     cls='bb-post-content'),
                   C('Share', [H('Questions about your car? Call ' + PHONE + ' or book online.', 'p', DK2, S(15, 700, 22),
                                 href=TEL, name='Call line')], pad=(20, 24), bg=YEL, radius=10, mar=(32, 0, 0, 0))],
          w='auto', cls='bb-shrink'),
        sidebar(),
    ], grid='minmax(0, 1fr) 320px', grid_tablet='1fr', grid_mobile='1fr', rows='auto', rows_tablet='auto', rows_mobile='auto', gap=48,
        tag='article', pad=(56, 32), pad_mobile=(32, 22), w=cu('min(1240px, 100%)'), mar=(0, 'auto'), cls='bb-sys')
    more = sp.wrap('More posts', [svc.title('More from the', 'blog'),
                                  W('posts', 'Related posts', _skin='cards', cards_columns='3', cards_columns_tablet='2',
                                    cards_columns_mobile='1', cards_posts_per_page=3, posts_post_type='post',
                                    posts_exclude=['current_post'], cards_show_excerpt='yes', cards_excerpt_length=18,
                                    cards_meta_data=['date'], cards_read_more_text='Read more »', cards_show_badge='yes',
                                    cards_badge_taxonomy='category', cards_show_avatar='', cards_thumbnail_size_size='medium_large',
                                    cls='bb-post-cards')])
    return el.book_popup([hero, content, more, tpl('request')],
                         json.load(open('ids.json'))['popup_book'])


def archive():
    el.seed('blog-archive')
    hero = svc.hero(h1='Car care tips &amp; auto repair <em>advice</em>',
                    intro='Straight answers from our NE Calgary mechanics: warning lights, winter tires, oil changes, brakes and the '
                          'maintenance that keeps your car out of the shop.',
                    eyebrow='BUSY BEE BLOG · NE CALGARY', slides=[('busy-bee-repair-bay-calgary', '')],
                    actions=[svc.yellow_btn('Book an appointment', '#book', name='Book'),
                             BTN('Browse services', '/services/', S(13, 800, 19.5), color=PAPER, bg='rgba(0,0,0,0)', pad=(14, 22),
                                 radius=6, border=(1, 'rgba(255,255,255,0.5)'), hover_bg=PAPER, hover_color=DK2, name='Services')],
                    aside=False, select=False, trust=None)
    cards = dict(columns='3', columns_tablet='2', columns_mobile='1', show_excerpt='yes', excerpt_length=22, meta_data=['date'],
                 read_more_text='Read more »', show_badge='yes', badge_taxonomy='category', show_avatar='',
                 thumbnail_size_size='medium_large')
    posts = sp.wrap('Posts', [W('archive-posts', 'Posts', _skin='archive_cards', **{'archive_cards_' + k: v for k, v in cards.items()},
                                pagination_type='numbers_and_prev_next',
                                nothing_found_message='New car care articles are on the way. Call (403) 930-5888 with any question.',
                                cls='bb-post-cards')], pad=(56, 32))
    return el.book_popup([hero, posts, tpl('request')], json.load(open('ids.json'))['popup_book'])


if __name__ == '__main__':
    seed_posts()
    print('blog page', blog_page())
    sid = ensure_template('tpl_single_post', 'Busy Bee – Single post', 'single-post')
    aid = ensure_template('tpl_archive', 'Busy Bee – Blog archive', 'archive')
    el.save('elementor_library', sid, single(), extra={'title': 'Busy Bee – Single post'})
    el.save('elementor_library', aid, archive(), extra={'title': 'Busy Bee – Blog archive'})
    set_conditions(sid, [('include', 'singular', 'post')])
    set_conditions(aid, [('include', 'archive', '')])
    for t in (sid, aid):
        el.regen(t)
