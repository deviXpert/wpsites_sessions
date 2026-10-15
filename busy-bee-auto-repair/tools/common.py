"""Shared constants for the Busy Bee builders."""
from el import *

INK = '#1A2024'
BEE = '#F7D710'
YEL = '#FFE600'
PAPER = '#FFFFFF'
PITCH = '#010101'
SOFT = '#FCF5DB'
GREY = '#E5E8EA'


def ink(a):
    """Ink colour at alpha a (0..1) as rgba – Tailwind's text-ink/55 etc."""
    return f'rgba(26,32,36,{a})'


def wht(a):
    return f'rgba(255,255,255,{a})'


PHONE = '(403) 930-5888'
TEL = 'tel:+14039305888'
PHONE2 = '(825) 540-1995'
TEL2 = 'tel:+18255401995'
EMAIL = 'busybeeautocalgary@gmail.com'
GBP_PLACE_ID = 'ChIJVUUo4XplcVMRCH6YcMDI9uU'  # Busy Bee Auto Repair – Google Business Profile
MAPS = 'https://www.google.com/maps/search/?api=1&query=Busy+Bee+Auto+Repair+324+41+Ave+NE+Calgary&query_place_id=' + GBP_PLACE_ID
WHATSAPP = "https://wa.me/14039305888?text=Hi%20Busy%20Bee%2C%20I'd%20like%20to%20ask%20about%20service%20for%20my%20vehicle."
FACEBOOK = 'https://www.facebook.com/profile.php?id=61575647326309'  # linked from busybeeauto.ca
INSTAGRAM = 'https://www.instagram.com/busybee_autorepair/'
REVIEWS = 'https://www.google.com/maps/place/?q=place_id:' + GBP_PLACE_ID
BOOK = '#book'

# Service detail pages don't exist yet: link to the services section until they are built.
from sitemap import SVC_URL as _U
SVC = {'engine': _U['engine'], 'battery': _U['battery'], 'brakes': _U['brakes'], 'suspension': _U['suspension'],
       'cooling': _U['cooling'], 'tires': _U['tires'], 'oil-change': _U['oil'], 'diagnostics': _U['electrical'],
       'transmission': _U['transmission'], 'alignment': _U['alignment'], 'maintenance': _U['maintenance']}

SH_SM = shadow(0, 1, 3, 0, 'rgba(0,0,0,0.1)')       # tailwind shadow-sm (first layer)
SH_LG = shadow(0, 10, 15, -3, 'rgba(0,0,0,0.1)')    # tailwind shadow-lg (first layer)
SH_INK = shadow(0, 8, 24, 0, 'rgba(26,32,36,0.18)')
SH_BEE = shadow(0, 8, 24, 0, 'rgba(26,32,36,0.14)')

PILL = 9999


def M(size=None, weight=None, lh=None, ls=None, tt=None, **kw):
    """Manrope typography."""
    return typo(ff='Manrope', size=size, weight=weight, lh=lh, ls=ls, tt=tt, **kw)


def S(size=None, weight=None, lh=None, ls=None, tt=None, **kw):
    """System font stack typography (inherits <body>)."""
    return typo(ff=None, size=size, weight=weight, lh=lh, ls=ls, tt=tt, **kw)
