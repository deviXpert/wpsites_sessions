"""Shared Elementor JSON helpers + site-wide header/footer for the Pak Translations redesign.
Only core Elementor / Elementor Pro widgets are used (no third-party addons)."""
import json, random, os, copy
D = os.path.dirname(os.path.abspath(__file__))
U = 'https://pak-translations.com'
UP = U + '/wp-content/uploads/'
PHONE, TEL, WA = '+92 337 1440929', 'tel:+923371440929', 'https://wa.me/923371440929'
EMAIL = 'info@pak-translations.com'
ADDRESS = 'B-14/16-C, Street No. 2, Behind Zamindara Bank, Mohallah Fattupura, Gujrat 50700, Punjab, Pakistan'
FB, TW, PROZ = 'https://www.facebook.com/PakTranslationsCompany', 'https://twitter.com/TranslationsPak', 'https://www.proz.com/profile/1415308'
MEDIA = {m['source_url']: m['id'] for m in json.load(open(os.path.join(D, 'wp-backup/media.json')))}

def seed(s): random.seed(s)
def rid(): return '%07x' % random.getrandbits(28)
def z(): return {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
def ICO(v, lib='fa-solid'):
    if v.startswith('fab '): return {'value': v, 'library': 'fa-brands'}
    if v.startswith('far '): return {'value': v, 'library': 'fa-regular'}
    return {'value': 'fas fa-' + v if not v.startswith('fas ') else v, 'library': 'fa-solid'}
def LNK(u, ext=False): return {'url': u, 'is_external': 'on' if ext else '', 'nofollow': '', 'custom_attributes': ''}

def C(els, cls='', d='col', box=False, **s):
    """Container. d='row'|'col'|'grid'. Layout comes from our own classes so pages never depend on generated CSS."""
    extra = {'row': 'x-dr', 'col': 'x-dc', 'grid': 'x-grid'}[d] + (' x-bx' if box else '') + ' e-no-lazyload'
    st = {'content_width': 'boxed' if box else 'full', 'flex_direction': 'row' if d == 'row' else 'column',
          'padding': z(), 'margin': z(), 'css_classes': (cls + ' ' + extra).strip(),
          'flex_gap': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'isLinked': True}}
    if d == 'row': st['flex_wrap'] = 'nowrap'
    st.update(s)
    return {'id': rid(), 'elType': 'container', 'isInner': False, 'settings': st, 'elements': els}
def W(t, cls='', **s):
    if cls: s['_css_classes'] = cls
    return {'id': rid(), 'elType': 'widget', 'widgetType': t, 'isInner': False, 'settings': s, 'elements': []}
def H(t, tag='h2', cls=''): return W('heading', ('x-h ' + cls).strip(), title=t, header_size=tag)
def T(html, cls=''): return W('text-editor', ('x-t ' + cls).strip(), editor=html)
def P(t, cls=''): return T(f'<p>{t}</p>', cls)
def EB(t): return P(t, 'x-eyebrow')
def BTN(t, url, cls='x-btn', icon='arrow-right', after=True, ext=False):
    return W('button', cls, text=t, link=LNK(url, ext), selected_icon=ICO(icon), icon_align='row-reverse' if after else 'row',
             icon_indent={'unit': 'px', 'size': 10})
def IMG(url, cls='', alt='', size='large', link=None):
    s = dict(image={'url': url, 'id': MEDIA.get(url, ''), 'alt': alt}, image_size=size)
    if link: s.update(link_to='custom', link=LNK(link))
    return W('image', cls, **s)
def IBOX(icon, title, desc, cls='', link=None, tag='h3', position='top'):
    s = dict(selected_icon=ICO(icon) if isinstance(icon, str) else icon, title_text=title, description_text=desc, title_size=tag, position=position)
    if link: s['link'] = LNK(link)
    return W('icon-box', cls, **s)
def ILIST(items, cls='', view='traditional'):
    """items: list of (text, icon or None, url or None)"""
    out = []
    for it in items:
        t, ic, u = (list(it) + [None, None])[:3]
        r = {'_id': rid(), 'text': t, 'selected_icon': ICO(ic) if ic else {'value': '', 'library': ''}}
        if u: r['link'] = LNK(u, u.startswith('http') and 'pak-translations.com' not in u)
        out.append(r)
    return W('icon-list', cls, icon_list=out, view=view)
def RAW(h, cls=''): return W('html', cls, html=h)
def sec(els, cls='', d='col', **kw): return C(els, ('x-sec ' + cls).strip(), d, box=True, **kw)
def head(eb, title, lead=None, center=True, tag='h2'):
    els = [EB(eb), H(title, tag, 'x-title')] + ([P(lead, 'x-lead')] if lead else [])
    return C(els, 'x-head rv' + (' x-center' if center else ''))

# ---------- Elementor Pro form ----------
def F(cid, ftype, label, ph='', req=False, width='100', **kw):
    f = {'_id': rid(), 'custom_id': cid, 'field_type': ftype, 'field_label': label, 'placeholder': ph,
         'required': 'true' if req else '', 'width': width}
    if ftype == 'upload':
        f.update(file_sizes='10', file_types='pdf,doc,docx,xls,xlsx,ppt,pptx,txt,rtf,jpg,jpeg,png,zip', allow_multiple_upload='yes', max_files='6')
    f.update(kw)
    return f
def FORM(name, fields, button, to=EMAIL, subject=None, cls='x-form', labels=True):
    return W('form', cls, form_name=name, form_fields=fields, button_text=button, show_labels='yes' if labels else '',
             input_size='md', button_size='md', button_width='100', selected_button_icon=ICO('paper-plane'), button_icon_align='row-reverse',
             button_icon_indent={'unit': 'px', 'size': 10}, submit_actions=['email'], email_to=to,
             email_subject=subject or f'New enquiry: {name} — Pak Translations', email_content='[all-fields]',
             email_from='email@pak-translations.com', email_from_name='Pak Translations', email_reply_to='email',
             success_message='Thank you! Your message has been sent — our team will get back to you shortly.',
             error_message='Sorry, something went wrong. Please email us at info@pak-translations.com.',
             required_field_message='This field is required.', invalid_message='Please check the highlighted field.',
             mark_required='yes')
def quote_form(cls='x-form', labels=False):
    return FORM('Free Translation Quote', [
        F('name', 'text', 'Full name', 'Full name *', True, '50'),
        F('email', 'email', 'Email address', 'Email address *', True, '50'),
        F('phone', 'tel', 'Phone / WhatsApp', 'Phone / WhatsApp', False, '100'),
        F('source_language', 'text', 'Translate from', 'From (e.g. Urdu)', True, '50'),
        F('target_language', 'text', 'Translate to', 'To (e.g. English)', True, '50'),
        F('files', 'upload', 'Upload documents (optional)', '', False, '100'),
        F('message', 'textarea', 'Project details', 'Tell us about your document, deadline or certification needs', False, '100', rows='3'),
    ], 'Get My Free Quote', subject='New quote request — Pak Translations website', cls=cls, labels=labels)

# ---------- assets: fonts, CSS, JS (live in the header so they load site-wide) ----------
def assets():
    css = open(os.path.join(D, 'pt.css')).read()
    js = open(os.path.join(D, 'pt.js')).read()
    return RAW('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
               '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap">'
               f'<style id="pt-css">{css}</style><script>{js}</script>', 'x-assets')

LOGO = UP + '2020/10/logo.png'
NAV = dict(menu='menu', layout='horizontal', pointer='none', dropdown='tablet', toggle='burger', full_width='stretch',
           text_align='aside', toggle_align='right', submenu_icon=ICO('chevron-down'), _css_classes='x-nav')

def header():
    seed('header')
    top = C([
        ILIST([('Certified translation in 120+ languages', 'certificate'), ('Gujrat, Pakistan · Serving clients worldwide', 'globe-asia', None)], 'x-top-l x-top-hide', 'inline'),
        ILIST([(EMAIL, 'envelope', 'mailto:' + EMAIL), (PHONE, 'fab fa-whatsapp', WA)], 'x-top-r', 'inline'),
    ], 'x-top', 'row', box=True)
    bar = C([
        IMG(LOGO, 'x-logo', 'Pak Translations logo', 'thumbnail', U + '/'),
        W('nav-menu', **NAV),
        BTN('Get a Quote', U + '/your-order/', 'x-btn x-btn-sm x-hcta', 'arrow-right'),
    ], 'x-bar', 'row', box=True, sticky='top', sticky_on=['desktop', 'tablet', 'mobile'], sticky_effects_offset=60)
    return C([assets(), top, bar], 'x-hdr')

SERVICES = [
    ('localization', 'Website & App Localization', 'globe'),
    ('document-translation', 'Document Translation', 'file-alt'),
    ('certified-translation', 'Certified Translation', 'stamp'),
    ('editing-proofreading', 'Editing & Proofreading', 'spell-check'),
    ('transcription', 'Audio & Video Transcription', 'headphones'),
    ('interpreting', 'Interpreting', 'comments'),
    ('subtitling', 'Subtitling & Captioning', 'closed-captioning'),
    ('content-creation', 'Content Writing', 'pen-nib'),
    ('language-material', 'Language Test & Material Development', 'graduation-cap'),
    ('linguistics', 'Linguistic Services', 'project-diagram'),
    ('desktop-publishing', 'Desktop Publishing (DTP)', 'object-group'),
]

def footer():
    seed('footer')
    cta = C([H('Have a document to translate? <span class="x-hl">Get a free quote today.</span>', 'h2'),
             C([BTN('Place an Order', U + '/your-order/', 'x-btn'), BTN('Chat on WhatsApp', WA, 'x-btn x-btn-o', 'fab fa-whatsapp', False, True)], 'x-btns', 'row')],
            'x-fcta', 'row', box=True)
    grid = C([
        C([IMG(LOGO, 'x-flogo', 'Pak Translations', 'medium', U + '/'),
           P('Pak Translations is a PhD-led translation company in Gujrat, Pakistan, delivering certified translation, localization, transcription and subtitling in 120+ Asian, European and African languages.'),
           W('social-icons', 'x-social', social_icon_list=[
               {'_id': rid(), 'social_icon': ICO('fab fa-facebook-f'), 'link': LNK(FB, True), 'item_icon_secondary_color': '#fff'},
               {'_id': rid(), 'social_icon': ICO('fab fa-twitter'), 'link': LNK(TW, True)},
               {'_id': rid(), 'social_icon': ICO('fab fa-whatsapp'), 'link': LNK(WA, True)},
               {'_id': rid(), 'social_icon': ICO('globe'), 'link': LNK(PROZ, True)}], shape='rounded', icon_size={'unit': 'px', 'size': 16})], 'x-fcol'),
        C([H('Services', 'p', 'x-fhead'), ILIST([(n, None, f'{U}/services/#{s}') for s, n, _ in SERVICES[:7]], 'x-flinks')], 'x-fcol'),
        C([H('Company', 'p', 'x-fhead'), ILIST([('About Us', None, U + '/about-us/'), ('Languages', None, U + '/languages/'), ('Sample Projects', None, U + '/sample/'),
                                                 ('Careers', None, U + '/career/'), ('Place an Order', None, U + '/your-order/'), ('Contact Us', None, U + '/contact-us/')], 'x-flinks')], 'x-fcol'),
        C([H('Get in Touch', 'p', 'x-fhead'), ILIST([(PHONE, 'fab fa-whatsapp', WA), (EMAIL, 'envelope', 'mailto:' + EMAIL),
                                                     ('ProZ.com profile', 'user-check', PROZ), (ADDRESS, 'map-marker-alt', None)], 'x-flinks')], 'x-fcol'),
    ], 'x-fgrid', box=True)
    bot = C([P('© 2026 Pak Translations. All rights reserved.'), P('Powered by <a href="https://hafizahsanali.com" target="_blank" rel="noopener">hafizahsanali.com</a>', 'x-credit')], 'x-fbot', 'row', box=True)
    wa = W('icon', 'x-wa', selected_icon=ICO('fab fa-whatsapp'), link=LNK(WA, True), view='default', **{'_attributes': ''})
    return C([cta, grid, bot, wa], 'x-ftr')

# ---------- shared page sections ----------
def phero(crumb, h1, lead, btns=None):
    """Inner-page hero with breadcrumb + the page's single H1."""
    els = [P(f'<a href="{U}/">Home</a> &nbsp;/&nbsp; {crumb}', 'x-crumbs rv'), H(h1, 'h1', 'rv'), P(lead, 'x-lead rv')]
    if btns is None:
        btns = [BTN('Get a Free Quote', U + '/your-order/', 'x-btn'), BTN('WhatsApp Us', WA, 'x-btn x-btn-o', 'fab fa-whatsapp', False, True)]
    if btns: els.append(C(btns, 'x-btns rv', 'row'))
    return C(els, 'x-phero x-center', box=True)

def split(media, copy_els, rev=False, cls=''):
    """media: list of widgets for the media column; copy_els: widgets for the text column."""
    return C([C(media, 'x-media rv ' + ('rv-r' if rev else 'rv-l')), C(copy_els, 'x-split-copy rv')],
             'x-split' + (' x-split-rev' if rev else '') + (' ' + cls if cls else ''), 'row')

def faq_sec(faqs, lead='Quick answers to common questions. Still curious? Our team replies fast on WhatsApp.', title='Frequently Asked <span class="x-hl">Questions</span>', bg=''):
    return sec([C([
        C([EB('FAQs'), H(title, 'h2', 'x-title'), P(lead, 'x-lead'), BTN('Ask on WhatsApp', WA, 'x-btn x-btn-g', 'fab fa-whatsapp', False, True)], 'x-faq-side rv'),
        W('accordion', 'x-faq rv', tabs=[{'_id': rid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faqs], faq_schema='yes', title_html_tag='h3',
          selected_icon=ICO('plus'), selected_active_icon=ICO('minus'), icon_align='right'),
    ], 'x-faq-wrap', 'row')], bg)

def cta_sec(title='Ready to Reach a Global Audience?', text='Tell us what you need translated — we will match you with the right linguist and send a free quote.', primary=('Get a Free Quote', None)):
    return sec([C([H(title, 'h2'), P(text),
                   C([BTN(primary[0], primary[1] or U + '/your-order/', 'x-btn'), BTN('Call / WhatsApp ' + PHONE, WA, 'x-btn x-btn-ol', 'fab fa-whatsapp', False, True)], 'x-btns', 'row')],
                  'x-cta rv rv-s')], 'x-center x-cta-sec')

def steps_sec(eb, title, lead, steps, dark=True):
    s = sec([head(eb, title, lead), C([IBOX(i, t, d, 'x-step', tag='h3') for i, t, d in steps], f'x-steps x-g{3 if len(steps) % 3 == 0 else 4} rv-st', 'grid')])
    return C([s], 'x-dark') if dark else s
