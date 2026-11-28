# CLAUDE.md: Build the Wassi Towing Ltd. website in WordPress + Elementor

You are building **wassitowing.ca**, a towing and roadside assistance site for **Wassi Towing Ltd.**, a new business (launching 2026) that covers **all of Calgary, Alberta**. The design, copy, brand assets and interaction code in this folder are final and approved. Your job is to rebuild them faithfully in WordPress with Elementor. Don't redesign anything and don't rewrite the copy.

## 1. What's in this folder

| Path | What it is | How to use it |
| --- | --- | --- |
| `design/html/*.html` | Static HTML of every page in its default state, plus `--state-*` files showing interactive states | **Source of truth for layout, spacing, colours and markup order.** Open in a browser, inspect styles, match them. |
| `design/screenshots/*--desktop.png` / `*--mobile.png` | Full-page renders at 1440px and 390px | Visual reference for QA. Your Elementor build should match these. |
| `content/website-content.md` | All page copy, SEO titles, meta descriptions, H1s, keyword map, FAQs, alt text | **Source of truth for words.** Copy text exactly, including 9 full service pages. `\[BRACKETS\]` = placeholder the client must fill. |
| `brand/logo/` | Logo in SVG + PNG (full colour, reversed, white, navy, stacked, symbol, app icon) | Header uses `horizontal_reversed.svg` (on navy). Footer the same. |
| `brand/favicon/` | Favicon PNGs (32/180/192/512) + SVG | Site Settings > Site Identity. |
| `brand/tokens.json`, `brand/tokens.css` | Colours, fonts, type scale, radii, spacing, motifs | Set up the Elementor Global Kit from these (section 3). |
| `interactions/` | Vanilla JS/HTML for the quote widget, Stranded mode, services filter, FAQ search, mobile sticky bar | Use as-is (section 6). |
| `seo/` | Page meta + keyword CSV, JSON-LD schema files | Section 8. |

## 2. Stack

- WordPress (latest), **Hello Elementor** theme plus a **child theme** for custom CSS/JS.
- **Elementor Pro** (needed for Theme Builder header/footer, the service page template and custom CSS).
- Use **Flexbox Containers** only (no legacy sections/columns).
- SEO plugin: **Rank Math** (or Yoast). Use one only.
- Fonts: Montserrat (600, 700, 800, 900 + italic 800/900) and Inter (400, 500, 600, 700). Self-host them via Elementor > Custom Fonts or the Google Fonts local option. Don't load from Google's CDN (privacy and speed).
- Don't add any other page builders or heavy plugins. Add a caching plugin and image optimisation at the end.

## 3. Global Kit setup (do first)

From `brand/tokens.json`:

- **Global colours:** Navy `#101D32`, Ink `#0B1424`, Navy-2 `#1A2B47`, Orange `#FF6B00`, Orange-Text `#B84D00`, Orange-Tint `#FFF1E6`, BG `#F5F6F8`, Line `#E2E6EC`, Muted `#5A6577`, On-Dark `#C5CEDB`.
- **Hard rule:** orange `#FF6B00` buttons always use **navy** text. White on this orange fails contrast. Orange *text* on white/light backgrounds must be `#B84D00`.
- **Global fonts:** Primary/Display = Montserrat 900 italic; Secondary = Montserrat 800; Body = Inter 400; Accent = Inter 600.
- **Type scale:** display `clamp(42px, 5.6vw, 74px)` lh 0.98; H2 `clamp(30px, 3.4vw, 45px)` lh 1.08, Montserrat 900 italic; H3 20–22px Montserrat 800; eyebrow 13–14px Montserrat 800, 0.14em tracking, uppercase; body 16–18px Inter.
- **Buttons:** radius 14px, min-height 48px (60px "large"), Montserrat 800, icon left.
- **Layout:** content width 1200px, side padding 24px, section vertical padding 88px (56px on mobile).
- Paste `brand/tokens.css` into Site Settings > Custom CSS.

## 4. Theme Builder templates

1. **Header** (all pages): orange emergency strip (alert icon, "Stuck right now? A real person answers: [PHONE]", plus an "I'm stuck right now" pill button with `data-wt-stranded="open"`), then a navy bar with the logo, nav (Home, Services, About, FAQs; active item white with an orange underline), "Get my quote" outline button (links to `/#quote`) and "Call [PHONE]" orange button (`tel:` link). Make the header sticky on scroll. On mobile, use a hamburger menu.
2. **Footer** (all pages): Ink background, logo plus a one-line description plus a Call button, then three columns (Services: all 9 links; Company; Contact), and a bottom row with © 2026, Privacy, Terms and "If anyone is hurt or in danger, call 911 first." Also put `interactions/mobile-sticky-bar.html` here.
3. **Call band** ("Stuck right now?"): save as a **global Elementor template** with hazard-stripe edges (`.wt-hazard` 14px strip top and bottom), an italic H2, a big tap-to-call `[PHONE]` and a "text us your location" button. Insert it near the bottom of Home, Services, the service pages and About. Don't add it to FAQs, which has its own dark call box.
4. **Single service template:** build ONE template from `design/html/service-template-flatbed-towing.html` and apply it to all 9 service pages (see section 5). The design only shows Flatbed Towing; every service uses the same section layout with its own copy.

## 5. Pages, slugs and section map

Copy text exactly from `content/website-content.md`. Each page has **exactly one H1**: the small keyword line (pill or eyebrow style) above the big italic headline. **The big headline is a styled `<p>`, NOT a heading.** Keep this; it's deliberate for SEO.

### Home `/`  (reference: `home.html`, `home--state-*.html`)
1. **Hero** (navy, faint road graphic bottom-right): H1 pill "Towing & Roadside Assistance in Calgary"; display text; subhead; buttons "Call now" (tel) and "I'm stuck right now" (`data-wt-stranded="open"`); trust line with 3 icons. Right column: **quote widget** (`interactions/quote-widget.html` in an HTML widget, anchor `#quote`).
2. **Dispatch board** (BG section, Ink rounded panel): "What happened?" eyebrow + H2 + "Dispatch board" pill; header row (YOUR PROBLEM / WE SEND / TYPICAL ARRIVAL); 9 linked rows (icon + problem, orange service name, "[X] min", orange arrow circle), each linking to its service page. Use a Container per row; rows wrap on mobile.
3. **Intro / SEO copy** (white): huge faded "CALGARY" word behind (absolute, `#F1F3F6`); left: eyebrow, quote line "Every quadrant. One call." with an orange left border, NW/NE/SW/SE badges; right: H2 "A new kind of tow truck company in Calgary" + 3 paragraphs with internal links to each service.
4. **How it works** (navy): 4 white "road sign" cards (orange top border, big italic 01–04, icon, H3, text), each on a grey "pole", sitting on a full-width asphalt strip (`#1B2433`) with a dashed white centre line (`--wt-road-dash`) and an orange truck badge on the left.
5. **Why Wassi bento** (white): wrapping tiles. Large orange tile (price promise + "Get my quote" dark button); navy tile with the live-tracking mini mockup; light tile (Damage-free gear); wide navy-outlined tile (Real people answer + big italic [PHONE]).
6. **Service area** (BG): left text + quadrant chips; right: inline SVG Calgary quadrant map (copy the `<svg>` from home.html into an HTML widget).
7. **Launch pledge** (peach `#FFF3E8` with dotted pattern): white card rotated -1deg, rotated "NEW IN CALGARY 2026" stamp, H2, 4 checklist rows, signature line "[Founder name]" with the symbol logo.
8. **Call band** (global template), then the footer.
- **Stranded mode overlay:** a Container with CSS ID `wt-stranded` and class `wt-stranded` (see `home--state-stranded-mode.html`): dark full-screen layout, 3 huge buttons (Call: tel; Text my exact location: `data-wt-sms-location`; "I'm safe, give me a quote" with `data-wt-stranded="close"` linking to `#quote`), a checklist of 4 `.wt-check` buttons (each with a `.wt-box` square), a 911 notice and an Exit button (`data-wt-stranded="close"`). Hidden until opened; `stranded-mode.js` handles everything.

### Services `/services/`  (reference: `services.html`, `services--state-filter-emergencies.html`)
1. **Hero** (light BG): H1 eyebrow "TOWING & ROADSIDE SERVICES IN CALGARY", display text, intro; right: "9 SERVICES, ONE CALL" with a 3×3 grid of icon tiles.
2. **Filter tabs + grid**: tabs (All services, Emergencies, Towing, Quick fixes, Planned moves) with `data-wt-filter`. **Featured full-width navy card** for Flatbed Towing ("MOST REQUESTED", big truck watermark). Then 8 cards (navy icon tile, Emergency/Book ahead tag, name, one-liner, "Typical arrival [X] min", "Get a price" arrow). Each card links to its service page and carries `data-wt-cats` (below).
3. Dashed "Not sure which one you need?" strip, then the call band.

`data-wt-cats` values:

| Service | data-wt-cats |
| --- | --- |
| Flatbed & Wheel-Lift Towing | `towing emergency` |
| Roadside Rescue | `quick emergency` |
| Tire Rescue | `quick emergency` |
| Fuel Drop | `quick emergency` |
| Battery Boost | `quick emergency` |
| Ditch & Snow Recovery | `towing emergency` |
| Trailer & Equipment Hauling | `planned` |
| Motorcycle Transport | `towing planned` |
| Prestige & Low-Clearance Towing | `towing planned` |

### 9 service pages `/services/<slug>/`  (template reference: `service-template-flatbed-towing.html`)
Slugs: `flatbed-towing`, `roadside-assistance`, `flat-tire-change`, `fuel-delivery`, `battery-boost`, `winch-out`, `local-hauling`, `motorcycle-towing`, `exotic-car-towing`. Create them as pages under a parent page "Services".

Template sections, in order:
1. **Hero** (peach-to-white gradient): breadcrumb; H1 navy pill with the service icon (H1 = the page's search phrase, e.g. "Flatbed Towing in Calgary"); display headline; intro paragraph(s); "Call now" + "Text my location" buttons; right: navy-outlined quick quote card (pickup, drop-off, vehicle select, "See my price"). Wire this to the same logic as the Home widget, or have it link to `/#quote`.
2. **What's included + Call us when** (white): left checklist with orange check squares; right: navy panel with dark "call us when" rows.
3. **Middle feature section** (BG): on the towing page, "Flatbed vs Wheel-lift" two cards with an orange **VS** circle between them. On other services, use this slot for that page's unique H2 section from the content doc (e.g. "How a car lockout works", "Why batteries die in Calgary winters", "Common Calgary winch-out situations"), in the same visual style: two cards, or one card plus a highlight panel.
4. **Price factors + FAQs + related**: add an H2 "What affects the price" list and an H2 "<Service> FAQs" accordion (3 Q&As from the doc) above "Related services". Render related services as navy pills with orange icon circles.
5. Call band.

Every service page **must include all H2 sections and copy from the content doc** (about 600–900 words each). This is the SEO body; don't trim it to fit the design. Add sections in the template's visual language where the design shows fewer blocks.

### About `/about/`  (reference: `about.html`)
Navy hero with a large faded symbol watermark (H1 eyebrow + display text) → story (text + photo placeholder) → "Four promises" as big outlined numbers 01–04 in two columns with navy top rules (no cards) → navy "Why new works in your favour" icon rows → fleet **spec sheet** (rows with dotted leaders) + photo + drivers card → call band.

### FAQs `/faqs/`  (reference: `faqs.html`, `faqs--state-search-insurance.html`)
Navy hero: H1 eyebrow "CALGARY TOWING FAQS", display text, search input `#wt-faq-search`, category chips (`data-wt-faq-cat`). Body: one Container per group (`data-wt-faq-group="<name>"`) with an Elementor **Accordion** (first item open). Empty state `#wt-faq-empty`. Finish with the dark "Didn't find your answer?" call box. Use `interactions/faq-search.js`.

## 6. Interactions (folder `interactions/`)

| File | Where | Notes |
| --- | --- | --- |
| `quote-widget.html` | Elementor HTML widget, Home hero right column (anchor `#quote`) | Edit `WT_QUOTE_CONFIG` (phone, SMS, price ranges, ETA). Uses geolocation for "Use my location". |
| `stranded-mode.js` | Enqueue site-wide in the footer (child theme) | Needs the `#wt-stranded` container. Escape closes; focus is managed. |
| `services-filter.js` | Services page only | Needs `data-wt-filter` / `data-wt-cats`. |
| `faq-search.js` | FAQs page only | Works with nested Accordion `.e-n-accordion-item`. |
| `mobile-sticky-bar.html` | Footer template | Shows under 768px; adds body bottom padding. |

All scripts push GA4-ready `dataLayer` events: `wt_quote_step`, `wt_quote_complete`, `wt_call_click`, `wt_sms_click`, `wt_stranded_open`. Set them up as conversions in GA4/GTM.

Enqueue example (child theme `functions.php`):
```php
add_action('wp_enqueue_scripts', function () {
  $d = get_stylesheet_directory_uri() . '/wt/';
  wp_enqueue_script('wt-stranded', $d . 'stranded-mode.js', [], '1.0', true);
  if (is_page('services')) wp_enqueue_script('wt-filter', $d . 'services-filter.js', [], '1.0', true);
  if (is_page('faqs'))     wp_enqueue_script('wt-faq', $d . 'faq-search.js', [], '1.0', true);
});
```

## 7. Icons

The design uses simple 24px stroke icons (2px stroke, round caps). Copy the exact inline `<svg>` from the HTML files into Elementor Icon widgets as custom SVG, or substitute the closest Font Awesome / Elementor icons: truck, battery, tire/circle, gas pump, key, hook/anchor, trailer, motorcycle, car, phone, map pin, message, check, shield, clock, tag, map, arrow-right, alert-triangle.

## 8. SEO (from `seo/` and the "SEO plan" section of the content doc)

- Set the **title tag, meta description, slug and H1** for every page exactly as in `seo/page-meta-and-keywords.csv`. Titles are 60 characters or fewer; meta descriptions 160 or fewer.
- Exactly **one H1 per page** (the keyword line). H2s as given in the doc. Never skip heading levels for styling.
- **Schema:** add `seo/schema-localbusiness-sitewide.json` site-wide (in Rank Math: Local SEO, or a custom JSON-LD block). Add a Service schema on each service page using `schema-service-template.json` as the pattern, plus breadcrumbs. Replace placeholders. Validate with Google's Rich Results Test.
- **Images:** WebP, lazy-loaded below the fold, alt text from the doc. Real truck and founder photos go into the labelled placeholders when the client supplies them.
- Phone numbers as text plus `tel:` links (never only inside images). Name, phone and service area must match the Google Business Profile exactly.
- XML sitemap on; submit to Search Console. No city-swap doorway pages.

## 9. Placeholders

Anything in `[BRACKETS]` is unconfirmed. **Don't invent values.** Keep the bracketed text visible on staging and collect it in a list for the client. The full list is in the "Facts to confirm before launch" section of the content doc (phone, SMS, email, 24/7 hours, price ranges, arrival times, insurance, founder name, fleet, etc.). The business is new: **never add fake reviews, ratings, years in business or job counts.**

## 10. Acceptance checklist

- [ ] Every page matches its desktop and mobile screenshots (spacing, colours, type, section order).
- [ ] All 9 service pages exist with full copy and correct slugs/titles/meta/H1.
- [ ] One H1 per page; display headlines are not headings.
- [ ] Quote widget completes all 3 steps; Call and Text links are correct.
- [ ] Stranded mode opens from the header strip and the hero, traps focus, closes with Exit and Escape, and the checklist toggles.
- [ ] Services filter and FAQ search/chips work; the FAQ empty state shows.
- [ ] Mobile sticky bar shows only under 768px and doesn't cover the footer.
- [ ] Tap targets 44px or larger; text contrast 4.5:1 or better (Orange-Text on light, navy on orange buttons).
- [ ] Lighthouse mobile: Performance 85+, Accessibility 95+, SEO 100.
- [ ] Schema validates; sitemap submitted; GA4 conversions receive `wt_*` events.
