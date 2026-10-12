import json,sys,re,os,base64,urllib.request,difflib
from dash import fix,plain
items=json.load(open('dump/all.json'))
SKIP={'custom_css','_css_classes','css_classes','_element_id','url','link','html_tag'}
changes=[]
def walk(o,path=''):
    if isinstance(o,dict): return {k:(o[k] if k in SKIP else walk(o[k],path+'/'+k)) for k in o}
    if isinstance(o,list): return [walk(v,path) for v in o]
    if isinstance(o,str):
        n=fix(o)
        if n!=o: changes.append((o,n))
        return n
    return o
plan=[]
for x in items:
    if x['status']!='publish': continue
    upd={};changes.clear()
    ed=x.get('meta',{}).get('_elementor_data')
    if ed:
        new=json.dumps(walk(json.loads(ed)))
        if changes: upd['meta']={'_elementor_data':new}
    for f in ('content','excerpt'):
        if isinstance(x.get(f),dict) and x[f].get('raw'):
            n=fix(x[f]['raw'])
            if n!=x[f]['raw']: upd[f]=n;changes.append((x[f]['raw'],n))
    if x['_t']!='elementor_library':
        n=fix(x['title']['raw'])
        if n!=x['title']['raw']: upd['title']=n;changes.append((x['title']['raw'],n))
    if upd: plan.append((x,upd,list(changes)))
for x,upd,ch in plan:
    print('##',x['_t'],x['id'],x['title']['raw'][:40],list(upd))
    seen=set()
    for o,n in ch:
        a=plain(o).split('\n');b=plain(n).split('\n')
        for la,lb in zip(a,b):
            if la!=lb and la.strip() not in seen: seen.add(la.strip());print('  -',la.strip()[:150]);print('  +',lb.strip()[:150])
if '--go' in sys.argv:
    H={'Authorization':'Basic '+base64.b64encode((os.environ['WP_USER']+':'+os.environ['WP_APP_PASSWORD']).encode()).decode(),'Content-Type':'application/json'}
    for x,upd,ch in plan:
        r=urllib.request.Request(os.environ['WP_URL']+f"wp-json/wp/v2/{x['_t']}/{x['id']}",data=json.dumps(upd).encode(),method='POST',headers=H)
        try: print(x["id"],urllib.request.urlopen(r).status)
        except urllib.error.HTTPError as e: print(x["id"],e.code,e.read()[:300])
