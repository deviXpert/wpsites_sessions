# EVTRON architecture (Phase 4)

Draft for Checkpoint 4, 18 November 2026.

## 1. Stack decision

The platform was set by the user: **WordPress + Astra + Elementor Pro + WooCommerce, with Stripe and PayPal**, hosted on the existing **Hostinger** plan. For the record, here's how it compares with the alternatives:

| | WordPress + Elementor Pro + WooCommerce (**chosen**) | Shopify | Headless (Next.js/Astro + CMS + Stripe) |
|---|---|---|---|
| Fit with brief | ✅ All needs met (variations, posts, forms, content, SEO) | ✅ Strong e-commerce | ✅ Anything, all custom |
| Who maintains | The developer (user), in tools already in use | Anyone, but theme dev is Liquid | Developer only |
| Performance | Good **if** kept lean (target 90+). Needs discipline | Good by default | Best possible |
| Instalments | Klarna (Stripe), PayPal Pay in 3 | **Shop Pay Installments** + others | Klarna via Stripe |
| Cost | Existing hosting + Elementor Pro (owned), plugins mostly free | Monthly plan + transaction fees | Hosting + much more dev time |
| Existing setup | Already installed on evtron.co.uk | Rebuild elsewhere | Rebuild elsewhere |

The only feature the chosen stack can't offer is **Shop Pay Installments** (Shopify-only). Klarna and PayPal Pay in 3 cover the same need.

## 2. Hosting (current, verified)
Hostinger shared/cloud hosting · **LiteSpeed** web server · Hostinger CDN (currently **disabled** by the user during API testing) · PHP 8.3 · HTTPS active. The site is **not live yet** (empty), so we build directly on it behind Coming Soon mode, with a staging copy for risky changes (Hostinger's one-click staging, if the plan includes it ❓).

## 3. Plugin list (lean by design)
| Purpose | Plugin | Why |
|---|---|---|
| Page builder | **Elementor + Elementor Pro** (installed) | Theme Builder, WooCommerce widgets, Loop Grid, Forms, Custom Code, Coming Soon |
| Theme | **Astra** (installed, free) | Light, Elementor-friendly. Header/footer are built in Elementor |
| Shop | **WooCommerce** | Products, variations, basket, checkout, orders, emails |
| Payments | **WooCommerce Stripe Gateway** (official, free) | Cards, Apple Pay, Google Pay, Link, **Klarna** |
| Payments | **WooCommerce PayPal Payments** (official, free) | PayPal, **Pay in 3** (Pay Later) |
| SEO | **Rank Math** (free) *or* Yoast | Recommend **Rank Math**: free WooCommerce Product schema, breadcrumbs, redirects, sitemap and 404 monitor in one plugin. Yoast needs a paid add-on for WooCommerce schema |
| Cache and performance | **LiteSpeed Cache** (free) | Native to the LiteSpeed server: page cache, CSS/JS optimise, WebP/AVIF via QUIC.cloud, lazy-load. WooCommerce-aware (basket/checkout excluded) |
| Email delivery | **FluentSMTP** (free) | Sends WooCommerce and form emails through an authenticated mailbox (SPF/DKIM) so they don't land in spam |
| Spam protection | **Cloudflare Turnstile** via Elementor Forms (native integration) or "Simple Cloudflare Turnstile" for WooCommerce checkout | Privacy-friendly, no cookie banner needed, no image puzzles |
| Security | **SG Security: delete** (left over from an old host). Use Hostinger's malware scanner + strong passwords, 2FA (e.g. "Two Factor" plugin) and limited admin users | Fewer plugins |
| Backups | Hostinger automatic backups + **UpdraftPlus** (free) to off-site storage (Google Drive/Dropbox) | Off-site copy before updates |
| Colour swatches | **No plugin.** A small Custom Code script turns WooCommerce's native variation `<select>` into accessible swatch buttons (the select stays as the source of truth) | Avoids a heavy swatch plugin |

**Not installed:** sliders, page-speed "all-in-ones", icon-font packs, Google Fonts loaders, chat widgets, popup builders.

## 4. Content model (WooCommerce)
| Product | Type | Attributes / variations | Notes |
|---|---|---|---|
| EVTRON Tethered EV Charger | Variable | **Colour** (Mythos Black, [Red TBC], Space Grey, Midnight Green) × **Cable** (7.5m, 10m) | 5m **not created** (unavailable). 10m variation set to "out of stock" until confirmed. Price per variation (+£35/+£90 per Q14) |
| Fox Tethered Solar EV Charger | Variable | Colour (Black, Blue, Purple, Pink) | Cable fixed at 5m (6m optional, TBC) |
| Fox Untethered Solar EV Charger | Simple | — (White) | |
| Extended warranty (+2 years, 5 total) | Simple, virtual | — | Offered as a **cross-sell** in the basket and as a checkbox-style upsell on product pages |
| Black / Steel charging post | Simple | — | Accessories page + cross-sells |
| CT clamp | **Not sold** for EVTRON (included). Only listed if it's a genuine optional accessory for another product | | |

- **Category structure:** `ev-chargers`, `accessories`. Product permalink `/%product_cat%/` gives `/ev-chargers/<product>/` (approved). This gets tested for clashes before launch.
- **Shipping:** "Installation included" is set as a zero-cost shipping method named **"Supplied and fitted"**, limited to the service area postcodes (Q5 ❓). Orders outside the area are blocked at checkout with a message pointing to Get a quote.
- **Checkout fields:** WooCommerce defaults + **installation address** (shipping address relabelled), phone (required), **parking type** and **vehicle** (optional), preferred installation weeks. Added with native WooCommerce checkout field code in Custom Code, or a tiny snippet (no field-editor plugin).
- **Photo upload:** not at checkout (keeps checkout fast and avoids a plugin). Instead, on the **Thank You page** an **Elementor Pro Form** ("Send us 3 photos") with File Upload fields, prefilled with the order number. Files are stored in a protected uploads folder and emailed to sales@. The same form is used on Get a quote.
- **Taxes:** depends on Q3. If VAT-registered: prices entered incl. VAT at 20%, with "incl. VAT" shown. If not: tax disabled and no VAT wording.
- **Accounts:** guest checkout ON. Account creation optional at checkout (for order tracking). `/my-account/` noindexed.
- **Emails:** WooCommerce emails restyled to the dark brand (header logo, ink background, warm-white text). From: `EVTRON <sales@evtron.co.uk>`. Admin copies to sales@.

## 5. Forms and email
| Form | Tool | Sends to | Spam | Consent wording |
|---|---|---|---|---|
| Get a quote (with photo upload) | Elementor Pro Form | sales@ | Turnstile + honeypot | "We'll use your details to prepare your quote and contact you about it. See our Privacy policy." (no pre-ticked marketing box) |
| Contact | Elementor Pro Form | info@ | Turnstile + honeypot | as above |
| Post-order photos | Elementor Pro Form (Thank You page) | sales@ | Turnstile | as above |
| Coming Soon "notify me" (optional) | Elementor Pro Form | info@ | Turnstile | Explicit opt-in checkbox (unticked) |

Form submissions are also saved in Elementor → Submissions (database) as a backup. **Mailboxes:** sales@ and info@ must exist (Hostinger Email ❓) and FluentSMTP sends through one of them. DNS gets SPF, DKIM and DMARC records.

## 6. Analytics and consent
**Recommendation: cookieless analytics, no cookie banner.**

| Option | Banner needed? | Cost | Notes |
|---|---|---|---|
| **A. Plausible (or similar cookieless tool)**, recommended | **No** (no cookies, no personal data) | about £8 to £9 a month | Lightweight script (<1KB). Tracks pages, sources, and custom events: finder, home check, add to basket, purchase, quote |
| B. GA4 + Consent Mode v2 + a light consent banner | Yes | Free | More detail and Google Ads integration later. Needs a dark-styled banner, and data only from people who accept |
| C. Both later | Yes | — | Start with A, add B when advertising begins |

**Cookies that remain without a banner:** WooCommerce session/basket cookies, Stripe and PayPal fraud-prevention cookies and Turnstile. These are **strictly necessary** under PECR, so no consent is required. They'll be listed in the cookie policy.

## 7. Performance plan (summary; detail in Phase 7)
- **Budgets per template (mobile):** HTML ≤ 60KB · CSS ≤ 120KB (after LiteSpeed optimise) · JS ≤ 150KB on content pages and ≤ 300KB on product/checkout (Stripe/PayPal are heavy and load only there) · fonts ≤ 120KB (4 to 5 WOFF2 files) · hero image ≤ 120KB AVIF/WebP · total ≤ 1MB on Home.
- **Elementor settings:** Optimized DOM output, Improved CSS/asset loading, Inline font icons on, Google Fonts **off** (self-hosted via Elementor Custom Fonts), Font Awesome **off** (inline SVG icons), lazy-load background images.
- **WooCommerce:** cart fragments script disabled on non-shop pages, no WooCommerce CSS/JS on content pages.
- **LiteSpeed Cache:** page cache, CSS/JS minify (combine off), defer JS, critical CSS (QUIC.cloud), image optimisation to WebP/AVIF, preload the LCP image.
- **Lighthouse CI:** a GitHub Action in this repo runs Lighthouse against key URLs (Home, Choose your charger, a product, Installation, Basket) on demand and after deploys, with assertions at 90+.

## 8. Development and deployment workflow
- **Build where it lives:** pages and templates are built in Elementor on evtron.co.uk behind **Coming Soon mode**, with "Discourage search engines" on.
- **Version control in this repo:** design tokens, Custom Code snippets (CSS/JS), checkout field snippets, Elementor template exports (`.json`) and product data (CSV), so everything can be rebuilt or reviewed. Synced to WordPress via the REST API, using the app password from environment variables.
- **Staging:** Hostinger staging (if available ❓) for plugin updates and risky changes after launch.
- **Launch:** checklist in `deployment.md` (Phase 9).

## 9. Secrets and access
- WordPress app password, and Stripe/PayPal keys **only** in environment variables or WordPress settings. Never in this repo.
- Stripe and PayPal accounts are owned by the client (task #2). The developer gets team or user access, not shared passwords.
- `WP_USER` in the session environment should be corrected to the admin login.

## 10. Questions for Checkpoint 4
1. **SEO plugin:** Rank Math (recommended) or Yoast?
2. **Analytics:** A (cookieless, no banner, about £9/month), B (GA4 + banner, free) or C?
3. **Mailboxes:** do sales@ and info@evtron.co.uk exist yet (Hostinger Email)? Which one should send the site's emails?
4. **Staging:** does the Hostinger plan include staging?
5. **Off-site backups:** OK to use UpdraftPlus to Google Drive or Dropbox (whose account)?
