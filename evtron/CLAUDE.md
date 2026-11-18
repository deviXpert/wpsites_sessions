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
- A Coming Soon / Maintenance page for logged-out visitors comes first (Elementor Maintenance Mode).
- Work in phases with checkpoints. The user approves each phase.

## Open (see brief-summary §9)
Brand name EVTRON vs EV-TRONX · accent colour (brand green vs the prompt's "no green") · meaning of "4 variants" · checkout model (full / deposit / survey-first).

## Conventions
- UK English, GBP, prices incl. VAT.
- **Honesty rules:** no invented reviews, accreditations, stats or awards. Unverified product claims stay as internal notes. Placeholders are clearly marked `[PLACEHOLDER]`.
- Don't copy competitor design, copy or imagery.
- Don't publish EV-TRONX connectivity, DLB/CT, app, PEN, surge or 7.4kW claims until verified. Smart Charge Points Regulations compliance must be confirmed before sale.
