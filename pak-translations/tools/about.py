"""About Us (page 611)."""
from lib import *
TITLE = 'About Us'
SEO = ('About Pak Translations | PhD-Led Translation Company',
       'Meet Pak Translations, a PhD-led translation company. Tested native linguists, strict quality control and 120+ languages for clients worldwide.',
       'translation company')

def build():
    seed('about')
    hero = phero('About Us', 'About Pak Translations — <span class="x-hl">A Name to Rely Upon</span>',
                 'We help businesses, institutions and individuals get their message across clearly and effectively — in any market, in 120+ languages.')
    story = sec([split(
        [IMG(UP + '2022/03/handshake-close-up-executives-scaled.jpg', '', 'Pak Translations agreeing a translation project with a client'),
         IBOX('globe-asia', '120+ languages', 'Asian, European &amp; African', 'x-media-badge', tag='p')],
        [EB('Who We Are'), H('A Translation Company Built on <span class="x-hl">Quality &amp; Trust</span>', 'h2', 'x-title'),
         P('Pak Translations exists to provide quality language services that help clients get their message across clearly and effectively — or reach entirely new markets. We specialise in Asian and African languages, covering both major and minor languages, and we keep expanding into European and rare regional languages.', 'x-lead'),
         P('We have brought together top talent in every language we offer, so our clients can rely on us for all their language needs with complete satisfaction and confidence — from a single certificate to millions of words of software localization.'),
         ILIST([(t, 'check-circle') for t in ('PhD-led team and quality process', 'Native, rigorously tested linguists', 'A huge variety of services', 'Support before, during and after delivery')], 'x-checks'),
         C([BTN('Explore Our Services', U + '/services/', 'x-btn x-btn-g')], 'x-btns', 'row')])])

    stats = C([C([
        W('counter', 'x-stat', starting_number=0, ending_number=120, suffix='+', title='Languages &amp; dialects', duration=2000),
        W('counter', 'x-stat', starting_number=0, ending_number=11, suffix='', title='Specialist language services', duration=1500),
        W('counter', 'x-stat', starting_number=0, ending_number=99, suffix='%', title='Accuracy on large localization projects', duration=2000),
    ], 'x-stats-grid x-g3 rv rv-s', 'grid')], 'x-stats x-stats-flat', box=True)

    values = [('handshake', 'Commitment', 'We take ownership of every project and see it through — on time, as agreed, without excuses.'),
              ('balance-scale', 'Honesty', 'Clear quotes, realistic deadlines and open communication if anything changes.'),
              ('mountain', 'Perseverance', 'Rare language? Tight deadline? Complex format? We find the right linguist and the right way.'),
              ('feather-alt', 'Simplicity', 'An easy ordering process and plain answers, so working with us is effortless.')]
    vals = sec([head('Our Values', 'The Principles <span class="x-hl">We Work By</span>', 'Pak Translations was founded on four simple principles that shape every project we take on.'),
                C([IBOX(i, t, d, 'x-card x-svc x-nomore', tag='h3') for i, t, d in values], 'x-g4 rv-st', 'grid')], 'x-bg')

    quality = sec([C([
        C([EB('Quality Control'), H('Every Linguist Tested. <span class="x-hl">Every File Checked.</span>', 'h2', 'x-title'),
           P('Quality is the backbone of our business. Linguists join our team only after rigorous skills testing, and we keep monitoring their work so that the quality we deliver stays consistently high. Our Translator Instructions — shared with every linguist during onboarding — require them to check deliverables thoroughly, and our own QA team reviews every translation before it reaches you.'),
           C([BTN('See Sample Projects', U + '/sample/', 'x-btn'), BTN('Join Our Team', U + '/career/', 'x-btn x-btn-o')], 'x-btns', 'row')], 'x-band-copy rv'),
        C([ILIST([(t, 'check-circle') for t in ('Skills test before onboarding', 'Written Translator Instructions', 'Self-proofreading by the linguist',
                                                 'Independent QA: layout, punctuation, terminology', 'Post-delivery support for every client')], 'x-checks x-checks-1')], 'x-band-side rv rv-r'),
    ], 'x-band', 'row')])

    founder = sec([C([
        C([IMG(UP + '2026/10/founder-dr-salman-riaz.jpg', '', 'Dr. Muhammad Salman Riaz, founder and CEO of Pak Translations')], 'x-founder-img rv rv-l'),
        C([EB('Meet the Founder'), H('Dr. Muhammad <span class="x-hl">Salman Riaz</span>', 'h2', 'x-title'),
           P('Every message deserves to be understood exactly as intended — that is the standard I set for every project we deliver.', 'x-quote'),
           P('Dr. Muhammad Salman Riaz holds a Ph.D. in Translation Studies from the University of Leeds, UK and an M.Phil. in Linguistics from the National University of Modern Languages (NUML), Pakistan.'),
           P('He brings over 10 years of experience in translation and localization, review, QA, transcription, subtitling, language-proficiency test development, and phonetic and morpho-syntactic services. Known for exceeding client expectations, he founded Pak Translations to offer the same level of quality in all Asian and European languages.'),
           P('Dr. Muhammad Salman Riaz<span>Founder &amp; CEO, Pak Translations</span>', 'x-sign'),
           C([BTN('View LinkedIn Profile', LINKEDIN, 'x-btn x-btn-g', 'fab fa-linkedin-in', True, True)], 'x-btns', 'row')], 'x-founder-copy rv'),
    ], 'x-founder', 'row')])

    faqs = [('Who are your translators?', 'Native-speaker linguists who have passed our skills test and follow our written Translator Instructions. Every project is also reviewed by our QA team.'),
            ('Do you work with businesses or individuals?', 'Both. We serve universities, development organisations and companies, as well as individuals who need certified translations for immigration, study or legal matters.'),
            ('How can I start a project?', f'Send your files through our <a href="{U}/your-order/">order form</a> or email {EMAIL}.')]
    return [hero, stats, story, vals, quality, founder, faq_sec(faqs, bg='x-bg'), cta_sec()]
