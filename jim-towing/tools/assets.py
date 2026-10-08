"""Push site-wide assets to Elementor's global places (no CSS/JS inside widgets):
  - CSS  -> Elementor Site Settings > Custom CSS (kit 390, _elementor_page_settings.custom_css)  — readable, commented
  - Head -> Custom Code snippet (font preloads, Font Awesome, LocalBusiness JSON-LD), location <head>
  - JS   -> Custom Code snippet (site interactions), location </body>
Usage: python3 assets.py"""
import json, os
from wp import req
import lib
c = json.load(open(os.path.join(lib.D, 'created.json')))
KIT = 390

HEADER = """/* =====================================================================
   JIM TOWING LTD. — GLOBAL STYLES (Elementor > Site Settings > Custom CSS)
   Design system for every page, the header/footer templates and the blog
   templates. Classes are prefixed `j-` and added to widgets/containers via
   Advanced > CSS Classes. Do not paste CSS into individual widgets.

   CONTENTS
   01  Fonts (Outfit headings, Figtree body) — self-declared @font-face
   02  Tokens (:root colours, radii, shadows, fonts) + base/reset
   03  Typography, sections, reveal animations
   04  Buttons (all states locked — Astra greys hovered/focused buttons)
   05  Header (topbar, sticky/auto-hide main bar, nav, call pill)
   06  Home hero, request form card, service ticker
   07  Split/media blocks, check lists, notes
   08  Service cards, scrolly service explorer, situation tabs
   09  Stats, why-cards, steps road, route map, chips, gallery, reviews
   10  FAQ accordion, CTA band, inner-page hero, Key facts ticket, Quick answer
   11  Feature cards, info blocks, comparison, related, pricing, contact
   12  Blog (archive cards, single post, prose, sidebar)
   13  Footer (road strip, dispatch board, brand panel, map, credits)
   14  Floating actions (call button, back-to-top, mobile call bar)
   15  Responsive (≤1100 / ≤1024 tablet / ≤767 mobile) + reduced motion
   ===================================================================== */

/* ---------- 01 · Fonts (Google Fonts, latin + latin-ext, variable weights) ---------- */
"""

def build_css():
    gf = open(os.path.join(lib.D, 'gfonts.css')).read().strip()
    css = open(os.path.join(lib.D, 'jim.css')).read().strip()
    css = css.replace('/* ==== Jim Towing Ltd. — design system (loaded site-wide from the header template) ==== */',
                      '/* ---------- 02 · Tokens + base ---------- */')
    return HEADER + gf + '\n\n' + css + '\n'

def head_html():
    return ('<!-- Jim Towing — head assets: preload the two variable fonts used site-wide, load Font Awesome 5 without blocking render, LocalBusiness schema -->\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="preload" as="font" type="font/woff2" href="https://fonts.gstatic.com/s/outfit/v15/QGYvz_MVcBeNP4NJtEtq.woff2" crossorigin>\n'
            '<link rel="preload" as="font" type="font/woff2" href="https://fonts.gstatic.com/s/figtree/v9/_Xms-HUzqDCFdgfMm4S9DQ.woff2" crossorigin>\n'
            '<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>\n'
            f'<link rel="preload" as="style" href="{lib._FA}" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
            f'<noscript><link rel="stylesheet" href="{lib._FA}"></noscript>\n'
            f'<script type="application/ld+json">{json.dumps(lib.LD)}</script>\n')

def js_html():
    return ('<!-- Jim Towing — site interactions: header states, scroll progress, reveals, counters, tilt/magnetic, '
            'situation tabs, scrolly explorer, gallery lightbox, steps road, live Calgary clock -->\n<script>\n' + open(os.path.join(lib.D, 'jim.js')).read() + '\n</script>\n')

if __name__ == '__main__':
    kit = req(f'wp/v2/elementor_library/{KIT}?context=edit')
    ps = kit['meta'].get('_elementor_page_settings') or {}
    if isinstance(ps, list): ps = {}
    ps['custom_css'] = build_css()
    r = req(f'wp/v2/elementor_library/{KIT}', 'POST', {'meta': {'_elementor_page_settings': ps}})
    print('kit css', r.get('id'), r.get('_err') or len(ps['custom_css']))
    for key, loc, prio, code in [('head', 'elementor_head', 1, head_html()), ('js', 'elementor_body_end', 10, js_html())]:
        r = req(f"wp/v2/elementor_snippet/{c['snippets'][key]}", 'POST', {'status': 'publish', 'meta': {'_elementor_location': loc, '_elementor_priority': prio, '_elementor_code': code}})
        print('snippet', key, r.get('id'), r.get('status'), r.get('_err') or '')
    req('elementor/v1/cache', 'DELETE')
