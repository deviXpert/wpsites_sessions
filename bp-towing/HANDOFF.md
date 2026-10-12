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
