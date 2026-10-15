"""Make → model list for the symptom checker dropdowns.
Model labels are shown to the visitor; the optional slug is the Imagin.studio `modelFamily` (default: label
lower-cased, spaces → '-').  Used by build_home.py (form options) and code.py (injects BB_CARS into bb.js)."""
import json

CARS = {
    'Acura': ['MDX', 'RDX', 'TLX', 'Integra', 'ILX', 'TL'],
    'Alfa Romeo': ['Giulia', 'Stelvio', 'Tonale'],
    'Audi': ['A3', 'A4', 'A5', 'A6', 'Q3', 'Q5', 'Q7', 'Q8', 'e-tron'],
    'BMW': ['3 Series', '5 Series', 'X1', 'X3', 'X5', 'X7'],
    'Buick': ['Encore', 'Envision', 'Enclave', 'Verano'],
    'Cadillac': ['Escalade', 'XT4', 'XT5', 'XT6', 'CT5', 'CTS'],
    'Chevrolet': [('Silverado 1500', 'silverado'), 'Equinox', 'Malibu', 'Cruze', 'Trax', 'Traverse', 'Blazer', 'Tahoe',
                  'Suburban', 'Colorado', 'Camaro', 'Spark'],
    'Chrysler': ['Pacifica', '300', ('Town & Country', 'town-and-country')],
    'Dodge': ['Grand Caravan', 'Durango', 'Charger', 'Challenger', 'Journey'],
    'Fiat': ['500', '500X'],
    'Ford': [('F-150', 'f150'), 'Escape', 'Explorer', 'Edge', 'Ranger', 'Bronco', 'Maverick', 'Mustang', 'Expedition', 'Focus',
             'Fusion', 'Transit'],
    'Genesis': ['G70', 'G80', 'GV70', 'GV80'],
    'GMC': ['Sierra', 'Canyon', 'Terrain', 'Acadia', 'Yukon', 'Savana'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'HR-V', 'Pilot', 'Odyssey', 'Passport', 'Ridgeline', 'Fit'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona', 'Palisade', 'Venue', 'Accent', 'Ioniq 5'],
    'Infiniti': ['Q50', 'QX50', 'QX60', 'QX80'],
    'Jeep': ['Wrangler', 'Grand Cherokee', 'Cherokee', 'Compass', 'Renegade', 'Gladiator'],
    'Kia': ['Forte', 'Soul', 'Seltos', 'Sportage', 'Sorento', 'Telluride', 'Carnival', 'Niro', 'Rio'],
    'Land Rover': ['Range Rover', 'Range Rover Sport', 'Range Rover Evoque', 'Discovery', 'Defender'],
    'Lexus': ['RX', 'NX', 'ES', 'IS', 'GX', 'UX'],
    'Lincoln': ['Navigator', 'Aviator', 'Nautilus', 'Corsair', 'MKX'],
    'Mazda': [('Mazda3', 'mazda3'), 'CX-5', 'CX-30', 'CX-50', 'CX-9', 'CX-90', ('Mazda6', 'mazda6'), 'MX-5'],
    'Mercedes-Benz': [('C-Class', 'c-class'), ('E-Class', 'e-class'), ('GLC', 'glc-class'), ('GLE', 'gle-class'),
                      ('GLA', 'gla-class'), ('A-Class', 'a-class'), ('S-Class', 's-class'), 'Sprinter'],
    'Mitsubishi': ['Outlander', 'RVR', 'Eclipse Cross', 'Mirage'],
    'Nissan': ['Rogue', 'Altima', 'Sentra', 'Kicks', 'Qashqai', 'Murano', 'Pathfinder', 'Frontier', 'Titan', 'Versa', 'Leaf'],
    'Porsche': ['Cayenne', 'Macan', '911', 'Panamera', 'Taycan'],
    'RAM': ['1500', '2500', 'ProMaster'],
    'Skoda': ['Octavia', 'Kodiaq'],
    'Smart': ['Fortwo'],
    'Subaru': ['Outback', 'Forester', 'Crosstrek', 'Impreza', 'Ascent', 'WRX', 'Legacy'],
    'Suzuki': ['Swift', 'SX4', 'Grand Vitara'],
    'Toyota': ['Corolla', 'Camry', 'RAV4', 'Corolla Cross', 'Highlander', 'Tacoma', 'Tundra', '4Runner', 'Sienna', 'Prius',
               'Sequoia', 'Venza', 'C-HR'],
    'Volkswagen': ['Jetta', 'Golf', 'Tiguan', 'Atlas', 'Taos', 'Passat'],
    'Volvo': ['XC40', 'XC60', 'XC90', 'S60', 'V60'],
}
OTHER = 'Other / not listed'
YEARS = [str(y) for y in range(2026, 1994, -1)] + ['Older']


def slug(s):
    return s.lower().replace('&', 'and').replace(' ', '-')


def models(make):
    out = []
    for m in CARS[make]:
        label, sl = (m if isinstance(m, tuple) else (m, slug(m)))
        out.append((label, sl))
    return out


def make_options():
    return '\n'.join(['Select make|'] + list(CARS) + [OTHER])


def model_options():
    # "label|value" – value carries the make so the email reads "Toyota Camry"; bb.js shows the selected make's models only
    rows = ['Select model|']
    for mk in CARS:
        rows += [f'{lab}|{mk} {lab}' for lab, _ in models(mk)]
    rows.append(f'{OTHER}|{OTHER}')
    return '\n'.join(rows)


def year_options():
    return '\n'.join(['Select year|'] + YEARS)


def js_data():
    data = {mk: {'slug': slug(mk), 'models': {f'{mk} {lab}': sl for lab, sl in models(mk)}} for mk in CARS}
    return 'window.BB_CARS=' + json.dumps(data, separators=(',', ':')) + ';'

