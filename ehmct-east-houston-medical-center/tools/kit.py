import json
def px(v,u='px'): return {'unit':u,'size':v,'sizes':[]}
def dims(t,r=None,b=None,l=None,u='px'):
    r=t if r is None else r; b=t if b is None else b; l=r if l is None else l
    return {'unit':u,'top':str(t),'right':str(r),'bottom':str(b),'left':str(l),'isLinked':len({t,r,b,l})==1}
def typo(_id,title,fam,w,size,lh=None,ls=None,tr=None,tsize=None,msize=None,lhu='em',style=None):
    t={'_id':_id,'title':title,'typography_typography':'custom','typography_font_family':fam,'typography_font_weight':str(w),**({'typography_font_size':px(size)} if size else {})}
    if lh is not None: t['typography_line_height']=px(lh,lhu)
    if ls is not None: t['typography_letter_spacing']=px(ls)
    if tr: t['typography_text_transform']=tr
    if tsize: t['typography_font_size_tablet']=px(tsize)
    if msize: t['typography_font_size_mobile']=px(msize)
    if style: t['typography_font_style']=style
    return t
C=lambda i,t,c:{'_id':i,'title':t,'color':c}
S={
 'system_colors':[C('primary','Navy (Primary)','#293A6E'),C('secondary','Emergency Red','#9F3135'),C('text','Body Text','#5F6D82'),C('accent','Dark Ink','#071830')],
 'custom_colors':[C('ehwhite','White','#FFFFFF'),C('ehborder','Border','#DFE5ED'),C('ehlight','Light Blue BG','#EDF3FA'),C('ehreddk','Red Hover','#83272B'),C('ehnavy2','Navy Light (gradient end)','#495D98'),C('ehpink','Soft Red Tint','#F8ECED'),C('ehsurf','Card Surface','#F6F8FB'),C('ehmuted','Muted Light Text','#DCE9F5')],
 'system_typography':[typo('primary','Headings','Poppins',700,None),typo('secondary','Subheadings','Poppins',600,18,1.3),typo('text','Body','Poppins',400,16,1.65),typo('accent','Buttons','Poppins',700,16,1.2)],
 'custom_typography':[
  typo('ehh1','Hero H1','Poppins',700,74,0.92,-4,'uppercase',56,40),
  typo('ehh2','Section Title (H2)','Poppins',700,56,1.1,-2,None,42,32),
  typo('ehh4','Hero Kicker','Poppins',700,24,1.35,None,None,20,18),
  typo('ehh3','Card Title','Poppins',600,18,1.3,-0.6,None,17,17),
  typo('ehserif','Serif Card Title','Gelasio',700,25,1.05,None,None,23,22),
  typo('eheye','Eyebrow','Poppins',700,12,1.6,2.4,'uppercase'),
  typo('ehbody','Body','Poppins',400,16,1.65,None,None,None,15),
  typo('ehsmall','Small Text','Poppins',400,13.4,1.6),
  typo('ehlabel','Label / Nav','Poppins',600,14,1.5),
  typo('ehstat','Stat Number','Poppins',600,24,1.1),
  typo('ehbtn','Button','Poppins',700,16,1.2),
 ],
 'default_generic_fonts':'Sans-serif',
 'body_color':'#5F6D82','body_typography_typography':'custom','body_typography_font_family':'Poppins','body_typography_font_size':px(16),'body_typography_font_weight':'400','body_typography_line_height':px(1.65,'em'),
 'link_normal_color':'#293A6E','link_hover_color':'#9F3135',
 'h1_color':'#293A6E','h1_typography_typography':'custom','h1_typography_font_family':'Poppins','h1_typography_font_weight':'700',
 'h2_color':'#293A6E','h2_typography_typography':'custom','h2_typography_font_family':'Poppins','h2_typography_font_weight':'700',
 'h3_color':'#293A6E','h3_typography_typography':'custom','h3_typography_font_family':'Poppins','h3_typography_font_weight':'600',
 'h4_color':'#293A6E','h4_typography_typography':'custom','h4_typography_font_family':'Poppins','h4_typography_font_weight':'600',
 'button_typography_typography':'custom','button_typography_font_family':'Poppins','button_typography_font_weight':'700','button_typography_font_size':px(16),
 'button_text_color':'#FFFFFF','button_background_color':'#9F3135','button_hover_text_color':'#FFFFFF','button_hover_background_color':'#83272B',
 'button_border_radius':dims(10),'button_padding':dims(14,26),
 'button_box_shadow_box_shadow_type':'yes','button_box_shadow_box_shadow':{'horizontal':0,'vertical':12,'blur':28,'spread':0,'color':'rgba(158,63,66,0.26)'},
 'form_label_typography_typography':'custom','form_label_typography_font_family':'Poppins','form_label_typography_font_weight':'700','form_label_typography_font_size':px(12),'form_label_color':'#293A6E',
 'form_field_typography_typography':'custom','form_field_typography_font_family':'Poppins','form_field_typography_font_size':px(14),
 'form_field_text_color':'#071830','form_field_background_color':'#F6F8FB','form_field_border_border':'solid','form_field_border_width':dims(1),'form_field_border_color':'#DFE5ED','form_field_border_radius':dims(10),'form_field_padding':dims(12,14),
 'form_field_focus_border_color':'#293A6E','form_field_focus_background_color':'#FFFFFF',
 'container_width':px(1440),'container_padding':dims(0,20),'space_between_widgets':{'column':'16','row':'16','isLinked':True,'unit':'px'},
 'viewport_tablet':1024,'viewport_mobile':767,
}
for t in S['custom_typography']:
    if t['_id']=='ehh1': t['typography_letter_spacing_tablet']=px(-3); t['typography_letter_spacing_mobile']=px(-1.5)
    if t['_id']=='ehh2': t['typography_letter_spacing_tablet']=px(-1.5); t['typography_letter_spacing_mobile']=px(-1)
json.dump({'meta':{'_elementor_page_settings':S}},open('kit_payload.json','w'))
