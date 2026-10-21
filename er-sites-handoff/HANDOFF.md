# Handoff: PageSpeed, accessibility and WP Rocket fixes for the ER sites

Paste this whole file into a new Claude session. It is everything we learned fixing mobile PageSpeed and accessibility on four emergency-room WordPress sites in October 2026. The new session should use it to apply the same fixes to another site (or finish the open items on these ones).

---

## 0. Instructions for the new session (read first)

You are fixing mobile PageSpeed performance and accessibility on an Elementor + WP Rocket WordPress site. Work like this, every time:

1. **Never change the live site without the owner's explicit go-ahead.** Save every fix as a Code Snippets snippet that is **switched off**, test it, report before/after numbers, then ask. Activating a snippet, clearing cache, and changing colours all need a "go".
2. **Prefer small Code Snippets PHP fixes that rewrite the HTML output** over editing theme files, plugin files, WP Rocket settings or page content. They don't touch the database content, and switching the snippet off undoes them instantly.
3. **Every snippet must be site-specific where it carries styling or text.** Copy the site's own colours, sizes and AI-summary prompts. Never paste one site's snippet onto another site unchanged (see the red-button incident in section 5).
4. **Test on a local copy first** (section 6), then activate, clear the WP Rocket cache, and re-test the live site, including clicking the things the snippet touches (menu, check-in button, reviews).
5. Access is through the WordPress REST API with an application password stored in the cloud environment as `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`. Each site has its own environment; a session can only reach the site of the environment it was started in. Never ask the owner to paste a password into chat.

---

## 1. The sites

| Site | Domain | Stack | Snippets (Code Snippets IDs) | Status |
|---|---|---|---|---|
| Altus Emergency Centers | altusemergency.com | Astra, Elementor Pro, ElementsKit, WP Rocket, Code Snippets, Yoast, SG Security, HFCM, Trustindex | 9 video, 10 AI links, 11 Slack, 14 icon font, 15 Trustindex | All live since 2026-10-09 |
| STAT Specialty Hospital | statspecialtyhospital.com | Astra, Elementor Pro, ElementsKit Lite, WP Rocket (Remove Unused CSS on), Code Snippets, Yoast, HFCM, LiteSpeed server, AccessiYes, Maddex Shield & Speed, CF7 | 8 AI links, 9 Slack, 10 icon font, 11 Trustindex, 12 QupHealth | All live; snippet 12 needs the blue-button version confirmed (open item) |
| Exceptional Emergency Center | eer24.com | Astra child, Elementor Pro, ElementsKit Lite, WP Rocket, Code Snippets, Yoast, HFCM, SG Security, Trustindex, accessibility-widget | 15 AI links, 16 Slack, 17 icon font, 18 Trustindex, 19 QupHealth, 22 hero CLS | All live since 2026-10-09 |
| nec24.com (separate earlier session) | nec24.com | Elementor | none (edited Elementor data directly) | Done, accessibility 87 → 100 |

Code and notes per site are in GitHub repo `deviXpert/wpsites_sessions`:
- Altus: branch `claude/project-thread-1828ay`, folder `altus-emergency/`
- Stat: branch `claude/project-thread-wzc9uu`, folder `stat-specialty-hospital/`
- eer24: branch `claude/project-thread-s781ls`, folder `eer24-exceptional-emergency/` (newest, most refined versions)
- nec24: branch `claude/modest-feynman-6n9gur`, folder `nec24/` (with `_elementor_data` backups)

### Results

| Page | Before (mobile perf) | After (mobile perf) | Accessibility |
|---|---|---|---|
| Altus homepage | 60–78 live (local copy median 74), 1.5 MB | 86–93 live, 401 KB | 92 → 100 |
| Altus Lake Jackson pediatric | | | → 100 |
| Altus Lumberton / Waxahachie / Lake Jackson | | Lumberton still slow (24 in one run) | 86 → 95–96 |
| Stat homepage | 42 (own Lighthouse; PSI said 73), 3.9 MB, TBT 3.2 s | 85–94, 440 KB, TBT 30–180 ms | 89 → 94–97 |
| Stat Laredo South / Laredo inpatient | 56 / 63 | 91 / 92 | |
| eer24 homepage | 56, 4.0 MB, TBT 3.2 s | 85–97, ~400 KB, CLS 0 | 92 → 100 |
| eer24 Beaumont | 62 | 94–95 | 90 → 97 |
| eer24 abdominal-pain, Amarillo Western, Tyler | | 93–97, 94, 95 | |

Our own Lighthouse runs (mobile, simulated throttling, CPU x6) are stricter than Google PageSpeed Insights; the same old Stat homepage got 42 from us and 73 from PSI. Scores swing a few points run to run, so run 3–4 times and report the range.

---

## 2. Problems found, root causes and fixes (summary)

| # | Problem (Lighthouse audit) | Root cause | Fix | Snippet |
|---|---|---|---|---|
| A1 | `aria-allowed-role` on background video | Elementor prints `role="presentation"` on hosted background `<video>` | Strip the role, add `aria-hidden="true"` | 3.1 |
| A2 | `aria-prohibited-attr` (and `crawlable-anchors`) on footer "Open Gemini / ChatGPT / Claude / Grok / Perplexity" AI-summary buttons | The `<a data-ai-provider>` tags have no `href`; an HFCM script fills the href in, but WP Rocket **Delay JS** holds that script until user interaction, so Lighthouse sees `<a>` without href + aria-label | Write the same href server-side, using the exact prompts from that site's HFCM "ai summary" script | 3.2 |
| A3 | `aria-required-parent` / `aria-required-children`, duplicate ids | Text copied from Slack was pasted into Elementor text widgets with Slack's wrapper markup (`role="listitem"`, `role="document"`, `tabindex`, `data-qa`, ids) | Strip those attributes from Slack-classed tags on output (or, as on nec24, replace the widget content with plain `<p>`) | 3.3 |
| A4 | `color-contrast` | Brand colours slightly too light | **Not applied** (visible design change, needs owner OK). Suggested values in section 7 | — |
| A5 | `aria-allowed-attr` on Elementor popup | Popup 36373 on Altus renders `role="document"` with `aria-modal` | **Open** | — |
| P1 | ~450 KB `elementskit.woff` icon font downloaded | ElementsKit loads its whole icon font just for 2–3 icons (hamburger, submenu arrow, arrow-circle) | Replace those `<i class="icon icon-…">` glyphs with inline SVGs, keep the `<i>` wrapper and ekit classes | 3.4 |
| P2 | ~500–800 KB of review photos + Trustindex JS/CSS/fonts loaded up front | Trustindex `cdn.trustindex.io/loader.js` loads on page load (far below the fold) and its review images carry `class="skip-lazy"`, so WP Rocket's lazyload ignores them | Load `loader.js` on first scroll/tap/key/mouse move; make its own fallback injector wait too; add `loading="lazy"` to the review images from an output buffer | 3.5 |
| P3 | 6–7 s mobile CPU, 1.3 MB JS (served uncompressed), 2× reCAPTCHA, TBT up to 3.2 s | QupHealth check-in widget `checkin.quphealth.com/static/js/my-widget.js` loaded by an HFCM snippet on page load. On eer24 the HFCM tag was marked `nowprocket`, so WP Rocket never delayed it | Replace the script tag with a small loader that injects it on first interaction; remember a tap on "Check-In Now" (on `pointerup`) and click the widget's own button once it renders; re-inject the site's button CSS right before load | 3.6 / 3.7 |
| P4 | Check-in buttons turned QupHealth's default uppercase crimson (#CC1E41) after P3 | WP Rocket **Remove Unused CSS** crawls the page; with the widget delayed, the widget's button isn't in the DOM during the crawl, so the site's custom button rules (Additional CSS / page CSS) are dropped from the used CSS | Add the site's button rules back from JS just before `my-widget.js` loads (RUCSS never sees JS-inserted styles) | inside 3.6 / 3.7 |
| P5 | Before the widget loads, placeholders looked different (plain red text in mobile header, blue/taller buttons on desktop top bar) and jumped when the widget swapped in | Elementor placeholder elements inside `.widget-root` are styled differently from the widget's button | Style the placeholders like the widget button from a head script | inside 3.6 |
| P6 | Homepage CLS 0.33 on mobile (eer24), exposed once the page became light | Chrome painted the hero before the section arrived; hero text centred in a 500px min-height and image widget had no height until load | Top-align hero on mobile and reserve the image height, from a head script | 3.8 |
| P7 | Lighthouse "large CSS" (~345 KB page CSS on Stat) | Elementor/Astra CSS built into every page | Not done; next lever if a site is stuck under 90 | — |

---

## 3. The code (verbatim, as running live)

All are Code Snippets snippets, type **PHP**, scope **Run everywhere** (front end). Save them **inactive** first. Rename function prefixes (`eer_`, `stat_`, `altus_`) per site so two sites' code never clashes if pasted together.

Hooks used and why:
- `elementor/frontend/the_content` filter: rewrites everything Elementor renders, including Theme Builder header and footer. Used for A1–A3, P1, Trustindex fallback.
- `template_redirect` at priority 0 with `ob_start()`: rewrites the **whole final HTML** (needed when the markup comes from HFCM or is filled in after Elementor renders, e.g. Trustindex images, the QupHealth script tag). Skip admin, AJAX, feeds and REST.
- `script_loader_tag`: swaps an enqueued script tag (Trustindex `loader.js`).
- Inline scripts we add carry `nowprocket data-nowprocket` so WP Rocket's Delay JS leaves them alone.
- Any CSS we need is inserted **by JavaScript** (`document.createElement("style")`), never as a `<style>` block, because WP Rocket's Remove Unused CSS strips inline `<style>` blocks and drops rules it didn't see used.

### 3.1 Background video role (Altus snippet 9)

```php
/**
 * A11y: Elementor background videos are output with role="presentation",
 * which is not allowed on <video>. Swap it for aria-hidden="true".
 */
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( false === strpos( $content, 'elementor-background-video-hosted' ) ) {
		return $content;
	}
	return preg_replace_callback(
		'/<video\b[^>]*\belementor-background-video-hosted\b[^>]*>/i',
		function ( $m ) {
			$tag = preg_replace( '/\s+role=(["\'])presentation\1/i', '', $m[0] );
			if ( false === stripos( $tag, 'aria-hidden' ) ) {
				$tag = preg_replace( '/^<video\b/i', '<video aria-hidden="true"', $tag );
			}
			return $tag;
		},
		$content
	);
}, 20 );
```

### 3.2 AI-summary links get a server-side href (eer24 snippet 15; Altus 10, Stat 8)

Copy `$default` and `$perplexity` **exactly** from the site's HFCM "ai summary" script, so the links match what the script would set. eer24 version:

```php
/**
 * A11y: the footer "AI summary" links are <a> tags with no href until a
 * delayed script fills it in, so Lighthouse sees them as generic elements
 * where aria-label is not permitted. Print the real href server-side.
 * URLs mirror the HFCM "ai summary" script (#28).
 */
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( false === strpos( $content, 'data-ai-provider' ) ) {
		return $content;
	}
	$default = 'Summarize the content at https://eer24.com/. Exceptional Emergency Centers provide 24/7 emergency care including condition treatment, inpatient and outpatient care, imaging, labs, and pediatrics. Highlight on-site diagnostics, board-certified physicians, and fast, compassionate care. Locations: Amarillo (Coulter & Western), Beaumont, Orange, Port Arthur, Livingston, Fort Worth, and Tyler. Ensure the summary is clear, concise, SEO-friendly, and emphasizes high-quality emergency care.Use only that URL as the source. If you cannot access it, say that clearly and do not guess.';
	$perplexity = 'Use web results to summarize Exceptional Emergency Care  from official pages under site:eer24.com. Prioritize pages under https://eer24.com/, cite exact URLs used, and clearly note any access limitations.';
	$bases = array(
		'gemini'     => 'https://www.google.com/search?udm=50&aep=11&q=',
		'grok'       => 'https://grok.com/?q=',
		'chatgpt'    => 'https://chatgpt.com/?q=',
		'perplexity' => 'https://www.perplexity.ai/search?q=',
		'claude'     => 'https://claude.ai/new?q=',
	);
	return preg_replace_callback(
		'/<a\b([^>]*\bdata-ai-provider=(["\'])([a-z]+)\2[^>]*)>/i',
		function ( $m ) use ( $bases, $default, $perplexity ) {
			$provider = strtolower( $m[3] );
			if ( ! isset( $bases[ $provider ] ) || preg_match( '/\shref=/i', $m[1] ) ) {
				return $m[0];
			}
			$prompt = 'perplexity' === $provider ? $perplexity : $default;
			$href   = $bases[ $provider ] . rawurlencode( $prompt );
			return '<a href="' . esc_url( $href ) . '"' . $m[1] . '>';
		},
		$content
	);
}, 20 );
```

The other sites use the same code with these prompt strings:

- **Altus** (HFCM #20):
  - `$default = 'Summarize the content at https://www.altusemergency.com/. Altus Emergency Centers offer 24/7 emergency care, including condition treatment, inpatient and outpatient care, imaging, labs, and a highlight on-site diagnostics, board-certified physicians, and fast, compassionate care. Locations: Lake Jackson, Lumberton, and Waxahachie, with outpatient centers in Beaumont, Orange, and Port Arthur. Ensure the summary is clear, concise, SEO-friendly, and emphasizes high-quality emergency care.Use only that URL as the source. If you cannot access it, say that clearly and do not guess.';`
  - `$perplexity = 'Use web results to summarize Altus Emergency Centers from official pages under site:altusemergency.com. Prioritize pages under https://altusemergency.com/, cite exact URLs used, and clearly note any access limitations.';`
- **Stat** (HFCM #23):
  - `$default = 'Summarize the content at https://statspecialtyhospital.com/. STAT Specialty Hospital provides 24/7 emergency and hospital care, including conditions treatment, inpatient and outpatient care, imaging, labs, and pediatrics. Highlight on-site diagnostics, experienced physicians, and patient-centred care with minimal wait times. Locations: Del Rio, Eagle Pass, Laredo North, and Laredo South. Ensure the summary is clear, concise, SEO-friendly, and emphasises fast, reliable healthcare.Use only that URL as the source. If you cannot access it, say that clearly and do not guess.';`
  - `$perplexity = 'Use web results to summarize Stat Specialty Hospital  from official pages under site:statspecialtyhospital.com.Prioritize pages under https://statspecialtyhospital.com/, cite exact URLs used, and clearly note any access limitations.';`

Alternative used on nec24: edit the footer Elementor HTML widget itself and add a static `href` to each `a.ai-btn` (the JS still rewrites it later). Back up `_elementor_data` first and clear Elementor's CSS cache afterwards (`DELETE /wp-json/elementor/v1/cache`).

### 3.3 Strip pasted Slack markup (eer24 16; identical on Altus 11 and Stat 9)

```php
/**
 * A11y: text pasted from Slack carried its wrapper markup (role="listitem",
 * role="document", tabindex, data-qa, duplicate ids) into several text
 * widgets. Strip those attributes from Slack-classed tags on output.
 */
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( false === strpos( $content, 'c-virtual_list__item' ) && false === strpos( $content, 'c-message_kit__' ) ) {
		return $content;
	}
	return preg_replace_callback(
		'/<(div|span)\b[^>]*\bclass=(["\'])[^"\']*\b(?:c-virtual_list__|c-message_kit__|c-message__|p-message_pane_|p-block_kit_)[^>]*>/i',
		function ( $m ) {
			return preg_replace(
				'/\s+(?:role|tabindex|id|aria-[a-z]+|data-qa(?:-[a-z]+)?|data-item-key)=(["\'])[^"\']*\1/i',
				'',
				$m[0]
			);
		},
		$content
	);
}, 20 );
```

Altus pages that had Slack markup: homepage (13), Lumberton (1088), Waxahachie (1299), Lake Jackson (1412), Lake Jackson pediatric (1491). Stat: homepage "Our Services". eer24: homepage, Beaumont. nec24: homepage widgets `ac703f5`, `341f5fc` (fixed by editing content to plain `<p>`).

### 3.4 ElementsKit icon font → inline SVG (eer24 17; Altus 14, Stat 10)

eer24's hamburger path was redrawn to match the font glyph's bar thickness and spacing. Altus/Stat use the older path `M3 4h18a1.75 1.75 0 0 1 0 3.5H3A1.75 1.75 0 0 1 3 4zm0 6.25h18a1.75 1.75 0 0 1 0 3.5H3a1.75 1.75 0 0 1 0-3.5zm0 6.25h18a1.75 1.75 0 0 1 0 3.5H3a1.75 1.75 0 0 1 0-3.5z`. Use the eer24 one on new sites, and compare screenshots of the menu before/after.

```php
/**
 * Perf: ElementsKit loads a 450 KB icon font for just three icons in the
 * header menu and on the homepage. Swap those glyphs for inline SVGs so the
 * font is never downloaded. The <i> wrapper and its ekit classes stay, so
 * the menu scripts and styles still find them.
 */
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( false === strpos( $content, 'class="' ) || false === strpos( $content, ' icon icon-' ) && false === strpos( $content, '"icon icon-' ) ) {
		return $content;
	}
	$svgs = array(
		'icon-menu-button-of-three-horizontal-lines' => '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" style="vertical-align:-.125em;pointer-events:none" aria-hidden="true" focusable="false"><path d="M2.5 .8h19a2.2 2.2 0 0 1 0 4.4h-19a2.2 2.2 0 0 1 0-4.4zm0 8.8h19a2.2 2.2 0 0 1 0 4.4h-19a2.2 2.2 0 0 1 0-4.4zm0 8.8h19a2.2 2.2 0 0 1 0 4.4h-19a2.2 2.2 0 0 1 0-4.4z"/></svg>',
		'icon-down-arrow1'                           => '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" style="vertical-align:-.125em;pointer-events:none" aria-hidden="true" focusable="false"><path d="M12 17.4 1.3 6.7l1.4-1.4L12 14.6l9.3-9.3 1.4 1.4z"/></svg>',
		'icon-arrow-right-circle'                    => '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" style="vertical-align:-.125em;pointer-events:none" aria-hidden="true" focusable="false"><g style="fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"><circle cx="12" cy="12" r="11"/><path d="M6.5 12h10.5M12.5 7.5 17 12l-4.5 4.5"/></g></svg>',
	);
	return preg_replace_callback(
		'/<i\b([^>]*?)\bclass="([^"]*)"([^>]*)>\s*<\/i>/i',
		function ( $m ) use ( $svgs ) {
			$classes = preg_split( '/\s+/', trim( $m[2] ) );
			foreach ( $svgs as $name => $svg ) {
				if ( in_array( 'icon', $classes, true ) && in_array( $name, $classes, true ) ) {
					$classes = array_diff( $classes, array( 'icon', $name ) );
					$classes[] = 'ekit-svg-icon';
					return '<i' . $m[1] . 'class="' . implode( ' ', $classes ) . '"' . $m[3] . '>' . $svg . '</i>';
				}
			}
			return $m[0];
		},
		$content
	);
}, 20 );
```

Check the site for other `icon icon-…` classes in use (`grep -o 'icon icon-[a-z0-9-]*'` on the page HTML). If any other ElementsKit glyph is used, add an SVG for it, or the font must keep loading. Confirm afterwards: no `elementskit.woff` request in the network log.

### 3.5 Trustindex reviews: delay loader.js and lazy-load photos (eer24 18; Altus 15, Stat 11)

```php
/**
 * Perf: the Trustindex reviews widget loads cdn.trustindex.io/loader.js on
 * page load, which then pulls ~550 KB of review photos, its CSS and fonts,
 * even though the widget sits far below the fold. Load it on the visitor's
 * first scroll, tap, key press or mouse move instead, and lazy-load the
 * review photos the widget prints in the page.
 */
function eer_ti_delay_js() {
	return "['scroll','pointerdown','touchstart','keydown','mousemove'].forEach(function(e){window.addEventListener(e,tiLoadLoader,{once:true,passive:true});});";
}

// The enqueued loader tag becomes a small injector that waits for interaction.
add_filter( 'script_loader_tag', function ( $tag, $handle, $src ) {
	if ( 'trustindex-loader-js' !== $handle && false === strpos( $src, 'cdn.trustindex.io/loader.js' ) ) {
		return $tag;
	}
	return '<script data-nowprocket>(function(){function tiLoadLoader(){if(window.TrustindexWidget||document.querySelector(\'script[src*="cdn.trustindex.io/loader.js"]\')){return;}var s=document.createElement("script");s.async=true;s.src=' . wp_json_encode( $src ) . ';s.setAttribute("data-ccm-injected","1");document.head.appendChild(s);}' . eer_ti_delay_js() . '})();</script>' . "\n";
}, 99, 3 );

// The widget's own fallback injector fires on DOMContentLoaded; make it wait too.
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( false === strpos( $content, 'tiLoaderFallback' ) ) {
		return $content;
	}
	return preg_replace(
		'/if\s*\(\s*"loading"\s*===\s*document\.readyState\s*\)\s*\{\s*document\.addEventListener\(\s*"DOMContentLoaded"\s*,\s*tiLoadLoader\s*\);\s*\}\s*else\s*\{\s*tiLoadLoader\(\);\s*\}/',
		eer_ti_delay_js(),
		$content
	);
}, 20 );

// The widget's review photos are printed with class="skip-lazy", and Trustindex
// fills them in after Elementor renders, so lazy-load them on the whole page
// from an output buffer opened before any template code runs.
function eer_ti_lazy_images( $html ) {
	if ( false === strpos( $html, 'ti-widget' ) ) {
		return $html;
	}
	return preg_replace_callback(
		'/<img\b(?![^>]*\bloading=)[^>]*\bsrc="https:\/\/(?:cdn\.trustindex\.io|lh3\.googleusercontent\.com)\/[^>]*>/i',
		function ( $m ) {
			return preg_replace( '/^<img\b/i', '<img loading="lazy"', $m[0] );
		},
		$html
	);
}
add_action( 'template_redirect', function () {
	if ( is_admin() || wp_doing_ajax() || is_feed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return;
	}
	ob_start( 'eer_ti_lazy_images' );
}, 0 );
```

Visible change: the reviews widget fills in on the first scroll instead of at page load.

### 3.6 QupHealth check-in widget delay, Exceptional / eer24 version (snippet 19), red #DC271D buttons

This is the final live eer24 version, including the button CSS re-injection and the placeholder styling. **The CSS strings are eer24-specific.**

```php
/**
 * Perf: the QupHealth check-in widget (HFCM snippet #1) loads my-widget.js,
 * 1.3 MB served uncompressed, on page load. It costs ~6 s of mobile CPU and
 * pulls reCAPTCHA twice before anyone taps "Check-In Now". Load it on the
 * visitor's first scroll, tap, key press or mouse move instead. A tap on a
 * check-in button before the widget is ready is remembered (on pointerup,
 * because WP Rocket's delay-JS swallows that first click), and the widget's
 * own button is clicked for the visitor once it has rendered.
 *
 * The site's styling for the widget button lives in Additional CSS, but WP
 * Rocket's Remove Unused CSS drops it once the widget no longer renders during
 * its crawl, and the button falls back to QupHealth's uppercase red. Those
 * rules (copied from Additional CSS) are added back by script just before the
 * widget loads, so RUCSS never sees them.
 *
 * Until the widget renders, each check-in spot shows its Elementor placeholder:
 * plain red text in the mobile header (widget 7ab4001), a blue button in the
 * desktop top bar, and buttons a few pixels taller elsewhere. They are styled
 * like the widget's red button from a head script, so the page looks the same
 * as before and nothing shifts when the widget swaps its button in.
 */
function eer_qup_css() {
	return 'button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.health-widget-container.css-p55m0s{background-color:#dc271d;padding:12px 25px;width:auto!important;border-radius:8px;box-shadow:unset}.css-e5fs27{font-family:Satoshi!important;font-size:clamp(14px, 4vw, 20px)!important;font-weight:500!important;text-transform:capitalize}@media(max-width:768px){button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.health-widget-container.css-p55m0s{padding:9px 10px;width:100%!important;border-radius:7px}.css-e5fs27{font-size:15px!important}}';
}
function eer_qup_placeholder_css() {
	return '.elementor-element-7ab4001.widget-root .elementor-icon-list-items{background-color:#dc271d;border-radius:7px;padding:9px 10px!important;min-width:117px;box-sizing:border-box;justify-content:center}.elementor-element-7ab4001.widget-root .elementor-icon-list-item>.elementor-icon-list-text{color:#fff!important;font-size:15px!important;line-height:22.5px!important;text-transform:capitalize}.widget-root .elementor-button{background-color:#dc271d!important;padding:12px 25px!important;border-radius:8px!important;font-size:clamp(14px, 4vw, 20px)!important;line-height:1.5!important;text-transform:capitalize;box-shadow:none!important;border-width:0!important}.widget-root .elementor-button .elementor-button-text{font-size:inherit!important;line-height:inherit!important}@media(max-width:768px){.widget-root .elementor-button{padding:9px 10px!important;border-radius:7px!important;font-size:15px!important}}';
}
function eer_qup_delay( $html ) {
	if ( false === strpos( $html, 'checkin.quphealth.com/static/js/my-widget.js' ) ) {
		return $html;
	}
	$head = '<script nowprocket data-nowprocket>(function(){var st=document.createElement("style");st.id="eer-qup-placeholder";st.textContent=' . wp_json_encode( eer_qup_placeholder_css() ) . ';document.head.appendChild(st);})();</script>';
	$pos  = stripos( $html, '</head>' );
	if ( false !== $pos ) {
		$html = substr_replace( $html, $head, $pos, 0 );
	}
	return preg_replace_callback(
		'/<script\b[^>]*\bsrc=(["\'])(https:\/\/checkin\.quphealth\.com\/static\/js\/my-widget\.js[^"\']*)\1[^>]*><\/script>/i',
		function ( $m ) {
			$src = wp_json_encode( $m[2] );
			return '<script nowprocket data-nowprocket>(function(){var src=' . $src . ',done=false,evs=["scroll","pointerdown","touchstart","keydown","mousemove","wheel"];'
				. 'function load(){if(done){return;}done=true;evs.forEach(function(e){window.removeEventListener(e,load,{passive:true});});var st=document.createElement("style");st.id="eer-qup-css";st.textContent=' . wp_json_encode( eer_qup_css() ) . ';document.head.appendChild(st);var s=document.createElement("script");s.src=src;s.async=true;document.head.appendChild(s);}'
				. 'evs.forEach(function(e){window.addEventListener(e,load,{passive:true});});'
				. 'function want(root){if(root.qupWant){return;}root.qupWant=1;load();root.style.cursor="progress";var n=0,t=setInterval(function(){var b=root.querySelector(".health-widget-container");if(b||++n>150){clearInterval(t);root.style.cursor="";if(b){b.click();}}},100);}'
				. 'function pending(e){var root=e.target.closest&&e.target.closest(".widget-root");return root&&!root.querySelector(".health-widget-container")?root:null;}'
				. 'var sx=0,sy=0;window.addEventListener("pointerdown",function(e){sx=e.clientX;sy=e.clientY;},{capture:true,passive:true});'
				. 'window.addEventListener("pointerup",function(e){var root=pending(e);if(root&&Math.abs(e.clientX-sx)<10&&Math.abs(e.clientY-sy)<10){want(root);}},{capture:true,passive:true});'
				. 'document.addEventListener("click",function(e){var root=pending(e);if(root){e.preventDefault();e.stopPropagation();want(root);}},true);'
				. '})();</script>';
		},
		$html,
		1
	);
}
add_action( 'template_redirect', function () {
	if ( is_admin() || wp_doing_ajax() || is_feed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return;
	}
	ob_start( 'eer_qup_delay' );
}, 0 );
```

### 3.7 QupHealth check-in widget delay, Stat version (snippet 12), blue #0082C2 buttons

Same logic, Stat's own blue button rules, no placeholder styling. Also saved in the project files as `stat/quphealth-delay-stat.php`.

```php
/**
 * Perf: the QupHealth check-in widget (HFCM snippet #2) loads my-widget.js,
 * 1.3 MB served uncompressed, on page load. It costs ~6 s of mobile CPU and
 * pulls reCAPTCHA twice before anyone taps "Check-In Now". Load it on the
 * visitor's first scroll, tap, key press or mouse move instead. A tap on a
 * check-in button before the widget is ready is remembered (on pointerup,
 * because WP Rocket's delay-JS swallows that first click), and the widget's
 * own button is clicked for the visitor once it has rendered.
 *
 * The site's blue styling for the widget button lived in the page CSS, but WP
 * Rocket's Remove Unused CSS drops it once the widget no longer renders during
 * its crawl, and the button falls back to QupHealth's red. Those rules are
 * added back by script, just before the widget loads, so RUCSS never sees them.
 */
function stat_qup_css() {
	return 'button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.health-widget-container.css-p55m0s{background-color:#0082c2;box-shadow:unset!important;padding:15px 35px;width:auto!important;border-radius:8px}.css-e5fs27{font-family:Satoshi!important;font-size:clamp(15px, 4vw, 18px)!important;font-weight:500!important;text-transform:capitalize}@media(max-width:768px){button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.health-widget-container.css-p55m0s{background-color:#0082c2;padding:9px 10px!important;box-shadow:unset!important;width:100%!important;border-radius:8px}.css-e5fs27{font-size:15px!important}}';
}
function stat_qup_delay( $html ) {
	if ( false === strpos( $html, 'checkin.quphealth.com/static/js/my-widget.js' ) ) {
		return $html;
	}
	return preg_replace_callback(
		'/<script\b[^>]*\bsrc=(["\'])(https:\/\/checkin\.quphealth\.com\/static\/js\/my-widget\.js[^"\']*)\1[^>]*><\/script>/i',
		function ( $m ) {
			$src = wp_json_encode( $m[2] );
			return '<script nowprocket data-nowprocket>(function(){var src=' . $src . ',done=false,evs=["scroll","pointerdown","touchstart","keydown","mousemove","wheel"];'
				. 'function load(){if(done){return;}done=true;evs.forEach(function(e){window.removeEventListener(e,load,{passive:true});});var st=document.createElement("style");st.id="stat-qup-css";st.textContent=' . wp_json_encode( stat_qup_css() ) . ';document.head.appendChild(st);var s=document.createElement("script");s.src=src;s.async=true;document.head.appendChild(s);}'
				. 'evs.forEach(function(e){window.addEventListener(e,load,{passive:true});});'
				. 'function want(root){if(root.qupWant){return;}root.qupWant=1;load();root.style.cursor="progress";var n=0,t=setInterval(function(){var b=root.querySelector(".health-widget-container");if(b||++n>150){clearInterval(t);root.style.cursor="";if(b){b.click();}}},100);}'
				. 'function pending(e){var root=e.target.closest&&e.target.closest(".widget-root");return root&&!root.querySelector(".health-widget-container")?root:null;}'
				. 'var sx=0,sy=0;window.addEventListener("pointerdown",function(e){sx=e.clientX;sy=e.clientY;},{capture:true,passive:true});'
				. 'window.addEventListener("pointerup",function(e){var root=pending(e);if(root&&Math.abs(e.clientX-sx)<10&&Math.abs(e.clientY-sy)<10){want(root);}},{capture:true,passive:true});'
				. 'document.addEventListener("click",function(e){var root=pending(e);if(root){e.preventDefault();e.stopPropagation();want(root);}},true);'
				. '})();</script>';
		},
		$html,
		1
	);
}
add_action( 'template_redirect', function () {
	if ( is_admin() || wp_doing_ajax() || is_feed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return;
	}
	ob_start( 'stat_qup_delay' );
}, 0 );
```

**How to build `*_qup_css()` for a new site:** open the live page *before* activating the delay, find the rules for `.health-widget-container.css-p55m0s` and `.css-e5fs27` (including any `@media(max-width:768px)` variant) in Additional CSS (`#wp-custom-css`) or in WP Rocket's used CSS (`#wpr-usedcss`), and copy them exactly. If the site's Additional CSS for the button changes later, update the function too. The `css-p55m0s` / `css-e5fs27` class names come from QupHealth's build; if QupHealth ships a new build they can change, so recheck after any QupHealth update.

**How to build the placeholder CSS:** find the Elementor elements inside `.widget-root` that show before the widget renders (e.g. eer24's mobile header icon-list widget `7ab4001` and `.elementor-button`s), measure the widget button's computed size/colour after load, and make the placeholder match so nothing shifts when the widget swaps in.

### 3.8 Homepage hero layout shift on mobile (eer24 snippet 22)

Element IDs (`elementor-13`, `a7d6aaf`, `40ae4ae`) and the image ratio are eer24-specific. Only add a fix like this if the **live** page shows the shift after the speed fixes.

```php
/**
 * Perf (CLS): on mobile the homepage HTML arrives in chunks, and Chrome paints
 * the hero before the rest of its section is parsed. The hero text is first
 * centred in the section's 500px min-height and the hero image's widget has
 * no height until the image loads, so the next section shows below it and is
 * pushed off screen (CLS 0.33 in Lighthouse). Top-align the hero lines and
 * reserve the image's height (500x509, full width minus 20px padding, at most
 * 509px). The finished layout is unchanged at every mobile width.
 * Added from a head script so WP Rocket's Remove Unused CSS cannot drop it.
 */
add_action( 'wp_head', function () {
	if ( ! is_front_page() ) {
		return;
	}
	$css = '@media(max-width:767px){.elementor-13 .elementor-element.elementor-element-a7d6aaf{--align-items:flex-start}.elementor-13 .elementor-element.elementor-element-a7d6aaf>.e-con-inner{align-content:flex-start}.elementor-13 .elementor-element.elementor-element-40ae4ae{min-height:min(calc((100vw - 20px) * 1.018), 509px)}}';
	echo '<script nowprocket data-nowprocket>(function(){var st=document.createElement("style");st.id="eer-hero-cls";st.textContent=' . wp_json_encode( $css ) . ';document.head.appendChild(st);})();</script>' . "\n";
}, 1 );
```

### 3.9 Clearing the WP Rocket cache over the REST API

There is no WP Rocket REST endpoint, so we cleared the cache with a **single-use** Code Snippets snippet, activated once, then deleted (two DELETE calls: deactivate/trash then delete). It calls `rocket_clean_domain()` once and sets an option so it never runs twice. Equivalent code (the exact text wasn't saved; on eer24 it left options `eer_rc_done`, `eer_rc_done2`, `eer_rc_done3`):

```php
add_action( 'init', function () {
	if ( get_option( 'site_rc_done' ) || ! function_exists( 'rocket_clean_domain' ) ) {
		return;
	}
	update_option( 'site_rc_done', time(), false );
	rocket_clean_domain();
} );
```

Use a new option name each time (or delete the option). If you have wp-admin, the simpler route is WP Rocket → Dashboard → Clear and preload cache. When Remove Unused CSS is on, also "Clear Used CSS" so it re-crawls with the new HTML. After editing Elementor content directly, clear Elementor's CSS cache too: `DELETE /wp-json/elementor/v1/cache`.

### 3.10 Local test harness (eer24 `snippets/test.php`)

Runs the snippets against a saved copy of a page, without WordPress:

```php
<?php
// Simulates both filters on a saved page: the content filter, plus the loader tag swap.
$filters=[]; $tagf=null;
function add_filter($h,$f,$p=10,$n=1){ global $filters,$tagf; if($h==="script_loader_tag") $tagf=$f; else $filters[]=$f; }
function add_action($h,$f,$p=10){}
function wp_json_encode($v){ return json_encode($v, JSON_UNESCAPED_SLASHES); }
function esc_url($u){ return htmlspecialchars($u, ENT_QUOTES); }
foreach (array_slice($argv,3) as $s) eval(file_get_contents(__DIR__."/$s.php"));
$html=file_get_contents($argv[1]);
foreach ($filters as $f) $html=$f($html);
$html=preg_replace_callback('/<script[^>]*id="trustindex-loader-js-js"[^>]*src="([^"]+)"[^>]*><\/script>/', function($m) use ($tagf){ return $tagf($m[0],'trustindex-loader-js',$m[1]); }, $html);
if (function_exists('eer_ti_lazy_images')) $html=eer_ti_lazy_images($html); // template_redirect output buffers
if (function_exists("eer_qup_delay")) $html=eer_qup_delay($html);
file_put_contents($argv[2],$html);
```

Usage: `php test.php in.html out.html 1-aibtn 2-slack 3-ekit-icons 4-trustindex-lazy 5-quphealth-delay` (each name is a snippet file next to it, without the `<?php` line, exactly as pasted into Code Snippets).

---

## 4. WP Rocket settings and how they interact with the fixes

We did **not** change any WP Rocket settings on these sites; every fix works with the existing configuration. What matters is knowing how these settings behave:

| WP Rocket setting | State on these sites | Effect we had to work around |
|---|---|---|
| **File Optimization → Delay JavaScript execution** | On | Delays HFCM scripts (e.g. the AI-summary href script) until interaction, so Lighthouse sees the pre-script DOM → fix A2 server-side. It also **swallows the first click/tap** on the page while it loads the delayed scripts → QupHealth tap is caught on `pointerup` (with a <10 px no-drag check), not `click`. Our own inline loaders carry `nowprocket data-nowprocket` so they run immediately. |
| **File Optimization → Remove Unused CSS (RUCSS)** | On (Stat, eer24) | Strips CSS not used in its crawl and strips inline `<style>` blocks. Anything rendered later by JS (QupHealth button) loses its styling → inject CSS from JS. SVG icon sizing goes in attributes, not a `<style>`. After changing HTML, clear used CSS so it re-crawls. |
| **Media → LazyLoad for images** | On | Skips images with `skip-lazy` (Trustindex photos) and images added after its pass → we add `loading="lazy"` from an output buffer. |
| **Delay JS exclusions** | QupHealth HFCM tag on eer24 was marked `nowprocket` (excluded) | Excluding a heavy third-party script from Delay JS makes it load on page load; we replaced the tag with our own interaction loader instead of relying on WP Rocket. |
| **Page cache** | On | Snippets change the cached HTML only after cache is cleared. Always clear and re-check. |

Recommendations for a new site (ask before changing settings on a live site):
- Keep Delay JS on. Do not add `nowprocket` to heavy widgets; use the pattern in 3.6 instead.
- Keep RUCSS on, but for every element that a delayed script renders, plan to re-inject its CSS from JS.
- `ElementsKit_Helper is not defined` appears in the console on Stat, eer24 and nec24 **before** our changes. It comes from Delay JS ordering. If it ever breaks the menu, add the ElementsKit frontend scripts to the Delay JS exclusions (e.g. `elementskit-lite`, `ekit`), test, and confirm nothing else regresses. We did not change it, because the menus worked.
- Elementor popups and CF7 (`wpcf7 is not defined` on Altus) show similar pre-existing delay errors; leave them unless something is broken.

---

## 5. What failed or caused problems (avoid these)

1. **Pasting one site's QupHealth snippet onto another site.** The owner pasted the eer24 version (red #DC271D hardcoded) onto Stat, and Stat's blue check-in buttons turned red. Fix: each site gets its own `*_qup_css()` from its own CSS. Keep **only one** QupHealth delay snippet active per site.
2. **Delaying QupHealth without re-injecting the button CSS.** RUCSS dropped the site's button rules and the buttons fell back to QupHealth's uppercase crimson (#CC1E41, 4px radius, slightly shorter). See `eer24/checkin-button-compare.png` in the project files: old fix (broken) / new fix / live.
3. **Catching the check-in tap on `click`.** With WP Rocket Delay JS, the first tap only loaded the widget and a second tap was needed. Use `pointerup` capture plus a capturing `click` handler that calls `preventDefault()`; poll for `.health-widget-container` and click it once rendered (up to 15 s).
4. **SVG icons with a `<style>` block.** RUCSS stripped it. Put `width/height/fill/style` attributes on the SVG.
5. **SVGs eating clicks.** Mobile submenu arrows stopped expanding the submenus until `pointer-events:none` was added to the SVG.
6. **Lazy-loading Trustindex photos only in the Elementor content filter.** On cached pages the photos still loaded at page open, because Trustindex prints them after Elementor renders. Use the `template_redirect` output buffer.
7. **Leaving the Trustindex fallback alone.** The widget's own `tiLoaderFallback` fires on DOMContentLoaded and loads `loader.js` anyway; the regex in 3.5 rewrites it to wait for interaction.
8. **Trusting CLS from a local copy.** The local eer24 homepage copy showed CLS 0.25–0.34 that the live site didn't. But once live and light, a real CLS 0.33 appeared. Always measure CLS on the live site after activation.
9. **Placeholder mismatch.** Before the widget rendered, the desktop top-bar "Check-in Now" showed blue and other buttons were 2–6 px taller, then jumped. Match placeholder size and colour to the rendered widget button.
10. **Google PageSpeed Insights API quota.** The free daily quota ran out; we ran Lighthouse ourselves. Tell the owner our numbers are stricter than PSI and ask them to re-run PSI.
11. **Playwright and localhost.** In this environment Playwright forces localhost through the proxy. Serve test copies with `page.route()` on the live URL instead of a local server.
12. **Environments.** A session only has the credentials of the environment it started in. To work on another site, the owner switches the project's cloud environment and a new thread is started.
13. **App password stopped working on Stat** mid-session (login refused). Ask the owner for a new application password via the environment settings, never in chat.

---

## 6. Step-by-step procedure for a new site

**Access**
1. Confirm `WP_URL`, `WP_USER`, `WP_APP_PASSWORD` in the environment. Test: `curl -u "$WP_USER:$WP_APP_PASSWORD" "$WP_URL/wp-json/wp/v2/users/me"`.
2. List plugins: `GET /wp-json/wp/v2/plugins`. Note Elementor, ElementsKit, WP Rocket (and whether RUCSS is on: look for `wpr-usedcss` in the page HTML), HFCM, Trustindex, QupHealth, Code Snippets.
3. List existing snippets: `GET /wp-json/code-snippets/v1/snippets` (note the next free IDs, and whether any older speed snippets exist).

**Baseline**
4. Run mobile Lighthouse on the homepage and 2–3 location/service pages, 3–4 runs each: `npx lighthouse URL --form-factor=mobile --throttling-method=simulate --output=json`. Record perf, accessibility, page weight, TBT, LCP, CLS and the failing audits.
5. Save each page's HTML (`curl -s URL > page.html`) and grep for the patterns:
   - `elementor-background-video-hosted` with `role="presentation"` → 3.1
   - `data-ai-provider` without `href` → 3.2 (copy prompts from HFCM: `GET` the HFCM snippet or view the page's inline script)
   - `c-virtual_list__item` / `c-message_kit__` → 3.3
   - `icon icon-` classes + `elementskit.woff` request → 3.4
   - `cdn.trustindex.io/loader.js`, `ti-widget`, `skip-lazy` → 3.5
   - `checkin.quphealth.com/static/js/my-widget.js` → 3.6/3.7
   - Popups with `role="document"` + `aria-modal`, contrast failures → report to owner

**Build and test locally**
6. Adapt each snippet: function prefix, site prompts, button CSS copied from this site, placeholder selectors, SVG list.
7. Run the harness (3.10) on each saved page; serve the output gzip-compressed with `<base href="LIVE_URL/">` and run Lighthouse on it, before and after.
8. In Playwright (Pixel 5 emulation), with the patched HTML routed in place of the live URL: one tap on "Check-In Now" opens the location list; the mobile menu and submenus open; no `elementskit.woff` request; reviews appear after scrolling; check-in buttons look the same before and after the widget loads (screenshot compare against live, mobile + desktop); simulate RUCSS by removing the button rules from the used CSS and confirm the colour is still right.

**Save inactive and ask**
9. `POST /wp-json/code-snippets/v1/snippets` with `{"name":"Perf: …","code":"…","scope":"global","active":false}`. Name them `A11y: …` / `Perf: …`.
10. Tell the owner: what each snippet does, before → after numbers, the visible changes (reviews and check-in load on first interaction), and that switching off undoes it. Wait for "go".

**Activate and verify live**
11. Activate (`PUT …/snippets/{id}` with `"active":true` or `POST …/snippets/{id}/activate`).
12. Clear WP Rocket cache (3.9) and, with RUCSS, used CSS. Delete the one-off cache snippet afterwards.
13. Re-run step 8 on the live site (menu, check-in tap, button colours before/after load on mobile and desktop, reviews) and run Lighthouse 3–4 times on the same pages. Check CLS on the live homepage specifically.
14. If something broke, switch that snippet off, clear cache, and report.
15. Write a `HANDOFF.md` for the site in the repo (snippet IDs, causes, scores, open items), commit to the session branch.

**If mobile is still under 90:** look at the heaviest remaining item in the Lighthouse "reduce JavaScript execution time" and "network payload" lists; then oversized images (resize/WebP, ~0.7 MB on Stat); then the large Elementor CSS; then per-page issues like popups shifting layout.

---

## 6A. How we measured page speed (tools, commands, comparison)

**Why not PageSpeed Insights directly:** the Google PSI API (`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=…&strategy=mobile&category=performance&category=accessibility`) was the first choice, but its free daily quota (no API key) was used up on every site. So we ran the same engine PSI uses, **Lighthouse**, ourselves in the cloud container's headless Chromium. If you have a PSI API key, add `&key=…` and use PSI as well; the owner checks results on pagespeed.web.dev.

**Lighthouse setup (Lighthouse 12, mobile, the same defaults PSI uses).** The earlier sessions did not save their exact scripts, so the commands below are equivalent ones that reproduce the same setup:
- Form factor mobile (Moto G Power-sized screen), **simulated throttling** (slow 4G, 150 ms RTT, ~1.6 Mbps) and **4x CPU slowdown** by default; on Altus we also ran with **6x CPU** to be stricter.
- Categories: performance, accessibility (plus best-practices and SEO for the baseline).
- Chromium is pre-installed at `/opt/pw-browsers/chromium`.

```bash
npm i -g lighthouse@12
export CHROME_PATH=/opt/pw-browsers/chromium   # or the chromium binary inside that folder
for i in 1 2 3 4; do
  lighthouse "https://example.com/" \
    --form-factor=mobile --screenEmulation.mobile --throttling-method=simulate \
    --only-categories=performance,accessibility \
    --chrome-flags="--headless=new --no-sandbox" \
    --output=json --output-path="home-run$i.json" --quiet
done
# stricter run (as on Altus): add --throttling.cpuSlowdownMultiplier=6
# desktop check: --preset=desktop
```

Pull out the numbers from each JSON:

```bash
for f in home-run*.json; do jq -r '[.categories.performance.score*100, .categories.accessibility.score*100,
  (.audits["largest-contentful-paint"].numericValue/1000), .audits["total-blocking-time"].numericValue,
  .audits["cumulative-layout-shift"].numericValue, .audits["speed-index"].numericValue/1000,
  (.audits["total-byte-weight"].numericValue/1024|floor)] | @tsv' "$f"; done
# columns: perf, a11y, LCP s, TBT ms, CLS, SI s, KiB
# failing accessibility audits:
jq -r '.audits | to_entries[] | select(.value.score==0 and (.value.details.type=="table" or .value.details.type=="list")) | .key' home-run1.json
# biggest JS cost and payload:
jq -r '.audits["bootup-time"].details.items[] | "\(.total|floor) ms  \(.url)"' home-run1.json | head
jq -r '.audits["network-requests"].details.items | sort_by(-.transferSize)[:15][] | "\(.transferSize/1024|floor) KiB  \(.url)"' home-run1.json
```

That is how we found the causes: `bootup-time` showed QupHealth `my-widget.js` at ~6–7 s CPU; `network-requests` showed `elementskit.woff` (~450 KB) and the Trustindex/Google review photos (~500–800 KB); the accessibility audits named the elements (video role, AI links, Slack markup, contrast).

**Testing a fix before it goes live (local copy):**
1. Save the live page: `curl -s https://example.com/ > before.html`.
2. Apply the snippets with the harness: `php test.php before.html after.html 1-aibtn 2-slack …`.
3. Add `<base href="https://example.com/">` right after `<head>` in both files so CSS, JS and images still load from the live site.
4. Serve both **gzip-compressed** (uncompressed local files make the score look worse than real), e.g. a tiny Node/Python server with gzip, or better, use Playwright `page.route("https://example.com/", …)` to serve the file in place of the live URL (Playwright forces localhost through the proxy here). Run Lighthouse 3–4 times on **before** and **after** under identical settings.
5. Functional check in Playwright with `devices["Pixel 5"]`: tap "Check-In Now" once → location list opens; open the mobile menu and a submenu; scroll → reviews appear; record all network requests and assert there is no `elementskit.woff` and no `my-widget.js` before interaction; take screenshots of the header/check-in buttons before and after the widget loads and compare them with live (that is how `eer24/checkin-button-compare.png` was made).

**After going live:** clear the WP Rocket cache, load each page once to warm the cache, then run the same Lighthouse loop on the live URLs and repeat the Playwright checks.

**How we compared before and after:**
- Same tool, same settings, same pages, same machine, run back to back. Never compare our Lighthouse number against a PSI number.
- 3–4 runs per page; report the **range** (e.g. 86–93) and median, because mobile scores swing 5–15 points run to run (the old Altus homepage ranged 50–92).
- Compare the metrics, not just the score: TBT and Speed Index (QupHealth), page weight in KiB (icon font, photos), LCP, CLS, and the list of failing accessibility audits.
- Our setup is stricter than PSI: the old Stat homepage scored 42 for us and 73 on PSI. After changes, ask the owner to re-run PSI on pagespeed.web.dev and expect a higher number than ours.
- If the score lands near the target, plug the measured metrics into Lighthouse's scoring weights (TBT 30%, LCP 25%, CLS 25%, FCP 10%, SI 10%) to estimate; we did this on Stat to predict ~90–92 before activating.

---

## 7. Open items per site

**Altus (altusemergency.com)**
- Elementor popup 36373: `aria-allowed-attr` (`role="document"` dialog with `aria-modal`) on Lumberton, Waxahachie, Lake Jackson → these score 95–96 accessibility instead of 100. Offered a snippet fix, not done.
- Lumberton page is very heavy: one run scored 24 (2.9 MB, TBT 1.9 s, CLS 0.37 from a popup). Needs its own pass.

**Stat (statspecialtyhospital.com)**
- **Confirm snippet 12 is the Stat blue version.** The owner pasted the eer24 red version on Stat; we provided `stat/quphealth-delay-stat.php` (blue #0082C2) to paste over it. Check the live check-in buttons are blue, only one QupHealth snippet is active, and the cache was cleared.
- App password for `dev@themaddex.com` was refused at the end of the session; a new one is needed in the Stat environment.
- color-contrast: brand blue `#0082C2` on white is 4.22:1 (use `#007BB8` → 4.64:1); green service headings `#39B54A` are 2.66:1 (use `#2E9A3D` → 3.62:1). Visible change, needs owner OK.
- `link-in-text-block` on /locations/laredo-south (underline links in body text).
- /services/laredo/inpatient has CLS ~0.15.
- Optional: oversized images (resize + WebP, ~0.7–0.8 MB), ~345 KB page CSS.

**Exceptional (eer24.com)**
- color-contrast on Beaumont: `#1275BA` on `#EBEBEB` (4.11:1) and white on `#0082C2` buttons (4.22:1). Needs slightly darker blues and owner OK.
- /locations/brownsville redirects to valleyregionalmedicalcenter.com (flag to owner).
- Leftover options `eer_rc_done`, `eer_rc_done2`, `eer_rc_done3` from the cache-clear snippets (harmless).

**nec24.com**
- Console error `ElementsKit_Helper is not defined` (WP Rocket Delay JS exclusions), pre-existing.

**All sites**
- `ElementsKit_Helper is not defined` console error is pre-existing; don't chase it unless the menu breaks.
- A weekly PageSpeed check routine (Mondays, report only) was proposed for Altus at project setup.

---

## 8. Other approaches used (nec24.com, earlier session)

Instead of output-filter snippets, nec24 was fixed by editing Elementor data directly through the REST API:
1. Back up `_elementor_data` of each page/template before changing it (saved in the repo under `nec24/backup/`).
2. Homepage (13) text widgets `ac703f5`, `341f5fc`: replaced Slack markup with plain `<p>`; underlined location links (`link-in-text-block`).
3. Homepage: four grey text colours `#7C7C7C` → `#666666` (contrast 4.17 → 5.7:1), approved by the owner.
4. Footer template (1208) HTML widget `03b81a3`: static `href` added to each `a.ai-btn`.
5. `DELETE /wp-json/elementor/v1/cache` to rebuild Elementor CSS.
Result: accessibility 87 → 100, SEO 92 → 100.

Use this direct-edit approach when the fix is a one-time content correction and the owner is fine with editing page data. Prefer snippets when the problem comes from a plugin's output or a script (it survives page edits and is instantly reversible).
