"""Long-form copy for the other 8 service pages, from the client's Google Docs (Nov 2026).  HTML exports are cached in
design/gdocs/<key>.html and parsed by docs_parse.py (word-for-word copy, doc hyperlinks kept as internal links).
Re-download a doc:  curl -sL "https://docs.google.com/document/d/<ID>/export?format=html" -o design/gdocs/<key>.html
Merged over service_content.PAGES together with docs_copy.OVERRIDES."""
import os

import docs_parse

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = {
    # key: (Google Doc id, heading for the intro copy that follows the hero paragraph, photo beside it)
    'tires': ('1_a6YpQxDFSMkZ_FUTwhdGTOe4dPEKobgnpQS_B7wNyg', 'Your tire shop in NE Calgary', 'pickup-truck-repair-calgary'),
    'alignment': ('1JqfFH7sV7e3kHlxKfYmDrHhF2LZ3fASqalVdwoHkszc', 'Wheel alignment in Calgary at Busy Bee', 'pickup-truck-repair-calgary'),
    'battery': ('12DWYoFrnD1bsohS9gJmL2jT6Tgo4FO71mPfvfKvaGFY', 'Battery replacement in Calgary at Busy Bee',
                'computer-diagnostics-calgary'),
    'electrical': ('1-5JE0XkSZ6g_8g4hZbLOhE345SMoANbxKUCCXsYcwgk', 'Auto electrical repair in Calgary at Busy Bee',
                   'battery-alternator-service-calgary'),
    'suspension': ('147Q6Ie61-o-mhBNQ0IcsBqpqSJjRi4jtTqhFJDMb_8c', 'Suspension repair in Calgary at Busy Bee', 'brake-repair-calgary'),
    'transmission': ('1WXQO9ySFQpLmlFGImJ3mem4FWZ-e8EkRwv8wxQctDks', 'Transmission repair in Calgary at Busy Bee',
                     'engine-repair-audi-calgary'),
    'cooling': ('1HzgaVoXByoKgMP6iaULecko1_ol7ahjO6uQpvUwacVw', 'Radiator repair in Calgary at Busy Bee', 'engine-repair-audi-calgary'),
    'maintenance': ('1aekQFKkRlEMViPpBH4pE_gZ8NXmiMX7rbM4Zo3PJsqE', 'Car maintenance in Calgary at Busy Bee', 'mobil-1-synthetic-oil-change-calgary'),
}


def load(key):
    _, lead, photo = DOCS[key]
    with open(os.path.join(HERE, '..', 'design', 'gdocs', key + '.html'), encoding='utf-8') as f:
        return docs_parse.parse(f.read(), lead, photo)


OVERRIDES = {k: load(k) for k in DOCS}
