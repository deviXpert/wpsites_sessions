"""Blog: listing on the News page (1081) and a Theme Builder single-post template (all posts).
First build only – afterwards patch live data with patch.py.
  python3 blog_templates.py listing [--force]   (refuses if page 1081 already has Elementor data, unless --force)
  python3 blog_templates.py single              (creates the site part once, id stored in inner_ids.json; rebuild with --force)
"""
import json, os, subprocess, sys
from el import C, W, T, H, EYEBROW, px, dims, gap, col, icon, put, regen, shadow, img
from figma_pages import banner, IDS_FILE
from patch import _api

D = os.path.dirname(os.path.abspath(__file__))
CHECKIN = 'https://portal.gorev.com/preregister.aspx?s=h%2f4vymVZJdRgfYtF7XRQTw%3d%3d&f=TY11yCMzYfJUUuhIahY6Qg%3d%3d&l=wQE4BShlAnIMHtZ%2bZ98z2Q%3d%3d'
NEWS_ID = 1081

CARD_CSS = (
    'selector .elementor-posts-container{align-items:stretch}'
    'selector .elementor-post{display:flex;flex-direction:column;background:#fff;border:1px solid #DFE5ED;border-radius:18px;'
    'overflow:hidden;box-shadow:0 10px 30px rgba(12,30,58,.06);transition:transform .25s,box-shadow .25s,border-color .25s}'
    'selector .elementor-post:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(12,30,58,.12);border-color:#C9D3E3}'
    'selector .elementor-post__thumbnail__link{margin:0 !important;width:100%}'
    'selector .elementor-post__thumbnail img{transition:transform .5s}'
    'selector .elementor-post:hover .elementor-post__thumbnail img{transform:translate(-50%,-50%) scale(1.04)}'
    'selector .elementor-post__text{padding:22px 24px 26px;display:flex;flex-direction:column;flex:1}'
    'selector .elementor-post__meta-data{order:-1;margin:0 0 10px;color:#9F3135;font:600 12px/1.4 Poppins,sans-serif;'
    'letter-spacing:1.2px;text-transform:uppercase;border:0;padding:0}'
    'selector .elementor-post__title{margin:0 0 10px}'
    'selector .elementor-post__title a{color:#293A6E;font:700 19px/1.35 Poppins,sans-serif;letter-spacing:-.3px}'
    'selector .elementor-post__title a:hover{color:#9F3135}'
    'selector .elementor-post__excerpt p{color:#5F6D82;font:400 14.5px/1.65 Poppins,sans-serif;margin:0 0 18px}'
    'selector .elementor-post__read-more{margin-top:auto;color:#9F3135;font:700 14px/1.2 Poppins,sans-serif;'
    'display:inline-flex;align-items:center;gap:8px}'
    'selector .elementor-post__read-more:after{content:"\\2192";transition:transform .2s}'
    'selector .elementor-post__read-more:hover:after{transform:translateX(4px)}'
    'selector .elementor-pagination{margin-top:48px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap}'
    'selector .elementor-pagination .page-numbers{min-width:44px;height:44px;padding:0 14px;display:inline-flex;align-items:center;'
    'justify-content:center;border-radius:999px;border:1px solid #DFE5ED;color:#293A6E;font:600 14px Poppins,sans-serif;margin:0 !important}'
    'selector .elementor-pagination .page-numbers.current{background:#293A6E;border-color:#293A6E;color:#fff}'
    'selector .elementor-pagination a.page-numbers:hover{border-color:#293A6E}')


def posts_listing():
    return W('posts', 'Blog – Posts Grid', _skin='classic', classic_columns='3', classic_columns_tablet='2',
             classic_columns_mobile='1', classic_posts_per_page=9, classic_thumbnail='top', classic_masonry='',
             classic_thumbnail_size_size='medium_large', classic_item_ratio=px(0.62), classic_image_width=px(100, '%'),
             classic_show_title='yes', classic_title_tag='h3', classic_excerpt_length=20, classic_show_excerpt='yes',
             classic_meta_data=['date'], classic_meta_separator='', classic_show_read_more='yes',
             classic_read_more_text='Read More', classic_open_new_tab='',
             classic_column_gap=px(28), classic_row_gap=px(32), classic_row_gap_mobile=px(22), classic_img_border_radius=dims(0),
             posts_post_type='post', posts_orderby='post_date', posts_order='desc',
             posts_exclude=['manual_selection'], posts_exclude_ids=['1'],
             pagination_type='numbers_and_prev_next', pagination_prev_label='← Previous', pagination_next_label='Next →',
             pagination_page_limit='', custom_css=CARD_CSS)


def listing():
    head = C('Blog – Head', [
        EYEBROW('Health Blog'),
        H('Latest Health <span>Articles</span>', 'h2', align='center', name='Section Title'),
        T('<p>Tips, symptoms and guidance from the emergency care team at East Houston Medical Center.</p>',
          align='center', name='Section Intro', _element_width='initial', _element_custom_width=px(640),
          _element_custom_width_tablet=px(100, '%'))],
        flex_direction='column', flex_align_items='center', flex_gap=gap(14), padding=dims(0))
    sec = C('Blog Listing', [head, C('Blog – Grid Wrap', [posts_listing()], padding=dims(0), width=px(1240),
                                     width_tablet=px(100, '%'), custom_css='selector{max-width:100%}')],
            inner=False, flex_direction='column', flex_align_items='center', flex_gap=gap(48), flex_gap_mobile=gap(32),
            padding=dims(90, 20, 100, 20), padding_tablet=dims(70, 24, 80, 24), padding_mobile=dims(56, 16, 64, 16))
    return [banner('News <span>& Blogs</span>', 'hero_v4_slide_4', 'Blog Banner'), sec]


# ---------------------------------------------------------------- single post
CONTENT_CSS = (
    'selector{color:#4A5568;font:400 16.5px/1.85 Poppins,sans-serif}'
    'selector p{margin:0 0 20px}'
    'selector h2{color:#293A6E;font:700 28px/1.3 Poppins,sans-serif;letter-spacing:-.6px;margin:40px 0 16px}'
    'selector h3{color:#293A6E;font:600 21px/1.4 Poppins,sans-serif;letter-spacing:-.3px;margin:30px 0 12px}'
    'selector h4{color:#293A6E;font:600 18px/1.4 Poppins,sans-serif;margin:24px 0 10px}'
    'selector h2 b,selector h3 b,selector h2 strong,selector h3 strong{font-weight:inherit}'
    'selector a{color:#9F3135;text-decoration:underline;text-underline-offset:3px}'
    'selector a:hover{color:#293A6E}'
    'selector ul,selector ol{margin:0 0 22px;padding-left:22px}'
    'selector li{margin:0 0 8px;padding-left:4px}'
    'selector ul li::marker{color:#9F3135}'
    'selector img{width:100%;height:auto;border-radius:18px;display:block;margin:0 0 26px}'
    'selector blockquote{margin:28px 0;padding:20px 24px;border-left:4px solid #9F3135;background:#F7F9FC;border-radius:0 12px 12px 0}'
    'selector table{width:100%;border-collapse:collapse;margin:0 0 24px}selector td,selector th{border:1px solid #DFE5ED;padding:10px 12px}'
    'selector > *:last-child{margin-bottom:0}'
    '@media(max-width:767px){selector{font-size:15.5px;line-height:1.8}selector h2{font-size:23px;margin-top:32px}selector h3{font-size:19px}}')

RECENT_CSS = (
    'selector .elementor-posts-container{gap:0 !important}'
    'selector .elementor-post{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid #EEF1F6;margin:0 !important}'
    'selector .elementor-post:first-child{padding-top:0}selector .elementor-post:last-child{border-bottom:0;padding-bottom:0}'
    'selector .elementor-post__thumbnail__link{flex:0 0 84px;width:84px !important;margin:0 !important}'
    'selector .elementor-post__thumbnail{border-radius:12px;overflow:hidden;padding-bottom:84px !important}'
    'selector .elementor-post__text{flex:1;min-width:0}'
    'selector .elementor-post__meta-data{order:-1;margin:0 0 4px;color:#9F3135;font:600 11px/1.4 Poppins,sans-serif;'
    'letter-spacing:1px;text-transform:uppercase;border:0;padding:0}'
    'selector .elementor-post__text{display:flex;flex-direction:column}'
    'selector .elementor-post__title{margin:0}'
    'selector .elementor-post__title a{color:#293A6E;font:600 14.5px/1.4 Poppins,sans-serif;'
    'display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}'
    'selector .elementor-post__title a:hover{color:#9F3135}')


def tag(name, _id):
    return '[elementor-tag id="%s" name="%s" settings="%%7B%%7D"]' % (_id, name)


def single():
    title = W('theme-post-title', 'Post – Title', header_size='h1', align='left', title_color='#FFFFFF',
              typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
              typography_font_size=px(50), typography_font_size_tablet=px(40), typography_font_size_mobile=px(30),
              typography_line_height=px(1.12, 'em'), typography_letter_spacing=px(-1.6), typography_letter_spacing_mobile=px(-0.8),
              _element_width='initial', _element_custom_width=px(900), _element_custom_width_tablet=px(100, '%'),
              __dynamic__={'title': tag('post-title', 'a1b2c3d')})
    info = W('post-info', 'Post – Meta', icon_list=[
        {'_id': 'd8a1f01', 'type': 'date', 'selected_icon': icon('far fa-calendar', 'fa-regular')},
        {'_id': 'd8a1f02', 'type': 'custom', 'custom_text': '5 min read', 'selected_icon': icon('far fa-clock', 'fa-regular')}],
        space_between=px(22), icon_color='#E6A6A9', text_color='rgba(230,234,241,0.9)', icon_size=px(14),
        icon_typography_typography='custom', icon_typography_font_family='Poppins', icon_typography_font_size=px(14),
        icon_typography_font_weight='500')
    crumb = W('text-editor', 'Post – Breadcrumb',
              editor='<p><a href="/">Home</a><span>/</span><a href="/news/">News &amp; Blogs</a></p>',
              custom_css='selector p{margin:0;display:flex;gap:10px;flex-wrap:wrap;font:600 12px/1.4 Poppins,sans-serif;'
                         'letter-spacing:1.4px;text-transform:uppercase;color:rgba(255,255,255,.55)}'
                         'selector a{color:#E6A6A9}selector a:hover{color:#fff}')
    hero_in = C('Post Banner – Card', [C('Post Banner – Content', [crumb, title, info], flex_direction='column',
                                          flex_gap=gap(18), padding=dims(0, 113, 0, 113), padding_tablet=dims(0, 40, 0, 40),
                                          padding_mobile=dims(0, 20, 0, 20))],
                flex_direction='column', flex_justify_content='flex-end', min_height=px(460), min_height_tablet=px(400),
                min_height_mobile=px(380), padding=dims(150, 0, 64, 0), padding_mobile=dims(160, 0, 36, 0),
                background_background='gradient', background_color='#0C1D3C', background_color_b='#293A6E',
                background_gradient_angle=px(135, 'deg'), border_radius=dims(46), border_radius_mobile=dims(24), overflow='hidden',
                custom_css='selector{position:relative}selector::after{content:"";position:absolute;right:-120px;top:-120px;width:520px;'
                           'height:520px;border-radius:50%;background:radial-gradient(circle,rgba(159,49,53,.35),rgba(159,49,53,0) 65%);'
                           'pointer-events:none}selector > .e-con{position:relative;z-index:1}')
    # Astra wraps singles in a narrow boxed container – let the template run full width
    hero = C('Post Banner', [hero_in], inner=False, padding=dims(10, 8, 0, 8), padding_mobile=dims(8, 8, 0, 8),
             custom_css='body.single-post .site-content>.ast-container{max-width:none;padding:0;display:block}'
                        'body.single-post #primary{margin:0;padding:0;width:100%;max-width:none;border:0}'
                        'body.single-post .ast-article-single{padding:0;margin:0;background:none;border:0}')

    content = W('theme-post-content', 'Post – Content', custom_css=CONTENT_CSS)
    # imported posts use <p>&nbsp;</p> as spacers – drop them so paragraph spacing comes from CSS
    tidy = W('html', 'Post – Tidy Spacers', _position='absolute', html='<script>document.addEventListener("DOMContentLoaded",function(){'
             'document.querySelectorAll(".elementor-widget-theme-post-content p").forEach(function(p){'
             'if(!p.querySelector("img,iframe,video,br")&&!p.textContent.replace(/[\\s\\u00a0]+/g,""))p.remove()})});</script>')
    nav = W('post-navigation', 'Post – Prev/Next', show_label='yes', prev_label='Previous Article', next_label='Next Article',
            show_arrow='yes', arrow='fa fa-angle-left', show_title='yes', show_borders='',
            custom_css='selector{margin-top:44px;padding-top:28px;border-top:1px solid #DFE5ED}'
                       'selector .post-navigation__prev--label,selector .post-navigation__next--label{color:#9F3135;'
                       'font:700 11.5px/1.4 Poppins,sans-serif;letter-spacing:1.2px;text-transform:uppercase}'
                       'selector .post-navigation__prev--title,selector .post-navigation__next--title{color:#293A6E;'
                       'font:600 15px/1.4 Poppins,sans-serif;white-space:normal}'
                       'selector .post-navigation__arrow-wrapper{color:#293A6E}')
    main = C('Post – Main', [content, nav, tidy], flex_direction='column', padding=dims(44, 48, 44, 48),
             padding_tablet=dims(36, 32, 36, 32), padding_mobile=dims(24, 18, 28, 18),
             background_background='classic', background_color='#FFFFFF', border_border='solid', border_width=dims(1),
             border_color='#DFE5ED', border_radius=dims(24), border_radius_mobile=dims(18),
             width=px(68, '%'), width_tablet=px(100, '%'))

    recent = W('posts', 'Sidebar – Recent Posts', _skin='classic', classic_columns='1', classic_columns_tablet='1',
               classic_columns_mobile='1', classic_posts_per_page=5, classic_thumbnail='left', classic_masonry='',
               classic_thumbnail_size_size='thumbnail', classic_item_ratio=px(1), classic_image_width=px(30, '%'),
               classic_show_title='yes', classic_title_tag='h4', classic_show_excerpt='', classic_meta_data=['date'],
               classic_meta_separator='', classic_show_read_more='', posts_post_type='post', posts_orderby='post_date',
               posts_order='desc', posts_exclude=['current_post', 'manual_selection'], posts_exclude_ids=['1'],
               custom_css=RECENT_CSS)
    recent_card = C('Sidebar – Recent Card', [
        W('heading', 'Sidebar – Recent Title', title='Recent Posts', header_size='h3', title_color='#293A6E',
          typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
          typography_font_size=px(20), custom_css='selector{padding-bottom:14px;border-bottom:2px solid #F1F3F7;position:relative}'
                                                 'selector::after{content:"";position:absolute;left:0;bottom:-2px;width:46px;height:2px;background:#9F3135}'),
        recent], flex_direction='column', flex_gap=gap(18), padding=dims(26, 24, 26, 24),
        background_background='classic', background_color='#FFFFFF', border_border='solid', border_width=dims(1),
        border_color='#DFE5ED', border_radius=dims(20))
    cta = C('Sidebar – Emergency Card', [
        W('heading', 'Sidebar – CTA Title', title='Need Emergency Care Now?', header_size='h3', title_color='#FFFFFF',
          typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
          typography_font_size=px(22), typography_line_height=px(1.25, 'em')),
        W('text-editor', 'Sidebar – CTA Text', editor='<p>Open 24/7 with no appointment needed. Walk in or call us now.</p>',
          text_color='rgba(230,234,241,0.88)', typography_typography='custom', typography_font_family='Poppins',
          typography_font_size=px(14.5), custom_css='selector p{margin:0}'),
        W('button', 'Sidebar – Call', text='Call (832) 400-2396', link={'url': 'tel:+18324002396', 'is_external': '', 'nofollow': ''},
          selected_icon=icon('fas fa-phone-alt'), icon_indent=px(10), border_radius=dims(10), text_padding=dims(14, 18),
          align='justify', g={'background_color': col('secondary'), 'button_text_color': col('ehwhite'),
                              'button_background_hover_color': col('ehreddk'), 'typography_typography': 'globals/typography?id=ehbtn'},
          custom_css='selector .elementor-button{white-space:nowrap}'),
        W('button', 'Sidebar – Check-In', text='Check-In Now', link={'url': CHECKIN, 'is_external': 'on', 'nofollow': ''},
          selected_icon=icon('fas fa-arrow-right'), icon_align='row-reverse', icon_indent=px(10), border_radius=dims(10),
          text_padding=dims(14, 18), align='justify', background_color='rgba(255,255,255,0.06)', border_border='solid',
          border_width=dims(1.5), border_color='rgba(255,255,255,0.8)', button_background_hover_color='#FFFFFF',
          hover_color='#293A6E', button_text_color='#FFFFFF', g={'typography_typography': 'globals/typography?id=ehbtn'})],
        flex_direction='column', flex_gap=gap(14), padding=dims(28, 24, 28, 24), background_background='gradient',
        background_color='#293A6E', background_color_b='#3E5596', background_gradient_angle=px(160, 'deg'), border_radius=dims(20))
    side = C('Post – Sidebar (sticky)', [recent_card, cta], flex_direction='column', flex_gap=gap(22), padding=dims(0),
             width=px(32, '%'), width_tablet=px(100, '%'),
             custom_css='@media(min-width:1025px){selector{position:sticky;top:30px;align-self:flex-start}}')
    row = C('Post – Row', [main, side], flex_direction='row', flex_direction_tablet='column', flex_gap=gap(32),
            flex_wrap='nowrap', flex_align_items='flex-start', padding=dims(0), width=px(1240), width_tablet=px(100, '%'),
            custom_css='selector{max-width:100%}')
    body = C('Post Body', [row], inner=False, flex_direction='column', flex_align_items='center',
             padding=dims(60, 20, 100, 20), padding_tablet=dims(48, 24, 80, 24), padding_mobile=dims(28, 12, 64, 12),
             background_background='classic', background_color='#F7F9FC',
             custom_css='selector{overflow:visible !important}')
    return [hero, body]


def mcp(ability, params):
    r = subprocess.run([os.path.join(D, 'mcp.sh'), ability, json.dumps(params)], capture_output=True, text=True).stdout
    return json.loads(r)


if __name__ == '__main__':
    what = sys.argv[1]; force = '--force' in sys.argv
    ids = json.load(open(IDS_FILE))
    if what == 'listing':
        cur = _api('GET', f'wp/v2/pages/{NEWS_ID}?context=edit&_fields=meta')['meta'].get('_elementor_data')
        if cur and cur != '[]' and not force:
            raise SystemExit('News page already has Elementor data – patch it instead')
        put(NEWS_ID, listing(), post_extra={'template': 'elementor_header_footer'}); regen(NEWS_ID)
    elif what == 'single':
        pid = ids.get('single-post')
        if pid and not force:
            raise SystemExit(f'single-post template {pid} exists – patch it instead (or --force)')
        if not pid:
            r = mcp('elementor/manage-site-parts', {'operations': [{'action': 'create', 'type': 'single-post',
                     'title': 'EHMC Single Post', 'conditions': ['include/singular/post']}]})
            print(r); pid = r['data']['results'][0]['id']
            ids['single-post'] = pid; json.dump(ids, open(IDS_FILE, 'w'), indent=1)
        put(pid, single(), post_extra={'_type': 'lib'})
        print(mcp('elementor/publish-document', {'post_id': pid}))
        regen(pid); print('single-post', pid)
