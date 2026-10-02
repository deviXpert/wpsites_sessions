import json,sys,re,os,urllib.request;sys.path.insert(0,'.');from wp import *
c=json.load(open('created.json'));P={p['id']:p for p in json.load(open('wp-backup/pages.json'))}
W=os.environ['WP_URL']
for pid,did in c['drafts'].items():
    slug=P[int(pid)]['slug']
    shell=urllib.request.urlopen(urllib.request.Request(f"{W}/about-us/?nc=1",headers={'User-Agent':'Mozilla/5.0'})).read().decode()
    body=req(f'wp/v2/pages/{did}?context=edit')['content']['rendered']
    ma=re.search(r'<[a-z]+ data-elementor-type="wp-page"',shell);mb=re.search(r'<[a-z]+ data-elementor-type="footer"',shell);a=ma.start() if ma else -1;b=mb.start() if mb else -1
    if a<0 or b<0: print('markers missing',pid,a,b);continue
    html=shell[:a]+body+shell[b:]
    html=html.replace('</head>',f'<link rel="stylesheet" href="{W}/wp-content/uploads/elementor/css/post-{did}.css"></head>')
    open(f'prev/{slug}.html','w').write(html);print('ok',slug)
