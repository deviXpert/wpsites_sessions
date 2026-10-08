"""Blog: Theme Builder archive (listing) + single-post templates, Blog posts page, menu item and a test article.
Usage: python3 blog.py            (idempotent; IDs stored in created.json under 'blog')"""
import json, os
from lib import *
from wp import req, ability
C_PATH = os.path.join(D, 'created.json')
c = json.load(open(C_PATH))
b = c.setdefault('blog', {})
def save(): json.dump(c, open(C_PATH, 'w'), indent=1)

def archive_tpl():
    seed('blog-archive')
    hero = C([C([C([RAW(f'<nav class="j-crumb" aria-label="Breadcrumb"><a href="{SITE}/">Home</a><span>/</span><em>Blog</em></nav>'),
                    H('Towing Tips &amp; ' + hl('Roadside Advice'), 'h1', 'j-splitw j-blog-h1'),
                    P('Towing tips, roadside safety advice and Calgary driving know-how from the Jim Towing team.', 'j-lead j-up j-up2')], 'j-phero-copy j-col'),
                 RAW(f'<a class="j-blog-call" href="{TEL}"><span class="ic"><i class="fas fa-phone-alt"></i></span><span><small>Stranded right now?</small><b>{PHONE}</b></span></a>', 'j-blog-call-w')],
                'j-in', fd='row')], 'j-phero j-blog-hero', tag='section')
    grid = W('archive-posts', 'j-blog-grid', _skin='archive_cards', archive_cards_columns='3', archive_cards_columns_tablet='2', archive_cards_columns_mobile='1',
             archive_cards_show_excerpt='yes', archive_cards_excerpt_length=22, archive_cards_meta_data=['date'], archive_cards_read_more_text='Read article',
             archive_cards_show_badge='yes', archive_cards_badge_taxonomy='category', archive_cards_show_avatar='', archive_cards_thumbnail_size_size='medium_large',
             archive_cards_item_ratio={'unit': 'px', 'size': 0.66}, pagination_type='numbers_and_prev_next', pagination_prev_label='Previous', pagination_next_label='Next',
             nothing_found_message='No articles yet — check back soon.')
    body = sec([C([grid], 'j-col')], 'j-paper')
    return wrap([hero, body, cta()])

def single_tpl():
    seed('blog-single')
    info = W('post-info', 'j-post-info', view='inline', icon_list=[
        {'_id': rid(), 'type': 'terms', 'taxonomy': 'category', 'selected_icon': ICO('folder')},
        {'_id': rid(), 'type': 'date', 'selected_icon': ICO('calendar-alt')}])
    hero = C([C([C([RAW(f'<nav class="j-crumb" aria-label="Breadcrumb"><a href="{SITE}/">Home</a><span>/</span><a href="{SITE}/blog/">Blog</a><span>/</span><em>Article</em></nav>'),
                    W('theme-post-title', 'j-h j-blog-h1 j-up', header_size='h1', __dynamic__={'title': '[elementor-tag id="b2c3d4e" name="post-title" settings="%7B%7D"]'}), info], 'j-phero-copy j-col')], 'j-in', fd='row')], 'j-phero j-blog-hero j-post-hero', tag='section')
    side = C([RAW(f'''<aside class="j-post-cta"><span class="j-dot"></span><small>Dispatch online 24/7</small><b>Need a tow right now?</b><p>Breakdowns, accidents, dead batteries or empty tanks — we're on the road across Calgary day and night.</p>
<a class="call" href="{TEL}"><i class="fas fa-phone-alt"></i>{PHONE}</a><a class="quote" href="{PAGES['contact']}#request"><i class="fas fa-paper-plane"></i>Request service</a></aside>
<nav class="j-post-svcs" aria-label="Our services"><small>Our services</small>''' + ''.join(f'<a href="{surl(s)}"><i class="fas fa-{ic}"></i>{t}</a>' for s, t, ic, *_ in SVC) + '</nav>')], 'j-post-side j-col')
    main = C([W('theme-post-featured-image', 'j-post-img', image_size='large', __dynamic__={'image': '[elementor-tag id="c3d4e5f" name="post-featured-image" settings="%7B%7D"]'}), W('theme-post-content', 'j-prose'),
              W('share-buttons', 'j-share', share_buttons=[{'_id': rid(), 'button': 'facebook'}, {'_id': rid(), 'button': 'twitter'}, {'_id': rid(), 'button': 'linkedin'}, {'_id': rid(), 'button': 'whatsapp'}, {'_id': rid(), 'button': 'email'}],
                view='icon', skin='flat', shape='circle', columns='0', alignment='left'),
              W('post-navigation', 'j-post-nav', show_label='yes', prev_label='Previous article', next_label='Next article', show_arrow='yes', show_title='yes', show_borders='')], 'j-post-main j-col')
    article = sec([C([main, side], 'j-post-grid')], 'j-white')
    more = sec([head('Keep reading', 'More from the ' + hl('Jim Towing Blog')),
                W('posts', 'j-blog-grid', _skin='cards', cards_columns='3', cards_columns_tablet='2', cards_columns_mobile='1', posts_per_page=3, cards_show_excerpt='yes', cards_excerpt_length=18,
                  cards_meta_data=['date'], cards_read_more_text='Read article', cards_show_badge='yes', cards_badge_taxonomy='category', cards_show_avatar='', posts_post_type='post', posts_exclude=['current_post'],
                  cards_thumbnail_size_size='medium_large')], 'j-paper')
    return wrap([hero, article, more, cta()])

POST_HTML = f'''<!-- wp:paragraph --><p>A breakdown on Deerfoot Trail, a fender-bender in a parking lot or a car that simply won't start on a cold January morning — vehicle trouble rarely happens at a convenient time. Here's exactly what to do while you wait for a tow truck in Calgary, so you stay safe and the tow goes smoothly.</p><!-- /wp:paragraph -->
<!-- wp:heading --><h2>1. Get yourself somewhere safe first</h2><!-- /wp:heading -->
<!-- wp:list --><ul><li>Turn on your <strong>hazard lights</strong> right away.</li><li>If the vehicle still rolls, move to the shoulder or a safe spot away from traffic.</li><li>On a busy road or highway shoulder, <strong>stay out of the vehicle</strong> and stand behind a barrier if you can.</li><li>Don't walk along highways like Stoney Trail or Deerfoot Trail.</li></ul><!-- /wp:list -->
<!-- wp:quote --><blockquote class="wp-block-quote"><p>If anyone is injured or there is a fire risk, call 911 first.</p></blockquote><!-- /wp:quote -->
<!-- wp:heading --><h2>2. Have the right details ready when you call</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>A quick, clear call gets the right truck to you faster. When you call <a href="{TEL}">{PHONE}</a>, tell the dispatcher:</p><!-- /wp:paragraph -->
<!-- wp:list {{"ordered":true}} --><ol><li>Your exact location — cross streets, exit number or a nearby landmark.</li><li>Your vehicle make and model.</li><li>What happened (won't start, accident, flat tire, out of fuel…).</li><li>Where you want the vehicle taken — home, your mechanic, a body shop or a dealership.</li></ol><!-- /wp:list -->
<!-- wp:paragraph --><p>We confirm the price and an estimated arrival time before we dispatch, so there are no surprises.</p><!-- /wp:paragraph -->
<!-- wp:heading --><h2>3. Not every problem needs a tow</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>A dead battery, a flat tire or an empty tank can often be fixed on the spot with <a href="{surl("roadside-assistance-calgary")}">roadside assistance</a>. If the engine won't run after a jump, there's a fluid leak, a damaged wheel or axle, or the car was in a collision, <a href="{surl("emergency-towing-calgary")}">towing</a> is the safer option. Our team will tell you honestly which one you need.</p><!-- /wp:paragraph -->
<!-- wp:heading --><h2>4. Ask for a flatbed when it matters</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p>AWD and 4WD vehicles, luxury and lowered cars, motorcycles and accident-damaged vehicles are best moved on a <a href="{surl("flatbed-towing-calgary")}">flatbed</a>, with all four wheels off the road. If you're not sure, just ask — we'll recommend the right method.</p><!-- /wp:paragraph -->
<!-- wp:heading --><h2>5. Calgary winter tips that prevent the call</h2><!-- /wp:heading -->
<!-- wp:list --><ul><li>Winter cold can drain a battery overnight — test your battery before November.</li><li>Refuel at a quarter tank, especially in winter.</li><li>Don't rely on the "distance to empty" number in extreme cold.</li><li>Keep your spare tire in good condition and know where your jack and wheel lock key are.</li></ul><!-- /wp:list -->
<!-- wp:paragraph --><p><strong>Stranded right now?</strong> Call Jim Towing at <a href="{TEL}">{PHONE}</a> — 24 hours a day, 7 days a week, across Calgary and surrounding areas.</p><!-- /wp:paragraph -->'''

if __name__ == '__main__':
    # category
    if not b.get('cat'):
        r = req('wp/v2/categories', 'POST', {'name': 'Towing Tips', 'slug': 'towing-tips', 'description': 'Roadside safety and towing advice for Calgary drivers.'})
        b['cat'] = r.get('id') or req('wp/v2/categories?slug=towing-tips')[0]['id']; save()
    # Blog page as posts page
    if not b.get('page'):
        r = req('wp/v2/pages', 'POST', {'title': 'Blog', 'slug': 'blog', 'status': 'publish', 'content': ''}); b['page'] = r['id']; save()
    print('settings', req('wp/v2/settings', 'POST', {'page_for_posts': b['page']}).get('page_for_posts'))
    # test post
    body = {'title': 'Stuck on the Road in Calgary? What to Do While You Wait for a Tow', 'slug': 'what-to-do-while-waiting-for-a-tow-calgary', 'status': 'publish',
            'content': POST_HTML, 'categories': [b['cat']], 'featured_media': IMG['winter'],
            'excerpt': 'Hazard lights, safety first, the details to give the dispatcher, when a tow beats roadside help, and Calgary winter tips that prevent the call.'}
    r = req(f"wp/v2/posts/{b['post']}", 'POST', body) if b.get('post') else req('wp/v2/posts', 'POST', body)
    b['post'] = r['id']; save(); print('post', r['id'], r.get('link'))
    # theme templates
    for key, kind, cond, data in [('archive', 'archive', ['include/archive'], archive_tpl()), ('single', 'single-post', ['include/singular/post'], single_tpl())]:
        if not b.get(key):
            rr = ability('elementor/manage-site-parts', {'operations': [{'action': 'create', 'type': kind, 'title': f'Jim Blog {key.title()}', 'conditions': cond}]})
            print(rr); b[key] = rr['results'][0]['id']; save()
        rr = req(f'wp/v2/elementor_library/{b[key]}', 'POST', {'status': 'publish', 'meta': {'_elementor_data': json.dumps(data), '_elementor_edit_mode': 'builder', '_elementor_page_settings': {'hide_title': 'yes'}}})
        print(key, b[key], rr.get('status'), rr.get('_err') or '')
    # menu item
    if not b.get('menu_item'):
        items = req(f"wp/v2/menu-items?menus={c['menu']}&per_page=100")
        contact = [i for i in items if i['title']['rendered'] == 'Contact'][0]
        r = req('wp/v2/menu-items', 'POST', {'title': 'Blog', 'url': SITE + '/blog/', 'menus': c['menu'], 'menu_order': contact['menu_order'], 'type': 'custom', 'status': 'publish'})
        req(f"wp/v2/menu-items/{contact['id']}", 'POST', {'menu_order': contact['menu_order'] + 1})
        b['menu_item'] = r.get('id'); save()
    req('elementor/v1/cache', 'DELETE')
    print('done', b)
