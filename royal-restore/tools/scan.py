import json, re, sys
from wp import req, all
types = req('wp/v2/types')
res = {}
for k, t in types.items():
    rb = t.get('rest_base'); ns = t.get('rest_namespace', 'wp/v2')
    if not rb or k in ('attachment', 'wp_font_face', 'wp_font_family', 'wp_global_styles'): continue
    items = all(f"{ns}/{rb}?context=edit&status=any")
    if not isinstance(items, list): print(k, 'ERR', str(items)[:120]); continue
    json.dump(items, open(f'backup/{k}.json', 'w'))
    for it in items:
        s = json.dumps(it)
        n = len(re.findall(r'rapid', s, re.I))
        if n: res[f"{k}/{it['id']}"] = n; print(k, it['id'], it.get('slug'), n, sorted(set(re.findall(r'.{0,25}rapid.{0,25}', s, re.I)))[:6])
json.dump(req('wp/v2/settings'), open('backup/settings.json', 'w'))
print('settings:', [ (k,v) for k,v in req('wp/v2/settings').items() if 'rapid' in str(v).lower()])
med = all('wp/v2/media?_fields=id,title,source_url,alt_text')
json.dump(med, open('backup/media.json', 'w'))
for m in med:
    if re.search('rapid|logo', json.dumps(m), re.I): print('media', m['id'], m['source_url'], m['alt_text'])
