/**
 * Perf: the Trustindex reviews widget prints ~20 review photos with
 * class="skip-lazy", so all of them (about 550 KB) download on page load
 * even though the widget sits far below the fold. Let the browser lazy-load
 * them instead.
 */
add_filter( 'elementor/frontend/the_content', function ( $content ) {
	if ( false === strpos( $content, 'ti-widget' ) ) {
		return $content;
	}
	return preg_replace_callback(
		'/<img\b[^>]*\bsrc="https:\/\/(?:cdn\.trustindex\.io|lh3\.googleusercontent\.com)\/[^>]*>/i',
		function ( $m ) {
			$tag = $m[0];
			if ( false !== stripos( $tag, 'loading=' ) ) {
				return $tag;
			}
			return preg_replace( '/^<img\b/i', '<img loading="lazy"', $tag );
		},
		$content
	);
}, 20 );
