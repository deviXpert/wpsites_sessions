"""Services (page 673). Each service has an anchor (#slug) that the home/footer links point to."""
from lib import *
TITLE = 'Services'
SEO = ('Professional Translation & Language Services | Pak Translations',
       'Certified & document translation, localization, transcription, subtitling, interpreting, proofreading and DTP in 120+ languages by native linguists.',
       'translation services')

DETAIL = {
    'localization': ('2022/03/russian-english-communication-language-concept-min-scaled.jpg',
        'Our experienced localizers adapt your website, mobile app, software or marketing content to local markets while staying sensitive to local cultural and language norms. We handle tags, placeholders and character limits correctly and follow your style guide and glossary — or help you create one.',
        ['Website, app &amp; software UI localization', 'Style-guide &amp; glossary development', 'Localization QA &amp; linguistic testing', 'Marketing &amp; e-commerce content']),
    'document-translation': ('2022/03/composition-with-books-table-scaled.jpg',
        'Brochures, certificates, SMS campaigns, affidavits, court summons, contracts, medical reports — whatever the document, our subject-matter linguists transfer your message into another language with both accuracy and readability.',
        ['Legal &amp; court documents', 'Medical &amp; healthcare reports', 'Business, financial &amp; technical files', 'Educational &amp; research material']),
    'certified-translation': ('2022/11/lawyer-with-weighing-scales.jpg',
        'Official translations of personal and legal documents for embassies, immigration authorities, universities and courts. Each certified translation is reviewed before delivery, and on request we provide a signed translator affidavit and guidance with notarization.',
        ['Birth, marriage &amp; death certificates', 'Degrees, diplomas &amp; transcripts', 'Wills, land records &amp; court orders', 'Translator affidavit on request']),
    'editing-proofreading': ('2022/11/student-female-performing-written-task-copybook-1.jpg',
        'Your documents, websites and subtitles must be error-free and presented in the right format and layout. Our expert editors and proofreaders make sure the final version is spotless, consistent and natural-sounding.',
        ['Bilingual review of translations', 'Monolingual proofreading', 'Formatting &amp; layout checks', 'Terminology consistency']),
    'transcription': ('2022/11/dr-muhammad-amer-k2ya7sNuG8I-unsplash.jpg',
        'Transcribing and translating audio and video demands accurate time-codes, faithful rendering of speech and output that readers can follow — despite background noise and interruptions. Our transcribers have the concentration and listening skills to deliver.',
        ['Interviews, focus groups &amp; research audio', 'Time-coded transcripts', 'Transcription + translation', 'Rare languages such as Balochi &amp; Mongolian']),
    'interpreting': ('2022/03/handshake-close-up-executives-scaled.jpg',
        'Interpreting happens on the spot, so it requires deep command of both languages and the ability to process and render speech instantly — the margin for error is almost zero. Our interpreters work in person, over the phone and by video conference.',
        ['Consecutive interpreting', 'Simultaneous interpreting', 'Telephone interpreting', 'Video-conference interpreting']),
    'subtitling': ('2022/11/1874661-cpecx-1545772698.jpg',
        'Subtitling requires precise synchronisation between subtitles and time-codes and delivery in formats such as SubRip (SRT) and VobSub. We prepare open or closed captions and soft or hard subtitles to your exact specifications.',
        ['SRT, VobSub &amp; other formats', 'Open &amp; closed captions', 'Soft &amp; hard (burned-in) subtitles', 'Subtitle translation &amp; review']),
    'content-creation': ('2022/03/working-hard-party-hard-weekends-cropped-shot-woman-typing-keyboard-sitting-front-computer-monitor-freelancer-translating-new-project-writing-some-notes-note-pad-min-scaled.jpg',
        'Our creative writers have years of experience producing convincing, engaging content that helps you reach your target audience effectively — in English and other languages.',
        ['Blog articles &amp; web copy', 'Social media posts', 'Print &amp; digital ads', 'Case studies, emails &amp; presentations']),
    'language-material': ('2022/11/learning-foreign-languages.jpg',
        'We develop reading, writing and listening tests for foreign and second-language learners in line with the proficiency levels you define, and we create and collate passages for use as practice material in language classes.',
        ['Proficiency test development', 'Reading &amp; listening passages', 'Writing tasks &amp; rubrics', 'Classroom practice material']),
    'linguistics': ('2022/11/close-up-student-working-with-laptop-dictionary.jpg',
        'From phonetic transcription and pronunciation validation to part-of-speech and case tagging, stress placement, and corpus or dictionary building, we support linguistic data projects — including data for text-to-speech (TTS) systems.',
        ['Phonetic transcription (IPA)', 'Pronunciation validation', 'PoS &amp; case tagging', 'Corpus &amp; dictionary building']),
    'desktop-publishing': ('2022/03/workplace-with-smartphone-notebook-black-table-top-view-min-scaled.jpg',
        'Translated text often needs re-layout. Our DTP specialists handle typesetting, formatting, layout adjustment and design for brochures, flyers, books and other documents — including right-to-left scripts like Urdu and Arabic.',
        ['Typesetting &amp; layout', 'RTL scripts (Urdu, Arabic, Persian)', 'Print-ready PDFs', 'Brochures, flyers &amp; books']),
}

def build():
    seed('services')
    hero = phero('Services', 'Professional Translation &amp; <span class="x-hl">Language Services</span>',
                 'One partner for every language need — translation, localization, transcription, subtitling, interpreting and more, delivered by tested native linguists in 120+ languages.')
    nav = C([ILIST([(n, None, f'#{s}') for s, n, _ in SERVICES], 'x-tags x-tags-lg')], 'x-svc-nav rv', box=True)
    blocks = []
    for i, (slug, name, icon) in enumerate(SERVICES):
        img, text, items = DETAIL[slug]
        rev = i % 2 == 1
        block = split([IMG(UP + img, '', f'{name} services by Pak Translations')],
                      [P(f'<i class="fas fa-{icon}" aria-hidden="true"></i>&nbsp; Service {i + 1:02d}', 'x-eyebrow'),
                       H(name, 'h2', 'x-title x-title-sm'), P(text, 'x-lead'), ILIST([(t, 'check-circle') for t in items], 'x-checks'),
                       C([BTN('Get a Quote', U + '/your-order/', 'x-btn'), BTN('Contact Us', U + '/contact-us/', 'x-btn x-btn-ol', 'envelope', False)], 'x-btns', 'row')], rev)
        blocks.append(C([C([block], 'x-svc-block', box=True)], 'x-svc-row' + (' x-bg' if rev else ''), _element_id=slug))
    steps = [('comments', 'Understanding', 'We discuss your requirements and reference material.'),
             ('file-signature', 'Order', 'Confirm through the order form or by email.'),
             ('user-tie', 'Assignment', 'The most relevant native linguist takes your project.'),
             ('search', 'Quality Assurance', 'Our QA team checks every detail before delivery.')]
    how = steps_sec('How It Works', 'From Request to <span class="x-hl">Delivery</span>', 'A clear, four-step process for every service.', steps)
    faqs = [('Which translation service do I need?', 'If your document is for an embassy, immigration office, university or court, you most likely need certified translation. For websites and apps choose localization, and for audio or video choose transcription or subtitling. Not sure? Message us and we will advise.'),
            ('What file formats do you accept?', 'Word, PDF, Excel, PowerPoint, scanned images, subtitle files (SRT and others), audio and video files, and localization files. We return the translation in the format you need.'),
            ('Can you handle large or urgent projects?', 'Yes. For large or urgent work we assign a team of linguists and reviewers, as we did for 18 hours of interview subtitling and two hours of urgent Mongolian AV translation.'),
            ('How is pricing calculated?', 'Usually per word for translation, per minute for transcription and subtitling, per hour for interpreting and review, and per page for DTP. Send your files for a free, no-obligation quote.')]
    return [hero, nav] + blocks + [how, faq_sec(faqs), cta_sec()]
