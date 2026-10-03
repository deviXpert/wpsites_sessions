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
              mega_menu(),
              BTN('Call For a Tow', TEL, 'bp-btn bp-hdr-cta bp-auto', icon='phone-alt'),
              mobile_menu()],
             'bp-mainbar', boxed=True, row=True, css_classes='bp-mainbar bp-row bp-keep bp-between bp-center bp-g24')
    return [SEC([HTML(assets_html(), 'bp-assets'), top, main], 'bp-header', boxed=False)]

def assets_html():
    css = open(os.path.join(HERE, 'ds.css')).read(); js = open(os.path.join(HERE, 'ds.js')).read()
    E = 'https://bptowingservice.ca/wp-content/plugins/elementor/assets/css/'
    EP = 'https://bptowingservice.ca/wp-content/plugins/elementor-pro/assets/css/'
    early = ''.join(f'<link rel="stylesheet" href="{u}">' for u in (
        EP + 'widget-nav-menu.min.css?ver=4.3.0', E + 'widget-icon-list.min.css?ver=4.3.3',
        E + 'widget-icon-box.min.css?ver=4.3.3', E + 'widget-social-icons.min.css?ver=4.3.3'))
    return (early + '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Manrope:wght@400..800&display=swap">'
            f'<style id="bp-ds">{css}</style><script id="bp-ds-js">{js}</script>')

SERVICES = [('Auto Towing', '/auto-towing-calgary/', 'truck', 'Flatbed & wheel-lift towing for cars, SUVs and light trucks.'),
            ('Roadside Assistance', '/roadside-assistance/', 'road', 'Quick fixes on the spot — boosts, tires, fuel and lockouts.'),
            ('Flat Tire Change or Replacement', '/flat-tire-change-or-replacement/', 'tools', 'On-site tire changes at home, work or the roadside.'),
            ('Fuel Delivery', '/fuel-delivery/', 'gas-pump', 'Gas, diesel & premium delivered to your location.'),
            ('Vehicle Jump Start', '/vehicle-jump-start-calgary/', 'car-battery', '24/7 battery boosts — even in extreme Calgary cold.'),
            ('Winch Out Service', '/winch-out-service-calgary/', 'link', 'Pulled out of snow, mud or ditches without damage.'),
            ('Local Hauling', '/local-hauling/', 'truck-loading', 'Equipment, trailers, ATVs and materials moved locally.'),
            ('Motorcycle Towing', '/motorcycle-towing/', 'motorcycle', 'Flatbed-only bike transport with soft straps.'),
            ('Special Vehicle Towing', '/special-vehicle-towing/', 'car-side', 'Luxury, exotic, lowered and oversized vehicles.'),
            ('Long Distance Towing', '/long-distance-towing/', 'route', 'Calgary, across Alberta and into neighbouring provinces.')]
MENU = [('Home', '/'), ('Services', '/services/'), ('About Us', '/about-us/'), ('FAQ', '/faq/'), ('Contact', '/contact/'), ('Blog', '/blog/')]

def mega_menu():
    """Desktop mega menu built from native containers/widgets (same items & link targets as WP menu 'Menu 1').
    Services panel opens on hover / keyboard focus (CSS :hover/:focus-within). Hidden on tablet/mobile."""
    items = []
    for title, path in MENU:
        link = W('heading', 'bp-mlink', title=title, header_size='div', link=LINK(SITE + path))
        if title != 'Services':
            items.append(C([link], 'bp-mitem')); continue
        feature = C([W('heading', 'bp-h', title='Services', header_size='div', link=LINK(SITE + path)),
                     BTN('Call For a Tow', TEL, 'bp-btn', icon='phone-alt')],
                    'bp-mega-feature', background_background='classic', background_image=img(4333),
                    background_size='cover', background_position='center center')
        links = [W('icon-box', 'bp-mega-link', selected_icon=ICO(ic), title_text=t, description_text=dsc, title_size='div', link=LINK(SITE + u), position='left')
                 for t, u, ic, dsc in SERVICES]
        panel = C([C([feature, C(links, 'bp-mega-grid')], 'bp-mega-inner', row=True, css_classes='bp-mega-inner bp-row')], 'bp-mpanel')
        items.append(C([link, panel], 'bp-mitem bp-has-mega'))
    return C(items, 'bp-mnav', row=True, css_classes='bp-mnav bp-row bp-keep bp-center', hide_tablet='hidden-tablet', hide_mobile='hidden-mobile')

def mobile_menu():
    """Elementor Pro Nav Menu in dropdown-only layout for tablet/mobile (uses WP menu 'Menu 1')."""
    return W('nav-menu', 'bp-nav bp-mobnav bp-auto', menu='menu-1', layout='dropdown', toggle='burger', full_width='stretch',
             submenu_icon={'value': 'fas fa-chevron-down', 'library': 'fa-solid'}, toggle_icon_normal=ICO('bars'), toggle_icon_active=ICO('times'),
             hide_desktop='hidden-desktop', toggle_align='right')

def footer():
    seed('footer')
    flink = lambda items, cls='bp-flinks bp-dots': ICONLIST([{'text': t, 'link': u, 'icon': ICO('circle')} for t, u in items], cls)
    hd = lambda t: W('heading', 'bp-h', title=t, header_size='p')
    services = [('Auto Towing', '/auto-towing-calgary/'), ('Roadside Assistance', '/roadside-assistance/'),
                ('Flat Tire Change or Replacement', '/flat-tire-change-or-replacement/'), ('Fuel Delivery', '/fuel-delivery/'),
                ('Vehicle Jump Start', '/vehicle-jump-start-calgary/'), ('Winch Out Service', '/winch-out-service-calgary/'),
                ('Local Hauling', '/local-hauling/'), ('Motorcycle Towing', '/motorcycle-towing/'), ('Long Distance Towing', '/long-distance-towing/')]
    quick = [('About Us', '/about-us/'), ("FAQ's", '/faq/'), ('Blog', '/blog/'), ('Contact', '/contact/')]
    wa = 'https://api.whatsapp.com/send/?phone=14039912265&text=Hi+BP+Towing%2C+I+need+immediate+assistance+with+my+vehicle.+Please+help%21&type=phone_number&app_absent=0'
    fb = 'https://www.facebook.com/people/BP-Towing/61583752828458/?mibextid=wwXIfr&rdid=WeEmuDyT7MokRuC0&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2F1BnVMwwrET%2F%3Fmibextid%3DwwXIfr'
    mapsrc = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d321200.49227131513!2d-114.087835!3d51.027623299999995!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40122c67a76bbbbf%3A0x554155f9f511cc61!2sBP%20Towing!5e0!3m2!1sen!2s!4v1775043038730!5m2!1sen!2s'
    brand = C([W('image', 'bp-logo bp-auto', image=img(2276), image_size='medium', link_to='custom', link=LINK(SITE + '/')),
               T('<p><em>Whether you’re stranded in Calgary, Airdrie, Stoney Trail or on Deerfoot Trail, BP Towing Service is ready to help 24/7.</em></p>')],
              'bp-fbrand', row=True, css_classes='bp-fbrand bp-row bp-center')
    top = C([brand, BTN('(403) 991-2265', TEL, 'bp-btn bp-fcall bp-auto', icon='phone-alt')], 'bp-ftop', row=True,
            css_classes='bp-ftop bp-row bp-between bp-center')
    follow = C([hd('Follow Us'), W('social-icons', 'bp-social', social_icon_list=[{'_id': rid(), 'social_icon': ICO('facebook', 'fa-brands'), 'link': dict(LINK(fb), is_external='on')}],
                shape='rounded', align='left', icon_size={'unit': 'px', 'size': 16})], 'bp-ffollow', row=True, css_classes='bp-ffollow bp-row bp-keep bp-center')
    col2 = C([hd('Services'), flink([(t, SITE + u) for t, u in services])], 'bp-g12')
    col3 = C([hd('Quick Links'), flink([(t, SITE + u) for t, u in quick])], 'bp-g12')
    col4 = C([hd('Get In Touch'), ICONLIST([
        {'text': '(403) 991-2265', 'icon': ICO('phone-alt'), 'link': TEL},
        {'text': '(403) 991-2265', 'icon': ICO('whatsapp', 'fa-brands'), 'link': wa},
        {'text': 'info@bptowingservice.ca', 'icon': ICO('envelope'), 'link': 'mailto:info@bptowingservice.ca'},
        {'text': '324 41 Ave NE, UNIT B, Calgary, AB T2E 2N3', 'icon': ICO('map-marker-alt'), 'link': 'https://maps.app.goo.gl/x9A31d95UqhkyaUp9'}], 'bp-flinks')], 'bp-g12')
    col5 = C([hd('Reach Us'), HTML(f'<iframe src="{mapsrc}" width="600" height="350" style="border:0;border-radius:10px" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="BP Towing location map"></iframe>', 'bp-map')], 'bp-g12')
    grid = C([col2, col3, col4, col5], 'bp-fgrid')
    copy_ = T('<p>Copyright  2026 © BP Towing Service, AB, Canada.</p>', 'bp-t bp-copy')
    credit = T('<p>Designed and Developed by <a href="https://hafizahsanali.com/" target="_blank" rel="noopener">hafizahsanali.com</a></p>', 'bp-t bp-credit')
    bottom = C([copy_, credit, follow], 'bp-fbottom', row=True, css_classes='bp-fbottom bp-row bp-between bp-center')
    return [SEC([top, grid, bottom], 'bp-footer')]
