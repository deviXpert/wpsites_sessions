"""Global Elementor templates (Templates → Saved Templates).  Every section that is identical on more than one page lives here once
and is embedded with Elementor's native Template widget, so editing it in one place updates the whole site.

  key            used on
  google_card    hero aside (home, services, service pages, about)
  booking        "Book your visit" section – home, 11 service pages, about
  reviews        Trustindex Google reviews – home, services, 11 service pages, about
  reasons        "Why drivers choose us" – services, 11 service pages
  location       "Your neighbourhood repair shop" + map – services, 11 service pages
  request        WhatsApp request form – services, blog archive, single post
  faq            general FAQ – services, contact
  suppliers      parts-supplier logo marquee – home, services
  services_grid  service cards grid – services, about

Pages call tpl('<key>'); run this file (or build_all.py) after changing a section's builder."""
import json
import el
from el import W, C


def tpl(key, name=None):
    """Template widget for a global section, wrapped in a full-width, zero-padding container (top level must be a container)."""
    tid = json.load(open('ids.json'))['tpl_' + key]
    w = W('template', name or f'Global – {key}', template_id=str(tid))
    if key == 'google_card':
        w['settings']['_element_width'] = ''
        return w
    return C(f'Global section – {key}', [w], cls='bb-global')


def sections():
    import build_home as home
    import build_services as svc
    return {
        'google_card': ('Google rating card', lambda: home.google_card_content()),
        'booking': ('Booking section (Book your visit)', lambda: home.book()),
        'reviews': ('Google reviews (Trustindex)', lambda: home.reviews()),
        'reasons': ('Why drivers choose us', lambda: svc.reasons()),
        'location': ('Location + map', lambda: svc.location()),
        'request': ('WhatsApp service request', lambda: svc.book()),
        'faq': ('General FAQ', lambda: svc.faq()),
        'suppliers': ('Parts suppliers marquee', lambda: home.suppliers()),
        'services_grid': ('Service cards grid', lambda: svc.services_grid()),
    }


if __name__ == '__main__':
    from build_inner import ensure_template
    popup = json.load(open('ids.json'))['popup_book']
    for key, (title, fn) in sections().items():
        tid = ensure_template('tpl_' + key, f'Busy Bee – Global: {title}', 'container')
        el.seed('global-' + key)
        el.save('elementor_library', tid, el.book_popup([fn()], popup), extra={'title': f'Busy Bee – Global: {title}'})
        el.regen(tid)
        print(key, tid)
