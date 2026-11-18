# Competitor teardown (Phase 1)

Researched on 18 November 2026 from a cloud browser (Chromium 1440×900 desktop and iPhone 13 emulation) plus raw HTML crawls. Data: `research/competitors/*.jsonl`. Screenshots: `research/shots/` (not committed) and contact sheets `research/sheet_*.jpg`.

**Method limits, stated honestly**
- **greenpluguk.com blocked automated access** (HTTP 403 to both the raw request and a real headless browser). I haven't assessed it and won't guess its content. If you want it covered, send screenshots or a PDF export.
- The research browser's traffic leaves from a **non-UK IP**. Hypervolt's root URL redirected to `/en-US/`, and Octopus showed a "visit Octopus US?" prompt and returned a 404 on `/ev-charger/`. I analysed the UK versions directly (`hypervolt.co.uk/en-GB/`, `octopus.energy/ev-charger-sales/`).
- **Lighthouse and PageSpeed were not run on competitors** (at your request). Performance notes below are limited to HTML weight, script counts and observed behaviour, not Core Web Vitals.
- Brief-listed references were also reviewed: **Vorsprung** (vorsprung.com), **NextGen Charge** and **Fox ESS**. Costco's Fox listings were not crawled.
- Nothing here is to be published. These are internal pattern notes, not claims about competitors.

---

## 1. At a glance

| Site | Stack | Look | Primary CTA | Pricing shown | Trust signals | Schema |
|---|---|---|---|---|---|---|
| **EVolt Energy** | Framer | **Pure black + neon green `#0FFF00`**, DM Sans | "Make An Enquiry" | "Prices start from £799" | Google reviews, Klarna, grant block | None |
| **Octopus** (EV chargers) | Next.js / Vercel / Storyblok | Deep purple `#100030` + pink, custom font | Postcode → "Show prices" | Only after postcode | Trustpilot, "most awarded" | Corporation, AggregateRating, WebSite |
| **Cord** | Magento | Charcoal `#1B1C1B` + hot pink, Nunito | "Shop the Cord Zero" | "From £479 / installed from £979" | Which? badge, Trustpilot, Feefo, no-quibble guarantee | Organization, FAQPage, ItemList |
| **myenergi** | **WordPress + WooCommerce** | White / near-black hero + **bright green `#40FF7A`** | "Get an installation quote" | Shop prices | Trustpilot, awards | Product, AggregateRating, Review, Breadcrumb, FAQ |
| **Hypervolt** | Custom JS app on S3 | White + purple glow | "Buy" | Behind the Buy flow | Trustpilot 4.8, warranty | Product, Offer, MerchantReturnPolicy, Breadcrumb |
| Vorsprung *(brief ref)* | Shopify | White, product-retail | Add to basket / Buy now | £ with strike-through discounts | Review stars, OZEV block | Product, Offer |
| NextGen Charge *(brief ref)* | Shopify | White + green | "Get a quote" / "Book installation" | Product price | 7-year warranty, grant banner | Organization only |
| Green Plug UK | ❌ blocked (403) | not seen | not seen | not seen | not seen | not seen |

## 2. Site by site

### EVolt Energy (evoltenergy.co.uk)
- **Structure:** Home / About / Services / Contact / Google Reviews. An installer-led services site, not a product shop. Phone number in the header.
- **Hero:** "EVolt Energy / Powering tomorrow, today." with a generic sustainability paragraph and a "HOT! Prices start from £799" pill.
- **Visual:** pure `#000` background with saturated `#0FFF00` buttons. **This is the closest competitor to a "dark + green" look, so EVTRON must be clearly different from it.**
- **Problems:** **3 H1s** on the homepage, duplicated headings (Framer breakpoints render twice), no structured data, 1.2MB HTML and 142 images on the home page, a very long mobile page (~23,800px), and a chat bubble overlapping the hero CTA on mobile. Copy is generic ("cutting-edge solutions"), and the same title tag is used on `/services`.
- **Good:** low-friction enquiry CTA and a visible phone number.

### Octopus Energy (EV charger sales)
- **Hero:** "Save up to 85% when you charge your EV at home" plus a "verify our claims" link. Strong claim, with the evidence linked.
- **Flow:** **postcode-gated prices** ("Enter your postcode for prices including installation"), then choose a charger, then installation. Bundled with their tariffs.
- **Trust:** brand scale, Trustpilot, 7-day support hours stated.
- **Problems (for this use):** the charger shop is a sub-section of an energy-supplier site, prices are hidden until a postcode is entered, and the experience relies on the Octopus tariff relationship.
- **Pattern worth learning:** a "how it works" step list, support hours stated plainly, and claims with a linked evidence page.

### Cord (cord-ev.com)
- **Structure:** clear product-type nav (Home chargers / Cables / Portable / Business / Tech support).
- **Best-in-set content:** "Installation, without the surprises": what's included vs what costs extra, "Is my installation standard?", a lead-times block, a survey-to-switch-on step list, and a "buy unit only" option. Title tags carry prices ("From £479, Installed From £979").
- **SEO:** good titles and metas, FAQPage schema on category and installation pages, breadcrumbs, and guide content (grant for flats and renters, tariff compatibility, cost to charge).
- **Problems:** the Black Friday countdown banner dominates the first screen. On mobile, the cookie banner plus promo cover most of the viewport. Hot-pink-on-charcoal is busy.

### myenergi (myenergi.com)
- **Relevant precedent:** **WordPress + WooCommerce**, i.e. the stack we'll use.
- **Structure:** a large mega-menu (Products / Home charging / Solar ecosystem / Installers / Business / Support / Our energi) aimed at many audiences, plus a country selector.
- **Visual:** dark hero, white body, **green `#40FF7A` buttons (nearly identical to EVTRON's `#3BE37F`)**.
- **SEO:** the richest schema in the set (Product, AggregateRating, Review, BreadcrumbList, FAQ) and Rank Math-style robots meta.
- **Problems:** a Cookiebot **full-screen consent modal** blocks first use on mobile. Only 25 of 68 home images have alt text, there's no OG image on the home page, and 19 scripts plus 13 stylesheets load on the home page. The product page H1 is lowercase "zappi ev charger".

### Hypervolt (hypervolt.co.uk/en-GB)
- **The brief's main visual reference.** A product-first homepage: "Meet the Home 3 Pro", three colourways side by side, "Process" (installer match → schedule → delivery), tariff comparison, durability stats (IK10 / IP66 / UV), warranty 3 or 5 years, cable options, colours, app.
- **Product page:** sub-tabs (Overview / Tech Specs / Compare / Warranty), a colour picker, Type 1/2 cable options, an accessories block and FAQs. **Product + Offer + MerchantReturnPolicy schema**.
- **Trust bar:** In stock · Free next-day delivery · Secure checkout · Installed in under 3 weeks · Trustpilot 4.8.
- **Problems:** the `/en-US/` shell has **no server-rendered content** (21KB, no headings), so it depends on JavaScript. The root redirects by geo, and the product page's meta description is thin. The purple glow and lightning-bolt imagery is a category cliché.

### Vorsprung (brief reference: feature cards, specs, FAQs)
- **Signature interaction:** an **EV savings calculator in the hero** (vehicle model → annual mileage → home/mixed/public → yearly saving, cost per mile, payback months).
- **Product page:** a feature icon row (Speed / Compatibility / OCPP / App / Safety / 30-day return), an OZEV grant explainer in 3 steps, "Pair with a cheaper tariff", and solar and dynamic charging sections.
- **Problems:** heavy discount styling ("Save 38%", strike-through prices), and a WhatsApp float that covers content on mobile. It sells the unit only (no installation), so it's a different offer from EVTRON's.

### NextGen Charge (brief reference)
- A "Get a free quote" page with a form for a transparent price breakdown and a grant check. A grant banner sits on every page.
- **Problems:** a **modal popup on load** ("Book your installation date") blocks the hero on desktop and mobile. The `<title>` is polluted with payment-icon text ("Next Gen ChargeAmerican ExpressApple Pay…"), the H1 is a long sentence, there's no OG image, and 40 scripts plus 27 stylesheets load on the home page.

### Fox ESS (manufacturer, for the Fox product pages)
Global corporate site; the UK charger range is A Series, A-Lite (L MAX) and C Series. The L Series datasheet (PDF) is the official spec source. Useful as a data source only, not as a design reference.

---

## 3. Common patterns and clichés to avoid
- **Lightning bolts, glowing edges and neon** (Hypervolt purple glow, EVolt neon green, bolt icons everywhere).
- **"Powering the future / tomorrow"** taglines and abstract sustainability copy.
- A hero photo of a car on a driveway with a cable plugged in.
- **Overlays stacked on the first screen:** cookie wall + promo banner + chat bubble + WhatsApp float + popups. The first mobile screen is often 50 to 80% covered.
- Discount theatre: countdowns, strike-throughs, "HOT!" pills.
- Trustpilot star bars as the main trust device.
- Grant banners ("Save up to £500 via Government Grant") repeated site-wide without explaining who qualifies.

## 4. Weaknesses and usability problems
1. **Price opacity:** Octopus needs a postcode, EVolt gives only "from £799", and Hypervolt hides the installed price inside the buy flow. Only Cord states installed prices clearly.
2. **Unclear "standard installation":** only Cord explains what's included and excluded, and what happens if your home isn't standard.
3. **Intrusive overlays on mobile** (all except Hypervolt to some degree).
4. **Generic, interchangeable copy** (EVolt, NextGen).
5. **Choice paralysis vs no guidance:** myenergi's mega-menu is huge, while most others give no "which charger suits me?" help apart from Cord's vehicle finder and Vorsprung's calculator.
6. **Solar compatibility is muddled:** solar is rarely explained in terms of "you need X inverter or meter".

## 5. Content and SEO gaps
- **Heading hygiene:** multiple H1s (EVolt), truncated or sentence H1s (NextGen), product-name-only H1s (Hypervolt, myenergi).
- **Title tags:** polluted (NextGen), duplicated across pages (EVolt), brand-only (Hypervolt product).
- **Schema:** missing entirely on EVolt and largely on NextGen. Only Hypervolt and myenergi mark up Product/Offer. **None of the sites reviewed use HowTo-style installation content or a properly marked-up price spec for installed bundles.**
- **Alt text:** poor on myenergi (25/68) and Fox (54/167).
- **Information gaps no one fills well:**
  - an honest, specific **grant eligibility explainer** (houses vs flats and renters, on-street, landlord), sourced to gov.uk and dated
  - "**tethered vs untethered**" and "**do I need solar compatibility?**" decision content
  - **Smart Charge Points Regulations**: what default off-peak hours and randomised delay mean for the owner
  - a **cost to charge at home** explainer that avoids invented savings figures
  - local / area pages (if EVTRON serves defined areas)

## 6. Performance observations (not lab-tested)
| Site | Home HTML | Scripts / stylesheets | Notes |
|---|---|---|---|
| EVolt | 1.2MB | 2 / inline | Very heavy HTML (Framer inlines everything), 142 images |
| Cord | 308KB | 9 / 4 | Reasonable |
| myenergi | 145KB | 19 / 13 | WooCommerce plugin sprawl, Cookiebot |
| Hypervolt | 163KB | 1 / 2 | Single bundle, but JS-rendered |
| NextGen | 354KB | 40 / 27 | Shopify app sprawl |
| Octopus | 818KB | 30 / 3 | Next.js page data |

**Lesson for us:** WooCommerce + Elementor can be fast or slow; plugin and script discipline decides it. We'll set budgets in Phase 7.

## 7. Opportunities: where EVTRON can be clearly better
1. **The most transparent price in the category.** Show the installed price, incl. VAT, on every card and product page, with no postcode gate. Next to it, a plain "**What's included / What would cost extra**" panel with the actual numbers (once you supply them).
2. **"Is my home standard?" check before checkout.** Four or five quick questions plus optional photo upload (meter, consumer unit, parking spot), in plain English, inside the purchase flow. This reduces refunds and builds trust. Competitors bury this.
3. **"Which charger suits me?" in 3 questions** (solar panels? / want a cable always attached? / colour preference), recommending one of the three products with honest reasons. That's a genuinely useful signature interaction, and it's small and fast.
4. **Honest configurator.** Live colour swatches and cable lengths, with unavailable options shown disabled with a reason ("5m not currently available"), plus clear CT-clamp-included messaging. This is the fairness the brief asks for.
5. **Owner-focused grant explainer**, sourced to gov.uk and dated, with a 3-question eligibility check that tells most house owners honestly that they're not eligible.
6. **Calm first screen.** No popups, no countdowns, no chat bubble over CTAs, and a small non-blocking consent banner (only if non-essential cookies are used at all).
7. **Distinctive dark design.** No glow and no bolts. Warm-white type on a tinted near-black, a technical "spec sheet" voice using IBM Plex Mono for numbers, generous whitespace and a restrained accent. That's far from EVolt's neon-on-black and Hypervolt's purple glow.
8. **SEO done properly:** one H1 per page, keyword-led titles, Product/Offer schema with accurate prices, FAQ and Breadcrumb schema, OG images, and alt text everywhere. Most competitors miss at least half of these.
9. **Speed as a feature:** a lean Elementor build (native widgets, few plugins, no heavy consent platform, self-hosted fonts) aiming for 90+ mobile Lighthouse scores, which most WooCommerce sites miss.
10. **Solar clarity for the Fox range:** explain exactly what's needed for solar-surplus charging (a Fox hybrid inverter, or a Fox smart meter/CT for other inverter brands, *once verified with Fox*).
