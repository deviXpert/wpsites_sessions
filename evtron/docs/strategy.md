# EVTRON: strategy, information architecture and SEO plan (Phase 2)

Draft for Checkpoint 2, dated 18 November 2026. Built on `brief-summary.md` and `competitor-teardown.md`.
Placeholders are marked **[PLACEHOLDER]**. Facts awaiting the client are marked ❓.

---

## 1. Positioning

**One line:** *The home EV charger, fully installed, at one honest price.*

EVTRON sells three hand-picked home chargers, each **supplied and fitted** for a fixed published price. The difference is **clarity**:
- you see the full installed price straight away (no postcode gate, no "from" pricing)
- you know exactly what "standard installation" includes, and what would cost extra, *before* you pay
- you get plain-English help choosing between tethered and untethered, and between solar and non-solar
- nothing is claimed that hasn't been verified (no fake reviews, stats or accreditations)

**Brand voice:** calm, precise, quietly confident. Short sentences. Numbers shown in IBM Plex Mono as a "spec sheet" voice. Positioning lines:
- Hero: **"Fast. Smart. Effortless."** (from the brief)
- Tagline: **"Driven by innovation."** (from the brief; footer/sign-off only, as it's generic)
- Supporting idea: **"One price. Fitted. No surprises."**

**Who it's for**
1. **New EV owners in a house with a driveway** (primary). They want it sorted quickly at a fair, clear price.
2. **Solar-panel owners** wanting to charge from surplus solar (→ Fox range).
3. **Design-conscious buyers** who care how it looks on the house (→ EVTRON colours).
4. **Renters and flat owners** who may qualify for the OZEV grant (→ grant explainer, quote route). ❓ depends on OZEV-approved installer status.

## 2. Conversion goals

| Priority | Goal | Where | Measured by |
|---|---|---|---|
| **Primary** | **Order a fitted charger online** (full payment; instalments via Klarna / PayPal Pay in 3) | Product page → basket → checkout | WooCommerce orders, revenue |
| Secondary | **Request a quote** (unsure if standard, non-standard home, business, multiple chargers, grant applicants) | Get a quote form (with photo upload) | Form submissions |
| Tertiary | Email or call | Contact page, footer (sales@ / info@) | Clicks on mailto/tel links |
| Micro | Use the charger finder; complete the "Is my home standard?" check | Home, Choose your charger, product pages | Analytics events (consent-aware) |

**The journey design rule:** every product page answers "what does it cost, what's included, will it work at my home?" above or right after the add-to-basket button.

## 3. Sitemap and information architecture

### 3.1 Pages

```
/                                   Home
/ev-chargers/                       Choose your charger (compare + 3-question finder)
  /ev-chargers/evtron-tethered-ev-charger/      Product: EVTRON tethered (4 colours, cable options)
  /ev-chargers/fox-tethered-solar-ev-charger/   Product: Fox L Series tethered (4 colours)
  /ev-chargers/fox-untethered-solar-ev-charger/ Product: Fox A Series untethered (white)
/accessories/                       Accessories (posts; optional CT clamp where genuinely optional)
  /accessories/black-charging-post/
  /accessories/steel-charging-post/
/installation/                      How installation works (included / extras / survey / timeline / "Is my home standard?")
/solar-ev-charging/                 Charging from solar (Fox range, requirements)
/ev-tariffs/                        EV tariffs and running costs (off-peak scheduling explainer)
/ev-charger-grants/                 Grants explained (OZEV, sourced from gov.uk)
/faqs/                              FAQs (grouped)
/get-a-quote/                       Quote request (with photo upload)
/about/                             About EVTRON
/contact/                           Contact
/guides/                            Guides hub (blog)
  /guides/<post-slug>/              Articles
/areas/                             ❓ only if the client serves defined areas (see 5.4)
Legal:
/terms/                             Terms of sale and installation
/privacy-policy/
/cookie-policy/
/warranty/                          Warranty (standard + extended)
/cancellations-returns/             Cancellation and refunds
WooCommerce (noindex):
/basket/  /checkout/  /order-received/ (endpoint)  /my-account/ (only if accounts are enabled)
Coming soon:
Elementor Maintenance Mode → "Coming soon" template for logged-out visitors until launch
```

**URL decisions**
- WooCommerce **product permalink base `/%product_cat%/`**, so products sit under their category (`/ev-chargers/...`, `/accessories/...`). `/ev-chargers/` and `/accessories/` are Elementor *pages* (designed comparison and listing), not default category archives. Product category archives get a different base (e.g. `/range/`), are set to noindex, and are kept out of navigation. ⚠️ This permalink shape can clash with other two-segment URLs (e.g. `/guides/post/`). I'll test it on the site before launch. **Fallback:** a fixed product base `/chargers/` for all products.
- WooCommerce "Cart" renamed **"Basket"** (UK convention), with the URL `/basket/`.
- Lowercase, hyphenated, no dates in guide URLs, no trailing parameters indexed.
- Product slugs include the keyword ("solar", "tethered") rather than SKUs.

### 3.2 Navigation

**Header (desktop):** Logo · **Chargers** (dropdown: the 3 products with price and swatch, "Compare all", "Accessories") · **Installation** · **Running costs** (dropdown: EV tariffs, Solar charging, Grants) · **Guides** · **FAQs** · **Contact** · [Basket icon with count] · **[Choose your charger]** (primary button)

**Header (mobile):** Logo · Basket · Menu button. The menu is a full-height dark panel with the same groups. "Choose your charger" is pinned at the bottom of the panel.

**Footer:** Chargers (3 products, Compare, Accessories) · Help (Installation, FAQs, Get a quote, Contact, Warranty, Cancellations) · Learn (Guides, Tariffs, Solar, Grants) · Company (About) · Legal (Terms, Privacy, Cookies) · Contact (sales@ / info@ evtron.co.uk, **[PLACEHOLDER] phone/hours**) · Legal line: **[PLACEHOLDER] company name, number, registered address, VAT status**.

**Trust bar** (slim, under the header on commerce pages): *Price includes standard installation* · *Clear what's included* · *Pay in full or in instalments* · *[PLACEHOLDER: lead time, e.g. "Installed in X weeks"]*. Only true statements; no stars until real reviews exist.

### 3.3 Templates (Elementor Theme Builder)

| Template | Used by |
|---|---|
| Header / Footer | All pages |
| Single Product | 3 chargers (+ simpler accessory variant) |
| Page (content) | Installation, Tariffs, Solar, Grants, About, Legal |
| Guides archive + Single post | Guides |
| Basket / Checkout / Thank you (Woo widgets) | Commerce flow |
| 404 | Not found |
| Coming soon | Maintenance mode |

### 3.4 Purchase flow
1. **Product page:** choose colour (swatches) → cable (EVTRON only; unavailable lengths shown disabled with a reason) → see the installed price update.
2. **"Is my home standard?"** (inline, about 5 yes/no questions) shown before or next to Add to basket. All yes: "Great, standard installation applies." Any no: "We may need to quote extra work. Add to basket and we'll confirm before installing, or get a quote first."
3. **Basket:** optional extras as cross-sells (extended warranty £89.99, charging post). Clear "what happens next" panel.
4. **Checkout:** guest checkout. Install address, parking type, vehicle (optional), **photo upload (optional, encouraged)**, preferred dates. Pay with card / Apple Pay / Google Pay / PayPal / Klarna / Pay in 3.
5. **Thank you page:** timeline (survey → booking → install), email confirmation from sales@.

❓ This depends on Q8, Q9, Q10 and Q25 (standard install definition, extras, survey and refund policy). The checker's questions will be built from the client's answers.

## 4. Keyword research (UK)

**Method:** Google UK autocomplete (en-GB, gl=uk) on 41 seed terms (`research/keywords/autocomplete-uk.json`), competitor title and heading targeting from Phase 1, and search-intent review. **I have no access to search volumes or difficulty scores.** In a normal project I'd verify volumes and difficulty in Ahrefs, Semrush or Google Keyword Planner before finalising. The tiers below are judgement, not data.

**Strategy for a brand-new domain:** head terms ("home ev charger", "ev charger installation") are dominated by established brands and energy suppliers, and a new site won't rank for them for months. So: win **specific, high-intent long-tail** queries first (product and brand terms, cable length, solar, tethered vs untethered, Klarna and finance), build topical depth with guides, and grow toward head terms.

### 4.1 Keyword clusters

| Cluster | Example queries (UK autocomplete) | Intent | Priority |
|---|---|---|---|
| Installed price | ev charger installed price · ev charger fitted price · home ev charger installation cost · ev charger cost uk · 7kw ev charger installation cost | Commercial | **High** |
| Tethered | tethered ev charger · tethered ev charger uk · tethered ev charger with 10m cable · tethered ev charger with long cable · tethered ev charger cable length | Commercial | **High** |
| Untethered | untethered ev charger · untethered ev charger uk · untethered ev charger 7kw · untethered ev charger installation | Commercial | High |
| Tethered vs untethered | tethered vs untethered ev charger (uk / pros and cons) | Informational → commercial | **High** (guide) |
| Fox ESS | fox ess ev charger · fox ev charger price · fox ev charger review · fox ess ev charger a series vs l series · fox ev charger untethered · fox ev charger app · fox ess ev charger installation | Commercial / brand | **High**: low competition, exact match to our stock |
| Solar | ev charger with solar · ev charger with solar panel · solar ev charger for home · ev charger with solar and battery · electric car charger with solar panels | Commercial | High |
| Smart / features | smart ev charger uk · smart ev charger 7kw · load balancing ev charger · ct clamp ev charger · pen fault protection ev charger | Commercial / info | Medium |
| Running costs | how much to charge electric car at home (uk / per month / overnight / calculator) · off peak ev charging hours · cheapest ev tariff uk · ev charging tariff comparison uk | Informational | Medium (guides, tariffs page) |
| Grants | ev charger grant uk · ozev grant eligibility · ev charger grants for home owners · ev chargepoint grant for renters · ev charger grant for flats | Informational | Medium (high volume, but OZEV install status ❓) |
| Finance | ev charger klarna · home ev charger klarna · ev charger pay monthly · ev charger finance | Commercial | Medium: few competitors target it |
| Installation how-to | can i install an ev charger myself uk · how long does ev charger installation take · ev charger installation requirements | Informational | Medium |
| Accessories | ev charger post · ev charger post mount · ev charging post for home | Commercial | Low–medium |
| Speed | 7kw ev charger how long to charge | Informational | Low–medium |
| Local | ev charger installers near me · ev charger fitted near me | Local commercial | ❓ depends on service area |

### 4.2 Keyword → page mapping

| Page | Primary keyword | Secondary keywords |
|---|---|---|
| Home `/` | home ev charger installed | ev charger fitted price, home ev charger installation, smart ev charger uk |
| Choose your charger `/ev-chargers/` | home ev chargers uk | best home ev charger uk, tethered or untethered, compare ev chargers |
| EVTRON tethered | tethered ev charger | tethered ev charger uk, tethered ev charger long cable / 10m cable, 7kw tethered ev charger installed |
| Fox tethered (solar) | fox ev charger | fox ess ev charger (L series), fox ev charger price, solar tethered ev charger |
| Fox untethered (solar) | untethered ev charger | fox ev charger untethered, fox ess a series, untethered ev charger 7kw |
| Accessories | ev charger post | ev charging post for home, ev charger post mount |
| Installation | ev charger installation cost | what's included in ev charger installation, how long does installation take, ev charger installation requirements |
| Solar EV charging | ev charger with solar panels | solar ev charger for home, charge electric car with solar |
| EV tariffs | off peak ev charging | ev charging tariffs uk, cheapest time to charge ev uk |
| Grants | ev charger grant uk | ozev grant eligibility, ev chargepoint grant renters / flats, ev charger grant homeowners |
| FAQs | ev charger faqs | (long-tail questions) |
| Get a quote | ev charger installation quote | — |
| Guide: Tethered vs untethered | tethered vs untethered ev charger | pros and cons uk |
| Guide: Cost to charge at home | how much to charge electric car at home uk | per month, overnight |
| Guide: Charging time on 7kW | 7kw ev charger how long to charge | — |
| Guide: Cable length | ev charger cable length | 5m vs 7.5m vs 10m |
| Guide: Can I install it myself? | can i install an ev charger myself uk | regulations, Part P |
| Guide: Fox L Series vs A Series | fox ess a series vs l series | — |
| Guide: PEN fault protection | pen fault protection ev charger | explained |
| Guide: Smart charger rules | off peak ev charging hours | smart charge point regulations explained |
| Guide: Paying in instalments | ev charger klarna | pay monthly ev charger |

One primary keyword per page, no two pages targeting the same primary keyword.

## 5. Content plan

### 5.1 Rules
- UK English, plain words, sentences under ~20 words, numbers in Plex Mono.
- **Every factual claim is either sourced (gov.uk, Fox datasheet, the brief marked as confirmed) or marked [PLACEHOLDER].**
- No savings figures unless calculated transparently from stated assumptions the visitor can change.
- Grant info dated and linked to gov.uk. The grant scheme ends 31 March 2027, so that page needs a review date.

### 5.2 Page outlines with draft copy

#### Home
1. **Hero:** H1 "Fast. Smart. Effortless. Home EV charging, fully installed." Sub: "Three carefully chosen chargers, each supplied and fitted for one clear price." CTAs: **Choose your charger** / How installation works. Visual: product cut-out on dark, the 4 colourways as small swatches. **[PLACEHOLDER images]**
2. **The three chargers:** cards with name, one-line positioning, installed price (Plex Mono), colour dots, "Tethered / Untethered", "Solar-ready" tag on Fox, and a View button.
   - EVTRON Tethered: "Our own design. Four finishes, a long cable, app scheduling. **[PLACEHOLDER: app/connectivity pending verification]**" £1,295 ❓
   - Fox Tethered: "Charge from your solar panels' surplus. Four colours." £995 ❓
   - Fox Untethered: "A clean socket, bring your own cable. Solar-compatible." £945 ❓
3. **Not sure? 3 questions** (charger finder, inline).
4. **What "fully installed" means:** included list + "what would cost extra" link. **[PLACEHOLDER until client defines it]**
5. **How it works:** 1 Order online → 2 Quick check (photos or survey ❓) → 3 Installation day → 4 Charge on off-peak.
6. **Pay your way:** full payment, or spread the cost (Klarna / PayPal Pay in 3, subject to status; once accounts are approved).
7. **Charging costs explained** (teaser): link to EV tariffs.
8. **FAQs (top 5)**
9. **Final CTA**

#### Choose your charger
H1 "Choose your home EV charger". Comparison table (sticky header on desktop, swipeable cards on mobile): price, tethered/untethered, cable, power, solar, app, IP rating, colours, warranty. Finder. "Tethered or untethered?" explainer. FAQs.

#### Product page (template)
1. Gallery (colour-linked) · H1 product name · one-line summary · price "Fully installed" · swatches · cable options (EVTRON) · **Is my home standard?** · Add to basket · instalment message · trust bar.
2. Key features (icons drawn for dark).
3. "What's included in the price" / "What might cost extra".
4. Smart charging and app (only verified content).
5. Solar (Fox only; requirements stated).
6. Safety and protection.
7. Specifications table (Plex Mono): **only verified rows**; unverified rows hidden, not shown as "TBC".
8. Installation timeline.
9. Product FAQs.
10. Compare with the other chargers.

**Fox Tethered spec rows (verified, Fox datasheet V1.3):** 7.3kW single-phase · 32A · Type 2 tethered · 5m cable (6m optional) · Wi-Fi 2.4GHz + Bluetooth · Plug & Charge / app · IP55 · IK08 · −25 to 50°C · 196×197×105mm · 3.7kg · protections incl. PEN, surge, 6mA DC detection · UKCA. *(The exact model is still to be confirmed by the client.)*

#### Installation
H1 "EV charger installation: what's included". Sections: included list ❓ · extras with prices ❓ · "Is my home standard?" checker · survey ❓ · timeline ❓ · safety and certification (BS 7671, PEN protection approach ❓, notifying the network operator ❓) · who installs ❓ · FAQs.

#### EV tariffs and running costs
H1 "Charging at home on an off-peak tariff". How scheduling works · default off-peak hours under UK smart charger rules (peak hours weekdays 8 to 11am and 4 to 10pm) · how to compare tariffs · providers mentioned only as examples, with **no claims of integration or eligibility** · a cost-to-charge calculator where the user enters battery size and their own pence per kWh (no invented rates).

#### Grants
H1 "EV charger grants in the UK (2026/27)". Verified from gov.uk (updated 1 April 2026): renters and flat owners with private off-street parking get 75% up to £500; an on-street cross-pavement grant up to £500; landlord and workplace grants £500 per socket; schemes run until 31 March 2027; owners of houses aren't eligible. Plus a 3-question "Am I likely to be eligible?" check. **Whether EVTRON can claim grants for customers depends on OZEV-approved installer status ❓.** Until confirmed, the page is informational only.

#### FAQs (grouped)
Charging (Type 2 compatibility, speed on 7kW, tethered vs untethered) · Installation (time, what's included, survey, permissions) · Smart and app · Solar · Payments (instalments, when you're charged) · Warranty and returns.

#### Get a quote
Fields: name, email, phone, postcode, property type, parking type, vehicle, charger of interest, preferred location for charger, photo upload (meter / consumer unit / parking spot, max 3 × 10MB), notes, consent. Spam protection: Elementor Forms honeypot + reCAPTCHA v3 *or* Cloudflare Turnstile (decided in Phase 4). Delivery to sales@.

#### About
Honest, brief: who EVTRON is, why three chargers, how pricing works. **[PLACEHOLDER: client story, Q28]**

#### Legal (drafts for the client's legal review)
Terms of sale and installation (incl. standard-installation definition and non-standard outcomes) · Privacy policy (UK GDPR; controller = **[PLACEHOLDER legal entity]**) · Cookie policy · Warranty (standard + extended) · Cancellations and refunds (Consumer Contracts Regulations 2013; services started within the 14-day period on request).

### 5.3 Launch guides (6, then 2 a month)
1. Tethered vs untethered EV chargers: which is right for you?
2. How much does it cost to charge an EV at home in the UK?
3. How long does a 7kW charger take to charge an EV?
4. EV charger cable length: 5m, 7.5m or 10m?
5. Can I install an EV charger myself in the UK?
6. Fox ESS L Series vs A Series: what's the difference?

### 5.4 Local intent
The client's service area is unconfirmed (Q5). **If** they cover defined regions, add `/areas/` plus one page per region, each with genuinely local content (installation lead times, typical home types, local network operator) and **no thin doorway pages**. If UK-wide, skip area pages and use `areaServed: GB` in schema.

## 6. Technical SEO plan

| Area | Plan |
|---|---|
| **SEO plugin** | One plugin for titles, meta, sitemaps and schema (Rank Math or Yoast; choice in Phase 4). Elementor doesn't handle meta. |
| **Titles** | Pattern `Primary keyword: benefit \| EVTRON`, ≤60 characters. E.g. "Tethered EV Charger, Fully Installed from £1,295 \| EVTRON" ❓ price |
| **Meta descriptions** | Unique, ≤155 characters, include price and what's included |
| **Headings** | One H1 per page. Elementor headings set to the correct H-level explicitly (Elementor defaults to H2) |
| **Canonical** | Self-referencing. Variation URLs (`?attribute_pa_colour=`) canonicalise to the product URL |
| **Robots** | noindex: basket, checkout, my-account, order endpoints, product category/tag archives, search results, coming-soon. Disallow in robots.txt: `/*?add-to-cart=`, `/*?orderby=`, `/wp-admin/` (except admin-ajax) |
| **Sitemap** | XML sitemap from the SEO plugin: pages, products, posts. Submit in Search Console |
| **Schema** | **Organization** (name, logo, email, `areaServed`) + **WebSite** sitewide · **Product + Offer** on products (GBP price, availability, `itemCondition: New`, brand EVTRON / Fox ESS, colour variants via `hasVariant`/ProductGroup where supported, `hasMerchantReturnPolicy` once the policy exists) · **BreadcrumbList** on everything but home · **Service** ("EV charger installation", `areaServed`, provider) on /installation/ · **FAQPage** on FAQs and product FAQs (valid markup, though Google now shows FAQ rich results mainly for authoritative government and health sites, so no rich result is expected) · **Article** on guides · **LocalBusiness: not used** unless the client has customer-facing premises · **Review/AggregateRating: not used** until real reviews exist |
| **Open Graph / Twitter** | Per-page title, description and a **dark-brand 1200×630 share image** (generated per template in Phase 6) |
| **Images** | WebP/AVIF, explicit dimensions, descriptive alt, filenames with keywords (`fox-tethered-ev-charger-pink.webp`) |
| **Internal linking** | Every guide links to 1 to 2 product pages plus a related guide. Product pages link to Installation, Grants (where relevant) and Compare. Breadcrumbs everywhere. A footer "Learn" column |
| **Redirects** | New site, so no legacy redirect map. Redirect `/shop/` → `/ev-chargers/`, `/cart/` → `/basket/`, `www` → apex, `http` → `https` (Hostinger / .htaccess) |
| **Locale** | WordPress language **English (UK)**, timezone **Europe/London**, currency GBP, prices incl. or excl. VAT per Q3 |
| **Pre-launch** | "Discourage search engines" ON during the build. The Coming-soon page sits in front. At launch: turn discouragement off, maintenance mode off, submit the sitemap |
| **Performance (SEO-relevant)** | Targets in Phase 7: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1. A lean plugin set. Self-hosted Manrope + Plex Mono (subset, 3 to 4 files) |
| **Accessibility (SEO-relevant)** | WCAG 2.2 AA, descriptive link text, form labels |

## 7. Measurement
- **Google Search Console** (domain property) at launch.
- **Analytics:** privacy-friendly and consent-aware. Options are decided in Phase 4: GA4 with Consent Mode v2 plus a lightweight consent banner, *or* cookieless analytics (e.g. Plausible) and no banner needed. Recommendation to follow in architecture.md.
- Events: finder completed, home-check result, add to basket, begin checkout, purchase, quote submitted, email/phone clicks.

## 8. Open items affecting this plan
Q3 VAT status (price wording) · Q5 service area (local pages, schema) · Q8–Q10 standard installation and survey (checker, installation page, terms) · Q15 EVTRON connectivity and compliance (what the product page can say, and whether it can be sold) · Q18–Q20 Fox models · Q21 OZEV list and installer (grant page scope) · Q24–Q25 warranty and refunds (legal pages, schema return policy).
