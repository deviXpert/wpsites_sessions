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
