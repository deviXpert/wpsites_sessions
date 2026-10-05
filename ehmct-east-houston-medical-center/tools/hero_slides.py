"""Hero slider = 4 slides per Figma (live patch, idempotent):
 1 main artboard photo (EHMC building; desktop 418:4 clean crop, mobile 266:3 clean photo)
 2 glass building (component 222:1226 / 307:2102)   3 building (222:1469 / 307:2104)   4 reception (222:1549 / 307:2161)
usage: python3 hero_slides.py [page_id]   (then run mobile_hero.py hero <page_id> for the mobile crops)
"""
import copy, re, sys
from patch import fetch, save, find, titled
from el import uid, img

pid = int(sys.argv[1]) if len(sys.argv) > 1 else 32
doc = fetch(pid)
car = find(doc['data'], titled('Hero – Slider'))
slides = car['elements']

def bg(key):
    i = img(key); i.update(alt='', size=''); return i

if len(slides) == 3:
    new = copy.deepcopy(slides[0])
    def reid(e):
        e['id'] = uid()
        for c in e['elements']: reid(c)
    reid(new)
    slides[2]['settings']['_title'] = 'Hero – Slide 4'
    slides[1]['settings']['_title'] = 'Hero – Slide 3'
    new['settings']['_title'] = 'Hero – Slide 2'
    slides.insert(1, new)
    car['settings']['carousel_items'].insert(1, {'_id': uid()[:7], 'slide_title': 'Slide #2'})
    for n, it in enumerate(car['settings']['carousel_items'], 1):
        it['slide_title'] = 'Slide #%d' % n
assert len(slides) == 4 and len(car['settings']['carousel_items']) == 4

slides[0]['settings']['background_image'] = bg('hero_slide_1_desktop')
for n in (2, 3, 4):   # Figma 222:1148/1471/1551 (desktop) and 436:1306/1307/1308 (mobile), exported as cropped
    slides[n - 1]['settings']['background_image'] = bg('hero_v4_slide_%d' % n)
    slides[n - 1]['settings']['background_image_mobile'] = bg('hero_v4_slide_%d_mobile' % n)

# Overlays straight from Figma (layer opacity multiplied into the stops)
G1 = 'linear-gradient(90deg,rgba(2,16,34,{0}) 0%,rgba(3,19,39,{1}) 32%,rgba(3,19,39,{2}) 62%,rgba(3,19,39,{3}) 100%)'
OV = {
    # desktop main 418:5 (100%) + 418:6 bottom 54% (rgba(2,13,29,.62) -> 0)
    1: ('linear-gradient(0deg,rgba(2,13,29,.62) 0%,rgba(2,13,29,0) 54%),' + G1.format(.9, .74, .22, .04),
        # mobile main 266:5 (90% layer) + 266:6 (20% tint)
        'linear-gradient(90deg,rgba(6,40,67,.2) 0%,rgba(12,50,105,0) 100%),'
        'linear-gradient(90deg,rgba(2,16,34,.855) 0%,rgba(3,19,39,.81) 67%,rgba(3,19,39,.287) 100%)'),  # handle spans 116% of width
}
for n in (2, 3, 4):
    # desktop 222:1149 (80% layer) + 222:1150 bottom 54%; mobile 307:2046 (80%) + 307:2047 left strip
    OV[n] = ('linear-gradient(0deg,rgba(6,40,67,.62) 0%,rgba(12,50,105,0) 54%),' + G1.format(.72, .592, .176, .032),
             # mobile: Figma's 80% overlay left the busy photos (flag, HOSPITAL sign) behind the headline,
             # so slides 2-4 use the darker main-artboard mobile overlay plus a soft band behind the text block
             'linear-gradient(180deg,rgba(2,16,34,0) 18%,rgba(2,16,34,.45) 30%,rgba(2,16,34,.45) 68%,rgba(2,16,34,0) 80%),'
             'linear-gradient(90deg,rgba(2,16,34,.855) 0%,rgba(3,19,39,.81) 67%,rgba(3,19,39,.287) 100%)')
for n, (desk, mob) in OV.items():
    st = slides[n - 1]['settings']
    css = ('/*ov*/selector::before{background-image:' + desk + ' !important;background-color:transparent !important;opacity:1 !important}'
           '@media(max-width:767px){selector::before{background-image:' + mob + ' !important}}/*ov*/')
    st['custom_css'] = (re.sub(r'/\*ov\*/.*?/\*ov\*/', '', st.get('custom_css', ''), flags=re.S).strip() + ' ' + css).strip()
# desktop/tablet dots per Figma 418:8-11: 18px white(.76) dots, active 38x18 #BE2424, 3px white(.72) ring, 8px gap
import re
DOTS = ('/*d-dots*/@media(min-width:768px){selector .swiper-pagination{display:flex;gap:8px;line-height:0;transform:none !important}'
        'selector .swiper-pagination-bullet{width:18px !important;height:18px !important;margin:0 !important;box-sizing:border-box;'
        'background:rgba(255,255,255,.76) !important;border:3px solid rgba(255,255,255,.72) !important;opacity:1}'
        'selector .swiper-pagination-bullet-active{width:38px !important;border-radius:999px;background:#BE2424 !important}}'
        # aligned with the kicker, 42.8px above it (Figma dots y=328.7, kicker text y=371.5)
        '@media(min-width:1025px){selector .swiper-pagination{left:max(58px,calc((100% - 1440px)/2)) !important;top:322.2px !important}}'
        '@media(min-width:768px) and (max-width:1024px){selector .swiper-pagination{left:36px !important;top:297.2px !important}}/*d-dots*/')
cs = car['settings']
cs['custom_css'] = (re.sub(r'/\*d-dots\*/.*?/\*d-dots\*/', '', cs.get('custom_css', ''), flags=re.S).strip() + ' ' + DOTS).strip()
print([s['settings']['_title'] for s in slides])
save(doc)
