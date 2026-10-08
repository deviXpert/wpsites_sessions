# Jim Towing Ltd. — Website Redesign Handoff

Site: **https://jimtowing.ca** (WordPress + **Astra** theme + Elementor / Elementor Pro, Yoast, Trustindex, WPForms)
Content sources: Google Doc 1 (homepage SEO content) `src/doc1.txt`, Google Doc 2 (6 service pages) `src/doc2.txt`, old site page text `src/page_*.txt`, listing site `src/listing.txt`.

## Before doing anything in a new session
1. Credentials come only from env vars `WP_URL` / `WP_USER` / `WP_APP_PASSWORD` (or `JIM_`-prefixed versions). Never paste them in chat.
2. `tools/wp.py` **refuses to run unless the host is `jimtowing.ca`** (override with `JIM_EXPECTED_HOST`).
3. Everything is built as **drafts**. The live pages are untouched until the user approves go-live.

## How to rebuild / preview
```bash
cd jim-towing/tools
python3 publish.py                      # rebuild + push everything (header, footer, all drafts)
python3 publish.py header home pricing  # push only some parts (names: header footer menu home about services service-areas pricing contact <service-slug>)
python3 prev.py home        # desktop screenshot of a draft via Elementor's anonymous preview link -> ../shots/
python3 prev.py home m      # mobile (390px)
python3 tile.py home_d 3    # tile screenshot chunks for quick review
```
`publish.py` writes a tiny HTML comment into post_content on each push, which forces a new WP revision. Without it, Elementor preview links keep showing the old snapshot.
The CSS/JS live in the **header** template (`jim.css`, `jim.js`), so push `header` after editing them.

## Design system
- Brand from the logo: ink `#0B0D12`, red `#E1251B`, gold `#FFC20E`, paper `#F6F5F1`, cream `#FBFAF7`.
- Fonts: **Archivo** (variable width, used 108–125% for headings) + **Manrope** (body). Font Awesome 5.15.4 from cdnjs.
- Motifs: hazard checker stripes (from the logo), animated road line, skewed red marquee.
- Interactions: word-by-word hero reveal, scroll reveals, sticky shrinking/auto-hiding header, scroll progress bar, magnetic buttons, card tilt, animated counters, scrollytelling service explorer (sticky photo), "What happened?" situation tabs (keyboard accessible), steps road with a truck that follows the scroll, animated Alberta route map (SVG), infinite photo strip with lightbox, mobile bottom call bar, desktop floating call button, back-to-top progress ring. Respects `prefers-reduced-motion`.
- Layout classes are self-contained (`j-*`); containers use `content_width: full`, zero padding/gap, and CSS controls the layout. Nothing depends on Elementor's per-element style settings.
- Only the **client's own photos** are used: 12 from jim.deveterslistings.com (IMG_15xx–19xx), 2 from the Google Business Profile, and 4 WhatsApp photos already in the library. All are WebP with alt text. No stock or AI-generated images. Transparent logo: media 415.

## What exists on the site (IDs in `tools/created.json`)
| Item | ID | Status |
|---|---|---|
| Header site part | 428 | published, **conditions = only the redesign drafts** |
| Footer site part | 430 | published, same scoped conditions |
| Menu "Jim Main Menu" | 15 | custom links pointing at the FINAL URLs |
| Home (redesign) | 432 | draft |
| 6 service pages (children of Services 161) | 437–442 | draft — final URLs `/services/<slug>/` |
| About / Services / Service Areas / Pricing / Contact (redesign) | 447 / 448 / 449 / 450 / 451 | draft |

Backup of the original site (pages, media, settings, menus) is in `tools/wp-backup/`. Theme was switched from Twenty Twenty-Five to Astra by the user.

## Go-live checklist (needs the user's OK)
1. Copy `_elementor_data` (+ `_elementor_edit_mode=builder`, template `elementor_header_footer`) from each redesign draft into the ORIGINAL page IDs, which keeps the URLs: Home 152, Services 161, Service Areas 164, About 166, Contact 168, Pricing 274. Then delete those 6 drafts.
2. Publish the 6 service drafts (437–442).
3. Set `created.json` `"live": true` and run `python3 publish.py header footer`. This switches the header/footer conditions to `include/general`.
4. Old service URLs `/flatbed-towing/` (227), `/roadside-assistance/` (229), `/tire-change/` (231), `/fuel-delivery/` (233) need 301 redirects to the new `/services/...` URLs. There's no redirect plugin installed (suggest "Redirection").
5. Yoast titles and descriptions per page are in `created.json` → `seo` (taken from the Google Docs). The Yoast ability on this site can't set them, so enter them in the Yoast box or use another method.
6. Old draft "Home" (386) still exists — leave it or delete it.
7. Elementor → Tools → Clear Files & Data once after go-live.

## Content decisions / open questions for the client
- **[VERIFY] items in Doc 2 were left out**: EV flatbed, lockout proof-of-ownership, battery 3–5 year figure, battery replacement FAQ, fuel types/diesel, exact fuel amount. Calgary→Red Deer ≈150 km and →Edmonton ≈300 km were kept (geographic facts).
- **Pricing conflict**: the old Pricing page said roadside from $69 and flatbed from $89; the new docs say everything "starts at $75". The redesign uses $75 everywhere — confirm.
- Testimonials on the listing site look like placeholders, so none were used. Reviews section = Google rating badge (4.9 ★, 51 reviews) + `[trustindex no-registration=google]` shortcode, which shows nothing until the **Trustindex plugin is connected** to the Google profile.
- The "25% off first transaction" promo from the listing site was not used (unconfirmed).
- Forms (Elementor Pro) email **jimtowingltd@gmail.com** and save submissions (Elementor → Submissions). Confirm the recipient.
- The business has no public street address on Google (service-area business), so the map embed is centred on Calgary and links to the Maps profile.
