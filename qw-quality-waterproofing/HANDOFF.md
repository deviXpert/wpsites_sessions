# Quality Waterproofing — Elementor Rebuild Handoff

New site (staging): **https://meteoric-cornflowerblue-pheasant-37.hostingersite.com** (WordPress + Astra + Elementor 4.4 / Elementor Pro "Advanced")
Old live site being replaced: https://qualitywaterproofinginc.ca · Client reference (for structure only): https://rccwaterproofing.com
Cloud environment: "Quality WaterProofing" (allowlist has the staging host, the old site and the reference site).

## ⚠️ Before doing anything in a new session
1. Credentials come from env vars only: `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. Never paste them in chat.
2. `tools/wp.py` and `tools/mcp.sh` **refuse to run unless the host is `meteoric-cornflowerblue-pheasant-37.hostingersite.com`** (override with `QW_EXPECTED_HOST` only if the site really moved). Other clients live in this repo.
3. `build.py` **overwrites** a page's Elementor data. If the user has edited a page in the Elementor editor, fetch the live `_elementor_data` and patch it instead of rebuilding.

## User requirements (agreed)
- Built in Elementor with **native widgets**; styling via widget controls + Global Colors/Fonts. Minimal CSS, kept in a global Elementor place.
- Focus areas: Toronto/GTA, Mississauga, Brampton, St. Catharines (added later, Niagara Region), North Bay. Services: exterior waterproofing, interior waterproofing, sump pump, exterior foundation crack repair, underpinning (added later, `/underpinning/` – old-site slug kept), interlocking.
- Logo tagline "Our company will help protect your home's basement from water damage" is used only as text: opening line of the About story and the footer company blurb (also the JSON-LD `slogan`). No standalone tagline/logo band (user asked to remove it).
- **Light theme** (like the reference site): white / cream / light-grey sections. Header: dark top bar + **white main bar** (logo variant for light backgrounds, media 117 `logo_light`); footer stays dark with the original cut-out logo (media 55, dark backgrounds only). Hero photo banners keep a dark overlay for white text.
- Test note: headless Chromium reports touch mode, so SmartMenus dropdowns don't open on synthetic hover in Playwright. Real desktop hover works.
- Images: client photo zips + photos from the old site. The user will revise copy later.

## Design system (Elementor kit, post 5, written by `tools/kit.py`)
- Colours: Ink `#0E1420` (primary), Gold `#C9A24B` (secondary), Steel blue `#2B5EA7` (accent), text `#4B5565`, plus custom: Ink card `#161E2D`, Gold light/dark, Blue dark, Cream `#F7F4EC`, Light `#EEF2F7`, Muted `#A9B3C4`, Line `#2A3448`.
- Content width **1440px** (kit). Side gutters: 20px on desktop/tablet, 16px on mobile, the same in header, sections and footer. Nested containers have 0 padding so everything lines up on one left edge.
- Favicon: QW mark on a dark rounded square (media 116, WordPress Site Icon).
- Fonts: **Sora** (headings/buttons/nav), **DM Sans** (body), **Cinzel** (serif eyebrows + tagline, matching the logo's tagline).
- Global typography presets: Hero H1, Section Title, Card Title, Eyebrow, Tagline, Body, Lead, Small, Button, Stat, Nav.
- **Custom CSS** (≈10 lines) lives in **Site Settings → Custom CSS** (kit `custom_css`): `.qw-hl` gold highlight words in headings, `.qw-hl-ink`, card hover lift. Elementor → Custom Code could not be used because its code and location fields can't be written over REST; to move it there, paste the same CSS into a Custom Code snippet in wp-admin.
- Sections carry the classes `qw-dark` / `qw-light` (set in the native "CSS Classes" field) so the highlight colour adapts.
- Logo: transparent PNG cut from the client logo (media 55). It is designed for dark backgrounds only.
- Home hero: background video loop (media 56, ~1.4 MB, built from 3 client clips) with a dark gradient overlay.

## IDs
| Item | ID |
|---|---|
| Header (Theme Builder, entire site) | 60 |
| Footer (Theme Builder, entire site) | 61 |
| Pages | see `tools/pages.json` (Home 63 = front page) |
| Menu "QW Main Menu" (slug `qw-main-menu`) | 4 – all items link to their pages (demo mode ended; `restore_menu.py` + `menu_backup.json` kept in case placeholder mode is needed again). Footer links are generated only for published pages (`live()` in build.py). |
| Media | see `tools/media.json` (key → id/url); sources + alt text in `tools/media_src.py` |

Pages (**all 15 published** – client demo mode ended; `build.py`/`yoast.py` keep each page's current status; Astra full-width / no title, template `elementor_header_footer`): Home, About, Services hub, 6 service pages (`/underpinning/`, `/exterior-waterproofing/`, `/interior-waterproofing/`, `/sump-pump-installation/`, `/foundation-crack-repair/`, `/interlocking/`), 5 location pages (`/basement-waterproofing-toronto|mississauga|brampton|st-catharines|north-bay/`), Projects (filterable gallery), Contact.

## How to rebuild / resume
```bash
cd qw-quality-waterproofing/tools
python3 build.py --dry all           # build JSON locally into out/
python3 build.py home contact        # push only some parts (header, footer, home, services, about-us, projects, contact, <slug>)
python3 kit.py && ./mcp.sh elementor/publish-document '{"post_id":5}'   # kit changes (always sends the full settings)
node shot.js /exterior-waterproofing/ /tmp/x.png [m]                   # Playwright screenshot (m = iPhone)
node overflow.js 360 390 768 1024 1440 1920                            # horizontal-overflow sweep of every page
node align.js /basement-waterproofing-toronto/                          # left-edge alignment check
python3 yoast.py                                                        # push Yoast metas (run after build.py)
```
- `el.py` = widget helpers (C/SECTION/H/T/BTN/IBOX/CARD/SERVICE_CARD (Pro CTA widget)/FAQ (accordion + FAQ schema)/FORM (Pro form)/…). Element IDs are seeded per page, so rebuilds keep the same IDs.
- `content.py` = all service + location copy (signs, steps, benefits, galleries, FAQs, neighbourhoods).
- After pushing, `build.py` calls MCP `elementor/clear-cache` (**required** – Elementor caches rendered HTML, so without it the live page keeps showing old content; `mcp.sh` now auto-reconnects when the MCP session expires); CSS is regenerated on the next page view.
- Elementor lazy-loads background images and gallery thumbnails. Screenshots need a slow scroll (shot.js already does this).

## SEO done
- One H1 per page with the keyword + city; H2/H3 hierarchy; descriptive image filenames and alt text in the media library.
- FAQ accordions output FAQPage schema. A LocalBusiness (HomeAndConstructionBusiness) JSON-LD sits in an HTML widget in the header template (areas served, services, social).
- Internal linking: services ↔ locations ↔ contact, plus the footer link lists.
- `seo_meta.md` lists meta titles and descriptions for every page, and the 301 redirect map from the old URLs.

## Open items / to confirm with client
1. **Yoast is installed** and every page's SEO title, meta description, focus keyphrase and social title/description are set by `tools/yoast.py` (Yoast bulk-editor REST). That endpoint only writes post meta, so the script re-saves each page to refresh Yoast's indexables. Pages show `noindex` because WordPress "Discourage search engines" is on; turn it off at launch. Set up the 301 redirects in `seo_meta.md` at go-live.
2. **Form emails** go to the WordPress admin email (default). Set "Email To" in the form widgets (Home hero, service/location pages, Contact) to the client's address. Submissions are also saved under Elementor → Submissions.
3. Claims used: "10+ years residential & commercial experience" and "free estimates" (both from the old site). The old About page also claimed "since 1961" and a "Consumer's Choice Award 25 years". These contradict the 10+ years and look like template text, so they were **not** used. No warranty terms, review counts or testimonials were added. Add real Google reviews when available.
4. No street address or hours on the old site, so the site uses service areas only. Add NAP details to the footer and the JSON-LD if the client has a business address.
5. Old-site services not requested (underpinning, walkouts, concrete, landscaping) are only mentioned in About/FAQ text.
6. The "Hello world!" post and the draft Privacy Policy page are still the WordPress defaults. A privacy policy page should be written before launch.
7. WordPress "Search engine visibility" was not changed. Check it at launch.

8. **Underpinning media:** real client footage (4 WhatsApp videos, Nov 19). Stills `up_*` (media 125–131) were pulled from the sharpest video frames (768px – fine for cards/gallery). Hero = 10s loop `up_video` (media 132). The Projects page has an Underpinning filter tab. The client also sent 3 underpinning photos as pasted images; they weren't received as files, so they still need adding.
