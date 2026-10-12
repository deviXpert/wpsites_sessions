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
