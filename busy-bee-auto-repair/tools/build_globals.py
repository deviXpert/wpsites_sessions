"""Global Elementor templates (Templates → Saved Templates) embedded on many pages with the native Template widget, so one edit
updates the whole site.  Currently: the Google rating card (links to the Google Business Profile)."""
import json
import el
from build_inner import ensure_template

if __name__ == '__main__':
    import build_home as home
    tid = ensure_template('tpl_google_card', 'Busy Bee – Google rating card (global)', 'container')
    el.seed('google-card')
    el.save('elementor_library', tid, [home.google_card_content()], extra={'title': 'Busy Bee – Google rating card (global)'})
    el.regen(tid)
    print('google card template', tid)
