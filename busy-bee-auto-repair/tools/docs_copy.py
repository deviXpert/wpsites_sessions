"""Long-form copy for Engine / Brake / Oil Change pages, from the client's Google Docs (Nov 2026):
  engine  https://docs.google.com/document/d/1NdacEbsPBENDME-W-LQRJzPLgRnwizio1vcYpSdLqco
  brakes  https://docs.google.com/document/d/13e_NYIfGRM8_zAoVXMcOJXRgnSKnAk6zd9_r7UasZXE
  oil     https://docs.google.com/document/d/1afvEGZ47QDLnKtgSq7fZoVGlZwHe74005lPSnuKg_CU
Merged over service_content.PAGES (hero, sections, FAQs, meta).  Bracketed link notes in the docs became real internal links."""
from sitemap import SVC_URL


def P(*ps):
    return ''.join(f'<p>{p}</p>' for p in ps)


def UL(*items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def A(text, key):
    return f'<a href="{SVC_URL[key]}">{text}</a>'


ENGINE = dict(
    seo_title='Engine Repair Calgary | Expert Engine Diagnostics & Repair',
    meta='Get reliable engine repair in Calgary at Busy Bee Auto Repair. Book engine diagnostics, maintenance and professional repairs for '
         'your vehicle.',
    focus='engine repair calgary',
    h1='Engine Repair <em>Calgary</em><span class="bb-h1-sub">Professional Engine Diagnostics &amp; Repair at Busy Bee Auto Repair</span>',
    intro='Your vehicle’s engine should respond smoothly when you start the car, accelerate, or drive through Calgary traffic. When '
          'something changes, such as unusual noise, reduced power, excessive smoke, or a warning light on the dashboard, it is worth '
          'finding out why. Ignoring these signs can allow a relatively small mechanical issue to develop into a more expensive repair.',
    sections=[
        ('rich', 'Engine repair in Calgary at Busy Bee', P(
            'At Busy Bee Auto Repair, we provide engine repair in Calgary for drivers who need help identifying and resolving '
            'engine-related problems. Our approach starts with understanding the symptoms, checking the relevant components, and '
            'determining what repair is actually needed. Whether your vehicle has developed a starting issue, an oil leak, or an ongoing '
            'performance problem, our team can help assess its condition and recommend the appropriate next step.',
            'We work with different makes and models, including cars, SUVs, vans, and light trucks. Our goal is to help Calgary drivers '
            'maintain dependable vehicle performance through proper inspection, practical repair solutions, and clear communication.'),
         'engine-repair-audi-calgary'),
        ('cards', 'When Does Your Car Need Engine Repair?', P(
            'Engine problems do not always begin with a complete breakdown. In many cases, your vehicle will show smaller warning signs '
            'before its performance becomes seriously affected. Recognizing these symptoms early can help you arrange an inspection before '
            'additional components are damaged.', 'Here are some common signs that your vehicle may need professional engine repair.'), [
            ('Check Engine Light Keeps Coming On', P(
                'The check engine light is one of the most common reasons drivers visit an auto repair shop. It can indicate anything from an '
                'emissions-related fault to an issue involving ignition, fuel delivery, or engine sensors.',
                'A warning light does not automatically mean that your engine needs replacement. The correct solution depends on the '
                'underlying fault.',
                'Our diagnostic process helps identify stored trouble codes and investigate the related components. Rather than replacing '
                'parts based on assumptions, we focus on understanding what is causing the warning.')),
            ('Engine Misfires and Rough Idling', P(
                'Does your vehicle shake when stopped at a traffic light? Does the engine feel uneven when you accelerate?',
                'These symptoms may indicate an engine misfire. A misfire occurs when one or more cylinders fail to burn the air-fuel '
                'mixture correctly.', 'Possible causes include:') + UL(
                'Worn or damaged spark plugs', 'Faulty ignition coils', 'Fuel injector problems', 'Vacuum leaks',
                'Compression-related issues') + P(
                'Driving with an ongoing misfire can affect fuel economy and potentially damage other components, including the catalytic '
                'converter. A proper inspection helps determine whether the problem is related to ignition, fuel delivery, or engine '
                'compression.')),
            ('Unusual Engine Knocking or Ticking Sounds', P(
                'An unfamiliar noise coming from under the hood should never be ignored.',
                'Different engine sounds can point towards different mechanical problems. For example, ticking may be associated with valve '
                'train components or lubrication issues, while deeper knocking can sometimes indicate internal engine wear.',
                'The location, frequency, and intensity of the sound all matter when identifying the cause.',
                'At Busy Bee Auto Repair, the appropriate inspection can help narrow down the source of the noise and establish whether the '
                'issue involves external components, lubrication, timing, or internal engine parts.')),
            ('Engine Overheating', P(
                'An overheating engine needs immediate attention. If your temperature gauge rises above its normal range or you notice a '
                'temperature warning, safely pull over and switch off the engine.',
                'Continuing to drive an overheating vehicle can cause serious damage, including cylinder head warping and head gasket '
                'failure.', 'Common reasons for overheating include:') + UL(
                'Coolant leaks', 'A malfunctioning thermostat', 'A damaged radiator', 'Water pump failure', 'Cooling fan problems',
                'Low coolant levels') + P(
                'The cooling system should be inspected to identify why the engine is getting too hot. If your vehicle is experiencing '
                'temperature-related problems, explore our ' + A('Cooling System Services in Calgary', 'cooling') + ' for more information.')),
            ('Reduced Engine Power and Poor Acceleration', P(
                'If your vehicle struggles to accelerate, feels weaker than usual, or has difficulty maintaining speed, there may be an '
                'underlying engine performance issue.',
                'Possible causes include restricted airflow, fuel delivery problems, ignition faults, sensor failures, or reduced engine '
                'compression.',
                'Modern vehicles rely on multiple electronic systems to regulate engine performance. A fault in one component can affect the '
                'way the entire engine operates.',
                'A diagnostic inspection can help identify the source instead of relying on unnecessary part replacements.')),
            ('Blue, White, or Black Exhaust Smoke', P('Exhaust smoke can provide useful clues about your vehicle’s condition.') + UL(
                '<strong>Blue smoke:</strong> May indicate that engine oil is entering the combustion chamber and burning with the fuel.',
                '<strong>White smoke:</strong> Persistent white smoke after the engine has warmed up may indicate coolant entering the '
                'combustion chamber.',
                '<strong>Black smoke:</strong> Can suggest an excessively rich air-fuel mixture or a fuel delivery problem.') + P(
                'Not every instance of white vapour indicates engine damage. Water condensation can produce temporary vapour, especially '
                'during cold weather.',
                'However, persistent smoke, unusual smells, or changes in engine performance deserve attention.')),
        ]),
        ('cards', 'Our Engine Repair and Maintenance Services in Calgary', P(
            'Engine performance depends on several connected systems working together. A problem with ignition, timing, fuel delivery, or '
            'lubrication can affect how efficiently your vehicle operates.',
            'Busy Bee Auto Repair offers engine-related inspection, maintenance, and repair services to help address these concerns.'), [
            ('Engine Component Inspection', P(
                'A detailed inspection helps identify visible damage, worn components, leaks, and other conditions that may affect engine '
                'operation. Checking the relevant components is an important step before recommending repairs.')),
            ('Timing System Service', P(
                'Timing components help coordinate the movement of engine valves and pistons. Depending on the vehicle, timing belts, '
                'chains, tensioners, and related parts may require inspection or replacement.',
                'A worn timing component can affect engine operation and, in certain engines, cause serious internal damage if it fails.')),
            ('Spark Plug Replacement', P(
                'Spark plugs create the spark needed to ignite the air-fuel mixture inside the cylinders. Worn plugs can contribute to '
                'misfires, difficult starting, rough idling, and reduced fuel efficiency.',
                'Replacing them according to the vehicle manufacturer’s maintenance schedule helps support consistent engine performance.')),
            ('Water Pump Replacement', P(
                'The water pump circulates coolant through the engine and cooling system. A failing pump can lead to coolant leaks, unusual '
                'noises, or overheating.',
                'If the water pump is not working correctly, the cooling system should be inspected before further engine damage occurs.')),
            ('Drive Belt Inspection and Replacement', P(
                'Drive belts operate important accessories and components, depending on your vehicle’s design. Cracks, unusual noises, or '
                'visible wear can indicate that a belt needs attention.',
                'Regular inspection helps identify deterioration before a belt fails unexpectedly.')),
            ('Throttle Body and Intake Cleaning', P(
                'The throttle body regulates the amount of air entering the engine. Dirt and carbon deposits can sometimes interfere with '
                'airflow and contribute to rough idling or inconsistent acceleration.',
                'Cleaning may be recommended when inspection confirms that deposits are affecting operation.')),
            ('Engine Oil Leak Detection', P(
                'Oil leaks should not be treated as minor issues without identifying their source. Leaks can develop around seals, gaskets, '
                'filters, or other engine components.',
                'We recommend addressing oil loss promptly because insufficient lubrication can increase friction and accelerate engine '
                'wear.')),
        ], False),
        ('cards', 'Engine Diagnostics vs. Engine Repair: What Is the Difference?', P(
            'Many drivers use these terms interchangeably, but they describe two different stages of automotive service.'), [
            ('Engine diagnostics', P(
                'Engine diagnostics is the process of identifying what is causing a vehicle’s symptoms. It may involve scanning trouble '
                'codes, checking sensor readings, inspecting wiring, and testing relevant mechanical components.')),
            ('Engine repair', P(
                'Engine repair involves correcting the identified problem. Depending on the diagnosis, this could mean replacing a faulty '
                'ignition component, repairing an oil leak, servicing the timing system, or addressing another mechanical issue.')),
        ], False, P(
            'For example, a check engine light may be caused by a faulty ignition coil. The warning light itself is not the problem. '
            'Identifying the faulty coil and correcting the underlying issue is what resolves the concern.',
            'This distinction matters because replacing parts without proper diagnosis can waste money and leave the original problem '
            'unresolved.'), 2),
        ('rich', 'Why Choose Busy Bee Auto Repair for Engine Repair in Calgary?', P(
            'Finding the right mechanic is about more than getting a vehicle back on the road. Drivers also want to understand what went '
            'wrong, what needs attention, and what they can expect from the repair process.',
            'At Busy Bee Auto Repair, we focus on practical automotive service supported by proper inspection and customer communication.')
         + UL('<strong>Experienced Automotive Service:</strong> Our team works with a range of domestic and imported vehicle makes and '
              'models, helping drivers address different engine-related concerns.',
              '<strong>Diagnostic-Based Approach:</strong> Identifying the cause of a problem is an important part of choosing the right '
              'repair. We aim to investigate symptoms before recommending solutions.',
              '<strong>Clear Repair Communication:</strong> Understanding the condition of your vehicle helps you make informed maintenance '
              'and repair decisions.',
              '<strong>Service for Different Vehicles:</strong> We provide automotive repair for cars, SUVs, vans, Jeeps, and pickup trucks.',
              '<strong>Convenient Calgary Location:</strong> Visit our shop at 324 41 Ave NE, Calgary, AB T2E 2N3, for assistance with '
              'your vehicle.')
         + P('Whether you are dealing with an engine warning light or a noticeable change in performance, our team can help you understand '
             'the next steps.'), 'computer-diagnostics-calgary'),
        ('rich', 'Engine Maintenance Tips for Calgary Drivers', P(
            'Calgary’s changing weather and driving conditions make regular vehicle maintenance particularly important. Cold starts, short '
            'city trips, heavy traffic, and temperature changes can all influence vehicle maintenance requirements.',
            'A few simple habits can help you keep your engine in better condition.')
         + UL('<strong>Follow the recommended oil change interval:</strong> Use the oil grade and service schedule specified by your vehicle '
              'manufacturer.',
              '<strong>Check coolant levels:</strong> Monitor the cooling system and arrange an inspection if you notice leaks or repeated '
              'coolant loss.',
              '<strong>Pay attention to warning lights:</strong> Dashboard warnings should be investigated rather than ignored.',
              '<strong>Replace air and oil filters when needed:</strong> Clean filters support proper airflow and lubrication system '
              'performance.',
              '<strong>Listen for unusual sounds:</strong> New knocking, ticking, or rattling noises may indicate a developing mechanical '
              'issue.',
              '<strong>Avoid prolonged overheating:</strong> Stop safely if your temperature gauge enters the danger zone.',
              '<strong>Follow scheduled maintenance:</strong> Your owner’s manual provides important service intervals based on your '
              'specific vehicle.')
         + P('Preventive maintenance cannot eliminate every mechanical problem, but it can help identify wear and potential faults before '
             'they become more serious.')),
        ('callout', 'Book Your Engine Repair Appointment in Calgary',
         'An engine problem can make everyday driving stressful, especially when you are unsure whether the vehicle is safe to operate or '
         'how serious the issue might be. Instead of guessing or continuing to drive with unexplained symptoms, arrange an inspection with '
         'Busy Bee Auto Repair. Our team can assess your vehicle, help identify the problem, and discuss suitable repair options. From '
         'engine diagnostics and misfire concerns to timing system service and oil leak inspection, we are here to help Calgary drivers '
         'make informed decisions about their vehicles.<br><br><strong>Looking for reliable engine repair in Calgary?</strong> Contact Busy '
         'Bee Auto Repair today at <a href="tel:+14039305888">(403) 930-5888</a> to discuss your vehicle’s symptoms or arrange an '
         'appointment. Address: 324 41 Ave NE, Calgary, AB T2E 2N3, Canada'),
    ],
    faqs=[
        ('How do I know if my car needs engine repair?', 'Common warning signs include a check engine light, unusual engine noises, rough '
         'idling, excessive exhaust smoke, overheating, oil leaks, and reduced acceleration. A professional inspection can help identify the '
         'underlying issue.'),
        ('Can I drive my car with the check engine light on?', 'It depends on the warning and how the vehicle is behaving. A steady check '
         'engine light generally indicates that the vehicle needs diagnosis soon. If the light flashes, or the engine is shaking, '
         'overheating, or losing power, safely stop driving and arrange professional assistance.'),
        ('What causes an engine to overheat?', 'Common causes include coolant leaks, a damaged radiator, a faulty thermostat, water pump '
         'problems, and cooling fan failures. The cooling system needs to be inspected to determine the actual cause.'),
        ('Is engine misfiring a serious problem?', 'It can be. Misfires may result from worn spark plugs, faulty ignition coils, fuel '
         'injector issues, or compression problems. Continuing to drive with a persistent misfire can cause additional damage.'),
        ('How much does engine repair cost in Calgary?', 'The cost depends on the vehicle, the underlying problem, labour requirements, and '
         'replacement parts. A minor ignition repair will generally cost less than major internal engine work. An inspection and repair '
         'estimate can help establish the expected cost.'),
        ('How long does engine repair take?', 'Repair time varies depending on the issue and parts availability. Some repairs can be '
         'completed within a few hours, while more complex mechanical work may require additional time.'),
        ('Does Busy Bee Auto Repair service different vehicle makes and models?', 'Yes. Busy Bee Auto Repair works with different domestic '
         'and imported vehicles, including cars, SUVs, vans, Jeeps, and pickup trucks.'),
        ('Where can I get professional engine repair in Calgary?', 'Busy Bee Auto Repair is located at 324 41 Ave NE, Calgary, AB T2E 2N3. '
         'Contact the shop at (403) 930-5888 to discuss your engine problem and arrange a visit.'),
    ],
)

BRAKES = dict(
    seo_title='Brake Repair Calgary | Brake Pads, Rotors & Replacement',
    meta='Need brake repair in Calgary? Get brake pad, rotor, caliper and ABS services at Busy Bee Auto Repair. Book your brake inspection '
         'today.',
    focus='brake repair calgary',
    h1='Brake Repair <em>Calgary</em><span class="bb-h1-sub">Brake Pad, Rotor &amp; Brake Replacement Services</span>',
    intro='Your brakes are the most important safety system in your vehicle. Whether you are slowing down in heavy Calgary traffic, '
          'approaching a busy intersection, or driving on an icy road, you need your braking system to respond properly every time you '
          'press the pedal.',
    sections=[
        ('rich', 'Professional brake repair in Calgary', P(
            'A change in braking performance should never be treated as a minor inconvenience. Squealing sounds, steering wheel vibration, a '
            'soft brake pedal, or longer stopping distances can indicate that one or more brake components need attention.',
            'At Busy Bee Auto Repair, we provide professional brake repair in Calgary for drivers experiencing braking problems or looking '
            'for routine brake maintenance. From worn brake pads and damaged rotors to caliper issues and ABS warning lights, our team '
            'inspects the braking system to identify the cause and recommend the necessary repairs.',
            'Our goal is simple: help you maintain reliable braking performance with proper inspections, quality replacement parts, and '
            'clear repair estimates.'), 'brake-repair-calgary'),
        ('cards', 'What Are the Warning Signs of Brake Problems?', P(
            'Brake components experience friction and wear every time you slow down. Over time, this can reduce their ability to perform '
            'effectively. Recognizing early warning signs can help prevent additional damage and avoid unsafe driving conditions.',
            'Here are some common symptoms that indicate your vehicle may need brake service.'), [
            ('Squealing or Grinding Noise When Braking', P(
                'A high-pitched squealing sound when applying the brakes can indicate worn brake pads. Many brake pads have wear indicators '
                'that produce noise when the friction material becomes thin.',
                'Grinding is more concerning. It may mean the brake pad material has worn away, allowing metal components to make contact '
                'with the rotor.',
                'If you hear persistent grinding, arrange an inspection as soon as possible. Continuing to drive may damage the rotors and '
                'increase the cost of repairs.')),
            ('Steering Wheel or Brake Pedal Vibration', P(
                'Does your steering wheel shake when you apply the brakes?',
                'This can happen when brake rotors develop uneven thickness, surface deposits, or excessive runout. These conditions may '
                'create vibrations that you feel through the pedal or steering wheel.',
                'However, vibration is not always caused by the brakes. Suspension and steering components can also contribute to similar '
                'symptoms.',
                'A proper inspection helps determine whether the issue is related to the rotors, calipers, suspension, or another part of the '
                'vehicle.')),
            ('Soft or Spongy Brake Pedal', P(
                'Your brake pedal should feel consistent when you press it. If it suddenly feels soft, spongy, or sinks closer to the floor '
                'than usual, there may be a problem with the hydraulic braking system.', 'Possible causes include:') + UL(
                'Air trapped inside brake lines', 'Brake fluid leakage', 'A failing master cylinder', 'Damaged brake hoses',
                'Problems with hydraulic components') + P(
                'A brake pedal that sinks or feels unusually soft can indicate a serious safety issue. Do not continue driving if braking '
                'performance is compromised. Arrange professional assistance.')),
            ('Vehicle Pulls to One Side During Braking', P(
                'If your vehicle moves towards the left or right when you apply the brakes, one side of the braking system may not be '
                'operating correctly.',
                'Potential causes include a sticking brake caliper, uneven pad wear, contaminated friction material, or a hydraulic problem.',
                'Uneven braking can make it harder to maintain vehicle control, particularly during sudden stops or slippery driving '
                'conditions.')),
            ('Brake or ABS Warning Light Appears', P(
                'Modern vehicles use electronic systems to monitor braking performance. If the ABS or brake warning light appears on your '
                'dashboard, the system may have detected a fault.',
                'An ABS warning can be related to wheel speed sensors, wiring, fuses, or other components.',
                'When ABS is not functioning correctly, the vehicle may still have conventional braking, but the anti-lock function may be '
                'unavailable. A red brake warning light can indicate a more serious condition, including low brake fluid or a hydraulic '
                'system problem.',
                'Do not ignore these warnings. Have the system inspected to understand what is happening.')),
        ]),
        ('cards', 'Complete Brake Repair Services in Calgary', P(
            'A vehicle’s braking system contains several components that work together to slow and stop the wheels. Replacing one worn '
            'component without checking the surrounding parts may leave an underlying problem unresolved.',
            'Busy Bee Auto Repair provides different brake services to address common braking concerns.'), [
            ('Brake Pad Replacement', P(
                'Brake pads create friction against the rotors to slow down your vehicle. Because they are designed to wear over time, they '
                'require periodic inspection and replacement.', 'The lifespan of brake pads depends on several factors, including:') + UL(
                'Driving habits and braking frequency', 'Vehicle weight', 'Road and traffic conditions', 'Brake pad material',
                'Driving environment') + P(
                'Frequent stop-and-go driving in Calgary can increase brake wear compared with steady highway driving.',
                'We inspect pad thickness and condition to determine whether replacement is necessary.')),
            ('Brake Rotor Replacement and Resurfacing', P(
                'Brake rotors are the metal discs that rotate with your wheels. When you apply the brakes, the pads press against these '
                'discs to create the friction required to slow your vehicle.',
                'Rotors can develop excessive wear, scoring, uneven surfaces, or thickness variation.',
                'Depending on their condition and manufacturer specifications, resurfacing may be an option. However, rotors that are too '
                'thin, cracked, or otherwise damaged need replacement.',
                'Replacing rotors when required helps maintain proper contact between the pads and braking surfaces.')),
            ('Brake Caliper Repair and Replacement', P(
                'Brake calipers apply pressure to the brake pads so they can clamp against the rotors.',
                'A sticking or seized caliper may cause uneven braking, excessive heat, premature pad wear, or a vehicle that pulls to one '
                'side.',
                'Other warning signs can include unusual burning smells and one wheel becoming noticeably hotter than the others.',
                'Our inspection helps identify caliper-related issues and determine whether repair or replacement is appropriate.')),
            ('Brake Fluid Flush and Replacement', P(
                'Brake fluid transfers hydraulic pressure from the brake pedal to the braking components at each wheel.',
                'Over time, brake fluid can absorb moisture. This can reduce its boiling point and affect braking performance, especially '
                'under demanding conditions.',
                'A brake fluid service may be recommended according to the manufacturer’s maintenance schedule or when testing shows that '
                'the fluid needs attention.',
                'Using the correct fluid specification is important because different vehicles require different types of brake fluid.')),
            ('Brake Line and Hose Repair', P(
                'Brake lines and flexible hoses carry hydraulic fluid throughout the braking system.',
                'Corrosion, physical damage, deterioration, or leakage can affect the system’s ability to maintain pressure.',
                'Any visible brake fluid leak should be treated seriously. Damaged lines and hoses need proper inspection and replacement '
                'where necessary.')),
            ('ABS Diagnostics and Repair', P(
                'The Anti-lock Braking System helps prevent the wheels from locking during hard braking, allowing the driver to maintain '
                'more steering control.', 'An ABS warning light may be caused by:') + UL(
                'Faulty wheel speed sensors', 'Damaged sensor wiring', 'Electrical connection problems', 'ABS module faults',
                'Related system issues') + P(
                'Proper diagnostics help identify the source of the warning rather than replacing components without confirmation.')),
        ], False),
        ('cards', 'Why Brake Maintenance Matters in Calgary', P(
            'Calgary driving conditions can put additional demands on your vehicle’s braking system. Traffic congestion, frequent '
            'intersections, changing temperatures, snow, ice, and road debris can all influence brake performance and component wear.'), [
            ('Winter Driving and Braking Performance', P(
                'During winter, drivers often encounter slippery roads, packed snow, and icy intersections. These conditions require careful '
                'braking and additional stopping distance.',
                'Your ABS system, brake pads, rotors, and tires all play important roles in vehicle control.',
                'Although good brakes cannot eliminate the risk of sliding on ice, properly maintained braking components help ensure that '
                'your vehicle’s braking system is functioning as intended.')),
            ('Stop-and-Go Traffic', P(
                'Repeated acceleration and braking in busy urban traffic can increase friction and heat within the braking system.',
                'This is one reason why brake pads may wear faster in city driving than during consistent highway travel.',
                'If you regularly commute through Calgary, periodic brake inspections can help identify wear before it becomes a more '
                'serious concern.')),
            ('Road Salt and Moisture', P(
                'Winter road treatments and moisture can contribute to corrosion on exposed metal components. Brake rotors may develop '
                'surface rust, while brake lines and other components can deteriorate over time.',
                'Some light surface rust after a vehicle has been parked in wet conditions is normal. Persistent corrosion, unusual noises, '
                'or reduced braking performance should be investigated.')),
        ], False),
        ('rich', 'Brake Repair vs. Brake Replacement: What Does Your Vehicle Need?', P(
            'Not every brake problem requires replacing the entire braking system.',
            'For example, if the brake pads are worn but the rotors remain within the manufacturer’s specifications and have an acceptable '
            'surface condition, replacing the pads alone may be appropriate.',
            'However, if the rotors are cracked, excessively worn, or below their minimum thickness, replacement may be necessary.',
            'Similarly, a brake fluid leak requires identifying and correcting the source of the leak rather than simply adding more fluid.',
            'At Busy Bee Auto Repair, we inspect the relevant components, explain their condition, and provide an estimate before proceeding '
            'with the recommended work.',
            'This approach helps drivers understand what their vehicle actually needs instead of paying for unnecessary replacements.')),
        ('rich', 'Why Choose Busy Bee Auto Repair for Brake Service?', P(
            'When it comes to brakes, quality workmanship and accurate inspections matter. You need a repair shop that takes your concerns '
            'seriously and explains the condition of your vehicle.', 'Drivers choose Busy Bee Auto Repair for several reasons:')
         + UL('<strong>Careful Brake Inspections:</strong> We assess brake pads, rotors, calipers, and other relevant components to identify '
              'wear and potential problems.',
              '<strong>Clear Repair Estimates:</strong> We explain the recommended work and provide an estimate before repairs begin.',
              '<strong>Quality Parts:</strong> We use quality replacement components suited to the vehicle and repair requirements.',
              '<strong>Warranty on Most Repairs:</strong> Our shop offers parts and labour warranty on most repairs, subject to applicable '
              'terms.',
              '<strong>Different Vehicle Makes and Models:</strong> We work with a range of domestic and imported cars, SUVs, vans, and light '
              'trucks.',
              '<strong>Convenient NE Calgary Location:</strong> Visit us at 324 41 Ave NE, Calgary, AB T2E 2N3.')
         + P('Whether your brakes are making unusual noises or you simply want to check their condition before winter, our team can help '
             'you determine the appropriate service.'), 'busy-bee-repair-bay-calgary'),
        ('callout', 'Book a Brake Inspection at Busy Bee Auto Repair',
         'A reliable braking system gives you better confidence behind the wheel. If you have noticed grinding noises, pedal vibration, '
         'uneven braking, or a dashboard warning, do not wait for the problem to become worse. Busy Bee Auto Repair provides brake '
         'inspection, brake pad replacement, rotor service, caliper replacement, brake fluid service, and ABS diagnostics in Calgary.'
         '<br><br>Call <a href="tel:+14039305888">(403) 930-5888</a> to discuss your braking concerns or book an appointment with our team. '
         '<strong>Visit Us:</strong> 324 41 Ave NE, Calgary, AB T2E 2N3, Canada. <strong>Business Hours:</strong> Monday to Friday, 9:00 AM '
         'to 6:00 PM.<br><br>Your safety matters. Let us help you keep your vehicle’s braking system in proper working condition.'),
    ],
    faqs=[
        ('How often should I replace my brake pads?', 'Brake pad lifespan varies depending on the vehicle, driving habits, road conditions, '
         'and pad material. Many brake pads last approximately 40,000 to 70,000 kilometres, but some wear faster. Regular inspections are '
         'the best way to determine when replacement is needed.'),
        ('Do I need to replace brake rotors every time I change brake pads?', 'No. Rotors do not automatically need replacement with every '
         'set of brake pads. If they meet the manufacturer’s minimum thickness requirements and their surface condition is acceptable, they '
         'may be suitable for continued use.'),
        ('Why do my brakes make a grinding noise?', 'Grinding may indicate that the brake pads have worn down enough for metal components to '
         'contact the rotor. It can also be caused by debris or other mechanical problems. Arrange an inspection promptly to prevent further '
         'damage.'),
        ('What causes a brake pedal to feel soft?', 'A soft or spongy brake pedal can result from air in the hydraulic system, leaking brake '
         'fluid, damaged hoses, or a failing master cylinder. Because this can affect stopping ability, the vehicle should be inspected '
         'before further driving.'),
        ('How much does brake repair cost in Calgary?', 'Brake repair costs depend on your vehicle’s make and model, the components requiring '
         'attention, and the replacement parts needed. A brake pad replacement will generally cost less than a repair involving rotors, '
         'calipers, or hydraulic components. Busy Bee Auto Repair can provide an estimate after inspecting your vehicle.'),
        ('Can I drive with the ABS warning light on?', 'An illuminated ABS warning light usually means the anti-lock braking function may '
         'not be working correctly. Conventional braking may still operate, but you should arrange an inspection as soon as possible. If the '
         'red brake warning light also appears or braking feels abnormal, stop safely and arrange assistance.'),
        ('Why does my car pull to one side when I brake?', 'Possible reasons include a sticking caliper, uneven brake pad wear, contaminated '
         'pads, or hydraulic pressure problems. Suspension and steering faults can also cause pulling, so a proper inspection is important.'),
        ('Is brake fluid replacement really necessary?', 'Yes. Brake fluid can absorb moisture over time, which may affect its performance '
         'and corrosion protection. Follow your vehicle manufacturer’s recommended service interval and have the fluid inspected when '
         'necessary.'),
        ('Where can I get brake repair in NE Calgary?', 'Busy Bee Auto Repair provides brake inspections and repair services at 324 41 Ave '
         'NE, Calgary, AB T2E 2N3. Call (403) 930-5888 to arrange an appointment.'),
        ('Does Busy Bee Auto Repair replace brake pads and rotors?', 'Yes. The shop lists brake pad replacement and rotor replacement or '
         'resurfacing among its brake services. The appropriate option depends on the condition and specifications of your braking '
         'components.'),
    ],
)

OIL = dict(
    seo_title='Oil Change Calgary | Synthetic Oil Change from $75',
    meta='Need an oil change in Calgary? Get Mobil 1 synthetic oil from $75 at Busy Bee Auto Repair, with a free multi-point vehicle '
         'inspection.',
    focus='oil change calgary',
    h1='Oil Change <em>Calgary</em><span class="bb-h1-sub">Synthetic Oil Change &amp; Vehicle Maintenance</span>',
    intro='Keeping up with regular oil changes is one of the simplest ways to protect your vehicle’s engine. Engine oil reduces friction '
          'between moving parts, helps control heat and carries dirt and small contaminants away from important engine components. As oil '
          'gets older, it gradually loses its ability to perform these jobs effectively.',
    sections=[
        ('rich', 'Professional oil change services in Calgary', P(
            'At Busy Bee Auto Repair, we provide professional oil change services in Calgary for drivers who want to maintain their vehicles '
            'without making routine maintenance complicated. Whether your car needs a conventional oil change, high-mileage oil or synthetic '
            'engine oil, our team can help you choose an option that suits your vehicle’s requirements.',
            'We offer Mobil 1 synthetic oil changes starting at $75, along with a free multi-point inspection. The final price depends on '
            'your vehicle, oil requirements and filter type.',
            'If you are searching for a dependable oil change in Calgary, visit our workshop at 324 41 Ave NE, Calgary, AB T2E 2N3.'),
         'mobil-1-synthetic-oil-change-calgary'),
        ('rich', 'Why Regular Oil Changes Matter for Your Vehicle', P(
            'Your engine contains many moving components that operate at high temperatures and under constant pressure. Engine oil creates a '
            'protective layer between these components, helping them move smoothly while reducing unnecessary friction.',
            'Over time, heat, engine operation and contaminants affect the condition of the oil. If it is not changed according to the '
            'manufacturer’s maintenance schedule, it may become less effective at protecting the engine.',
            'Regular oil changes help with:')
         + UL('<strong>Reducing engine friction:</strong> Fresh oil helps lubricate internal components and supports smoother engine '
              'operation.',
              '<strong>Managing engine heat:</strong> Oil helps carry heat away from engine parts that operate under demanding conditions.',
              '<strong>Removing contaminants:</strong> Engine oil collects dirt and tiny particles that can build up during normal driving.',
              '<strong>Protecting engine components:</strong> Proper lubrication helps reduce unnecessary wear on internal parts.',
              '<strong>Supporting fuel efficiency:</strong> The correct oil helps the engine operate as designed, although fuel economy also '
              'depends on driving habits and vehicle condition.')
         + P('An oil change is a relatively small maintenance task, but delaying it for too long can contribute to larger mechanical '
             'problems.')),
        ('cards', 'Oil Change Services Available in Calgary', P(
            'Different vehicles have different lubrication requirements. The right oil depends on the engine design, manufacturer '
            'recommendations, mileage and driving conditions.',
            'At Busy Bee Auto Repair, we help Calgary drivers choose suitable oil options based on their vehicle’s needs.'), [
            ('Synthetic Oil Change', P(
                'Synthetic engine oil is designed to provide consistent lubrication across a range of operating temperatures. It is commonly '
                'recommended for modern vehicles and engines that require specific oil performance standards.',
                'Depending on the formulation and manufacturer approval, synthetic oil can offer benefits such as:') + UL(
                'Reliable lubrication during cold starts.', 'Resistance to breakdown under high operating temperatures.',
                'Protection against engine deposits.', 'Performance suited to many modern engine designs.') + P(
                'We offer Mobil 1 synthetic oil changes starting at $75. Pricing may vary depending on the vehicle’s oil capacity, filter and '
                'other requirements.')),
            ('Conventional Oil Change', P(
                'Conventional oil is a traditional engine lubricant suitable for certain vehicles that allow its use. It can be an '
                'appropriate option when it meets the manufacturer’s recommended viscosity and performance specifications.',
                'However, not every engine is designed for conventional oil. Always check your owner’s manual before choosing an oil type.')),
            ('High-Mileage Oil Change', P(
                'Vehicles with higher mileage may have different maintenance needs compared with newer cars. High-mileage engine oil is '
                'formulated for older engines and may include additives designed to help condition seals and manage deposits.',
                'It is worth considering when your vehicle has accumulated significant mileage, but the correct choice still depends on the '
                'engine manufacturer’s specifications and the vehicle’s actual condition.')),
        ], False, P('Not sure which oil your car needs? Our team can help you identify the appropriate option before the service begins.')),
        ('steps', 'What Is Included in an', 'Oil Change?', [
            ('Check requirements', 'We identify the recommended oil grade, capacity and filter specifications.'),
            ('Drain old oil', 'Used oil is removed from the engine.'),
            ('Replace the filter', 'The old filter is replaced with a suitable filter for the vehicle.'),
            ('Add fresh oil', 'The correct amount and type of oil are added according to the vehicle’s requirements.'),
            ('Check the level', 'The level is checked to help ensure it is within the recommended range.'),
            ('Look for concerns', 'We look for noticeable leaks or maintenance issues where accessible.'),
            ('Multi-point inspection', 'A free inspection helps identify visible concerns that may need attention. If it reveals an issue '
                                       'that requires additional work, we can discuss it with you before proceeding.'),
        ]),
        ('rich', 'How Often Should You Change Your Engine Oil?', P(
            'There is no single oil-change interval that works for every vehicle. The recommended schedule depends on the engine, oil '
            'specification, vehicle age and driving conditions.',
            'Some vehicles have oil-life monitoring systems that calculate when maintenance is due. Others follow a mileage-based or '
            'time-based service schedule.',
            'As a general guide, many modern vehicles using synthetic oil have recommended intervals somewhere around 8,000 to 12,000 '
            'kilometres. However, this is not a universal rule. Your owner’s manual should always be the primary reference.',
            'You may need more frequent oil changes if you regularly:')
         + UL('Drive in heavy stop-and-go traffic.', 'Make frequent short trips where the engine does not fully warm up.',
              'Drive in extreme cold or very hot weather.', 'Tow heavy loads or carry substantial weight.',
              'Operate your vehicle in dusty conditions.')
         + P('Calgary drivers can experience changing temperatures, winter cold starts and busy city traffic. These conditions may affect '
             'the way a vehicle is used, so it is important to follow the maintenance schedule recommended for your specific engine.'),
         'engine-repair-audi-calgary'),
        ('cards', 'Signs Your Vehicle May Need an Oil Change', P(
            'Your vehicle may provide several indications that an oil service is due. Some signs are easy to notice, while others require a '
            'closer inspection.'), [
            ('Dark or dirty-looking oil', P('Engine oil naturally changes colour as it collects contaminants. Colour alone does not confirm '
                                            'that an oil change is overdue, but it can be worth checking the oil’s condition and service '
                                            'history.')),
            ('Oil change reminder', P('Many modern vehicles display a maintenance reminder when an oil service is due. Follow the vehicle’s '
                                      'maintenance instructions rather than ignoring the warning.')),
            ('Low oil level', P('If the dipstick shows that the oil level is below the recommended range, the engine may need attention. '
                                'Low oil can result from consumption or a leak.')),
            ('Unusual engine noise', P('Insufficient or degraded lubrication can contribute to engine noise. However, knocking, ticking or '
                                       'other unusual sounds can have several causes and should not automatically be treated as a routine '
                                       'oil-change issue.')),
            ('Visible oil leaks', P('Oil spots under your parked vehicle may indicate a leak from the engine or another component. Adding '
                                    'fresh oil will not fix the underlying problem.')),
        ], True, P('<strong>If your oil pressure warning light comes on while driving, safely stop the vehicle and switch off the engine as '
                   'soon as possible.</strong> Continuing to drive with low oil pressure can cause serious engine damage. Arrange an '
                   'inspection rather than assuming an oil change alone will solve the issue.')),
        ('rich', 'Choosing the Correct Engine Oil for Your Car', P(
            'The oil recommended for one vehicle may not be suitable for another. Two cars from the same manufacturer can require different '
            'oil grades depending on their engine design and model year.', 'Before selecting engine oil, consider these factors:')
         + UL('<strong>Oil viscosity:</strong> The grade, such as 0W-20 or 5W-30, describes how the oil flows under different temperature '
              'conditions.',
              '<strong>Manufacturer specifications:</strong> Some engines require oil that meets particular industry or manufacturer '
              'standards.',
              '<strong>Engine type:</strong> Turbocharged, naturally aspirated, hybrid and other engine designs can have different '
              'lubrication requirements.',
              '<strong>Vehicle mileage and condition:</strong> An older engine may have different maintenance considerations, but its '
              'original specifications still matter.',
              '<strong>Climate and driving habits:</strong> Temperature and driving patterns can influence maintenance needs.')
         + P('Using thicker or thinner oil simply because of the weather is not always the right decision. The safest approach is to use oil '
             'that meets the specifications listed by your vehicle manufacturer.')),
        ('rich', 'Oil Change Services for Calgary Drivers', P(
            'Calgary’s weather can change significantly throughout the year. Winter temperatures can make cold starts more demanding, while '
            'summer driving and heavy traffic can place additional demands on a vehicle.',
            'Regular maintenance helps you stay ahead of common vehicle issues throughout these seasonal changes.',
            'Before winter, it is useful to check your oil level, battery condition, coolant and other essential maintenance items. During '
            'warmer months, regular inspections can help identify leaks, worn components and fluid-related concerns.',
            'An oil change is also a good opportunity to review other maintenance needs. For example, if your vehicle has unusual vibrations '
            'or uneven tyre wear, you may benefit from a separate ' + A('wheel alignment', 'alignment') + ' inspection. If you notice '
            'squealing or reduced braking performance, have the ' + A('brake system', 'brakes') + ' checked rather than assuming an oil '
            'service will address the issue.',
            'Our goal is to help you understand your vehicle’s maintenance needs so you can make informed decisions about its care.'),
         'busy-bee-repair-bay-calgary'),
        ('rich', 'Why Choose Busy Bee Auto Repair for an Oil Change in Calgary?', P(
            'Routine maintenance should be straightforward. You should know what service your vehicle needs, what oil is being used and what '
            'the expected cost will be.',
            'At Busy Bee Auto Repair, we focus on practical vehicle maintenance and clear communication.')
         + UL('<strong>Synthetic oil options:</strong> Mobil 1 synthetic oil changes are available starting at $75.',
              '<strong>Vehicle-specific recommendations:</strong> Oil selection is based on your vehicle’s requirements.',
              '<strong>Free multi-point inspection:</strong> Get an additional look at visible maintenance concerns during your visit.',
              '<strong>Upfront estimates:</strong> Understand the expected service cost before additional work is carried out.',
              '<strong>Convenient Calgary location:</strong> Visit our workshop at 324 41 Ave NE, Calgary.',
              '<strong>Walk-ins welcome:</strong> You can visit during regular business hours or contact us to arrange your service.')
         + P('We also provide other automotive services, including ' + A('engine repair', 'engine') + ', ' + A('brake repair', 'brakes') +
             ' and ' + A('tire services', 'tires') + ', helping drivers address different vehicle maintenance needs in one workshop.')),
        ('callout', 'Book Your Oil Change in Calgary',
         'Do not wait for an engine warning or unusual noise before checking your vehicle’s maintenance schedule. Regular oil changes help '
         'maintain proper lubrication and support the long-term care of your engine. Whether you need a synthetic oil change, conventional '
         'oil service or help choosing the correct lubricant, Busy Bee Auto Repair is here to help.<br><br><strong>Visit Busy Bee Auto '
         'Repair</strong> – 324 41 Ave NE, Calgary, AB T2E 2N3 · Phone: <a href="tel:+14039305888">(403) 930-5888</a> · Alternate phone: '
         '<a href="tel:+18255401995">(825) 540-1995</a> · Email: <a href="mailto:busybeeautocalgary@gmail.com">busybeeautocalgary@gmail.com'
         '</a> · Hours: Monday to Friday, 9:00 AM to 6:00 PM. Call our team or visit the workshop to discuss your vehicle’s oil-change '
         'requirements.'),
    ],
    faqs=[
        ('How much does an oil change cost in Calgary?', 'The cost depends on your vehicle’s engine, oil capacity, oil type and filter '
         'requirements. Busy Bee Auto Repair offers Mobil 1 synthetic oil changes starting at $75. Contact the workshop to confirm pricing '
         'for your specific vehicle.'),
        ('How often should I get an oil change?', 'Follow the mileage and time intervals recommended in your owner’s manual. The correct '
         'interval varies by vehicle, engine type, oil specification and driving conditions.'),
        ('Is synthetic oil better than conventional oil?', 'Synthetic oil is designed for consistent performance across different '
         'temperatures and may offer advantages in certain engines. However, the best option is the oil that meets your vehicle '
         'manufacturer’s specifications.'),
        ('Can I switch from conventional oil to synthetic oil?', 'In many vehicles, switching to synthetic oil is acceptable if the oil meets '
         'the required viscosity and manufacturer specifications. Check your owner’s manual or ask a technician before changing oil types.'),
        ('What happens if I delay an oil change?', 'Old engine oil can lose some of its lubricating and cleaning effectiveness. Delaying '
         'maintenance for too long may increase engine wear and contribute to deposits or mechanical problems.'),
        ('Does an oil change include an oil filter replacement?', 'An oil filter replacement is normally part of a complete oil change. The '
         'filter helps capture contaminants, so replacing it helps maintain proper oil filtration.'),
        ('What does the oil pressure warning light mean?', 'It can indicate that the engine is not receiving adequate oil pressure. Stop '
         'safely and switch off the engine as soon as possible. Continuing to drive may cause serious damage. Have the vehicle inspected '
         'before driving again.'),
        ('Can I get an oil change without an appointment?', 'Busy Bee Auto Repair welcomes walk-ins. You can also call ahead to check '
         'availability and discuss your vehicle’s service requirements.'),
        ('Does Busy Bee Auto Repair offer synthetic oil changes?', 'Yes. Mobil 1 synthetic oil changes are available starting at $75. The '
         'final cost depends on the vehicle and its oil requirements.'),
        ('Where can I get an oil change near NE Calgary?', 'Busy Bee Auto Repair is located at 324 41 Ave NE, Calgary, AB T2E 2N3. Call '
         '(403) 930-5888 to ask about oil change availability or visit the workshop during business hours.'),
    ],
)

OVERRIDES = {'engine': ENGINE, 'brakes': BRAKES, 'oil': OIL}
