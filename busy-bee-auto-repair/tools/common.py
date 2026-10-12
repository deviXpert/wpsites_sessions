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
MAPS = 'https://maps.google.com/?q=324+41+Ave+NE+Calgary+AB+T2E+2N3'
WHATSAPP = "https://wa.me/14039305888?text=Hi%20Busy%20Bee%2C%20I'd%20like%20to%20ask%20about%20service%20for%20my%20vehicle."
INSTAGRAM = 'https://www.instagram.com/busybee_autorepair/'
REVIEWS = 'https://www.google.com/search?q=Busy+Bee+Auto+Repair+Calgary+reviews'
BOOK = '#book'

# Service detail pages don't exist yet: link to the services section until they are built.
SVC = {k: '#services' for k in ('engine', 'battery', 'brakes', 'suspension', 'cooling', 'tires', 'oil-change',
                                 'diagnostics', 'transmission')}

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
