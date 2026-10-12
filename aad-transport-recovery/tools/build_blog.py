"""Blog for the AAD site: Elementor Theme Builder templates (Archive = blog listing, Single Post) styled like the redesign.
Global CSS/JS (redesign.css/js) already loads site-wide from the header template; blog-only CSS lives in blog.css.
Usage: python3 build_blog.py            -> writes built_blog.json
       python3 build_blog.py --publish  -> creates/updates the templates via Elementor's site-editor API (IDs in created.json)"""
import json, random, os, sys
D = os.path.dirname(os.path.abspath(__file__))
U = 'https://aadrecovery.co.uk'
PHONE, TEL = '07771 004242', 'tel:07771004242'
HERO_IMG = U + '/wp-content/uploads/2026/09/IMG_20260327_110403_860-scaled.webp'

random.seed('aad-blog')  # stable element IDs between rebuilds
def rid(): return '%07x' % random.getrandbits(28)
def z(): return {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
def C(els, cls='', **s):
    st = {'content_width': s.pop('cw', 'full'), 'padding': s.pop('pad', z()), 'flex_gap': {'unit': 'px', 'size': s.pop('gap', 0), 'column': '0', 'row': '0', 'isLinked': True}}
    fd, fw = s.get('flex_direction', 'column'), s.get('flex_wrap', '')
    extra = ('x-dr' if fd == 'row' else 'x-dc') + (' x-wrap' if fw == 'wrap' else '') + (' x-bx' if st['content_width'] == 'boxed' else '') + ' e-no-lazyload'
    st['css_classes'] = (cls + ' ' + extra).strip()
    st.update(s)
    return {'id': rid(), 'elType': 'container', 'isInner': False, 'settings': st, 'elements': els}
def W(t, cls='', **s):
    if cls: s['_css_classes'] = cls
    return {'id': rid(), 'elType': 'widget', 'widgetType': t, 'isInner': False, 'settings': s, 'elements': []}
def H(t, tag='h2', cls=''): return W('heading', 'x-h ' + cls, title=t, header_size=tag)
def T(html, cls=''): return W('text-editor', 'x-t ' + cls, editor=html)
def ICO(v): return {'value': 'fas fa-' + v, 'library': 'fa-solid'}
def BTN(t, url, cls='x-btn', icon='phone-alt'):
    return W('button', cls, text=t, link={'url': url, 'is_external': '', 'nofollow': ''}, selected_icon=ICO(icon), icon_align='row', icon_indent={'unit': 'px', 'size': 10})
def RAW(h): return W('html', '', html=h)
def eyebrow(t): return T(f'<p>{t}</p>', 'x-eyebrow')
def sec(els, cls, **kw): return C(els, 'x-sec ' + cls, flex_direction='column', cw='boxed', **kw)

CSS = open(os.path.join(D, 'blog.css')).read()
ASSETS = RAW('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">'
             f'<style>.x-root.x-blog .x-hero{{background-image:url({HERO_IMG})!important}}{CSS}</style>')

def crumbs(*parts):
    links = ' <span>/</span> '.join(f'<a href="{u}">{t}</a>' if u else t for t, u in parts)
    return T(f'<p>{links}</p>', 'x-crumbs rv')

def hero(els, extra=''):
    return C([C(els, 'x-hero-copy', flex_direction='column')], 'x-hero x-hero-slim ' + extra, flex_direction='row', cw='boxed')

def cta():
    return sec([C([
        C([H('Broken Down? <span class="x-hl">We\'re On Our Way.</span>', 'h2', 'x-cta-title'),
           T('<p>AAD Transport &amp; Recovery provides 24/7 breakdown recovery, towing and vehicle transport across Birmingham and the West Midlands.</p>', 'x-cta-text')], 'x-cta-copy', flex_direction='column'),
        C([BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-white'), BTN('Get A Quote', U + '/contact/', 'x-btn x-btn-ghost', 'file-signature')], 'x-btnrow', flex_direction='row', flex_wrap='wrap'),
    ], 'x-cta rv', flex_direction='row')], 'x-sec-cta')

def cards_skin(prefix, cols=3, per_page=None):
    s = {'_skin': 'cards' if prefix == 'cards_' else 'archive_cards',
         prefix + 'columns': str(cols), prefix + 'columns_tablet': '2', prefix + 'columns_mobile': '1',
         prefix + 'thumbnail_size_size': 'medium_large', prefix + 'item_ratio': {'unit': 'px', 'size': 0.62},
         prefix + 'show_title': 'yes', prefix + 'title_tag': 'h3',
         prefix + 'show_excerpt': 'yes', prefix + 'excerpt_length': 22,
         prefix + 'meta_data': ['date'], prefix + 'meta_separator': '•',
         prefix + 'show_read_more': 'yes', prefix + 'read_more_text': 'Read Article',
         prefix + 'show_badge': 'yes', prefix + 'badge_taxonomy': 'category',
         prefix + 'show_avatar': '', prefix + 'card_hover_effect': 'none',
         prefix + 'column_gap': {'unit': 'px', 'size': 28}, prefix + 'row_gap': {'unit': 'px', 'size': 28}}
    if per_page: s[prefix + 'posts_per_page'] = per_page
    return s

# ---------- BLOG LISTING (Archive template) ----------
def archive():
    h = hero([crumbs(('Home', U + '/'), ('Blog', None)),
              T('<p><span class="x-dot"></span> Recovery Advice · Birmingham</p>', 'x-badge rv'),
              W('theme-archive-title', 'x-h x-hero-title rv', header_size='h1', __dynamic__={'title': '[elementor-tag id="' + rid() + '" name="archive-title" settings="%7B%22include_context%22%3A%22%22%2C%22fallback%22%3A%22Recovery%20Tips%20%26%20News%22%7D"]'}),
              T('<p>Breakdown tips, towing guides and vehicle recovery advice from the AAD Transport &amp; Recovery team — helping drivers across Birmingham and the West Midlands stay safe on the road.</p>', 'x-hero-lead rv')])
    grid = W('archive-posts', 'x-blog-grid', **cards_skin('archive_cards_'),
             pagination_type='numbers_and_prev_next', pagination_page_limit='', pagination_prev_label='← Previous', pagination_next_label='Next →',
             pagination_align='center', nothing_found_message='No articles found yet — check back soon for recovery tips and news.')
    body = sec([C([eyebrow('LATEST ARTICLES'), H('Tips, Guides &amp; <span class="x-hl">Recovery News</span>', 'h2', 'x-title')], 'x-blog-head rv', flex_direction='column'), grid], 'x-sec-blog')
    return [C([ASSETS, h, body, cta()], 'x-root x-page x-blog', flex_direction='column')]

# ---------- SINGLE POST ----------
def single():
    info = W('post-info', 'x-post-meta rv', view='inline', icon_list=[
        {'_id': rid(), 'type': 'date', 'selected_icon': ICO('calendar-alt'), 'show_icon': 'custom', 'link': ''},
        {'_id': rid(), 'type': 'terms', 'taxonomy': 'category', 'selected_icon': ICO('folder-open'), 'show_icon': 'custom', 'link': ''}])
    h = hero([crumbs(('Home', U + '/'), ('Blog', U + '/blog/'), ('Article', None)),
              W('theme-post-title', 'x-h x-hero-title rv', header_size='h1', __dynamic__={'title': '[elementor-tag id="' + rid() + '" name="post-title" settings="%7B%7D"]'}), info], 'x-post-hero')
    article = C([
        W('theme-post-featured-image', 'x-post-img', image_size='large'),
        W('theme-post-content', 'x-prose'),
        W('post-info', 'x-post-tags', view='inline', icon_list=[{'_id': rid(), 'type': 'terms', 'taxonomy': 'post_tag', 'selected_icon': ICO('tags'), 'show_icon': 'custom', 'link': ''}]),
        W('share-buttons', 'x-share', share_buttons=[{'_id': rid(), 'button': b} for b in ('facebook', 'twitter', 'linkedin', 'whatsapp', 'email')], view='icon', skin='flat', shape='circle', columns='0', alignment='left'),
        W('post-navigation', 'x-post-nav', show_label='yes', prev_label='Previous Article', next_label='Next Article', show_arrow='yes', show_title='yes', show_borders=''),
    ], 'x-prose-card x-post-card rv', flex_direction='column')
    aside = C([
        C([T('<p class="x-toc-h">In this article</p><nav class="x-toc-list"></nav>', 'x-toc-inner')], 'x-toc', flex_direction='column'),
        C([T('<p class="x-callcard-k">Broken down right now?</p>', 'x-callcard-k'),
           H('24/7 Recovery <span class="x-hl">In Birmingham</span>', 'p', 'x-callcard-t'),
           T('<p>Fast, fully insured breakdown recovery and towing — day or night.</p>', 'x-callcard-d'),
           BTN('Call ' + PHONE, TEL, 'x-btn x-btn-sm x-btn-pulse')], 'x-callcard', flex_direction='column'),
    ], 'x-post-aside', flex_direction='column')
    body = sec([C([article, aside], 'x-legal x-post-layout', flex_direction='row')], 'x-sec-legal x-sec-post')
    related = sec([eyebrow('KEEP READING'), H('More From <span class="x-hl">The Blog</span>', 'h2', 'x-title'),
                   W('posts', 'x-blog-grid', **cards_skin('cards_', 3, 3), posts_post_type='related', posts_include=['terms'],
                     posts_related_taxonomies=['category'], posts_related_fallback='fallback_recent', posts_avoid_duplicates='', nothing_found_message='')], 'x-sec-related')
    return [C([ASSETS, h, body, related, cta()], 'x-root x-page x-blog', flex_direction='column')]

TEMPLATES = {
    'blog_archive': {'title': 'Blog – Archive (Listing)', 'type': 'archive', 'build': archive, 'conditions': [{'type': 'include', 'name': 'archive', 'sub_name': '', 'sub_id': ''}]},
    'blog_single': {'title': 'Blog – Single Post', 'type': 'single-post', 'build': single, 'conditions': [{'type': 'include', 'name': 'singular', 'sub_name': 'post', 'sub_id': ''}]},
}

if __name__ == '__main__':
    built = {k: v['build']() for k, v in TEMPLATES.items()}
    json.dump(built, open(os.path.join(D, 'built_blog.json'), 'w'))
    print('built', {k: len(json.dumps(v)) for k, v in built.items()})
    if '--publish' in sys.argv:
        import wp
        cf = os.path.join(D, 'created.json'); created = json.load(open(cf))
        for k, v in TEMPLATES.items():
            tid = created.get(k)
            if not tid:
                r = wp.req('wp/v2/elementor_library', 'POST', {'title': v['title'], 'status': 'publish', 'meta': {'_elementor_template_type': v['type'], '_elementor_edit_mode': 'builder'}})
                tid = r.get('id')
                if not tid: raise SystemExit(f'create failed: {r}')
                created[k] = tid; json.dump(created, open(cf, 'w'), indent=1)
            r = wp.req(f'wp/v2/elementor_library/{tid}', 'POST', {'status': 'publish', 'title': v['title'], 'template': 'elementor_header_footer', 'meta': {
                '_elementor_edit_mode': 'builder', '_elementor_template_type': v['type'], '_elementor_data': json.dumps(built[k]),
                '_elementor_page_settings': {'page_template': 'elementor_header_footer'}}})
            print(k, tid, r.get('_err') or 'data ok')
            r = wp.req(f'elementor/v1/site-editor/templates-conditions/{tid}', 'POST', {'conditions': v['conditions']})
            print('  conditions', r)
