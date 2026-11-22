"""Make a dealership's QR code for showroom displays. Each points to /book/?dealer=<slug>, so bookings record the dealer
(and their £150 referral fee can be tracked). Outputs print-ready SVG (scales to any size) and a 1200px PNG.
Usage: python3 make_dealer_qr.py "Smith Motors" ["Another Dealer" ...]   -> ../marketing/qr/<slug>.svg/.png"""
import os
import re
import sys

import qrcode
import qrcode.image.svg

OUT = os.path.join(os.path.dirname(__file__), '..', 'marketing', 'qr')
os.makedirs(OUT, exist_ok=True)

for name in sys.argv[1:] or ['website']:
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:60]
    url = f'https://evtron.co.uk/book/?dealer={slug}'
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=2)
    qr.add_data(url); qr.make(fit=True)
    qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(os.path.join(OUT, f'{slug}.svg'))
    img = qr.make_image(fill_color='#0B0F14', back_color='white').resize((1200, 1200))
    img.save(os.path.join(OUT, f'{slug}.png'))
    print(slug, '->', url)
