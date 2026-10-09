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
		'icon-menu-button-of-three-horizontal-lines' => '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M2 5h20v2H2zm0 6h20v2H2zm0 6h20v2H2z"/></svg>',
		'icon-down-arrow1'                           => '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 17.4 1.3 6.7l1.4-1.4L12 14.6l9.3-9.3 1.4 1.4z"/></svg>',
		'icon-arrow-right-circle'                    => '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24zm0 22a10 10 0 1 1 0-20 10 10 0 0 1 0 20zm.3-15.7-1.4 1.4 3.3 3.3H6v2h8.2l-3.3 3.3 1.4 1.4 5.7-5.7z"/></svg>',
	);
	$count   = 0;
	$content = preg_replace_callback(
		'/<i\b([^>]*?)\bclass="([^"]*)"([^>]*)>\s*<\/i>/i',
		function ( $m ) use ( $svgs, &$count ) {
			$classes = preg_split( '/\s+/', trim( $m[2] ) );
			foreach ( $svgs as $name => $svg ) {
				if ( in_array( 'icon', $classes, true ) && in_array( $name, $classes, true ) ) {
					$classes = array_diff( $classes, array( 'icon', $name ) );
					$classes[] = 'ekit-svg-icon';
					$count++;
					return '<i' . $m[1] . 'class="' . implode( ' ', $classes ) . '"' . $m[3] . '>' . $svg . '</i>';
				}
			}
			return $m[0];
		},
		$content
	);
	if ( $count ) {
		$content = '<style>.ekit-svg-icon{display:inline-block;line-height:1}.ekit-svg-icon svg{width:1em;height:1em;fill:currentColor;vertical-align:-.125em}</style>' . $content;
	}
	return $content;
}, 20 );
