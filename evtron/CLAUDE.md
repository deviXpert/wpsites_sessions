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

## Open
Batch 2 business details (brief-summary §9). EV-TRONX smart-charging compliance. Fox exact SKUs.

## Conventions
- UK English, GBP, prices incl. VAT.
- **Honesty rules:** no invented reviews, accreditations, stats or awards. Unverified product claims stay as internal notes. Placeholders are clearly marked `[PLACEHOLDER]`.
- Don't copy competitor design, copy or imagery.
- Don't publish EV-TRONX connectivity, DLB/CT, app, PEN, surge or 7.4kW claims until verified. Smart Charge Points Regulations compliance must be confirmed before sale.
