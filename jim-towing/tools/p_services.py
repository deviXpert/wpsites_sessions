from lib import *
from p_home import route_map

def fc(icon, title, text, n=None, cls=''):
    return C([RAW(f'<span><i class="fas fa-{icon}"></i></span>', 'j-ico'), RAW(f'<span>{n}</span>', 'j-fc-n') if n else None, H(title, 'h3', 'j-h3'), T(text if text.startswith('<') else f'<p>{text}</p>')], f'j-fc j-col rv {cls}')
def ib(title, html, variant='', icon=None):
    return C([RAW(f'<span><i class="fas fa-{icon}"></i></span>', 'j-ico') if icon else None, H(title, 'h3', 'j-h3'), T(html)], f'j-ib j-col rv {variant}')
def info(*blocks): return C(list(blocks), 'j-info')
def split(media_key, els, rev=False, cls='j-white', second=None):
    media = C([IMGW(media_key, 'j-m1'), IMGW(second, 'j-m2')], 'j-media rv rv-l') if second else C([IMGW(media_key, 'j-img j-img-tall')], 'j-col rv ' + ('rv-r' if rev else 'rv-l'))
    return sec([C([media, C(els, 'j-stack j-col rv')], 'j-split' + (' j-split-rev' if rev else ''), fd='row')], cls)
def quick(text):
    import re as _re
    m = _re.search(r'\$\d+', text)
    pts = [('clock', 'Available 24/7'), ('tag', f'From {m.group(0)}' if m else 'Free quote'), ('map-marker-alt', 'Calgary &amp; area'), ('shield-alt', 'Price confirmed before dispatch')]
    side = RAW(f'<div class="j-qa-side"><div><span class="ic"><i class="fas fa-bolt"></i></span></div><div><b>Quick answer</b><span>The short version — everything you need to know in 20 seconds.</span></div>'
               f'<a href="{TEL}"><i class="fas fa-phone-alt"></i>{PHONE}</a></div>')
    main = C([EB('In short'), T(f'<p>{text}</p>'), RAW('<div class="j-qa-pts">' + ''.join(f'<span><i class="fas fa-{i}"></i>{t}</span>' for i, t in pts) + '</div>')], 'j-qa-main j-col')
    return sec([C([side, main], 'j-qa2 rv')], 'j-paper j-sec-tight')
def chips(items, icon='map-marker-alt', big=False): return RAW(f'<div class="j-chips{" big" if big else ""}">' + ''.join(f'<span><i class="fas fa-{icon}"></i>{c}</span>' for c in items) + '</div>')
def facts(rows): return rows
def phone_link(): return f'<a href="{TEL}">{PHONE}</a>'
def link(slug, text): return f'<a href="{surl(slug)}">{text}</a>'
CR = ('Services', PAGES['services'])

NEIGH = ['Downtown', 'Beltline', 'Mission', 'Kensington', 'Marlborough', 'Falconridge', 'Saddle Ridge', 'Taradale', 'Brentwood', 'Dalhousie', 'Crowfoot', 'Tuscany', 'Seton', 'Mahogany', 'Auburn Bay', 'Douglasdale', 'Signal Hill', 'Aspen Woods', 'Glenmore', 'Evergreen']

def emergency():
    s = 'emergency-towing-calgary'; seed(s)
    hero = page_hero([CR, ('24/7 Emergency Towing', '')], f'24/7 Emergency Towing in {hl("Calgary")}',
        'Breakdowns, accidents and vehicles that are unsafe to drive — <strong>towed safely to your home, mechanic, body shop or dealership</strong>, any hour of the day.',
        [('Service', 'Emergency towing — cars, SUVs, motorcycles, light-duty trucks'), ('Hours', '24 hours a day, 7 days a week'), ('Area', 'All of Calgary + Airdrie, Chestermere, Okotoks, Cochrane'),
         ('Starting price', 'From $75 — final price depends on distance, vehicle, time and location'), ('Phone', phone_link())], 'redsuv')
    when = split('winter', [EB('When to call'), H(f'When Do You Need {hl("Emergency Towing?")}', 'h2'),
        P('You need an emergency tow when your vehicle cannot be driven safely or legally. Common situations in Calgary include:'),
        ul(['Engine or transmission failure on Deerfoot Trail, Stoney Trail or Glenmore Trail', 'A collision where the vehicle is not drivable', 'Overheating, fluid leaks or warning lights that tell you to stop driving',
            'A vehicle stuck in snow, ice or a ditch during winter', 'A dead battery that a jump-start cannot fix'], 'j-checks one'),
        BTNS(CALL())], second='suv_op')
    how = steps([('Call ' + PHONE, 'Tell us your location, vehicle type and what happened.'), ('Get a Quote &amp; ETA', 'We confirm the price range and an arrival estimate before dispatch.'),
                 ('We Dispatch a Truck', 'You get direct communication from our team until we arrive.'), ('Safe Loading &amp; Transport', 'Your vehicle goes to your home, mechanic, body shop or dealership.')],
                title=f'How Emergency Towing {hl("Works")}', eyebrow='Step by step', lead='From your call to safe delivery — clear, simple and fully communicated.')
    blocks = sec([head('Good to know', f'While You Wait &amp; {hl("What It Costs")}'), info(
        ib('What should I do while waiting for a tow truck?', '<p>Move to a safe place if you can, turn on your hazard lights, stay out of the vehicle if you are on a busy road or highway shoulder, and keep your phone on so the driver can reach you.</p><p><strong>If anyone is injured or there is a fire risk, call 911 first.</strong></p>', 'dark', 'shield-alt'),
        ib('How much does emergency towing cost in Calgary?', f'<p>Jim Towing\'s rates <strong>start at $75</strong>. The final price depends on the distance, your vehicle type, the time of day and your location.</p><p>We give you a quote before we dispatch — with no hidden fees. <a href="{PAGES["pricing"]}">See pricing</a>.</p>', 'red', 'tag'))], 'j-paper')
    areas = sec([C([C([EB('Coverage'), H(f'Calgary Neighbourhoods {hl("We Cover")}', 'h2'), P(f'Emergency towing across every quadrant of Calgary — and nearby Airdrie, Chestermere, Okotoks and Cochrane. <a href="{PAGES["areas"]}">View all service areas</a>.')], 'j-col'),
                     C([chips(NEIGH + ['and more'])], 'j-col')], 'j-split', fd='row')], 'j-white j-sec-tight')
    faqs = [('Is Jim Towing available 24/7 in Calgary?', 'Yes. We take emergency calls 24 hours a day, 7 days a week, including holidays.'),
            ('How fast can a tow truck arrive?', 'Arrival time depends on your location and traffic. We confirm an estimated arrival time when you call.'),
            ('Can you tow after a car accident?', 'Yes. We tow accident-damaged vehicles to a body shop, repair shop or your home. If there are injuries, call 911 first.'),
            ('Where will you take my vehicle?', 'Anywhere you choose: your home, a mechanic, a dealership or a repair shop.'),
            ('Do you tow SUVs and motorcycles?', f'Yes. We tow cars, SUVs, motorcycles and light-duty trucks. {link("flatbed-towing-calgary", "Flatbed towing")} is available for AWD and low-clearance vehicles.'),
            ('What information do you need when I call?', 'Your location, vehicle make/model, the problem, and where you want it towed.')]
    body = [hero, quick('Jim Towing Ltd. provides 24/7 emergency towing across Calgary, Alberta for breakdowns, accidents and vehicles that are unsafe to drive. Rates start at <strong>$75</strong>, and you can call <a href="' + TEL + '">' + PHONE + '</a> any time — including nights, weekends and holidays — to get a dispatch and a quote.'),
            when, how, blocks, areas, faq_section(faqs, cls='j-paper'), related(['flatbed-towing-calgary', 'roadside-assistance-calgary', 'pricing', 'areas']),
            cta(f'Stranded {hl("Right Now?")}', f'Call {PHONE} for immediate dispatch. We confirm your price before we roll — no hidden fees, no surprises.')]
    return s, '24/7 Emergency Towing in Calgary', wrap(body), ('24/7 Emergency Towing in Calgary | From $75 | Jim Towing', 'Need an emergency tow in Calgary? Jim Towing offers 24/7 towing for breakdowns and accidents with clear pricing from $75. Call 587-914-0130.')

def flatbed():
    s = 'flatbed-towing-calgary'; seed(s)
    hero = page_hero([CR, ('Flatbed Towing', '')], f'Professional Flatbed Towing in {hl("Calgary")}',
        'All four wheels off the road. <strong>Damage-conscious transport</strong> for AWD vehicles, luxury and lowered cars, motorcycles and accident-damaged vehicles — 24/7.',
        [('Service', 'Flatbed (platform) towing'), ('Best for', 'AWD/4WD, luxury, lowered cars, motorcycles, accident-damaged vehicles'), ('Hours', '24/7'), ('Starting price', 'From $89'), ('Phone', phone_link())], 'luxury')
    what = split('moto_night', [EB('The basics'), H(f'What Is {hl("Flatbed Towing?")}', 'h2'),
        P('Flatbed towing uses a truck with a flat, tilting platform. The vehicle is winched onto the bed and secured with straps, so <strong>no wheels roll on the road during transport</strong>. This is why it is the safest towing method for many vehicles.'),
        P("If you're unsure which method your vehicle needs, ask us — we'll recommend the right one.", 'j-note'), BTNS(CALL())])
    vs = sec([head('Compare', f'Flatbed vs. Hook-and-Chain (Wheel-Lift): {hl("Which Is Better?")}', center=True),
              RAW('<div class="j-vs rv"><div><span class="tag">Recommended</span><h3>Flatbed towing</h3><p>The better choice for most vehicles that need extra protection.</p><ul>'
                  + ''.join(f'<li><i class="fas fa-check"></i>{x}</li>' for x in ['AWD and 4WD vehicles', 'Low-clearance and luxury vehicles', 'Motorcycles', 'Vehicles with damaged wheels, axles or transmissions', 'Less wear on tires, transmission and drivetrain'])
                  + '</ul></div><div><span class="tag">Situational</span><h3>Wheel-lift towing</h3><p>Can be fine in limited cases.</p><ul>'
                  + ''.join(f'<li><i class="fas fa-minus"></i>{x}</li>' for x in ['Some front-wheel-drive vehicles', 'Short distances only', 'Puts wear on the lifted wheels', 'Not ideal for damaged or low vehicles'])
                  + '</ul></div></div>')], 'j-paper')
    need = sec([head('Who needs it', f'Which Vehicles {hl("Need a Flatbed Tow?")}'), C([
        fc('cogs', 'AWD / 4WD Vehicles', 'Towing with drive wheels on the ground can damage the drivetrain.', '01'),
        fc('gem', 'Luxury &amp; Lowered Cars', 'Low front bumpers and splitters need a low-angle bed.', '02', 'rv-d1'),
        fc('motorcycle', 'Motorcycles', 'Secured upright with proper tie-downs.', '03', 'rv-d2'),
        fc('car-crash', 'Accident-Damaged Vehicles', 'No further stress on damaged parts.', '04'),
        fc('ban', 'Non-Running or Non-Rolling', 'Loaded safely onto the bed by winch.', '05', 'rv-d1'),
        C([H('Not sure?', 'h3', 'j-h3'), P('Tell us your vehicle and situation — we\'ll recommend the right method before we dispatch.'), BTNS(BTN(f'Call {PHONE}', TEL, 'j-btn-dark j-btn-sm'))], 'j-ib red j-col rv rv-d2')], 'j-fgrid j-cols3')], 'j-white')
    protect = split('lift', [EB('Our process'), H(f'How We {hl("Protect Your Vehicle")}', 'h2'),
        ul(['Professional flatbed equipment and winching', 'Wheel straps and safe tie-down methods', 'Careful loading angle for low vehicles', 'Inspection of loading points before we move your car'], 'j-checks one'),
        ib('How much does flatbed towing cost in Calgary?', f'<p>Flatbed towing <strong>starts at $89</strong>. Pricing depends on distance, vehicle type, time of day and location. Call {phone_link()} for a quote before dispatch.</p>', 'dark', 'tag')], rev=True, cls='j-paper')
    faqs = [('Is flatbed towing safer for my car?', 'For most vehicles, yes. All four wheels stay off the road, so there is less wear on tires, transmission and drivetrain.'),
            ('Can you flatbed tow a motorcycle?', 'Yes. We secure motorcycles with proper tie-downs for safe transport.'),
            ('Should I use a flatbed for an AWD vehicle?', 'Yes. AWD and 4WD vehicles are best moved on a flatbed to avoid drivetrain damage.'),
            ("Can you tow a car that won't start or roll?", 'Yes. We winch non-running vehicles onto the flatbed.'),
            ('Do you offer flatbed towing at night?', 'Yes — 24/7, including weekends and holidays.'),
            ('Can you move my vehicle to a dealership or body shop?', 'Yes, to any destination you choose.')]
    body = [hero, quick(f'Flatbed towing carries your whole vehicle on a flat platform with all four wheels off the road. Jim Towing Ltd. offers 24/7 flatbed towing in Calgary for AWD vehicles, luxury and lowered cars, motorcycles and accident-damaged vehicles. Rates start at <strong>$89</strong>. Call <a href="{TEL}">{PHONE}</a>.'),
            what, vs, need, protect, gallery(['luxury', 'moto_night', 'moto', 'dealer', 'construction', 'lift', 'equip', 'downtown'], 'j-dark j-grain', 'Flatbed Jobs ' + hl('We\'ve Handled')),
            faq_section(faqs, cls='j-white'), related(['emergency-towing-calgary', 'long-distance-towing-alberta', 'pricing']),
            cta(f'Protect {hl("Your Vehicle.")}', f'Call {PHONE} for flatbed towing in Calgary — careful loading, secure tie-downs and clear pricing before dispatch.')]
    return s, 'Professional Flatbed Towing in Calgary', wrap(body), ('Flatbed Towing Calgary | AWD, Luxury & Motorcycle | Jim Towing', 'Safe flatbed towing in Calgary for AWD, luxury, lowered cars and motorcycles. Damage-free transport, 24/7. Rates from $89. Call 587-914-0130.')

def roadside():
    s = 'roadside-assistance-calgary'; seed(s)
    hero = page_hero([CR, ('Roadside Assistance', '')], f'24/7 Roadside Assistance in {hl("Calgary")}',
        'Jump-starts, flat tire changes, emergency fuel delivery and lockout help. <strong>Many problems are fixed on the spot — no tow needed.</strong>',
        [('Services', 'Jump-start, flat tire change, fuel delivery, lockout'), ('Hours', '24/7, all holidays'), ('Area', 'Calgary + nearby communities'), ('Starting price', 'From $69'), ('Phone', phone_link())], 'suv_op')
    inc = sec([head("What's included", f'What Does Roadside Assistance {hl("Include?")}'), C([
        fc('car-battery', 'Battery Boost / Jump-Start', f'<p>Safe jump-start for dead batteries. {link("battery-jump-start-calgary", "More on jump-starts")}.</p>', '01'),
        fc('life-ring', 'Flat Tire Change', '<p>We install your spare so you can drive to a tire shop.</p>', '02', 'rv-d1'),
        fc('gas-pump', 'Emergency Fuel Delivery', f'<p>Fuel brought to your location. {link("emergency-fuel-delivery-calgary", "More on fuel delivery")}.</p>', '03', 'rv-d2'),
        fc('key', 'Vehicle Lockout', '<p>Help regaining access to a locked vehicle safely.</p>', '04', 'rv-d3')], 'j-fgrid j-cols4')], 'j-white')
    tow = split('dealer', [EB('Honest advice'), H(f'When Is a Tow Better Than {hl("Roadside Help?")}', 'h2'),
        P('If the engine will not run after a jump, there is a fluid leak, you have a damaged wheel or axle, or the car was in a collision, <strong>towing is the safer option</strong>.'),
        P('Our team will tell you honestly whether roadside help will work or you need a tow.', 'j-note'),
        BTNS(BTN('Emergency towing', surl('emergency-towing-calgary'), 'j-btn-dark', 'arrow-right', True), CALL('j-btn-line'))], rev=True, cls='j-paper')
    tips = sec([head('Local know-how', f'Calgary-Specific {hl("Roadside Tips")}', center=True), C([
        fc('snowflake', 'Winter Batteries', 'Winter cold can drain a battery overnight. Test your battery before November.', None),
        fc('tools', 'Spare-Tire Ready', 'Keep a spare tire in good condition and know where your jack and wheel lock key are.', None, 'rv-d1'),
        fc('exclamation-triangle', 'Stay Safe While Waiting', 'Do not leave your vehicle running in a closed garage while you wait for help.', None, 'rv-d2')], 'j-fgrid j-cols3')], 'j-dark j-grain')
    get = sec([info(
        ib('How do I get roadside assistance in Calgary?', f'<p>Call {phone_link()}, give your location and the problem, and we dispatch a technician. You\'ll get a quote and an arrival estimate.</p>', '', 'phone-alt'),
        ib('How much does roadside assistance cost?', '<p>Our roadside rates <strong>start at $69</strong>. The final price depends on the service, location and time. We confirm before dispatch.</p>', 'red', 'tag'))], 'j-white j-sec-tight')
    faqs = [('Do you offer roadside assistance at night?', 'Yes. We are available 24/7, including weekends and holidays.'),
            ("What if the jump-start doesn't work?", 'We can tow your vehicle to your home or a repair shop.'),
            ("Can you change a flat tire if I don't have a spare?", 'We can tow you to a tire shop instead.'),
            ('Can you unlock my car?', 'Yes, we help with lockouts using safe methods.'),
            ('Do I need a membership?', 'No. You can call us any time — no membership required.'),
            ('Which areas do you cover?', f'All Calgary neighbourhoods plus nearby communities such as Airdrie, Chestermere, Okotoks and Cochrane. <a href="{PAGES["areas"]}">See service areas</a>.')]
    body = [hero, quick(f'Jim Towing Ltd. provides 24/7 roadside assistance in Calgary, including battery jump-starts, flat tire changes, emergency fuel delivery and vehicle lockout help. Many problems can be fixed on the spot without a tow. Call <a href="{TEL}">{PHONE}</a> for fast dispatch.'),
            inc, tow, tips, get, faq_section(faqs, cls='j-paper'), related(['battery-jump-start-calgary', 'emergency-fuel-delivery-calgary', 'emergency-towing-calgary']),
            cta(f'Need Roadside Help {hl("Now?")}', f'Call {PHONE} — jump-starts, tire changes, fuel and lockouts across Calgary, 24/7. No membership required.')]
    return s, '24/7 Roadside Assistance in Calgary', wrap(body), ('Roadside Assistance Calgary | 24/7 Help | Jim Towing', '24/7 roadside assistance in Calgary: jump-starts, flat tire change, fuel delivery and lockouts. Fast dispatch, clear pricing. Call 587-914-0130.')

def longdist():
    s = 'long-distance-towing-alberta'; seed(s)
    hero = page_hero([CR, ('Long-Distance Transport', '')], f'Long-Distance Vehicle Transport &amp; Towing {hl("Across Alberta")}',
        'From Calgary to Airdrie, Chestermere, Okotoks, Cochrane, Red Deer, Edmonton and beyond — <strong>secure transport with flatbed available</strong>.',
        [('Service', 'Long-distance towing / vehicle transport'), ('Popular routes', 'Calgary to Airdrie, Red Deer, Edmonton, Okotoks, Cochrane, Chestermere'), ('Method', 'Flatbed available'), ('Price', 'Quote based on distance and vehicle'), ('Phone', phone_link())], 'longdist')
    when = split('heavy_night', [EB('Common reasons'), H(f'When Do People Need {hl("Long-Distance Towing?")}', 'h2'),
        ul(['Moving a vehicle after relocating within Alberta', 'Taking a non-running vehicle to a specialist shop or dealership', 'Transporting a vehicle after an accident to a preferred body shop',
            'Moving a purchased or sold vehicle (private sale, auction)', 'A breakdown far from Calgary that needs a ride home'], 'j-checks one'), BTNS(CALL())])
    routes = [('Calgary → Airdrie / Chestermere / Cochrane / Okotoks', 'Short regional runs.'), ('Calgary → Red Deer', 'About 150 km along Highway 2.'),
              ('Calgary → Edmonton', 'About 300 km along Highway 2.'), ('Other Alberta destinations', 'On request — ask us about your destination.')]
    rl = ''.join(f'<div class="j-route-i"><i class="fas fa-route"></i><div><b>{a}</b><span>{b}</span></div></div>' for a, b in routes)
    pop = sec([C([C([EB('Popular routes'), H(f'Where We {hl("Transport Vehicles")}', 'h2'), RAW(f'<div class="j-routes">{rl}</div>'),
                     P(f'Most popular routes run along Highway 2 — but we cover communities across Alberta. <a href="{PAGES["areas"]}">See service areas</a>.')], 'j-stack j-col rv rv-l'),
                   C([RAW(route_map())], 'j-col rv rv-r')], 'j-split', fd='row')], 'j-paper')
    quote = sec([info(
        ib('How is long-distance towing priced?', f'<p>Price depends on the distance, vehicle type, pickup and drop-off locations, and time. Short local towing starts at <strong>$75</strong>. For long distance, call {phone_link()} and we\'ll give a clear quote before we move your vehicle.</p>', 'dark', 'tag'),
        ib('How to get a quote fast', '<p>Have these ready when you call:</p>' + '<ul class="j-mini">' + ''.join(f'<li>{x}</li>' for x in ['Pickup address', 'Destination', 'Vehicle make, model and year', 'Whether it runs', 'Your preferred timing']) + '</ul>', '', 'clipboard-list'))], 'j-white')
    faqs = [('Can you tow my car from Calgary to Edmonton?', 'Yes. We provide long-distance towing between Calgary and Edmonton. Call for a quote.'),
            ('Do you offer flatbed for long distances?', f'Yes — {link("flatbed-towing-calgary", "flatbed transport")} is recommended for AWD, luxury and non-running vehicles.'),
            ('How long does the trip take?', 'It depends on distance, weather and traffic. We give an estimate when you book.'),
            ('Can you tow a non-running vehicle?', 'Yes, we load it on a flatbed.'),
            ('Do you tow to places other than Alberta cities?', 'We cover communities across Alberta. Call us to confirm your route.'),
            ('Can I schedule a transport in advance?', f'Yes. Call {PHONE} to plan a pickup time.')]
    body = [hero, quick(f'Jim Towing Ltd. provides long-distance towing and vehicle transport from Calgary to cities across Alberta, including Airdrie, Chestermere, Okotoks, Cochrane, Red Deer and Edmonton. Pricing depends on distance and vehicle type. Call <a href="{TEL}">{PHONE}</a> for a quote.'),
            when, pop, quote, faq_section(faqs, cls='j-paper'), related(['flatbed-towing-calgary', 'areas', 'pricing']),
            cta(f'Moving a Vehicle {hl("Across Alberta?")}', f'Call {PHONE} for a long-distance towing quote — clear pricing before we move your vehicle.')]
    return s, 'Long-Distance Vehicle Transport & Towing Across Alberta', wrap(body), ('Long-Distance Towing from Calgary | Edmonton, Red Deer | Jim Towing', 'Secure long-distance towing from Calgary to Airdrie, Red Deer, Edmonton and across Alberta. Affordable, safe vehicle transport. Call 587-914-0130.')

def jump():
    s = 'battery-jump-start-calgary'; seed(s)
    hero = page_hero([CR, ('Battery Jump-Start', '')], f'Battery Jump-Start Service in {hl("Calgary")}',
        'Dead battery at home, at work, in a parking lot or at the roadside? <strong>We come to you 24/7</strong> with professional boost equipment.',
        [('Service', 'Mobile battery jump-start'), ('Hours', '24/7'), ('Where', 'Home, work, parking lots, roadside in Calgary'), ('Starting price', 'From $69'), ('Phone', phone_link())], 'dusk')
    signs = sec([head('Warning signs', f'How Do I Know My {hl("Battery Is Dead?")}'), C([
        fc('volume-up', 'Clicking, No Crank', 'The engine clicks but does not turn over.', '01'),
        fc('lightbulb', 'Dim Lights', 'Headlights or interior lights are dim.', '02', 'rv-d1'),
        fc('tachometer-alt', 'Flickering Dash', 'Dashboard lights flicker or stay off.', '03', 'rv-d2'),
        fc('key', 'Nothing Happens', 'Nothing happens when you turn the key or press start.', '04', 'rv-d3')], 'j-fgrid j-cols4')], 'j-white')
    how = steps([('Confirm by Phone', 'We check your location and confirm the issue by phone.'), ('Technician Arrives', 'A technician arrives with professional jump equipment.'),
                 ('Safe Connection', 'We connect it safely to avoid electrical damage.'), ('Start &amp; Advise', "We start your vehicle and advise you to drive for a while so the battery can charge. If it won't start, we offer a tow to a shop.")],
                title=f'What Happens During a {hl("Jump-Start?")}', eyebrow='The process', light=True)
    winter = split('winter', [EB('Calgary winters'), H(f'Why Do Batteries Die More in {hl("Calgary Winters?")}', 'h2'),
        P('Cold weather slows the chemical reaction inside a battery and makes the engine harder to turn over. Older batteries are more likely to fail in extreme cold.'),
        P('Short trips, leaving lights on and a failing alternator also drain batteries.'),
        P('Tip: have your battery tested before winter sets in.', 'j-note')], rev=True, cls='j-white')
    after = sec([info(
        ib('After the jump: what next?', '<p>Drive for at least <strong>20–30 minutes</strong> if possible, and have the battery and alternator tested soon. If it dies again, the battery or charging system likely needs replacement.</p>', 'dark', 'road'),
        ib('Can a jump-start damage my car?', '<p>Done properly, no. Modern vehicles have sensitive electronics, so professional equipment and the correct connection order matter — a good reason to call a trained technician.</p>', '', 'microchip'))], 'j-paper')
    faqs = [('How much does a jump-start cost in Calgary?', 'Our jump-start rates start at $69. We confirm your price when you call.'),
            ('How long does a jump-start take?', 'The jump itself usually takes only a few minutes once we arrive.'),
            ("What if my car still won't start?", f'It may need a new battery, starter or alternator. We can {link("emergency-towing-calgary", "tow it to your mechanic")}.'),
            ('Do you do jump-starts in underground parkades?', 'Often yes, depending on access. Tell us the location when you call.'),
            ('Is this available at night and on weekends?', 'Yes, 24/7.')]
    body = [hero, quick(f'If your car battery is dead in Calgary, Jim Towing Ltd. can come to your location 24/7 and jump-start your vehicle safely. Service rates start at <strong>$69</strong>. If the vehicle still will not start, we can tow it to a repair shop. Call <a href="{TEL}">{PHONE}</a>.'),
            signs, how, winter, after, faq_section(faqs, cls='j-white'), related(['roadside-assistance-calgary', 'emergency-towing-calgary', 'emergency-fuel-delivery-calgary']),
            cta(f'Dead {hl("Battery?")}', f'Call {PHONE} now — we come to you with professional boost equipment, day or night.')]
    return s, 'Battery Jump-Start Service in Calgary', wrap(body), ('Battery Jump-Start Calgary | Dead Battery Help 24/7 | Jim Towing', 'Dead battery in Calgary? Jim Towing offers fast, safe 24/7 jump-start service at your location. Clear pricing from $69. Call 587-914-0130.')

def fuel():
    s = 'emergency-fuel-delivery-calgary'; seed(s)
    hero = page_hero([CR, ('Emergency Fuel Delivery', '')], f'Emergency Fuel Delivery in {hl("Calgary")}',
        'Ran out of gas? We deliver emergency fuel to your location, 24/7 — <strong>enough to get you to the nearest station</strong>.',
        [('Service', 'Emergency fuel delivery'), ('Hours', '24/7'), ('Where', 'Anywhere in Calgary and nearby communities'), ('Starting price', 'From $69 (fuel extra)'), ('Phone', phone_link())], 'night_sedan')
    what = steps([('Hazards On', 'Turn on hazard lights and move to the shoulder or a safe spot if the car still rolls.'), ('Stay Clear of Traffic', 'Stand behind a barrier if possible. Do not walk along highways or Stoney Trail.'),
                  ('Call ' + PHONE, 'Give your exact location — cross streets, exit number or a landmark.'), ('We Bring Fuel', 'We bring fuel and get you moving again.')],
                 title=f'What Should I Do If I {hl("Run Out of Gas?")}', eyebrow='Stay safe', light=True)
    blocks = sec([info(
        ib('How much fuel do you deliver?', '<p>Enough to reach the nearest gas station safely — not a full tank. Fill up right after.</p>', '', 'gas-pump'),
        ib('Why is it unsafe to wait on the shoulder?', '<p>Highway shoulders are dangerous, especially at night, in snow or in low visibility. A fast fuel delivery gets you off the roadside sooner.</p>', 'dark', 'exclamation-triangle'),
        ib('How much does fuel delivery cost?', '<p>Our service rates <strong>start at $69</strong> (fuel extra). Fuel cost and distance may affect the final price. We confirm the price before dispatch.</p>', 'red wide', 'tag'))], 'j-white')
    tips = split('heavy_night', [EB('Prevention'), H(f'Tips to Avoid Running Out of Fuel {hl("in Calgary")}', 'h2'),
        ul(['Refuel at a quarter tank, especially in winter.', 'Do not rely on the "distance to empty" number in extreme cold.', 'Watch for long gaps between stations on highways outside the city.'], 'j-checks one'),
        BTNS(CALL())], cls='j-paper')
    faqs = [('How fast can fuel arrive?', 'Arrival depends on your location and traffic. We provide an estimate when you call.'),
            ('Will fuel delivery fix my car?', f'If it only ran out of fuel, yes. Sometimes a car needs to be primed or restarted a few times. If it still will not start, we can {link("emergency-towing-calgary", "tow it")}.'),
            ('Is the fuel included in the price?', 'We confirm the total, including fuel, when you call.'),
            ('Is fuel delivery available at night?', 'Yes, 24/7.'),
            ('Can you deliver fuel on the highway?', 'Yes, to safe roadside locations in Calgary and nearby areas. Call 911 if you are in immediate danger.')]
    body = [hero, quick(f'If you run out of gas in Calgary, Jim Towing Ltd. delivers emergency fuel directly to your location, 24/7. We bring enough fuel to get you to the nearest station. Call <a href="{TEL}">{PHONE}</a> for dispatch and a quote.'),
            what, blocks, tips, faq_section(faqs, cls='j-white'), related(['roadside-assistance-calgary', 'battery-jump-start-calgary', 'emergency-towing-calgary']),
            cta(f'Out of {hl("Gas?")}', f'Call {PHONE} now — fuel delivered to your location anywhere in Calgary, day or night.')]
    return s, 'Emergency Fuel Delivery in Calgary', wrap(body), ('Emergency Fuel Delivery Calgary | Out of Gas? | Jim Towing', 'Ran out of gas in Calgary? Jim Towing delivers emergency fuel to your location 24/7 so you can reach the station. Call 587-914-0130.')

def build_all():
    for f in (emergency, flatbed, roadside, longdist, jump, fuel):
        s, title, data, seo = f()
        yield s, title, data, seo
