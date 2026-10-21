import json, sys, re
p = json.load(open(sys.argv[1]))
data = json.loads(p['meta']['_elementor_data']) if isinstance(p['meta']['_elementor_data'], str) else p['meta']['_elementor_data']
def txt(s):
    for k in ('title','editor','text','html','description_text','title_text','heading','shortcode'):
        if s.get(k): return re.sub(r'<[^>]+>',' ',str(s[k]))[:70].replace('\n',' ')
    return ''
def walk(els, d=0):
    for e in els:
        s = e.get('settings', {})
        hide = [k.replace('hide_','') for k in ('hide_desktop','hide_tablet','hide_mobile') if s.get(k)]
        tag = s.get('header_size','') if e.get('widgetType')=='heading' else ''
        print('  '*d + f"{e['elType']}:{e.get('widgetType','')} {e['id']} {tag} {'HIDE:'+','.join(hide) if hide else ''} {s.get('css_classes','')} | {txt(s)}")
        walk(e.get('elements', []), d+1)
walk(data)
