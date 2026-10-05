import json, copy, random, subprocess, os, sys
from conds_content import PAGES
from el import put, regen

BASE = json.load(open('frac_data.json'))
FRAC = json.load(open('frac.json'))[0]
MEDIA = json.load(open('media.json'))
P = lambda t: '<p><span style="font-weight: 400;">%s</span></p>' % t
esc = lambda t: t.replace('&', '&amp;')

def walk(e, fn):
    fn(e)
    for c in e['elements']: walk(c, fn)

def build(pg):
    d = copy.deepcopy(BASE)
    seen = []
    def newid(e): e['id'] = '%07x' % random.getrandbits(28)
    for e in d: walk(e, newid)
    hero = d[0]['elements'][0]
    m = MEDIA[pg['img']]
    hero['settings']['background_image'] = {'url': m['url'], 'id': m['id'], 'size': '', 'alt': pg['hero'], 'source': 'library'}
    heads = []
    def collect(e):
        if e.get('widgetType'): seen.append(e)
    for e in d: walk(e, collect)
    W = lambda t, name=None: [e for e in seen if e['widgetType'] == t and (name is None or e['settings'].get('_title') == name)]
    W('heading', 'Hero – Title')[0]['settings']['title'] = '%s <span>ER</span>' % pg['hero']
    sec = d[1]
    for e in sec['elements']:
        if e.get('widgetType') == 'heading': e['settings']['title'] = pg['sym_title']
        if e.get('widgetType') == 'text-editor': e['settings']['editor'] = P(pg['sym_intro'])
    boxes = [e for e in seen if e['widgetType'] == 'icon-box']
    assert len(boxes) == 8
    for b, (t, s) in zip(boxes, pg['symptoms']):
        b['settings']['title_text'] = t; b['settings']['description_text'] = s
    help_col = d[2]['elements'][0]
    eds = [e for e in help_col['elements'] if e.get('widgetType') == 'text-editor']
    eds[0]['settings']['editor'] = P(pg['help_intro'])
    eds[1]['settings']['editor'] = '<ul>' + ''.join('<li><b>%s </b>%s</li>' % (esc(t), s) for t, s in pg['help']) + '</ul>'
    W('text-editor', 'FAQ – Intro')[0]['settings']['editor'] = P(pg['faq_intro'])
    acc = W('nested-accordion')[0]
    for it, (q, a) in zip(acc['settings']['items'], pg['faq']): it['item_title'] = q
    for cont, (q, a) in zip(acc['elements'], pg['faq']):
        cont['settings']['_title'] = 'FAQ – Answer: ' + q
        cont['elements'][0]['settings']['editor'] = P(a)
    return d

def wp(method, path, body=None):
    cmd = ['curl', '-sS', '-X', method, '-u', os.environ['WP_USER'] + ':' + os.environ['WP_APP_PASSWORD'], os.environ['WP_URL'] + '/wp-json/' + path]
    if body is not None: cmd[4:4] = ['-H', 'Content-Type: application/json', '--data-binary', json.dumps(body)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)

ids = json.load(open('cond_ids.json')) if os.path.exists('cond_ids.json') else {}
layout = {k: FRAC['meta'][k] for k in ('ast-site-content-layout', 'site-content-style', 'site-sidebar-layout') if k in FRAC['meta']}
for pg in PAGES:
    if pg['slug'] not in ids:
        r = wp('POST', 'wp/v2/pages', {'title': pg['title'], 'slug': pg['slug'], 'status': 'draft',
                                        'template': FRAC['template'], 'excerpt': pg['meta_desc'], 'meta': layout})
        ids[pg['slug']] = r['id']
        json.dump(ids, open('cond_ids.json', 'w'))
    pid = ids[pg['slug']]
    put(pid, build(pg), {'_elementor_page_settings': FRAC['meta'].get('_elementor_page_settings') or {}},
        {'template': FRAC['template']})
    regen(pid)
print(ids)
