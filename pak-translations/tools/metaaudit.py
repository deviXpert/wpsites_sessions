import re, urllib.request, html, random
U = 'https://pak-translations.com'; UA = {'User-Agent': 'Mozilla/5.0'}
def m(s, pat):
    x = re.search(pat, s); return html.unescape(x.group(1)) if x else None
for p in ['/', '/about-us/', '/services/', '/languages/', '/sample/', '/career/', '/contact-us/', '/your-order/']:
    s = urllib.request.urlopen(urllib.request.Request(f'{U}{p}?nc={random.random()}', headers=UA), timeout=60).read().decode('utf-8', 'ignore')
    head = s[:s.find('</head>')]; body = s[s.find('<body'):]
    t = m(head, r'<title>([^<]*)'); d = m(head, r'name="description" content="([^"]*)')
    can = m(head, r'rel="canonical" href="([^"]*)'); rob = m(head, r'name="robots" content="([^"]*)')
    ogt = m(head, r'og:title" content="([^"]*)'); ogd = m(head, r'og:description" content="([^"]*)'); ogi = m(head, r'og:image" content="([^"]*)'); tw = m(head, r'twitter:card" content="([^"]*)')
    imgs = re.findall(r'<img\b[^>]*>', body); noalt = [i for i in imgs if not re.search(r'alt="[^"]+"', i)]
    print(f"\n{p}\n  title({len(t or '')}): {t}\n  desc({len(d or '')}): {d}\n  canonical={can}  robots={rob}")
    print(f"  og:title={ogt == t} og:desc={bool(ogd)} og:image={ogi} twitter={tw}")
    print(f"  h1={len(re.findall(r'<h1', body))} imgs={len(imgs)} missing_alt={len(noalt)} faq_schema={'FAQPage' in s} http_links={len(re.findall(r'href=.http://pak-translations', body))}")
