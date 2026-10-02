"""Internal linking for the AAD site. Patches each published page's LIVE _elementor_data in place (so manual Elementor
edits are kept): service cards/boxes get their service page URL, and the first mention of another service in body
text becomes a link (max one per service, MAX_TEXT per page, never to the page itself); form service dropdowns get
the full service list (current service preselected). Safe to re-run.
Usage:  cd tools && python3 link_pages.py            (dry run: prints what would change)
        python3 link_pages.py --apply"""
import json, re, sys
from wp import req, all as wp_all
from build import U, MENU

MAX_TEXT = 6
SLUGS = [s for _, xs in MENU for _, s, _, _ in xs]
# exact card/box titles (lower-case, '&amp;' -> '&') -> service slug
TITLES = {t.replace('&amp;', '&').lower(): s for _, xs in MENU for t, s, _, _ in xs}
TITLES.update({
    'breakdown recovery': 'emergency-breakdown-recovery-birmingham', 'car breakdown recovery birmingham': 'emergency-breakdown-recovery-birmingham',
    'emergency roadside recovery': 'emergency-breakdown-recovery-birmingham', 'birmingham towing': 'towing-service-birmingham',
    'towing services': 'towing-service-birmingham', 'battery services': 'flat-battery-service-birmingham',
    'flat battery assistance': 'flat-battery-service-birmingham', 'flat battery': 'flat-battery-service-birmingham',
    'tyre & flat tyre services': 'flat-tyre-services-birmingham', 'flat or damaged wheel': 'flat-tyre-services-birmingham',
    'wheel changes': 'flat-tyre-services-birmingham', 'out of fuel': 'fuel-delivery-services-birmingham',
    'fuel delivery services': 'fuel-delivery-services-birmingham', 'vehicle transportation': 'vehicle-transport-birmingham',
    'motorcycle transportation': 'motorcycle-recovery-birmingham', 'car lockout': 'car-lockout-service-birmingham',
})
# body-text phrases per service, longest/most specific first
PHRASES = [
    ('emergency-breakdown-recovery-birmingham', [r'emergency breakdown recovery', r'breakdown recovery']),
    ('commercial-vehicle-towing-birmingham', [r'commercial vehicle towing']),
    ('accident-recovery-birmingham', [r'accident recovery']),
    ('flatbed-recovery-birmingham', [r'flatbed recovery']),
    ('wheel-lift-recovery-birmingham', [r'wheel[- ]lift recovery', r'wheel[- ]lift']),
    ('heavy-duty-recovery-birmingham', [r'heavy[- ]duty recovery']),
    ('motorcycle-recovery-birmingham', [r'motorcycle recovery', r'motorbike recovery']),
    ('rv-trailer-recovery-birmingham', [r'RV (?:&amp;|&|and) trailer recovery', r'caravan recovery']),
    ('long-distance-recovery-birmingham', [r'long[- ]distance recovery']),
    ('towing-service-birmingham', [r'towing services?']),
    ('vehicle-transport-birmingham', [r'vehicle transport(?:ation)?', r'car transport(?:ation)?']),
    ('roadside-assistance-birmingham', [r'roadside assistance']),
    ('flat-battery-service-birmingham', [r'flat batter(?:y|ies)', r'jump[- ]starts?']),
    ('flat-tyre-services-birmingham', [r'flat tyres?', r'punctures?']),
    ('fuel-delivery-services-birmingham', [r'fuel delivery', r'(?:run|ran|running) out of fuel']),
    ('car-lockout-service-birmingham', [r'car lockouts?', r'locked out of your (?:car|vehicle)']),
]
SKIP_TEXT = ('x-eyebrow', 'x-sc-text', 'x-card-sub', 'x-card-title', 'x-hero', 'x-fabout', 'x-fcopy', 'x-flegal', 'x-cta')
url = lambda s: f'{U}/{s}/'
norm = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t).replace('&amp;', '&')).strip().lower()

def walk(els, path=()):
    for e in els:
        yield e, path
        yield from walk(e.get('elements', []), path + (e.get('settings', {}).get('css_classes', '') + ' ' + e.get('settings', {}).get('_css_classes', ''),))

def link_text(html, slug_re, href):
    """Link the first match outside <a>/<h*> tags. Returns (new html, matched text) or (None, None)."""
    parts = re.split(r'(<[^>]+>)', html)
    depth = 0
    for i, p in enumerate(parts):
        if p.startswith('<'):
            if re.match(r'<(a|h[1-6])\b', p, re.I): depth += 1
            elif re.match(r'</(a|h[1-6])>', p, re.I): depth -= 1
            continue
        if depth: continue
        m = re.search(r'(?<![\w-])(' + slug_re + r')(?![\w-])', p, re.I)
        if m:
            parts[i] = p[:m.start()] + f'<a class="x-ilink" href="{href}">{m.group(1)}</a>' + p[m.end():]
            return ''.join(parts), m.group(1)
    return None, None

SERVICE_OPTIONS = '\n'.join(['Please choose a service|'] + [t.replace('&amp;', '&') for _, xs in MENU for t, _, _, _ in xs] + ['Other / Not sure'])
LABEL = {s: t.replace('&amp;', '&') for _, xs in MENU for t, s, _, _ in xs}

def fix_forms(data, self_slug):
    """Every form's service dropdown lists all services; on a service page that service is preselected."""
    log = []
    for e, _ in walk(data):
        if e.get('widgetType') != 'form': continue
        for f in e['settings'].get('form_fields', []):
            if f.get('field_type') != 'select': continue
            want = LABEL.get(self_slug, '')
            if f.get('field_options') != SERVICE_OPTIONS or f.get('field_value', '') != want:
                f['field_options'] = SERVICE_OPTIONS; f['field_value'] = want; f['field_label'] = 'Select Service'
                log.append(f'form  service dropdown -> {len(SERVICE_OPTIONS.splitlines()) - 1} options' + (f', preselected "{want}"' if want else ''))
    return log

FIX_URLS = {'tel:(077)-710-04242': 'tel:07771004242', 'http://www.allaboutcookies.org/': 'https://allaboutcookies.org/', 'http://www.aboutcookies.org/': 'https://www.aboutcookies.org/'}

def fix_links(data):
    """Bad tel: links, outdated http links, and '#contact-form' anchors on pages that have no form (-> Contact page)."""
    log = []
    has_form = any(e['settings'].get('_element_id') == 'contact-form' for e, _ in walk(data))
    fixes = dict(FIX_URLS, **({} if has_form else {'#contact-form': f'{U}/contact/'}))
    def sub(v):
        if isinstance(v, dict): return {k: sub(x) for k, x in v.items()}
        if isinstance(v, list): return [sub(x) for x in v]
        if isinstance(v, str):
            for a, b in fixes.items():
                if v == a or f'"{a}"' in v:
                    log.append(f'link  {a} -> {b}'); v = b if v == a else v.replace(f'"{a}"', f'"{b}"')
        return v
    for e, _ in walk(data): e['settings'] = sub(e.get('settings', {}))
    return log

def process(data, self_slug):
    log = fix_links(data) + fix_forms(data, self_slug)
    here = url(self_slug) if self_slug else None
    linked = lambda: set(re.findall(r'https://maroon-raven-160825\.hostingersite\.com/([a-z0-9-]+)/', json.dumps(data)))
    # 1) cards: x-sc photo cards (arrow button), image-box / icon-box titles, headings in feature cards
    for e, path in walk(data):
        st = e.get('settings', {})
        cls = st.get('css_classes', '')
        if e.get('elType') == 'container' and re.search(r'(^|\s)x-sc(\s|$)', cls):
            ws = [w for w, _ in walk(e.get('elements', []))]
            title = next((w['settings'].get('title', '') for w in ws if w.get('widgetType') == 'heading'), '')
            s = TITLES.get(norm(title))
            btn = next((w for w in ws if 'x-sc-go' in w['settings'].get('_css_classes', '')), None)
            if s and btn and url(s) != here and btn['settings'].get('link', {}).get('url') != url(s):
                btn['settings']['link'] = {**btn['settings'].get('link', {}), 'url': url(s), 'custom_attributes': 'aria-label|Learn more about ' + norm(title).title()}
                log.append(f'card  "{norm(title)}" -> {s}')
        if e.get('widgetType') in ('image-box', 'icon-box'):
            s = TITLES.get(norm(st.get('title_text', '')))
            if s and url(s) != here and (st.get('link') or {}).get('url') != url(s):
                st['link'] = {'url': url(s), 'is_external': '', 'nofollow': ''}
                log.append(f'box   "{norm(st["title_text"])}" -> {s}')
        if e.get('widgetType') == 'heading' and not re.search(r'x-title|x-hero|x-sc-title|x-step', st.get('_css_classes', '')) and any(re.search(r'x-fc\b|x-fcard|x-wcard|x-tile|x-chk', p) for p in path[-2:]):
            s = TITLES.get(norm(st.get('title', '')))
            if s and url(s) != here and (st.get('link') or {}).get('url') != url(s):
                st['link'] = {'url': url(s), 'is_external': '', 'nofollow': ''}
                log.append(f'head  "{norm(st["title"])}" -> {s}')
    # 2) contextual links in body text
    done = linked(); n = 0
    for s, pats in PHRASES:
        if n >= MAX_TEXT: break
        if s == self_slug or s in done: continue
        for e, path in walk(data):
            if e.get('widgetType') != 'text-editor' or any(k in ' '.join(path) + e['settings'].get('_css_classes', '') for k in SKIP_TEXT): continue
            new = None
            for pat in pats:
                new, hit = link_text(e['settings'].get('editor', ''), pat, url(s))
                if new: break
            if new:
                e['settings']['editor'] = new; n += 1
                log.append(f'text  "{hit}" -> {s}')
                break
    return log

if __name__ == '__main__':
    apply = '--apply' in sys.argv
    for p in wp_all('wp/v2/pages?status=publish&context=edit&_fields=id,slug,meta'):
        data = json.loads(p['meta'].get('_elementor_data') or '[]')
        slug = p['slug'] if p['slug'] in SLUGS else None
        log = process(data, slug)
        print(f"\n## {p['id']} {p['slug']}: {len(log)} change(s)"); [print('   ', l) for l in log]
        if log and apply:
            r = req(f"wp/v2/pages/{p['id']}", 'POST', {'meta': {'_elementor_data': json.dumps(data)}})
            print('    saved' if r.get('id') else f'    ERROR {r}')
