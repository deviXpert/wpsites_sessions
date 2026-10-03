"""Samples / case studies (page 988, slug /sample/). Facts are from the original page."""
from lib import *
TITLE = 'Samples'
SEO = ('Translation Sample Projects & Case Studies | Pak Translations',
       'See real translation projects by Pak Translations: Urdu localization for a mobile brand, Punjabi healthcare website, legal translation, Balochi & Mongolian AV translation and subtitling.',
       'translation sample projects')

CASES = [
    ('localization', 'Localization', '2022/11/busy-curly-afro-woman-works-from-home-uses-laptop-smartphone-workplace-checks-newsfeed-poses-white-desk-with-folders-notepads.jpg',
     'Localization demands specialist knowledge of source and target languages and cultures — plus correct handling of tags and placeholders.',
     [('Millions of words', 'Urdu localization for a leading mobile phone brand', 'For several years we have regularly localized the content of one of the leading mobile phone companies into Urdu — millions of words at 99% or higher accuracy.'),
      ('100% accuracy', 'Indian Punjabi website for a US healthcare company', 'Localization, revision, QA and style-guide development under a tight deadline. We split the work across 4 Indian Punjabi linguists and delivered with 100% accuracy.')]),
    ('document-translation', 'Document Translation', '2022/11/lawyer-with-weighing-scales.jpg',
     'From children\'s books to court proceedings, we choose words that suit the reader — and the authority receiving the document.',
     [('30,000+ words', 'Legal translation in South Asian languages', 'Claim forms, marriage and death certificates, wills, land-record forms, court proceedings, legal contracts and court orders, translated on a regular basis.'),
      ('Children\'s books', 'Translation for a US school', 'Simple, familiar language that young readers easily understand — challenging to get right, and our client was delighted with the result.')]),
    ('transcription', 'Audio/Video Transcription &amp; Translation', '2022/11/dr-muhammad-amer-k2ya7sNuG8I-unsplash.jpg',
     'Rare languages and urgent deadlines are where a strong linguist network matters most.',
     [('52 minutes', 'Balochi into English AV translation', 'Balochi translators are rare. Our translator delivered this interview about the situation of the people of Balochistan within the deadline, followed by our QA.'),
      ('~2 hours', 'Urgent Mongolian into English AV translation', 'Interviews on Mongolian history, sports and tradition — 5 translators and revisers worked in parallel to deliver good-quality work on time.')]),
    ('subtitling', 'Subtitling', '2022/11/1874661-cpecx-1545772698.jpg',
     'Large subtitling projects need tight coordination between subtitlers and reviewers.',
     [('18 hours', 'English SRT subtitles for CPEC interviews', 'Around 10 subtitlers created English SRT files for a series of interviews mostly about the CPEC project in Balochistan, reviewed by 2 further linguists before delivery.')]),
]

def build():
    seed('samples')
    hero = phero('Sample Projects', 'Translation Sample Projects &amp; <span class="x-hl">Case Studies</span>',
                 'Real projects we have delivered — from millions of words of Urdu localization to rare-language audio translation and large-scale subtitling.')
    out = [hero]
    for i, (slug, name, img, intro, items) in enumerate(CASES):
        rev = i % 2 == 1
        cards = [C([H(n, 'p', 'x-case-n'), H(t, 'h3'), P(d)], 'x-card x-case') for n, t, d in items]
        block = split([IMG(UP + img, '', f'{name} project by Pak Translations')],
                      [EB(f'Case Study {i + 1:02d}'), H(name, 'h2', 'x-title x-title-sm'), P(intro, 'x-lead'), C(cards, 'x-cases-col rv-st')] +
                      [C([BTN(f'Explore {name.split(" &amp;")[0].split("/")[0]} Services', f'{U}/services/#{slug}', 'x-btn x-btn-ol')], 'x-btns', 'row')], rev, 'x-split-top')
        out.append(sec([block], 'x-bg' if rev else '', _element_id=slug))
    out.append(cta_sec('Have a Similar Project?', 'Whether it is one certificate or a multi-language localization program, we would love to help. Get a free quote today.'))
    return out
