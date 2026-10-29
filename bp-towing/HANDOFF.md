# BP Towing Service — Handoff

Site: **https://bptowingservice.ca** (Astra child + Elementor Pro). Creds via env `WP_URL` / `WP_USER` / `WP_APP_PASSWORD`.

Header: Elementor template **4486** ("BP Redesign — Header"). All design CSS/JS lives in its HTML widget `f4f1080` (`<style id="bp-ds">`).
Canvas pages embed 4486 directly; blog posts / archives / 404 use Theme Builder header **4523**, which embeds 4486 inside `.elementor-location-header`.

## 2026-10-12 — mobile menu fix
- Bug: on Theme Builder pages (blog posts), the menu opened as a 22px-wide strip. An `.elementor-location-header` override made the dropdown `position:absolute` with `width:auto`, so it took its width from the 46px hamburger widget.
- Also: tapping outside didn't close the menu, and the page behind it kept scrolling.
- Fix: added `<style id="bp-mobfix">` + `<script id="bp-mobfix-js">` to the end of widget `f4f1080` (source: `fix.css`, `fix.js`). The menu now closes on an outside tap, on Esc, or when you tap a link, and page scroll is locked while it's open.
- Rollback: `backup/header-4486-before-mobile-menu-fix.json` (`meta._elementor_data`).
- Not fixed: the Theme Builder header template 4523 embeds the full header; `/auto-towing/` renders the 404 template (that slug isn't a page).

## 2026-10-12 — site-wide check + clean-up
Crawled all 34 public pages/posts at 390px (mobile) and 1440px (desktop), checking: HTTP status, JS errors, failed requests, broken images, horizontal overflow, H1 count, internal links (`tools/crawl.js`, `tools/links.js`).

Fixed:
- **Long dashes (— / –) removed from all copy** (14 pages, 3 posts, header, 404 template), using `tools/dash.py` + `tools/apply.py` (dry run by default; `--go` writes). Rules: "Label – text" → "Label: text"; mid-sentence → comma, or a full stop + capital before "we/you/it…"; "Yes – we" → "Yes, we"; number ranges "20–35" → "20 to 35". Only visible text is touched (CSS, scripts, links and HTML comments are skipped). Ordinary hyphens and non-breaking hyphens (‑) are left as they are.
- Post 4437 (Calgary Zoo story) was stuck in Elementor "builder" mode with no data, so the Single Post template (hero, H1) didn't load → set `_elementor_edit_mode` to empty. Its in-body image (`tow-cars-1024x768.png`, media 4440) had been deleted → swapped for media 4439 `towing-services.jpeg` with alt text.
- Post 4280 (Ram 1500): 4 dead links (`/towing-calgary/`, `/services/flatbed-towing/`, `/services/accident-recovery/`, `/areas/se-calgary/`) → home / auto-towing page / plain text.
- Phone links `tel:(403) 991-2265` → `tel:+14039912265` (header 4486, footer 4487, Home 4478).
- Thank You page heading set to H1.

Not changed (tell user):
- Yoast SEO titles still use "–" as the separator (e.g. "Winch Out Service Calgary | Vehicle Recovery – BP Towing"). Change it under Yoast → Settings → Site basics → Title separator.
- One Google review avatar in the Trustindex widget sometimes fails to load (Google-hosted image, the plugin refreshes it).
- Backup of all content before this pass: `backup/all-content-2026-10-12.json.gz`.

## 2026-10-29 — Home areas section + Junk Car Removal page
- **Home (4478) areas section** (`78b5676`): rewritten from client notes. H2 "Towing Service Areas in Calgary & Surrounding Areas"; Calgary list (NW/NE/SE/SW/N/S/E/W/Downtown + "Balzac & CrossIron Mills Area"); "Nearby Cities & Communities: Pickup on Request" (Airdrie, Cochrane, Chestermere, Canmore, Banff, Okotoks); availability note + call CTA. Backup: `backup/home-4478-before-areas-update.json`.
- **New page 4580 `/junk-car-removal-calgary/`**: built by `tools/build_junk.py`, which copies the Long Distance Towing page (4529) layout and swaps in the client's copy. FAQ wording "BP Towing advertises…" changed to "Yes. BP Towing offers…". The H1 dash became a colon. Photos from the media library: 2281, 2434, 2867, 4418. Tips section removed, timeline cut to 4 steps (`bp-tl-4`).
- **Yoast title/description can be set through the API**: `POST /wp-json/yoast/v1/bulk_editor/update_search` with `{"items":[{"id":…,"seo_title":…,"meta_description":…,"focus_keyphrase":…}]}`. `GET /yoast/v1/bulk_editor/posts?content_type=page` lists the current values.
- Header widget CSS: added `<style id="bp-v9">` (4-column timeline, `.bp-note-c`, `.bp-list-1`, `.bp-areas-txt h3`).
- Not done yet: the new page isn't linked from menus (header mega menu 4486, mobile nav menu, footer services list 4487) or from the home "Cash for Junk Cars" card / junk-car blog post.
- **Junk Car Removal linked site-wide**: home "Cash for Junk Cars" card (now links; photo swapped to media 2434), Services hub card (page 32), header mega menu (new icon-box after Long Distance), mobile/WP menu "Menu 1" (id 34, child of Services, order 13; About/FAQ/Contact/Blog moved to 14 to 17), footer services list (also added the missing Special Vehicle Towing), blog post 4425 ("Cash for junk cars and scrap vehicles" bullet). Backups in `backup/*-before-junk-links.*`.
