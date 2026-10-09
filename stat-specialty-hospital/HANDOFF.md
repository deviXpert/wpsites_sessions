# Stat Specialty Hospital — statspecialtyhospital.com

WordPress + Astra, Elementor Pro, ElementsKit Lite, WP Rocket (Remove Unused CSS on), Code Snippets, Yoast, HFCM, LiteSpeed server.
Access: REST API with the app password in the "Stat" environment (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`).
Same approach as `altus-emergency/` on branch `claude/project-thread-1828ay`.

## PageSpeed snippets (Code Snippets, active since 2026-10-09)

| Snippet | ID | Fixes | Cause |
|---|---|---|---|
| `snippets/1-aibtn.php` | 8 | aria-prohibited-attr | Footer AI-summary `<a>` tags have no href; HFCM #23 sets it, but WP Rocket delays that script |
| `snippets/2-slack.php` | 9 | aria-required-parent | Slack markup pasted into homepage "Our Services" text widgets |
| `snippets/3-ekit-icons.php` | 10 | ~450 KB icon font | ElementsKit font used only for the menu and submenu-arrow icons |
| `snippets/4-trustindex-lazy.php` | 11 | ~800 KB review photos | Trustindex `loader.js` and Google review photos load before the widget is in view |
| `snippets/5-quphealth-delay.php` | 12 | ~6 s mobile CPU, 1.3 MB JS, 2× reCAPTCHA | HFCM #2 loads QupHealth `my-widget.js` (uncompressed on their server) on page load; now waits for first scroll/tap, and a tap on "Check-In Now" before it is ready opens the widget once it renders |

Test: `php snippets/test.php in.html out.html 1-aibtn 2-slack 3-ekit-icons 4-trustindex-lazy 5-quphealth-delay`.
Local Lighthouse (mobile, gzip-served copy, base href to the live site):

| Page | Before | After |
|---|---|---|
| Homepage (3 runs) | perf 33–35, a11y 89, 3,848 KiB, TBT 1.2–1.5 s | perf 78–87, a11y 97, 376 KiB, TBT 0–180 ms |
| /locations/laredo-south | perf 36, a11y 90 | perf 83, a11y 94 |
| /services/laredo/inpatient | perf 27, a11y 93 | perf 83, a11y 96 |

Playwright (Pixel 5): one tap on "Check-In Now" loads the widget and opens the location picker.
`ElementsKit_Helper is not defined` in the console was already there before these snippets.

## Live after activation (2026-10-09)
Snippets 8–12 activated on the owner's go; WP Rocket cache cleared with a single-use `rocket_clean_domain()` snippet (deleted after, two DELETEs).
- Fix in #12: WP Rocket's delay-JS swallows the first click before its scripts load, so a "Check-In Now" tap is now caught on `pointerup` (no drag), and the widget's button is clicked once it renders. Playwright: one tap opens the picker on the homepage and Laredo South.
- Local Lighthouse on the live site, mobile (same setup that scored the old homepage 42 while PSI said 73): homepage 85–94 (TBT 3.2 s → 30–180 ms, 3.9 MB → 440 KiB), Laredo South 91, Laredo inpatient 92. Accessibility 94–97.
- Menu opens and no `elementskit.woff` request on the live homepage.

## Still open
- color-contrast: brand blue `#0082C2` on white is 4.22:1 (needs 4.5; `#007BB8` gives 4.64), green `#39B54A` service headings are 2.66:1 (need 3:1 for large bold; `#2E9A3D` gives 3.62). Visible colour change, needs the owner's OK.
- link-in-text-block on /locations/laredo-south.
- /services/laredo/inpatient has CLS ~0.15.
