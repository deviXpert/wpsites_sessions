# nec24.com – Accessibility / Agentic fixes (2026-10-09)

Backups of `_elementor_data` before changes are in `backup/` (pages-13 = Home, elementor_library-1208 = Footer).

Changes:
- Home (13), text-editor widgets `ac703f5` and `341f5fc`: removed Slack markup pasted from a Slack message (role="listitem" etc.), replaced with plain `<p>`; location links underlined (link-in-text-block).
- Home (13): 4 text/description colours `#7C7C7C` -> `#666666` (contrast 4.17 -> 5.7:1).
- Footer (1208), HTML widget `03b81a3` (AI summary buttons): added static `href` to each `a.ai-btn` (JS still rewrites them with the prompt URL). Fixes aria-prohibited-attr + crawlable-anchors.
- Cleared Elementor CSS cache (DELETE /wp-json/elementor/v1/cache).

Result (Lighthouse mobile, local): Accessibility 87 -> 100, SEO 92 -> 100.
Open item: console error `ElementsKit_Helper is not defined` (WP Rocket delay JS exclusions).
