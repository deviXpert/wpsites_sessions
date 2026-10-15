/**
 * AAD – block sales pitches / spam in Elementor Pro form submissions (all forms, site-wide).
 * Rejected submissions are not emailed or stored; the visitor sees a generic error with the phone number.
 * Managed from the repo: aad-transport-recovery/tools/form_spam_filter.php (pushed by publish_spam_filter.py).
 */
if ( ! function_exists( 'aad_form_spam_reason' ) ) {
	function aad_form_spam_reason( $text ) {
		$t = strtolower( wp_strip_all_tags( (string) $text ) );
		$patterns = array(
			'/\bseo\b/', '/search engine/', '/\bserp/', '/rank(ing|ings)?\s+(on|in|higher|your|#|1st|first|top)/', '/first page of google/', '/page\s*(1|one) (of|on) google/',
			'/digital marketing/', '/\bmarketing (agency|services|manager|team|campaign|expert|strategy)/', '/social media/', '/\bsmm\b/', '/\bppc\b/', '/google ads/', '/facebook ads/',
			'/backlink/', '/link[\s-]?building/', '/guest post/', '/domain authority/', '/\bda\s*\/\s*pa\b/', '/organic traffic/', '/website traffic/', '/more traffic to/',
			'/web(site)?\s*(design|redesign|development|developer)/', '/(re)?design (of )?your (web)?site/', '/app development/', '/wordpress (expert|developer)/',
			'/lead[\s-]?gen/', '/(new|more|qualified) (clients|customers|leads)/', '/\d+\s*(to|-)\s*\d+\s*new clients/', '/white[\s-]?hat/', '/grow (your|the) business/',
			'/opt[\s-]?out/', '/unsubscribe/', '/not interested in our services/', '/our (agency|solutions)/', '/(services|solutions) (we|i) (offer|provide)/', '/(outsourc|virtual assistant|content writ)/',
			'/google (my )?business profile/', '/\bgmb\b/', '/\b(crypto|bitcoin|forex)\b/', '/business (loan|funding)/', '/merchant (cash|services)/',
			'/https?:\/\//', '/\bwww\./',
		);
		foreach ( $patterns as $p ) {
			if ( preg_match( $p, $t ) ) { return $p; }
		}
		return false;
	}
}
add_action( 'elementor_pro/forms/validation', function ( $record, $ajax_handler ) {
	$fields = (array) $record->get( 'fields' );
	$text = '';
	foreach ( $fields as $f ) {
		if ( isset( $f['type'] ) && in_array( $f['type'], array( 'text', 'textarea', 'email' ), true ) ) { $text .= ' ' . ( is_array( $f['value'] ) ? implode( ' ', $f['value'] ) : $f['value'] ); }
	}
	if ( ! aad_form_spam_reason( $text ) ) { return; }
	$target = isset( $fields['message'] ) ? 'message' : ( $fields ? array_key_first( $fields ) : 'message' );
	$ajax_handler->add_error( $target, 'Sorry, we can\'t accept this message. If you need recovery or a quote, please call us on 07771 004242.' );
	$ajax_handler->add_error_message( 'Sorry, we can\'t accept this message. If you need recovery or a quote, please call us on 07771 004242.' );
}, 10, 2 );
