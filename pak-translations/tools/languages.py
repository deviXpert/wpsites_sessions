"""Languages (page 633). Language lists come from the original page, with spelling fixes."""
import json
from lib import *
TITLE = 'Languages'
SEO = ('Languages We Translate | 120+ Languages incl. Urdu, Arabic & Pashto',
       'Professional translation in 120+ languages: Urdu, Punjabi, Pashto, Sindhi, Balochi, Arabic, Persian, Chinese, French, German, Spanish, African languages and more.',
       'translation languages')
FIX = {'icelandinc': 'Icelandic', 'Mnaipuri': 'Manipuri', 'Czheck': 'Czech', 'Arabic(all dialects)': 'Arabic (all dialects)'}
ICONS = {'South Asia': 'om', 'East Asia': 'torii-gate', 'South East-Asia': 'umbrella-beach', 'West Asia': 'mosque', 'Central Asia': 'mountain',
         'North Asia': 'snowflake', 'Western Europe': 'landmark', 'Northern Europe': 'tree', 'Southern Europe': 'sun', 'Eastern Europe': 'church', 'African': 'globe-africa'}
ORDER = ['South Asia', 'West Asia', 'East Asia', 'South East-Asia', 'Central Asia', 'North Asia', 'Western Europe', 'Southern Europe', 'Northern Europe', 'Eastern Europe', 'African']
NAMES = {'South East-Asia': 'Southeast Asia', 'African': 'Africa'}

def regions():
    P633 = {p['id']: p for p in json.load(open(os.path.join(D, 'wp-backup/pages.json')))}[633]
    out, cur = {}, None
    def walk(n):
        nonlocal cur
        for e in n:
            t = e.get('widgetType')
            if t == 'heading' and e['settings'].get('title') in ICONS: cur = e['settings']['title']
            elif t == 'icon-list' and cur and cur not in out:
                out[cur] = [FIX.get(x['text'].strip(), x['text'].strip()) for x in e['settings']['icon_list']]
            walk(e.get('elements', []))
    walk(json.loads(P633['meta']['_elementor_data']))
    return out

def build():
    seed('languages')
    R = regions()
    total = len({l.lower() for v in R.values() for l in v})
    hero = phero('Languages', 'Languages We Translate: <span class="x-hl">120+ Languages</span> &amp; Dialects',
                 'From Urdu, Punjabi and Pashto to Arabic, Chinese, French and Swahili — our native linguists cover major world languages and rare regional ones across Asia, Europe and Africa.')
    cards = [C([C([C([RAW(f'<span class="x-region-ic">{FAI(ICONS[r])}</span>', 'x-region-icw'), H(NAMES.get(r, r), 'h2', 'x-region-h')], 'x-region-name', 'row'),
                   P(f'{len(R[r])} language{"s" if len(R[r]) > 1 else ""}', 'x-count')], 'x-region-top', 'row'),
                ILIST([(l,) for l in R[r]], 'x-tags')], 'x-region') for r in ORDER if r in R]
    grid = sec([head('Coverage by Region', 'Asian, European &amp; <span class="x-hl">African Languages</span>', 'Every language below is handled by native linguists who have passed our skills test.'),
                C(cards, 'x-regions rv-st', 'col')], 'x-bg')
    pairs = ['Urdu to English', 'English to Urdu', 'Punjabi to English', 'Pashto to English', 'Arabic to English', 'English to Arabic', 'Persian to English', 'Sindhi to English',
             'German to English', 'French to English', 'Chinese to English', 'English to Spanish', 'German to Urdu', 'French to Arabic', 'Balochi to English', 'Hindi to English']
    pair_sec = sec([split(
        [IMG(UP + '2022/03/375306-PBRSKN-852.jpg', '', 'Translation between world languages')],
        [EB('Language Pairs'), H('Not Just English — <span class="x-hl">Any Language Pair</span>', 'h2', 'x-title'),
         P('Our services are not limited to combinations where English is the source or target language. We regularly translate German, French and Spanish into other languages, and we can arrange linguists for lesser-known languages spoken in these regions too.', 'x-lead'),
         P('<strong>Popular translation pairs:</strong>'), ILIST([(p,) for p in pairs], 'x-tags'),
         C([BTN('Ask About Your Language', U + '/contact-us/', 'x-btn x-btn-g', 'envelope', False)], 'x-btns', 'row')])])
    faqs = [('Do you translate rare or regional languages?', 'Yes. Alongside major languages we cover regional ones such as Balochi, Saraiki, Hindko, Pahari, Mirpuri, Sylheti, Chittagonian and Rohingya, plus many African languages. If your language is not listed, ask us — we can often arrange a linguist.'),
            ('Do you translate between two non-English languages?', 'Yes — for example German, French or Spanish into other languages. Please check with us for any uncommon pair; we may well be able to help.'),
            ('Which Arabic dialects do you cover?', 'We work with Modern Standard Arabic and regional dialects. Tell us the target country or audience and we will assign a suitable native linguist.')]
    return [hero, grid, pair_sec, faq_sec(faqs, bg='x-bg'), cta_sec('Need a Language Not Listed?', 'Tell us the language or pair you need — we will find the right native linguist and send you a free quote.')]
