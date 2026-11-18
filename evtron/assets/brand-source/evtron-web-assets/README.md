# EVTRON web assets

Logo: "Crossover" mark + rounded lowercase wordmark. Dark-first brand.

## Install
Copy everything in this folder to the site's `public/` directory (keep `logo/` as a subfolder).

## <head> tags
```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/favicon-16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0B0F14">
<meta property="og:image" content="/social-avatar-800.png">
```

## Which logo where
- Header on dark: `/logo/evtron-horizontal-dark.svg` (green mark, warm-white name)
- Header on light: `/logo/evtron-horizontal-light.svg`
- Over photos: `/logo/evtron-horizontal-white.svg`
- Print / single colour: `/logo/evtron-horizontal-black.svg`
- Square spaces: `/logo/evtron-stacked-*.svg`; symbol only: `/logo/evtron-icon-*.svg`; round badge: `/logo/evtron-badge-dark.svg`
- Always use `<img>` with width/height set, preserving aspect ratio. Horizontal viewBox is 360×76.
- Alt text: "EVTRON"

## Rules
- Min width: horizontal 100px, stacked 56px, symbol 24px.
- Clear space on all sides = height of the "o".
- No glows, shadows, gradients, recolouring, rotation, or retyping the name. No hyphen.

## Colours
| Token | Hex | Use |
|---|---|---|
| ink | #0B0F14 | base background |
| charge-green | #3BE37F | mark, primary buttons (on dark) |
| deep-green | #0B7A3B | accent on light (5.5:1 on white) |
| warm-white | #F2EFE9 | text on dark |
| slate | #8D96A3 | secondary text |
| paper | #F5F6F1 | light background |

## Fonts (Google Fonts, free)
- Manrope 300/400/500/600: headings and body
- IBM Plex Mono 400: specs, labels, tariffs only
