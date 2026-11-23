# EVTRON (evtron.co.uk): project context

UK home EV charger brand. Sells chargers **supplied and fitted** at fixed VAT-inclusive prices. Products: EV-TRONX tethered (own brand, EMS3-70-C), Fox ESS tethered (L Series), Fox ESS untethered (A Series?). Source of truth: client brief (summarised in `docs/brief-summary.md`).

## Where things are
- `docs/`: phase documents (see `docs/README.md`).
- `research/`: competitor crawl data, contact sheets, official sources (Fox datasheet, gov.uk pages). Raw screenshots and WP API dumps are git-ignored.
- `assets/brand-source/evtron-web-assets/`: the client's logo pack (README there has the logo usage rules).

## Site access
- Live site: WordPress on Hostinger (LiteSpeed + Hostinger CDN), Astra + Elementor Pro. WooCommerce to be added.
- Credentials come only from env vars `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. Never write them to files or chat. Note: the app password belongs to the **admin** account; `WP_USER` must be that account's login or email.
- Read-only until the user gives the go-ahead for a phase that changes the site. Work on drafts and don't overwrite published pages without the user's OK.

## Decisions (agreed)
- Platform: **WordPress + Elementor Pro + WooCommerce**, payments **Stripe + PayPal**.
- Use **native Elementor widgets wherever possible**. Custom CSS/JS goes only in **Elementor → Custom Code (global)**.
- **Dark theme only.** No light theme or toggle. Base `#0B0F14`, warm-white `#F2EFE9` text. WCAG 2.2 AA.
- Brand fonts: Manrope (300 to 600), IBM Plex Mono 400 (specs and labels), self-hosted.
- Coming Soon page exists (Elementor Maintenance Mode, template #45). OFF (user request, 18 Nov 2026); site public, noindex nofollow. Use tools/qa_window.py for approved short QA windows.
- Work in phases with checkpoints. The user approves each phase.

- Brand in text: **EV-Tron** (user decision 18 Nov 2026; supersedes "EVTRON everywhere"). Logo artwork stays as supplied (wordmark "evtron"). URL slugs unchanged. Accent: logo **charge-green #3BE37F**, used sparingly.
- Variants (from client photos): EVTRON tethered = black/red/grey/green; Fox tethered (L Series) = black/blue/purple/pink; Fox untethered (A Series) = white (per brief; the client photo shows black, so authentic white images are needed).
- Payments: full payment default (Stripe incl. Apple/Google Pay + PayPal). Instalments via Klarna/Clearpay (Stripe) and/or PayPal Pay in 3. Shop Pay Installments is Shopify-only, so not possible.

- Enquiry emails: sales@ and info@ evtron.co.uk. Site maintained by the developer (user), not the client.
- Product photos come later: use clearly marked placeholder images until then.
- Client is a new business, possibly not VAT-registered. Price wording ("incl. VAT") depends on that.

- Design: **Direction A "Spec Sheet"** chosen (docs/design-system.md, tokens in design/tokens.css). Control borders #6A7688 (not the prototype #3A4655).
- Plugins: Yoast SEO (free), All-in-One WP Migration for backups, no staging. Mailboxes sales@/info@ to be created.

- Client answers received 18 Nov 2026: see docs/client-answers.md (Crimson Red, install package, £15/m extra cable, England coverage, not VAT registered, Mon–Sat 8:30–6:30).
- **V2 glassmorphism is FINAL** (client decision 19 Nov 2026): page 141, front page. V1 (page 95) and V3 Simple (page 182) set to draft, kept for reference. build_v2.py appends V1's how/costs/faqs/matcher sections from page 95.

- **Selling (21 Nov 2026):** EV-Tron Tethered (own brand, configurator page) plus **Fox ESS Tethered £995 / Untethered £945** (partner brand, solar-compatible, installed prices) published on the general product template, in the main menu and footer. Homepage stays EV-Tron-only; solar FAQs point to Fox. Fox colours and a charger-only Fox price still to confirm.
- **Purchase paths:** charger only = online (configurator → WooCommerce basket → checkout, £595 / 10m £675, add-ons as hidden products); supply and install = callback form (atomic e-form → submissions + email to sales@), then remote survey and quote. CT clamp is a separate £15 add-on.
- **WooCommerce:** product base `/ev-chargers/` (set by the user in Permalinks). Products: EV-Tron 254 (12 variations), add-ons 250–253, Fox 267/272 (published 21 Nov). Templates: EV-Tron 273 (configurator, snippet 07), general product 300-ish (`tpl_product_generic` in tools/created.json). Shop pages skin: snippet 08.
- Menus trimmed to pages the site will have (no compare, accessories, tariffs, guides or get-a-quote pages).
- **Pages (tools/build_pages.py):** Installation (request form → sales@), FAQs, Contact (3-step form → info@), Warranty (renders docs/legal/warranty-terms.md), For dealerships (5-step form → sales@), For installers (login link to /my-account/ + 4-step application → sales@), legal pages rendering `docs/legal/<slug>.md` (drafts to UK law, written 22 Nov 2026; [PLACEHOLDER:…] highlighted on the page until filled). Grants page removed (client, 22 Nov). V2 styles (snippet 145) load site-wide: build scripts must keep its scope `include/general`.
- **Round 2 (22 Nov 2026):** EV-Tron now solar compatible (client); coverage "Nationwide" (client, 23 Nov); warranty wording "3 years included, upgrade to 5 for extra peace of mind for only £89.99"; app name not shown; PEN wording = included with every installation (253V claim unverified vs manual's 270V); 12-point protection labelled manufacturer spec; Type 2 cable range (5/10/15/20m, £113.99–£313.99); Fox L07P specs from the Fox datasheet. Dealer referral fee: £150 paid to the dealership per completed installation (user, 22 Nov). AlphaMax PDF = Vorsprung's product, not used. £995 = Fox ESS Tethered installed price only; EV-Tron shows £595 charger-only, installation quoted after survey (user, 23 Nov). No 'inc. VAT' anywhere until VAT status confirmed. QR landing page /book/ (not in menus): `?dealer=<slug>` fills a hidden Dealership field on the 4-step survey form (→ sales@) for £150 referral tracking; QR codes via tools/make_dealer_qr.py → marketing/qr/. Real product photos (client) replaced the renders (media keys render_evtron*; illustrations kept as illus_*). Client marketing drafts in assets/marketing/ (the client's 'dealership pop up banner' = the printed showroom pull-up). Our own banner designs (Design canvas TVovtFeBZfxo1ZH2RG9xEk, source in marketing/banner-design/) rendered with a real /book/ QR = media banner_pullup / banner_counter, used on For dealerships, the homepage dealer section and the pop-up. Homepage dealership pop-up (snippet 05): 6s after landing, once per visitor (localStorage evDealerPop), Esc/close/'Maybe later'. Delivery (tools/setup_shipping.py, zone 'United Kingdom', one flat rate): chargers free, cables £4.95 (shipping class 'cables', flat rate charged once per order). Cable = 32A Type 2 lead per client's reference link (evcables.com, Wottz): IP54, CE/UKCA, 2-year warranty; brand not named on site. Open questions are listed in the 22 Nov chat summary.

## Open
Batch 2 business details (brief-summary §9). EV-TRONX smart-charging compliance. Fox exact SKUs.

## Conventions
- UK English, GBP, prices incl. VAT.
- **Honesty rules:** no invented reviews, accreditations, stats or awards. Unverified product claims stay as internal notes. Placeholders are clearly marked `[PLACEHOLDER]`.
- Don't copy competitor design, copy or imagery.
- Don't publish EV-TRONX connectivity, DLB/CT, app, PEN, surge or 7.4kW claims until verified. Smart Charge Points Regulations compliance must be confirmed before sale.
