"""Copy for the service pages – taken from design/content-seo.md ("Service pages").  Owner-to-confirm notes from the doc
are left out of the published copy (see HANDOFF.md for the open list).
Section kinds: list (H2 + service items), signs (H2 + warning signs), steps (H2 + numbered process), text (H2 + paragraphs),
prices (H2 + native Elementor Price List), callout (highlighted H2 + text)."""

PAGES = {
    'tires': dict(
        seo_title='Tire Shop Calgary | New & Used Tires, Repair & Install | Busy Bee',
        meta='Calgary tire shop for new and used tires, flat tire repair, installation, rotation, and balancing. Winter and all-season '
             'tires for all makes. Call today.',
        focus='tire shop calgary', eyebrow='TIRE SHOP · NE CALGARY',
        h1='Tire shop in Calgary: new &amp; used tires, repair &amp; <em>installation</em>',
        intro='Need tires in Calgary? Busy Bee Auto Repair & Tire Shop sells new and used tires and handles installation, flat tire '
              'repair, rotation, and balancing in one visit. We’ll help you pick the right tire for Calgary winters and your budget.',
        offer=('circle-dashed', 'New &amp; used tires', 'Ask what we have in stock for your size'),
        cta='Check tire stock', photos=['winter-tire-change-calgary', 'busy-bee-service-bays-calgary'],
        sections=[
            ('list', 'Tire services', 'we offer', [
                ('New tires', 'All-season, winter, and all-weather tires from trusted brands.'),
                ('Used tires', 'Quality-checked used tires with plenty of tread left, a smart budget option.'),
                ('Tire installation', 'Mounting, balancing, and a new valve stem on every tire.'),
                ('Flat tire repair', 'Patch and plug repairs done to safety standards. Tire repair up to 16 inch: $84.'),
                ('Tire rotation', 'Even wear and longer tire life.'),
                ('Wheel balancing', 'Removes vibration at highway speed.'),
                ('Seasonal changeovers', 'Quick swaps between summer and winter sets.')]),
            ('text', 'Used tires in Calgary', ['Good used tires can save you hundreds. Every used tire we sell is inspected for tread '
                                              'depth, age, sidewall damage, and repairs before it goes on your car. Ask what we have '
                                              'in stock for your size.'], 'battery-alternator-service-calgary'),
            ('signs', 'Signs you need new tires', [
                'Tread at or below 4/32" (3 mm), which is too low for Calgary snow.', 'Cracks, bulges, or cuts in the sidewall.',
                'Vibration or pulling to one side.', 'Tires more than 6 years old, whatever the tread.',
                'A slow leak that keeps coming back.']),
            ('callout', 'Why Calgary drivers buy tires from us',
             'Honest advice, not upselling. Fair prices on new and used tires. Proper installation and balancing every time. And '
             'because we’re a full repair shop, we’ll spot alignment or suspension problems that are wearing your tires out early.'),
        ],
        faqs=[('When should I switch to winter tires in Calgary?', 'When temperatures stay below 7°C, usually from mid-October.'),
              ('Can a tire with a nail be repaired?', 'Usually, if the hole is in the tread and smaller than 6 mm. Sidewall damage '
                                                      'can’t be safely repaired.'),
              ('Do you sell used winter tires?', 'Yes, subject to stock. Call to check your size.')],
        cta_text='Call (403) 930-5888 to check tire stock and pricing.', related=['alignment', 'suspension', 'brakes']),

    'alignment': dict(
        seo_title='Wheel Alignment Calgary | Car & Tire Alignment | Busy Bee Auto',
        meta='Wheel alignment in NE Calgary. Fix pulling, crooked steering, and uneven tire wear. Fast car and tire alignment for all '
             'makes. Book today.',
        focus='wheel alignment calgary', eyebrow='WHEEL ALIGNMENT · NE CALGARY', h1='Wheel alignment in <em>Calgary</em>',
        intro='Calgary potholes and curbs knock wheels out of alignment fast. A proper wheel alignment stops your car pulling, '
              'straightens the steering wheel, and stops your tires wearing out early. We’ll check and adjust your alignment to '
              'manufacturer specifications.',
        offer=('gauge', 'About an hour', 'Most alignments are done while you wait'),
        cta='Book alignment', photos=['busy-bee-service-bays-calgary', 'busy-bee-repair-bay-calgary'],
        sections=[
            ('signs', 'Signs you need a wheel alignment', [
                'Your car pulls left or right on a straight road.', 'The steering wheel sits off-center when driving straight.',
                'Tires are wearing faster on one edge.', 'You hit a big pothole or curb.',
                'You just installed new tires or suspension parts.']),
            ('steps', 'What our alignment service', 'includes', [
                ('Inspect', 'Tires, steering, and suspension parts first, since worn parts stop an alignment from holding.'),
                ('Measure', 'Camber, caster, and toe.'), ('Adjust', 'To the manufacturer’s specifications.'),
                ('Test drive', 'To confirm the car tracks straight.')]),
            ('text', 'How much does a wheel alignment cost in Calgary?',
             ['Price depends on your vehicle and whether it needs a front-end or a four-wheel alignment. Call us for an exact quote.'],
             'winter-tire-change-calgary'),
        ],
        faqs=[('How often do I need an alignment?', 'About once a year, and any time you get new tires or hit a hard pothole.'),
              ('Is alignment the same as balancing?', 'No. Alignment sets the wheel angles. Balancing removes vibration by evening '
                                                      'out the weight.'),
              ('How long does it take?', 'Usually about an hour.')],
        cta_text='Book your wheel alignment: (403) 930-5888.', related=['tires', 'suspension', 'brakes']),

    'oil': dict(
        seo_title='Oil Change Calgary from $75 | Mobil 1 Synthetic | Busy Bee Auto',
        meta='Mobil 1 synthetic oil change in NE Calgary from $75, with a free multi-point inspection. Conventional and high-mileage '
             'options. Walk-ins welcome.',
        focus='oil change calgary', eyebrow='OIL CHANGE · NE CALGARY', h1='Oil change in Calgary: Mobil 1 synthetic from <em>$75</em>',
        intro='Get a full synthetic Mobil 1 oil change in NE Calgary from $75, with a free inspection included. We change the oil and '
              'filter, check your fluids, and flag anything that needs attention, so you leave knowing exactly where your car stands.',
        offer=('droplets', 'From $75', 'Mobil 1 synthetic · walk-ins welcome'),
        cta='Book an oil change', photos=['mobil-1-synthetic-oil-change-calgary', 'busy-bee-repair-bay-calgary'],
        sections=[
            ('list', 'Oil change', 'options', [
                ('Synthetic oil change (Mobil 1)', 'Best protection for modern engines and Calgary’s cold starts. From $75.'),
                ('Conventional oil change', 'A budget option for older, low-mileage vehicles.'),
                ('High-mileage oil change', 'For vehicles over 120,000 km, helping reduce leaks and oil burning.')]),
            ('signs', 'Every oil change includes', [
                'Drain and refill with the correct oil grade for your engine.', 'New oil filter.', 'Fluid top-ups and a leak check.',
                'A free multi-point inspection: brakes, tires, belts, battery, and lights.'], 'check'),
            ('prices', 'Oil change prices in Calgary', [('Mobil 1 synthetic oil change', 'From $75',
                                                         'Includes a free multi-point inspection')]),
            ('text', 'How often should you change your oil in Calgary?',
             ['Most modern cars on synthetic oil need a change every 8,000 to 12,000 km. Calgary counts as “severe” driving, with cold '
              'starts, short trips, and dust, so many vehicles do better at the shorter end. We’ll set your next reminder based on '
              'your car and driving.'], 'engine-repair-audi-calgary'),
        ],
        faqs=[('Do I need an appointment?', 'No, walk-ins are welcome.'), ('How long does it take?', 'About 30 to 45 minutes.'),
              ('Will it affect my warranty?', 'No. We use oil that meets your manufacturer’s specification and record the service '
                                              'for your warranty file.')],
        cta_text='Drop in or call (403) 930-5888 for your oil change today.', related=['maintenance', 'battery', 'tires']),

    'brakes': dict(
        seo_title='Brake Repair & Replacement Calgary | Pads & Rotors | Busy Bee',
        meta='Brake repair and replacement in NE Calgary: pads, rotors, calipers, and brake fluid. Free brake inspection with every '
             'service. Book today.',
        focus='brake replacement calgary', eyebrow='BRAKE REPAIR · NE CALGARY',
        h1='Brake repair &amp; brake replacement in <em>Calgary</em>',
        intro='Grinding, squealing, or a soft pedal means your brakes need attention now. Our Calgary brake shop inspects the whole '
              'system, explains what’s worn, and replaces only what you need, with quality pads and rotors built for stop-and-go city '
              'driving and icy winters.',
        offer=('disc-3', 'Grinding or squealing?', 'Book a brake inspection'),
        cta='Book a brake inspection', photos=['brake-repair-calgary', 'busy-bee-repair-bay-calgary'],
        sections=[
            ('list', 'Brake', 'services', [
                ('Brake inspection and diagnosis', ''), ('Brake pad replacement', ''), ('Rotor replacement or resurfacing', ''),
                ('Brake caliper replacement', ''), ('Brake fluid flush', ''), ('Brake line and hose repair', ''),
                ('ABS warning light diagnosis', '')]),
            ('signs', 'Warning signs your brakes need service', [
                'Squealing or grinding when you stop', 'A soft, spongy, or sinking brake pedal',
                'Vibration in the pedal or steering wheel when braking', 'The car pulls to one side when braking',
                'A brake or ABS warning light']),
            ('callout', 'Why trust us with your brakes',
             'Brakes are safety-critical, so we never cut corners. We measure pad and rotor thickness, show you the results, and use '
             'quality parts covered by warranty.'),
        ],
        faqs=[('How long do brake pads last?', 'Typically 40,000 to 70,000 km, often less with heavy city driving.'),
              ('Do I need new rotors every time?', 'Not always. We measure them and only recommend replacement when they’re below '
                                                  'spec or warped.'),
              ('How much does brake replacement cost in Calgary?', 'It depends on your vehicle and parts. We’ll give you an exact '
                                                                  'quote before any work.')],
        cta_text='Book a brake inspection: (403) 930-5888.', related=['suspension', 'alignment', 'tires']),

    'battery': dict(
        seo_title='Car Battery Replacement Calgary | Free Battery Test | Busy Bee',
        meta='Car battery replacement in NE Calgary with free battery testing. Alternator and starter diagnosis, warranty-backed '
             'batteries for Alberta winters.',
        focus='car battery calgary', eyebrow='BATTERY &amp; ALTERNATOR · NE CALGARY',
        h1='Car battery replacement in Calgary, with free battery <em>testing</em>',
        intro='Calgary winters kill weak batteries. Drop by for a free battery test and we’ll check your battery, alternator, and '
              'starter in minutes. If you need a new car battery, we’ll install the right one with a warranty, and reset your car’s '
              'electronics where needed.',
        offer=('battery-charging', 'Free battery test', 'No appointment or purchase needed'),
        cta='Get a free battery test', photos=['battery-alternator-service-calgary', 'busy-bee-repair-bay-calgary'],
        sections=[
            ('list', 'Battery &amp; charging', 'services', [
                ('Free battery test', ''), ('Car battery replacement and installation', ''), ('Alternator testing and replacement', ''),
                ('Starter motor diagnosis and replacement', ''), ('Terminal cleaning and corrosion protection', ''),
                ('Battery registration', 'For vehicles that need it (BMW, Mercedes, VW).')]),
            ('signs', 'Signs your battery is failing', [
                'Slow or clicking starts, especially on cold mornings', 'Dim headlights or flickering dash lights',
                'Battery warning light', 'A battery more than 3 to 5 years old', 'A swollen case or corroded terminals']),
            ('callout', 'Battery or alternator?',
             'Many drivers aren’t sure which one failed. A weak battery struggles to start the car; a failing alternator stops the '
             'battery charging, so it dies again after a jump. We test both, so you don’t replace a good battery.'),
        ],
        faqs=[('How long do car batteries last in Calgary?', 'Usually 3 to 5 years. Extreme cold shortens that.'),
              ('Is the battery test really free?', 'Yes, no appointment or purchase needed.'),
              ('Could it be my alternator instead?', 'It can be. We test both, so you don’t replace a good battery.')],
        cta_text='Get a free battery test today: (403) 930-5888.', related=['electrical', 'maintenance', 'engine']),

    'transmission': dict(
        seo_title='Transmission Shop Calgary | Transmission Repair | Busy Bee Auto',
        meta='Transmission repair in NE Calgary. Diagnosis for slipping, hard shifts, and leaks, plus transmission fluid changes and '
             'flushes. All makes and models.',
        focus='transmission shop calgary', eyebrow='TRANSMISSION SHOP · NE CALGARY', h1='Transmission repair in <em>Calgary</em>',
        intro='Slipping gears, delayed shifts, or a burning smell are early warnings. Our Calgary transmission shop diagnoses the real '
              'problem first. Many issues are fixed with a fluid service, a solenoid, or a sensor rather than a full rebuild.',
        offer=('unplug', 'Diagnose first', 'Not every problem needs a rebuild'),
        cta='Book a transmission diagnosis', photos=['busy-bee-repair-bay-calgary', 'engine-repair-audi-calgary'],
        sections=[
            ('list', 'Transmission', 'services', [
                ('Diagnosis and road testing', ''), ('Fluid change and filter service', ''), ('Transmission flush', ''),
                ('Cooler line inspection and repair', ''), ('Solenoid and sensor repair', ''), ('Leak repair', ''),
                ('Clutch repair (manual transmissions)', '')]),
            ('signs', 'Symptoms of transmission trouble', [
                'Gears slipping, or RPMs rising without the car speeding up', 'Harsh, delayed, or erratic shifting',
                'Red fluid leaking under the car', 'A burning smell', 'Whining, clunking, or humming noises',
                'Check engine light with transmission codes']),
            ('steps', 'Diagnose, explain,', 'repair', [
                ('Diagnose', 'Scan, fluid check and road test to find the real cause.'),
                ('Explain', 'Every option, from a fluid service to a repair, in plain English.'),
                ('Repair', 'Only the work you approve, then a final road test.')]),
        ],
        faqs=[('How often should transmission fluid be changed?', 'Typically every 50,000 to 100,000 km. Check your owner’s manual, '
                                                                 'and go sooner if you tow.'),
              ('Do I need a rebuild?', 'Not necessarily. We diagnose first and explain every option.')],
        cta_text='Book a transmission diagnosis: (403) 930-5888.', related=['engine', 'maintenance', 'electrical']),

    'engine': dict(
        seo_title='Engine Repair Calgary | Check Engine Light Diagnosis | Busy Bee',
        meta='Engine repair in NE Calgary: check engine light, misfires, overheating, oil leaks, and timing belts. Honest diagnosis '
             'and clear quotes on all makes.',
        focus='engine repair calgary', eyebrow='ENGINE REPAIR · NE CALGARY', h1='Engine repair in <em>Calgary</em>',
        intro='Engine misfiring, losing power, or showing a check engine light? Our certified mechanics use computer diagnostics to '
              'find the exact cause, explain it in plain English, and give you a clear quote before we start.',
        offer=('settings-2', 'Check engine light?', 'Same-day diagnosis, often'),
        cta='Book an engine diagnosis', photos=['engine-repair-audi-calgary', 'computer-diagnostics-calgary'],
        sections=[
            ('list', 'Engine problems', 'we fix', [
                ('Check engine light', 'Fault code reading and root-cause diagnosis.'),
                ('Misfires and rough idle', 'Spark plugs, ignition coils, and fuel injectors.'),
                ('Overheating', 'Head gaskets, water pumps, and thermostats.'),
                ('Knocking or ticking', 'Lifters, timing components, and oil pressure issues.'),
                ('Oil and coolant leaks', 'Gaskets and seals.'), ('Loss of power', 'Fuel system, intake, and sensors.')]),
            ('signs', 'Engine maintenance we offer', [
                'Timing belt and timing chain service', 'Drive belt replacement', 'Spark plug replacement',
                'Throttle body and intake cleaning', 'Fuel system service', 'Air and cabin filter replacement'], 'check'),
            ('steps', 'Our', 'process', [
                ('Diagnose', 'With computer scanning and hands-on testing.'), ('Explain', 'The problem and your options.'),
                ('Repair', 'Only after your approval.'), ('Test drive', 'And recheck before you pick up.')]),
        ],
        faqs=[('Is it safe to drive with the check engine light on?', 'If it’s flashing, stop driving and call us. A steady light is '
                                                                     'less urgent, but book a diagnosis soon.'),
              ('Repair or replace the engine?', 'We’ll compare costs honestly, including the car’s overall condition.')],
        cta_text='Book an engine diagnosis: (403) 930-5888.', related=['electrical', 'cooling', 'transmission']),

    'electrical': dict(
        seo_title='Auto Electrical Repair & Car Diagnostics Calgary | Busy Bee',
        meta='Car diagnostics and auto electrical repair in NE Calgary. Warning lights, wiring faults, starters, alternators, and '
             'sensors found and fixed at the source.',
        focus='auto electrical repair calgary', eyebrow='ELECTRICAL &amp; DIAGNOSTICS · NE CALGARY',
        h1='Auto electrical repair &amp; vehicle diagnostics in <em>Calgary</em>',
        intro='Modern cars run on electronics, and electrical faults are easy to misdiagnose. We use advanced diagnostic equipment to '
              'trace the problem to its source, so you pay for one correct repair instead of a series of guesses.',
        offer=('circle-gauge', 'Advanced diagnostics', 'Find the real cause first'),
        cta='Book a diagnostic', photos=['computer-diagnostics-calgary', 'busy-bee-repair-bay-calgary'],
        sections=[
            ('list', 'Electrical &amp; diagnostic', 'services', [
                ('Computer diagnostics', 'Warning light scans.'), ('Wiring and connector repair', ''),
                ('Alternator and starter replacement', ''), ('Battery and charging system testing', ''),
                ('Ignition system inspection', ''), ('Power window, lock, and lighting repairs', ''),
                ('Parasitic battery drain testing', '')]),
            ('signs', 'Common electrical symptoms', [
                'Several warning lights at once', 'A battery that keeps dying overnight',
                'Lights, windows, or gauges working only some of the time', 'No-start or intermittent stalling',
                'A burning plastic smell']),
            ('callout', 'Why a proper diagnostic saves you money',
             'A diagnostic is skilled testing time. It saves you money by fixing the right part first, instead of replacing parts '
             'until the fault goes away.'),
        ],
        faqs=[('Why do I pay for a diagnostic?', 'It’s skilled testing time. It saves you money by fixing the right part first.'),
              ('Can you fix intermittent problems?', 'Yes. These take patience, and we’ll keep you updated as we test.')],
        cta_text='Book a diagnostic: (403) 930-5888.', related=['battery', 'engine', 'maintenance']),

    'suspension': dict(
        seo_title='Suspension & Steering Repair Calgary | Shocks, Struts | Busy Bee',
        meta='Suspension and steering repair in NE Calgary: shocks, struts, ball joints, tie rods, control arms, and wheel bearings. '
             'Smoother, safer handling.',
        focus='suspension repair calgary', eyebrow='SUSPENSION &amp; STEERING · NE CALGARY',
        h1='Suspension &amp; steering repair in <em>Calgary</em>',
        intro='Calgary’s potholes are brutal on suspension. If your ride is bouncy, noisy, or wandering on the highway, our mechanics '
              'will inspect your suspension and steering and fix what’s worn, restoring stable handling and protecting your tires.',
        offer=('waves', 'Pothole damage?', 'Book a suspension inspection'),
        cta='Book a suspension inspection', photos=['busy-bee-service-bays-calgary', 'brake-repair-calgary'],
        sections=[
            ('list', 'Suspension &amp; steering', 'services', [
                ('Shock and strut replacement', ''), ('Coil spring replacement', ''), ('Control arm and bushing replacement', ''),
                ('Ball joint and tie rod ends', ''), ('Sway bar link replacement', ''), ('Wheel bearing replacement', ''),
                ('Power steering and rack', 'Power steering pump, rack and pinion, and steering gearbox repair.')]),
            ('signs', 'Signs of suspension problems', [
                'Clunking over bumps', 'Excessive bouncing or nose-diving when braking', 'Loose or wandering steering',
                'Uneven or cupped tire wear', 'A humming noise that rises with speed (often a wheel bearing)']),
            ('callout', 'Alignment after suspension work',
             'New suspension parts change your wheel angles. We’ll tell you when an alignment is needed and can do it in the same '
             'visit.'),
        ],
        faqs=[('Do I need an alignment after suspension work?', 'Usually, yes. We’ll tell you when and can do it in the same visit.'),
              ('How long do shocks and struts last?', 'Often 80,000 to 160,000 km, less on rough roads.')],
        cta_text='Book a suspension inspection: (403) 930-5888.', related=['alignment', 'tires', 'brakes']),

    'cooling': dict(
        seo_title='Radiator Repair Calgary | Cooling System Service | Busy Bee Auto',
        meta='Radiator repair and cooling system service in NE Calgary: coolant flushes, thermostats, water pumps, and hoses. Stop '
             'overheating before it damages your engine.',
        focus='radiator repair calgary', eyebrow='RADIATOR &amp; COOLING · NE CALGARY',
        h1='Radiator repair &amp; cooling system service in <em>Calgary</em>',
        intro='An overheating engine can be ruined in minutes. Our Calgary mechanics repair radiators, water pumps, thermostats, and '
              'hoses, and flush old coolant, so your engine stays at the right temperature through hot summers and freezing winters.',
        offer=('snowflake', 'Engine overheating?', 'Stop driving and call us'),
        cta='Book cooling system service', photos=['computer-diagnostics-calgary', 'engine-repair-audi-calgary'],
        sections=[
            ('list', 'Cooling system', 'services', [
                ('Radiator repair and replacement', ''), ('Coolant flush and refill', ''), ('Thermostat replacement', ''),
                ('Water pump replacement', ''), ('Hose and clamp replacement', ''), ('Pressure test and leak detection', ''),
                ('Heater core diagnosis', 'No heat in winter.')]),
            ('signs', 'Warning signs', [
                'The temperature gauge climbing into the red', 'Sweet-smelling steam or puddles of green, orange, or pink coolant',
                'Coolant level dropping', 'No cabin heat in winter']),
            ('callout', 'What to do if your car overheats',
             'Pull over, turn off the engine, and don’t open a hot radiator cap. Call us on (403) 930-5888.'),
        ],
        faqs=[('How often should coolant be flushed?', 'Typically every 3 to 5 years or about 100,000 km. Check your manual.'),
              ('What should I do if my car overheats?', 'Pull over, turn off the engine, and don’t open a hot radiator cap. Call us.')],
        cta_text='Book cooling system service: (403) 930-5888.', related=['engine', 'maintenance', 'electrical']),

    'maintenance': dict(
        seo_title='Car Maintenance Calgary | Scheduled Service & Tune-Ups | Busy Bee',
        meta='Scheduled car maintenance in NE Calgary: fluid checks, belts, filters, spark plugs, and inspections that keep your '
             'warranty valid and prevent breakdowns.',
        focus='car maintenance calgary', eyebrow='CAR MAINTENANCE · NE CALGARY',
        h1='Car maintenance &amp; scheduled service in <em>Calgary</em>',
        intro='Regular maintenance is the cheapest way to avoid big repair bills. We follow your manufacturer’s schedule, adjusted for '
              'Calgary’s tough conditions, and keep a record for your warranty.',
        offer=('clipboard-check', 'Keep your warranty', 'Skip the dealer prices'),
        cta='Book scheduled maintenance', photos=['busy-bee-repair-bay-calgary', 'mobil-1-synthetic-oil-change-calgary'],
        sections=[
            ('list', 'Maintenance', 'services', [
                ('Manufacturer-scheduled maintenance', ''), ('Fluid checks and top-ups', 'Coolant, brake, power steering, washer.'),
                ('Belt and chain inspection', 'And replacement when due.'), ('Air and cabin filter replacement', ''),
                ('Spark plugs and tune-ups', ''), ('Transmission fluid change', ''),
                ('Seasonal inspections', 'For winter and summer.')]),
            ('callout', 'Does dealer maintenance matter for my warranty?',
             'No. In Canada you can have your car maintained at an independent shop without voiding the manufacturer’s warranty, as '
             'long as the work follows the schedule and uses the right parts and fluids. We document every service.'),
            ('steps', 'A typical service', 'timeline', [
                ('8,000 km', 'Oil and filter, tire rotation, fluid top-ups and a multi-point inspection.'),
                ('50,000 km', 'Air and cabin filters, brake inspection, coolant and belt checks.'),
                ('100,000 km', 'Spark plugs, transmission fluid, coolant flush and timing components as scheduled.')]),
        ],
        faqs=[('What does a tune-up include?', 'Usually spark plugs, filters, a fluid check, and a full inspection, depending on your '
                                               'vehicle.'),
              ('How do I know what my car needs?', 'Bring it in. We’ll check the mileage against your maintenance schedule and give '
                                                   'you a clear list.')],
        cta_text='Book scheduled maintenance: (403) 930-5888.', related=['oil', 'brakes', 'battery']),
}
