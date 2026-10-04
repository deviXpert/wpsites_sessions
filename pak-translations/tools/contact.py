"""Contact Us (page 706). Form keeps the original recipient (hr@pak-translations.com).
Per client: no address/location, no WhatsApp, no ProZ, no cards/map — only phone, email and the form."""
from lib import *
TITLE = 'Contact Us'
SEO = ('Contact Pak Translations | Get a Free Translation Quote',
       'Contact Pak Translations for a free translation quote. Call +92 337 1440929, email info@pak-translations.com or send us a message using the contact form.',
       'contact translation agency')

def build():
    seed('contact')
    hero = phero('Contact Us', 'Contact <span class="x-hl">Pak Translations</span>',
                 'We will be happy to serve you. Send us an email or fill out the form — our team responds quickly.', [])
    form = FORM('Contact Form', [
        F('name', 'text', 'Full name', 'Your name', True, '50'), F('email', 'email', 'Email address', 'you@example.com', True, '50'),
        F('phone', 'tel', 'Phone number', '+92 ...', False, '50'), F('subject', 'text', 'Subject', 'e.g. Document translation', False, '50'),
        F('message', 'textarea', 'Message', 'How can we help?', True, '100', rows='5'),
    ], 'Send Message', to='hr@pak-translations.com', subject='New contact message — Pak Translations website')
    main = sec([C([
        ILIST([(PHONE, 'phone-alt', TEL), (EMAIL, 'envelope', 'mailto:' + EMAIL)], 'x-contact-inline rv', 'inline'),
        C([form], 'x-form-card rv'),
    ], 'x-contact-main')], 'x-contact-sec')
    return [hero, main]
