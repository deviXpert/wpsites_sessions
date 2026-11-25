# 1 · Design Spec – Graphics Storm Studio (Glassmorphism, Dark Navy)

**Status:** applied to the live kit (Elementor → Site Settings) on 2026-11-25. The source of truth is `tools/kit.py`, and an export is in `templates/site-settings.json`.

## Why dark navy
Frosted glass only reads as glass when there is rich colour behind it. On a dark navy base, the blue/violet gradient glows show through translucent panels, white text stays far above WCAG AA, and the brand blue `#0684C4` looks premium instead of corporate. A light theme would need much stronger panel opacity to keep contrast, and most of the glass effect would be lost.

## Colours → Site Settings › Global Colors
| Global (ID) | Name | Hex | Use |
|---|---|---|---|
| System `primary` | Brand Blue | `#0684C4` | Brand accents, hover backgrounds in menus |
| System `secondary` | Accent Violet (CTA) | `#7C5CFF` | Primary buttons and CTAs only (white text: 4.6:1 ✔ AA) |
| System `text` | Body Text | `#C9D3E8` | Paragraphs (12.6:1 on navy ✔) |
| System `accent` | Light Blue | `#5DB0D8` | Eyebrows, icons, links, active menu (7.9:1 ✔) |
| `gsnavy` | Navy – Page Background | `#070B1F` | Body background |
| `gsnavy2` | Navy – Raised Surface | `#0E1738` | Dropdowns, opaque fallback |
| `gswhite` | White – Headings | `#FFFFFF` | All headings |
| `gsmuted` | Muted Text | `#93A1BF` | Captions, copyright (7.0:1 ✔) |
| `gsvioletdk` | Violet – Hover | `#6545F0` | Button hover |
| `gsglass` | Glass Fill 6% | `#FFFFFF0F` | Standard glass cards |
| `gsglass2` | Glass Fill Strong 10% | `#FFFFFF1A` | Forms, hero panels, ghost buttons |
| `gsline` | Glass Border 14% | `#FFFFFF24` | 1px card borders, dividers |
| `gsvioletglow` / `gsblueglow` | Blob glows | `#7C5CFF59` / `#0684C44D` | Background gradients |
| `gstransparent` | Transparent | `#070B1F00` | Header at top of page |
| Legacy – … | old colours | – | Kept only so old pages don't break. Delete after launch |

## Fonts → Site Settings › Global Fonts
**Sora** (geometric, for headings and buttons) paired with **Inter** (for body, nav and forms). Both come from Google Fonts, and only the weights used are loaded: Sora 600/700 and Inter 400/500/600.

| Global (ID) | Font / weight | Desktop / Tablet / Mobile | Line height | Letter spacing |
|---|---|---|---|---|
| `gsh1` H1 – Hero | Sora 700 | 64 / 48 / 38 px | 1.08 | −1.5px |
| `gsh2` H2 – Section | Sora 700 | 46 / 38 / 30 | 1.15 | −1px |
| `gsh3` H3 – Card | Sora 600 | 24 / 22 / 20 | 1.3 | −0.3px |
| `gsh4` H4 – Small title | Sora 600 | 19 / 18 / 18 | 1.4 | – |
| `gseyebrow` Eyebrow | Inter 600, UPPERCASE | 13 | 1.5 | 2px |
| `gslead` Lead paragraph | Inter 400 | 19 / 18 / 17 | 1.65 | – |
| `gsbody` Body | Inter 400 | 17 / 16 / 16 | 1.7 | – |
| `gssmall` Small | Inter 400 | 14 | 1.6 | – |
| `gsbtn` Button | Sora 600 | 16 | 1.2 | – |
| `gsnav` Navigation | Inter 500 | 15 | 1.4 | – |
| `gsstat` Stat number | Sora 700 | 52 / 44 / 38 | 1 | −1px |

Site Settings › Typography also sets Body (Inter 17px, `#C9D3E8`), Links (`#5DB0D8` → hover white) and H1–H6 (Sora, white, same sizes as above), so plain headings look right too.

## Spacing scale (8-pt)
`8 · 16 · 24 · 32 · 48 · 64 · 96 · 112`
- **Section padding (top/bottom):** 112 desktop / 88 tablet / 64 mobile (hero: 96 / 72 / 48)
- **Gaps:** 48 between a section title and its content; 24 between cards; 20 inside columns; 14 between buttons
- **Layout (Site Settings › Layout):** content width **1240px**, container padding **0 24px** (mobile 0 16px), widget space 20px
- **Breakpoints:** mobile ≤ 767, tablet ≤ 1024 (Elementor defaults kept)

## Radius & shadow
| Token | Value |
|---|---|
| Card radius | 20px (hero/form panels 24, CTA band 28, inputs 12, images 14–18) |
| Buttons | 999px (pill) |
| Card shadow | `0 20px 50px rgba(2,6,23,.45)` |
| Card hover shadow | `0 28px 60px rgba(6,132,196,.28)` plus border → Light Blue, translateY −6px, 300ms |
| Button glow | `0 12px 30px rgba(124,92,255,.35)` |

## Glass recipe
| Layer | Where it's set | Value |
|---|---|---|
| Fill | Container › Style › Background (Classic) | Global `gsglass` (6%) or `gsglass2` (10%) |
| Border | Container › Style › Border | Solid 1px, global `gsline` |
| Radius | Container › Style › Border radius | 20px |
| Shadow | Container › Style › Box shadow | `0 20 50 0 rgba(2,6,23,.45)` |
| Padding | Container › Layout › Padding | 32 / 28 / 24 |
| Blur | **Advanced › CSS Classes** | `gs-glass` (16px) or `gs-glass--strong` (26px) |
| Hover lift | Advanced › Transform › Hover › Offset Y −6, plus Border/Box-shadow hover | native |

**Background blobs** are native too. On each section: Style › Background › Gradient **Radial** (violet 30% → navy at 55%) plus Background Overlay › Gradient **Radial** (blue 28% → transparent). Three variants rotate (a/b/c) so neighbouring sections never look the same. `.gs-blob` is also available if you want an extra free-floating shape.

## Buttons (Site Settings › Buttons)
| Style | How |
|---|---|
| **Primary** (violet pill) | Comes from Site Settings: Sora 600 16px, white on `#7C5CFF`, hover `#6545F0`, radius 999, padding 16/30, violet glow. Just drop in a Button widget |
| **Ghost** (glass pill) | Button › Style: background `gsglass2`, border 1px `gsline`, text white; hover background white, text navy; shadow transparent; CSS class `gs-glass` |
| **Text link** | Background transparent, padding 0, text Light Blue, plus an arrow icon |

Every button uses Hover Animation **Float** and an icon on the right (arrow, phone, WhatsApp or paper plane).

## Form fields (Site Settings › Form Fields)
Inter 16px, white text, fill `rgba(255,255,255,.06)`, 1px border `rgba(255,255,255,.18)`, radius 12, padding 14/16. On focus: fill 10%, border Light Blue. Labels are Inter 500 14px `#DCE4F5`. Add the `gs-form` class to the Form widget to get readable placeholders.

## Motion
- **Entrance:** only hero copy uses Fade In Up (fast). Nothing else animates on scroll, which keeps the page light and avoids layout shift.
- **Hover:** float on buttons, lift on cards.
- **Reduced motion:** visitors with "reduce motion" switched on get no animation (handled in the global CSS).
