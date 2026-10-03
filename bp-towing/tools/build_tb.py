"""Theme Builder templates for Astra: Archive (category/tag/date/author), Search Results, 404."""
from lib import *
import build_single as bsg, build_hf

TEL = 'tel:+14039912265'
tag = bsg.tag

def posts_grid(widget='archive-posts'):
    return W(widget, 'bp-archive', _skin='classic', classic_columns='3', classic_columns_tablet='2', classic_columns_mobile='1',
             classic_thumbnail='top', classic_thumbnail_size_size='medium_large', classic_item_ratio={'unit': 'px', 'size': 0.62},
             classic_show_title='yes', classic_title_tag='h2', classic_show_excerpt='yes', classic_excerpt_length=18,
             classic_meta_data=['date'], classic_show_read_more='yes', classic_read_more_text='Read More',
             pagination_type='numbers_and_prev_next', pagination_prev_label='« Previous', pagination_next_label='Next »',
             nothing_found_message="It seems we can't find what you're looking for.")

def search_form(cls='bp-search'):
    return W('search-form', cls, skin='classic', placeholder='Search...', button_type='icon', icon='search', size='md')

def archive():
    seed('tb-archive')
    hero = SEC([C([W('theme-archive-title', 'bp-h bp-h1', header_size='h1', __dynamic__={'title': tag('archive-title', {'include_context': 'yes'})})],
                  'bp-phero-copy bp-post-head')], 'bp-phero bp-post-hero bp-aura bp-gridbg bp-sec')
    return [hero, SEC([posts_grid()], 'bp-sec bp-soft bp-archive-sec')]

def search():
    seed('tb-search')
    hero = SEC([C([W('theme-archive-title', 'bp-h bp-h1', header_size='h1', __dynamic__={'title': tag('archive-title', {'include_context': 'yes'})}),
                   search_form('bp-search bp-search-hero')], 'bp-phero-copy bp-post-head')], 'bp-phero bp-post-hero bp-aura bp-gridbg bp-sec')
    return [hero, SEC([posts_grid()], 'bp-sec bp-soft bp-archive-sec')]

def not_found():
    seed('tb-404')
    links = [W('icon-box', 'bp-mega-link bp-404-link', selected_icon=ICO(ic), title_text=t, description_text=dsc, title_size='div',
               link=LINK(SITE + u), position='left') for t, u, ic, dsc in build_hf.SERVICES]
    hero = SEC([C([HTML('<div class="bp-404-num" aria-hidden="true">404</div>'),
                   W('heading', 'bp-h bp-h1', title='Page Not Found', header_size='h1'),
                   T("<p>The page you're looking for doesn't exist or has moved. Try searching, or jump to one of our services below.</p>", 'bp-lead'),
                   search_form('bp-search bp-search-hero'),
                   C([BTN('Back to Home', SITE + '/', 'bp-btn', icon='arrow-right'),
                      BTN('(403) 991-2265', TEL, 'bp-btn bp-btn-glass', icon='phone-alt')], 'bp-btns bp-mid', row=True)],
                  'bp-phero-copy bp-404-copy')], 'bp-phero bp-404 bp-aura bp-gridbg bp-sec')
    grid = SEC([C([W('heading', 'bp-h bp-h2', title='Our Services', header_size='h2')], 'bp-head-c'),
                C(links, 'bp-mega-grid bp-404-grid')], 'bp-sec bp-soft')
    return [hero, grid]
