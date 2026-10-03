"""Theme Builder parts for Astra: header/footer wrappers (embed library templates 4486/4487) + Single Post template.
Static texts reused from the old single template 4074 ('Recent Post', 'Get Immediate Towing', global form 3358)."""
from lib import *
import json

def tag(name, settings=None):
    s = json.dumps(settings or {}).replace('"', '%22').replace(' ', '')
    return f'[elementor-tag id="{rid()}" name="{name}" settings="{s}"]'

def wrapper(tid, cls):
    seed('wrap-' + cls)
    return [{'id': rid(), 'elType': 'container', 'isInner': False, 'settings': {'content_width': 'full', 'css_classes': 'bp ' + cls},
             'elements': [W('template', '', template_id=tid)]}]

def single():
    seed('single-post')
    info = W('post-info', 'bp-postinfo', icon_list=[
        {'_id': rid(), 'type': 'terms', 'taxonomy': 'category', 'selected_icon': ICO('tag'), 'link': ''},
        {'_id': rid(), 'type': 'date', 'selected_icon': ICO('calendar-alt'), 'link': ''},
        {'_id': rid(), 'type': 'time', 'selected_icon': ICO('clock', 'fa-regular'), 'link': ''}], view='inline')
    title = W('theme-post-title', 'bp-h bp-h1', header_size='h1', __dynamic__={'title': tag('post-title')})
    hero = SEC([C([info, title], 'bp-phero-copy bp-post-head')], 'bp-phero bp-post-hero bp-sec',
               background_background='classic', background_size='cover', background_position='center center',
               __dynamic__={'background_image': tag('post-featured-image')})
    content = C([W('theme-post-content', 'bp-prose')], 'bp-post-main')
    form_tpl = tree(3358)[0]
    aside = C([
        C([W('heading', 'bp-h bp-h3', title='Get Immediate Towing', header_size='div'),
           FORM(3358, form_tpl['id'], widths=[100, 100, 100, 100, 100])], 'bp-formcard bp-glass bp-spot bp-on-dark bp-post-form'),
        C([W('heading', 'bp-h bp-h3', title='Recent Post', header_size='div'),
           W('posts', 'bp-recent', _skin='classic', classic_columns='1', classic_columns_tablet='2', classic_columns_mobile='1',
             classic_posts_per_page=4, classic_thumbnail='left', classic_thumbnail_size_size='thumbnail',
             classic_item_ratio={'unit': 'px', 'size': 1}, classic_image_width={'unit': '%', 'size': 32},
             classic_show_title='yes', classic_title_tag='div', classic_meta_data=['date'], classic_show_excerpt='',
             classic_show_read_more='', posts_post_type='post', posts_exclude=['current_post'])], 'bp-post-recent bp-glass-light')],
        'bp-post-aside')
    body = SEC([content, aside], '', row=True, css_classes='bp bp-sec bp-soft bp-post-body bp-row bp-g48')
    return [hero, body]
