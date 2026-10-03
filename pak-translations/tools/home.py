"""New home page (built from scratch; none of the old page's widgets are reused)."""
import json
from lib import *

def build():
    seed('home')
    hero = C([
        C([
            P('<i class="fas fa-award" aria-hidden="true"></i>&nbsp; PhD-led translation company in Pakistan', 'x-eyebrow rv'),
            H('Professional Translation Services in Pakistan — <span class="x-hl">Accurate, Certified &amp; On Time</span>', 'h1', 'rv'),
            P('Pak Translations is your one-stop language partner. From certified document translation for immigration to website localization, transcription and subtitling, our tested native linguists work in <strong>120+ languages</strong> — and every project is quality-checked before it reaches you.', 'x-lead rv'),
            C([BTN('Get a Free Quote', '#quote', 'x-btn', 'arrow-right'), BTN('WhatsApp Us', WA, 'x-btn x-btn-o', 'fab fa-whatsapp', False, True)], 'x-btns rv', 'row'),
            C([IBOX('language', '120+ Languages', 'Asian, European &amp; African', 'x-chip', tag='p'),
               IBOX('stamp', 'Certified Translation', 'Immigration, legal &amp; academic', 'x-chip', tag='p'),
               IBOX('check-double', 'Two-Step QA', 'Every file reviewed', 'x-chip', tag='p')], 'x-trust rv', 'row'),
        ], 'x-hero-copy'),
        C([H('Get a Free Quote', 'h2', 'x-card-title'),
           P("Send us your document and we'll reply with a clear, no-obligation price.", 'x-card-sub'),
           quote_form()], 'x-hero-card rv rv-r', _element_id='quote'),
    ], 'x-hero', 'row', box=True)

    langs = ['اردو Urdu', 'English', 'العربية Arabic', '中文 Chinese', 'Español', 'Français', 'Deutsch', 'हिन्दी Hindi', 'پښتو Pashto', 'ਪੰਜਾਬੀ Punjabi',
             'فارسی Persian', 'Türkçe', 'Русский', '日本語', '한국어', 'বাংলা Bengali', 'தமிழ் Tamil', 'Kiswahili', 'Italiano', 'Português', 'Bahasa Melayu', 'سنڌي Sindhi']
    track = ''.join(f'<span>{l}</span>' for l in langs)
    marq = C([RAW(f'<div class="x-marq-track" aria-hidden="true">{track}{track}</div>')], 'x-marq')

    stats = C([C([
        W('counter', 'x-stat', starting_number=0, ending_number=10, suffix='+', title='Years of translation expertise', duration=1800),
        W('counter', 'x-stat', starting_number=0, ending_number=120, suffix='+', title='Languages &amp; dialects', duration=2000),
        W('counter', 'x-stat', starting_number=0, ending_number=99, suffix='%', title='Accuracy on large localization projects', duration=2000),
        W('counter', 'x-stat', starting_number=0, ending_number=1, suffix='M+', title='Words localized for one client alone', duration=1200),
    ], 'x-stats-grid x-g4 rv rv-s', 'grid')], 'x-stats', box=True)

    svc_desc = {
        'localization': 'Adapt websites, apps and software for new markets with culturally sensitive localization that respects tags, placeholders and style guides.',
        'document-translation': 'Accurate, readable translation of brochures, contracts, reports, court papers, medical records and more.',
        'certified-translation': 'Certified translations of birth and marriage certificates, degrees and legal papers for embassies and immigration.',
        'editing-proofreading': 'Expert editors make your text error-free, natural-sounding and correctly formatted before it goes live.',
        'transcription': 'Time-coded transcription and translation of interviews, research audio and video — even with background noise.',
        'interpreting': 'Consecutive and simultaneous interpreting in person, over the phone or by video conference.',
        'subtitling': 'Perfectly synced SRT and VobSub subtitles, open or closed captions, soft or hard-coded.',
        'content-creation': 'Persuasive blogs, social posts, ad copy, case studies and email campaigns written for your audience.',
        'language-material': 'Reading, writing and listening tests and practice material for foreign and second-language learners.',
        'linguistics': 'Phonetic transcription, pronunciation validation, PoS tagging and corpus or dictionary building.',
        'desktop-publishing': 'Typesetting, layout and design of translated brochures, flyers and books — ready to print or publish.',
    }
    svc = sec([
        head('Our Services', 'Translation &amp; Language Services <span class="x-hl">Built Around You</span>',
             'Whatever your language need — a single certificate or a multilingual product launch — we match it with a specialist linguist and a rigorous quality process.'),
        C([IBOX(ic, n, svc_desc[s], 'x-card x-svc', f'{U}/services/#{s}') for s, n, ic in SERVICES] +
          [C([H('Not sure what you need?', 'h3'), P('Tell us about your project and we will recommend the right service.'), BTN('Talk to Us', U + '/contact-us/', 'x-btn x-btn-sm')], 'x-card x-card-dark x-dc')],
          'x-g3 rv-st', 'grid'),
    ], 'x-bg')

    why = sec([C([
        C([IMG(UP + '2022/03/workers-considering-term-agreement-min-scaled.jpg', '', 'Pak Translations team reviewing a translation project with a client'),
           IBOX('user-graduate', 'PhD-led team', 'Founded by a translation scholar', 'x-media-badge', tag='p')], 'x-media rv rv-l'),
        C([EB('Why Pak Translations'), H('Why Clients Choose <span class="x-hl">Pak Translations</span>', 'h2', 'x-title'),
           P('We combine academic expertise with real-world project management, so you get translations that are accurate, culturally right and delivered when promised.', 'x-lead'),
           C([IBOX('layer-group', 'A one-stop shop for language needs', 'From document translation to website localization and text-to-speech linguistic data — one partner for every language task.', 'x-feat', tag='h3', position='left'),
              IBOX('user-check', 'Rigorously tested linguists', 'Every linguist passes a skills test before onboarding and follows our Translator Instructions, so quality is consistent on every project.', 'x-feat', tag='h3', position='left'),
              IBOX('headset', 'Support during and after delivery', 'We answer questions quickly — even after office hours — and stay available for post-delivery queries.', 'x-feat', tag='h3', position='left'),
              IBOX('clock', 'On-time delivery, fair prices', 'Deadlines are agreed up front and backed by a team that can step in. Top-quality work, priced to fit your budget.', 'x-feat', tag='h3', position='left')], 'x-feats rv-st'),
        ], 'x-split-copy rv'),
    ], 'x-split', 'row')])

    steps = [('comments', 'Understanding', 'We discuss your requirements, ask questions, request reference material and suggest how to get the best result.'),
             ('file-signature', 'Order', 'You confirm the order through our simple order form, by email or on WhatsApp.'),
             ('user-tie', 'Assignment', 'We assign your project to the most relevant native linguist, who translates and self-proofreads it.'),
             ('search', 'Quality Assurance', 'Our QA team checks formatting, layout, punctuation, terminology and missing lines.'),
             ('paper-plane', 'Delivery', 'Your finished translation is delivered in the format you need — on or before the deadline.'),
             ('hands-helping', 'Post-Delivery Support', 'Need a tweak or have a question? We remain available long after delivery.')]
    how = C([sec([
        head('How It Works', 'A Simple, Transparent <span class="x-hl">Translation Process</span>', 'Six clear steps from first message to final file — so you always know where your project stands.'),
        C([IBOX(i, t, d, 'x-step', tag='h3') for i, t, d in steps], 'x-steps x-g3 rv-st', 'grid'),
    ])], 'x-dark')

    cert = sec([C([
        C([EB('Certified Translation'), H('Certified Translation for <span class="x-hl">Immigration, Visa &amp; Legal</span> Documents', 'h2', 'x-title'),
           P('Applying for a visa, immigration or university abroad? We translate and certify your personal and legal documents so they are ready to submit. On request we can provide a signed translator affidavit and guide you through the notarization process.'),
           C([BTN('Order Certified Translation', U + '/your-order/', 'x-btn'), BTN('Ask a Question', WA, 'x-btn x-btn-o', 'fab fa-whatsapp', False, True)], 'x-btns', 'row')], 'x-band-copy rv'),
        C([ILIST([(t, 'check-circle') for t in ('Birth, marriage &amp; death certificates', 'Degrees, diplomas &amp; transcripts', 'Court orders, wills &amp; contracts',
                                                 'Land records &amp; affidavits', 'Medical reports &amp; claim forms', 'Business &amp; financial documents')], 'x-checks x-checks-1')], 'x-band-side rv rv-r'),
    ], 'x-band', 'row')])

    popular = ['Urdu', 'English', 'Arabic', 'Punjabi', 'Pashto', 'Sindhi', 'Balochi', 'Saraiki', 'Hindi', 'Bengali', 'Persian (Farsi)', 'Dari', 'Turkish', 'Chinese',
               'Japanese', 'Korean', 'French', 'German', 'Spanish', 'Italian', 'Russian', 'Swahili', 'Malay', 'Indonesian']
    lang = sec([C([
        C([EB('Languages'), H('120+ Languages — Including <span class="x-hl">Rare &amp; Regional</span> Ones', 'h2', 'x-title'),
           P('We cover major world languages and hard-to-find regional ones such as Balochi, Saraiki, Hindko, Sylheti and Rohingya — plus non-English pairs like German, French or Spanish into other languages.', 'x-lead'),
           BTN('See All Languages', U + '/languages/', 'x-btn x-btn-g')], 'x-split-copy rv'),
        C([ILIST([(l,) for l in popular], 'x-tags')], 'x-media rv rv-r'),
    ], 'x-split', 'row')], 'x-bg')

    cases = [('1M+', 'Words localized into Urdu', 'Ongoing localization for one of the leading mobile phone brands at 99%+ accuracy.'),
             ('18 hrs', 'Of interviews subtitled', 'English SRT subtitles for a CPEC documentary, produced by 10 subtitlers and reviewed by 2 linguists.'),
             ('52 min', 'Of Balochi audio translated', 'Rare-language audio-visual translation into English, QA\'d and delivered on deadline.')]
    work = sec([
        head('Proven Results', 'Recent <span class="x-hl">Translation Projects</span>', 'A few examples of the localization, subtitling and audio-visual work we deliver for clients around the world.'),
        C([C([H(n, 'p', 'x-case-n'), H(t, 'h3'), P(d)], 'x-card x-case') for n, t, d in cases], 'x-g3 rv-st', 'grid'),
        C([BTN('View Sample Projects', U + '/sample/', 'x-btn x-btn-ol')], 'x-btns rv', 'row'),
    ], 'x-center')

    founder = sec([C([
        C([IMG(UP + '2020/10/Salman-Background-Removed.png', '', 'Dr. Muhammad Salman Riaz, founder of Pak Translations', 'large')], 'x-founder-img rv rv-l'),
        C([EB('Meet the Founder'), H('Led by <span class="x-hl">Dr. Muhammad Salman Riaz</span>', 'h2', 'x-title'),
           P('Pak Translations was founded on commitment, honesty, perseverance and simplicity — and on the belief that every message deserves to be understood exactly as intended.', 'x-quote'),
           P('Dr. Riaz holds a Ph.D. in Translation Studies from the University of Leeds, UK and an M.Phil. in Linguistics from the National University of Modern Languages, Pakistan. With over a decade of experience in translation, localization, QA, transcription, subtitling and language-test development, he personally oversees the quality of our work.'),
           P('Dr. Muhammad Salman Riaz<span>Founder &amp; CEO, Pak Translations</span>', 'x-sign'),
           BTN('More About Us', U + '/about-us/', 'x-btn x-btn-g')], 'x-founder-copy rv'),
    ], 'x-founder', 'row')])

    P530 = {p['id']: p for p in json.load(open(os.path.join(D, 'wp-backup/pages.json')))}[530]
    slides = []
    def walk(n):
        for e in n:
            if e.get('widgetType') == 'testimonial-carousel':
                for s in e['settings']['slides']:
                    slides.append({'_id': rid(), 'content': s['content'].strip().strip('"').replace('👍', '').strip(), 'name': ' '.join(s['name'].split()),
                                   'title': ' '.join(s.get('title', '').replace('<br>', ', ').split()).replace(' ,', ',').replace(', ,', ','), 'image': s.get('image', {})})
            walk(e.get('elements', []))
    walk(json.loads(P530['meta']['_elementor_data']))
    for s in slides:
        s['title'] = s['title'].replace(', <a', ' · <a').replace('Director,,', 'Director,')
    testi = sec([
        head('Client Reviews', 'What Our <span class="x-hl">Clients Say</span>', 'Universities, development organisations and individuals trust us with their most important words.'),
        W('testimonial-carousel', 'x-testi rv', slides=slides, skin='default', layout='image_inline', alignment='left', slides_per_view='2', slides_per_view_tablet='1',
          slides_per_view_mobile='1', slides_to_scroll='1', autoplay='yes', autoplay_speed=6000, loop='yes', pause_on_hover='yes', speed=600,
          pagination='bullets', show_arrows='yes', space_between={'unit': 'px', 'size': 24}, image_size='thumbnail'),
    ], 'x-bg')

    faqs = [('How much do translation services cost?', 'Pricing depends on the language pair, word count, subject matter (for example legal or medical) and your deadline. Send us your document through the quote form or on WhatsApp and we will reply with a clear, no-obligation quote.'),
            ('Do you provide certified translations for immigration and visas?', 'Yes. We translate and certify personal and legal documents such as birth and marriage certificates, degrees, transcripts and court papers. On request we can also provide a signed translator affidavit and guidance with notarization.'),
            ('Which languages do you translate?', 'We work in 120+ languages across South Asia, East and Southeast Asia, the Middle East, Europe and Africa — including regional languages such as Urdu, Punjabi, Pashto, Sindhi, Balochi and Saraiki. See our <a href="https://pak-translations.com/languages/">full language list</a>.'),
            ('Can you translate between two non-English languages?', 'Yes. Our services are not limited to English. We regularly handle pairs such as German, French or Spanish into other languages — just ask about your combination.'),
            ('How long does a translation take?', 'It depends on the length and complexity of the content. We agree a realistic deadline with you before starting, and if anything unexpected happens we inform you immediately and reassign the work so your delivery date is protected.'),
            ('How do I place an order?', 'Use our <a href="https://pak-translations.com/your-order/">order form</a> to share your files and requirements, or contact us by email at info@pak-translations.com or on WhatsApp at +92 337 1440929.'),
            ('Do you offer support after delivery?', 'Absolutely. If you have questions or need a revision after delivery, we are here to help — our support does not end when the project does.')]
    faq = sec([C([
        C([EB('FAQs'), H('Frequently Asked <span class="x-hl">Questions</span>', 'h2', 'x-title'),
           P('Quick answers about our translation services, pricing and certified translations. Still curious? Our team replies fast on WhatsApp.', 'x-lead'),
           BTN('Ask on WhatsApp', WA, 'x-btn x-btn-g', 'fab fa-whatsapp', False, True)], 'x-faq-side rv'),
        W('accordion', 'x-faq rv', tabs=[{'_id': rid(), 'tab_title': q, 'tab_content': f'<p>{a}</p>'} for q, a in faqs], faq_schema='yes', title_html_tag='h3',
          selected_icon=ICO('plus'), selected_active_icon=ICO('minus'), icon_align='right'),
    ], 'x-faq-wrap', 'row')])

    cta = sec([C([H('Ready to Reach a Global Audience?', 'h2'),
                  P('Tell us what you need translated — we will match you with the right linguist and send a free quote.'),
                  C([BTN('Get a Free Quote', '#quote', 'x-btn'), BTN('Call / WhatsApp ' + PHONE, WA, 'x-btn x-btn-ol', 'fab fa-whatsapp', False, True)], 'x-btns', 'row')], 'x-cta rv rv-s')], 'x-center x-cta-sec')

    ld = {'@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': U + '/#business', 'name': 'Pak Translations', 'url': U + '/',
          'logo': LOGO, 'image': LOGO, 'description': 'Professional and certified translation services in Pakistan: document translation, localization, transcription, subtitling, interpreting and DTP in 120+ languages.',
          'telephone': '+923371440929', 'email': EMAIL, 'priceRange': '$$',
          'address': {'@type': 'PostalAddress', 'streetAddress': 'B-14/16-C, Street No. 2, Behind Zamindara Bank, Mohallah Fattupura', 'addressLocality': 'Gujrat', 'addressRegion': 'Punjab', 'postalCode': '50700', 'addressCountry': 'PK'},
          'founder': {'@type': 'Person', 'name': 'Dr. Muhammad Salman Riaz', 'jobTitle': 'Founder & CEO', 'alumniOf': ['University of Leeds', 'National University of Modern Languages']},
          'areaServed': 'Worldwide', 'knowsLanguage': ['ur', 'en', 'ar', 'pa', 'ps', 'sd', 'fa', 'hi', 'bn', 'zh', 'fr', 'de', 'es', 'tr', 'ru'],
          'sameAs': [FB, TW, PROZ],
          'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Translation services', 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for _, n, _ in SERVICES]}}
    schema = RAW(f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
    return [hero, stats, marq, svc, why, how, cert, lang, work, founder, testi, faq, cta, schema]

if __name__ == '__main__':
    json.dump(build(), open(os.path.join(D, 'built_home.json'), 'w'))
    print('ok')
