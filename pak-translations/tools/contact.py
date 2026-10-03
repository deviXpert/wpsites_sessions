"""Contact Us (page 706). Form keeps the original recipient (hr@pak-translations.com)."""
from lib import *
TITLE = 'Contact Us'
SEO = ('Contact Pak Translations | Translation Agency in Gujrat, Pakistan',
       'Contact Pak Translations for a free translation quote. WhatsApp +92 337 1440929, email info@pak-translations.com or visit our office in Gujrat, Punjab, Pakistan.',
       'contact translation agency')

def build():
    seed('contact')
    hero = phero('Contact Us', 'Contact <span class="x-hl">Pak Translations</span>',
                 'We will be happy to serve you. Message us on WhatsApp, send an email or fill out the form — our team responds quickly.', [])
    cards = C([
        IBOX('fab fa-whatsapp', 'WhatsApp / Call', PHONE, 'x-card x-svc x-nomore', WA, 'h2'),
        IBOX('envelope-open-text', 'Email Us', EMAIL, 'x-card x-svc x-nomore', 'mailto:' + EMAIL, 'h2'),
        IBOX('map-marker-alt', 'Visit Us', 'Behind Zamindara Bank, Mohallah Fattupura, Gujrat 50700, Punjab, Pakistan', 'x-card x-svc x-nomore', 'https://www.google.com/maps/search/?api=1&query=' + ADDRESS.replace(' ', '+'), 'h2'),
        IBOX('user-check', 'ProZ.com', 'View our verified profile', 'x-card x-svc x-nomore', PROZ, 'h2'),
    ], 'x-g4 x-contact-cards rv-st', 'grid')
    info = C([cards], 'x-stats x-contact-wrap', box=True)
    form = FORM('Contact Form', [
        F('name', 'text', 'Full name', 'Your name', True, '50'), F('email', 'email', 'Email address', 'you@example.com', True, '50'),
        F('phone', 'tel', 'Phone / WhatsApp', '+92 ...', False, '50'), F('subject', 'text', 'Subject', 'e.g. Urdu to English certificate', False, '50'),
        F('message', 'textarea', 'Message', 'How can we help?', True, '100', rows='5'),
    ], 'Send Message', to='hr@pak-translations.com', subject='New contact message — Pak Translations website')
    main = sec([C([
        C([EB('Send a Message'), H('Let\'s Talk About <span class="x-hl">Your Project</span>', 'h2', 'x-title'),
           P('Tell us what you need translated, the languages involved and your deadline. For an instant reply, WhatsApp us — or use our detailed order form to upload files.', 'x-lead'),
           ILIST([(f'{ADDRESS}', 'map-marker-alt'), (PHONE, 'fab fa-whatsapp', WA), (EMAIL, 'envelope', 'mailto:' + EMAIL)], 'x-checks x-checks-1 x-contact-list'),
           W('social-icons', 'x-social x-social-dark', social_icon_list=[
               {'_id': rid(), 'social_icon': ICO('fab fa-facebook-f'), 'link': LNK(FB, True)}, {'_id': rid(), 'social_icon': ICO('fab fa-twitter'), 'link': LNK(TW, True)},
               {'_id': rid(), 'social_icon': ICO('fab fa-whatsapp'), 'link': LNK(WA, True)}], shape='rounded'),
           C([BTN('Place a Detailed Order', U + '/your-order/', 'x-btn x-btn-g')], 'x-btns', 'row')], 'x-faq-side rv'),
        C([form], 'x-form-card rv'),
    ], 'x-faq-wrap', 'row')])
    gmap = sec([W('google_maps', 'x-map rv', address='Mohallah Fattupura, Gujrat 50700, Punjab, Pakistan', zoom={'unit': 'px', 'size': 15}, height={'unit': 'px', 'size': 440})], 'x-map-sec')
    return [hero, info, main, gmap]
