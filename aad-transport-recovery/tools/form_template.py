"""Move the (identical) quote form into one saved Elementor template and replace every page's form widget with a
Template widget pointing at it. Template ID stored in created.json as 'quote_form'. Idempotent.
Usage: python3 form_template.py [--apply] [--backup DIR] [--only PAGE_ID]"""
import sys, os, json, copy, wp
D = os.path.dirname(os.path.abspath(__file__))
apply = '--apply' in sys.argv
bk = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
cf = os.path.join(D, 'created.json'); created = json.load(open(cf))

def find_form(els):
    for e in els:
        if e.get('widgetType') == 'form': return e
        f = find_form(e.get('elements', []))
        if f: return f

SVC = 'form_fields[field_966fc98]'
# preselect the page's service: the Template widget on each page carries data-service="<option>"
PRESELECT = {'id': 'aadqfjs', 'elType': 'widget', 'widgetType': 'html', 'isInner': False, 'elements': [], 'settings': {'html':
    '<script>(function(){function go(){document.querySelectorAll(".x-formtpl[data-service]").forEach(function(w){'
    'var s=w.querySelector(\'select[name="' + SVC + '"]\'),v=w.getAttribute("data-service");'
    'if(s&&v&&!s.value){for(var i=0;i<s.options.length;i++){if(s.options[i].value===v){s.selectedIndex=i;break}}}})}'
    'if(document.readyState!=="loading")go();else document.addEventListener("DOMContentLoaded",go)})();</script>'}}

# 1) the shared template (built from the Contact page form)
tid = created.get('quote_form')
if not tid:
    src = find_form(json.loads(wp.req('wp/v2/pages/1216?context=edit')['meta']['_elementor_data']))
    form = copy.deepcopy(src); form['id'] = 'aadqf01'
    form['settings']['form_name'] = 'Quote Form'
    form['settings']['button_icon_indent'] = {'unit': 'px', 'size': 10}
    data = [{'id': 'aadqfc1', 'elType': 'container', 'isInner': False, 'elements': [form, PRESELECT], 'settings': {
        'content_width': 'full', 'css_classes': 'x-formwrap x-dc e-no-lazyload', 'flex_direction': 'column',
        'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
        'margin': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}}}]
    print('template: create from Contact form', src['id'])
    if apply:
        r = wp.req('wp/v2/elementor_library', 'POST', {'title': 'AAD – Quote Form (shared)', 'status': 'publish', 'meta': {
            '_elementor_template_type': 'container', '_elementor_edit_mode': 'builder', '_elementor_data': json.dumps(data)}})
        if '_err' in r: raise SystemExit(r)
        tid = created['quote_form'] = r['id']; json.dump(created, open(cf, 'w'), indent=1)
        print('template id', tid)

elif '--refresh-template' in sys.argv and apply:  # push the template body again (form from Contact backup/source + script)
    t = json.loads(wp.req(f'wp/v2/elementor_library/{tid}?context=edit')['meta']['_elementor_data'])
    t[0]['elements'] = [el for el in t[0]['elements'] if el['id'] != PRESELECT['id']] + [PRESELECT]
    print('template refresh', tid, wp.req(f'wp/v2/elementor_library/{tid}', 'POST', {'meta': {'_elementor_data': json.dumps(t)}}).get('_err') or 'ok')

# 2) swap each page's form widget for a Template widget
def swap(els, n):
    for i, e in enumerate(els):
        if e.get('widgetType') == 'form':
            svc = next((f.get('field_value') for f in e['settings']['form_fields'] if f.get('custom_id') == 'field_966fc98'), '') or ''
            st = {'template_id': str(tid or 'NEW'), '_css_classes': 'x-formtpl'}
            if svc: st['_attributes'] = 'data-service|' + svc
            els[i] = {'id': e['id'], 'elType': 'widget', 'widgetType': 'template', 'isInner': False, 'elements': [], 'settings': st}
            n[0] += 1
        else: swap(e.get('elements', []), n)
for x in wp.all('wp/v2/pages?context=edit&status=any'):
    raw = x['meta'].get('_elementor_data')
    if not raw or ('--only' in sys.argv and str(x['id']) != sys.argv[sys.argv.index('--only') + 1]): continue
    d = json.loads(raw); n = [0]; swap(d, n)
    if not n[0]: continue
    print('page', x['id'], x['slug'], 'forms ->template:', n[0])
    if bk: os.makedirs(bk, exist_ok=True); json.dump(x, open(f'{bk}/pages-{x["id"]}.json', 'w'))
    if apply:
        r = wp.req(f'wp/v2/pages/{x["id"]}', 'POST', {'meta': {'_elementor_data': json.dumps(d)}})
        if '_err' in r: print('  ERROR', r)
