"""Replace leftover staging-domain URLs (darkblue-kudu-638106 / maroon-raven-160825 .hostingersite.com)
with the live domain in Elementor data + post content of pages, posts, templates and nav blocks.
Usage: python3 fix_urls.py [--apply] [--backup DIR]
Dry run by default. GUIDs are left untouched (WordPress convention)."""
import sys, os, re, json, wp
LIVE = 'aadrecovery.co.uk'
NAME = 'AAD Transport And Recovery'
HOSTS = r'(?:darkblue-kudu-638106|maroon-raven-160825)\.hostingersite\.com'
RULES = [
    (re.compile(r'https?:(\\/|/)\1' + HOSTS), lambda m: f'https:{m.group(1)}{m.group(1)}{LIVE}'),  # URLs (plain or JSON-escaped slashes)
    (re.compile(r'(@)' + HOSTS), lambda m: '@' + LIVE),                                             # form "from" addresses
    (re.compile(HOSTS), lambda m: NAME),                                                             # bare host used as a name (form subject / from-name)
]
def fix(s):
    n = 0
    for rx, rep in RULES:
        s, k = rx.subn(rep, s); n += k
    return s, n
apply = '--apply' in sys.argv
bk = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
total = 0
for t in ['pages', 'posts', 'elementor_library', 'navigation']:
    for x in wp.all(f'wp/v2/{t}?context=edit&status=any'):
        upd = {}
        meta = x.get('meta') if isinstance(x.get('meta'), dict) else {}
        for key in ('_elementor_data',):
            if meta.get(key):
                new, n = fix(meta[key])
                if n: upd.setdefault('meta', {})[key] = new; total += n
        raw = (x.get('content') or {}).get('raw')
        if raw:
            new, n = fix(raw)
            if n: upd['content'] = new; total += n
        if not upd: continue
        print(t, x['id'], x['slug'], 'fields:', list(upd.get('meta', {})) + (['content'] if 'content' in upd else []))
        if bk:
            os.makedirs(bk, exist_ok=True)
            json.dump(x, open(f'{bk}/{t}-{x["id"]}.json', 'w'))
        if apply:
            r = wp.req(f'wp/v2/{t}/{x["id"]}', 'POST', upd)
            if '_err' in r: print('  ERROR', r)
print('replacements:', total, '(applied)' if apply else '(dry run)')
