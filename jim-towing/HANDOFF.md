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
- Fonts: **Outfit** (headings) + **Figtree** (body), applied site-wide (incl. plain h1–h6/body). Font Awesome 5.15.4 from cdnjs.
- Motifs: hazard checker stripes (from the logo), animated road line, skewed red marquee.
- Interactions: word-by-word hero reveal, scroll reveals, sticky shrinking/auto-hiding header, scroll progress bar, magnetic buttons, card tilt, animated counters, scrollytelling service explorer (sticky photo), "What happened?" situation tabs (keyboard accessible), steps road with a truck that follows the scroll, animated Alberta route map (SVG), infinite photo strip with lightbox, mobile bottom call bar, desktop floating call button, back-to-top progress ring. Respects `prefers-reduced-motion`.
- Layout classes are self-contained (`j-*`); containers use `content_width: full`, zero padding/gap, and CSS controls the layout. Nothing depends on Elementor's per-element style settings.
- Only the **client's own photos** are used: 12 from jim.deveterslistings.com (IMG_15xx–19xx), 2 from the Google Business Profile, and 4 WhatsApp photos already in the library. All are WebP with alt text. No stock or AI-generated images. Transparent logo: media 415.

## Status: LIVE (2026-10-08)
| Page | ID | URL |
|---|---|---|
| Home (front page) | 432 | `/` (slug `home`) |
| Services hub | 161 | `/services/` |
| 6 service pages | 437–442 | `/services/<slug>/` |
| Service Areas | 164 | `/service-areas/` |
| About | 166 | `/about/` |
| Contact | 168 | `/contact/` |
| Pricing | 274 | `/pricing/` |
| Header / Footer site parts | 428 / 430 | conditions `include/general` |
| Menu "Jim Main Menu" | 15 | custom links |

- The redesigns were copied into the original page IDs, so URLs are unchanged. `created.json` → `pages` now points at the live IDs and `"live": true`. `publish.py` only updates the build (Elementor data) on existing pages and never changes their title, slug, status or parent. Pre-go-live mapping is saved in `created.pre-golive.json`.
- Yoast SEO titles and descriptions are set through `POST yoast/v1/bulk_editor/update_search` (`items: [{id, seo_title, meta_description}]`). Values are in `created.json` → `seo`.
- Trashed (restorable from WP trash): redesign duplicates 447–451, old service pages 227 `/flatbed-towing/`, 229 `/roadside-assistance/`, 231 `/tire-change/`, 233 `/fuel-delivery/`. The user had already trashed the old Home 152 and draft 386.
- Old URLs: `/flatbed-towing/` and `/roadside-assistance/` 301 to the new pages automatically (WordPress slug guessing). **`/tire-change/` and `/fuel-delivery/` return 404.** They need a redirect plugin (e.g. Redirection) to point to `/services/roadside-assistance-calgary/` and `/services/emergency-fuel-delivery-calgary/`.
- Pricing (client decision): roadside help (jump-start, lockout, fuel, tire) **from $69**, local/emergency towing **from $75**, flatbed **from $89**, long distance = quote.
- Trustindex is connected (widget shows 14 reviews; Google profile shows 51, so the plugin may need a re-sync or upgrade to pull all).
- Content width 1440px (`.j-in`). Maps (footer, Contact, Service Areas) embed the business listing via `cid=5630118754390366668` (`MAP_EMBED` in lib.py) so Google shows "Jim Towing Ltd. 4.9★". Footer map is dark-styled (invert + hue-rotate keeps the pin red).
- Service pages: Key facts panel = `ticket_html()` in lib.py (icon rows, price block auto-extracted from the "Starting price" fact, call button); Quick answer = `quick()` in p_services.py (dark side panel + text + chips, price chip auto-extracted).
- Footer map band (business listing). The service ticker under the home hero is a flat dark strip of service links (no tilt).

## Content decisions / open questions for the client
- **[VERIFY] items in Doc 2 were left out**: EV flatbed, lockout proof-of-ownership, battery 3–5 year figure, battery replacement FAQ, fuel types/diesel, exact fuel amount. Calgary→Red Deer ≈150 km and →Edmonton ≈300 km were kept (geographic facts).
- **Pricing conflict**: the old Pricing page said roadside from $69 and flatbed from $89; the new docs say everything "starts at $75". The redesign uses $75 everywhere — confirm.
- Testimonials on the listing site look like placeholders, so none were used. Reviews section = Google rating badge (4.9 ★, 51 reviews) + `[trustindex no-registration=google]` shortcode, which shows nothing until the **Trustindex plugin is connected** to the Google profile.
- The "25% off first transaction" promo from the listing site was not used (unconfirmed).
- Forms (Elementor Pro) email **jimtowingltd@gmail.com** and save submissions (Elementor → Submissions). Confirm the recipient.
- The business has no public street address on Google (service-area business), so the map embed is centred on Calgary and links to the Maps profile.
