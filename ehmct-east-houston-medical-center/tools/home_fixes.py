"""Home (32) live patch: flip-card hint removed, Baytown map -> campus image, slider rounded as a whole (no slide edges mid-swipe)."""
import re, sys
from patch import fetch, save, find, titled, walk
from el import W, img, px, dims

doc = fetch(int(sys.argv[1]) if len(sys.argv) > 1 else 32); d = doc['data']

n = 0
for e in walk(d):
    if e.get('widgetType') == 'flip-box':
        s = e['settings']; new = re.sub(r'<span class="ehmc-hint">.*?</span>', '', s.get('description_text_b', ''))
        if new != s.get('description_text_b'): s['description_text_b'] = new; n += 1
print('flip hints removed', n)

card = find(d, titled('Locations – Baytown Card'))
card['elements'] = [e for e in card['elements'] if e['settings'].get('_title') not in
                    ('Locations – Baytown Map (placeholder embed)', 'Locations – Baytown Directions Link', 'Locations – Baytown Campus Image')]
houston_map = find(d, titled('Locations – Houston Map (placeholder embed)'))['settings']
card['elements'].append(W('image', 'Locations – Baytown Campus Image', image=img('baytown_campus'), image_size='full',
                          width=px(100, '%'), height=houston_map.get('height', px(200)), **{'object-fit': 'cover', 'object-position': 'center center'},
                          custom_css='selector img{width:100%;height:200px;object-fit:cover;object-position:center center}',
                          image_border_radius=dims(8), image_border_border='solid', image_border_width=dims(1), image_border_color='#DFE5ED'))

car = find(d, titled('Hero – Slider'))['settings']
SL = ('/*slide-r*/selector .swiper{border-radius:46px;overflow:hidden}selector .swiper-slide > .e-con,selector .swiper-slide.e-con'
      '{border-radius:0 !important}@media(max-width:1024px){selector .swiper{border-radius:46px}}'
      '@media(max-width:767px){selector .swiper{border-radius:26px 26px 0 0}}/*slide-r*/')
car['custom_css'] = (re.sub(r'/\*slide-r\*/.*?/\*slide-r\*/', '', car['custom_css'], flags=re.S).strip() + ' ' + SL).strip()
save(doc)
