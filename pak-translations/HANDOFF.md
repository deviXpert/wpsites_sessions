# Pak Translations — Elementor Redesign Handoff

Site: **https://pak-translations.com** (LIVE) — WordPress + Astra child + Elementor 4.3 / Elementor Pro 4.3 + Yoast. Hosting: Hostinger (hcdn).

## Rules agreed with the user
- Build **only with core Elementor + Elementor Pro widgets** (container, heading, text-editor, button, image, icon-box, icon-list, counter, accordion, form, testimonial-carousel, nav-menu, social-icons, icon, html). The user will delete Master Addons, PowerPack, Premium Addons, Transition Slider, Sticky Header Effects later — nothing may depend on them.
- All forms = Elementor Pro Form widget (recipients kept: quote/order → info@pak-translations.com, contact → hr@pak-translations.com).
- Fonts: **Outfit** (headings/buttons/nav) + **Figtree** (body). Brand colours from logo: green #6DB52E / dark green #2F6E14, yellow #F8C300, ink #0B1A10.
- SEO: one H1 per page, alt text, FAQ schema (accordion `faq_schema`), ProfessionalService JSON-LD on home, Yoast titles/descriptions (writable via `yoast/v1/bulk_editor/update_search`).
- Never overwrite live pages without the user's OK. Credentials only from env (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`); `tools/wp.py` refuses any host other than pak-translations.com.

## Security findings (site was SEO-spam hacked)
- Old home (ID 530): hidden HTML widget with ~28 spam links + 2 casino text widgets. New home is built from scratch; user wants old home deleted after approval.
- 3 spam pages: 2617, 2603, 1142 (essay spam) — DELETED (confirmed gone). 11,095 orphaned spam categories (no posts exist). ~37 duplicate "Default Kit" posts (active kit 26951).
- User confirmed deletion: `tools/del_spam_cats.py` (keeps category 1) — run started; re-run it if interrupted (already-deleted IDs count as done).
- Recommend: change admin + hosting passwords, update all plugins, re-enable Wordfence and run a scan (the injection source is likely still present).

## Settings changed
- Front page = 39107; menu item 919 (Home) → page 39107. Yoast title/description/focus keyphrase set via `yoast/v1/bulk_editor/update_search` (fields `seo_title`, `meta_description`, `focus_keyphrase`); re-save the page afterwards so Yoast refreshes its indexable.
- Footer credit: "Powered by hafizahsanali.com" (user request).
- Elementor experiment **Flexbox Container → active** (needed for the new layout; old section pages unaffected).

## How it works
- `tools/pt.css`, `tools/pt.js` — design system + animations (reveal, stagger, scroll progress, spotlight cards, marquee, sticky shrinking header via Elementor Pro sticky). Loaded by an HTML widget inside the header.
- `tools/lib.py` — Elementor JSON helpers, header(), footer(), forms. Layout uses our own classes (`x-dr/x-dc/x-grid/x-bx`) so pages don't depend on Elementor's generated CSS.
- `tools/home.py` — new home page. Add more pages as modules exposing `build()` (+ optional `TITLE`).
- `python3 tools/push_preview.py home` — pushes `/redesign-preview-<name>/` (published, **password-protected**, Canvas template with header/footer embedded) and clears Elementor cache (element cache otherwise serves stale HTML). Preview IDs + password in git-ignored `tools/preview_state.json`.
- Screenshots: `node tools/shot.js <url> prev/name <password>` then `python3 tools/slice.py prev/name_d.png`.

## Status
| Item | ID | Status |
|---|---|---|
| **New home (LIVE front page)** | 39107 | approved & live (Canvas template, header/footer embedded). Update with `python3 tools/publish_live.py home` — NOT push_preview.py |
| Old home | 530 | moved to Trash (slug now home__trashed; /home/ 301s to /) |
| About, Services, Languages, Samples, Career, Contact, Your Order | 611, 673, 633, 988, 693, 706, 319 | to redesign next |

## Go-live plan (after approval)
1. Create Elementor Pro header + footer theme templates from `lib.header()/footer()` with condition include/general (`elementor/v1/site-editor/templates-conditions/<id>`); remove conditions from old header 33/27 and footer 37.
2. Copy each page body into the ORIGINAL page IDs (keeps URLs), template `elementor_header_footer`; new home → set as front page; delete old home 530 + preview pages.
3. Set kit global fonts (Outfit/Figtree) + colours via `elementor/v1/globals/*`; set Yoast titles/descriptions; clear Elementor cache + Hostinger cache.
