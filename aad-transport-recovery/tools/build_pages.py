import json, re, os, copy, runpy, sys
D = os.path.dirname(os.path.abspath(__file__))
G = runpy.run_path(os.path.join(D, 'build.py'))  # reuse helpers from the home build
C, W, H, T, BTN, ICO, RAW, sec, eyebrow, split = (G[k] for k in ('C', 'W', 'H', 'T', 'BTN', 'ICO', 'RAW', 'sec', 'eyebrow', 'split'))
U, PHONE, TEL = G['U'], G['PHONE'], G['TEL']
P = {p['id']: p for p in json.load(open(f'{D}/wp-backup/pages.json'))}
M = {m['id']: m for m in json.load(open(f'{D}/wp-backup/media.json'))}
CONTACT = U + '/contact/'

def murl(i):
    m = M.get(i)
    if not m: return None
    s = m['media_details'].get('sizes', {})
    return (s.get('large') or {}).get('source_url', m['source_url'])

def val(v):
    return v.get('value') if isinstance(v, dict) and '$$type' in v else v

def clean(html):
    html = re.sub(r'</?(section|div)[^>]*>', '', html or '')
    html = re.sub(r'\s(style|data-dc-tpl|aria-level)="[^"]*"', '', html)
    html = re.sub(r'<span>(.*?)</span>', r'\1', html, flags=re.S)
    return html.strip()

def plain(html): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html or '')).strip()

ICONS = [('24/7|clock|hour|availab|around the clock', 'clock'), ('local|birmingham|based|area', 'map-marked-alt'), ('communicat|talk', 'comments'),
         ('handl|care|safe', 'shield-alt'), ('practical|solution|no-nonsense', 'tools'), ('transport', 'truck-moving'), ('hazard', 'exclamation-triangle'),
         ('position|surround', 'road'), ('call|contact', 'phone-alt'), ('detail|share|information', 'clipboard-list'), ('follow|instruction', 'hands-helping'),
         ('quote|price|cost', 'pound-sign'), ('destination|garage', 'warehouse'), ('problem|fault', 'wrench'), ('condition', 'car-crash'), ('access', 'parking'),
         ('location|collection', 'map-marker-alt'), ('vehicle', 'car'), ('recover', 'truck-pickup')]
def icon_for(t):
    t = t.lower()
    for pat, ic in ICONS:
        if re.search(pat, t): return ic
    return 'check'

class Block:
    def __init__(s):
        s.heads, s.texts, s.imgs, s.btns, s.iboxes, s.icboxes, s.steps, s.cards, s.cols, s.chips = [], [], [], [], [], [], [], [], [], []
        s.acc = s.form = s.map = None

def collect(el, b, depth=0):
    for e in el:
        st, w = e.get('settings', {}), e.get('widgetType')
        if w is None:
            kids = e.get('elements', [])
            kw = [k.get('widgetType') for k in kids]
            hs = [k for k in kids if k.get('widgetType') in ('heading', 'e-heading')]
            txt = [k for k in kids if k.get('widgetType') == 'text-editor']
            if depth > 0 and hs and re.fullmatch(r'0\d', plain(str(val(hs[0]['settings'].get('title'))))):
                b.steps.append((plain(str(val(hs[0]['settings']['title']))), plain(str(val(hs[1]['settings']['title']))) if len(hs) > 1 else '',
                                clean(txt[0]['settings']['editor']) if txt else ''))
                continue
            if depth > 0 and len(hs) == 1 and len(txt) == 1 and len(kids) <= 3 and not any(x in kw for x in ('e-image', 'image', 'form')):
                b.cards.append((plain(str(val(hs[0]['settings']['title']))), clean(txt[0]['settings']['editor'])))
                for k in kids:
                    if k.get('widgetType') in ('e-button', 'button'):
                        t = plain(str(val(k['settings'].get('text'))))
                        if t and t != 'Learn More': b.btns.append(t)
                continue
            if depth > 0 and kids and all(k == 'text-editor' for k in kw) and len(kids) > 1:
                for k in kids: b.cols.append(clean(k['settings']['editor']))
                continue
            if depth > 0 and len(hs) >= 3 and len(hs) == len(kids):
                b.chips += [plain(str(val(h['settings']['title']))) for h in hs]
                continue
            collect(kids, b, depth + 1)
            continue
        if w in ('heading', 'e-heading'):
            t = str(val(st.get('title')))
            b.heads.append((re.sub(r'</?strong>', '', t).strip(), val(st.get('tag')) or st.get('header_size') or 'h2'))
        elif w == 'text-editor':
            h = clean(st.get('editor'))
            if h and h not in b.texts: b.texts.append(h)
        elif w == 'e-paragraph':
            t = str(val(st.get('paragraph')))
            if 'Get a free Quote' in t or 'call you back within minutes' in t: continue
            b.texts.append('<p>' + t + '</p>')
        elif w == 'e-image':
            try: b.imgs.append(val(val(val(st['image'])['src'])['id']))
            except Exception: pass
        elif w in ('e-button', 'button'):
            t = plain(str(val(st.get('text'))))
            if t and t != 'Learn More': b.btns.append(t)
        elif w == 'image-box':
            b.iboxes.append((st.get('title_text', '').strip(), st.get('description_text', '').strip(), (st.get('image') or {}).get('url')))
        elif w == 'icon-box':
            b.icboxes.append((st.get('title_text', '').strip(), st.get('description_text', '').strip()))
        elif w == 'accordion': b.acc = copy.deepcopy(st)
        elif w == 'form': b.form = copy.deepcopy(st)
        elif w == 'google_maps': b.map = copy.deepcopy(st)
        collect(e.get('elements', []), b, depth + 1)

def btnrow(btns, has_form, cls='x-btnrow rv', dark=False):
    out = []
    for t in dict.fromkeys(btns):
        if 'Call' in t: out.append(BTN('Call Now: ' + PHONE, TEL, 'x-btn' + (' x-btn-white' if dark else '')))
        else: out.append(BTN('Get A Quote', '#contact-form' if has_form else CONTACT, 'x-btn x-btn-ghost' + (' x-btn-ghost-dark' if not dark else '')))
    return C(out, cls, flex_direction='row', flex_wrap='wrap') if out else None

def twotone(t):
    t = t.replace('&amp;', '&').strip().rstrip()
    words = t.split()
    if len(words) < 3: return t.replace('&', '&amp;')
    k = max(1, len(words) // 2)
    return (' '.join(words[:k]) + ' <span class="x-hl">' + ' '.join(words[k:]) + '</span>').replace('& ', '&amp; ')

def hero_block(b, page_title, img):
    h1 = b.heads[0][0] if b.heads else page_title
    copyc = [T('<p><span class="x-dot"></span> 24/7 Recovery · Birmingham</p>', 'x-badge rv'),
             H(twotone(h1), 'h1', 'x-hero-title rv')]
    for t in b.texts: copyc.append(T(t, 'x-hero-lead rv'))
    r = btnrow(b.btns or ['Call', 'Quote'], bool(b.form), 'x-btnrow rv', dark=False)
    if r: copyc.append(r)
    copyc.append(C([W('icon-box', 'x-chip', selected_icon=ICO(i), title_text=t, description_text=d, position='left', title_size='p')
                    for i, t, d in (('clock', 'Availability', '24/7, 365 days'), ('bolt', 'Fast Response', 'Birmingham &amp; West Midlands'), ('shield-alt', 'Fully Insured', 'Experienced operators'))],
                   'x-chips rv', flex_direction='row', flex_wrap='wrap'))
    cols = [C(copyc, 'x-hero-copy', flex_direction='column')]
    if b.form:
        f = b.form; f.update(selected_button_icon={'value': 'fas fa-paper-plane', 'library': 'fa-solid'}, button_icon_align='row-reverse')
        cols.append(C([T('<p><strong>Get A Free <span class="x-hl">Quote</span></strong></p>', 'x-card-title'),
                       T("<p>Tell us what's happened — we'll call you back within minutes.</p>", 'x-card-sub'), W('form', 'x-form', **f)],
                      'x-hero-card rv rv-right', flex_direction='column', _element_id='contact-form'))
    return C(cols, 'x-hero' + ('' if b.form else ' x-hero-slim'), flex_direction='row', cw='boxed', background_background='classic',
             background_image={'url': img, 'id': ''}, background_size='cover')

def crumbs(title):
    return T(f'<p><a href="{U}/">Home</a> <span>/</span> {title}</p>', 'x-crumbs rv')

def icon_cards(items, dark, cls='x-wcard'):
    return C([W('icon-box', f'{cls} rv rv-d{i % 4}', selected_icon=ICO(icon_for(t + ' ' + d)), title_text=t, description_text=d, title_size='h3')
              for i, (t, d) in enumerate(items)], 'x-grid x-grid-4 x-grid-auto', flex_direction='row', flex_wrap='wrap')

def section_for(b, idx, state, page):
    if b.cards and (b.imgs or len(b.cards) == 1) and not b.heads:
        b.heads = [(b.cards[0][0], 'h2')] + [(t, 'h3') for t, _ in b.cards[1:]]
        b.texts = [b.cards[0][1]] + b.texts + [d for _, d in b.cards[1:]]
        b.cards = []
    heads = b.heads
    title = heads[0][0] if heads else ''
    has_form = state['has_form']
    # FAQ
    if b.acc:
        b.acc['faq_schema'] = 'yes'; b.acc['selected_icon'] = ICO('plus'); b.acc['selected_active_icon'] = ICO('minus')
        return sec([C([C([eyebrow('FAQs'), H('Frequently Asked <span class="x-hl">Questions</span>', 'h2', 'x-title'),
                          T('<p>Still have a question? Call us any time — day or night.</p>', 'x-body'), BTN('Call Now: ' + PHONE, TEL)], 'x-faq-intro rv', flex_direction='column'),
                       C([W('accordion', 'x-faq', **b.acc)], 'x-faq-wrap rv rv-right')], 'x-split x-split-faq', flex_direction='row')], 'x-sec-faq')
    # contact info + form
    if b.form and b.icboxes:
        info = []
        for t, d in b.icboxes:
            ic, link = {'Phone': ('phone-alt', TEL), 'Email': ('envelope', 'mailto:general@aadtransportrecovery.co.uk'), 'Address': ('map-marker-alt', 'https://maps.google.com/?q=Walsall+Rd+Birmingham+B42+1TQ')}.get(t, ('info', ''))
            if t == 'Email': d = 'general@aadtransportrecovery.co.uk'
            info.append(W('icon-box', 'x-ccard rv', selected_icon=ICO(ic), title_text=t, description_text=d, title_size='h3', link={'url': link}))
        info.append(C([T('<p><span class="x-dot"></span> Operators standing by 24/7</p>', 'x-live-pill')], 'x-ccard-live rv'))
        f = b.form; f.update(selected_button_icon={'value': 'fas fa-paper-plane', 'library': 'fa-solid'}, button_icon_align='row-reverse')
        return sec([C([C([eyebrow('GET IN TOUCH'), H('Talk To Our <span class="x-hl">Recovery Team</span>', 'h2', 'x-title'),
                          T('<p>Call, email or send the form — we respond fast, day or night.</p>', 'x-body')] + info, 'x-contact-info', flex_direction='column'),
                       C([T('<p><strong>Get A Free <span class="x-hl">Quote</span></strong></p>', 'x-card-title'),
                          T("<p>Tell us what's happened — we'll call you back within minutes.</p>", 'x-card-sub'), W('form', 'x-form', **f)],
                         'x-hero-card x-contact-card rv rv-right', flex_direction='column', _element_id='contact-form')], 'x-split x-split-contact', flex_direction='row')], 'x-sec-contact')
    if b.map and not heads and not b.texts:
        return sec([C([W('google_maps', 'x-map', **{k: v for k, v in b.map.items() if not k.startswith('_')})], 'x-map-wrap x-map-full rv')], 'x-sec-map')
    # steps
    if b.steps:
        steps = [C([H(n, 'p', 'x-step-n'), H(t if t and t.lower() != 'step' else f'Step {n}', 'h3', 'x-step-t'), T(d, 'x-step-d')], f'x-step rv rv-d{i % 4}', flex_direction='column')
                 for i, (n, t, d) in enumerate(b.steps)]
        extra = [T(t, 'x-lead rv') for t in b.texts]
        tail = [H(h, 'p', 'x-step-note rv') for h, _ in heads[1:]]
        return sec([eyebrow('HOW IT WORKS'), H(twotone(title), 'h2', 'x-title rv')] + extra + [C(steps, 'x-steps x-steps-' + str(min(len(steps), 4)), flex_direction='row', flex_wrap='wrap')] + tail, 'x-sec-how')
    # image-box grids
    if b.iboxes:
        withimg = [x for x in b.iboxes if x[2]]
        intro = [T(t, 'x-lead rv') for t in b.texts]
        if withimg:
            cards = [C([W('image', 'x-sc-bg', image={'url': im, 'id': ''}, image_size='full'), RAW(f'<span class="x-sc-num">{i + 1:02d}</span>'),
                        C([H(t, 'h3', 'x-sc-title'), T('<p>' + d + '</p>', 'x-sc-text'),
                           W('button', 'x-sc-go', text='', link={'url': CONTACT, 'custom_attributes': 'aria-label|Enquire about ' + t}, selected_icon=ICO('arrow-right'))], 'x-sc-body', flex_direction='column')],
                       f'x-sc rv rv-d{i % 4}', flex_direction='column') for i, (t, d, im) in enumerate(withimg)]
            return sec([eyebrow('WHAT WE DO'), H(twotone(title), 'h2', 'x-title rv')] + intro + [C(cards, 'x-grid x-grid-sc x-grid-sc3')], 'x-sec-svc')
        numbered = all(re.match(r'\d\.', t) for t, _, _ in b.iboxes)
        items = sorted(b.iboxes, key=lambda x: x[0]) if numbered else b.iboxes
        if numbered:
            steps = [C([H(t.split('.')[0].zfill(2), 'p', 'x-step-n'), H(t.split('.', 1)[1].strip(), 'h3', 'x-step-t'), T('<p>' + d + '</p>', 'x-step-d')], f'x-step rv rv-d{i % 4}', flex_direction='column') for i, (t, d, _) in enumerate(items)]
            return sec([eyebrow('HOW IT WORKS'), H(twotone(title), 'h2', 'x-title rv')] + intro + [C(steps, 'x-steps x-steps-' + str(min(len(steps), 4)), flex_direction='row', flex_wrap='wrap')], 'x-sec-how')
        state['dark'] = not state['dark']
        grid = icon_cards([(t, d) for t, d, _ in items], state['dark'], 'x-wcard' if state['dark'] else 'x-fcard')
        tail = [T(t, 'x-lead rv') for t in b.cols]
        inner = [eyebrow('WHY US' if 'why' in title.lower() else 'GOOD TO KNOW'), H(twotone(title), 'h2', 'x-title rv')] + intro + [grid] + tail
        if state['dark']:
            return C([C(inner, 'x-sec', flex_direction='column', cw='boxed')], 'x-dark', flex_direction='column')
        return sec(inner, 'x-sec-feat')
    # feature cards (sub containers with heading+text)
    if b.cards and len(b.cards) >= 2 and not b.imgs:
        cards = [C([RAW(f'<span class="x-fc-ic"><i class="fas fa-{icon_for(t)}"></i></span>'), H(t, 'h3', 'x-fc-title'), T(d, 'x-fc-text')], f'x-fc rv rv-d{i % 4}', flex_direction='column')
                 for i, (t, d) in enumerate(b.cards)]
        head = [eyebrow('AT A GLANCE'), H(twotone(title), 'h2', 'x-title rv')] if title else []
        return sec(head + [T(t, 'x-lead rv') for t in b.texts] + [C(cards, 'x-grid x-grid-fc x-grid-fc' + str(min(len(cards), 3)))], 'x-sec-fc')
    # area chips / columns
    if b.cols:
        items = []
        for c in b.cols:
            items += [plain(x) for x in re.split(r'<br\s*/?>|</p>|</li>', c) if plain(x)]
        chips = C([H(a, 'p', 'x-area') for a in items], 'x-areas x-areas-center', flex_direction='row', flex_wrap='wrap')
        return sec([eyebrow('COVERAGE' if 'area' in plain(' '.join(b.texts)).lower() or 'birmingham' in title.lower() else 'KEY FACTORS'), H(twotone(title), 'h2', 'x-title rv'),
                    T(b.texts[0], 'x-lead rv') if b.texts else RAW(''), C([chips], 'x-chipbox rv')] + [T(t, 'x-note x-note-c rv') for t in b.texts[1:]], 'x-sec-area x-sec-center')
    # image + text split
    if b.imgs and heads:
        img = murl(b.imgs[0])
        state['flip'] = not state['flip']
        body = ''.join(b.texts)
        extra = btnrow(b.btns, has_form, 'x-btnrow')
        return split(img, twotone(title), body, state['flip'], extra)
    # cta (last block with buttons)
    if b.btns and idx == state['last']:
        return sec([C([C([H(twotone(title).replace('x-hl', 'x-hl'), 'h2', 'x-cta-title'), T(''.join(b.texts), 'x-cta-text')], 'x-cta-copy', flex_direction='column'),
                       btnrow(b.btns, has_form, 'x-btnrow', dark=True)], 'x-cta rv', flex_direction='row')], 'x-sec-cta')
    # destinations chips inside a text block (accident recovery)
    if b.chips:
        chips = C([C([RAW(f'<i class="fas fa-{icon_for(c)}"></i>'), H(c, 'p', 'x-dest-t')], 'x-dest rv', flex_direction='column') for c in b.chips], 'x-dests', flex_direction='row', flex_wrap='wrap')
        r = btnrow(b.btns, has_form, 'x-btnrow rv')
        return sec([C([eyebrow('AFTER AN ACCIDENT'), H(twotone(title), 'h2', 'x-title rv')] + [T(t, 'x-lead rv') for t in b.texts] + [chips] + ([r] if r else []), 'x-panel', flex_direction='column')], 'x-sec-panel')
    # long legal text
    if not heads and b.texts and len(plain(''.join(b.texts))) > 1500:
        return sec([C([C([T('<p class="x-toc-h">On this page</p><nav class="x-toc-list"></nav>', 'x-toc-inner')], 'x-toc', flex_direction='column'),
                       C([T(''.join(b.texts), 'x-prose')], 'x-prose-card rv', flex_direction='column')], 'x-legal', flex_direction='row')], 'x-sec-legal')
    # prose block (heading + text, maybe button, maybe side image)
    content = [H(twotone(title), 'h2', 'x-title rv')] if title else []
    content += [T(t, 'x-body x-prose-sm rv') for t in b.texts]
    for h, _ in heads[1:]: content.append(H(h, 'h3', 'x-sub rv'))
    r = btnrow(b.btns, has_form, 'x-btnrow rv')
    if r: content.append(r)
    return sec([C(content, 'x-textblock', flex_direction='column')], 'x-sec-text')

HERO_IMG = {256: 13, 258: 12, 260: 611, 577: 579, 905: 606, 1001: 611, 1164: 12, 1183: 12}

def build_page(pid, override_blocks=None):
    p = P[pid]
    data = json.loads(p['meta'].get('_elementor_data') or '[]')
    blocks = []
    for top in data:
        b = Block(); collect([top], b); blocks.append(b)
    if override_blocks: blocks = override_blocks
    state = {'flip': True, 'dark': False, 'has_form': any(b.form for b in blocks), 'last': len(blocks) - 1}
    title = p['title']['raw'].split('|')[0].strip()
    img = murl(HERO_IMG[pid])
    hero = hero_block(blocks[0], title, img)
    hero['elements'][0]['elements'].insert(0, crumbs(title))
    out = [RAW(f'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><style>.x-root.x-page .x-hero{{background-image:url({img})!important}}</style>'), hero]
    for i, b in enumerate(blocks[1:], 1):
        out.append(section_for(b, i, state, p))
    return [C(out, 'x-root x-page', flex_direction='column')]

if __name__ == '__main__':
    res = {pid: build_page(pid) for pid in (256, 258, 577, 905, 1001, 1164, 1183)}
    json.dump(res, open(f'{D}/built_pages.json', 'w'))
    print('ok', {k: len(json.dumps(v)) for k, v in res.items()})

def build_services():
    img = murl(611)
    hero = C([C([crumbs('Services'), T('<p><span class="x-dot"></span> 24/7 Recovery · Birmingham</p>', 'x-badge rv'),
                 H('Our <span class="x-hl">Services</span>', 'h1', 'x-hero-title rv'),
                 T(G['te']("Whatever's happened to your vehicle, we provide"), 'x-hero-lead rv'),
                 btnrow(['Call', 'Quote'], False, 'x-btnrow rv')], 'x-hero-copy', flex_direction='column')],
             'x-hero x-hero-slim', flex_direction='row', cw='boxed')
    svc = copy.deepcopy(G['svc'])
    return [C([RAW(f'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><style>.x-root.x-page .x-hero{{background-image:url({img})!important}}</style>'), hero, svc,
               copy.deepcopy(G['reasons']), copy.deepcopy(G['whys']), copy.deepcopy(G['how']), copy.deepcopy(G['reviews']), copy.deepcopy(G['cta'])], 'x-root x-page', flex_direction='column')]

if __name__ == '__main__':
    res = json.load(open(f'{D}/built_pages.json'))
    res['260'] = build_services()
    json.dump(res, open(f'{D}/built_pages.json', 'w'))
    print('services ok')
