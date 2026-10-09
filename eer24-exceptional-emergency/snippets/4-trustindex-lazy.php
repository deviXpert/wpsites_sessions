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
