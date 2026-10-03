"""New page: Long Distance Towing (slug long-distance-towing). Copy supplied by the client, used verbatim except:
[phone]/[Phone Number] -> (403) 991-2265 (tel link); bracketed author notes removed."""
from lib import *

TEL = 'tel:+14039912265'
PH = '<a href="tel:+14039912265"><strong>(403) 991-2265</strong></a>'
SLUG = 'long-distance-towing'
TITLE = 'Long Distance Towing'
SEO_TITLE = 'Long Distance Towing Calgary & Alberta | 24/7 | BP Towing'
SEO_DESC = ('Need long distance towing in Calgary or across Alberta? BP Towing offers 24/7 flatbed & heavy-duty towing from NW, N, SW & SE Calgary. '
            'Call (403) 991-2265 for a quote.')
FOCUS = 'long distance towing Calgary'

def ul(items, cls=''): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

SERVICES = [  # (service, best for, icon)
    ('Flatbed long distance towing', 'Luxury, AWD/4x4, electric, low-clearance and damaged vehicles', 'truck-moving'),
    ('Wheel-lift towing', 'Standard vehicles, shorter regional runs', 'truck-pickup'),
    ('Heavy-duty long distance towing', 'Trucks, vans, RVs, trailers and light commercial vehicles', 'truck'),
    ('Accident vehicle transport', 'Collision recovery to shops, yards or insurance sites', 'car-crash'),
    ('Dealership & auction transport', 'Vehicle moves for dealers, brokers and private buyers', 'gavel'),
    ('Motorcycle towing', 'Secure strapped transport for bikes', 'motorcycle'),
    ('Interprovincial towing', 'Alberta to BC, Saskatchewan and beyond', 'route'),
    ('Emergency 24/7 towing', 'Highway breakdowns and urgent roadside recovery', 'exclamation-triangle'),
]
AREAS = [
    ('Long Distance Towing in North Calgary', 'Beddington Heights, Country Hills, Harvest Hills, Coventry Hills, Panorama Hills, Livingston, Carrington, Evanston, Sage Hill, Kincora, Nolan Hill, Sherwood, Cityscape, Skyview Ranch, Redstone, Cornerstone, Stonegate, Huntington Hills, Thorncliffe, Greenview, Renfrew.'),
    ('Long Distance Towing in North West (NW) Calgary', 'Tuscany, Rocky Ridge, Royal Oak, Arbour Lake, Scenic Acres, Hamptons, Edgemont, Dalhousie, Brentwood, Varsity, University Heights, Silver Springs, Ranchlands, Hawkwood, Citadel, Hidden Valley, Sandstone, Charleswood, Montgomery, Bowness, Parkdale.'),
    ('Long Distance Towing in North East (NE) Calgary', 'Saddle Ridge, Taradale, Martindale, Falconridge, Castleridge, Cityscape, Redstone, Skyview Ranch, Temple, Pineridge, Marlborough, Forest Lawn, Calgary International Airport area, Deerfoot Trail corridor.'),
    ('Long Distance Towing in West &amp; South West (SW) Calgary', 'Signal Hill, Aspen Woods, Springbank Hill, West Springs, Cougar Ridge, Discovery Ridge, Coach Hill, Patterson, Strathcona Park, Glamorgan, Marda Loop, Killarney, Altadore, Mount Royal, Lakeview.'),
    ('Long Distance Towing in South Calgary', 'Shawnessy, Evergreen, Millrise, Somerset, Bridlewood, Woodbine, Woodlands, Midnapore, Sundance, Lake Bonavista, Acadia, Haysboro, Fish Creek Park area.'),
    ('Long Distance Towing in South East (SE) Calgary', 'McKenzie Towne, Auburn Bay, Mahogany, Seton, Cranston, New Brighton, Copperfield, Douglasdale, Chaparral, Walden, Legacy, Riverbend, Ogden, Inglewood.'),
    ('Central Calgary', 'Downtown, Beltline, Bridgeland, Mission, Victoria Park, Kensington, Hillhurst.'),
]
WHY = [  # (label, text, icon)
    ('24/7 availability:', 'Day, night, weekends and holidays.', 'clock'),
    ('Fast dispatch from Calgary:', 'Quick pickup in every quadrant of the city.', 'shipping-fast'),
    ('Safe flatbed transport:', 'Vehicle is loaded, strapped and secured properly.', 'truck-loading'),
    ('Transparent pricing:', 'Clear quote before we dispatch; any after-hours or toll charges are explained upfront.', 'file-invoice-dollar'),
    ('Experienced drivers:', 'Trained for Alberta\'s highway, winter and rural conditions, with 7+ years towing in Calgary.', 'id-badge'),
    ('All vehicle types:', 'Cars, SUVs, pickups, vans, motorcycles, AWD and luxury vehicles.', 'car-side'),
    ('Door-to-door service:', 'Home, shop, dealership, auction or storage.', 'map-marker-alt'),
    ('Insured towing:', 'Fully insured with cargo coverage while your vehicle is in transit.', 'shield-alt'),
]
STEPS = [
    ('Call or request a quote.', 'Give us your vehicle details, pickup location and destination.'),
    ('Get a clear price.', 'We quote based on distance, vehicle type and urgency.'),
    ('We dispatch a truck.', 'Our driver arrives at your Calgary location, or wherever you are in Alberta.'),
    ('Secure loading.', 'The vehicle is inspected, loaded onto the flatbed and strapped down.'),
    ('Safe delivery.', 'We transport it to your chosen destination and confirm handover.'),
]
FAQ = [
    ('What is long distance towing?', 'Long distance towing is the transport of a vehicle over a long route, generally 100 km or more, using a flatbed or tow truck. It is used for breakdowns, accidents, vehicle purchases and relocations.'),
    ('Do you offer long distance towing in Calgary?', 'Yes. BP Towing offers 24/7 long distance towing from all areas of Calgary, including North, North West, North East, South, South East, South West and Central Calgary, as well as nearby towns like Airdrie, Cochrane, Okotoks and Chestermere.'),
    ('Do you provide long distance towing across Alberta?', 'Yes. We tow vehicles from Calgary to Edmonton, Red Deer, Lethbridge, Medicine Hat, Banff, Grande Prairie, Fort McMurray and other Alberta destinations.'),
    ('Can you tow my vehicle out of Alberta?', 'Yes. We provide interprovincial towing to British Columbia, Saskatchewan and other provinces. Call for a custom quote.'),
    ('How much does long distance towing cost in Calgary?', 'The price depends on distance, vehicle type, truck type, time of day and road conditions. Most companies charge a base hook-up fee plus a per-kilometre rate. Call us for an accurate quote.'),
    ('How far can a tow truck tow a car?', 'A professional flatbed tow truck can transport a vehicle hundreds or even thousands of kilometres, since the vehicle rides on the bed rather than being pulled on its own wheels.'),
    ('Is flatbed towing better for long distance?', 'Yes. A flatbed keeps all four wheels off the road, protecting the transmission, tires, suspension and drivetrain. It is the safest option for AWD, luxury, electric and damaged vehicles.'),
    ('Can you tow an AWD, 4x4 or electric vehicle long distance?', 'Yes. We use flatbed transport for AWD, 4x4 and electric vehicles, which should not be towed with their wheels on the ground.'),
    ('Do you offer 24/7 emergency long distance towing?', 'Yes. We are available 24 hours a day, 7 days a week, including holidays and during winter weather.'),
    ('How fast can you arrive for pickup in Calgary?', 'Arrival time depends on your location and current demand. We dispatch from Calgary and aim to reach most areas quickly. In most Calgary neighbourhoods, expect 20 to 35 minutes.'),
    ('Can you tow a vehicle after an accident?', 'Yes. We recover and transport accident-damaged vehicles to repair shops, insurance yards or your home.'),
    ('Do you tow motorcycles, vans and trucks long distance?', 'Yes. We handle motorcycles, cars, SUVs, pickups, vans and light commercial vehicles. Contact us for heavier or oversized loads.'),
    ('Is my vehicle insured while being towed?', 'Yes. BP Towing carries commercial liability and cargo insurance, so your vehicle is covered while in our care. Ask your dispatcher for coverage details when booking.'),
    ('How do I book long distance towing?', f'Call {PH}, or send your pickup location, destination and vehicle details through our contact form. We\'ll confirm the price and send a truck.'),
]

def head(eyebrow, title, tag='h2', cls='bp-h2', center=False):
    out = []
    if eyebrow: out.append(W('heading', 'bp-h bp-eyebrow', title=eyebrow, header_size='div', _animation='fadeInUp'))
    out.append(W('heading', 'bp-h ' + cls, title=title, header_size=tag, _animation='fadeInUp', _animation_delay=80))
    return out

def accordion(items):
    kids = [{'id': rid(), 'elType': 'container', 'isInner': True, 'settings': {'content_width': 'full', 'css_classes': 'bp-col'},
             'elements': [T(f'<p>{a}</p>')]} for _, a in items]
    s = {'items': [{'item_title': q, '_id': rid()} for q, _ in items], 'title_tag': 'h3', 'faq_schema': 'yes',
         'accordion_item_title_icon': ICO('chevron-down'), 'accordion_item_title_icon_active': ICO('chevron-down'),
         'default_state': 'expanded', 'max_items_expended': 'one', '_css_classes': 'bp-faq'}
    return {'id': rid(), 'elType': 'widget', 'widgetType': 'nested-accordion', 'isInner': False, 'settings': s, 'elements': kids}

def split(txt, mid, surface='bp-light', media_left=False, extra=''):
    tcol = C([HTML('<span class="bp-kicker"></span>')] + txt, 'bp-f1')
    mcol = C([IMG(mid, 'bp-media bp-media-wide', size='large')], 'bp-frame bp-split-media', animation='fadeInLeft' if media_left else 'fadeInRight')
    return SEC([mcol, tcol] if media_left else [tcol, mcol], '', row=True, css_classes=f'bp bp-sec {surface} bp-split bp-row bp-g64 bp-center {extra}')

def build(stats_id):
    seed('long-distance'); S_ = []
    # 1 hero + quote form
    form_tpl = tree(3358)[0]
    copy_ = C(head('', 'Long Distance Towing in Calgary &amp; Alberta', 'h1', 'bp-h1') + [
        T('<p>Long distance towing is the transport of a vehicle over a long distance, typically 100 km or more, on a flatbed or wheel-lift tow truck, so the vehicle is not driven and takes no extra wear. BP Towing Service provides 24/7 long distance towing in Calgary, across Alberta and into neighbouring provinces. We pick up from any Calgary community, including the NW, N, NE, SW, SE and Central areas, and deliver directly to your home, workshop, dealership, auction or storage facility.</p>', 'bp-lead'),
        T(f'<p>📞 Call {PH} for an instant quote | Available 24/7, 365 days a year</p>', 'bp-lead bp-callline'),
        C([BTN('(403) 991-2265', TEL, 'bp-btn', icon='phone-alt')], 'bp-btns', row=True, animation='fadeInUp', animation_delay=200)], 'bp-hero-copy')
    side = C([FORM(3358, form_tpl['id'], widths=[100, 50, 50, 100, 100])], 'bp-hero-side bp-formcard bp-glass bp-spot bp-on-dark', animation='fadeInRight')
    S_.append(SEC([copy_, side], 'bp-hero bp-hero-svc', row=True, background_background='slideshow',
                  background_slideshow_gallery=[{'id': i, 'url': MEDIA[i]['source_url']} for i in (4298, 4471, 4433)],
                  background_slideshow_ken_burns='yes', background_slideshow_slide_duration=6000, background_slideshow_transition='fade',
                  background_size='cover', background_position='center center'))
    # 2 ticker (service names from the table)
    names = [s for s, _, _ in SERVICES]
    sp = lambda h: ''.join('<span' + (' aria-hidden="true"' if h else '') + '>' + n + '</span>' for n in names)
    S_.append(SEC([HTML(f'<div class="bp-tk"><div class="bp-tk-track">{sp(0)}{sp(1)}</div></div>')], 'bp-ticker', boxed=False))
    # 3 what is
    S_.append(split(head('', 'What Is Long Distance Towing?') + [
        T('<p>Long distance towing is a professional service for moving cars, SUVs, trucks, vans, motorcycles and other vehicles between cities, regions or provinces. It is used when a vehicle is broken down, damaged after a collision, not drivable, or simply being relocated. Because the vehicle rides on a flatbed, its odometer, tires, transmission and drivetrain are protected during the trip.</p><p><strong>Common reasons people book long distance towing:</strong></p>' + ul([
            'Breakdown far from home (highway, rural road or another city)', 'Accident recovery and transport to a repair shop or insurer\'s yard',
            'Moving a vehicle after buying it (private sale, dealership or online auction)', 'Relocating to or from Alberta',
            'Transporting a vehicle to a specialist mechanic or collision centre',
            'Moving classic, luxury, low-clearance or AWD vehicles that cannot be driven or towed by wheel-lift']), 'bp-t bp-list')], 4296))
    # 4 services (table -> cards)
    cards = []
    for i, (svc, best, ic) in enumerate(SERVICES):
        cards.append(ANIM(C([W('icon-box', 'bp-feat bp-glass bp-spot', selected_icon=ICO(ic), title_text=svc, title_size='h3',
                               description_text=f'<strong>Best for:</strong> {best}')], 'bp-cardwrap'), 'fadeInUp', (i % 4) * 100))
    S_.append(SEC([C(head('', 'Our Long Distance Towing Services in Calgary'), 'bp-head-c'), C(cards, 'bp-grid-4')], 'bp-sec bp-dark bp-aura bp-gridbg bp-ld-svc'))
    # 5 stats
    S_.append(SEC([W('template', '', template_id=stats_id)], '', boxed=False))
    # 6 areas
    acards = [ANIM(C([W('heading', 'bp-h bp-area-t', title=t, header_size='h3'), T(f'<p>{c}</p>', 'bp-t bp-area-c')],
                     'bp-area bp-glass-light bp-spot'), 'fadeInUp', (i % 3) * 100) for i, (t, c) in enumerate(AREAS)]
    S_.append(SEC([C(head('', 'Long Distance Towing Across Calgary: Areas We Cover') +
                     [T('<p>We dispatch from Calgary and serve every quadrant of the city with fast pickup.</p>', 'bp-lead')], 'bp-head-c'),
                   C(acards, 'bp-grid-3 bp-area-grid'),
                   T('<p><strong>Surrounding communities near Calgary:</strong> Airdrie, Cochrane, Chestermere, Okotoks, High River, Strathmore, Balzac, Springbank, Bearspaw, Langdon, Black Diamond, Turner Valley.</p>', 'bp-t bp-area-more')],
                  'bp-sec bp-soft'))
    # 7 across Alberta
    S_.append(split(head('', 'Long Distance Towing Across Alberta') + [
        T('<p>BP Towing provides long distance towing from Calgary to all major Alberta cities and highways, including:</p>' + ul([
            'Calgary to Edmonton (approx. 300 km) via Highway 2 (QEII)', 'Calgary to Red Deer (approx. 150 km)',
            'Calgary to Lethbridge (approx. 210 km) via Highway 2 and Highway 3', 'Calgary to Medicine Hat via Highway 1 (Trans-Canada)',
            'Calgary to Banff, Canmore and Lake Louise via Highway 1', 'Calgary to Grande Prairie, Fort McMurray and Lloydminster',
            'Calgary to Drumheller, Brooks, Camrose and Leduc', 'Northern and rural Alberta pickups, on request']) +
          '<p><strong>Beyond Alberta:</strong> We also arrange towing to British Columbia (Kelowna, Vancouver, Kamloops), Saskatchewan (Regina, Saskatoon) and other provinces. Call us for interprovincial rates.</p>',
          'bp-t bp-list bp-list-pin')], 4367, surface='bp-light', media_left=True))
    # 8 why choose (photo + numbered rows)
    rows = [ANIM(C([W('icon-box', 'bp-feat-row', selected_icon=ICO(ic), title_text=l.rstrip(':'), title_size='h3', description_text=t, position='left')],
                   'bp-step'), 'fadeInUp', (i % 4) * 80) for i, (l, t, ic) in enumerate(WHY)]
    S_.append(SEC([C([IMG(4471, 'bp-media', size='large')], 'bp-oc-media', animation='fadeInLeft'),
                   C(head('', 'Why Choose BP Towing for Long Distance Towing?') + [C(rows, 'bp-oc-rows bp-oc-2col')], 'bp-oc-copy')],
                  '', row=True, css_classes='bp bp-sec bp-onecall bp-light bp-row bp-g64'))
    # 9 how it works (timeline)
    steps = [ANIM(C([HTML(f'<span class="bp-tl-n">{i + 1}</span>'), W('heading', 'bp-h bp-tl-t', title=a, header_size='h3'), T(f'<p>{b}</p>', 'bp-t bp-tl-d')],
                    'bp-tl-step bp-glass bp-spot'), 'fadeInUp', i * 120) for i, (a, b) in enumerate(STEPS)]
    S_.append(SEC([C(head('', 'How Long Distance Towing Works (Step by Step)'), 'bp-head-c'), C(steps, 'bp-timeline')], 'bp-sec bp-dark bp-gradient'))
    # 10 cost
    S_.append(split(head('', 'How Much Does Long Distance Towing Cost in Calgary?') + [
        T('<p>Long distance towing cost depends on:</p>' + ul([
            '<strong>Distance:</strong> Usually charged per kilometre after a base hook-up fee',
            '<strong>Vehicle type and weight:</strong> A motorcycle costs less to tow than a heavy truck',
            '<strong>Truck type:</strong> Flatbed vs wheel-lift vs heavy-duty',
            '<strong>Time and urgency:</strong> After-hours, holiday and emergency calls may cost more',
            '<strong>Road and weather conditions:</strong> Winter and remote pickups may affect pricing',
            '<strong>Vehicle condition:</strong> Accident-damaged or stuck vehicles may need extra equipment']) +
          f'<p>For an exact figure, call {PH} or request a free quote online.</p>', 'bp-t bp-list')], 4433, surface='bp-soft'))
    # 11 tips
    S_.append(SEC([C(head('', 'Tips Before Booking Long Distance Towing'), 'bp-head-c'),
                   T(ul(['Have your vehicle\'s make, model, year and condition ready.', 'Confirm exact pickup and drop-off addresses.',
                         'Remove valuables and personal items from the vehicle.',
                         'Tell the dispatcher if the vehicle is AWD, lowered, damaged, or won\'t roll or steer.',
                         'Ask whether the quote includes tolls, fuel and after-hours fees.']), 'bp-t bp-list bp-tips')], 'bp-sec bp-light'))
    # 12 reviews (shared site element)
    rv = find(3427, lambda e: e.get('widgetType') in ('pt-heading', 'shortcode'))
    S_.append(SEC([C(head((rv[0]['settings'].get('subtitle') or '').strip(), rv[0]['settings']['title']), 'bp-head-c'),
                   W('shortcode', 'bp-reviews', shortcode=rv[1]['settings']['shortcode'])], 'bp-sec bp-soft'))
    # 13 FAQ
    S_.append(SEC([C([HTML('<span class="bp-kicker"></span>')] + head('', 'Frequently Asked Questions (FAQs)'), 'bp-faq-side bp-f1'),
                   C([accordion(FAQ)], 'bp-faq-main')], 'bp-sec bp-light', row=True, css_classes='bp bp-sec bp-light bp-row bp-g64 bp-faqwrap'))
    # 14 final CTA
    S_.append(SEC([W('heading', 'bp-h', title='Call BP Towing for Long Distance Towing in Calgary &amp; Alberta', header_size='h2', _animation='zoomIn'),
                   T('<p>Whether you\'re broken down on Highway 2, moving a vehicle from NW Calgary to Edmonton, or shipping a car across provinces, BP Towing has a truck ready.</p>'
                     f'<p>📞 Call {PH} now for a fast, no-obligation quote.<br>📍 Serving: Calgary, Alberta and beyond.</p>', 'bp-t'),
                   BTN('(403) 991-2265', TEL, 'bp-btn bp-btn-white bp-btn-xl bp-pulse', icon='phone-alt')], 'bp-sec bp-cta'))
    return S_
