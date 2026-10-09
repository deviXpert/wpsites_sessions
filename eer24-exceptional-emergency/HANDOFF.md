# Exceptional Emergency Center — eer24.com

WordPress + Astra child, Elementor Pro, ElementsKit Lite, WP Rocket, Code Snippets, Yoast, HFCM, SG Security, Trustindex (wp-reviews-plugin-for-google), accessibility-widget.
Access: REST API with the app password in this site's environment (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`).
Same approach as `stat-specialty-hospital/` on branch `claude/project-thread-wzc9uu`; the snippets are the Stat ones with this site's AI-summary prompts.

## PageSpeed snippets (Code Snippets, active since 2026-10-09)

| Snippet | ID | Fixes | Cause |
|---|---|---|---|
| `snippets/1-aibtn.php` | 15 | aria-prohibited-attr | Footer AI-summary `<a>` tags (Elementor HTML widget) have no href; HFCM #28 sets it, but WP Rocket delays that script |
| `snippets/2-slack.php` | 16 | aria-required-parent | Slack markup pasted into text widgets (homepage, Beaumont) |
| `snippets/3-ekit-icons.php` | 17 | ~450 KB icon font | ElementsKit font used only for the hamburger and submenu-arrow icons |
| `snippets/4-trustindex-lazy.php` | 18 | ~500 KB review photos | Trustindex `loader.js` and Google review photos load before the widget is in view |
| `snippets/5-quphealth-delay.php` | 19 | ~7 s mobile CPU, 1.3 MB JS, 2× reCAPTCHA | HFCM #1 loads QupHealth `my-widget.js` (marked `nowprocket`, so WP Rocket never delays it) on page load |
| `snippets/6-hero-cls.php` | 22 | homepage CLS 0.33 on mobile | Hero text centred in the section's min-height and the hero image widget has no height until the image loads, so partial paints move it; top-aligned on mobile and the image height reserved (front page only) |

Test: `php snippets/test.php in.html out.html 1-aibtn 2-slack 3-ekit-icons 4-trustindex-lazy 5-quphealth-delay`.

Baseline, live, mobile Lighthouse 12 (simulated throttling): homepage perf 56, a11y 92, 4.0 MB, TBT 3.2 s; /locations/beaumont perf 62, a11y 90, 3.8 MB.
Local copy (gzip-served, base href to the live site), 2 runs each:

| Page | Before | After |
|---|---|---|
| Homepage | perf 24, a11y 92, 3,945 KiB, TBT 1.0 s | perf 68–71, a11y 100, 339 KiB, TBT 0 |
| /locations/beaumont | perf 37–39, a11y 90, 3,721 KiB | perf 87–91, a11y 97, 376 KiB |

The local homepage copy has a hero layout shift (CLS 0.25 before, 0.34 after) that the live site does not show (CLS 0.03) and that Playwright does not reproduce; check CLS on the live site after activation.
Playwright (Pixel 5, patched copy routed in place of the live URL): one tap on "Check-In Now" loads the widget and opens the location list; mobile menu and Locations submenu open the same as live; no `elementskit.woff` request.
`ElementsKit_Helper is not defined` in the console is already there on the live site.

Note: Playwright forces localhost through the proxy, so serve test copies with `page.route` on the live URL instead.

## Check-in button styling (fix before activation)
On Stat, delaying the widget turned the check-in buttons into QupHealth's default uppercase crimson (`#CC1E41`, 4px radius). The site's button rules live in Additional CSS (`#wp-custom-css`), and WP Rocket's Remove Unused CSS drops them once the widget no longer renders during its crawl.
- #19 now adds those rules (copied from Additional CSS: `#DC271D`, 12px 25px / 9px 10px on mobile, Satoshi label) from script just before `my-widget.js` loads. If Additional CSS for the button changes, update `eer_qup_css()` too.
- #19 also styles the mobile header placeholder (widget 7ab4001, plain red text until the widget renders) as the same red button from a head script, so the header looks unchanged and there is no swap shift.
- #17 hamburger SVG redrawn to match the font glyph's bar width, thickness and spacing.
Test with the rules stripped from used CSS (simulating RUCSS): without the fix the buttons render `#CC1E41` uppercase (matches the owner's Stat screenshot); with it the button styles match the live site exactly on mobile and desktop.

## Live after activation (2026-10-09)
Snippets 15–19 activated on the owner's go, then 22 for the layout shift they exposed. WP Rocket cache cleared each time with a single-use `rocket_clean_domain()` snippet (deleted after; leaves options `eer_rc_done`, `eer_rc_done2`, `eer_rc_done3`).
- #19 placeholder CSS extended: before the widget renders, every check-in spot (desktop top bar was blue, others 2–6px taller) now matches the widget's red button size, so nothing moves when it swaps in. Checked on mobile and desktop: sizes and colours equal before and after load.
- Homepage CLS: once the page got light, Chrome painted the hero before its section had fully arrived (CLS 0.33). #22 fixes it; final layout unchanged at 320–767px.
- Live Lighthouse, mobile: homepage 85–97 (CLS 0, TBT 70–140 ms, 4.0 MB → ~400 KiB), Beaumont 94–95, Beaumont abdominal-pain 93–97, Amarillo Western 94, Tyler 95. Accessibility 94–100.
- One tap on "Check-In Now" loads the widget and opens the location list; menu opens; no `elementskit.woff` request.

## Still open
- color-contrast on Beaumont: `#1275BA` on `#EBEBEB` (4.11:1) and white on `#0082C2` buttons (4.22:1). Visible colour change, needs the owner's OK.
- /locations/brownsville redirects to valleyregionalmedicalcenter.com.
