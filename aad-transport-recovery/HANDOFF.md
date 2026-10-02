# AAD Transport & Recovery — WordPress Redesign Handoff

Site: **https://maroon-raven-160825.hostingersite.com** (WordPress + Astra child + Elementor / Elementor Pro, Yoast, Trustindex)
Content source for new service pages: Google Doc https://docs.google.com/document/d/1tm9CqX6-TecfKiAPSj79lJA-qgvueNt4NuKzKEHdxTg/edit (copy saved as `tools/gdoc.html`, parsed to `tools/doc_pages.json`)

## ⚠️ Before doing anything in a new session
1. Credentials come from env vars only — **`AAD_WP_URL`, `AAD_WP_USER`, `AAD_WP_APP_PASSWORD`** (preferred) or `WP_URL`/`WP_USER`/`WP_APP_PASSWORD`. Never paste them in chat.
2. `tools/wp.py` **refuses to run unless the host is `maroon-raven-160825.hostingersite.com`** (override with `AAD_EXPECTED_HOST` only if the AAD site has genuinely moved). This guard exists because a previous session's env pointed at a different client site (`hotpink-lobster-615998…`, a medical site); 13 drafts were accidentally created there and were immediately and permanently deleted (verified).
3. Always work on drafts; never overwrite live pages without the user's OK.

## How to resume
```bash
cd aad-transport-recovery/tools
python3 -c "import wp; print(wp.U)"          # must print the AAD URL
python3 publish_services.py                   # builds + pushes the 13 service pages as drafts (records IDs in created.json)
python3 publish_services.py --assets          # also re-pushes home page + header/footer templates (CSS/JS live in them)
python3 apply_metas.py                        # sets Yoast SEO title + meta description on the 13 service pages
python3 link_pages.py [--apply]               # internal links (cards + first in-text mention), patches LIVE data; publish_services.py runs it automatically
```
Python 3 only (stdlib). Playwright/Chromium preview helpers: `prev.py`, `shotp2.js`, `sheet.py`, `live.js` (launch Chromium with the HTTPS proxy + `ignoreHTTPSErrors`).

## Design decisions (agreed with user)
- Fonts: **Outfit** (headings, buttons, menu) + **Figtree** (body) — from reference site easypickinglocksmith.co.uk (inspiration only, not copied).
- Colours (Elementor kit): navy `#011D5E`, footer navy `#010F35`, orange `#FE6402`, text `#4B546E`, cream `#FAF9F5`, light `#F4F6FA`.
- All headings capitalised; two-tone headings (second half orange gradient via `<span class="x-hl">`).
- All buttons have icons (phone / quote / paper-plane / arrow).
- Service cards = tall photo cards w/ number badge + round orange arrow (reference style), smooth hover.
- Animations: scroll reveal (`.rv`), scroll progress bar, card tilt (desktop), sticky shrinking header, pulse CTAs; respects reduced-motion.
- SEO: one H1 per page, alt text on all media (set in library), FAQ schema (accordion `faq_schema`), LocalBusiness JSON-LD (header template only), aria-labels on icon buttons. Yoast meta titles/descriptions for the 13 service pages are set from the Google Doc (`tools/service_metas.json`, applied by `tools/apply_metas.py` via Yoast's `bulk_editor/update_search` route + a re-save so the indexable refreshes; plain REST `meta` writes to `_yoast_*` are silently ignored). Other pages' metas: user handling.
- Google reviews section uses shortcode `[trustindex no-registration=google]`.

## What exists on the AAD site (IDs in `tools/created.json`)
| Item | ID | Status |
|---|---|---|
| New Home (Canvas template, header/footer embedded) | 1208 | published; user temporarily unset it as front page while reviewing |
| Header template (site-wide) | 1202 | published, include/general |
| Footer template (site-wide) | 1203 | published, include/general |
| Old header/footer | 241 / 272 | conditions removed |
| Redesign pages: About 1215, Contact 1216, Emergency 1217, Towing 1218, Flatbed 1219, Privacy 1220, Cookie 1221, Services hub 1222 | | published (these now own the live URLs) |
| 13 new service pages from Google Doc | 1267–1279 (slug→ID in `created.json` → `svc`) | **published** 2026-10-02 (template `elementor_header_footer`), Yoast metas set |

Original-site backup (pages, posts, templates, media list, menus, settings) is in `tools/wp-backup/`.

## Open issues / next steps
1. **Boxed hero on inner pages (Elementor Full Width template):** cause = stale Elementor per-post CSS (element IDs changed between rebuilds). User does NOT want extra CSS hacks. Agreed approach (pending user confirmation): keep site-wide header/footer, keep element IDs stable (builders now seed `random` per page — `build_services.py` uses `random.seed(slug)`; apply same to `build_pages.py`), then user runs **Elementor → Tools → Clear Files & Data** once.
2. ~~Publish the 13 service pages~~ (done, IDs 1267–1279, live).
3. ~~Menu~~ done: header now has a custom **mega menu** (desktop) + slide-in **drawer** (≤1024px) and a rebuilt footer listing every service. All generated from `MENU` in `build.py` — edit that list and run `python3 publish_services.py --assets`. The WordPress menu "mian" (Appearance → Menus) is **no longer used** by the header. Cards on Home/Services hub/About + in-text mentions now link to the service pages (`link_pages.py`).
4. Car Lockout & Roadside Assistance sections in the doc have no FAQ/CTA — a generic closing CTA was added; tell the user.
5. On approval: copy each redesign draft's `_elementor_data` into the ORIGINAL page IDs (keeps URLs/SEO), then delete drafts.
6. Old home page (ID 25) still published at `/home/` (duplicate content) — suggested setting it to draft; awaiting user.
7. Site title is still the raw domain (user handling metas). WordPress "Discourage search engines" was on (user removing).
8. Elementor element caching was disabled by the user during the redesign — remind to re-enable at the end.

## Tool overview (`tools/`)
- `build.py` — home page + header/footer templates (mega menu/drawer HTML from `MENU`, `mega_html()`); holds shared helpers (C/W/H/T/BTN…) and the CSS/JS asset widget (reads `redesign.css`, `redesign.js`).
- `build_pages.py` — redesigns existing inner pages from their Elementor data (+ Services hub).
- `parse_doc.py` — parses `gdoc.html` → `doc_pages.json` (handles inconsistent heading levels, tables, notes cut-off).
- `build_services.py` — builds the 13 service pages with varied sections (split+photo, navy checklist, tick tiles, feature/numbered/dark cards, steps, destination panel, areas+photo, 24/7 phone band, comparison table, reviews, FAQ, CTA). Image picks per page in `IMGS`.
- `publish_services.py` — build + push drafts. `pushpages.py` — push inner-page drafts.
- Layout classes are self-contained (`x-dr`/`x-dc`/`x-bx` + `e-no-lazyload`) so pages don't depend on Elementor's generated CSS.

## Notes (2026-10-02, later)
- **Never rebuild the redesign pages (1215–1222) with `build_pages.py` + `pushpages.py`**: the Towing page (1218) was edited by the user in Elementor on 2026-09-30, and `build_pages.py` still re-randomises element IDs. Patch live data instead (as `link_pages.py` does).
- Content width: boxed containers are 1440px (was capped at 1240px in `redesign.css`; Elementor kit already 1440px).
- Hero form card: sized to content + `position:sticky` (desktop); hero uses `overflow:clip` so sticky works.
- Sticky header on inner pages fixed by making `[data-elementor-type="header"]` sticky (the inner `.x-header` was trapped in its 107px wrapper).
