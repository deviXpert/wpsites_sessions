# 3 · Header, Footer & Inner Pages

The same conventions as the homepage apply: section → boxed inner, globals only, and the glass card recipe.

## Header – Theme Builder (ID 5717, `templates/gs-header.json`)
| Part | Settings |
|---|---|
| **Root container** | HTML tag `header`, Full width. Background Classic = global `gstransparent`. Z-index 99. **Motion Effects › Sticky: Top**, Sticky On: desktop, tablet and mobile, **Effects Offset 60**. CSS class **`gs-glass-header`** (after 60px of scroll it becomes 72% navy with blur, a shadow and a hairline border) |
| **Header bar** (boxed) | Row, Space Between, Align Center, padding 14/24 (mobile 12/16) |
| **Logo** | For now a Heading (`div`) reading "Graphics <span>Storm</span> Studio" in *H4*, with class `gs-grad`, linking to /. **Swap it for the Site Logo widget** once the logo is uploaded (Site Settings › Site Identity) |
| **Nav Menu** (Pro) | Menu **GSS Main** (new menu ID 9: Home, About Us, Services ▸ 4 services, Our Work, Contact Us). Horizontal, pointer Underline (Fade), submenu chevron, global *Navigation*. Items white → Light Blue on hover/active. Dropdown `#0E1738`, radius 14, item hover Brand Blue. **Breakpoint: Tablet** (burger, full-width dropdown, toggle on 10% white glass) |
| **CTA button** | "Free Consultation" → /contact-us/, size small, **hidden on mobile** |

Display conditions are currently **only the 9 redesign drafts**. At launch, change them to **Entire Site** (see the checklist).

## Footer – Theme Builder (ID 5719, `templates/gs-footer.json`)
- **Section** with HTML tag `footer`, bg variant c, padding 80/64/48.
- **Columns row** (wraps on tablet, stacks on mobile):
  1. **Brand (34%):** logo, a one-line agency description, and **Social Icons** (circle, glass fill, 1px border, hover violet). Icons: Instagram, WhatsApp, Facebook, LinkedIn. ⚠ The Facebook and LinkedIn links are placeholders (`#facebook-url-here`), so enter the real URLs or delete those icons.
  2. **Company (18%):** H2 styled as *H4* "Company", plus an Icon List of links (Home, About, Our Work, Contact, Free Consultation).
  3. **Services (22%):** links to the four service pages plus Logo & Branding.
  4. **Get in touch (26%):** email (mailto), phone (tel), and both office addresses.
- **Bottom bar:** a 1px top border (`gsline`). On the left, a **Heading with the Current Date Time dynamic tag** (format `Y`) that outputs "© 2026 Graphics Storm Studio. All rights reserved." and updates the year automatically. On the right, an inline Icon List with Privacy Policy and Terms. ⚠ Neither page exists yet; create them before launch.

## About Us (draft 5725 → replaces page 2738)
1. **Page hero** (shared pattern): eyebrow, H1 *A Design-Led Digital Marketing Agency Built for <span>Growth</span>*, lead, and two buttons (Free proposal / Call). Centred, max width 760, bg a.
2. **Our story:** Row with 📷 `about-team.webp` (1000×1100, radius 24) at 45% and copy at 55% (H2, two paragraphs, three glass timeline cards: Where it began / How we evolved / Where we are today). Below that, the **stats panel** (same as the homepage).
3. **CEO message:** a large glass strong quote card with a quote icon in violet, the quote in *H3*, then a row with 📷 `ceo-portrait.webp` (400×400, round, 64px) and the name and role.
4. **Values:** Grid 3/2/1 with 6 glass icon boxes (Client satisfaction, Clear communication, Team of experts, Premium designs, Professional service, On-time delivery).
5. **Team:** Grid 5/3/2 of glass cards, each with 📷 `team-<firstname>.webp` (600×600), name (H3 in *H4*) and role (Light Blue). Team: Fahad Mustafa Butt (CEO), Nabeel Ali Butt (Creative Director), Saba Baig (Project Manager), Isha Tariq (Content Manager), Muhammad Usman (Graphic Designer).
6. **CTA Band** template.

## Service page template (×4) (`templates/gs-service-page.json`)
Drafts: Website Development 5727 → 5429 · SEO 5729 → 5607 · Social Media Marketing 5731 → 5516 · Graphic Design 5733 → 5562.
All four use the same structure; only the copy changes (all of it lives in `tools/content.py`).
1. **Hero** (bg a): Row 56/44, stacks on tablet. Left: eyebrow (service name), **H1** with gradient keyword, lead, buttons *Get a Free Quote* (→ `#service-quote`) and *Call +1 (812) 818-2053*. Right: glass strong panel "What's included" with an Icon List of 6 checks.
2. **Benefits** (bg b): section head *Why Invest in Professional <span>[Service]</span>?* and a Grid 3/3/1 of 3 glass icon boxes.
3. **Services we offer** (bg c): Grid 3/2/1 of 6 glass icon boxes (the sub-services).
4. **Process** (bg a): the same 4 steps as the homepage.
5. **FAQ + quote form** (bg b): Row 55/45. Left: H2 "[Service] FAQs" and an Accordion with **FAQ schema**. Right (CSS ID `service-quote`): glass strong panel with a Form (Name, Email, Phone, Project details). The form name is "[Service] Quote", so submissions can be told apart.
6. **CTA Band** template.

**To create a 5th service later:** in Elementor, open any service page, then Save as Template, then duplicate it and change the texts. Or add an entry to `SERVICE_PAGES` in `content.py` and run `python3 build.py --push`.

**SEO meta titles and descriptions** for each service are in `content.py` (`meta_title`, `meta_desc`). Paste them into Rank Math/Yoast (see the checklist).

## Our Work (draft 5737 → replaces page 4569)
1. Page hero: H1 *Websites, Brands & Campaigns That <span>Get Results</span>*.
2. **Portfolio:** an inline category list (Websites · Branding · Social Media · SEO · Graphic Design) and a **Grid 3/2/1 of 6 project cards**. Each card is glass with hover lift and contains 📷 `project-N.webp` (1200×900, 4:3, radius 14), the category eyebrow, an H2 project title in *H3*, and a one-line result.
   ⚠ The project names and results are bracketed placeholders, so replace them with real projects before publishing.
   *Later upgrade (native):* create a "Project" post type with ACF or Pods, then use a **Loop Grid** with a **Taxonomy Filter** widget for real filtering. No custom code needed.
3. Testimonials carousel.
4. CTA Band template.

## Contact Us (draft 5739 → replaces page 2802)
1. Page hero (no buttons): H1 *Let's Talk About <span>Growing Your Business</span>*.
2. **Contact row** (40/60, stacks on tablet):
   - **Info column:** an H2 in *H3*, intro text, then 5 glass Icon Boxes with the icon on the left: Email (mailto), Call (tel), WhatsApp (wa.me, opens in a new tab), Canada office, USA office.
   - **Form column:** glass strong panel with the **full Form**: Name*, Email*, Phone, Website, Monthly budget (select), Services (checkboxes), Project details, honeypot. Button *Send My Request*, plus a privacy note below.
3. **FAQ:** 3 questions with FAQ schema.

*(Optional)* Add a **Google Maps** widget under the offices. It loads a third-party iframe, so lazy-load it or leave it out for speed.

## Services hub (draft 5735 → replaces page 4213)
Page hero, then the 6 service cards (titles as H2, since this page lists the services), then the process with the stats panel, then the CTA band.
