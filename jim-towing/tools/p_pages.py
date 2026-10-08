from lib import *
from p_home import svc_cards, stats_html, why_cards, situations_html, route_map, form_widget
from p_services import fc, ib, info, split, chips, phone_link, NEIGH

GMAP = f'<div class="j-gmap"><iframe title="Jim Towing Ltd. on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAP_EMBED}" allowfullscreen></iframe></div>'
BASE_FACTS = [('Hours', 'Open 24 hours, 7 days a week'), ('Based in', 'Calgary, Alberta'), ('Google rating', f'{RATING} ★ from {REVIEWS} reviews'), ('Starting price', 'Roadside from $69 · Towing from $75'), ('Phone', phone_link())]

def about():
    seed('about')
    hero = page_hero([('About', '')], f'About Jim Towing {hl("Ltd.")}',
        "We're a Calgary-based towing and roadside assistance team focused on <strong>fast dispatch, safe transport and clear communication</strong>. Whether it's a breakdown, accident recovery or a quick on-site fix, we treat your vehicle with care and get you to the next step with minimal stress.",
        BASE_FACTS, 'logo_truck')
    story = split('downtown', [EB('Who we are'), H(f'Fast, Reliable Towing &amp; Roadside Help — {hl("Done Right")}', 'h2'),
        P('Jim Towing Ltd. provides professional towing and roadside assistance in Calgary with quick dispatch, careful vehicle handling and clear communication from start to finish.'),
        P('Breakdowns and accidents don\'t wait for a convenient time. That\'s why we focus on responsive service and practical solutions — whether you need a tow across town or roadside assistance to get going again.'),
        P("We serve Calgary and nearby communities with a straightforward approach: answer quickly, arrive prepared and complete the job safely. If you're unsure what you need, call — our team will help you choose the right service for your situation."),
        BTNS(CALL(), BTN('Our services', PAGES['services'], 'j-btn-line', 'arrow-right', True))], second='winter')
    mission = sec([C([C([EB('Our mission'), H(f'Get You Back to Safety — {hl("With Service You Can Trust")}', 'h2'),
                         P("Our mission is simple: get you back to safety quickly with service you can trust. We show up prepared, treat your vehicle like it's our own, and keep you informed with straightforward timelines and pricing.", 'j-lead')], 'j-col'),
                       C([RAW('<blockquote class="j-quote"><p>“Our goal is to make a stressful moment easier — fast dispatch, safe transport and clear communication.”</p><cite>— Jim Towing Ltd.</cite></blockquote>')], 'j-col')], 'j-split', fd='row'),
                    C([fc('hard-hat', 'Safety', 'Safe loading, secure tie-downs and safe roadside practices on every call.', '01'),
                       fc('handshake', 'Respect', "We treat you — and your vehicle — the way we'd want to be treated.", '02', 'rv-d1'),
                       fc('stopwatch', 'Reliability', 'Quick dispatch and clear ETAs, day or night, 7 days a week.', '03', 'rv-d2'),
                       fc('user-tie', 'Professionalism', 'Prepared operators, the right equipment and honest advice.', '04', 'rv-d3')], 'j-fgrid j-cols4 j-mt')], 'j-paper')
    why = sec([C([C([EB('Why choose us'), H(f'Why Customers {hl("Choose Jim Towing")}', 'h2', 'j-h2')], 'j-col'), C([P("Choosing a towing company is about more than finding a truck. Here's what you can expect every time you call.", 'j-lead')], 'j-col')], 'j-headrow j-row j-wrap rv', fd='row'),
               RAW(stats_html()), C(why_cards(), 'j-why')], 'j-dark j-grain')
    body = [hero, story, mission, why, gallery(cls='j-white'), reviews('j-paper'),
            cta(f'Need Towing or Roadside Help {hl("Right Now?")}', f'Call {PHONE} for fast dispatch in Calgary and surrounding areas, or send a request online and we\'ll respond as quickly as possible.')]
    return 'about', 'About (redesign)', wrap(body), ('About Jim Towing Ltd. | Calgary Towing & Roadside Assistance', 'Jim Towing Ltd. is a Calgary-based towing and roadside assistance team focused on fast dispatch, safe transport and clear communication — 24/7.')

def services():
    seed('services')
    hero = page_hero([('Services', '')], f'Towing &amp; Roadside {hl("Services")}',
        'Fast dispatch, safe transport and reliable help whenever you need it. <strong>Six core services</strong> for drivers across Calgary and nearby Alberta communities.',
        [('Services', 'Emergency towing, flatbed, roadside assistance, long-distance transport, jump-starts, fuel delivery'), ('Hours', '24/7, including holidays'), ('Area', 'Calgary + surrounding communities'), ('Starting price', 'Roadside $69 · Towing $75 · Flatbed $89'), ('Phone', phone_link())], 'construction')
    grid = sec([head('All services', f'Choose the Help {hl("You Need")}', 'Every service is available 24/7 — tap a card for full details, pricing guidance and FAQs.'), C(svc_cards(), 'j-svc-grid')], 'j-paper')
    sit = sec([head('What happened?', f'Not Sure Which Service? {hl("Start Here.")}', 'Pick your situation and we\'ll point you to the right service.', True), RAW(situations_html(), 'rv')], 'j-white')
    whyl = split('dealer', [EB('Why Jim Towing'), H(f'One Call. {hl("The Right Help.")}', 'h2'),
        ul(['24/7 emergency dispatch', 'Quick dispatch across Calgary', 'Affordable rates — roadside help from $69', 'Friendly, trained towing operators', 'Damage-conscious towing methods', 'Honest pricing — no hidden charges', 'Full roadside assistance services', 'Available day, night, weekends and holidays']),
        P('When you call Jim Towing, you\'re calling a team that puts your safety and time first.', 'j-note'), BTNS(CALL())], rev=True, cls='j-paper')
    how = steps([('Contact Jim Towing', 'Call us and tell us what happened, your current location and the type of assistance you need.'),
                 ('We Identify the Right Service', 'We match the help to your situation — towing, flatbed, roadside, jump-start, fuel or long distance.'),
                 ('Professional Assistance', 'Our team is dispatched to your location with the appropriate equipment.'),
                 ('Safe Transport or Roadside Fix', 'We tow your vehicle to your destination — or get you moving again on the spot.')], lead='Four simple steps from your call to safe transport.')
    faqs = [('Is Jim Towing available 24/7?', 'Yes. Towing and roadside assistance are available 24 hours a day, 7 days a week, including nights, weekends and holidays.'),
            ('How much does towing cost in Calgary?', f'Roadside help starts from $69, local towing from $75 and flatbed towing from $89. The final price depends on the vehicle, pickup location, destination, distance and service required. <a href="{PAGES["pricing"]}">See pricing</a>.'),
            ('Does roadside assistance always require towing?', 'No. Some problems, such as a dead battery or lack of fuel, can be resolved where you are. If the vehicle cannot be safely driven, towing may be required.'),
            ('Do you offer flatbed towing?', 'Yes — for luxury cars, AWD vehicles, SUVs, motorcycles, lowered vehicles and accident-damaged vehicles.'),
            ('Do you provide long-distance towing?', 'Yes. We transport vehicles across Alberta, including Airdrie, Chestermere, Okotoks, Cochrane, Red Deer and Edmonton.')]
    body = [hero, grid, sit, whyl, how, faq_section(faqs, cls='j-white'), cta()]
    return 'services', 'Services (redesign)', wrap(body), ('Towing & Roadside Services in Calgary | Jim Towing', 'Emergency towing, flatbed towing, roadside assistance, long-distance transport, battery jump-starts and fuel delivery in Calgary — 24/7, roadside help from $69.')

def areas():
    seed('areas')
    hero = page_hero([('Service Areas', '')], f'Service Areas — Calgary &amp; {hl("Beyond")}',
        "Jim Towing Ltd. provides fast towing and roadside assistance across Calgary, Alberta and nearby communities. If you're stranded, <strong>we'll dispatch quickly and get you to a safe destination</strong>.",
        [('Calgary', 'NW, NE, SW, SE &amp; Central'), ('Nearby', 'Airdrie, Chestermere, Okotoks, Cochrane &amp; more'), ('Long distance', 'Red Deer, Edmonton &amp; across Alberta'), ('Hours', '24/7'), ('Phone', phone_link())], 'downtown')
    quads = [('Central Calgary', ['Downtown', 'Beltline', 'Mission', 'Kensington']), ('NE Calgary', ['Marlborough', 'Falconridge', 'Saddle Ridge', 'Taradale']),
             ('NW Calgary', ['Brentwood', 'Dalhousie', 'Crowfoot', 'Tuscany']), ('SE Calgary', ['Seton', 'Mahogany', 'Auburn Bay', 'Douglasdale']), ('SW Calgary', ['Signal Hill', 'Aspen Woods', 'Glenmore', 'Evergreen'])]
    qh = ''.join(f'<div class="rv"><h4>{q}</h4><div class="j-chips">' + ''.join(f'<span>{n}</span>' for n in ns) + '</div></div>' for q, ns in quads)
    qh += '<div class="rv j-quad-cta"><h4>Not listed?</h4><p>We cover all Calgary neighbourhoods. Call to confirm dispatch availability.</p><a href="' + TEL + '"><i class="fas fa-phone-alt"></i> ' + PHONE + '</a></div>'
    city = sec([C([C([EB('Calgary coverage'), H(f'Every Quadrant of {hl("Calgary")}', 'h2'), P('We cover Calgary proper and many nearby communities. Common service areas include the neighbourhoods below — and many more.', 'j-lead'), BTNS(CALL('j-btn-dark'))], 'j-stack j-col rv'),
                     C([RAW(f'<div class="j-quad">{qh}</div>')], 'j-col')], 'j-split', fd='row')], 'j-paper')
    near = sec([C([C([EB('Surrounding communities'), H(f'Nearby Communities &amp; {hl("Alberta Routes")}', 'h2'),
                      P('Surrounding areas we often dispatch to:'),
                      chips(['Airdrie', 'Chestermere', 'Cochrane', 'Okotoks', 'Strathmore', 'Rocky View County', 'Crossfield', 'High River', 'Black Diamond', 'Turner Valley'], big=True),
                      P('<strong>Long-distance transport</strong> to Red Deer, Edmonton and other Alberta destinations is available on request.'),
                      BTNS(BTN('Long-distance transport', surl('long-distance-towing-alberta'), 'j-btn-dark', 'arrow-right', True))], 'j-stack j-col rv rv-l'),
                   C([RAW(route_map())], 'j-col rv rv-r')], 'j-split', fd='row')], 'j-white')
    gm = sec([C([C([EB('Find us'), H(f'Jim Towing Ltd. on {hl("Google Maps")}', 'h2'), P(f'View our business profile for directions, details and {REVIEWS} customer reviews.'),
                    BTNS(BTN('Open in Google Maps', MAPS, 'j-btn-dark', 'external-link-alt', True))], 'j-stack j-col rv'), C([RAW(GMAP)], 'j-col rv rv-r')], 'j-split', fd='row')], 'j-paper')
    faqs = [('What areas do you serve?', 'All Calgary neighbourhoods plus nearby Alberta communities such as Airdrie, Chestermere, Okotoks and Cochrane.'),
            ('Do you tow outside Calgary?', f'Yes. We provide {"<a href=" + chr(34) + surl("long-distance-towing-alberta") + chr(34) + ">long-distance transport</a>"} across Alberta, including Red Deer and Edmonton.'),
            ("I'm not sure if I'm in range — what should I do?", f'Call {PHONE} and we\'ll confirm dispatch availability for your location.'),
            ('Are you available 24/7 in all areas?', 'Yes — we take calls 24 hours a day, 7 days a week, including holidays.')]
    body = [hero, city, near, gm, faq_section(faqs, cls='j-white'), cta(f'Need a Tow in Calgary {hl("Right Now?")}', 'Call for immediate dispatch or request service online — fast response, clear communication and safe transport.')]
    return 'service-areas', 'Service Areas (redesign)', wrap(body), ('Towing Service Areas | Calgary & Surrounding Alberta | Jim Towing', 'Jim Towing serves all of Calgary — NE, NW, SE, SW — plus Airdrie, Chestermere, Okotoks, Cochrane, Red Deer, Edmonton and more. 24/7 dispatch: 587-914-0130.')

def pricing():
    seed('pricing')
    hero = page_hero([('Pricing', '')], f'Towing &amp; Roadside {hl("Pricing")}',
        'Clear starting rates for common services in Calgary. <strong>We confirm your price before dispatch</strong> — no hidden fees, no surprises.',
        [('Roadside help', 'From $69'), ('Local towing', 'From $75'), ('Flatbed', 'From $89'), ('Long distance', 'Quote based on distance &amp; vehicle'), ('Price confirmed', 'Before dispatch'), ('Phone', phone_link())], 'logo_truck')
    def card(title, price, items, hot=False, flag=None, btn='Call for a Quote'):
        return C([RAW(f'<span>{flag}</span>', 'j-pc-flag') if flag else None, H(title, 'h3', 'j-h3'), RAW(f'<div class="j-price"><small>Starting from</small>{price}</div>' if price.startswith('$') else f'<div class="j-price"><small>Pricing</small>{price}</div>'),
                  ul(items), BTNS(BTN(btn, TEL, 'j-btn-sm ' + ('j-btn-gold' if hot else 'j-btn-dark')))], 'j-pc j-col rv' + (' hot' if hot else ''))
    cards = sec([head('Starting rates (CAD)', f'Simple, Honest {hl("Starting Rates")}', 'Typical starting prices. We confirm your exact total after a quick call.', True), C([
        card('Roadside Help', '$69<sup>*</sup>', ['Battery jump-start', 'Lockout service', 'Fuel delivery (fuel extra)', 'Flat tire change (spare required)']),
        card('Local Towing', '$75<sup>*</sup>', ['Standard tow — cars &amp; SUVs', 'Tows within Calgary', 'Accident &amp; breakdown towing', 'Safe loading &amp; transport'], True, 'Most requested'),
        card('Flatbed Towing', '$89<sup>*</sup>', ['Low-clearance &amp; luxury vehicles', 'AWD / 4x4 recommended', 'Motorcycles', 'Non-running vehicles']),
        card('Long Distance', 'Quote', ['Calgary ↔ Airdrie, Okotoks, Cochrane', 'Calgary ↔ Red Deer, Edmonton', 'Flatbed available', 'Scheduled pickups'])], 'j-prices'),
        P('* Starting rates. Final pricing may vary by distance, time of day, vehicle type/condition and access.', 'j-center j-small rv')], 'j-paper')
    factors = sec([head('What affects the price', f'What Determines {hl("Your Final Price?")}', center=True),
                   RAW('<div class="j-factors">' + ''.join(f'<div class="rv rv-d{i % 4}"><i class="fas fa-{ic}"></i>{t}</div>' for i, (ic, t) in enumerate([('road', 'Distance'), ('car-side', 'Vehicle type &amp; condition'), ('clock', 'Time of day'), ('map-marker-alt', 'Location &amp; access'), ('tools', 'Service required')])) + '</div>')], 'j-white j-sec-tight')
    quote = split('suv_op', [EB('Get a quote'), H(f'Your Price, Confirmed {hl("Before We Roll")}', 'h2'),
        P('Call us with a few details and we\'ll give you a clear price before dispatch:'),
        ul(['Your exact location', 'Vehicle make, model and condition', 'What happened', 'Where you want the vehicle taken'], 'j-checks'),
        P('No hidden fees. No surprises.', 'j-note'), BTNS(CALL(), QUOTE('j-btn-line'))], cls='j-paper')
    faqs = [('How much does towing cost in Calgary?', 'Roadside help starts from $69, local towing from $75 and flatbed towing from $89. The final price depends on the vehicle, pickup location, destination, distance and type of service required.'),
            ('Do you give a price before dispatch?', 'Yes. We confirm the price range when you call, before we dispatch a truck.'),
            ('Is fuel included in fuel delivery pricing?', 'We confirm the total, including fuel, when you call.'),
            ('How is long-distance towing priced?', 'By distance, vehicle type, pickup and drop-off locations and timing. Call for a clear quote.'),
            ('Are there hidden fees?', 'No. We aim to give you clear information about the service and expected costs before we proceed.')]
    body = [hero, cards, factors, quote, faq_section(faqs, cls='j-white'), cta(f'Need Help {hl("Right Now?")}', f'Call {PHONE} for a fast estimate and dispatch, or send a request and we\'ll get back to you ASAP.')]
    return 'pricing', 'Pricing (redesign)', wrap(body), ('Towing Prices Calgary | Roadside From $69 | Jim Towing', 'Clear towing and roadside pricing in Calgary: roadside help from $69, local towing from $75, flatbed from $89. Price confirmed before dispatch. Call 587-914-0130.')

def contact():
    seed('contact')
    hero = page_hero([('Contact', '')], f'Contact Jim Towing {hl("Ltd.")}',
        "Need towing or roadside help in Calgary? <strong>Call for the fastest dispatch</strong> — or send a request and we'll call you back as quickly as possible.",
        [('Phone', phone_link()), ('Email', f'<a href="mailto:{EMAIL}" style="font-size:15px">{EMAIL}</a>'), ('Hours', 'Open 24 hours, 7 days a week'), ('Service area', 'Calgary, Alberta &amp; surrounding areas')], 'night_sedan')
    soc = ''.join(f'<a class="j-cc" href="{u}" target="_blank" rel="noopener"><i class="fab fa-{i}"></i><small>Follow us</small><b>{n}</b></a>' for i, n, u in SOC)
    cards = sec([RAW(f'<div class="j-cgrid"><a class="j-cc rv" href="{TEL}"><i class="fas fa-phone-alt"></i><small>Call or text 24/7</small><b>{PHONE}</b><span>Fastest way to get help</span></a>'
                     f'<a class="j-cc rv rv-d1" href="mailto:{EMAIL}"><i class="fas fa-envelope"></i><small>Email</small><b>{EMAIL}</b><span>For quotes &amp; scheduled transport</span></a>'
                     f'<a class="j-cc rv rv-d2" href="{MAPS}" target="_blank" rel="noopener"><i class="fab fa-google"></i><small>Google Business Profile</small><b>{RATING} ★ · {REVIEWS} reviews</b><span>Directions, details &amp; reviews</span></a></div>')], 'j-paper j-sec-tight')
    form = sec([C([C([EB('Request service'), H(f'Send Us Your {hl("Details")}', 'h2', 'j-h2 j-cf-t'), P("Fill in the form and we'll call you back to confirm dispatch, pricing and next steps.", 'j-cf-s'), form_widget(name='Contact Page Request', btn='Send Request'),
                      P(f'Emergency? Don\'t wait for a reply — <a href="{TEL}">call {PHONE}</a>.', 'j-cf-note')], 'j-formcard j-col rv rv-l', _element_id='request'),
                   C([RAW(GMAP), RAW(f'<div class="j-cgrid j-cgrid-soc">{soc}</div>')], 'j-stack j-col rv rv-r')], 'j-split j-split-top', fd='row')], 'j-white')
    faqs = [('What information should I have ready?', 'Your exact location, vehicle make/model, and what issue you\'re experiencing (battery, lockout, tire, fuel, breakdown or accident), plus where you want the vehicle taken.'),
            ('Are you open 24/7?', 'Yes. We operate 24 hours a day, 7 days a week, including holidays.'),
            ('How quickly can you arrive?', 'Arrival time depends on traffic and your location. We confirm an estimated arrival time when you call.')]
    body = [hero, cards, form, faq_section(faqs, cls='j-paper')]
    return 'contact', 'Contact (redesign)', wrap(body), ('Contact Jim Towing | 24/7 Towing Calgary | 587-914-0130', 'Contact Jim Towing Ltd. for 24/7 towing and roadside assistance in Calgary. Call 587-914-0130, email jimtowingltd@gmail.com or request service online.')

def build_all():
    for f in (about, services, areas, pricing, contact):
        yield f()
