import wp, json
from concurrent.futures import ThreadPoolExecutor
ids=[c['id'] for c in json.load(open('wp-backup/categories.json')) if c['id']!=1]
def d(i):
    r=wp.req(f'wp/v2/categories/{i}?force=true','DELETE'); return i, ('_err' not in r) or r.get('_err')==404 and 'term_invalid' in r.get('body','')
ok=0
with ThreadPoolExecutor(6) as ex:
    for n,(i,res) in enumerate(ex.map(d,ids)):
        ok+=bool(res)
        if n%500==0: print(n,ok,flush=True)
print('done',ok,'of',len(ids))
