"""Single source of truth for the Busy Bee page tree (URLs from design/content-seo.md → "Site structure").
Menus, footers, service cards and cross-links all read from here."""

# key, menu label, URL, Lucide icon, one-line summary, card photo (media.json key)
SERVICE_PAGES = [
    ('engine', 'Engine Repair', '/engine-repair-calgary/', 'settings-2', 'Check engine lights, misfires, leaks and timing belts.',
     'engine-repair-audi-calgary'),
    ('brakes', 'Brake Repair', '/brake-repair-calgary/', 'disc-3', 'Pads, rotors, calipers and brake fluid service.',
     'brake-repair-calgary'),
    ('oil', 'Oil Change', '/oil-change-calgary/', 'droplets', 'Mobil 1 synthetic from $75, with a free inspection.',
     'mobil-1-synthetic-oil-change-calgary'),
    ('tires', 'Tire Shop', '/tire-shop-calgary/', 'circle-dashed', 'New and used tires, repair, rotation and balancing.',
     'winter-tire-change-calgary'),
    ('alignment', 'Wheel Alignment', '/wheel-alignment-calgary/', 'gauge', 'Stop pulling, straighten the wheel, save your tires.',
     'busy-bee-service-bays-calgary'),
    ('battery', 'Battery & Alternator', '/car-battery-replacement-calgary/', 'battery-charging',
     'Free battery testing and charging-system checks.', 'battery-alternator-service-calgary'),
    ('electrical', 'Electrical & Diagnostics', '/auto-electrical-diagnostics-calgary/', 'circle-gauge',
     'Warning lights, wiring, starters and sensors.', 'computer-diagnostics-calgary'),
    ('suspension', 'Suspension & Steering', '/suspension-repair-calgary/', 'waves', 'Shocks, struts, ball joints, tie rods and bearings.',
     'brake-repair-calgary'),
    ('transmission', 'Transmission Repair', '/transmission-repair-calgary/', 'unplug', 'Fluid service, diagnosis and repair.',
     'busy-bee-repair-bay-calgary'),
    ('cooling', 'Radiator & Cooling', '/radiator-repair-calgary/', 'snowflake', 'Radiators, water pumps, thermostats and flushes.',
     'computer-diagnostics-calgary'),
    ('maintenance', 'Car Maintenance', '/car-maintenance-calgary/', 'clipboard-check',
     'Scheduled service, tune-ups and seasonal inspections.', 'busy-bee-repair-bay-calgary'),
]
SVC_URL = {k: url for k, _, url, *_ in SERVICE_PAGES}

PAGES = [('Home', '/'), ('Services', '/services/'), ('About', '/about-us/'), ('Blog', '/blog/'), ('Contact', '/contact-us/')]
URL = dict((t.lower(), u) for t, u in PAGES)
