"""Build the EV-Tron footer (Theme Builder footer site part) with native Elementor V4 elements + nav-menu widgets.
Run: EVTRON_WP_USER=<admin login> python3 build_footer.py"""
import json, urllib.parse, wp
from build_home import el, div, p, h, btn, cfg, st, cl, MONO, SITE

C = json.load(open('created.json'))
FID = C['footer']
cfg.clear(); st.clear(); cl.clear()

ROWS = [('01', 'Chargers', 'footer-chargers'), ('02', 'Help', 'footer-help'), ('03', 'Learn', 'footer-learn'), ('04', 'Legal', 'footer-legal')]

top = div('Footer top', [
    div('Footer CTA', [
        p('Footer eyebrow', 'Ready when you are', ['ev-label'], 'color: var(--ev-accent);'),
        h('Footer title', 'Plug in to simpler home charging.', 'h2', ['ev-h-display'], 'margin-top: 20px; font-size: clamp(36px, 5vw, 64px);'),
        p('Footer lead', 'Buy your charger online, or let a qualified electrician fit it after a free remote survey.', ['ev-lead'], 'margin-top: 20px;'),
        div('Footer buttons', [btn('Footer CTA 1', 'Buy now', '/ev-chargers/evtron-tethered-ev-charger/#configure'), btn('Footer CTA 2', 'Request installation', '/ev-chargers/evtron-tethered-ev-charger/#details', 'ghost')],
            'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px;'),
    ], 'display: flex; flex-direction: column; justify-content: center;'),
    div('Charging clock', [
        div('Clock head', [p('Clock label', 'Smart charging clock · UK time', ['ev-label']), p('Clock live', 'Live', ['ev-label'], 'color: var(--ev-accent);')],
            'display: flex; justify-content: space-between; gap: 12px;'),
        p('Clock fallback', 'UK smart chargers come set to avoid charging in default peak hours: weekdays 8am to 11am and 4pm to 10pm. Outside those hours is usually the best time to plug in.', ['ev-body'], 'margin-top: 20px;'),
        p('Clock source', 'Source: Electric Vehicles (Smart Charge Points) Regulations 2021. Your own tariff’s off-peak times may differ.', ['ev-small'], 'margin-top: 16px;'),
    ], 'padding: 32px; background-color: var(--ev-s1); border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); @media(--mobile){ padding: 20px; }'),
], 'display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr); gap: 80px; align-items: center; @media(--tablet){ grid-template-columns: minmax(0, 1fr); gap: 48px; }')

rows = []
for n, label, slug in ROWS:
    rows.append(div(f'Index {label}', [
        p(f'Index {label} label', f'{n}  {label}', None, MONO + 'font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ev-muted); width: 160px; flex-shrink: 0; padding-top: 10px; @media(--mobile){ width: auto; padding-top: 0; }'),
        el('nav-menu', f'Index {label} menu', {'menu_name': slug, 'layout': 'horizontal', 'pointer': 'none', 'dropdown': 'none', 'toggle': 'none', 'align_items': 'start'},
           'main-menu { font-size: 16px; font-weight: 500; color: #F2EFE9; padding: 10px 14px; }\nmain-menu:hover { color: #3BE37F; }'),
    ], 'display: flex; align-items: flex-start; gap: 24px; padding-top: 18px; padding-bottom: 18px; border-bottom: 1px solid var(--ev-divider); @media(--mobile){ flex-direction: column; gap: 4px; }'))

index = div('Footer index', [
    div('Index rows', rows, 'display: flex; flex-direction: column; border-top: 1px solid var(--ev-divider);'),
    div('Footer contact', [
        p('Contact label', 'Talk to us', ['ev-label']),
        p('Contact emails', '<a href="mailto:sales@evtron.co.uk">sales@evtron.co.uk</a><br><a href="mailto:info@evtron.co.uk">info@evtron.co.uk</a>', None, MONO + 'font-size: 15px; line-height: 1.9; color: var(--ev-text); margin-top: 14px;'),
        p('Contact note', 'Sales and order questions to sales@. Everything else to info@.', ['ev-small'], 'margin-top: 14px;'),
    ], 'display: flex; flex-direction: column; padding: 24px; border: 1px solid var(--ev-divider); border-radius: var(--ev-r-md); align-self: start;'),
], 'display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 48px; margin-top: 96px; @media(--tablet){ grid-template-columns: minmax(0, 1fr); margin-top: 72px; }')

wordmark = el('e-image', 'Footer wordmark', {'image': {'src': {'id': 26}, 'size': 'full'}},
              'width: 100%; height: auto; margin-top: 96px; opacity: 0.07; @media(--mobile){ margin-top: 64px; }')

legal = div('Footer legal', [
    p('Legal company', '[PLACEHOLDER] Company name · Company number · Registered address · VAT status', None, MONO + 'font-size: 12px; color: var(--ev-muted);'),
    p('Legal copy', '© 2026 EV-Tron · Driven by innovation', None, MONO + 'font-size: 12px; color: var(--ev-muted);'),
], 'display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-top: 24px; padding-top: 20px; border-top: 1px dashed var(--ev-control);')

X = div('Site footer', [div('Footer inner', [top, index, wordmark, legal], classes=['ev-container'])],
        'padding-top: 120px; padding-bottom: 32px; padding-left: 0; padding-right: 0; background-color: var(--ev-ink); border-top: 1px solid var(--ev-divider); @media(--mobile){ padding-top: 80px; }', tag='footer')

if __name__ == '__main__':
    r = wp.ability('elementor/build-composition', {'post_id': FID, 'xml_structure': X, 'element_config': cfg, 'style': st, 'classes': cl, 'mode': 'replace_children'})
    print('success', r.get('success'), r.get('message') or '', [w for w in (r.get('warnings') or []) if 'not linked' not in w and 'toggle' not in w][:6])
    print(wp.req('wp-abilities/v1/abilities/elementor/publish-document/run?' + urllib.parse.urlencode({'input[post_id]': FID}), 'DELETE').get('status'))
    # Elementor's nav-menu reads `menu`, not `menu_name`: patch after publishing
    d = wp.req(f'wp/v2/elementor_library/{FID}?context=edit'); data = json.loads(d['meta']['_elementor_data'])
    def walk(e):
        for x in e:
            if x.get('widgetType') == 'nav-menu':
                s = x['settings']; s['menu'] = s.get('menu_name')
                s['custom_css'] = (s.get('custom_css') or '') + '\nselector .elementor-nav-menu--main .elementor-item{font-family:var(--ev-font);}\nselector .elementor-nav-menu--main .elementor-nav-menu > li:first-child > a{padding-left:0}'
            walk(x.get('elements', []))
    walk(data)
    print('menus patched', wp.req(f'wp/v2/elementor_library/{FID}', 'POST', {'meta': {'_elementor_data': json.dumps(data)}}).get('id'))
    wp.req('wp-abilities/v1/abilities/elementor/clear-cache/run', 'DELETE')
