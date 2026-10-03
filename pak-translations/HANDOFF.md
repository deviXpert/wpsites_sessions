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

## Status — ALL PAGES LIVE (2026-10-03)
| Page | ID | URL |
|---|---|---|
| Home (front page) | 39107 | / |
| About | 611 | /about-us/ |
| Services (11 anchored sections, e.g. /services/#certified-translation) | 673 | /services/ |
| Languages | 633 | /languages/ |
| Samples | 988 | /sample/ |
| Career (Elementor form → info@) | 693 | /career/ |
| Contact (Elementor form → hr@, Google map) | 706 | /contact-us/ |
| Your Order (Elementor form → info@) | 319 | /your-order/ |
| Header template (site-wide, holds CSS/JS/fonts) | 33 | include/general |
| Footer template (site-wide, "Powered by hafizahsanali.com") | 37 | include/general |

All pages use template `elementor_header_footer`; each has one H1, Yoast title/description/focus keyphrase, and FAQ schema where there is an FAQ.
Elementor globals set: colours (#6DB52E, #0B1A10, #4A5560, #F8C300), fonts (Outfit headings, Figtree text).
Old home 530 is in Trash. Preview pages deleted. Spam categories deleted (11,094 removed; only Uncategorized left). Duplicate kits deleted.

## Updating pages
- Edit the module (`tools/<page>.py`, `lib.py`, `pt.css`), then `python3 tools/golive.py <page>` (no args = header/footer + all pages). It also sets Yoast meta and clears the Elementor cache (needed — element cache serves stale HTML otherwise).
- For a risky change, preview first: `python3 tools/push_preview.py <page>` (password page), then delete the preview.

## Remaining recommendations for the user
- Security: change WP admin + hosting passwords, update plugins, re-enable Wordfence & scan (spam injection source likely still present).
- Addons (Master Addons, PowerPack, Premium Addons, Transition Slider, Sticky Header Effects) are unused by the new design and can be deactivated/deleted; re-check pages afterwards.
- Duplicate "Default Kit" posts: DELETED (37 removed; only the active kit 26951 remains). Elementor kits need `force_delete_kit=1` on REST DELETE.
- Purge Hostinger cache after changes.

## Go-live plan (DONE — kept for reference)
1. Create Elementor Pro header + footer theme templates from `lib.header()/footer()` with condition include/general (`elementor/v1/site-editor/templates-conditions/<id>`); remove conditions from old header 33/27 and footer 37.
2. Copy each page body into the ORIGINAL page IDs (keeps URLs), template `elementor_header_footer`; new home → set as front page; delete old home 530 + preview pages.
3. Set kit global fonts (Outfit/Figtree) + colours via `elementor/v1/globals/*`; set Yoast titles/descriptions; clear Elementor cache + Hostinger cache.

## Round 2 fixes (2026-10-03)
- Languages region cards: icon + title aligned, count badge inline, masonry columns (no gaps).
- Full width: pages get Astra meta `ast-site-content-layout=full-width-container` (+ CSS fallback) — Astra's 1240px `.ast-container` was boxing the page.
- Content container width 1440px on desktop (`.x-bx>.e-con-inner`).
- Top bar: icons/text were clipped by inherited overflow — fixed (`.x-top *{overflow:visible}`).
- Hero trust chips: icon left of text, even 3-column row.
- Founder photo: background removed (rembg isnet-general-use), composited on dark brand background → media 39125 `2026/10/founder-dr-salman-riaz.jpg` (Home + About).
- Forms: phone fields are text (Elementor tel validation rejects spaces), custom success message, `save-to-database` + email, honeypot anti-spam field. All 4 forms tested live (TEST submissions sent to info@ / hr@).
- SEO: titles ≤ ~65 chars, descriptions ≤ ~160; OG/Twitter social title+description; share image media 39126 set as featured image on all pages (Yoast og:image); alt text added to all used media.
- Link check: `python3 tools/linkcheck.py` — all internal links/anchors OK. Facebook/ProZ block bots (fine in browsers).
- Hostinger CDN served a stale copy of the OLD home (with spam) at the bare URL — purge CDN in hPanel after big changes.
- User removed the addon plugins and installed WP Mail SMTP during this round.
