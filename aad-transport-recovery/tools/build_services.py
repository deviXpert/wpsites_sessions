import json, re, os, copy, runpy, random, html
D = os.path.dirname(os.path.abspath(__file__))
BP = runpy.run_path(os.path.join(D, 'build_pages.py'))
G = BP['G']
C, W, H, T, BTN, ICO, RAW, sec, eyebrow, split = (G[k] for k in ('C', 'W', 'H', 'T', 'BTN', 'ICO', 'RAW', 'sec', 'eyebrow', 'split'))
U, PHONE, TEL = G['U'], G['PHONE'], G['TEL']
murl, twotone, crumbs, btnrow, icon_for, plain = (BP[k] for k in ('murl', 'twotone', 'crumbs', 'btnrow', 'icon_for', 'plain'))
CONTACT = U + '/contact/'

# quote form settings from the existing emergency page
_b = BP['Block'](); BP['collect'](json.loads(BP['P'][577]['meta']['_elementor_data']), _b)
FORM = _b.form; FORM.update(selected_button_icon={'value': 'fas fa-paper-plane', 'library': 'fa-solid'}, button_icon_align='row-reverse')

IMGS = {
    'accident-recovery-birmingham': [597, 540, 611, 532, 600],
    'wheel-lift-recovery-birmingham': [578, 576, 574, 573, 503],
    'long-distance-recovery-birmingham': [582, 494, 588, 591, 590],
    'heavy-duty-recovery-birmingham': [594, 593, 537, 590, 538],
    'motorcycle-recovery-birmingham': [595, 545, 594, 593, 605],
    'rv-trailer-recovery-birmingham': [791, 533, 594, 582, 590],
    'commercial-vehicle-towing-birmingham': [537, 593, 590, 538, 494],
    'flat-battery-service-birmingham': [575, 559, 576, 589, 546],
    'flat-tyre-services-birmingham': [540, 586, 604, 585, 561],
    'fuel-delivery-services-birmingham': [536, 534, 494, 501, 535],
    'car-lockout-service-birmingham': [612, 613, 601, 602, 599],
    'roadside-assistance-birmingham': [532, 579, 546, 575, 589],
    'vehicle-transport-birmingham': [563, 567, 564, 566, 562],
}
LINKS = {'Emergency Breakdown Recovery': '/emergency-breakdown-recovery-birmingham/', 'Accident Recovery Birmingham': '/accident-recovery-birmingham/',
         'Flatbed Recovery Birmingham': '/flatbed-recovery-birmingham/', 'Towing Service Birmingham': '/towing-service-birmingham/',
         'Wheel-Lift Recovery': '/wheel-lift-recovery-birmingham/', 'Long-Distance Recovery': '/long-distance-recovery-birmingham/',
         'Heavy-Duty Recovery': '/heavy-duty-recovery-birmingham/', 'Motorcycle Recovery': '/motorcycle-recovery-birmingham/',
         'Commercial Vehicle Towing': '/commercial-vehicle-towing-birmingham/', 'Vehicle Transport Birmingham': '/vehicle-transport-birmingham/',
         'Roadside Assistance': '/roadside-assistance-birmingham/', 'Flat Battery Service': '/flat-battery-service-birmingham/'}

def esc(t): return html.escape(t, quote=False)
def linkify(t, slug):
    t = esc(t)
    for name, path in LINKS.items():
        if slug in path: continue
        if name in t: t = t.replace(name, f'<a href="{U}{path}">{name}</a>', 1)
    return t
def P_(t, slug): return '<p>' + linkify(t, slug) + '</p>'

def is_head(b):
    t = b['text']
    if b['tag'] in ('h1', 'h2', 'h3'): return True
    if b['tag'] != 'p' or b['list']: return False
    if b.get('cell'): return False
    return len(t) < 95 and not re.search(r'[.:,;]$', t) and not re.match(r'(Call |Yes|No[ ,.])', t) and t[0].isupper() and (b['bold'] or len(t.split()) <= 12)

NOTES = re.compile(r'^(Recommended Internal Links|Content & SEO Notes|SEO Details|Focus Keyword|Internal Link|Schema|Suggested Slug|Meta Title)', re.I)
def normalize(blocks):
    out = []
    for b in blocks:
        if NOTES.match(b['text']): break
        if re.match(r'Call:?\s*0?7771', b['text']) and b['tag'] in ('h1', 'h2', 'h3'): continue
        if b.get('cell'):
            if out and out[-1]['tag'] == 'table': t = out[-1]
            else: t = {'tag': 'table', 'text': '', 'rows': [], 'list': None, 'bold': False}; out.append(t)
            r, cidx = b['cell'][1], b['cell'][2]
            while len(t['rows']) <= r: t['rows'].append([])
            t['rows'][r].append(b['text']); continue
        out.append(b)
    while len(out) > 1 and out[-1]['tag'] == 'h1': out.pop()
    from collections import Counter
    cnt = Counter(b['tag'] for b in out[1:] if b['tag'] in ('h1', 'h2'))
    top = 'h2' if cnt.get('h2', 0) >= cnt.get('h1', 0) else 'h1'
    for b in out[1:]:
        if b['tag'] in ('h1', 'h2', 'h3'):
            b['lvl'] = 2 if b['tag'] == top or b['tag'] == 'h1' else 3
    out[0]['lvl'] = 1
    return out

def sections(blocks):
    blocks = normalize(blocks)
    intro, secs, i = [], [], 1
    while i < len(blocks) and not is_head(blocks[i]):
        intro.append(blocks[i]); i += 1
    cur = None; item_mode = False; faq = False
    while i < len(blocks):
        b = blocks[i]; t = b['text']
        q = t.endswith('?') and (b['tag'] == 'p' or faq) and len(t) < 170
        if faq and (q or (b['tag'] == 'p' and b['bold'] and t.endswith('?'))):
            cur['subs'].append({'title': t, 'body': []}); item_mode = True; i += 1; continue
        if is_head(b) or (faq is False and q and cur is not None and re.search(r'FAQ|Frequently', cur['title'], re.I)):
            j = i + 1; n = 0
            while j < len(blocks) and not is_head(blocks[j]): n += 1; j += 1
            prev = blocks[i - 1]
            lvl = b.get('lvl')
            stepish = re.match(r'(Step\s*)?\d+[.:]\s', t)
            if lvl == 2 and not stepish: sub = False
            elif lvl == 3 or stepish: sub = cur is not None
            else: sub = cur is not None and n <= 2 and (item_mode or (prev['tag'] == 'p' and prev['text'].endswith(':')))
            if sub:
                cur['subs'].append({'title': t, 'body': []}); item_mode = True
            else:
                cur = {'title': t, 'body': [], 'subs': [], 'tail': [], 'phead': b['tag'] == 'p'}; secs.append(cur); item_mode = False
                faq = bool(re.search(r'FAQ|Frequently Asked', t, re.I))
        else:
            if cur is None: intro.append(b)
            elif cur['subs'] and item_mode and (faq or not (b['tag'] == 'p' and cur['subs'][-1]['body'] and len(cur['subs'][-1]['body']) >= 2)):
                cur['subs'][-1]['body'].append(b)
            elif cur['subs']:
                cur['tail'].append(b)
            else:
                cur['body'].append(b)
        i += 1
    # merge runs of paragraph-style headings with short bodies into the previous section as cards
    merged = []
    for sc in secs:
        short_ = len(sc['body']) <= 2 and not sc['subs'] and not any(b['tag'] in ('li', 'table') for b in sc['body'])
        if merged and (re.match(r'Call:?\s*0?7771', sc['title'])):
            merged[-1]['tail'] += sc['body']; continue
        if merged and sc.get('phead') and short_ and not re.search(r'FAQ|Frequently', merged[-1]['title'], re.I) and len(merged[-1]['body']) <= 2 and not sc['title'].endswith('?'):
            merged[-1]['subs'].append({'title': sc['title'], 'body': sc['body']}); continue
        merged.append(sc)
    secs = merged
    if not intro and secs and len(secs[0]['body']) <= 3 and not secs[0]['subs']:
        intro = secs[0]['body']; secs = secs[1:]
    return intro, secs

def lists_of(body):
    out, curl = [], None
    for b in body:
        if b['tag'] == 'li':
            if curl is None or curl['type'] != b['list']: curl = {'type': b['list'], 'items': []}; out.append(curl)
            curl['items'].append(b['text'])
        else: curl = None
    return out

def paras(body, slug): return [b['text'] for b in body if b['tag'] != 'li' and not re.fullmatch(r'0?7771 ?004242', b['text'])]

def ul_html(items, slug): return '<ul>' + ''.join(f'<li>{linkify(x, slug)}</li>' for x in items) + '</ul>'

def rich(body, slug):
    out, curl = [], None
    for b in body:
        if b['tag'] == 'li':
            if curl is None: curl = []; out.append(curl)
            curl.append(b['text'])
        else:
            curl = None
            if re.fullmatch(r'0?7771 ?004242', b['text']): continue
            out.append(P_(b['text'], slug))
    return ''.join(x if isinstance(x, str) else ul_html(x, slug) for x in out)

def faq_items(sec_):
    if sec_['subs'] and all(x['title'].endswith('?') for x in sec_['subs']):
        out = [{'q': x['title'], 'a': [b['text'] for b in x['body']]} for x in sec_['subs']]
        if sec_['body'] and '? ' in sec_['body'][0]['text'][:170]:
            qq, a = sec_['body'][0]['text'].split('? ', 1); out.insert(0, {'q': qq + '?', 'a': [a]})
        return [x for x in out if x['a']]
    items, q = [], None
    allb = sec_['body'] + [x for s in sec_['subs'] for x in ([{'tag': 'p', 'text': s['title'], 'bold': True, 'list': None}] + s['body'])] + sec_['tail']
    for b in allb:
        t = b['text']
        if t.endswith('?') and len(t) < 160:
            q = {'q': t, 'a': []}; items.append(q)
        elif '? ' in t[:160] and (q is None or not q['a']) and t.split('? ')[0][0].isupper() and len(t.split('? ')[0]) < 140 and not items:
            qq, a = t.split('? ', 1); items.append({'q': qq + '?', 'a': [a]}); q = items[-1]
        elif q is not None: q['a'].append(t)
    return [x for x in items if x['a']]

class Ctx:
    def __init__(s, slug):
        s.slug = slug; s.imgs = [murl(i) for i in IMGS[slug]]; s.ii = 1; s.flip = True; s.dark = False; s.cardstyle = 0; s.listi = 0; s.alt = 0
    def img(s):
        u = s.imgs[s.ii % len(s.imgs)]; s.ii += 1; return u

def comp_table(sec_, c):
    tb = [b for b in sec_['body'] + sec_['tail'] if b['tag'] == 'table'][0]
    rows = tb['rows']; head, body = rows[0], rows[1:]
    th = ''.join(f'<th>{esc(h)}</th>' for h in head)
    trs = ''.join('<tr>' + ''.join(f'<td>{esc(x)}</td>' for x in r) + '</tr>' for r in body)
    rest = [b for b in sec_['body'] + sec_['tail'] if b['tag'] != 'table']
    return sec([eyebrow('SIDE BY SIDE'), H(twotone(esc(sec_['title'])), 'h2', 'x-title rv')] + [T(P_(b['text'], c.slug), 'x-lead rv') for b in rest if b['tag'] == 'p'][:1] +
               [RAW(f'<div class="x-cmp rv"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')] +
               [T(P_(b['text'], c.slug), 'x-note x-note-c rv') for b in rest if b['tag'] == 'p'][1:], 'x-sec-cmp x-sec-center')

def comp_reasons(sec_, items, c):
    ps = paras(sec_['body'] + sec_['tail'], c.slug)
    lists = ''.join(f'<li>{linkify(x, c.slug)}</li>' for x in items)
    return sec([C([C([eyebrow('AT A GLANCE'), H(twotone(esc(sec_['title'])), 'h2', 'x-title')] + [T(P_(p, c.slug), 'x-body') for p in ps[:-1] or ps[:1]] +
                     ([T(P_(ps[-1], c.slug), 'x-note')] if len(ps) > 1 else []), 'x-reasons-intro rv', flex_direction='column'),
                   C([T(f'<ul>{lists}</ul>', 'x-checks')], 'x-reasons-lists rv rv-right', flex_direction='column')], 'x-reasons', flex_direction='row')], 'x-sec-reasons')

def comp_tiles(sec_, items, c):
    ps = paras(sec_['body'] + sec_['tail'], c.slug)
    tiles = C([C([RAW(f'<span class="x-tk-ic"><i class="fas fa-{icon_for(x)}"></i></span>'), H(esc(x), 'p', 'x-tk-t')], f'x-tk x-tk-light rv rv-d{i % 3}', flex_direction='row') for i, x in enumerate(items)], 'x-grid x-grid-tk')
    return sec([eyebrow('GOOD TO KNOW'), H(twotone(esc(sec_['title'])), 'h2', 'x-title rv')] + [T(P_(ps[0], c.slug), 'x-lead rv')] * bool(ps) + [tiles] +
               [T(P_(p, c.slug), 'x-note x-note-c rv') for p in ps[1:]], 'x-sec-tiles x-sec-center')

def comp_split(sec_, c, lists=True):
    c.flip = not c.flip
    return split(c.img(), twotone(esc(sec_['title'])), rich(sec_['body'] + sec_['tail'], c.slug), c.flip,
                 C([BTN('Call Now: ' + PHONE, TEL), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost x-btn-ghost-dark')], 'x-btnrow', flex_direction='row', flex_wrap='wrap') if c.flip else None)

def comp_steps(title, steps, lead, c):
    els = [C([H(f'{i + 1:02d}', 'p', 'x-step-n'), H(esc(t), 'h3', 'x-step-t'), T('<p>' + linkify(d, c.slug) + '</p>', 'x-step-d')], f'x-step rv rv-d{i % 4}', flex_direction='column')
           for i, (t, d) in enumerate(steps)]
    n = len(steps); cols = 3 if n in (3, 5, 6, 9) else 4 if n in (4, 7, 8) else 2
    return sec([eyebrow('HOW IT WORKS'), H(twotone(esc(title)), 'h2', 'x-title rv')] + [T(P_(p, c.slug), 'x-lead rv') for p in lead] +
               [C(els, f'x-steps x-steps-{cols}', flex_direction='row', flex_wrap='wrap')], 'x-sec-how')

def comp_cards(sec_, c):
    subs = sec_['subs']; style = ['fc', 'dark', 'num'][c.cardstyle % 3]; c.cardstyle += 1
    lead = [T(P_(p, c.slug), 'x-lead rv') for p in paras(sec_['body'], c.slug)]
    tail = [T(rich(sec_['tail'], c.slug), 'x-note x-note-c rv')] if sec_['tail'] else []
    head = [eyebrow('GOOD TO KNOW' if style != 'dark' else 'KEY SITUATIONS'), H(twotone(esc(sec_['title'])), 'h2', 'x-title rv')]
    if style == 'fc':
        cards = [C([RAW(f'<span class="x-fc-ic"><i class="fas fa-{icon_for(s["title"])}"></i></span>'), H(esc(s['title']), 'h3', 'x-fc-title'), T(rich(s['body'], c.slug), 'x-fc-text')],
                   f'x-fc rv rv-d{i % 3}', flex_direction='column') for i, s in enumerate(subs)]
        n = len(cards)
        return sec(head + lead + [C(cards, 'x-grid x-grid-fc x-grid-fc' + ('2' if n in (2, 4) else '3'))] + tail, 'x-sec-fc')
    if style == 'dark':
        grid = C([W('icon-box', f'x-wcard rv rv-d{i % 4}', selected_icon=ICO(icon_for(s['title'])), title_text=esc(s['title']), description_text=plain(rich(s['body'], c.slug)), title_size='h3')
                  for i, s in enumerate(subs)], 'x-grid x-grid-4 x-grid-auto', flex_direction='row', flex_wrap='wrap')
        return C([C(head + lead + [grid] + tail, 'x-sec', flex_direction='column', cw='boxed')], 'x-dark', flex_direction='column')
    cards = [C([H(f'{i + 1:02d}', 'p', 'x-nc-n'), C([H(esc(s['title']), 'h3', 'x-nc-title'), T(rich(s['body'], c.slug), 'x-nc-text')], 'x-nc-body', flex_direction='column')],
               f'x-nc rv rv-d{i % 2}', flex_direction='row') for i, s in enumerate(subs)]
    return sec(head + lead + [C(cards, 'x-grid x-grid-nc')] + tail, 'x-sec-nc')

def comp_dests(sec_, items, c):
    tiles = C([C([RAW(f'<i class="fas fa-{icon_for(x)}"></i>'), H(esc(x), 'p', 'x-dest-t')], 'x-dest rv', flex_direction='column') for x in items], 'x-dests', flex_direction='row', flex_wrap='wrap')
    ps = paras(sec_['body'] + sec_['tail'], c.slug)
    return sec([C([eyebrow('WHERE WE CAN TAKE IT'), H(twotone(esc(sec_['title'])), 'h2', 'x-title rv')] + [T(P_(p, c.slug), 'x-lead rv') for p in ps] + [tiles,
                  C([BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-white'), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost')], 'x-btnrow', flex_direction='row', flex_wrap='wrap')],
                 'x-panel', flex_direction='column')], 'x-sec-panel')

def comp_why(sec_, items, c):
    ps = paras(sec_['body'] + sec_['tail'], c.slug)
    tiles = C([C([RAW('<span class="x-tk-ic"><i class="fas fa-check"></i></span>'), H(esc(x), 'p', 'x-tk-t')], f'x-tk rv rv-d{i % 4}', flex_direction='row') for i, x in enumerate(items)],
              'x-grid x-grid-tk')
    inner = [eyebrow('WHY US'), H(twotone(esc(sec_['title'])), 'h2', 'x-title rv')] + ([T(P_(ps[0], c.slug), 'x-lead rv')] if ps else []) + [tiles] + [T(P_(p, c.slug), 'x-lead x-why-tail rv') for p in ps[1:]]
    return C([C(inner, 'x-sec', flex_direction='column', cw='boxed')], 'x-dark', flex_direction='column')

def comp_band(sec_, c):
    ps = paras(sec_['body'] + sec_['tail'], c.slug)
    return sec([C([C([RAW('<span class="x-band-ic"><i class="fas fa-headset"></i></span>'), H(twotone(esc(sec_['title'])), 'h2', 'x-band-title')] + [T(P_(p, c.slug), 'x-band-text') for p in ps],
                     'x-band-copy', flex_direction='column'),
                   C([RAW(f'<a class="x-band-phone" href="{TEL}"><small>24/7 Recovery Line</small>{PHONE}</a>'), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost')], 'x-band-cta', flex_direction='column')],
                  'x-band rv', flex_direction='row')], 'x-sec-band')

def comp_areas(sec_, items, c):
    ps = paras(sec_['body'] + sec_['tail'], c.slug)
    chips = C([H(esc(a), 'p', 'x-area') for a in items], 'x-areas', flex_direction='row', flex_wrap='wrap')
    return sec([C([C([eyebrow('COVERAGE'), H(twotone(esc(sec_['title'])), 'h2', 'x-title')] + [T(P_(p, c.slug), 'x-body') for p in ps] + [chips], 'x-area-copy rv', flex_direction='column'),
                   C([W('image', 'x-media', image={'url': c.img(), 'id': ''}, image_size='full')], 'x-media-wrap rv rv-right')], 'x-split', flex_direction='row')], 'x-sec-area')

def comp_text(sec_, c):
    c.flip = not c.flip
    return sec([C([C([H(twotone(esc(sec_['title'])), 'h2', 'x-title rv'), T(rich(sec_['body'] + sec_['tail'], c.slug), 'x-body x-prose-sm rv')], 'x-tb-copy', flex_direction='column'),
                   C([W('image', 'x-tb-img', image={'url': c.img(), 'id': ''}, image_size='full')], 'x-tb-media rv rv-right')], 'x-textblock x-textblock-img' + (' x-tb-rev' if c.flip else ''), flex_direction='row')], 'x-sec-text')

def build(pg):
    slug = pg['slug']; random.seed(slug); c = Ctx(slug)
    blocks = pg['blocks']
    h1 = blocks[0]['text'] if blocks and blocks[0]['tag'] == 'h1' else slug
    intro, secs = sections(blocks)
    short = h1.split(' – ')[0].split(' - ')[0]
    lead = [b['text'] for b in intro if not b['text'].startswith(('For ', 'Call ')) or len(intro) < 2][:3]
    hero_copy = [crumbs(esc(short)), T('<p><span class="x-dot"></span> 24/7 Recovery · Birmingham</p>', 'x-badge rv'), H(twotone(esc(h1)), 'h1', 'x-hero-title rv')]
    hero_copy += [T(P_(p, slug), 'x-hero-lead rv') for p in lead]
    hero_copy += [C([BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-pulse'), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost')], 'x-btnrow rv', flex_direction='row', flex_wrap='wrap'),
                  C([W('icon-box', 'x-chip', selected_icon=ICO(i), title_text=t, description_text=d, position='left', title_size='p')
                     for i, t, d in (('clock', 'Availability', '24/7, 365 days'), ('bolt', 'Fast Response', 'Birmingham &amp; West Midlands'), ('shield-alt', 'Fully Insured', 'Experienced operators'))],
                    'x-chips rv', flex_direction='row', flex_wrap='wrap')]
    hero = C([C(hero_copy, 'x-hero-copy', flex_direction='column'),
              C([T('<p><strong>Get A Free <span class="x-hl">Quote</span></strong></p>', 'x-card-title'), T("<p>Tell us what's happened — we'll call you back within minutes.</p>", 'x-card-sub'), W('form', 'x-form', **copy.deepcopy(FORM))],
                'x-hero-card rv rv-right', flex_direction='column', _element_id='contact-form')], 'x-hero', flex_direction='row', cw='boxed')
    out = [RAW('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">'
               f'<style>.x-root.x-page .x-hero{{background-image:url({c.imgs[0]})!important}}</style>'), hero]
    faqs = []
    for k, s in enumerate(secs):
        title = s['title']; lst = lists_of(s['body'] + s['tail']); ps = paras(s['body'] + s['tail'], slug)
        last = k == len(secs) - 1
        if re.search(r'FAQ|Frequently', title, re.I):
            faqs = faq_items(s); continue
        if last or (title.startswith('Need ') and title.endswith('?')):
            out.append(('CTA', s)); continue
        if any(b['tag'] == 'table' for b in s['body'] + s['tail']):
            out.append(comp_table(s, c)); continue
        if s['title'].startswith('Get ') and not s['body'] and k + 1 < len(secs):
            nxt = secs[k + 1]; nxt['title'] = s['title'].replace('Get ', 'Need ', 1).rstrip('?') + '?' if False else nxt['title']
            out.append(('CTA', {'title': s['title'], 'body': [{'tag': 'p', 'text': nxt['title'], 'list': None, 'bold': False}] + nxt['body'], 'tail': nxt['tail'], 'subs': []})); secs[k + 1] = {'title': '__skip', 'body': [], 'subs': [], 'tail': []}; continue
        if s['title'] == '__skip': continue
        ol = [l for l in lst if l['type'] == 'ol']
        numsubs = s['subs'] and all(re.match(r'\d+\.', x['title']) for x in s['subs'])
        if ol or numsubs or re.match(r'How .* Works', title):
            if numsubs: steps = [(re.sub(r'^\d+\.\s*', '', x['title']), plain(rich(x['body'], slug))) for x in s['subs']]
            elif ol: steps = [tuple(x.split('. ', 1)) if '. ' in x[:80] else (x, '') for x in ol[0]['items']]
            else: steps = [(x['title'], plain(rich(x['body'], slug))) for x in s['subs']] or [(x, '') for x in (lst[0]['items'] if lst else [])]
            if steps:
                out.append(comp_steps(title, steps, [p for p in ps if p not in sum((x for x in []), [])][:2] if not numsubs else ps[:2], c)); continue
        if s['subs'] and len(s['subs']) >= 2:
            out.append(comp_cards(s, c)); continue
        items = lst[0]['items'] if lst else []
        if title.startswith('Why Choose') and items:
            out.append(comp_why(s, items, c)); continue
        if items and re.search(r'across|areas?\b|locations', title, re.I) and all(len(x) < 40 for x in items):
            out.append(comp_areas(s, items, c)); continue
        if items and len(items) <= 6 and all(len(x) < 40 for x in items) and re.search(r'garage|destination|taken|location|home', ' '.join(items + ps), re.I) and re.search(r'garage|destination|transport|location', title, re.I):
            out.append(comp_dests(s, items, c)); continue
        if re.search(r'24/7', title) and not items:
            out.append(comp_band(s, c)); continue
        if items:
            style = c.listi % 4; c.listi += 1
            if style == 1: out.append(comp_reasons(s, items, c))
            elif style == 2 and all(len(x) < 70 for x in items): out.append(comp_tiles(s, items, c))
            else:
                sp = comp_split(s, c); c.alt += 1
                if c.alt % 2 == 0: sp['settings']['css_classes'] += ' x-sec-alt'
                out.append(sp)
            continue
        out.append(comp_text(s, c) if c.ii % 2 else comp_split(s, c))
    cta = None
    out2 = []
    if not any(isinstance(x, tuple) for x in out):
        out.append(('CTA', {'title': f'Need {short}?', 'body': [{'tag': 'p', 'text': 'Contact A.A.D Transport & Recovery 24/7 for fast, practical help anywhere in Birmingham and the surrounding areas.', 'list': None, 'bold': False}], 'tail': [], 'subs': []}))
    for x in out:
        if isinstance(x, tuple): cta = x[1]
        else: out2.append(x)
    out = out2
    out.append(copy.deepcopy(G['reviews']))
    if faqs:
        acc = {'tabs': [{'_id': '%07x' % random.getrandbits(28), 'tab_title': esc(q['q']), 'tab_content': ''.join(P_(a, slug) for a in q['a'])} for q in faqs],
               'faq_schema': 'yes', 'selected_icon': ICO('plus'), 'selected_active_icon': ICO('minus'), 'title_html_tag': 'h3'}
        out.append(sec([C([C([eyebrow('FAQs'), H('Frequently Asked <span class="x-hl">Questions</span>', 'h2', 'x-title'), T('<p>Still have a question? Call us any time — day or night.</p>', 'x-body'),
                              BTN('Call Now: ' + PHONE, TEL)], 'x-faq-intro rv', flex_direction='column'), C([W('accordion', 'x-faq', **acc)], 'x-faq-wrap rv rv-right')],
                           'x-split x-split-faq', flex_direction='row')], 'x-sec-faq'))
    if cta:
        ps = paras(cta['body'] + cta['tail'], slug)
        out.append(sec([C([C([H(twotone(esc(cta['title'])), 'h2', 'x-cta-title'), T(''.join(P_(p, slug) for p in ps if not p.startswith('Call ')), 'x-cta-text')], 'x-cta-copy', flex_direction='column'),
                           C([BTN('Call Now: ' + PHONE, TEL, 'x-btn x-btn-white'), BTN('Get A Quote', '#contact-form', 'x-btn x-btn-ghost')], 'x-btnrow', flex_direction='row', flex_wrap='wrap')],
                          'x-cta rv', flex_direction='row')], 'x-sec-cta'))
    return [C(out, 'x-root x-page', flex_direction='column')], short, pg['meta']

if __name__ == '__main__':
    pages = [p for p in json.load(open(f'{D}/doc_pages.json')) if p['slug'] in IMGS]
    res = {}
    for pg in pages:
        data, title, meta = build(pg)
        res[pg['slug']] = {'data': data, 'title': title, 'meta': meta}
        print(pg['slug'], title, len(json.dumps(data)))
    json.dump(res, open(f'{D}/built_services.json', 'w'))
