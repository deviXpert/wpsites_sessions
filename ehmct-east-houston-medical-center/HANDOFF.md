# East Houston Medical Center (EHMC) — Elementor Build Handoff

Site: https://hotpink-lobster-615998.hostingersite.com (WordPress + Astra + Elementor 4.3 / Elementor Pro, Yoast SEO, Trustindex Google reviews)
Design source: Figma file "East Houston Medical Center" (key in env `FIGMA_FILE_KEY`)
Live reference for contact/social info: https://ehmct.com

## ⚠️ Before doing anything in a new session
1. Credentials come from env vars only — never paste them in chat.
2. `tools/el.py`, `tools/wp.sh` and `tools/mcp.sh` **refuse to run unless `WP_URL` is `hotpink-lobster-615998.hostingersite.com`** (override with `EHMC_EXPECTED_HOST` only if the site has genuinely moved). Another client (AAD, `maroon-raven-160825…`) lives in this repo; never mix the two.
3. The site is **live**. The user also edits in the Elementor editor — fetch live `_elementor_data` and patch it; don't regenerate pages from scripts without the user's OK.

## Credentials (never commit them)
Read from environment variables only:
- `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` – WordPress REST + MCP (application password)
- `FIGMA_ACCESS_TOKEN`, `FIGMA_FILE_KEY`, `FIGMA_NODE_ID`

## How the site is built
- **Classic Elementor flexbox containers** (not V4 atomic). The site's MCP endpoint
  (`/wp-json/mcp/mcp-adapter-default-server`, called via `scripts/mcp.sh`) only builds V4 atomic
  elements, so pages are written as `_elementor_data` JSON through the WP REST API (`el.put`).
- After every write, call `el.regen(post_id)` (MCP `elementor/update-page-settings`) so Elementor
  regenerates its CSS; then view the preview once (`scripts/warm.sh <id>`) – the CSS file is
  only generated on first view after a save.
- Global Colors / Global Fonts / kit defaults live in the Default Kit (post 7), defined in
  `scripts/kit.py`. Write the kit through MCP `update-page-settings` (a raw REST write does not
  regenerate kit CSS and an MCP save with partial settings can reset it – always send the full set).
- Content width is 1440px globally; header/hero content is also clamped to 1440 via custom CSS.

## IDs
| Item | ID |
|---|---|
| Home page (published, front page content) | 32 |
| Header (Theme Builder, Entire Site) | 33 |
| Footer – current white design (Entire Site) | 34 |
| Footer – old light design (draft, unassigned) | 782 |
| QA preview page (draft, temporary – can delete) | 41 |
| Nav menu "EHMC Primary" | 4 (mobile-only call item 749) |
| Fracture template page (user-built layout used for condition pages) | 556 |
| New condition pages (published) | see `tools/cond_ids.json` (691–712) |
| Other condition pages (user-built) | 123 abdominal-pain, 427 seizures, 472 burns, 527 trauma-injury, 529 chest-pain, 575 covid-19, 593 sore-throat, 649 flu |
| Community Events page (published, `/community-events/`) | 994 |
| Careers page (published, `/careers/`, Zoho Recruit job board embed) | 997 |
| Conditions page (published, `/conditions/`, Figma 436:46) | 1086 |
| Departments page (published, `/departments/`, Figma 436:1016) | 1089 |
| Request An Appointment (published, `/request-an-appointment/`, Elementor Pro form → dev@themaddex.com + Submissions) | 1154 |
| Site icon / favicon (Settings → site_icon; source in `assets/`) | media 2065 |
| News & Blogs listing (page 1081, Posts widget, 9/page, excludes post 1) | 1081 |
| Single Post template (Theme Builder, include/singular/post) | 2734 |
| Media | see `tools/media.json` (key → id/url); mobile hero photo 968, event gallery 980–992, careers photo 993 |

## Tools (`tools/`)
- **`patch.py` – the default way to change anything live**: `fetch(id[, 'elementor_library'])` → edit `doc['data']` →
  `save(doc)`. Backs up the live JSON to `backups/`, refuses to save if the post changed after the fetch, regenerates CSS.
- `mobile_hero.py` – mobile-only (≤767px) Figma match for home hero/dots/stats (32) and header pill (33). Only sets
  `*_mobile` keys and a CSS block between `/*m-figma*/` markers, so it is safe to re-run on live data.
- `header_call.py` – desktop Call button shows the number; mobile-only "Header – Mobile Actions" row under the logo
  pill (Figma: "View Our ER" → /#locations, "Call Now" → tel). Header also has `/*hdr-mid*/` CSS for 1025–1279px.
- `fix_banners.py` – mobile only: inner-page banners (page[0] > banner > content) start their content at 150px so it
  clears the header action row (ends y=138). Applied to all 24 inner pages; new pages with that banner need it too.
- Hero slider = 4 slides (`hero_slides.py`, idempotent): 1 EHMC building (desktop 1069, mobile 968), 2 hospital
  entrance, 3 aerial, 4 reception (media 1102–1107, desktop + mobile exported exactly as cropped in Figma 222:1468 /
  307:2103). Overlays per slide and breakpoint from Figma (`/*ov*/` CSS on each slide ::before); mobile slides 2–4
  use the darker main-artboard mobile overlay + a text band (Figma 80% overlay left the headline unreadable).
  Desktop/tablet dots per Figma (`/*d-dots*/`): 18px, active 38px #BE2424, aligned with the kicker.
- Conditions tabs (home): on mobile the active card's image opens directly below that card (flex `order` + `:has()`).
  Hidden tab images were lazy-loaded (fetched only on tap); HTML widget 'Conditions – Preload Tab Images'
  (absolute, inside 'Conditions – Grid') switches them to eager when the section is ~800px away (only the images
  visible at the current breakpoint).
- Conditions mobile (Figma 442:727): cards/image 353 wide (section 20px sides), 18px gaps, image 353x353 r18.
  Each tab has a mobile-only '… Illustration (Mobile)' square image (media 1056–1063, generated from the portraits
  with the subject zoomed out) and the portrait widget is hidden on mobile.
- Header buttons are equal height: 56px desktop/tablet (`/*eq-h*/`), 46px mobile. Mobile action row has explicit
  z_index 1 and the logo pill z_index 3 (containers inherit the header's --z-index:50, which covered the open menu).
- Desktop/tablet hero card frame per Figma 418:3: 8px #F2F3F6, radius 50, soft shadow 0 10px 30px rgba(4,38,72,.08) (`/*d-frame*/` CSS on 'Hero').
- Hero avatars use Figma crops (media 1014–1016) with CSS ring/shadow; hero card has a 4px #F1F2F3 curved outline.
- `figma_pages.py` – first build of /conditions/ and /departments/ (same refuse-to-overwrite rules). Condition cards
  link to their condition pages; desktop only in Figma, mobile = one column.
- `blog_templates.py` – first build of the blog listing (page 1081) and single-post template 2734 (content + sticky
  sidebar: recent posts + emergency CTA). `fix_post_images.py` copies post images missing on this site from ehmct.com
  (map in post_images.json) and sets featured images.
- `appointment_page.py` – first build of /request-an-appointment/ (fields from ehmct.com WPForms 632).
- `home_fixes.py` – flip-card hint removed, Baytown map → campus image (media 1115), slider rounded on `.swiper`
  (slides square, so no edges show mid-swipe).
- `qa_crawl.js` – full-site QA (run in a dir with pages.json from the REST API): overflow, broken images, `#` links,
  JS errors, 4xx responses, screenshots at 1440/393.
- `inner_pages.py` – first build of Community Events / Careers. Refuses to overwrite once built (`--rebuild-draft` only
  while still a draft). Careers' Zoho embed needs the `.embed_jobs_head` / `.embed_jobs_head3` wrappers; Zoho's own CSS is
  intentionally not loaded (our CSS overrides it).
- `el.py` – helpers: `C()` container, `W()` widget, `H()/T()/BTN()`, `put()`, `regen()`.
- `page.py` – full homepage generator (`python3 page.py page` writes page 32, `qa <id>` writes a full preview).
- `hf.py` – original header/footer generator. **Header has since been edited directly** (menu CSS for
  hover-delay dropdown grid with icons, mobile card menu) – read the live header before regenerating.
- `footer2.py` – current white footer (replaces container index 1 of footer 34, keeps the
  "Need Emergency Care Now" contact section at index 0). `footer2_dark.py` = dark variant.
- `clone.py` + `conds_content.py` – condition pages cloned from /fracture/ with new copy + Yoast meta.
- `shot.sh`, `qa.sh`, `warm.sh`, `mtest.js` – Playwright screenshots (trust proxy CA in Chromium NSS first).
- Run everything from inside `tools/` (scripts read their JSON files from the current directory). Figma text dumps are in `figma/`.

## WARNING before regenerating
The user also edits pages in the Elementor editor. Regenerating from these scripts overwrites
those edits. Always fetch the live `_elementor_data` first and patch it, or confirm with the user.

## Check-In
Header "Check-In Now" links to the GoRev pre-registration portal; the home Team card button is "Request an Appointment" → /request-an-appointment/
(same URL as ehmct.com), new tab. The header Check-In button is hidden on mobile.

## Open items
- Default 'Hello world!' post (id 1) still published – hidden from listing/sidebar; delete when the user agrees.
- Blog posts: no excerpts or categories set (listing uses 20-word auto excerpts; all 'Uncategorized').
- FAQ image media 24 was deleted; replaced by 1122 (Figma export).
- Mobile Figma pass done for header, hero (dots/kicker/title/pills/wait card/trust strip) and stats. Remaining home
  sections (Conditions, Team, Care Under One Roof, Reviews, Locations, FAQ) not yet compared section by section.
- Knee Pain page (743) section heading reads "Symptoms of SORE…" (copy slip from Sore Throat) – not touched.
- Figma stats icons are outline style; live uses solid Font Awesome icons (users, shield).
- Community Events / Careers are not in the nav menu yet (user renamed "Services" → "Conditions" on 2026-10-05).
- Headless Chromium renders 10px Poppins slightly wide (hero trust text wraps to 4 lines in screenshots only).
- Baytown location shows "Coming soon" – real details pending.
- Phone: (832) 400-2396 confirmed by the user (Contact Us 400-9662 fixed 2026-10-05).
- Reviews block "4.9 / 5 based on 1,200+" vs Trustindex shows 588 Google reviews.
- Hero desktop slide 2–4 sources in Figma are ~900px / 768px wide (upscaled on large screens) – ask for originals.
- TikTok link `@east.houston.medi` copied from ehmct.com – verify.
- Rotate the application password that was pasted in chat.
- Remaining Figma pages: About Us, Contact Us, more condition pages (knee pain, UTI, back pain, earache, nausea & vomiting).
