# 4 · Pre-launch Checklist

## A. Already done in this session ✔
- [x] Backed up pages, kit, menus, plugins, themes and the media list to `backup/` (JSON). **Also take a full Hostinger backup** (hPanel → Backups) before launch.
- [x] Theme is **Hello Elementor** 3.5.2. The old Onum-based "Astra" + "Astra Child" are inactive, so bootstrap.css, slick.css, flaticon.css, font-awesome.css, simple-likes and particles.js no longer load.
- [x] Elementor 4.4.2 / Pro 4.3.1 are already current, and **Flexbox Containers are on** (Elementor → Settings → Features).
- [x] CSS Print Method is still **External File**.
- [x] Site Settings applied: colours, fonts, type scale, buttons, form fields, layout, and the global CSS (Site Settings → Custom CSS).
- [x] New menu **GSS Main** created (includes Contact Us; the old "Main Menu" is untouched).
- [x] Header, Footer and CTA Band templates are published, but shown **only on the redesign drafts**. The 9 redesign pages are saved as drafts.

## B. Update order (when you launch)
1. Take a **full backup** (Hostinger + All-in-One WP Migration export downloaded to your computer).
2. Update WordPress core, then **Elementor**, then **Elementor Pro**, then the other plugins, then Hello Elementor. Update one at a time and check the site after each.
3. Go to Elementor → Tools → **Regenerate CSS & Data**.

## C. Launch steps (`python3 tools/launch.py` does steps 2–4 after you say go)
1. Review every draft (links below) while logged in, on desktop and mobile.
2. Copy each draft's design into the **original page** (same ID and URL, so SEO and backlinks are kept): Home 21, About 2738, Website Development 5429, SEO 5607, Social Media Marketing 5516, Graphic Design 5562, Services 4213, Our Work 4569, Contact 2802. Then move the drafts to Trash.
3. Header and Footer: Display Conditions → **Entire Site**.
4. Appearance → Menus: you don't need to assign GSS Main to a location (the Nav Menu widget uses it directly).
5. Elementor → Tools → **Clear Files & Data**, then visit each page once.
6. Turn **off** the Under Construction plugin, then delete it.

## D. Clean-up (old Onum theme leftovers)
| Item | Safe to remove? | Why |
|---|---|---|
| Themes **Astra** (v1.2.7 by OceanThemes) and **Astra Child** | ✅ Approved: **delete in Appearance → Themes** (the REST API can't delete themes) | They are actually the old Onum theme renamed (Onum 1.2.7). Inactive, outdated, and ship old jQuery plugins (a security risk if left installed). Also removes bootstrap.css, slick.css, flaticon.css, font-awesome.css, simple-likes-public.css, particles.js, isotope, magnific-popup and countdown |
| **Kirki** | ✔ **Deleted** 2026-11-27 | It was only the Onum theme's customizer framework |
| **Meta Box** | ✔ **Deleted** 2026-11-27 | Used by Onum for header/footer builder fields. Check that nothing else uses it |
| **Happy Elementor Addons** | ✅ After launch | Only the old pages use its widgets (gradient heading, CF7). The new build uses none |
| **Essential Addons for Elementor** | ✅ After launch | Not used by the new build; loads CSS/JS on every page |
| **Contact Form 7 + Country & Phone Field** | ✅ After launch | Replaced by the Elementor Pro Form (native styling, Submissions, honeypot, reCAPTCHA v3) |
| **All-in-One WP Migration** | ⚠ Deactivate when not in use | Big attack surface; reactivate only to export or import |
| **Under Construction** | ✅ After launch | |
| `ot_header_builders` / `ot_footer_builders` posts (IDs 3050, 3069, 261) | ✅ | Orphaned Onum header/footer data, no longer rendered |
| Old menus "Main Menu" (2), "Menu2" (6) | ✅ After launch | Replaced by GSS Main |
| **127 Media Library items** (uploads 2022/2023) | ✔ **Deleted** 2026-11-27 (list in `backup/media.json`) | All 127 files return 404 (verified). The library entries are empty shells, so delete them and upload fresh images (section F) |
| Legacy colours in Site Settings ("Legacy – …") | ✅ After launch | Only the old pages used them |
| Customizer → Additional CSS of the old theme | ✅ | It no longer loads with Hello, so nothing to do. All CSS now lives in Site Settings → Custom CSS |
| **Joinchat** | – | It is **not installed** (the old button was part of the old theme or code). The new design adds WhatsApp buttons natively (CTA band, Contact, footer). If you want a floating button, install Joinchat and set its colour to `#25D366` or violet |
| **Tidio** | Keep if you use live chat | It loads about 300KB of third-party JS on every page. Consider "load on click" in Tidio settings |
| **Google Tag Manager** (GTM-W59NCNT) | Re-add | It was printed by the old theme, so with Hello Elementor it's **gone**. Add it back with Elementor → Custom Code (Pro) → `<head>` + `<body>` snippets, or the GTM4WP plugin |

## E. Forms & reCAPTCHA
1. Elementor → Settings → Integrations → **reCAPTCHA v3**: add a Site Key and Secret Key (google.com/recaptcha/admin; you can reuse the existing v3 keys from CF7's integration page), threshold 0.5.
2. In each Form widget, add a field of type **reCAPTCHA v3** (badge position: inline, bottom of the form). There are 6 forms: home hero, 4 service pages, contact.
3. Every form already has a **Honeypot** field (hidden from humans, catches bots).
4. Check **WP Mail SMTP** is connected (Settings → Email Test), then submit each form once and confirm the email arrives and that Elementor → **Submissions** shows the entry.
5. Create **Privacy Policy** and **Terms** pages (the footer already links to `/privacy-policy/` and `/terms-of-service/`).

## F. Images to upload (WebP, under 200KB each, with descriptive filenames and alt text)
| File | Where | Size | Notes / free source |
|---|---|---|---|
| `logo.svg` (+ `logo-light.svg`) | Site Settings → Site Identity, then swap the text logo in the Header/Footer for the **Site Logo** widget | SVG, ~180×48 | White or light version for the dark background |
| `favicon.png` | Site Settings → Site Identity | 512×512 | |
| `og-image.jpg` | SEO plugin default social image | 1200×630 | Brand gradient + logo |
| `client-logo-1…5.svg` | Home → Client Logos | 240×96, transparent | Light or monochrome versions; only with client permission |
| `about-team.webp` | About → Our story | 1000×1100 | Real team photo is best; otherwise Unsplash/Pexels "creative team office" |
| `ceo-portrait.webp` | About → CEO message | 400×400 square | |
| `team-fahad / nabeel / saba / isha / muhammad.webp` | About → Team | 600×600 square | Consistent background |
| `project-1…6.webp` | Our Work | 1200×900 (4:3) | Website screenshots in a device mockup (free: Mockuuups, Shots.so, Figma Community) |
| Testimonial photos (optional) | Home/Our Work carousel | 300×300 | Only with the client's permission |

**Royalty-free sources:** Unsplash, Pexels (photos) · unDraw, Storyset, Blush (illustrations, recolour to `#0684C4` / `#7C5CFF`) · Font Awesome (already used for icons, no images needed) · Haikei.app or Mesh Gradient (extra background blobs, but the native gradients already cover this).
**Where images aren't needed:** service cards, benefits, process, values and stats all use icons and gradients, so no photo dependency.

## G. SEO (no SEO plugin is installed, so install **Rank Math** or **Yoast**)
- Paste the meta titles and descriptions from `tools/content.py` (`PAGES_META`, `SERVICE_PAGES[*].meta_title / meta_desc`, `ABOUT`).
- Every page has exactly **one H1**, with no skipped heading levels (checked automatically).
- FAQ sections output **FAQPage schema** (native accordion setting). Add Organization/LocalBusiness schema through the SEO plugin (both offices, phone, email, Instagram).
- Settings → Reading: "Discourage search engines" must be **off** after launch. Submit the sitemap in Google Search Console.
- The homepage slug is `xa-interactive-inc` (an old leftover). It's the front page, so the URL is `/` and the slug doesn't matter. Optionally rename it to `home`.

## H. Security
- Keep everything updated, and remove the unused plugins and themes (section D).
- SiteGround **Security Optimizer** (already active): enable *Disable XML-RPC*, *Lock system folders*, *Disable themes/plugins editor*, *Hide WordPress version*, **2-Factor Authentication for admins**, and *Login attempts limit*.
- `/wp-json/wp/v2/users` is already blocked (403 ✔).
- Add **HSTS** and **X-Frame-Options/SAMEORIGIN** headers (Hostinger hPanel → Security, or Security Optimizer's headers option).
- **Revoke the Application Password** used for this build (Users → Profile → Application Passwords) once the work is finished.
- External links in the build open with `rel="noopener noreferrer"`.

## I. Speed
- Elementor → Settings → Features: turn on **Inline Font Icons** (no Font Awesome CSS), **Optimized Markup** and **Optimized CSS Loading** (safe once the old pages are gone).
- Elementor → Settings → Performance: Optimized image loading **on**, Google Fonts **Swap**, load Google Fonts locally (*Load Google Fonts Locally* = on, which also helps GDPR).
- Caching: Hostinger **LiteSpeed Cache** (or hPanel Cache Manager), with page cache on and CSS/JS minify on. **Don't** combine Elementor CSS, and exclude `/wp-admin` and form pages from cache if submissions misbehave.
- Upload WebP images at the sizes above. Lazy load is on by default.
- Test with PageSpeed Insights (mobile). Aim for LCP under 2.5s and CLS under 0.1.

## J. QA before going live
- [ ] Every page on a desktop (1440), laptop (1280), tablet (768/1024) and phones (390 and 360). No horizontal scroll, menu toggle works, sticky header blurs on scroll.
- [ ] Keyboard only: Tab through the menu, buttons and forms. The focus outline is visible.
- [ ] Every form sends (section E).
- [ ] Every link works (menu, footer, cards, tel:, mailto:, WhatsApp).
- [ ] Replace the placeholders: images, Facebook/LinkedIn URLs, Our Work project names.
- [ ] Browsers: Chrome, Safari (iOS uses the `-webkit-backdrop-filter` path), Firefox, Edge.
