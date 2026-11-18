# EVTRON dark design system (Direction A: "Spec Sheet")

Chosen 18 November 2026. Reference prototype: https://claude.ai/artifact/6L1r4JwgViDfoEK84ScWzg (`prototypes/a-spec-sheet.html`).
**Dark only.** No light theme, no toggle, and the system light-mode setting is ignored.

## 1. Principles
1. **Numbers are the design.** Prices, specs and measurements are set in IBM Plex Mono, so they read like a datasheet.
2. **Flat, layered dark.** Elevation comes from lighter surfaces and hairline borders, never heavy shadows.
3. **One accent, rarely.** Charge-green only for the primary action, "included/yes" states, focus and selection.
4. **Show, don't decorate.** No glows, bolts, gradients on brand marks, neon or grid-line backgrounds.
5. **Honest UI.** Unavailable options are visible but disabled, with a reason. Unconfirmed details never appear as facts.

## 2. Tokens (CSS custom properties)
Lives in **Elementor → Custom Code → "EVTRON tokens"** (`<head>`, all pages, priority 1), and mirrored in Elementor Global Colours and Fonts (section 9). The source file is `design/tokens.css`.

```css
:root{
  color-scheme: dark;
  /* Surfaces: elevation by lightness */
  --ev-ink:#0B0F14;      /* page background (level 0) */
  --ev-s1:#11161D;       /* panels, cards (level 1) */
  --ev-s2:#171E27;       /* raised within panels, table heads (level 2) */
  --ev-s3:#1F2833;       /* selected / pressed fills (level 3) */
  /* Lines */
  --ev-divider:#2A3441;  /* decorative hairlines only (not for controls) */
  --ev-control:#6A7688;  /* borders of inputs, ghost buttons, chips, swatches: ≥3:1 on every surface */
  /* Text */
  --ev-text:#F2EFE9;     /* headings, key figures (warm white) */
  --ev-body:#C3C7CD;     /* running text */
  --ev-muted:#939CA8;    /* labels, captions, secondary */
  /* Accent and states */
  --ev-accent:#3BE37F;   /* charge-green (logo) */
  --ev-accent-hover:#5CEB97;
  --ev-accent-ink:#06210F;     /* text on accent */
  --ev-accent-tint:rgba(59,227,127,.08); /* highlighted rows, selected tiles */
  --ev-warn:#F2C14E;     /* "may cost extra", TBC notes, placeholders (internal) */
  --ev-error:#FF8A80;    /* form errors */
  --ev-success:#3BE37F;  /* same as accent */
  /* Type */
  --ev-font:"Manrope",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --ev-mono:"IBM Plex Mono",ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;
  /* Radius */
  --ev-r-sm:6px;   /* buttons, inputs */
  --ev-r-md:10px;  /* panels, cards, tables */
  --ev-r-pill:999px; /* chips */
  /* Spacing (4px base) */
  --ev-1:4px;--ev-2:8px;--ev-3:12px;--ev-4:16px;--ev-5:24px;--ev-6:32px;--ev-7:48px;--ev-8:72px;--ev-9:96px;
  /* Layout */
  --ev-max:1440px; --ev-gutter:max(16px,env(safe-area-inset-left,0px));
  /* Motion */
  --ev-fast:150ms; --ev-ease:cubic-bezier(.2,.7,.2,1);
}
html,body{background:var(--ev-ink);color:var(--ev-body)}
```

**No white flash:** the same `background:#0B0F14` and `color-scheme:dark` are also set inline in the critical `<head>` (Custom Code, priority 1), with `<meta name="color-scheme" content="dark">` and `<meta name="theme-color" content="#0B0F14">`. Astra's own body background is set to `#0B0F14` in the Customizer so the theme never paints white first.

## 3. Surfaces and elevation
| Level | Token | Used for | Border |
|---|---|---|---|
| 0 | `--ev-ink` | Page, header (92% opacity + blur), footer | — |
| 1 | `--ev-s1` | Cards, receipt panel, calculator, form panels | 1px `--ev-divider` |
| 2 | `--ev-s2` | Table header, inputs, inner wells, mobile menu | 1px `--ev-divider` (controls: `--ev-control`) |
| 3 | `--ev-s3` | Pressed or selected segment, hover on rows | — |

No `box-shadow` on cards. The only shadow allowed is a 1px inner highlight on the sticky header when scrolled (optional).

## 4. Typography
Self-hosted (Phase 5). **Manrope** 300, 400, 600 (Latin subset, WOFF2, variable if available). **IBM Plex Mono** 400, 500. `font-display: swap`, with the two critical files preloaded (Manrope 600 and 400). That's 4 to 5 files in total.

| Role | Font / weight | Size (fluid) | Line height | Tracking | Notes |
|---|---|---|---|---|---|
| Display (home H1) | Manrope 600 + 300 second line | `clamp(40px,7vw,76px)` | 1.02 | −0.035em | Only on Home |
| H1 (pages) | Manrope 600 | `clamp(34px,5vw,56px)` | 1.06 | −0.03em | |
| H2 | Manrope 600 | `clamp(28px,4vw,44px)` | 1.08 | −0.025em | |
| H3 | Manrope 600 | `clamp(19px,2vw,22px)` | 1.25 | −0.01em | |
| Lead | Manrope 400 | `clamp(17px,2vw,19px)` | 1.6 | 0 | max 56ch |
| Body | Manrope 400 | 16px (17px ≥1000px) | 1.6 | 0 | max 68ch |
| Small | Manrope 400 | 14px | 1.5 | 0 | |
| Label / eyebrow | Plex Mono 500 | 12px | 1.3 | 0.08em, UPPERCASE | `--ev-muted` |
| Price (large) | Plex Mono 500 | `clamp(30px,4vw,40px)` | 1 | 0 | tabular-nums |
| Price (card) | Plex Mono 500 | 22px | 1.1 | 0 | |
| Spec value | Plex Mono 400/500 | 14.5px | 1.4 | 0 | |

Headings use `text-wrap: balance`. Numbers use `font-variant-numeric: tabular-nums`.

## 5. Spacing and layout
- 4px base scale (`--ev-1` to `--ev-9`). Gaps via flex/grid `gap`.
- Container max **1440px** (user decision). Side gutter **16px** (<768px) and **32px** (≥768px), safe-area aware.
- Section padding: **72px** block (56px <768px), with a 1px `--ev-divider` top border between sections.
- Breakpoints: 600 (small), 768 (tablet), 1000 (desktop nav), 1440 (wide). Content stays at 1440 on ultrawide; backgrounds run full width.
- Mobile first. No horizontal scrolling except inside tables (`overflow-x:auto` wrapper with a visible focus ring).
- Touch targets **≥44×44px** (swatches 32px visual with a 44px hit area via padding).

## 6. Components and states
Every interactive component defines: default · hover · focus-visible · active · selected · disabled · error/success where relevant.

| Component | Default | Hover | Focus | Selected | Disabled |
|---|---|---|---|---|---|
| **Primary button** | bg accent, text accent-ink, 48px high, radius 6 | bg accent-hover | 2px accent outline, 3px offset | — | 45% opacity, `not-allowed`, no hover |
| **Ghost button** | transparent, 1px `--ev-control`, text `--ev-text` | bg `--ev-s2` | as above | — | as above |
| **Segment (charger picker)** | 1px control border | bg s2 | outline | bg s3, border accent, `aria-pressed=true` | — |
| **Chip (cable length)** | pill, 1px control border, mono 13px | border text | outline | border accent, text warm-white, `aria-checked` | 45% + line-through + tooltip reason (e.g. "5m not currently available") |
| **Colour swatch** | 32px circle, 2px control border, 44px hit area | — | outline | 2px accent ring, 3px offset; name shown below | n/a |
| **Card (product)** | s1, 1px divider, radius 10 | border control | outline on link | — | — |
| **Receipt line** | dashed divider | — | — | "Included" in accent | — |
| **Datasheet table** | s1 head, divider rows, mono values | row bg s3 | — | highlighted rows accent-tint | — |
| **Input / select / textarea** | bg s2, 1px control border, 48px, text warm-white, placeholder muted | border text | 2px accent outline | — | 45% |
| **Input error** | border `--ev-error` + message below with icon, `aria-invalid`, `aria-describedby` | | | | |
| **Input success** | border accent + ✓ icon (only after validation) | | | | |
| **Checkbox / radio** | `accent-color: var(--ev-accent)`, 20px, label clickable | | outline | | |
| **Range slider** | `accent-color` accent, 32px track hit area | | outline | | |
| **Alert / notice** | s1 panel, 3px left rule in state colour (warn, error, success), icon + text | | | | |
| **Accordion (FAQ)** | divider rows, `+`/`−` in mono accent | text warm-white | outline | open | |

**Autofill:** `input:-webkit-autofill{ -webkit-text-fill-color:#F2EFE9; box-shadow:0 0 0 1000px #171E27 inset; caret-color:#F2EFE9 }` so Chrome and Safari autofill stays dark.
**Scrollbars:** handled by `color-scheme: dark`, plus `scrollbar-color:#3A4655 #0B0F14` on Firefox.
**WooCommerce:** basket, checkout, notices, Stripe/PayPal elements and the mini-cart are styled to these tokens. Stripe Payment Element uses the `night` theme with variables (`colorBackground:#171E27`, `colorText:#F2EFE9`, `colorPrimary:#3BE37F`, `borderRadius:6px`). The PayPal buttons use the `black` colour option.

## 7. Iconography and imagery
- **Icons:** 24px line icons, **1.8px stroke, round caps and joins** (to echo the logo's rounded strokes), in `--ev-text` or `--ev-muted`. Accent only for state (✓). Inline SVG, no icon fonts.
- **Product photography:** cut-outs on transparent or `#11161D` backgrounds. Graded slightly darker and warmer; no white boxes. Consistent 4:3 tiles, product at 60 to 70% of the tile height, soft floor shadow allowed *inside the image*.
- **Lifestyle photography (later):** dusk or evening exteriors and warm practical light. Darken the top 30% for text overlays.
- **Placeholders:** clearly labelled `PLACEHOLDER IMAGE` in amber mono until the client's photos arrive (task #1).
- **Logos:** header and footer `evtron-horizontal-dark.svg`; over photos `evtron-horizontal-white.svg`. Minimum width 100px, clear space = "o" height.
- **Share images (OG):** 1200×630, `--ev-ink` background, warm-white headline in Manrope 600, the green mark, and a price in mono where relevant.
- **Favicons and app icon:** from the logo pack (dark).

## 8. Motion
- Only `opacity` and `transform`. 150ms `--ev-ease` for state changes. Numbers update instantly (no count-up animation).
- No scroll-jacking, parallax or autoplay. Optional 8px fade-up on section entry, **from a visible resting state** (content never starts hidden).
- `@media (prefers-reduced-motion: reduce)`: all transitions off.
- No layout shift: images and media have explicit `width`/`height` or `aspect-ratio`.

## 9. Elementor mapping
**Site Settings → Global Colours**
| Elementor slot | Token |
|---|---|
| Primary | Accent `#3BE37F` |
| Secondary | Surface 1 `#11161D` |
| Text | Body `#C3C7CD` |
| Accent | Warm white `#F2EFE9` |
| Custom: Ink | `#0B0F14` |
| Custom: Surface 2 | `#171E27` |
| Custom: Surface 3 | `#1F2833` |
| Custom: Muted | `#939CA8` |
| Custom: Divider | `#2A3441` |
| Custom: Control border | `#6A7688` |
| Custom: Accent ink | `#06210F` |
| Custom: Warning | `#F2C14E` |
| Custom: Error | `#FF8A80` |

**Global Fonts:** Primary = Manrope 600 (headings) · Secondary = Manrope 300 (display second line) · Text = Manrope 400 · Accent = IBM Plex Mono 500 (prices, labels).
**Site Settings:** Theme Style → Typography (H1 to H6 per section 4), Buttons (primary style), Form Fields (input style above), Images (radius 10). Layout → content width 1440, widgets gap 24. Breakpoints: mobile 767, tablet 999 (match 768/1000).
**Custom Code (global):** (1) critical head (meta, background, `color-scheme`, font preloads) · (2) tokens and component CSS that Elementor controls can't express (focus rings, autofill, forced-colors, print, tabular numbers) · (3) small interaction scripts (receipt, highlight, calculator, finder, checker), each loaded `defer` and only on pages that use them.

## 10. Forced colours, high contrast and print
```css
@media (forced-colors: active){
  .ev-btn,.ev-chip,.ev-swatch,.ev-card,input,select,textarea{border:1px solid CanvasText}
  .ev-btn-primary{background:ButtonText;color:ButtonFace}
  :focus-visible{outline:2px solid Highlight}
  .ev-swatch{forced-color-adjust:none} /* keep the real finish colour visible */
}
@media print{
  :root{color-scheme:light}
  html,body{background:#fff!important;color:#111!important}
  header nav,footer,.ev-btn,.ev-calc,.ev-receipt .ev-btn{display:none!important}
  a[href^="http"]::after{content:" (" attr(href) ")";font-size:.85em}
  .ev-accent-text{color:#0B7A3B!important} /* deep-green, 5.4:1 on white */
}
```
Print is light and ink-friendly for product, installation, warranty and legal pages.

## 11. Contrast (WCAG 2.2 AA), all combinations in use
Ratios against each surface. Body text needs ≥4.5, large text (≥24px, or 18.66px bold) ≥3, UI component boundaries and focus ≥3.

| Foreground | ink #0B0F14 | s1 #11161D | s2 #171E27 | s3 #1F2833 | Use | Result |
|---|---|---|---|---|---|---|
| Warm white #F2EFE9 | 16.75 | 15.82 | 14.62 | 12.98 | headings, figures | ✅ AAA |
| Body #C3C7CD | 11.32 | 10.70 | 9.89 | 8.78 | running text | ✅ AAA |
| Muted #939CA8 | 6.92 | 6.54 | 6.04 | 5.36 | labels, captions | ✅ AA |
| Accent #3BE37F | 11.42 | 10.79 | 9.97 | 8.85 | "included", icons, focus | ✅ |
| Warning #F2C14E | 11.45 | 10.82 | 10.00 | 8.88 | notices | ✅ |
| Error #FF8A80 | 8.42 | 7.96 | 7.35 | 6.53 | form errors | ✅ |
| **Control border #6A7688** | 4.17 | 3.94 | 3.64 | 3.23 | input, chip, ghost button, swatch outlines | ✅ ≥3:1 |
| Divider #2A3441 | 1.52 | 1.44 | 1.33 | — | decorative only | n/a (not a control) |

| Pair | Ratio | Result |
|---|---|---|
| Accent-ink #06210F on accent #3BE37F (primary button) | 10.13 | ✅ |
| Accent-ink on hover #5CEB97 | 11.19 | ✅ |
| Focus ring accent on ink / s1 | 11.42 / 10.79 | ✅ |
| Print: deep-green #0B7A3B on white | 5.44 | ✅ |

The prototype used `#3A4655` for control borders (2.0:1, fails). **The build uses `#6A7688`.**

## 12. Do / don't
- ✅ Prices in mono, with "fully installed" next to them.
- ✅ Disabled options with a reason. TBC details stay out of customer-facing pages.
- ❌ Pure black (#000) or pure white (#fff) text on pure black.
- ❌ Green as large background fills, green headings, or more than one green button per view.
- ❌ Drop shadows, glows, gradients, lightning-bolt icons.
- ❌ Third-party embeds that can't be made dark (e.g. a default Google Maps embed). Use a static dark map image or skip it.
