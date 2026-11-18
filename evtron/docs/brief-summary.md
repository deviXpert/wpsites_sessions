# EVTRON: brief summary (Phase 0)

Source: client brief `EV_TRONX_Complete_Website_Brief_Branded.docx` (dated 7 November 2026), the user's build prompt, the EVTRON logo pack (`assets/brand-source/`), product photos shared in chat, and the user's chat instructions. Research date: 18 November 2026.

**Status:** draft for Checkpoint 1. Items marked ❓ are open questions; items marked ⚠️ are risks or conflicts.

---

## 1. The business

| | |
|---|---|
| Brand / domain | **EVTRON**, evtron.co.uk ❓ the brief says **EV-TRONX** throughout (see section 9, Q1) |
| What it sells | Home EV chargers, **supplied and fitted** at a fixed price incl. VAT for a defined "standard installation". Extra work is quoted separately |
| Market | UK homeowners and renters with off-street parking who drive (or are about to drive) a BEV or PHEV with a Type 2 inlet |
| Brand line | Tagline "Driven by innovation." Suggested headline "Fast. Smart. Effortless." |
| Tone | Premium, modern, clear, honest. The brief stresses fairness: never show unavailable options and never sell an included item twice |
| Service area | ❓ Not stated (UK-wide? a region? which installers?) |

## 2. Products and proposed prices (all "proposed" in the brief, so all need confirming)

| Product | Variants | Proposed installed price (incl. VAT) | Notes |
|---|---|---|---|
| **EV-TRONX tethered** (model EMS3-70-C) | Mythos Black · Space Grey · Midnight Green. ❓ The client photo also shows a **dark red** unit | **£1,295** | 7kW, Type 2, tethered. Supplier quote is a 7.5m cable. **Not** solar-compatible |
| **Fox tethered**, solar-compatible | Black · Blue · Pink. ❓ The photo shows black, teal-blue, **purple** and pink | **£995** | Almost certainly the **Fox ESS L Series L07P** (official datasheet saved in `research/sources/`) |
| **Fox untethered**, solar-compatible | ❓ The brief says **white**, but the photo shows a **black** unit | **£945** | Probably the **Fox ESS A Series** (single-phase, 7.3kW). Exact SKU still needed |

**EV-TRONX cable options:** 5m (base, **not available**, so it must not be sellable), 7.5m (+£35 proposed, but the supplier quote already includes 7.5m ❓), 10m (+£90, availability unconfirmed).

**Accessories:** black charging post £200, steel charging post £280 (❓ is fitting included?), CT clamp £20 (only where it isn't already included; it is included with EV-TRONX per the supplier quote).

**Warranty:** 3 years standard proposed (⚠️ the manufacturer manual says 1 year, so EVTRON must define and underwrite the extra cover in writing). Extended warranty +£89.99 for 5 years in total.

### Verified Fox ESS L Series facts (official datasheet V1.3, June 2026)
L07P: 7.3kW single-phase, 32A, Type 2 tethered plug, 5m cable (6m optional), Bluetooth plus 2.4GHz Wi-Fi, plug & charge / app start, IP55 / IK08, −25 to 50°C, 196×197×105mm, 3.7kg. Protection: over/under-voltage, overcurrent, leakage, ground, **surge, tamper, PEN**, 6mA DC detection (RCD-DD to IEC 62955). Certified CE/CB/RCM/**UKCA**, EN/IEC 61851-1. Features: solar linkage, scheduled charging. **Note: IP55, not IP65.**
A Series (Fox site): IP55/IK08, OCPP 1.6/2.0.1, dynamic load balancing, solar linkage. Full datasheet not reachable; exact model still needed.

## 3. EV-TRONX feature and spec content (from the brief)
7kW single-phase AC, up to 32A (adjustable 4 to 32A), 90 to 270V input, Type 2, IP65 (tethered manual), −20 to +50°C, about 274×204mm, RFID start/stop, plug-and-charge / RFID / app modes, scheduling, LED states (blue standby, green charging/complete, red fault), protection (over/under-voltage, overcurrent, earth leakage, thermal derating), auto stop.
**Do not publish yet:** DLB/CT clamp operation, Wi-Fi/Bluetooth/4G (listed as *optional*), Ethernet, app name (the manual says "WeGoodCharger"; the spec mentions Tuya/proprietary), the 7.4kW claim, solar, PEN fault protection, surge protection.

## 4. Required pages and buying journey (from the brief)
Home · Choose your charger (compare the three) · Product pages (gallery, colours, cable, features, specs, price) · Accessories · Installation explained (included / excluded / survey) · EV tariffs and savings (no unverified integrations) · FAQs · Get a quote (contact details, postcode, car, charger, location, **photo upload**) · Legal (terms, privacy, cookies, warranty, cancellation).

## 5. Decisions already given by the user (in chat)
- **Platform:** WordPress + **Elementor Pro + WooCommerce**, with **Stripe and PayPal** payments. This answers most of Phase 4.
- Use **native Elementor widgets as much as possible**. Any custom CSS or JS goes in **Elementor → Custom Code (global)**.
- **"4 variants of the products"** ❓ needs clarifying (see Q3).
- A **Coming Soon / maintenance page** for logged-out visitors first (Elementor's built-in Maintenance Mode can do this).
- The brief is the source of truth. Learn from competitors without copying them.

## 5a. Checkpoint 1 answers (18 Nov 2026)
- **Brand:** **EVTRON everywhere.** The own-brand charger (EMS3-70-C) is sold as an EVTRON charger. "EV-TRONX" is not used on the site.
- **Accent:** follow the logo palette, i.e. **charge-green `#3BE37F`** as the single accent (option A), used sparingly.
- **Variants follow the client's product photos:**
  - **EVTRON tethered:** 4 colours: black, red (deep maroon), grey, green. Names to confirm: Mythos Black / Space Grey / Midnight Green from the brief, plus a name for the red.
  - **Fox tethered (L Series):** 4 colours: black, blue (teal), purple, pink.
  - **Fox untethered (A Series):** black (overrides the brief's "white").
- **Payments:** **full payment by default** (Stripe cards, Apple Pay and Google Pay, plus PayPal), **plus an instalment option.**
  - ⚠️ **Shop Pay Installments is Shopify-only** (Affirm via Shopify Payments) and can't run on WooCommerce.
  - Proposed WooCommerce equivalents: **Klarna** and/or **Clearpay** via the Stripe gateway, and **PayPal Pay in 3** via WooCommerce PayPal Payments. All need the merchant accounts approved, and the order limits must cover £945 to £1,295+.
  - Since 15 July 2026, third-party BNPL lenders are FCA-regulated. EVTRON should confirm with its provider or adviser what it must display and whether any permission applies to it as the retailer.

## 6. Current state of evtron.co.uk (audited 18 Nov 2026, read-only)
- Fresh WordPress install on **Hostinger** (LiteSpeed + Hostinger CDN). Theme **Astra 4.14.3**. Plugins: **Elementor 4.4.0**, **Elementor Pro 4.3.1**, SG Security (inactive, left over from an earlier host). An Elementor MCP composer endpoint is present.
- **No pages, posts, media or menus.** Front page shows latest posts. Site title "evtron.co.uk", no tagline, timezone empty, language en_US (should be en_GB).
- **WooCommerce is not installed yet.**
- REST access works with the admin account and app password. ⚠️ The environment's `WP_USER` is wrong: it should be the admin login, not the current email.
- **So there is nothing to migrate and no redirect map is needed** (unless an older site existed on another domain ❓).

## 7. Brand inputs received (logo pack)
- Logos: horizontal / stacked / icon / badge in dark, light, white and black versions, plus favicon, app icon, apple-touch icon, social avatar and webmanifest. **The dark-background version is supplied.**
- Palette: ink `#0B0F14` (base), **charge-green `#3BE37F`** (mark, primary buttons on dark), deep-green `#0B7A3B` (accent on light), warm-white `#F2EFE9`, slate `#8D96A3`, paper `#F5F6F1`.
- Fonts: **Manrope** 300/400/500/600 for headings and body. **IBM Plex Mono** 400 for specs, labels and tariffs.
- Rules: no glows, shadows, gradients, recolouring or retyping; no hyphen ("EVTRON", not "EV-TRON"). Minimum horizontal width 100px; clear space = the "o" height.

⚠️ **Conflict:** your prompt says to avoid green as the main accent and to start from amber `#FFB020` if there's no palette. The supplied palette's accent **is green** (`#3BE37F`), and the prompt also says to use the logo palette. Two competitors already pair dark backgrounds with bright green (EVolt uses `#0FFF00` on black; myenergi's buttons use `#40FF7A`, almost identical to ours). Options are in Q2.

## 8. Compliance and fact-check findings (affect content, so they matter now)
1. ⚠️ **Smart Charge Points Regulations 2021 (GB).** Home chargers sold in Great Britain must have smart functionality: network connectivity, demand-side response, default off-peak hours, randomised delay, and security requirements. The brief lists EV-TRONX Wi-Fi/Bluetooth/4G as **optional**. **The EV-TRONX variant must be confirmed as a compliant smart charge point with a statement of compliance before it's sold.** This is a launch blocker for EV-TRONX, not just a copy question. Source: [GOV.UK guidance](https://www.gov.uk/guidance/regulations-electric-vehicle-smart-charge-points), [OPSS guide PDF](https://assets.publishing.service.gov.uk/media/628ce214e90e071f653a494a/Guide-to-evscp-regulations-2021-V2.1.pdf).
2. **OZEV grants (verified on gov.uk, last updated 1 April 2026):** for **renters and flat owners** with private off-street parking, 75% of cost up to **£500**, available until **31 March 2027**. Owners of houses are **not eligible**. There is also an on-street (cross-pavement) household grant up to £500, plus landlord and workplace grants (up to £500 per socket). Grants require an **OZEV-approved installer** and a chargepoint on the **eligible model list**. ❓ Is EVTRON or its installer OZEV-approved, and are the products on the list? If not, the site shouldn't promote grants beyond a factual explainer.
3. **PEN fault protection** (BS 7671) must be handled by the charger or a separate device. Fox L Series lists PEN; for EV-TRONX it's unverified. The installation page must state how EVTRON's standard install handles it.
4. **Power ratings:** EV-TRONX is 7kW (don't say 7.4kW). Fox L07P is 7.3kW officially.
5. **Fox IP rating is IP55**, not IP65. Keep each product's specs separate.
6. **Consumer law:** selling fitted chargers online is a distance contract (14-day cancellation, with rules when installation starts within the period), and "standard installation" must be defined before payment. This affects checkout design (see Q4).

## 9. Clarifying questions (batch 1, the most important)
1. **Brand name:** is the site brand **EVTRON** and **EV-TRONX** the product name of EVTRON's own charger? Or should it be EVTRON everywhere?
2. **Accent colour** (brand green vs your "no green" rule). My recommendation is **A**:
   - **A (recommended):** keep charge-green `#3BE37F` as the single accent, used sparingly (CTAs and key highlights only). Stay distinctive through layout, typography (Manrope + Plex Mono "spec sheet" voice), warm-white and restraint, not colour. It's your logo, so it's honest to the brand.
   - **B:** use amber `#FFB020` for CTAs and keep green only in the logo. More distinct from EVolt and myenergi, but splits the brand.
   - **C:** use warm-white as the primary button colour and green only for state and highlight. Most premium-looking, slightly lower CTA salience.
3. **"4 variants":** what are the four? (a) 4 colours of EV-TRONX (black, grey, green **and red**, as in the photo)? (b) 4 colours of Fox tethered (black, blue, **purple**, pink)? (c) 4 products (EV-TRONX, Fox tethered, Fox untethered + one more)?
4. **Checkout model:** sell the fitted charger outright at the full price, take a **deposit** (balance after survey), or collect a **photo survey first, then pay**? I'd recommend full payment with a mandatory pre-payment "is my home standard?" check plus photo upload, and a clear refund if the survey finds it non-standard.

**Batch 2 (after you answer batch 1):** legal entity name, company number, VAT number and registered address · phone, email and opening hours · service area · who installs (in-house or partner), and NICEIC/NAPIT/OZEV status · standard installation definition (cable length, consumer unit, earthing, drilling) · lead times · Fox exact SKUs and the untethered colour · EV-TRONX app name and connectivity · warranty terms · Stripe and PayPal accounts (business) · Klarna or other finance? · any real customer reviews or Trustpilot account · high-res product photos (originals, not WhatsApp screenshots) and any installation photos.

## 10. Missing inputs checklist
| Input | Status |
|---|---|
| Logo (incl. dark/reversed) | ✅ received |
| Palette and fonts | ✅ received (accent conflict, Q2) |
| Product photos | ⚠️ only WhatsApp screenshots. Need originals, ideally on a transparent or dark background |
| Supplier PDFs (`Specs.pdf`, two manuals, earlier briefs) | ❌ not received |
| Fox exact SKUs, colours, warranty | ❌ (L Series datasheet found independently) |
| Legal entity / contact / address | ❌ |
| Installer accreditations (NICEIC/NAPIT/OZEV) | ❌. Nothing will be claimed until supplied |
| Reviews / testimonials | ❌. None will be shown until real ones exist |
| Standard installation definition and exclusions | ❌ |
| Warranty and cancellation terms | ❌ (drafts for legal review will be written) |
| Payment accounts (Stripe, PayPal) | ❌ |
| Lifestyle / installation photography | ❌. Placeholders will be clearly marked |
