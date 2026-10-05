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
| Media | see `tools/media.json` (key → id/url) |

## Tools (`tools/`)
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

## Open items
- Baytown location shows "Coming soon" – real details pending.
- Phone conflict: Figma shows 832-400-9662, live site uses (832) 400-2396 (currently used).
- Reviews block "4.9 / 5 based on 1,200+" vs Trustindex shows 588 Google reviews.
- New hero banners 2 & 3 from Figma are low-res (1000px / 768px).
- TikTok link `@east.houston.medi` copied from ehmct.com – verify.
- Rotate the application password that was pasted in chat.
- Remaining Figma pages: About Us, Contact Us, more condition pages (knee pain, UTI, back pain, earache, nausea & vomiting).
