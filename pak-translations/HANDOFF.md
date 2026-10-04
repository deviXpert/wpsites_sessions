# Pak Translations — Elementor Redesign Handoff

> **Start here in a new session.** Say "continue pak-translations" and read this file first.
> Git branch for this site: **`pak-translations`** (the user wants each site's branch named after the website).
> Full history of what was done and why: [`SESSION_LOG.md`](SESSION_LOG.md).

| | |
|---|---|
| Live site | **https://pak-translations.com** (LIVE production site — every change is public) |
| Stack | WordPress · Astra child theme · Elementor 4.3.x + Elementor Pro 4.3 · Yoast SEO · WP Mail SMTP · Loginizer · Security Optimizer · Wordfence (inactive) · Classic Editor |
| Hosting | Hostinger (CDN "hcdn" in front — purge in hPanel after big changes) |
| Status | **Redesign complete and LIVE** (all 8 pages, site-wide header/footer) as of 2026-10-03 |
| Owner contact on site | Dr. Muhammad Salman Riaz · WhatsApp +92 337 1440929 · info@pak-translations.com · Gujrat, Punjab, Pakistan |
| Developer credit | Footer: "Powered by hafizahsanali.com" (user request — keep it) |

---

## 1. Before doing anything in a new session
1. **Credentials come only from environment variables**: `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` (optionally prefixed `PAK_`). Never print or commit them.
   `tools/wp.py` **refuses to run unless the host is `pak-translations.com`** (override with `PAK_EXPECTED_HOST` only if the site moved). If the env points at another site, stop and ask the user.
2. Check access: `cd pak-translations/tools && python3 -c "import wp; print(wp.req('wp/v2/users/me')['name'])"` → `admin`.
3. Python 3 stdlib only for REST. Screenshots need Node + Playwright (preinstalled; Chromium at `/opt/pw-browsers`). Image work used `pip install pillow "rembg[cpu]"`.
4. This is LIVE: for risky changes preview first (see §4), and tell the user what will change.

## 2. Rules agreed with the user (keep following these)
- **Only core Elementor + Elementor Pro widgets** (container, heading, text-editor, button, image, icon, icon-box, icon-list, counter, accordion, form, testimonial-carousel, nav-menu, social-icons, google_maps, html). The user **deleted** Master Addons, PowerPack, Premium Addons, Transition Slider, Sticky Header Effects, All-in-One WP Migration — never reintroduce addon widgets.
- **All forms = Elementor Pro Form widget.**
- **Fonts:** Outfit (headings/buttons/nav) + Figtree (body). **Colours** (from logo): green `#6DB52E`, dark green `#2F6E14`, yellow `#F8C300`, ink `#0B1A10`, text `#4A5560`, light bg `#F5F8F1`. Set as Elementor globals too.
- Modern UI: dark hero with grid + glows, gradient-highlight headings (`<span class="x-hl">`), pill eyebrows, cards with hover lift + mouse spotlight, scroll reveal (`rv`, `rv-l`, `rv-r`, `rv-s`, `rv-st` stagger), scroll progress bar, sticky shrinking header, language marquee, animated counters, floating WhatsApp button. Respects `prefers-reduced-motion`.
- **SEO:** one H1 per page, Yoast title (≤ ~65 chars) + description (≤ ~160) + focus keyphrase + social title/description, alt text on every image, FAQ schema (accordion `faq_schema`), ProfessionalService JSON-LD on home, share image as featured image.
- Content may be rewritten for SEO but **only with facts from the business** (no invented claims). "120+ languages" = the real list (121).
- Desktop content container width **1440px**. Pages must be full width (Astra container neutralised).
- Ask before deleting things; the user explicitly approved every deletion so far.
- When the user sends several comments, **note them all first and wait for "go"** before changing anything.
- Commit + push after each round to branch **`pak-translations`** (also mirror to the session's designated branch if the harness requires it).

## 3. What is on the site now
| Page | ID | URL | Module | Form → recipient |
|---|---|---|---|---|
| Home (front page) | 39107 | `/` | `tools/home.py` | Free quote → info@ |
| About | 611 | `/about-us/` | `about.py` | — |
| Services (11 anchored sections `#localization`, `#document-translation`, `#certified-translation`, `#editing-proofreading`, `#transcription`, `#interpreting`, `#subtitling`, `#content-creation`, `#language-material`, `#linguistics`, `#desktop-publishing`) | 673 | `/services/` | `services.py` | — |
| Languages (11 region cards) | 633 | `/languages/` | `languages.py` | — |
| Samples / case studies | 988 | `/sample/` | `samples.py` | — |
| Career | 693 | `/career/` | `career.py` | Application (CV upload) → info@ |
| Contact (+ Google map) | 706 | `/contact-us/` | `contact.py` | Contact → **hr@** |
| Your Order | 319 | `/your-order/` | `order.py` | Order (6 uploads) → info@ |
| Header template (site-wide; **holds all CSS/JS/fonts** in an HTML widget) | 33 | include/general | `lib.header()` | |
| Footer template (site-wide) | 37 | include/general | `lib.footer()` | |
| Old header (inactive, condition page #104) | 27 | — | untouched | |

- All pages: template `elementor_header_footer`, Astra meta `ast-site-content-layout=full-width-container`, featured image = share image (media **39126**).
- Media added: **39125** founder photo on dark bg (`/wp-content/uploads/2026/10/founder-dr-salman-riaz.jpg`), **39126** social share image. Local copies in `assets/`.
- Forms: `save-to-database` + email actions, honeypot field, phone fields are text (Elementor tel rejects spaces), custom success message. Submissions visible in wp-admin → Elementor → Submissions.
- Menu "Menu" (id 3, location primary): Home 919 → page 39107, About 920, Services 921, Samples 991, Languages 922, Career 923, Contact 924.
- Elementor experiment **Flexbox Container = active** (enabled this project). Active kit **26951** (all duplicate kits deleted).
- Yoast metas set for all 8 pages (see `SEO` tuples in each module; home's in `golive.py` `HOME_SEO`).
- Old home (530) is in WP Trash; `/home/` 301s to `/`.

## 4. How to change things
```bash
cd pak-translations/tools
# edit page module / lib.py / pt.css / pt.js, then:
python3 golive.py services            # republish one or more pages (sets Yoast meta, clears Elementor cache)
python3 golive.py                     # header + footer templates + ALL pages
# CSS/JS only? they live in the header template:
python3 -c "import wp,json; from lib import header; wp.req('wp/v2/elementor_library/33','POST',{'meta':{'_elementor_data':json.dumps([header()])}}); wp.req('elementor/v1/cache','DELETE')"
```
- **Always clear Elementor cache** after REST updates (`DELETE elementor/v1/cache`) — the element cache otherwise serves stale HTML. `golive.py` does this.
- **Hostinger CDN** can keep serving an old copy at the bare URL (it once served the old spam home for hours). Verify with a plain request (no `?nc=`), and ask the user to purge in hPanel.
- **Preview before risky changes:** `python3 push_preview.py <module>` → password-protected `/redesign-preview-<module>/` (Canvas template, header/footer embedded; password in git-ignored `tools/preview_state.json`). Delete preview pages afterwards. Never preview `home` this way (would re-password the live page).
- Do **not** `import golive` from other scripts — it runs the publish on import.
- New page: create module with `TITLE`, `SEO=(title, description, keyphrase)`, `build()` returning a list of sections; add it to `PAGES` in `golive.py` (create the WP page first if it doesn't exist).

### Library (`tools/lib.py`)
- Primitives: `C(els, cls, d='row'|'col'|'grid', box=True)` container (layout via our own classes `x-dr/x-dc/x-grid/x-bx`, never relying on Elementor generated CSS), `W`, `H`, `T`, `P`, `EB` (eyebrow), `BTN`, `IMG`, `IBOX`, `ILIST`, `RAW`, `F`/`FORM`/`quote_form`.
- Sections: `sec`, `head`, `phero` (inner-page hero with breadcrumb + H1), `split`, `faq_sec`, `cta_sec`, `steps_sec`; `header()`, `footer()`, `SERVICES` list, contact constants (`PHONE`, `WA`, `EMAIL`, `ADDRESS`, `FB`, `TW`, `PROZ`).
- `seed('<page>')` keeps Elementor element IDs stable between rebuilds.
- Design system: `tools/pt.css` (later rules override earlier ones — appended "fix" blocks at the bottom), `tools/pt.js` (reveal, progress bar, spotlight).

### QA tools
| Script | Purpose |
|---|---|
| `node tools/shot.js <url> prev/name [password]` | full-page desktop (1440) + mobile (390) screenshots; prints horizontal-overflow offenders |
| `node tools/shot1920.js <url> out.png [selector]` | 1920px viewport shot |
| `python3 tools/slice.py img.png 1800` | slice tall screenshots for viewing |
| `python3 tools/linkcheck.py` | crawl all pages, check internal/external links + #anchors (Facebook/ProZ block bots — fine in browsers) |
| `python3 tools/metaaudit.py` | title/description lengths, canonical, robots, OG/Twitter, H1 count, missing alt |
| `node tools/formtest.js <file>` | submits each form once (TEST) — `ONLY=/,/your-order/` to limit; sends real emails |
| `node tools/faqtest.js` | opens every FAQ item and checks column widths stay constant |

## 5. Security notes (site was SEO-spam hacked)
- Removed: hidden spam-link HTML widget + 2 casino text widgets (old home), 3 spam essay pages (2617, 2603, 1142), 11,094 orphaned spam categories, 37 duplicate Elementor kits.
- The injection source was **not** found/fixed. User was advised to change WP admin + hosting passwords, update plugins, re-enable Wordfence and scan. Re-check for spam after any CDN purge: `curl -s https://pak-translations.com/ | grep -ciE 'casino|garuda|hatori|mostbet'`.
- Original-site backup (pages incl. old Elementor data, templates, media list, menus, settings, categories) in `tools/wp-backup/` (taken before any change).

## 6. Open items / ideas for next session
- [ ] **PUBLISH PENDING (2026-10-04):** client round 3 + home edits (commits 98b2e37, 1a75da3) are built but NOT live. Run `python3 golive.py` (header, footer, all pages) once REST auth works. Last attempt: `WP_URL` = pak-translations.com but every authenticated REST call returns `401 rest_not_logged_in`, even with a bogus username. That means WordPress never processed the Basic auth header. Likely causes: a stale application password, or the header being stripped by the host/CDN/security plugin.
- [ ] Confirm the user received the 4 TEST form emails (WP Mail SMTP delivery).
- [ ] Optional cleanup: old saved templates 171, 97, 71, 64, 54, 47 and old header 27 (unused) — ask before deleting.
- [ ] Optional: blog/insights section for SEO content (no posts exist yet), Google Business Profile link, Urdu landing page.
- [ ] Security scan follow-up (Wordfence) — ask the user for results.
- [ ] Re-run `linkcheck.py`, `metaaudit.py` and mobile screenshots after any big change.
