import json, random
from el import *
D = json.load(open('footer_backup_v2.json'))
SVC=[('Abdominal Pain','abdominal-pain'),('Allergic Reactions','allergic-reactions'),('Blood Clots','blood-clots'),('Broken Bones','broken-bones'),('Burns','burns'),('Chest Pain','chest-pain'),('COVID-19','covid-19'),('Diabetic Emergency','diabetic-emergency'),('Difficulty Breathing','difficulty-breathing'),('Flu','flu'),('Fracture','fracture'),('High Fever','high-fever'),('Infection','infection'),('Seizures','seizures'),('Severe Bleeding','severe-bleeding'),('Sore Throat','sore-throat'),('Trauma Injury','trauma-injury')]
QL=[('Home','/'),('About Us','/about-us/'),('Conditions','/#conditions'),('Physicians','/#team'),('Departments','/#departments'),('Patient Reviews','/#reviews'),('Locations','/#locations'),('Contact Us','/#contact')]
MUTED='rgba(220,233,245,0.72)'
LINK_CSS=('selector .elementor-icon-list-item a{transition:color .2s,transform .2s;display:inline-flex}'
          'selector .elementor-icon-list-item a:hover{transform:translateX(4px)}')
def title(t):
    return H(t, 'h4', 'ehh3', 'ehwhite', name='Footer – %s Title' % t, typography_font_size=px(17),
             custom_css='selector .elementor-heading-title{display:inline-block;padding-bottom:10px;position:relative}'
                        'selector .elementor-heading-title::after{content:"";position:absolute;left:0;bottom:0;width:28px;height:2px;background:var(--e-global-color-secondary)}')
def links(name, lst, cols=1, chev=True):
    css = LINK_CSS + ('selector .elementor-icon-list-items{display:block !important;columns:%d;column-gap:22px}selector .elementor-icon-list-item{break-inside:avoid}' % cols if cols>1 else '')
    return W('icon-list', 'Footer – %s Links' % name,
      icon_list=[dict(_id=uid(), text=t, link={'url':u,'is_external':'','nofollow':''},
                      selected_icon=icon('fas fa-angle-right') if chev else {'value':'','library':''}) for t,u in lst],
      space_between=px(10), icon_size=px(11), text_indent=px(8), icon_color='#C9444A', text_color=MUTED, text_color_hover='#FFFFFF',
      icon_typography_typography='custom', icon_typography_font_family='Poppins', icon_typography_font_size=px(14), custom_css=css)
contact = W('icon-list','Footer – Contact Details', icon_list=[
    dict(_id=uid(), text='15149 Wallisville Rd,<br>Houston, TX 77049', selected_icon=icon('fas fa-map-marker-alt'), link={'url':'https://www.google.com/maps/dir/?api=1&destination=15149+Wallisville+Rd+Houston+TX+77049','is_external':'on','nofollow':''}),
    dict(_id=uid(), text='(832) 400-2396', selected_icon=icon('fas fa-phone-alt'), link={'url':'tel:+18324002396','is_external':'','nofollow':''}),
    dict(_id=uid(), text='info@ehmct.com', selected_icon=icon('fas fa-envelope'), link={'url':'mailto:info@ehmct.com','is_external':'','nofollow':''}),
    dict(_id=uid(), text='Open 24 hours, 7 days a week', selected_icon=icon('fas fa-clock'))],
  space_between=px(14), icon_size=px(14), text_indent=px(12), icon_color='#C9444A', text_color=MUTED, text_color_hover='#FFFFFF', icon_self_vertical_align='flex-start',
  icon_typography_typography='custom', icon_typography_font_family='Poppins', icon_typography_font_size=px(14), icon_typography_line_height=px(1.5,'em'),
  custom_css='selector .elementor-icon-list-icon{width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.08);display:flex !important;align-items:center;justify-content:center;flex:0 0 30px;margin-top:-4px;padding:0 !important} selector .elementor-icon-list-icon svg{margin:0 !important;top:0 !important}')
mapw = W('google_maps','Footer – Map', address='East Houston Medical Center, 15149 Wallisville Rd, Houston, TX 77049', zoom=px(14), height=px(150),
  _margin=dims(6,0,0,0), custom_css='selector iframe{border-radius:12px;display:block;filter:saturate(.9)} selector{border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,.12)}')
soc_list=[('fab fa-facebook-f','https://www.facebook.com/easthoustonmct/'),('fab fa-instagram','https://www.instagram.com/easthoustonmedcntr/'),('fab fa-linkedin-in','https://www.linkedin.com/company/east-houston-medical-center'),('fab fa-tiktok','https://www.tiktok.com/@east.houston.medi')]
social = W('social-icons','Footer – Social Links', social_icon_list=[{'_id':uid(),'social_icon':{'value':i,'library':'fa-brands'},'link':{'url':u,'is_external':'on','nofollow':''}} for i,u in soc_list],
  shape='circle', align='left', icon_color='custom', icon_primary_color='rgba(255,255,255,0.08)', icon_secondary_color='#FFFFFF', icon_size=px(15), icon_padding=px(0.75,'em'), icon_spacing=px(10),
  hover_primary_color='#9F3135', hover_secondary_color='#FFFFFF', hover_animation='float', border_border='solid', border_width=dims(1), border_color='rgba(255,255,255,0.15)')
brand = C('Footer – Brand', [
    W('image','Footer – Logo', image=img('ehmc-logo'), image_size='full', width=px(200), align='left',
      custom_css='selector img{background:#fff;padding:12px 16px;border-radius:12px}'),
    T('<p>Expert emergency care and compassionate treatment, available 24/7 when Houston needs it most.</p>','ehsmall', None, name='Footer – Blurb',
      text_color=MUTED, typography_font_size=px(14), typography_line_height=px(1.7,'em')),
    social], flex_gap=gap(20), width=px(25,'%'), width_tablet=px(100,'%'), padding=dims(0))
col = lambda name, kids, w, wt: C('Footer – '+name, kids, flex_gap=gap(18), width=px(w,'%'), width_tablet=px(wt,'%'), width_mobile=px(100,'%'), padding=dims(0))
cols = C('Footer – Columns', [brand,
    col('Quick Links',[title('Quick Links'), links('Quick Links', QL)], 13, 30),
    col('Services',[title('Our Services'), links('Services', [(n,'/%s/'%s) for n,s in SVC], cols=2)], 28, 66),
    col('Visit Us',[title('Visit Us'), contact, mapw], 22, 100)],
  content_width='boxed', flex_direction='row', flex_wrap='nowrap', flex_wrap_tablet='wrap', flex_justify_content='space-between', flex_gap=gap(30,44),
  padding=dims(72,20,48,20), padding_mobile=dims(52,16,36,16))
bottom = C('Footer – Bottom Bar', [
    T('<p>© 2026 East Houston Medical Center. All rights reserved.</p>','ehsmall', None, name='Footer – Copyright', text_color=MUTED, typography_font_size=px(13), _element_width='auto'),
    T('<p><a href="/about-us/">About</a> &nbsp;·&nbsp; <a href="/#locations">Locations</a> &nbsp;·&nbsp; <a href="/#contact">Contact</a></p>','ehsmall', None, name='Footer – Bottom Links',
      text_color=MUTED, typography_font_size=px(13), _element_width='auto', custom_css='selector a{color:inherit} selector a:hover{color:#fff}')],
  content_width='boxed', flex_direction='row', flex_direction_mobile='column', flex_wrap='wrap', flex_justify_content='space-between', flex_align_items='center', flex_gap=gap(10),
  padding=dims(20,20,20,20), border_border='solid', border_width=dims(1,0,0,0), border_color='rgba(255,255,255,0.1)',
  custom_css='selector p{margin:0}')
warn = [e for e in D[1]['elements'] if e.get('widgetType')=='text-editor'][0]
footer = C('Footer', [cols, bottom, warn], inner=False, flex_gap=gap(0), padding=dims(0),
  background_background='classic', background_color='#0B1A3A',
  custom_css='selector{background-image:radial-gradient(900px 400px at 85% 0%,rgba(73,93,152,.35),transparent 70%),radial-gradient(600px 300px at 0% 100%,rgba(159,49,53,.18),transparent 70%)}')
D[1] = footer
put(34, D, post_extra={'_type':'lib'}); regen(34)
