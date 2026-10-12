# AAD Transport & Recovery — WordPress Redesign Handoff

Site: **https://aadrecovery.co.uk** (live; previously staged at maroon-raven-160825 / darkblue-kudu-638106 .hostingersite.com) (WordPress + Astra child + Elementor / Elementor Pro, Yoast, Trustindex)
Content source for new service pages: Google Doc https://docs.google.com/document/d/1tm9CqX6-TecfKiAPSj79lJA-qgvueNt4NuKzKEHdxTg/edit (copy saved as `tools/gdoc.html`, parsed to `tools/doc_pages.json`)

## ⚠️ Before doing anything in a new session
1. Credentials come from env vars only — **`AAD_WP_URL`, `AAD_WP_USER`, `AAD_WP_APP_PASSWORD`** (preferred) or `WP_URL`/`WP_USER`/`WP_APP_PASSWORD`. Never paste them in chat.
2. `tools/wp.py` **refuses to run unless the host is `aadrecovery.co.uk`** (override with `AAD_EXPECTED_HOST` only if the AAD site has genuinely moved). This guard exists because a previous session's env pointed at a different client site (`hotpink-lobster-615998…`, a medical site); 13 drafts were accidentally created there and were immediately and permanently deleted (verified).
3. Always work on drafts; never overwrite live pages without the user's OK.

## How to resume
```bash
cd aad-transport-recovery/tools
python3 -c "import wp; print(wp.U)"          # must print the AAD URL
python3 publish_services.py                   # builds + pushes the 13 service pages as drafts (records IDs in created.json)
python3 publish_services.py --assets          # also re-pushes home page + header/footer templates (CSS/JS live in them)
```
Python 3 only (stdlib). Playwright/Chromium preview helpers: `prev.py`, `shotp2.js`, `sheet.py`, `live.js` (launch Chromium with the HTTPS proxy + `ignoreHTTPSErrors`).

## Design decisions (agreed with user)
- Fonts: **Outfit** (headings, buttons, menu) + **Figtree** (body) — from reference site easypickinglocksmith.co.uk (inspiration only, not copied).
- Colours (Elementor kit): navy `#011D5E`, footer navy `#010F35`, orange `#FE6402`, text `#4B546E`, cream `#FAF9F5`, light `#F4F6FA`.
- All headings capitalised; two-tone headings (second half orange gradient via `<span class="x-hl">`).
- All buttons have icons (phone / quote / paper-plane / arrow).
- Service cards = tall photo cards w/ number badge + round orange arrow (reference style), smooth hover.
- Animations: scroll reveal (`.rv`), scroll progress bar, card tilt (desktop), sticky shrinking header, pulse CTAs; respects reduced-motion.
- SEO: one H1 per page, alt text on all media (set in library), FAQ schema (accordion `faq_schema`), LocalBusiness JSON-LD (header template only), aria-labels on icon buttons. User adds Yoast meta titles/descriptions themself.
- Google reviews section uses shortcode `[trustindex no-registration=google]`.

## What exists on the AAD site (IDs in `tools/created.json`)
| Item | ID | Status |
|---|---|---|
| New Home (Canvas template, header/footer embedded) | 1208 | published; user temporarily unset it as front page while reviewing |
| Header template (site-wide) | 1202 | published, include/general |
| Footer template (site-wide) | 1203 | published, include/general |
| Old header/footer | 241 / 272 | conditions removed |
| Redesign drafts: About 1215, Contact 1216, Emergency 1217, Towing 1218, Flatbed 1219, Privacy 1220, Cookie 1221, Services hub 1222 | | drafts (built from existing page content) |
| 13 new service pages from Google Doc | — | **built locally (`built_services.json`), NOT yet on the site** |

Original-site backup (pages, posts, templates, media list, menus, settings) is in `tools/wp-backup/`.

## URL fix after go-live (2026-10-12)
- Site moved to **aadrecovery.co.uk**, but Elementor data still held 449 staging links (`darkblue-kudu-638106…`, `maroon-raven-160825…`) in 22 pages + 4 templates (menus/buttons/cards, header, footer), and the contact forms used the staging domain as from-address/name/subject.
- Fixed with `tools/fix_urls.py --apply` (dry run without `--apply`; re-running reports 0). Pre-fix copies of every changed item: `tools/wp-backup/pre-url-fix/`. Form from-address → `email@aadrecovery.co.uk`, name/subject → "AAD Transport And Recovery". Admin user's Website field (used in Yoast author schema) → live domain. GUIDs left as-is (WP convention).
- Crawl after fix: all 26 sitemap/internal pages 200, no broken internal links or assets, no staging URLs; http:// and www. 301 to https://aadrecovery.co.uk/; all original-site URLs still resolve.
- Still open: contact forms send to `ahsanhashmi1925@gmail.com` (switch to the client's inbox?); default "Hello world!" post is published and in the sitemap; Elementor → Tools → Clear Files & Data + LiteSpeed purge-all recommended so generated CSS/cache rebuilds.

## Form recipients (2026-10-12)
- All 19 Elementor forms (13 service pages, Towing/Flatbed/Emergency, Contact, Home 1208, old Home template 21) now email `ahsanhashmi1925@gmail.com, info@aadrecovery.co.uk` (Email + Email 2 "To"). Script: `tools/form_recipients.py ADDRESS [--apply]`; backups in `tools/wp-backup/pre-form-recipients/`.

## Blog (2026-10-12)
- Page **Blog** (ID 1303, `/blog/`) set as the WordPress posts page.
- Theme Builder templates, built by `tools/build_blog.py` (`--publish` creates/updates them; IDs in `created.json`), styles in `tools/blog.css`:
  - **Blog – Archive (Listing)** ID 1304, condition *All archives* (blog page, categories, tags, author, date, search). Hero with archive title (fallback "Recovery Tips & News" on /blog/), Archive Posts widget (cards, 3/2/1 cols, pagination), CTA.
  - **Blog – Single Post** ID 1306, condition *Posts*. Hero (title, date, category), article card (featured image, content, tags, share, prev/next), sticky aside (auto table of contents from H2–H4 + 24/7 call card), related posts (hidden when none), CTA.
  - Both use page template `elementor_header_footer`; blog.css also stretches Astra's narrow/separate post container only on pages containing `.x-blog`. Alternative without CSS: Astra Customizer → Blog → Single Post → container *Full Width*.
  - Templates were created with `wp/v2/elementor_library` + conditions via `elementor/v1/site-editor/templates-conditions/{id}` (that endpoint also refreshes Elementor's conditions cache). Clear CSS with `DELETE elementor/v1/cache`.
- Menu: the header is a custom HTML mega-menu (not the WP menu), so Blog was added by `tools/add_blog_nav.py` to the desktop nav + mobile drawer (template 1202 and Canvas home 1208) and to the footer Company links (1203 + 1208). Also added to WP menu "Mian" (item 1308) for completeness. Backups: `tools/wp-backup/pre-blog-nav/`.
- Author was left out of the post meta because the admin user's display name is their email; the author archive slug also contains the email.
- Only the default "Hello world!" post exists; replace it with real articles (set a featured image for best cards).

## Open issues / next steps
1. **Boxed hero on inner pages (Elementor Full Width template):** cause = stale Elementor per-post CSS (element IDs changed between rebuilds). User does NOT want extra CSS hacks. Agreed approach (pending user confirmation): keep site-wide header/footer, keep element IDs stable (builders now seed `random` per page — `build_services.py` uses `random.seed(slug)`; apply same to `build_pages.py`), then user runs **Elementor → Tools → Clear Files & Data** once.
2. Publish the 13 service pages as drafts → screenshot desktop + mobile → user review.
3. Add new service pages to the Services menu (menu "mian", id in `wp-backup/menus.json`) and link matching cards on Home/Services hub.
4. Car Lockout & Roadside Assistance sections in the doc have no FAQ/CTA — a generic closing CTA was added; tell the user.
5. On approval: copy each redesign draft's `_elementor_data` into the ORIGINAL page IDs (keeps URLs/SEO), then delete drafts.
6. Old home page (ID 25) still published at `/home/` (duplicate content) — suggested setting it to draft; awaiting user.
7. Site title is still the raw domain (user handling metas). WordPress "Discourage search engines" was on (user removing).
8. Elementor element caching was disabled by the user during the redesign — remind to re-enable at the end.

## Tool overview (`tools/`)
- `build.py` — home page + header/footer templates; holds shared helpers (C/W/H/T/BTN…) and the CSS/JS asset widget (reads `redesign.css`, `redesign.js`).
- `build_pages.py` — redesigns existing inner pages from their Elementor data (+ Services hub).
- `parse_doc.py` — parses `gdoc.html` → `doc_pages.json` (handles inconsistent heading levels, tables, notes cut-off).
- `build_services.py` — builds the 13 service pages with varied sections (split+photo, navy checklist, tick tiles, feature/numbered/dark cards, steps, destination panel, areas+photo, 24/7 phone band, comparison table, reviews, FAQ, CTA). Image picks per page in `IMGS`.
- `publish_services.py` — build + push drafts. `pushpages.py` — push inner-page drafts.
- Layout classes are self-contained (`x-dr`/`x-dc`/`x-bx` + `e-no-lazyload`) so pages don't depend on Elementor's generated CSS.
