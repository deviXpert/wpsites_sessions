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
