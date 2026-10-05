"""Creates the Community Events and Careers pages (content from ehmct.com, EHMC theme).

Only used for the FIRST build. Once a page exists it is live and may be edited in Elementor:
  python3 inner_pages.py events|careers          -> refuses if the page already has Elementor data
  python3 inner_pages.py events|careers --qa     -> writes to QA draft 41 instead
  python3 inner_pages.py careers --rebuild-draft  -> only while the page is still an unpublished draft
Later changes go through patch.py (fetch live data, patch, save).
"""
import json, os, sys, subprocess
from el import C, W, H, T, BTN, EYEBROW, px, dims, gap, img, icon, col, typ, shadow, CARD_SHADOW, put, regen
from patch import _api

IDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inner_ids.json')
YT = 'https://youtu.be/H-A0sAEzRXc'


def banner(title_html, intro, img_key, name):
    title = W('heading', 'Banner – Title', title=title_html, header_size='h1', align='center', align_mobile='center',
              typography_typography='custom', typography_font_family='Poppins', typography_font_weight='700',
              typography_font_size=px(74), typography_font_size_tablet=px(56), typography_font_size_mobile=px(40),
              typography_line_height=px(0.92, 'em'), typography_line_height_mobile=px(1, 'em'),
              typography_letter_spacing=px(-4), typography_letter_spacing_tablet=px(-3), typography_letter_spacing_mobile=px(-1.5),
              typography_text_transform='uppercase', title_color='#FFFFFF',
              custom_css='selector .elementor-heading-title span{color:var(--e-global-color-secondary);}')
    kids = [title]
    if intro:
        kids.append(T('<p>' + intro + '</p>', color='ehwhite', align='center', name='Banner – Intro',
                      _element_width='initial', _element_custom_width=px(760), _element_custom_width_tablet=px(100, '%'),
                      _flex_align_self='center'))
    inner = C(name + ' – Image', kids, flex_direction='column', flex_justify_content='center', flex_align_items='center',
              flex_gap=gap(18), min_height=px(520), min_height_tablet=px(440), min_height_mobile=px(380),
              padding=dims(120, 24, 60, 24), padding_mobile=dims(110, 20, 40, 20),
              background_background='classic', background_image=img(img_key), background_position='center center',
              background_size='cover', background_repeat='no-repeat',
              background_overlay_background='gradient', background_overlay_color='rgba(2,16,34,0.88)',
              background_overlay_color_b='rgba(12,30,58,0.55)', background_overlay_gradient_angle=px(90, 'deg'),
              background_overlay_opacity=px(1),
              border_radius=dims(46), border_radius_mobile=dims(24), overflow='hidden')
    return C(name, [inner], inner=False, padding=dims(10, 10, 0, 10), padding_mobile=dims(8, 8, 0, 8))


def section(title, kids, **s):
    base = dict(flex_direction='column', flex_align_items='center', flex_gap=gap(24),
                padding=dims(100, 20, 100, 20), padding_tablet=dims(70, 24, 70, 24), padding_mobile=dims(56, 16, 56, 16),
                custom_css='selector > .e-con-inner{max-width:1240px}')
    base.update(s)
    return C(title, kids, inner=False, content_width='boxed', **base)


# ---------------------------------------------------------------- Community Events
def events():
    gal = [img('community_event_%02d' % i) for i in range(1, 14)]
    video = W('video', 'Events – Video', youtube_url=YT, video_type='youtube', controls='yes', modestbranding='yes',
              rel='', aspect_ratio='169', _element_width='initial', _element_custom_width=px(1000),
              _element_custom_width_tablet=px(100, '%'), _flex_align_self='center',
              _border_radius=dims(24), _border_radius_mobile=dims(16),
              _box_shadow_box_shadow_type='yes', _box_shadow_box_shadow=CARD_SHADOW,
              custom_css='selector .elementor-wrapper{border-radius:inherit;overflow:hidden}selector{overflow:hidden}')
    gallery = W('gallery', 'Events – Gallery', gallery=gal, gallery_layout='justified', ideal_row_height=px(240),
                ideal_row_height_tablet=px(180), ideal_row_height_mobile=px(130), gap=px(12), gap_mobile=px(8),
                link_to='file', open_lightbox='yes', lazyload='yes', overlay_background='yes',
                overlay_background_color='rgba(41,58,110,0.35)', image_hover_animation='zoom-in',
                content_hover_animation='fade-in', show_all_galleries='', _element_width='initial',
                _element_custom_width=px(100, '%'),
                custom_css='selector .e-gallery-item{border-radius:14px;overflow:hidden}')
    s1 = section('Events Gallery', [
        EYEBROW('Community Events'),
        H('Events <span>Gallery</span>', 'h2', align='center', name='Section Title'),
        video, gallery], flex_gap=gap(28))
    return [banner('Community <span>Events</span>', None, 'community_event_09', 'Events Banner'), s1]


# ---------------------------------------------------------------- Careers
ZOHO_CSS = r"""
<style>
#ehmc-jobs{font-family:Poppins,sans-serif;width:100%;max-width:none;margin:0;padding:0;background:none;box-shadow:none;border:0}#ehmc-jobs .embed_jobs_head2,#ehmc-jobs .embed_jobs_head3{margin:0;padding:0;background:none;box-shadow:none;border:0;width:auto}
#ehmc-jobs .rec_filter_cls{display:flex;justify-content:flex-end;margin:0 0 18px}
#ehmc-jobs .rec-grp-drop{height:46px;padding:0 40px 0 16px;border:1px solid #DFE5ED;border-radius:999px;background:#fff;color:#293A6E;font:600 14px Poppins,sans-serif;cursor:pointer}
#ehmc-jobs .embed_jobs_head3,#ehmc-jobs #rec_job_listing_div{display:block !important;width:100% !important;float:none !important}#ehmc-jobs .rec_job_listing_div_jobs{display:block !important;width:100% !important;float:none !important;flex:none !important;margin:0 !important}#ehmc-jobs .rec_filter_cls{width:100% !important;float:none !important}#ehmc-jobs .rec_job_listing_div_jobs ul,#ehmc-jobs .rec_job_listing_div_jobs li{width:auto !important;float:none !important}#ehmc-jobs .rec_job_listing_div_jobs li::before{display:none !important}
#ehmc-jobs .rec-grp-heading{display:flex;align-items:center;gap:12px;margin:26px 0 16px;padding:0;border:0;font:700 22px/1.3 Poppins,sans-serif;color:#293A6E}
#ehmc-jobs .rec-grp-cnt{display:inline-block;padding:4px 12px;border-radius:999px;background:#F8ECED;color:#9F3135;font:600 13px/1.4 Poppins,sans-serif}
#ehmc-jobs .rec-group{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0;padding:0;list-style:none}
#ehmc-jobs .rec-job-info{position:relative;display:flex !important;flex-direction:column;gap:6px;margin:0;padding:20px 64px 20px 22px;list-style:none;background:#fff;border:1px solid #DFE5ED;border-radius:16px;box-shadow:0 10px 26px rgba(12,30,58,.06);transition:transform .2s,box-shadow .2s,border-color .2s}
#ehmc-jobs .rec-job-info:hover{transform:translateY(-2px);border-color:#C9D3E3;box-shadow:0 16px 34px rgba(12,30,58,.12)}
#ehmc-jobs .rec-job-info::after{content:"";position:absolute;right:20px;top:50%;width:32px;height:32px;margin-top:-16px;border-radius:50%;background:#9F3135 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12h14M13 6l6 6-6 6'/%3E%3C/svg%3E") center/14px no-repeat}
#ehmc-jobs .rec-job-info li{margin:0;padding:0;list-style:none;border:0}
#ehmc-jobs .rec-job-title{order:2}
#ehmc-jobs .rec-job-title a{color:#293A6E !important;font:600 16px/1.4 Poppins,sans-serif;text-decoration:none}
#ehmc-jobs .rec-job-title a::before{content:"";position:absolute;inset:0}
#ehmc-jobs .zrsite_Job_Type{order:1;align-self:flex-start;padding:3px 10px;border-radius:999px;background:#EDF2F9;color:#293A6E;font:600 11px/1.5 Poppins,sans-serif;text-transform:uppercase;letter-spacing:.6px}
#ehmc-jobs .zrsite_Location{order:3;color:#5F6D82;font:400 13.5px/1.5 Poppins,sans-serif;padding-left:20px !important;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239F3135' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z'/%3E%3Ccircle cx='12' cy='9.5' r='2.5'/%3E%3C/svg%3E") left center/14px no-repeat}
@media(max-width:767px){#ehmc-jobs .rec-group{grid-template-columns:1fr}#ehmc-jobs .rec_filter_cls{justify-content:stretch}#ehmc-jobs .rec-grp-drop{width:100%}#ehmc-jobs .rec-grp-heading{font-size:19px}}
</style>
<div id="ehmc-jobs" class="embed_jobs_head"><div class="embed_jobs_head2"><div class="embed_jobs_head3"><div id="rec_job_listing_div"></div></div></div></div>
<script src="https://static.zohocdn.com/recruit/embed_careers_site/javascript/v1.1/embed_jobs.js"></script>
<script>
rec_embed_js.load({widget_id:"rec_job_listing_div",page_name:"Careers",source:"CareerSite",site:"https://ehmct.zohorecruit.com",brand_color:"#293A6E",empty_job_msg:"No current Openings"});
</script>
"""

BENEFITS = [('fas fa-user-friends', 'A professional and collaborative healthcare environment'),
            ('fas fa-chart-line', 'Opportunities for career development and advancement'),
            ('fas fa-shield-alt', 'A commitment to safety, quality, and regulatory compliance'),
            ('fas fa-heartbeat', 'A mission-driven organization focused on community health')]


def benefit(ic, text):
    return W('icon-box', 'Careers – Offer', selected_icon=icon(ic), view='stacked', position='inline-start',
             position_mobile='inline-start', text_align_mobile='left', title_text=text, description_text='', title_size='p',
             icon_size=px(18), icon_padding=px(14), icon_space=px(16), content_vertical_alignment='middle',
             title_bottom_space=px(0), custom_css='selector .elementor-icon-box-description{display:none}selector .elementor-icon-box-title{margin:0}',
             _padding=dims(20, 22), _background_background='classic', _background_color='#FFFFFF',
             _border_border='solid', _border_width=dims(1), _border_color='#DFE5ED', _border_radius=dims(16),
             _element_width='initial', _element_custom_width={'unit': 'custom', 'size': 'calc(50% - 8px)', 'sizes': []},
             _element_custom_width_mobile=px(100, '%'),
             title_typography_typography='custom', title_typography_font_family='Poppins', title_typography_font_weight='600',
             title_typography_font_size=px(15), title_typography_line_height=px(1.45, 'em'),
             g={'primary_color': col('ehlight'), 'secondary_color': col('secondary'), 'title_color': col('primary')})


def careers():
    p1 = ('East Houston Medical Center is committed to delivering high-quality, compassionate care to the communities we serve. '
          'We value skilled professionals who are dedicated to clinical excellence, teamwork, and patient-centered service.')
    p2 = ('Employment opportunities at East Houston Medical Center vary based on organizational needs. To ensure applicants have '
          'access to the <strong>most current and accurate job listings</strong>, all open positions are posted and managed through '
          'our <strong>Job Portal</strong>.')
    p3 = ('Applicants interested in employment opportunities are encouraged to view available positions and submit applications '
          'via our official Indeed page.')
    photo = W('image', 'Careers – Photo', image=img('careers_team_01'), image_size='full', width=px(100, '%'),
              image_border_radius=dims(32), image_border_radius_mobile=dims(20), object_fit='cover',
              height=px(560), height_tablet=px(420), height_mobile=px(260),
              image_box_shadow_box_shadow_type='yes', image_box_shadow_box_shadow=CARD_SHADOW)
    intro = C('Careers – Intro Copy', [
        EYEBROW('Careers', align='left'),
        H('Become A Part Of The <span>Healthcare Revolution!</span>', 'h2', name='Section Title'),
        T('<p>' + p1 + '</p><p>' + p2 + '</p><p>' + p3 + '</p>', name='Careers – Intro Text'),
        BTN('View Open Positions', '#open-positions', name='Careers – Jobs Button')],
        flex_direction='column', flex_align_items='flex-start', flex_gap=gap(18), width=px(50, '%'), width_mobile=px(100, '%'), padding=dims(0))
    s1 = section('Careers Intro', [
        C('Careers – Row', [C('Careers – Photo Col', [photo], width=px(50, '%'), width_mobile=px(100, '%'), padding=dims(0)), intro],
          flex_direction='row', flex_direction_mobile='column', flex_align_items='center', flex_gap=gap(64),
          flex_gap_tablet=gap(36), flex_gap_mobile=gap(28), flex_wrap='nowrap', padding=dims(0))])

    offers = C('Careers – Offers Card', [
        C('Careers – Offers Head', [
            H('View Current Employment Opportunities on our <span>Job Board</span>', 'h3', typo='ehh4', name='Offers Title'),
            T('<p>East Houston Medical Center offers:</p>', name='Offers Lead')],
          flex_direction='column', flex_gap=gap(8), padding=dims(0)),
        C('Careers – Offers Grid', [benefit(i, t) for i, t in BENEFITS], flex_direction='row', flex_wrap='wrap',
          flex_gap=gap(16), padding=dims(0)),
        T('<p><em>Please note that position availability and requirements may change without notice. Only roles currently '
          'posted on Indeed are actively accepting applications.</em></p>', typo='ehsmall', name='Offers Note')],
        flex_direction='column', flex_gap=gap(24), padding=dims(48, 48), padding_tablet=dims(36, 32),
        padding_mobile=dims(28, 20), background_background='classic', border_radius=dims(32), border_radius_mobile=dims(20),
        g={'background_color': col('ehsurf')})
    s2 = section('Careers Offers', [offers], padding=dims(0, 20, 100, 20), padding_tablet=dims(0, 24, 70, 24),
                 padding_mobile=dims(0, 16, 56, 16))

    jobs = W('html', 'Careers – Zoho Job Listing', html=ZOHO_CSS.strip(), _element_width='initial',
             _element_custom_width=px(100, '%'))
    s3 = section('Open Positions', [
        EYEBROW('Open Positions'),
        H('<span>Interested?</span>', 'h2', align='center', name='Section Title'),
        T('<p>Browse our current openings below and apply online.</p>', align='center', name='Section Intro'),
        jobs], _element_id='open-positions', background_background='classic', g={'background_color': col('ehsurf')},
        border_radius=dims(46), border_radius_mobile=dims(24))
    s3 = C('Open Positions – Wrap', [s3], inner=False, padding=dims(0, 10, 0, 10), padding_mobile=dims(0, 8, 0, 8))
    s3['elements'][0]['isInner'] = True
    return [banner('Careers', 'Join a team dedicated to fast, compassionate emergency care for the East Houston community.',
                   'careers_team_01', 'Careers Banner'), s1, s2, s3]


PAGES = {
    'events': dict(title='Community Events', slug='community-events', build=events,
                   excerpt='See photos and video from East Houston Medical Center community events in Houston.'),
    'careers': dict(title='Careers', slug='careers', build=careers,
                    excerpt='Explore careers at East Houston Medical Center and apply to current open positions on our job board.'),
}

if __name__ == '__main__':
    key = sys.argv[1]; qa = '--qa' in sys.argv
    pg = PAGES[key]
    ids = json.load(open(IDS_FILE)) if os.path.exists(IDS_FILE) else {}
    if qa:
        pid = 41
    elif pg['slug'] in ids:
        pid = ids[pg['slug']]
        cur = _api('GET', f'wp/v2/pages/{pid}?context=edit&_fields=status,meta')
        live = cur['meta'].get('_elementor_data')
        draft_ok = '--rebuild-draft' in sys.argv and cur['status'] == 'draft'
        if live and live != '[]' and not draft_ok:
            raise SystemExit(f'{pg["slug"]} ({pid}) already built – patch it with patch.py instead of regenerating')
    else:
        layout = {'ast-site-content-layout': 'full-width-container', 'site-content-style': 'default', 'site-sidebar-layout': 'no-sidebar'}
        r = _api('POST', 'wp/v2/pages', {'title': pg['title'], 'slug': pg['slug'], 'status': 'draft', 'excerpt': pg['excerpt'],
                                          'template': 'elementor_header_footer', 'meta': layout})
        pid = ids[pg['slug']] = r['id']
        json.dump(ids, open(IDS_FILE, 'w'), indent=1)
    put(pid, pg['build'](), post_extra={'template': 'elementor_header_footer'})
    regen(pid)
    print(pg['slug'], pid)
