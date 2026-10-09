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
