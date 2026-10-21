# KTC Towing — Home Page SEO Handoff

Site: **https://ktctowing.ca** (WordPress + Astra + Elementor / Elementor Pro, Yoast, LiteSpeed Cache, Trustindex)
Home page = page **1729** (`elementor_header_footer`). Header template 3707, footer 3713, gallery 4661, bottom form 3953.
Content source: `KTC_Towing_Homepage_Content_Final_Order.docx` (user upload, 2026-10-21).

## Before doing anything
- Credentials from env only: `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. `tools/wp.py` refuses to run unless the host is `ktctowing.ca`.
- Original home page data + templates backed up in `tools/wp-backup/` (restore: POST `meta._elementor_data` from `page-1729.json`).

## How to rebuild / re-push
```bash
cd ktc-towing/tools
python3 build.py                         # wp-backup/page-1729.json -> built_home.json
python3 -c "import wp;wp.post('wp/v2/pages/1729',{'meta':{'_elementor_data':open('built_home.json').read()}})"
# then clear Elementor CSS/element cache (empty response = OK):
python3 -c "import wp;wp.req('DELETE','elementor/v1/cache')"
node shot.js https://ktctowing.ca/ new   # desktop + mobile full-page screenshots in shots/
```

## Done (2026-10-21)
- No desktop/mobile duplicate sections remain. The only desktop-only content (service-areas card) now shows on every device. The remaining `elementor-hidden-mobile` items are a decorative divider and the header's top bar (address/email).
- Flip cards: the back side repeated the front title as a second `<h3>` (32 headings for 16 services), so the back title was removed. The Condo & Parkade card had a dead button and now links to the underground parkade page.
- Fixed duplicate headings ("Why the right truck" cards renamed). Result: 1 H1, 16 H2, no duplicate heading text.
- The second marquee was a word-for-word copy of the first and now lists service areas. Fixed a JS `const track` redeclaration error caused by the two marquee scripts.
- Heading hierarchy follows the doc. New sections from the doc: How it works (4 steps), Pricing, Towing by situation (7 cards), Winter towing. Section order follows the doc. Added areas Skyview/Inglewood/Beltline, 2 FAQs (FAQPage schema auto-updates, now 11 Qs), and the Section 5 CTA button.
- Alt text: 28 gallery images that had camera-filename alts (e.g. "WhatsApp Image...") or none, both logos, and image 1868 ("KTC Towing tow truck in Calgary").

## Open / for the user
1. Yoast meta description can't be set via REST. Paste the doc's version (adds "Call (587) 435-0770.") in Yoast on the home page.
2. Conflicting facts: counter "25 min Average Arrival" vs "about 20 minutes" in the text. Counter "25+ Years of Experience" vs `foundingDate: 2023` in the LocalBusiness schema (HFCM). Confirm and fix one side.
3. Doc items marked [VERIFY] were used as already on the site ($50 start, 20 min, flat-rate long distance). The doc's "93 Google reviews" and review quotes were not added as static text; the Trustindex widget already shows the live count.
4. `http://www` → `https://www` → `https://` is a 2-hop redirect (server/host level), which could be made one hop.
5. Yoast breadcrumb schema shows "Home > Home" on the front page (Yoast setting).
