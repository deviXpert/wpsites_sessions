"""Global Colors / Fonts / theme style for the Elementor Default Kit (post 5). Run: python3 kit.py  (writes through MCP so kit CSS regenerates)."""
import json, subprocess, os
def px(v,u='px'): return {'unit':u,'size':v,'sizes':[]}
def dims(t,r=None,b=None,l=None,u='px'):
    r=t if r is None else r; b=t if b is None else b; l=r if l is None else l
    return {'unit':u,'top':str(t),'right':str(r),'bottom':str(b),'left':str(l),'isLinked':len({t,r,b,l})==1}
def typo(_id,title,fam,w,size,lh=None,ls=None,tr=None,tsize=None,msize=None,lhu='em'):
    t={'_id':_id,'title':title,'typography_typography':'custom','typography_font_family':fam,'typography_font_weight':str(w)}
    if size: t['typography_font_size']=px(size)
    if lh is not None: t['typography_line_height']=px(lh,lhu)
    if ls is not None: t['typography_letter_spacing']=px(ls)
    if tr: t['typography_text_transform']=tr
    if tsize: t['typography_font_size_tablet']=px(tsize)
    if msize: t['typography_font_size_mobile']=px(msize)
    return t
C=lambda i,t,c:{'_id':i,'title':t,'color':c}
HF,BF,SF='Sora','DM Sans','Cinzel'
INK,GOLD,TEXT,BLUE='#0E1420','#C9A24B','#4B5565','#2B5EA7'
S={
 'system_colors':[C('primary','Ink (Primary)',INK),C('secondary','Gold (Secondary)',GOLD),C('text','Body Text',TEXT),C('accent','Steel Blue (Accent)',BLUE)],
 'custom_colors':[C('qwink2','Ink Card','#161E2D'),C('qwgoldlt','Gold Light','#E8CC84'),C('qwgolddk','Gold Dark','#A9822F'),C('qwbluedk','Blue Dark','#1C3F74'),
                  C('qwcream','Cream BG','#F7F4EC'),C('qwlight','Light BG','#EEF2F7'),C('qwwhite','White','#FFFFFF'),C('qwborder','Border','#E3E6EC'),C('qwmuted','Muted (on dark)','#A9B3C4'),C('qwline','Line (on dark)','#2A3448')],
 'system_typography':[typo('primary','Headings',HF,700,None),typo('secondary','Subheadings',HF,600,20,1.3),typo('text','Body',BF,400,17,1.7),typo('accent','Buttons',HF,600,15,1.2)],
 'custom_typography':[
  typo('qwh1','Hero H1',HF,700,58,1.08,-1.5,None,44,33),
  typo('qwh2','Section Title (H2)',HF,700,42,1.15,-1,None,34,27),
  typo('qwh3','Card Title (H3)',HF,600,21,1.3,-0.3,None,20,19),
  typo('qweye','Eyebrow (serif)',SF,700,14,1.5,3,'uppercase',None,12),
  typo('qwtag','Tagline (serif)',SF,600,22,1.45,1,'uppercase',19,16),
  typo('qwbody','Body',BF,400,17,1.7,None,None,None,16),
  typo('qwlead','Lead',BF,400,19,1.65,None,None,18,17),
  typo('qwsmall','Small',BF,400,14,1.6),
  typo('qwbtn','Button',HF,600,15,1.2,0.3),
  typo('qwstat','Stat Number',HF,700,46,1,None,None,40,34),
  typo('qwnav','Nav',HF,500,15,1.2),
 ],
 'default_generic_fonts':'Sans-serif',
 'body_color':TEXT,'body_typography_typography':'custom','body_typography_font_family':BF,'body_typography_font_size':px(17),'body_typography_font_weight':'400','body_typography_line_height':px(1.7,'em'),
 'link_normal_color':BLUE,'link_hover_color':'#A9822F',
 **{f'h{i}_color':INK for i in range(1,7)},
 **{k:v for i in range(1,7) for k,v in ((f'h{i}_typography_typography','custom'),(f'h{i}_typography_font_family',HF),(f'h{i}_typography_font_weight','700' if i<3 else '600'))},
 'button_typography_typography':'custom','button_typography_font_family':HF,'button_typography_font_weight':'600','button_typography_font_size':px(15),
 'button_text_color':INK,'button_background_color':GOLD,'button_hover_text_color':INK,'button_hover_background_color':'#E8CC84',
 'button_border_radius':dims(4),'button_padding':dims(16,28),
 'form_label_typography_typography':'custom','form_label_typography_font_family':HF,'form_label_typography_font_weight':'600','form_label_typography_font_size':px(13),'form_label_color':INK,
 'form_field_typography_typography':'custom','form_field_typography_font_family':BF,'form_field_typography_font_size':px(15),
 'form_field_text_color':INK,'form_field_background_color':'#FFFFFF','form_field_border_border':'solid','form_field_border_width':dims(1),'form_field_border_color':'#D7DCE4','form_field_border_radius':dims(4),
 'form_field_focus_border_color':GOLD,
 'container_width':px(1440),'container_padding':dims(0,20),'space_between_widgets':{'column':'16','row':'16','isLinked':True,'unit':'px'},
 'page_title_selector':'h1.entry-title','viewport_tablet':1024,'viewport_mobile':767,
 'custom_css':'''/* Quality Waterproofing – global helpers (Site Settings > Custom CSS) */
/* Highlighted words inside headings: <span class="qw-hl">…</span> */
.qw-hl{color:#A9822F}
.qw-dark .qw-hl{color:#D9B661}
.qw-dark .qw-light .qw-hl{color:#A9822F}
.qw-hl-ink{color:#1C3F74}
/* Hero form card sits above the video */
.qw-hero .elementor-background-video-container{opacity:.9}
/* Smooth lift on light cards */
.qw-light{transition:transform .35s ease,box-shadow .35s ease}
.qw-light:hover{transform:translateY(-4px)}
@media (prefers-reduced-motion:reduce){.qw-light,.qw-light:hover{transition:none;transform:none}}
''',
 'site_name':'Quality Waterproofing','site_description':'Basement Waterproofing & Foundation Repair in Toronto & the GTA',
}
if __name__=='__main__':
    r=subprocess.run([os.path.dirname(os.path.abspath(__file__))+'/mcp.sh','elementor/update-page-settings',json.dumps({'post_id':5,'settings':S})],capture_output=True,text=True)
    print(r.stdout[:500],r.stderr[:300])
