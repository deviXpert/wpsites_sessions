from lib import *

def form_widget(cls='j-form', name='Hero Service Request', btn='Request Dispatch', msg=True):
    opts = '\n'.join(['24/7 Emergency Towing', 'Flatbed Towing', 'Roadside Assistance', 'Long-Distance Transport', 'Battery Jump-Start', 'Emergency Fuel Delivery', 'Not sure — please advise'])
    f = [
        {'_id': rid(), 'custom_id': 'name', 'field_type': 'text', 'field_label': 'Your name', 'placeholder': 'Your name', 'required': 'true', 'width': '50'},
        {'_id': rid(), 'custom_id': 'phone', 'field_type': 'tel', 'field_label': 'Phone number', 'placeholder': 'Phone number', 'required': 'true', 'width': '50'},
        {'_id': rid(), 'custom_id': 'location', 'field_type': 'text', 'field_label': 'Pickup location', 'placeholder': 'Pickup location (address, cross streets or landmark)', 'required': 'true', 'width': '100'},
        {'_id': rid(), 'custom_id': 'service', 'field_type': 'select', 'field_label': 'Service needed', 'field_options': opts, 'width': '100'},
    ]
    if msg:
        f.append({'_id': rid(), 'custom_id': 'message', 'field_type': 'textarea', 'field_label': 'Vehicle & details', 'placeholder': 'Vehicle make/model, destination and what happened', 'rows': 3, 'width': '100'})
    f.append({'_id': rid(), 'custom_id': 'hp', 'field_type': 'honeypot', 'field_label': 'Honeypot', 'width': '100'})
    return W('form', cls, form_name=name, form_fields=f, show_labels='', input_size='md', button_text=btn, button_size='md',
             selected_button_icon=ICO('paper-plane'), button_icon_align='row-reverse', button_icon_indent={'unit': 'px', 'size': 10},
             submit_actions=['email', 'save-to-database'], email_to=EMAIL, email_subject='New service request from jimtowing.ca',
             email_content='[all-fields]', email_from_name='Jim Towing Website', email_reply_to='', email_content_type='html',
             success_message=f"Thanks — we've received your request and will call you back shortly. For the fastest dispatch, call {PHONE}.",
             error_message=f'Something went wrong. Please call us directly at {PHONE}.', required_message='This field is required.', form_id='jim-request-form')

def build():
    seed('home')
    # ---------- hero ----------
    trust = (f'<div class="j-trust"><div><span class="j-ti g"><i class="fab fa-google" style="color:#4285F4"></i></span><span><b>{RATING} {stars()}</b><span>{REVIEWS} Google reviews</span></span></div>'
             '<div><span class="j-ti"><i class="fas fa-clock"></i></span><span><b>24/7</b><span>Nights, weekends, holidays</span></span></div>'
             '<div><span class="j-ti"><i class="fas fa-tag"></i></span><span><b>From $75</b><span>Quote before dispatch</span></span></div></div>')
    hero = C([
        W('image', 'j-hero-bg', image={'url': iu('downtown', 'full'), 'id': IMG['downtown']}, image_size='1536x1536'),
        C([
            C([T('<p><span class="j-dot"></span>Dispatch online now &middot; Calgary, Alberta</p>', 'j-pill rv'),
               H(f'24/7 Towing Services in {hl("Calgary")}', 'h1', 'j-splitw'),
               P('When you need a reliable towing service in Calgary, <strong>Jim Towing is ready to help.</strong> We provide 24/7 towing and roadside assistance for breakdowns, accidents, dead batteries, flat tires, low fuel and other roadside emergencies.', 'j-lead rv rv-d1'),
               BTNS(CALL(), QUOTE('j-btn-ghost', '#request'), cls='rv rv-d2'),
               RAW(trust, 'rv rv-d3')], 'j-hero-copy j-col'),
            C([H('Need a tow? <span style="color:var(--j-red)">Get help now.</span>', 'h2', 'j-cf-t'),
               P("Send your details and we'll call you back to confirm dispatch and pricing.", 'j-cf-s'),
               form_widget(),
               P(f'Stranded right now? <a href="{TEL}">Call {PHONE}</a> for immediate dispatch.', 'j-cf-note')], 'j-card-form j-col rv rv-r', _element_id='request'),
        ], 'j-in', fd='row'),
    ], 'j-hero', tag='section')

    # ---------- intro ----------
    badge = RAW('<div class="j-badge-in"><svg viewBox="0 0 150 150" aria-hidden="true"><defs><path id="jc" d="M75,75 m-56,0 a56,56 0 1,1 112,0 a56,56 0 1,1 -112,0"/></defs><text><textPath href="#jc">Calgary towing • Roadside help • 24/7 • </textPath></text></svg><b>24/7</b></div>', 'j-badge')
    intro = sec([C([
        C([IMGW('winter', 'j-m1'), IMGW('suv_op', 'j-m2'), badge], 'j-media rv rv-l'),
        C([EB('Reliable towing in Calgary'),
           H(f'Help That Shows Up When You Need It {hl("Most")}', 'h2', 'j-h2'),
           T('<p>Vehicle problems rarely happen at a convenient time. A breakdown on your way to work, an accident late at night or a dead battery in a parking lot can leave you wondering what to do next. <strong>That\'s where Jim Towing comes in.</strong></p>'
             '<p>Our Calgary towing services are designed to provide practical help for different roadside situations. From emergency towing and flatbed transportation to battery jump-starts and emergency fuel delivery, our team can get your vehicle safely transported — or get you back on the road when a tow isn\'t necessary.</p>'
             '<p>Our professional towing team serves Calgary and surrounding Alberta communities with a focus on fast dispatch, safe vehicle handling, clear communication and dependable service. Whether you need a tow across Calgary or long-distance transport to another Alberta city, we can get your vehicle where it needs to go.</p>'),
           T('<p>We know drivers searching for “towing Calgary”, “tow truck Calgary” or “emergency towing near me” usually need help quickly — that\'s why we focus on responsive dispatch and professional vehicle handling.</p>', 'j-note'),
           BTNS(CALL('j-btn-dark'), BTN('Explore services', '#services', 'j-btn-line', 'arrow-down', True))], 'j-stack j-col rv rv-r'),
    ], 'j-split', fd='row')], 'j-white')

    # ---------- services grid ----------
    cards = svc_cards()
    services = sec([headrow('Our services', f'Towing &amp; Roadside {hl("Services")}', 'Jim Towing provides six core services for Calgary drivers — one call covers everything from a dead battery to a cross-Alberta move.', BTN('View all services', PAGES['services'], 'j-btn-line j-btn-sm', 'arrow-right', True)),
                    C(cards, 'j-svc-grid')], 'j-paper', _element_id='services')

    # ---------- scrolly details ----------
    det = [
        ('emergency-towing-calgary', 'redsuv', '<p>When your vehicle cannot be safely driven, you need a towing company that responds when you need it. Our 24/7 Emergency Towing service covers breakdowns, accidents and any situation where your vehicle needs to be transported safely — day or night, 7 days a week.</p>',
         ['Local repair shop', 'Dealership', 'Home', 'Private location', 'Your preferred destination'], 'Our goal is simple: dispatch professional help, handle your vehicle carefully and get it transported safely.'),
        ('flatbed-towing-calgary', 'luxury', '<p>Some vehicles need extra care. A flatbed loads your vehicle onto the truck rather than pulling it along the road — the practical choice when vehicle protection is a priority.</p>',
         ['Luxury cars', 'AWD vehicles', 'Low-clearance vehicles', 'SUVs', 'Motorcycles', 'Accident-damaged vehicles'], "Not sure which method is right? We'll help determine the appropriate towing solution for your vehicle."),
        ('roadside-assistance-calgary', 'suv_op', '<p>Not every roadside problem requires a tow. Sometimes your vehicle simply needs a little assistance to get moving again — and if it can\'t be safely driven, we can arrange the tow on the spot.</p>',
         ['Dead batteries', 'Flat tires', 'Running out of fuel', 'Vehicle lockouts', 'Other minor roadside problems'], 'If your vehicle can safely continue after roadside help, we help you avoid an unnecessary tow.'),
        ('long-distance-towing-alberta', 'longdist', '<p>Need to move your vehicle outside Calgary? We provide secure vehicle transportation across Alberta — between Calgary and Airdrie, Chestermere, Okotoks, Cochrane, Red Deer and Edmonton, depending on your requirements.</p>',
         ['Breakdowns outside Calgary', 'Moving a vehicle between cities', 'Delivery to a dealership', 'Transport to a repair facility', 'Relocating within Alberta'], 'Our priority is safe handling and dependable transport from pickup to destination.'),
        ('battery-jump-start-calgary', 'dusk', '<p>A dead battery can leave you stranded at home, at work, in a parking lot or on the side of the road. Our team comes to your location with the right equipment and safely boosts your vehicle.</p>',
         ["Your vehicle won't start", 'You left your lights on', 'Your battery has lost power', 'The vehicle sat for a long time', 'You need a temporary boost'], 'If it starts but still has battery or mechanical problems, we can help decide whether towing is the better option.'),
        ('emergency-fuel-delivery-calgary', 'night_sedan', '<p>Running out of fuel can happen to anyone — especially in an unfamiliar area or when your fuel gauge isn\'t reading correctly. Instead of leaving your vehicle and walking to a station, call us with your location.</p>',
         ['Fuel brought to your location', 'Enough to reach the nearest station', 'Available 24/7', 'No need to leave your vehicle unattended'], 'We bring emergency fuel directly to you so you can continue to the nearest suitable gas station.'),
    ]
    figs = ''.join(f'<figure class="{"on" if i == 0 else ""}"><img src="{iu(im, "large")}" alt="{esc(ia(im))}" loading="lazy" width="768" height="1024"><figcaption><b>{i + 1:02d}</b>{SVC[i][1]}</figcaption></figure>' for i, (s, im, *_) in enumerate(det))
    dots = ''.join('<i></i>' for _ in det)
    blocks = []
    for i, (s, im, body, items, note) in enumerate(det):
        t, ic = SVC[i][1], SVC[i][2]
        blocks.append(C([IMGW(im, 'j-img'), RAW(f'<span><i class="fas fa-{ic}"></i>SERVICE {i + 1:02d}</span>', 'j-sb-n'), H(t, 'h3', 'j-h3'), T(body), ul(items), P(note, 'j-note'),
                         BTNS(BTN('Learn more', surl(s), 'j-link', 'arrow-right', True))], 'j-sb j-col'))
    scrolly = sec([head('Service details', f'Everything You Need, {hl("One Call Away")}', 'Scroll through each service to see exactly how we help — and where we can take your vehicle.'),
                   C([RAW(f'{figs}<div class="j-sticky-dots" aria-hidden="true">{dots}</div>', 'j-sticky'), C(blocks, 'j-col')], 'j-scrolly')], 'j-white')

    # ---------- why ----------
    stats = stats_html()
    wc = why_cards()
    why = sec([C([C([EB('Why Jim Towing'), H(f'Why Calgary Drivers {hl("Choose Us")}', 'h2', 'j-h2')], 'j-col'), C([P("Choosing a towing company is about more than simply finding a truck. When you're stranded, you want a company that communicates clearly and handles your vehicle responsibly.", 'j-lead')], 'j-col')], 'j-headrow j-row j-wrap rv', fd='row'),
               RAW(stats), C(wc, 'j-why')], 'j-dark j-grain')

    # ---------- situations ----------
    sit = sec([head('What happened?', f'The Right Help for Every {hl("Roadside Situation")}', "Whether your car stopped working, you've been in an accident or simply ran out of fuel — pick your situation and we'll point you to the right service.", True),
               RAW(situations_html(), 'rv')], 'j-paper')

    # ---------- areas ----------
    area = sec([C([
        C([EB('Service area'), H(f'Serving Calgary &amp; {hl("Surrounding Areas")}', 'h2', 'j-h2'),
           P('Jim Towing provides towing and roadside assistance across Calgary, Alberta, with service extending to surrounding communities and Alberta destinations depending on the type of service required.'),
           P('<strong>Long-distance transport destinations include:</strong>'),
           RAW('<div class="j-chips big">' + ''.join(f'<span><i class="fas fa-map-marker-alt"></i>{c}</span>' for c in ['Calgary', 'Airdrie', 'Chestermere', 'Okotoks', 'Cochrane', 'Red Deer', 'Edmonton']) + '</div>'),
           P('For a specific pickup and destination, contact Jim Towing to confirm service availability and pricing.', 'j-note'),
           BTNS(BTN('See all service areas', PAGES['areas'], 'j-btn-dark', 'arrow-right', True), CALL('j-btn-line'))], 'j-stack j-col rv rv-l'),
        C([RAW(route_map())], 'j-col rv rv-r'),
    ], 'j-split', fd='row')], 'j-white')

    how = steps([('Contact Jim Towing', 'Call us and tell us what happened, your current location and the type of assistance you need.'),
                 ('We Identify the Right Service', 'Emergency towing, flatbed, roadside assistance, a jump-start, fuel delivery or long-distance transport — we match the help to your situation.'),
                 ('Professional Assistance', 'Our team is dispatched to your location with the appropriate equipment for the job.'),
                 ('Safe Transport or Roadside Fix', 'We tow your vehicle to the requested destination — or, if roadside help solves it, get you moving again.')],
                lead='Four simple steps from your call to safe transport — scroll to follow the truck.')

    faqs = [('What towing services does Jim Towing provide in Calgary?', 'Jim Towing provides 24/7 emergency towing, professional flatbed towing, roadside assistance, long-distance vehicle transport, battery jump-start service and emergency fuel delivery.'),
            ('Is Jim Towing available 24/7?', 'Yes. Jim Towing provides towing and roadside assistance 24 hours a day, 7 days a week, including nights, weekends and holidays.'),
            ('How much does towing cost in Calgary?', 'The cost depends on the vehicle, pickup location, destination, distance and type of service required. Jim Towing currently advertises towing starting from $75, while the final price depends on the specific job.'),
            ('Does Jim Towing offer flatbed towing?', 'Yes. Jim Towing provides professional flatbed towing for vehicles including luxury cars, AWD vehicles, SUVs, motorcycles, lowered vehicles and accident-damaged vehicles.'),
            ('Can Jim Towing help with a dead battery?', 'Yes. Jim Towing provides a battery jump-start service in Calgary for vehicles with dead or weak batteries.'),
            ('What if I run out of gas?', 'Jim Towing provides emergency fuel delivery and can bring fuel to your location so you can continue your journey.'),
            ('Does Jim Towing provide long-distance towing?', 'Yes. Jim Towing provides long-distance vehicle transport across Alberta, including routes involving Calgary, Airdrie, Chestermere, Okotoks, Cochrane, Red Deer and Edmonton.'),
            ('Does roadside assistance always require towing?', 'No. Some roadside problems, such as a dead battery or lack of fuel, may be resolved at your current location. If the vehicle cannot be safely driven, towing may be required.'),
            ('How do I request towing in Calgary?', f'Call Jim Towing at <a href="{TEL}">{PHONE}</a>, provide your location and explain the problem with your vehicle. The team can help determine the appropriate towing or roadside assistance service.')]

    body = [hero, marquee(), intro, services, scrolly, why, sit, area, how, gallery(cls='j-paper', title='On The Job ' + hl('Across Calgary')), reviews('j-white'), faq_section(faqs, title='Towing in Calgary: ' + hl('Your Questions'), cls='j-paper'), cta()]
    return wrap(body)

def route_map():
    cities = [('Edmonton', 250, 46, '≈ 300 km north'), ('Red Deer', 262, 186, '≈ 150 km north'), ('Airdrie', 272, 318, 'North of Calgary'),
              ('Cochrane', 150, 360, 'West of Calgary'), ('Chestermere', 372, 398, 'East of Calgary'), ('Okotoks', 250, 492, 'South of Calgary')]
    hub = (265, 410)
    grid = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="540"/>' for x in range(0, 501, 50)) + ''.join(f'<line x1="0" y1="{y}" x2="500" y2="{y}"/>' for y in range(0, 541, 50))
    routes = ''
    for i, (n, x, y, k) in enumerate(cities):
        cx, cy = (hub[0] + x) / 2 + (30 if x >= hub[0] else -30), (hub[1] + y) / 2
        routes += f'<path class="route r{i + 1}" d="M{hub[0]},{hub[1]} Q{cx},{cy} {x},{y}"/>'
    pts = ''
    for n, x, y, k in cities:
        anchor, dx = ('end', -16) if x < 200 else ('start', 16)
        pts += f'<g class="city"><circle class="p" cx="{x}" cy="{y}" r="7"/><circle class="c" cx="{x}" cy="{y}" r="6"/><text x="{x + dx}" y="{y - 2}" text-anchor="{anchor}">{n}</text><text class="k" x="{x + dx}" y="{y + 15}" text-anchor="{anchor}">{k}</text></g>'
    pts += f'<g class="city hub"><circle class="p" cx="{hub[0]}" cy="{hub[1]}" r="10"/><circle class="c" cx="{hub[0]}" cy="{hub[1]}" r="10"/><text x="{hub[0] - 20}" y="{hub[1] + 6}" text-anchor="end">Calgary</text><text class="k" x="{hub[0] - 20}" y="{hub[1] + 23}" text-anchor="end">Home base · 24/7 dispatch</text></g>'
    hwy = '<path class="hwy" d="M250,30 C256,120 262,160 262,186 S270,300 268,340 S262,440 250,520"/><text x="226" y="262" style="font:600 11px Manrope;fill:#596070" transform="rotate(-88 226 262)">HWY 2</text>'
    return f'<div class="j-map" role="img" aria-label="Map of Jim Towing routes from Calgary to Airdrie, Cochrane, Chestermere, Okotoks, Red Deer and Edmonton"><svg viewBox="0 0 500 540"><g class="grid">{grid}</g>{hwy}{routes}{pts}</svg></div>'


def svc_cards():
    cards = []
    spans = ['big', 'big', '', '', '', 'big']
    for i, (s, t, ic, im, d) in enumerate(SVC):
        cards.append(C([
            W('image', 'j-sc-bg', image={'url': iu(im, 'full'), 'id': IMG[im]}, image_size='large'),
            RAW(f'<span><i class="fas fa-{ic}"></i>{i + 1:02d}</span>', 'j-sc-num'),
            C([H(t, 'h3', 'j-h3'), P(d, 'j-sc-t'), RAW(f'<a class="j-sc-go" href="{surl(s)}">Learn more <i class="fas fa-arrow-right" aria-hidden="true"></i></a>')], 'j-sc-body j-col'),
        ], f'j-sc j-col {spans[i]} rv rv-d{i % 3}', tag='article'))
    cards.append(C([RAW('<span><i class="fas fa-question"></i>Not sure?</span>', 'j-sc-num'),
                    C([H('Not Sure What You Need?', 'h3', 'j-h3'), P("Tell us what happened and where you are. We'll recommend the right service — towing, flatbed or a roadside fix — and confirm the price before dispatch."), BTNS(BTN(f'Call {PHONE}', TEL, 'j-btn-dark'))], 'j-sc-body j-col')],
                   'j-sc j-sc-cta j-col big rv rv-d1'))
    return cards

def stats_html():
    return (f'<div class="j-stats rv"><div class="j-stat"><b><span data-count="{RATING}">{RATING}</span><em>★</em></b><span>Google rating</span></div>'
             f'<div class="j-stat"><b><span data-count="{REVIEWS}">{REVIEWS}</span><em>+</em></b><span>Google reviews</span></div>'
             '<div class="j-stat"><b><span data-count="24">24</span><em>/7</em></b><span>Dispatch &amp; support</span></div>'
             '<div class="j-stat"><b><em>$</em><span data-count="75">75</span></b><span>Towing starts from</span></div></div>')

def why_cards():
    why_items = [('clock', '24/7 Availability', 'Vehicle emergencies happen at any time. Jim Towing provides towing and roadside assistance 24 hours a day, 7 days a week.'),
                 ('shield-alt', 'Professional Vehicle Handling', 'Appropriate towing equipment and safe loading procedures help reduce the risk of damage during transport.'),
                 ('map-marker-alt', 'Local Calgary Service', 'A local towing team serving Calgary drivers and surrounding Alberta communities when they need assistance.'),
                 ('th-large', 'Multiple Services', 'Emergency towing, flatbed, roadside assistance, jump-starts, long-distance transport and fuel delivery — one provider.'),
                 ('comments', 'Clear Communication', 'Clear information about the service required, vehicle transportation and expected costs before we proceed.')]
    wc = [C([RAW(f'<span><i class="fas fa-{i}"></i></span>', 'j-ico'), H(t, 'h3', 'j-h3'), P(d)], f'j-wc j-col rv rv-d{k % 3}') for k, (i, t, d) in enumerate(why_items)]
    wc.append(C([IMGW('heavy_night', 'j-img')], 'j-wc j-wc-photo j-col rv rv-d2'))
    return wc

def situations_html():
    sits = [('car-crash', 'Car Breakdown', 'redsuv', "If your vehicle won't start or cannot be safely driven, emergency towing may be the best solution.", 'emergency-towing-calgary', 'Emergency Towing'),
            ('exclamation-triangle', 'Vehicle Accident', 'shop', 'After an accident, a damaged vehicle may not be safe to drive. We transport it to a repair facility, dealership or another suitable location.', 'flatbed-towing-calgary', 'Flatbed Towing'),
            ('car-battery', 'Dead Battery', 'dusk', 'If your battery is dead but the vehicle is otherwise operational, a battery jump-start may get you back on the road.', 'battery-jump-start-calgary', 'Battery Jump-Start'),
            ('gas-pump', 'Empty Fuel Tank', 'night_sedan', "If you've run out of fuel, emergency fuel delivery helps you refuel without leaving your vehicle unattended.", 'emergency-fuel-delivery-calgary', 'Fuel Delivery'),
            ('route', 'Long-Distance Move', 'longdist', 'If your vehicle needs to travel outside Calgary, long-distance vehicle transport is the practical solution.', 'long-distance-towing-alberta', 'Long-Distance Transport')]
    tabs = ''.join(f'<button class="j-sit-tab" role="tab" id="jst{i}" aria-controls="jsp{i}" aria-selected="{"true" if i == 0 else "false"}"><i class="fas fa-{ic}" aria-hidden="true"></i>{t}</button>' for i, (ic, t, *_) in enumerate(sits))
    pans = ''.join(f'<div class="j-sit-panel{" on" if i == 0 else ""}" role="tabpanel" id="jsp{i}" aria-labelledby="jst{i}"><img src="{iu(im, "large")}" alt="{esc(ia(im))}" loading="lazy" width="768" height="1024"><div><small>Recommended: {svn}</small><h3>{t}</h3><p>{d}</p><a href="{surl(s)}">Learn about {svn} <i class="fas fa-arrow-right"></i></a></div></div>' for i, (ic, t, im, d, s, svn) in enumerate(sits))
    return f'<div class="j-sit"><div class="j-sit-tabs" role="tablist" aria-label="Roadside situations">{tabs}</div><div class="j-sit-panels">{pans}</div></div>'
