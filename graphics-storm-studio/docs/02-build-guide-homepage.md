# 2 · Homepage Build Guide

The finished build is the draft **"Home – Redesign"** (page ID 5723); the importable file is `templates/gs-home.json`.
Page settings: Template **Elementor Full Width** (`elementor_header_footer`), Hide Title **on**.

**Conventions used on every section**
- **Outer container** (the section): Content Width **Full**, HTML tag `section`, Direction Column. Padding 112/0 (tablet 88, mobile 64). Background is a native radial gradient plus a radial overlay (variant a/b/c, see the spec).
- **Inner container:** Content Width **Boxed** (it takes the 1240px width from Site Settings), Gap 48, Padding 0 24 (mobile 0 16).
- **Section head** (a saved template, `gs-section-title.json`): Eyebrow (Heading `p`, global *Eyebrow*, colour *Light Blue*), H2 (global *H2 – Section*, colour *White*, CSS class `gs-grad`, highlighted words wrapped in `<span>`), and an intro (Text Editor, global *Lead*, max width 720px, 100% on tablet).
- **Glass card:** see the spec. Background `gsglass`, border 1px `gsline`, radius 20, card shadow, padding 32/28/24, class `gs-glass`, hover lift.
- **Rows** stack on mobile (Direction Column), and two-column rows also stack on tablet. Grids are native **Grid containers** with 3 columns on desktop, 2 on tablet and 1 on mobile.

---

## 1 · Hero (`#free-proposal`)
**SEO title (H1):** *Grow Faster With a Digital Marketing Agency That <span>Delivers Results</span>*

| Structure | Widgets & settings |
|---|---|
| Section (bg variant **a**, padding 96/72/48, gap 64) → Inner (boxed) | |
| ▸ **Hero Row**: Direction Row, Align Center, Gap 56, Direction **Column on tablet & mobile** | |
| ▸▸ **Hero Copy** (width 55% / tablet 100%), Gap 24, Motion › Entrance *Fade In Up* (fast) | **Eyebrow:** "Digital Marketing Agency · USA & Canada" |
| | **Heading H1:** global *H1 – Hero*, class `gs-grad` |
| | **Text Editor (Lead):** "Graphics Storm Studio builds high-converting websites, ranks you on Google with proven SEO services and grows your audience with social media marketing and standout graphic design – all from one dedicated team." |
| | **Buttons row** (wrap; column on mobile, stretched): *Get a Free Proposal* (primary → `#free-proposal`) and *View Our Work* (ghost → /our-portfolio/) |
| | **Icon List (inline)**, global *Small*: ★ 130+ happy clients · 🏆 5+ years experience · 🌎 USA & Canada offices |
| ▸▸ **Hero Form** column (45% / tablet 100%), CSS ID `free-proposal` | **Glass panel strong** (`gs-glass--strong`, bg `gsglass2`, radius 24, padding 32/28/22): H2 "Get Your Free Proposal" (global *H3*), Small text "We reply within 1 business day", **Form** (Elementor Pro): Full name*, Email*, Phone/WhatsApp, Services checkboxes (Website Development, SEO, Social Media Marketing, Graphic Design, Logo & Branding, Paid Ads), honeypot, button *Get My Free Proposal* (100%, paper-plane icon). CSS class `gs-form` |
| ▸ **Client Logos** (column, gap 24) | Small muted label "Trusted by growing brands across the USA, Canada & beyond" + Grid 5/3/2 of 5 **Image** placeholders (width 140px, opacity .75). 📷 `client-logo-1…5.svg` – 240×96, light version, transparent background |

**Form actions:** Email to info@graphicsstormstudio.com (Reply-To = the email field) and Collect Submissions (Elementor → Submissions). See "reCAPTCHA" in the checklist.

## 2 · Services (`#services`)
- **Section head:** eyebrow "What we do". H2 *Digital Marketing Services Built to <span>Grow Your Business</span>*. Intro: "From website development and SEO services to social media marketing and graphic design – everything you need to attract, convert and keep customers."
- **Grid** 3 / 2 / 1, gap 24. There are 6 **glass cards with hover lift**, each a Container (Justify *Space Between*) holding:
  - **Icon Box:** View *Stacked*, Shape *Rounded*. Primary colour `gsglass2`, secondary (icon) *Light Blue*. Icon 26px, padding 16, radius 14. Title tag **h3**, global *H3*, white. Description global *Body*. The whole box links to the service page.
  - **Button "Learn more"** (text-link style).
- The six cards are Website Development, Search Engine Optimization, Social Media Marketing, Graphic Design, Logo & Brand Identity, and Paid Advertising (PPC). They link to the matching service pages, with PPC linking to Contact.
- To reuse a card, save one as `GS – Service Card` (`templates/gs-service-card.json`).

## 3 · Why Choose Us + Stats
- **Row** (copy 45% / cards 55%; stacks on tablet), gap 56.
  - **Copy:** eyebrow "Why Graphics Storm Studio". H2 *The Digital Marketing Partner That Treats Your Growth <span>Like Its Own</span>*. Lead paragraph. Icon List with check-circle icons (Personalised campaigns… / Reach your ideal audience faster / Low cost, high return marketing / Honest monthly reporting). Ghost button *About Our Agency*.
  - **Cards:** a 2×2 grid (1 column on mobile) of glass Icon Boxes: Results you can measure · One dedicated team · Budget-friendly plans · On-time delivery.
- **Stats panel:** glass strong (radius 24, padding 48/40/28) containing a Grid 4 / 2 / 2 of **Counter** widgets (0 → 514+, 180+, 130+, 5+). Number uses global *Stat* in white, title uses *Body*. Duration 1.6s.

## 4 · Process
Section head: "How we work", H2 *A Simple 4-Step Process to <span>Predictable Growth</span>*. Grid 4 / 2 / 1 of glass cards, each with a number heading (`01`…`04`, global *Stat*, class `gs-grad`), an H3 title and body text: Discover → Strategy → Create & Launch → Measure & Grow.

## 5 · Testimonials
Section head: "Client reviews", H2 *What Our Clients <span>Say About Us</span>*.
**Testimonial Carousel** (Pro) with 3 / 2 / 1 slides per view, space 24, autoplay 6s, loop, pause on hover, bullets. Slide background `rgba(255,255,255,.06)`, border 1px 14% white, radius 20, padding 32/28. Content uses *Body*, name uses *H4* in white, title uses *Small* in Light Blue.
The slides are the 4 real reviews from the old site. The photos were removed because they were hot-linked from globaldigitalnetwork.net, and the review that named that company was dropped. Add real client photos (300×300) to each slide when you have them.

## 6 · FAQ (SEO rich results)
Row: intro 38% / accordion 62% (stacks on tablet).
**Accordion** widget (nested): **FAQ Schema = Yes** (outputs FAQPage structured data), title tag h3, one item open at a time, +/− icons. Item background `gsglass`, border 1px `gsline`, radius 16, padding 20/22. Titles use global *H4* in white (Light Blue on hover/active). The 5 questions target "digital marketing agency", "SEO", "website" and pricing searches.

## 7 · CTA Band (saved template, reused sitewide)
A **Template** widget pointing at **GS – CTA Band** (Templates → Saved Templates, ID 5721). Edit it once and it updates on every page.
Inside: glass strong panel with a 135° gradient (violet 22% → blue 18%), radius 28, padding 64/48/32, centred. Eyebrow "Free strategy call", H2 *Ready to Grow Your Business <span>Online?</span>*, lead text, buttons *Get a Free Proposal* (primary) and *Chat on WhatsApp* (ghost, opens in a new tab with rel=noopener).

---

### Responsive summary (already set in the build)
| | Desktop | Tablet (≤1024) | Mobile (≤767) |
|---|---|---|---|
| Hero | 2 columns | stacked, form below copy | stacked, buttons full width |
| Grids | 3–4 columns | 2 | 1 (stats 2) |
| Section padding | 112 | 88 | 64 |
| H1 / H2 | 64 / 46 | 48 / 38 | 38 / 30 |
| Header CTA button | shown | shown | hidden (menu toggle only) |
