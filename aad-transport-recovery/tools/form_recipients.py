"""Add a recipient to every Elementor form's "Email" / "Email 2" To field (pages + templates).
Usage: python3 form_recipients.py ADDRESS [--apply] [--backup DIR]   (dry run by default)"""
import sys, os, re, json, wp
addr = sys.argv[1]
apply = '--apply' in sys.argv
bk = sys.argv[sys.argv.index('--backup') + 1] if '--backup' in sys.argv else None
RX = re.compile(r'("email_to(?:_2)?"\s*:\s*")([^"]*)(")')
def add(m):
    cur = [a.strip() for a in m.group(2).split(',') if a.strip()]
    if addr.lower() in (a.lower() for a in cur): return m.group(0)
    return m.group(1) + ', '.join(cur + [addr]) + m.group(3)
total = 0
for t in ['pages', 'elementor_library']:
    for x in wp.all(f'wp/v2/{t}?context=edit&status=any'):
        d = (x.get('meta') or {}).get('_elementor_data') if isinstance(x.get('meta'), dict) else None
        if not d: continue
        new = RX.sub(add, d)
        if new == d: continue
        json.loads(new)  # sanity: still valid JSON
        n = sum(1 for a, b in zip(RX.findall(d), RX.findall(new)) if a != b); total += n
        print(t, x['id'], x['slug'], n, 'field(s)')
        if bk:
            os.makedirs(bk, exist_ok=True); json.dump(x, open(f'{bk}/{t}-{x["id"]}.json', 'w'))
        if apply:
            r = wp.req(f'wp/v2/{t}/{x["id"]}', 'POST', {'meta': {'_elementor_data': new}})
            if '_err' in r: print('  ERROR', r)
print('fields updated:', total, '(applied)' if apply else '(dry run)')
