"""Your Order (page 319). Elementor Pro order form (original fields, cleaned)."""
from lib import *
TITLE = 'Place Your Order'
SEO = ('Order Translation Online | Free Quote | Pak Translations',
       'Place your translation order online: upload documents, choose source and target languages and set your deadline. Certified and professional translation in 120+ languages.',
       'order translation online')

def build():
    seed('order')
    hero = phero('Place Your Order', 'Place Your <span class="x-hl">Translation Order</span>',
                 'Share a few details about your project and upload your files — we will confirm the price and deadline before any work begins.', [BTN('Start Your Order', '#order-form', 'x-btn', 'arrow-down')])
    form = FORM('Translation Order', [
        F('client_type', 'select', 'Individual or business', '', True, '50', field_options='Individual\nBusiness / Organisation'),
        F('name', 'text', 'Name &amp; designation', 'Your name (and role)', True, '50'),
        F('email', 'email', 'Email', 'you@example.com', True, '50'), F('phone', 'tel', 'Contact number', '+92 ...', True, '50'),
        F('source_language', 'text', 'Source language(s)', 'e.g. Urdu', True, '50'), F('target_language', 'text', 'Target language(s)', 'e.g. English', True, '50'),
        F('service', 'select', 'Service required', '', False, '50', field_options='Certified translation\nDocument translation\nLocalization\nEditing & proofreading\nTranscription\nSubtitling\nInterpreting\nContent writing\nLanguage test / material development\nLinguistic services\nDesktop publishing (DTP)\nOther'),
        F('domain', 'text', 'Domain / content', 'Medical, legal, IT, personal...', False, '50'),
        F('deadline', 'date', 'Deadline', '', False, '50'),
        F('certified', 'select', 'Need certification / affidavit?', '', False, '50', field_options='No\nYes - certified translation\nYes - with translator affidavit\nNot sure'),
        F('message', 'textarea', 'Order details', 'Describe your requirements: purpose, format, word count, special instructions...', False, '100', rows='5'),
        F('files', 'upload', 'Upload supporting files (up to 6)', '', False, '100'),
    ], 'Place Order', subject='New translation order — Pak Translations website')
    steps = [('paper-plane', 'Submit your order', 'Fill out the form and upload your files.'),
             ('file-invoice-dollar', 'Get confirmation', 'We confirm price and deadline — no surprises.'),
             ('user-tie', 'We translate &amp; QA', 'A native linguist translates; our QA team checks.'),
             ('check-double', 'Receive your files', 'Delivered on time, with post-delivery support.')]
    main = sec([C([
        C([EB('How Ordering Works'), H('Simple, Secure &amp; <span class="x-hl">Transparent</span>', 'h2', 'x-title'),
           C([IBOX(i, t, d, 'x-feat', tag='h3', position='left') for i, t, d in steps], 'x-feats rv-st'),
           C([IBOX('fab fa-whatsapp', 'Prefer to chat?', f'WhatsApp us on {PHONE} or email {EMAIL}', 'x-media-badge x-inline-badge', WA, 'p')], 'x-dc')], 'x-faq-side rv'),
        C([form], 'x-form-card rv'),
    ], 'x-faq-wrap', 'row')], _element_id='order-form')
    return [hero, main]
