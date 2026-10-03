"""Header + footer theme templates, rebuilt from the theme's rendered header (yprm 73) / footer (yprm 80) — same text & link targets."""
from lib import *
TEL = 'tel:(403) 991-2265'
def header():
    seed('header')
    top = C([ICONLIST([{'text': '324 41 Ave NE, UNIT B, Calgary, AB T2E 2N3', 'icon': ICO('map-marker-alt')},
                       {'text': 'info@bptowingservice.ca', 'icon': ICO('envelope'), 'link': 'mailto:info@bptowingservice.ca'}], '', view='inline'),
             ICONLIST([{'text': '(403) 991-2265', 'icon': ICO('phone-alt'), 'link': TEL}], '', view='inline')],
            'bp-topbar', boxed=True, row=True, css_classes='bp-topbar bp-row bp-keep bp-between bp-center')
    main = C([W('image', 'bp-logo bp-auto', image=img(2276), image_size='medium', link_to='custom', link=LINK(SITE + '/')),
              W('nav-menu', 'bp-nav', menu='menu-1', layout='horizontal', align_items='center', pointer='none',
                submenu_icon={'value': 'fas fa-chevron-down', 'library': 'fa-solid'}, dropdown='tablet', toggle='burger', full_width='stretch',
                text_align='aside'),
              BTN('Call For a Tow', TEL, 'bp-btn bp-hdr-cta bp-auto', icon='phone-alt')],
             'bp-mainbar', boxed=True, row=True, css_classes='bp-mainbar bp-row bp-keep bp-between bp-center bp-g24')
    return [SEC([HTML(assets_html(), 'bp-assets'), top, main], 'bp-header', boxed=False)]

def assets_html():
    css = open(os.path.join(HERE, 'ds.css')).read(); js = open(os.path.join(HERE, 'ds.js')).read()
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Manrope:wght@400..800&display=swap">'
            f'<style id="bp-ds">{css}</style><script id="bp-ds-js">{js}</script>')

def footer():
    seed('footer')
    flink = lambda items, cls='bp-flinks bp-dots': ICONLIST([{'text': t, 'link': u, 'icon': ICO('circle')} for t, u in items], cls)
    hd = lambda t: W('heading', 'bp-h', title=t, header_size='p')
    services = [('Auto Towing', '/auto-towing-calgary/'), ('Roadside Assistance', '/roadside-assistance/'),
                ('Flat Tire Change or Replacement', '/flat-tire-change-or-replacement/'), ('Fuel Delivery', '/fuel-delivery/'),
                ('Vehicle Jump Start', '/vehicle-jump-start-calgary/'), ('Winch Out Service', '/winch-out-service-calgary/'),
                ('Local Hauling', '/local-hauling/'), ('Motorcycle Towing', '/motorcycle-towing/')]
    quick = [('About Us', '/about-us/'), ("FAQ's", '/faq/'), ('Blog', '/blog/'), ('Contact', '/contact/')]
    wa = 'https://api.whatsapp.com/send/?phone=14039912265&text=Hi+BP+Towing%2C+I+need+immediate+assistance+with+my+vehicle.+Please+help%21&type=phone_number&app_absent=0'
    fb = 'https://www.facebook.com/people/BP-Towing/61583752828458/?mibextid=wwXIfr&rdid=WeEmuDyT7MokRuC0&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2F1BnVMwwrET%2F%3Fmibextid%3DwwXIfr'
    mapsrc = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d321200.49227131513!2d-114.087835!3d51.027623299999995!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40122c67a76bbbbf%3A0x554155f9f511cc61!2sBP%20Towing!5e0!3m2!1sen!2s!4v1775043038730!5m2!1sen!2s'
    col1 = C([W('image', 'bp-logo', image=img(2276), image_size='medium', link_to='custom', link=LINK(SITE + '/')),
              T('<p><em>Whether you’re stranded in Calgary, Airdrie, Stoney Trail or on Deerfoot Trail, BP Towing Service is ready to help 24/7.</em></p>'),
              hd('Follow Us'),
              W('social-icons', 'bp-social', social_icon_list=[{'_id': rid(), 'social_icon': ICO('facebook', 'fa-brands'), 'link': dict(LINK(fb), is_external='on')}],
                shape='rounded', align='left')], 'bp-g16')
    col2 = C([hd('Services'), flink([(t, SITE + u) for t, u in services])], 'bp-g12')
    col3 = C([hd('Quick Links'), flink([(t, SITE + u) for t, u in quick])], 'bp-g12')
    col4 = C([hd('Get In Touch'), ICONLIST([
        {'text': '(403) 991-2265', 'icon': ICO('phone-alt'), 'link': TEL},
        {'text': '(403) 991-2265', 'icon': ICO('whatsapp', 'fa-brands'), 'link': wa},
        {'text': 'info@bptowingservice.ca', 'icon': ICO('envelope'), 'link': 'mailto:info@bptowingservice.ca'},
        {'text': '324 41 Ave NE, UNIT B, Calgary, AB T2E 2N3', 'icon': ICO('map-marker-alt'), 'link': 'https://maps.app.goo.gl/x9A31d95UqhkyaUp9'}], 'bp-flinks')], 'bp-g12')
    col5 = C([hd('Reach Us'), HTML(f'<iframe src="{mapsrc}" width="600" height="350" style="border:0;border-radius:10px" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="BP Towing location map"></iframe>', 'bp-map')], 'bp-g12')
    grid = C([col1, col2, col3, col4, col5], 'bp-fgrid')
    copy_ = T('<p>Copyright  2026 © BP Towing Service, AB, Canada.</p>', 'bp-t bp-copy')
    return [SEC([grid, copy_, HTML('<div class="bp-wordmark" aria-hidden="true">BP TOWING</div>')], 'bp-footer')]
