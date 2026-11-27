"""Animated SVG infographics (self-contained: CSS + SMIL inside the SVG, no JS, no fonts to load).
Used in Elementor Image widgets. Respects prefers-reduced-motion. Output: ../templates/infographics/*.svg"""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates', 'infographics')
FONT = "font-family:'Sora','Inter','Segoe UI',Roboto,Arial,sans-serif"

def wrap(w, h, title, desc, body, extra_css=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">{title}</title><desc id="d">{desc}</desc>
<defs>
<linearGradient id="gBV" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0684C4"/><stop offset="1" stop-color="#7052FF"/></linearGradient>
<linearGradient id="gSky" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5DB0D8"/><stop offset=".5" stop-color="#0684C4"/><stop offset="1" stop-color="#9D86FF"/></linearGradient>
<linearGradient id="gBar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0684C4"/><stop offset="1" stop-color="#9D86FF"/></linearGradient>
<radialGradient id="glowV"><stop offset="0" stop-color="#7052FF" stop-opacity=".45"/><stop offset="1" stop-color="#7052FF" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB"><stop offset="0" stop-color="#0684C4" stop-opacity=".45"/><stop offset="1" stop-color="#0684C4" stop-opacity="0"/></radialGradient>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#020617" flood-opacity=".55"/></filter>
</defs>
<style>
text{{{FONT};fill:#fff}} .m{{fill:#C9D3E8}} .s{{fill:#93A1BF}} .a{{fill:#5DB0D8}}
.glass{{fill:rgba(255,255,255,.07);stroke:rgba(255,255,255,.18);stroke-width:1}}
.glass2{{fill:rgba(255,255,255,.11);stroke:rgba(255,255,255,.22);stroke-width:1}}
.flow{{fill:none;stroke:url(#gSky);stroke-width:2;stroke-dasharray:5 9;animation:flow 1.4s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-28}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.6s ease-out infinite}}
@keyframes pulse{{0%{{transform:scale(.85);opacity:.9}}100%{{transform:scale(1.6);opacity:0}}}}
.float{{animation:float 5s ease-in-out infinite}} @keyframes float{{50%{{transform:translateY(-6px)}}}}
.grow{{transform-box:fill-box;transform-origin:bottom;animation:grow 4s cubic-bezier(.2,.7,.2,1) infinite}}
@keyframes grow{{0%{{transform:scaleY(.08)}}35%,85%{{transform:scaleY(1)}}100%{{transform:scaleY(.08)}}}}
.draw{{stroke-dasharray:600;stroke-dashoffset:600;animation:draw 5s ease-in-out infinite}}
@keyframes draw{{0%{{stroke-dashoffset:600}}45%,85%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:600}}}}
.pop{{transform-box:fill-box;transform-origin:center;animation:pop 5s ease-in-out infinite}}
@keyframes pop{{0%,8%{{transform:scale(0);opacity:0}}16%,88%{{transform:scale(1);opacity:1}}100%{{transform:scale(0);opacity:0}}}}
{extra_css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}} .draw{{stroke-dashoffset:0}} .pop{{transform:none;opacity:1}}}}
</style>
{body}
</svg>'''

def d(i, base=0.0, step=0.35):  # staggered animation-delay attribute
    return f'style="animation-delay:{base + i * step:.2f}s"'

def blobs(w, h):
    return ''
    return f'<circle cx="{w*.18:.0f}" cy="{h*.2:.0f}" r="{w*.32:.0f}" fill="url(#glowV)"/><circle cx="{w*.85:.0f}" cy="{h*.85:.0f}" r="{w*.35:.0f}" fill="url(#glowB)"/>'

# ---------------- icons (24px box, centred on 0,0) ----------------
def i_web(c='#5DB0D8'):
    return f'<g fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"><rect x="-12" y="-9" width="24" height="18" rx="3"/><path d="M-12 -3H12"/><circle cx="-8" cy="-6" r=".8" fill="{c}"/><circle cx="-5" cy="-6" r=".8" fill="{c}"/><path d="M-5 3l-3 2 3 2M5 3l3 2-3 2"/></g>'
def i_seo(c='#5DB0D8'):
    return f'<g fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"><circle cx="-3" cy="-3" r="8"/><path d="M3 3l8 8"/><path d="M-7 -1l3-3 2 2 3-4"/></g>'
def i_social(c='#5DB0D8'):
    return f'<g fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"><path d="M0 9s-11-6.5-11-13.5A5.5 5.5 0 0 1 0 -8a5.5 5.5 0 0 1 11 3.5C11 2.5 0 9 0 9z"/></g>'
def i_design(c='#5DB0D8'):
    return f'<g fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"><path d="M0 -11l7 12-7 9-7-9z"/><circle cx="0" cy="1" r="2"/><path d="M0 -11v10"/></g>'

# ================= HOME: combined growth engine =================
def home():
    W, H = 680, 600
    hub = (340, 236)
    nodes = [(118, 86, 'Website', 'Fast, mobile-first', i_web), (562, 86, 'SEO', 'Page-one rankings', i_seo),
             (118, 386, 'Social Media', 'Reach &amp; engagement', i_social), (562, 386, 'Graphic Design', 'Brand that sells', i_design)]
    paths, parts = [], []
    for k, (x, y, t, sub, ic) in enumerate(nodes):
        sx = x + (92 if x < hub[0] else -92); cy = (y + hub[1]) / 2
        p = f'M{sx} {y} C {(sx+hub[0])/2:.0f} {y}, {(sx+hub[0])/2:.0f} {hub[1]}, {hub[0] + (-58 if x < hub[0] else 58)} {hub[1]}'
        paths.append(f'<path id="p{k}" class="flow" d="{p}"/>')
        parts.append(f'<circle r="4" fill="#fff"><animateMotion dur="2.4s" begin="{k*0.6:.1f}s" repeatCount="indefinite" path="{p}"/></circle>')
        parts.append(f'''<g class="float" {d(k, 0, .7)}><g filter="url(#soft)"><rect class="glass2" x="{x-92}" y="{y-34}" width="184" height="68" rx="16"/></g>
<rect x="{x-80}" y="{y-20}" width="40" height="40" rx="11" fill="rgba(6,132,196,.22)" stroke="rgba(93,176,216,.5)"/>
<g transform="translate({x-60} {y})">{ic()}</g>
<text x="{x-30}" y="{y-3}" font-size="14" font-weight="700">{t}</text><text class="m" x="{x-30}" y="{y+15}" font-size="11">{sub}</text></g>''')
    bars = ''.join(f'<rect class="grow" {d(i, 0, .18)} x="{196 + i*36}" y="{560 - h}" width="22" height="{h}" rx="6" fill="url(#gBar)"/>'
                   for i, h in enumerate([14, 20, 18, 28, 32, 42, 50, 62]))
    trend = '<path class="draw" d="M200 548 L236 540 L272 542 L308 530 L344 524 L380 512 L416 504 L452 492" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    body = f'''{blobs(W, H)}
<g opacity=".25">{''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#93A1BF"/>' for x in range(20, W, 40) for y in range(20, H, 40))}</g>
{''.join(paths)}
<path class="flow" d="M{hub[0]} {hub[1]+64} V 430"/>
{''.join(parts)}
<circle r="4" fill="#fff"><animateMotion dur="1.6s" repeatCount="indefinite" path="M{hub[0]} {hub[1]+64} V 430"/></circle>
<circle class="pulse" cx="{hub[0]}" cy="{hub[1]}" r="62" fill="none" stroke="#5DB0D8" stroke-width="2"/>
<circle class="pulse" style="animation-delay:1.3s" cx="{hub[0]}" cy="{hub[1]}" r="62" fill="none" stroke="#9D86FF" stroke-width="2"/>
<g filter="url(#soft)"><circle cx="{hub[0]}" cy="{hub[1]}" r="62" fill="url(#gBV)"/></g>
<circle cx="{hub[0]}" cy="{hub[1]}" r="54" fill="none" stroke="rgba(255,255,255,.35)"/>
<text x="{hub[0]}" y="{hub[1]-6}" text-anchor="middle" font-size="22" font-weight="800">GSS</text>
<text x="{hub[0]}" y="{hub[1]+14}" text-anchor="middle" font-size="10.5" font-weight="600" letter-spacing="1.5">GROWTH ENGINE</text>
<g filter="url(#soft)"><rect class="glass" x="170" y="430" width="340" height="150" rx="20"/></g>
<text class="a" x="194" y="460" font-size="11" font-weight="700" letter-spacing="1.6">RESULT</text>
<text x="194" y="482" font-size="15" font-weight="700">More leads &amp; revenue</text>
<g transform="translate(-6 0)">{bars}</g>{trend}
<g class="pop" style="animation-delay:1.6s"><rect x="398" y="446" width="96" height="30" rx="15" fill="#7052FF"/><text x="446" y="466" text-anchor="middle" font-size="13" font-weight="800">▲ 3× leads</text></g>'''
    return wrap(W, H, 'How Graphics Storm Studio grows your business',
                'Animated infographic: website development, SEO, social media marketing and graphic design all feed one growth engine that produces more leads and revenue.', body)

# ================= SERVICE: Website development =================
def web():
    W, H = 600, 460
    blocks = [(70, 112, 300, 70, '#0684C4', .55), (70, 196, 92, 74, '#7052FF', .45), (174, 196, 92, 74, '#5DB0D8', .4),
              (278, 196, 92, 74, '#9D86FF', .4), (70, 284, 200, 12, '#fff', .35), (70, 304, 150, 12, '#fff', .22)]
    bl = ''.join(f'<rect class="pop" {d(i, 0.2, .35)} x="{x}" y="{y}" width="{w}" height="{h}" rx="{8 if h > 20 else 6}" fill="{c}" fill-opacity="{o}"/>' for i, (x, y, w, h, c, o) in enumerate(blocks))
    body = f'''{blobs(W, H)}
<g filter="url(#soft)"><rect class="glass2" x="46" y="58" width="348" height="290" rx="18"/></g>
<path d="M46 92H394" stroke="rgba(255,255,255,.18)"/>
<circle cx="68" cy="75" r="5" fill="#FF6B6B"/><circle cx="84" cy="75" r="5" fill="#FFC857"/><circle cx="100" cy="75" r="5" fill="#3DDC97"/>
<rect x="124" y="67" width="200" height="16" rx="8" fill="rgba(255,255,255,.08)"/><text class="s" x="136" y="79" font-size="10">yourbusiness.com</text>
{bl}
<g class="float"><g filter="url(#soft)"><rect class="glass2" x="420" y="150" width="124" height="232" rx="22"/></g>
<rect x="470" y="160" width="24" height="5" rx="2.5" fill="rgba(255,255,255,.3)"/>
{''.join(f'<rect class="pop" {d(i, 1.2, .3)} x="434" y="{178 + i*46}" width="96" height="36" rx="8" fill="{c}" fill-opacity=".45"/>' for i, c in enumerate(['#0684C4', '#7052FF', '#5DB0D8', '#9D86FF']))}
<text class="a" x="482" y="400" text-anchor="middle" font-size="11" font-weight="700">MOBILE-FIRST</text></g>
<g transform="translate(150 410)"><path d="M-62 0 A62 62 0 0 1 62 0" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="10" stroke-linecap="round"/>
<path class="arc" d="M-62 0 A62 62 0 0 1 58 -18" fill="none" stroke="url(#gSky)" stroke-width="10" stroke-linecap="round"/>
<rect class="needle" x="-1.5" y="-48" width="3" height="48" rx="1.5" fill="#fff"/>
<circle r="6" fill="#fff"/></g>
<text x="232" y="402" font-size="30" font-weight="800">98</text><text class="m" x="232" y="420" font-size="11">PageSpeed score</text>
<g class="pop" style="animation-delay:2.2s"><rect x="282" y="20" width="112" height="28" rx="14" fill="#7052FF"/><text x="338" y="39" text-anchor="middle" font-size="12" font-weight="700">✓ SEO-ready</text></g>'''
    css = '''.arc{stroke-dasharray:200;stroke-dashoffset:200;animation:arc 5s ease-in-out infinite}
@keyframes arc{0%{stroke-dashoffset:200}45%,85%{stroke-dashoffset:18}100%{stroke-dashoffset:200}}
.needle{transform-box:fill-box;transform-origin:50% 100%;animation:needle 5s ease-in-out infinite}
@keyframes needle{0%{transform:rotate(-90deg)}45%,85%{transform:rotate(72deg)}100%{transform:rotate(-90deg)}}
@media (prefers-reduced-motion:reduce){.arc{stroke-dashoffset:18}.needle{transform:rotate(72deg)}}'''
    return wrap(W, H, 'Website development infographic', 'Animated infographic: a responsive website being built block by block on desktop and mobile, with a PageSpeed score of 98.', body, css)

# ================= SERVICE: SEO =================
def seo():
    W, H = 600, 460
    rows = ['competitor-one.com', 'competitor-two.com', 'competitor-three.com']
    res = ''.join(f'''<g transform="translate(0 {i*58})"><rect class="glass" x="46" y="124" width="320" height="46" rx="12"/>
<text class="s" x="64" y="143" font-size="10">{r}</text><rect x="64" y="152" width="{180 - i*30}" height="7" rx="3.5" fill="rgba(255,255,255,.14)"/>
<text class="s" x="346" y="152" text-anchor="end" font-size="13" font-weight="700">#{i+2}</text></g>''' for i, r in enumerate(rows))
    css = '''.climb{animation:climb 6s cubic-bezier(.5,0,.2,1) infinite}
@keyframes climb{0%,12%{transform:translateY(232px)}45%,85%{transform:translateY(0)}100%{transform:translateY(232px)}}
.rank::after{content:''} .type{animation:type 6s steps(24) infinite}
@keyframes type{0%{width:0}30%,90%{width:220px}100%{width:0}}'''
    body = f'''{blobs(W, H)}
<g filter="url(#soft)"><rect class="glass2" x="30" y="40" width="352" height="330" rx="20"/></g>
<rect x="46" y="58" width="320" height="40" rx="20" fill="rgba(255,255,255,.09)" stroke="rgba(93,176,216,.45)"/>
<g transform="translate(68 78)">{i_seo()}</g>
<clipPath id="cp"><rect class="type" x="92" y="62" width="220" height="30"/></clipPath>
<text clip-path="url(#cp)" x="94" y="83" font-size="13" font-weight="500">digital marketing agency</text>
<g transform="translate(0 58)">{res}</g>
<g class="climb"><g filter="url(#soft)"><rect x="46" y="124" width="320" height="46" rx="12" fill="url(#gBV)"/></g>
<text x="64" y="143" font-size="10" font-weight="600" fill="#E6EEFF">yourbusiness.com ✓</text><rect x="64" y="152" width="210" height="7" rx="3.5" fill="rgba(255,255,255,.55)"/>
<text x="346" y="153" text-anchor="end" font-size="16" font-weight="800">#1</text></g>
<g class="float"><g filter="url(#soft)"><rect class="glass2" x="404" y="96" width="170" height="220" rx="18"/></g>
<text class="a" x="420" y="122" font-size="10.5" font-weight="700" letter-spacing="1.4">ORGANIC TRAFFIC</text>
<text x="420" y="150" font-size="24" font-weight="800">+214%</text>
<path d="M420 290 H560" stroke="rgba(255,255,255,.15)"/>
<path d="M420 286 L444 280 L468 282 L492 262 L516 244 L540 214 L558 186 L558 290 L420 290Z" fill="url(#gBV)" opacity=".25"/>
<path class="draw" d="M420 286 L444 280 L468 282 L492 262 L516 244 L540 214 L558 186" fill="none" stroke="url(#gSky)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<circle class="pop" style="animation-delay:2s" cx="558" cy="186" r="6" fill="#fff"/></g>
<g class="pop" style="animation-delay:2.6s"><rect x="420" y="336" width="138" height="32" rx="16" fill="#7052FF"/><text x="489" y="357" text-anchor="middle" font-size="12.5" font-weight="700">Page 1 on Google</text></g>'''
    return wrap(W, H, 'SEO services infographic', 'Animated infographic: a search for "digital marketing agency" where your website climbs from 4th to 1st position, with organic traffic rising 214%.', body, css)

# ================= SERVICE: Social media =================
def smm():
    W, H = 600, 460
    css = '''.heart{animation:heart 3.2s ease-out infinite;opacity:0}
@keyframes heart{0%{transform:translate(0,0) scale(.6);opacity:0}15%{opacity:1}100%{transform:translate(var(--x,0px),-150px) scale(1.15);opacity:0}}
.like{transform-box:fill-box;transform-origin:center;animation:like 3.2s ease-in-out infinite}
@keyframes like{0%,20%{transform:scale(1)}28%{transform:scale(1.35)}36%,100%{transform:scale(1)}}'''
    hearts = ''.join(f'<g class="heart" style="animation-delay:{i*0.55:.2f}s;--x:{x}px"><g transform="translate({300 + x//3} 300)"><path d="M0 9s-11-6.5-11-13.5A5.5 5.5 0 0 1 0 -8a5.5 5.5 0 0 1 11 3.5C11 2.5 0 9 0 9z" fill="#FF6B9A"/></g></g>' for i, x in enumerate([-30, 24, -10, 40, -44, 8]))
    stats = [('Reach', 128), ('Engagement', 104), ('Leads', 84)]
    sb = ''.join(f'''<text class="m" x="440" y="{150 + i*62}" font-size="11.5" font-weight="600">{t}</text>
<rect x="440" y="{160 + i*62}" width="130" height="12" rx="6" fill="rgba(255,255,255,.1)"/>
<rect class="grow2" style="animation-delay:{i*.4:.1f}s" x="440" y="{160 + i*62}" width="{w}" height="12" rx="6" fill="url(#gSky)"/>''' for i, (t, w) in enumerate(stats))
    css += '''.grow2{transform-box:fill-box;transform-origin:left;animation:grow2 4.5s cubic-bezier(.2,.7,.2,1) infinite}
@keyframes grow2{0%{transform:scaleX(.05)}40%,85%{transform:scaleX(1)}100%{transform:scaleX(.05)}}'''
    body = f'''{blobs(W, H)}
<g filter="url(#soft)"><rect class="glass2" x="216" y="34" width="168" height="340" rx="28"/></g>
<rect x="286" y="46" width="28" height="6" rx="3" fill="rgba(255,255,255,.3)"/>
<circle cx="242" cy="78" r="11" fill="url(#gBV)"/><text x="260" y="76" font-size="10.5" font-weight="700">yourbrand</text><text class="s" x="260" y="88" font-size="8.5">Sponsored</text>
<rect x="230" y="98" width="140" height="150" rx="14" fill="url(#gBV)" opacity=".8"/>
<circle cx="300" cy="160" r="30" fill="rgba(255,255,255,.18)"/><path d="M288 176l12-26 12 26z" fill="rgba(255,255,255,.55)"/>
<g class="like" transform="translate(246 270) scale(.75)">{i_social("#FF6B9A")}</g>
<text x="262" y="274" font-size="11" font-weight="700">2,481 likes</text>
<rect x="232" y="286" width="120" height="7" rx="3.5" fill="rgba(255,255,255,.15)"/><rect x="232" y="300" width="90" height="7" rx="3.5" fill="rgba(255,255,255,.1)"/>
{hearts}
<g class="float"><g filter="url(#soft)"><rect class="glass2" x="424" y="112" width="160" height="200" rx="18"/></g>{sb}</g>
<g class="float" style="animation-delay:1s"><g class="pop" style="animation-delay:.8s"><g filter="url(#soft)"><rect class="glass2" x="24" y="96" width="166" height="54" rx="16"/></g>
<circle cx="50" cy="123" r="13" fill="#7052FF"/><text x="50" y="128" text-anchor="middle" font-size="13" font-weight="800">+</text>
<text x="72" y="119" font-size="11.5" font-weight="700">New followers</text><text class="a" x="72" y="135" font-size="11" font-weight="600">+1,240 this month</text></g></g>
<g class="float" style="animation-delay:2s"><g class="pop" style="animation-delay:1.8s"><g filter="url(#soft)"><rect class="glass2" x="24" y="246" width="166" height="54" rx="16"/></g>
<circle cx="50" cy="273" r="13" fill="#0684C4"/><text x="50" y="277" text-anchor="middle" font-size="11" font-weight="800">✉</text>
<text x="72" y="269" font-size="11.5" font-weight="700">New lead</text><text class="a" x="72" y="285" font-size="11" font-weight="600">from Instagram ad</text></g></g>
<g class="pop" style="animation-delay:2.4s"><rect x="210" y="396" width="180" height="34" rx="17" fill="#7052FF"/><text x="300" y="418" text-anchor="middle" font-size="12.5" font-weight="700">▲ 3× reach in 90 days</text></g>'''
    return wrap(W, H, 'Social media marketing infographic', 'Animated infographic: a social media post collecting likes, new followers and leads, with reach, engagement and leads bars growing.', body, css)

# ================= SERVICE: Graphic design =================
def design():
    W, H = 600, 460
    logo = 'M150 300 C 150 200, 250 160, 300 220 S 430 300, 430 190'
    css = '''.sw{transform-box:fill-box;transform-origin:center bottom;animation:sw 5s ease-in-out infinite}
@keyframes sw{0%,10%{transform:scaleY(0)}22%,88%{transform:scaleY(1)}100%{transform:scaleY(0)}}'''
    sw = ''.join(f'<rect class="sw" {d(i, .4, .22)} x="{70 + i*48}" y="360" width="38" height="48" rx="10" fill="{c}"/>' for i, c in enumerate(['#0684C4', '#5DB0D8', '#7052FF', '#9D86FF', '#FFFFFF']))
    body = f'''{blobs(W, H)}
<g filter="url(#soft)"><rect class="glass2" x="40" y="40" width="380" height="300" rx="20"/></g>
<g stroke="rgba(255,255,255,.07)">{''.join(f'<path d="M{x} 52V328"/>' for x in range(70, 420, 30))}{''.join(f'<path d="M52 {y}H408"/>' for y in range(70, 340, 30))}</g>
<path class="draw" d="{logo}" fill="none" stroke="url(#gSky)" stroke-width="10" stroke-linecap="round"/>
<g stroke="#9D86FF" stroke-width="1.5"><path d="M150 300 L150 230"/><path d="M300 220 L240 170"/><path d="M300 220 L360 270"/><path d="M430 190 L430 240"/></g>
{''.join(f'<rect class="pop" {d(i, .3, .4)} x="{x-6}" y="{y-6}" width="12" height="12" rx="2" fill="#070B1F" stroke="#fff" stroke-width="2"/>' for i, (x, y) in enumerate([(150, 300), (300, 220), (430, 190)]))}
{''.join(f'<circle class="pop" {d(i, .5, .4)} cx="{x}" cy="{y}" r="4.5" fill="#9D86FF"/>' for i, (x, y) in enumerate([(150, 230), (240, 170), (360, 270), (430, 240)]))}
<g><g transform="translate(-4 -24)"><path d="M0 0l9 15-9 11-9-11z" fill="#fff" stroke="#070B1F" stroke-width="1.5"/><circle cy="14" r="2.4" fill="#070B1F"/></g>
<animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1;0" keyTimes="0;.45;.85;1" calcMode="linear" path="{logo}"/></g>
{sw}
<g class="float"><g filter="url(#soft)"><rect class="glass2" x="440" y="70" width="136" height="150" rx="18"/></g>
<text x="508" y="150" text-anchor="middle" font-size="60" font-weight="800" fill="url(#gSky)">Aa</text>
<text class="m" x="508" y="182" text-anchor="middle" font-size="11">Sora · Inter</text><text class="s" x="508" y="200" text-anchor="middle" font-size="10">Brand typography</text></g>
<g class="float" style="animation-delay:1.2s"><g filter="url(#soft)"><rect class="glass2" x="440" y="238" width="136" height="110" rx="18"/></g>
<circle cx="478" cy="282" r="18" fill="url(#gBV)"/><rect x="504" y="270" width="56" height="8" rx="4" fill="rgba(255,255,255,.5)"/><rect x="504" y="286" width="40" height="6" rx="3" fill="rgba(255,255,255,.25)"/>
<text class="a" x="508" y="330" text-anchor="middle" font-size="10.5" font-weight="700" letter-spacing="1.2">LOGO + ID</text></g>
<g class="pop" style="animation-delay:2.4s"><rect x="340" y="370" width="200" height="34" rx="17" fill="#7052FF"/><text x="440" y="392" text-anchor="middle" font-size="12.5" font-weight="700">Brand guidelines ready ✓</text></g>'''
    return wrap(W, H, 'Graphic design infographic', 'Animated infographic: a logo being drawn with the pen tool on a design grid, with a brand colour palette, typography and logo identity cards.', body, css)


# ================= ABOUT: team & story =================
def about():
    W, H = 600, 500
    cx, cy = 300, 200
    roles = [('CEO', -150, -110), ('Creative', 150, -110), ('Projects', -190, 40), ('Content', 190, 40), ('Design', 0, 128)]
    lines = ''.join(f'<path class="flow" d="M{cx} {cy} L{cx+x} {cy+y}"/>' for _, x, y in roles)
    av = ''.join(f"""<g class="float" {d(i, 0, .6)}><g class="pop" {d(i, .2, .3)}><g filter="url(#soft)"><circle cx="{cx+x}" cy="{cy+y}" r="34" class="glass2"/></g>
<circle cx="{cx+x}" cy="{cy+y-8}" r="10" fill="url(#gBV)"/><path d="M{cx+x-16} {cy+y+18} a16 13 0 0 1 32 0" fill="url(#gBV)"/>
<text x="{cx+x}" y="{cy+y+52}" text-anchor="middle" font-size="11.5" font-weight="700">{t}</text></g></g>""" for i, (t, x, y) in enumerate(roles))
    chips = [('5+', 'years', 28, 418), ('130+', 'clients', 222, 430), ('180+', 'websites', 416, 418)]
    ch = ''.join(f"""<g class="pop" {d(i, 1.6, .35)}><g filter="url(#soft)"><rect class="glass2" x="{x}" y="{y}" width="156" height="50" rx="16"/></g>
<text x="{x+16}" y="{y+32}" font-size="20" font-weight="800">{n}</text><text class="m" x="{x+26+len(n)*13}" y="{y+31}" font-size="11.5">{t}</text></g>""" for i, (n, t, x, y) in enumerate(chips))
    body = f"""{lines}
<circle class="pulse" cx="{cx}" cy="{cy}" r="48" fill="none" stroke="#5DB0D8" stroke-width="2"/>
<g filter="url(#soft)"><circle cx="{cx}" cy="{cy}" r="48" fill="url(#gBV)"/></g>
<text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="16" font-weight="800">ONE</text><text x="{cx}" y="{cy+16}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="1.4">TEAM</text>
{av}{ch}"""
    return wrap(W, H, 'About Graphics Storm Studio infographic', 'Animated infographic: one connected team of CEO, creative, project, content and design specialists, with 5+ years, 130+ happy clients and 180+ websites.', body)

# ================= SERVICES HUB: growth funnel =================
def funnel():
    W, H = 600, 460
    tiers = [('Attract', 'Social media · Design · Ads', 480, '#9D86FF'), ('Rank', 'SEO · Content', 400, '#7052FF'),
             ('Convert', 'Website · Landing pages', 320, '#0684C4'), ('Grow', 'Leads · Sales · Loyalty', 240, '#5DB0D8')]
    t = ''
    for i, (name, sub, w, c) in enumerate(tiers):
        y = 46 + i * 92; x = (W - w) / 2
        t += f"""<g class="pop" {d(i, .1, .35)}><g filter="url(#soft)"><path d="M{x} {y} H{x+w} L{x+w-36} {y+76} H{x+36} Z" fill="{c}" fill-opacity=".28" stroke="{c}" stroke-opacity=".7"/></g>
<text x="{W/2}" y="{y+34}" text-anchor="middle" font-size="17" font-weight="800">{name}</text><text class="m" x="{W/2}" y="{y+54}" text-anchor="middle" font-size="11.5">{sub}</text></g>"""
    drops = ''.join(f'<circle r="4.5" fill="#fff"><animateMotion dur="3s" begin="{k*0.6:.1f}s" repeatCount="indefinite" path="M{W/2 + off} 30 V 420"/><animate attributeName="opacity" values="0;1;1;0" dur="3s" begin="{k*0.6:.1f}s" repeatCount="indefinite"/></circle>' for k, off in enumerate([-60, 30, -15, 55, -40]))
    body = f"""{drops}{t}
<g class="pop" style="animation-delay:1.8s"><rect x="210" y="414" width="180" height="34" rx="17" fill="#7052FF"/><text x="300" y="436" text-anchor="middle" font-size="12.5" font-weight="700">▲ More customers</text></g>"""
    return wrap(W, H, 'Digital marketing funnel infographic', 'Animated infographic: social media, design and ads attract visitors, SEO ranks you, your website converts them and you grow with more leads and sales.', body)

# ================= OUR WORK: showcase =================
def work():
    W, H = 600, 460
    css = """.cyc{animation:cyc 9s ease-in-out infinite;opacity:0}
@keyframes cyc{0%{opacity:0;transform:translateY(10px)}6%,30%{opacity:1;transform:none}36%,100%{opacity:0;transform:translateY(-10px)}}
@media (prefers-reduced-motion:reduce){.cyc{opacity:0}.cyc.first{opacity:1}}"""
    screens = [('url(#gBV)', 'Website launch', '3× more enquiries'), ('#7052FF', 'Brand identity', 'New logo + guidelines'), ('#0684C4', 'SEO campaign', '+214% organic traffic')]
    sc = ''.join(f"""<g class="cyc{' first' if i == 0 else ''}" style="animation-delay:{i*3}s">
<rect x="96" y="96" width="300" height="168" rx="8" fill="{c}" fill-opacity=".55"/>
<rect x="116" y="118" width="140" height="14" rx="7" fill="rgba(255,255,255,.75)"/><rect x="116" y="142" width="200" height="9" rx="4.5" fill="rgba(255,255,255,.35)"/>
<rect x="116" y="196" width="80" height="26" rx="13" fill="#fff" fill-opacity=".85"/>
<g filter="url(#soft)"><rect class="glass2" x="330" y="300" width="210" height="64" rx="16"/></g>
<text class="a" x="350" y="326" font-size="10.5" font-weight="700" letter-spacing="1.3">{t.upper()}</text><text x="350" y="348" font-size="15" font-weight="800">{r}</text></g>""" for i, (c, t, r) in enumerate(screens))
    body = f"""<g class="float"><g filter="url(#soft)"><rect class="glass2" x="80" y="80" width="332" height="200" rx="14"/></g>
<path d="M60 286 H432 L414 300 H78 Z" fill="rgba(255,255,255,.16)"/></g>
<g class="float" style="animation-delay:1.5s"><g filter="url(#soft)"><rect class="glass2" x="440" y="70" width="100" height="196" rx="20"/></g>
<rect x="452" y="94" width="76" height="60" rx="8" fill="url(#gBV)" fill-opacity=".6"/><rect x="452" y="162" width="76" height="8" rx="4" fill="rgba(255,255,255,.4)"/><rect x="452" y="176" width="56" height="8" rx="4" fill="rgba(255,255,255,.25)"/>
<rect x="452" y="196" width="76" height="40" rx="8" fill="#7052FF" fill-opacity=".45"/></g>
{sc}
<g class="pop" style="animation-delay:.6s"><g filter="url(#soft)"><rect class="glass2" x="60" y="320" width="150" height="80" rx="16"/></g>
<text class="a" x="78" y="346" font-size="10.5" font-weight="700" letter-spacing="1.3">PROJECTS</text><text x="78" y="380" font-size="26" font-weight="800">514+</text><text class="m" x="146" y="380" font-size="10.5">last month</text></g>"""
    return wrap(W, H, 'Our work portfolio infographic', 'Animated infographic: a laptop and phone cycling through website, brand identity and SEO projects with their results.', body, css)

# ================= CONTACT: message flow =================
def contact():
    W, H = 600, 460
    path = 'M190 170 C 300 60, 360 300, 440 220'
    body = f"""<g class="float"><g filter="url(#soft)"><rect class="glass2" x="40" y="90" width="170" height="220" rx="18"/></g>
<text x="60" y="122" font-size="13" font-weight="700">Free proposal</text>
{''.join(f'<rect class="pop" {d(i, .1, .25)} x="60" y="{140 + i*34}" width="130" height="24" rx="8" fill="rgba(255,255,255,.09)" stroke="rgba(255,255,255,.2)"/>' for i in range(3))}
<rect class="pop" style="animation-delay:1s" x="60" y="248" width="130" height="30" rx="15" fill="#7052FF"/><text class="pop" style="animation-delay:1s" x="125" y="268" text-anchor="middle" font-size="11.5" font-weight="700">Send ➤</text></g>
<path class="flow" d="{path}"/>
<g><path d="M-12 -8 L14 0 L-12 8 L-7 0 Z" fill="#fff"/><animateMotion dur="3.5s" repeatCount="indefinite" rotate="auto" path="{path}"/></g>
<g class="float" style="animation-delay:1.2s"><g filter="url(#soft)"><rect class="glass2" x="410" y="120" width="160" height="200" rx="18"/></g>
<circle cx="440" cy="152" r="14" fill="url(#gBV)"/><text x="462" y="150" font-size="11.5" font-weight="700">GSS team</text><text class="a" x="462" y="164" font-size="9.5">online</text>
<g class="pop" style="animation-delay:1.8s"><rect x="426" y="182" width="126" height="40" rx="12" fill="rgba(6,132,196,.35)"/><text x="436" y="200" font-size="10.5">Thanks! We'll send</text><text x="436" y="214" font-size="10.5">your plan today ✓</text></g>
<g class="pop" style="animation-delay:2.4s"><rect x="426" y="232" width="100" height="30" rx="12" fill="rgba(112,82,255,.45)"/><text x="436" y="251" font-size="10.5">Call booked 📅</text></g></g>
<g class="pop" style="animation-delay:.4s"><g filter="url(#soft)"><rect class="glass2" x="200" y="350" width="200" height="60" rx="18"/></g>
<circle cx="230" cy="380" r="13" fill="none" stroke="#5DB0D8" stroke-width="2.5"/><path d="M230 372 V380 L236 384" stroke="#5DB0D8" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<text x="252" y="376" font-size="12.5" font-weight="700">Reply within</text><text class="a" x="252" y="393" font-size="12" font-weight="600">1 business day</text></g>"""
    return wrap(W, H, 'Contact infographic', 'Animated infographic: your proposal request flies to the Graphics Storm Studio team, who reply within one business day and book a call.', body)

# ================= LEGAL: privacy shield / terms document =================
def privacy():
    W, H = 600, 400
    body = f"""<circle class="pulse" cx="300" cy="190" r="96" fill="none" stroke="#5DB0D8" stroke-width="2"/>
<g filter="url(#soft)"><path d="M300 70 L392 104 V186 C392 252 350 296 300 318 C250 296 208 252 208 186 V104 Z" fill="url(#gBV)" fill-opacity=".85"/></g>
<rect x="272" y="178" width="56" height="46" rx="8" fill="#fff" fill-opacity=".92"/><path d="M282 178 v-14 a18 18 0 0 1 36 0 v14" fill="none" stroke="#fff" stroke-width="7"/><circle cx="300" cy="198" r="6" fill="#0684C4"/>
{''.join(f'<g class="pop" {d(i, .3, .35)}><g filter="url(#soft)"><rect class="glass2" x="{x}" y="{y}" width="132" height="40" rx="14"/></g><text x="{x+66}" y="{y+25}" text-anchor="middle" font-size="12" font-weight="700">{t}</text></g>' for i, (t, x, y) in enumerate([('✓ No data selling', 40, 90), ('✓ HTTPS secured', 428, 90), ('✓ Your rights', 40, 260), ('✓ Spam protected', 428, 260)]))}"""
    return wrap(W, H, 'Privacy infographic', 'Animated infographic: a shield and padlock protecting your data – no data selling, HTTPS security, your privacy rights and spam protection.', body)

def terms():
    W, H = 600, 400
    items = ['Clear scope &amp; pricing', 'You own final work', 'Honest results', '30-day website support']
    body = f"""<g class="float"><g filter="url(#soft)"><rect class="glass2" x="170" y="40" width="260" height="320" rx="20"/></g>
<rect x="200" y="70" width="150" height="14" rx="7" fill="rgba(255,255,255,.7)"/><rect x="200" y="94" width="110" height="9" rx="4.5" fill="rgba(255,255,255,.3)"/>
{''.join(f'<g class="pop" {d(i, .3, .45)}><circle cx="212" cy="{140 + i*48}" r="11" fill="#7052FF"/><path d="M206 {140 + i*48} l4 4 8-8" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="232" y="{145 + i*48}" font-size="13" font-weight="600">{t}</text></g>' for i, t in enumerate(items))}
<path class="draw" d="M210 334 c14 -22 26 8 40 -10 s22 -4 36 -12 s18 6 30 -2" fill="none" stroke="url(#gSky)" stroke-width="3" stroke-linecap="round"/></g>"""
    return wrap(W, H, 'Terms of service infographic', 'Animated infographic: a service agreement with clear scope and pricing, ownership of final work, honest results and 30-day website support.', body)

# ================= ABOUT: our story / journey =================
def story():
    W, H = 600, 640
    path = 'M90 560 C 170 540, 160 450, 250 430 S 360 360, 330 300 S 400 190, 470 170 S 520 110, 520 80'
    stops = [(90, 560, 'Design studio', 'Where it began', 'right'), (250, 430, '+ Web development', 'Websites that sell', 'right'),
             (330, 300, '+ SEO &amp; social', 'Full-service marketing', 'left'), (470, 170, '130+ clients', 'USA · Canada · worldwide', 'left')]
    pins = ''
    for i, (x, y, t, sub, side) in enumerate(stops):
        bx = x + 26 if side == 'right' else x - 26 - 190
        pins += f"""<g class="pop" {d(i, .4, .9)}><circle cx="{x}" cy="{y}" r="16" fill="url(#gBV)"/><circle cx="{x}" cy="{y}" r="6" fill="#fff"/>
<g filter="url(#soft)"><rect class="glass2" x="{bx}" y="{y-28}" width="190" height="56" rx="16"/></g>
<text x="{bx+16}" y="{y-4}" font-size="14" font-weight="800">{t}</text><text class="m" x="{bx+16}" y="{y+14}" font-size="11.5">{sub}</text></g>"""
    body = f"""<g opacity=".22">{''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#93A1BF"/>' for x in range(20, W, 40) for y in range(20, H, 40))}</g>
<path d="{path}" fill="none" stroke="rgba(255,255,255,.10)" stroke-width="14" stroke-linecap="round"/>
<path class="draw" d="{path}" fill="none" stroke="url(#gSky)" stroke-width="6" stroke-linecap="round" style="stroke-dasharray:700;stroke-dashoffset:700"/>
<circle r="7" fill="#fff"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.6;1" calcMode="linear" path="{path}"/></circle>
{pins}
<g class="pop" style="animation-delay:3.6s"><g transform="translate(520 80)"><circle class="pulse" r="22" fill="none" stroke="#9D86FF" stroke-width="2"/>
<path d="M0 -14 L5 -2 L14 0 L5 3 L0 14 L-5 3 L-14 0 L-5 -2 Z" fill="#fff"/></g></g>
<g class="pop" style="animation-delay:4s"><rect x="40" y="40" width="210" height="64" rx="18" class="glass2"/>
<text class="a" x="60" y="66" font-size="10.5" font-weight="700" letter-spacing="1.4">OUR JOURNEY</text><text x="60" y="90" font-size="17" font-weight="800">5+ years of growth</text></g>"""
    css = '.draw{stroke-dasharray:700;stroke-dashoffset:700;animation:drawS 5s ease-in-out infinite}@keyframes drawS{0%{stroke-dashoffset:700}60%,92%{stroke-dashoffset:0}100%{stroke-dashoffset:700}}'
    return wrap(W, H, 'Graphics Storm Studio journey infographic', 'Animated infographic: our journey from a design studio, adding web development, then SEO and social media, to 130+ clients across the USA, Canada and worldwide.', body, css)

# ================= REVIEWS =================
def star(x, y, s=1, fill='#FFC857'):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -10 L2.9 -3.1 L10 -3.1 L4.3 1.2 L6.5 8.1 L0 4 L-6.5 8.1 L-4.3 1.2 L-10 -3.1 L-2.9 -3.1 Z" fill="{fill}"/>'

def reviews():
    W, H = 600, 480
    stars_big = ''.join(f'<g class="pop" {d(i, .2, .18)}>{star(78 + i*30, 160, 1.3)}</g>' for i in range(5))
    cards = [('“Fantastic brand guidelines and logos!”', 'Mr. James · Branding', 250, 70), ('“Fast communication, great result.”', 'Anthony · Website', 290, 190),
             ('“Brief well met, fast delivery.”', 'Lisa P. · Marketing', 250, 310)]
    cs = ''.join(f"""<g class="float" {d(i, 0, .8)}><g class="pop" {d(i, 1.1, .5)}><g filter="url(#soft)"><rect class="glass2" x="{x}" y="{y}" width="300" height="96" rx="18"/></g>
<circle cx="{x+30}" cy="{y+32}" r="14" fill="url(#gBV)"/><text x="{x+30}" y="{y+37}" text-anchor="middle" font-size="12" font-weight="800">{who[0]}</text>
{''.join(star(x+60 + k*16, y+28, .65) for k in range(5))}
<text x="{x+20}" y="{y+64}" font-size="12.5" font-weight="700">{q}</text><text class="m" x="{x+20}" y="{y+82}" font-size="10.5">{who}</text></g></g>""" for i, (q, who, x, y) in enumerate(cards))
    body = f"""<g filter="url(#soft)"><rect class="glass2" x="40" y="70" width="190" height="170" rx="20"/></g>
<text class="a" x="62" y="100" font-size="10.5" font-weight="700" letter-spacing="1.4">CLIENT RATING</text>
<text x="60" y="142" font-size="38" font-weight="800">5.0</text>
<g transform="translate(-4 0)">{stars_big}</g>
<text class="m" x="62" y="200" font-size="11">from verified clients</text><text class="m" x="62" y="218" font-size="11">USA · Canada · worldwide</text>
{cs}
<g class="pop" style="animation-delay:2.8s"><rect x="40" y="290" width="190" height="40" rx="20" fill="#7052FF"/><text x="135" y="315" text-anchor="middle" font-size="13" font-weight="700">✎ Leave a review</text></g>"""
    return wrap(W, H, 'Client reviews infographic', 'Animated infographic: a 5.0 client rating with five stars and review cards from website, branding and marketing clients.', body)

FILES = {'gss-growth-engine.svg': home, 'gss-website-development.svg': web, 'gss-seo-services.svg': seo,
         'gss-social-media-marketing.svg': smm, 'gss-graphic-design.svg': design,
         'gss-about.svg': about, 'gss-services-funnel.svg': funnel, 'gss-our-work.svg': work, 'gss-contact.svg': contact,
         'gss-privacy.svg': privacy, 'gss-terms.svg': terms, 'gss-our-story.svg': story, 'gss-reviews.svg': reviews}
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n, f in FILES.items():
        s = f(); open(os.path.join(OUT, n), 'w').write(s); print(n, len(s.encode()), 'bytes')
