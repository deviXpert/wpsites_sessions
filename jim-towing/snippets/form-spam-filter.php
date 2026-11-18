<?php
/**
 * Jim Towing — block spam / sales pitches on Elementor Pro forms (server-side).
 * Paste into WPCode → Add Snippet → PHP Snippet, Location: "Run Everywhere", then Activate.
 * (Paste without the opening "<?php" line if WPCode already shows one.)
 *
 * A submission is rejected when ANY of these is true:
 *  - phone is not a valid Canada/US number (10 digits, or 11 starting with 1; area code can't start with 0/1)
 *  - any field contains a link, an email address, or non-Latin script (Cyrillic, Chinese, Arabic, ...)
 *  - text matches common sales/SEO/"what's your price" spam phrases (many languages)
 *  - the same IP sent more than 3 requests in the last hour
 */
add_action( 'elementor_pro/forms/validation', function ( $record, $ajax_handler ) {
	$fields = $record->get( 'fields' );
	$val    = function ( $id ) use ( $fields ) { return isset( $fields[ $id ]['value'] ) ? trim( (string) $fields[ $id ]['value'] ) : ''; };
	$call   = ' Please call us at 587-914-0130.';
	$block  = function () use ( $ajax_handler, $call ) { $ajax_handler->add_error_message( 'Sorry, we couldn\'t send your request.' . $call ); };

	// 1) Phone must be North American.
	if ( isset( $fields['phone'] ) ) {
		$d = preg_replace( '/\D+/', '', $val( 'phone' ) );
		if ( strlen( $d ) === 11 && $d[0] === '1' ) { $d = substr( $d, 1 ); }
		$ca = array( 204,226,236,249,250,257,263,289,306,343,354,365,367,368,382,403,416,418,428,431,437,438,450,460,468,474,506,514,519,548,579,581,584,587,604,613,639,647,672,683,705,709,742,753,778,780,782,807,819,825,867,873,879,902,905 );
		if ( strlen( $d ) !== 10 || ! preg_match( '/^[2-9]\d{2}[2-9]\d{6}$/', $d ) || ! in_array( (int) substr( $d, 0, 3 ), $ca, true ) ) {
			$ajax_handler->add_error( 'phone', 'Please enter a valid Canadian phone number, e.g. 587-914-0130.' );
			return;
		}
	}

	$text = implode( "\n", array_map( function ( $f ) { return is_array( $f['value'] ) ? implode( ' ', $f['value'] ) : (string) $f['value']; }, $fields ) );

	// 2) Links, emails, non-Latin scripts.
	if ( preg_match( '~https?://|www\.|\[url|<a\s|\b[a-z0-9-]+\.(ca|com|net|org|ru|xyz|top|info|io|co|us|uk|biz|online|site|store)\b~i', $text )
		|| preg_match( '/[\w.+-]+@[\w-]+\.[\w.]+/', $text )
		|| preg_match( '/[\p{Cyrillic}\p{Han}\p{Arabic}\p{Hebrew}\p{Thai}\p{Hangul}\p{Hiragana}\p{Katakana}\p{Devanagari}]/u', $text ) ) {
		$block(); return;
	}

	// 3) Sales / SEO / price-question spam phrases.
	$spam = '/\b(seo|backlinks?|search engine|google (ranking|first page)|first page of google|web ?design|website (design|redesign|development|traffic)|'
		. 'digital marketing|marketing (services|agency)|social media (marketing|management)|lead generation|guest post|outsourc|'
		. 'virtual assistant|app development|crypto|bitcoin|forex|investment opportunit|loan offer|'
		. 'din pris|jeres pris|ihren? preis|ihre preise|votre prix|vos prix|uw prijs|je prijs|tu precio|su precio|il tuo prezzo|'
		. 'twoja cena|ditt pris|hinnan|jūsų kain|wanted to know your price|know your prices?|price list|videos?|animation|explainer|advertis\w*|promot\w*|your (business|website|site|company|brand)|social media|instagram|tiktok|youtube|samples? of|our (services|team|work|agency|company)|i just visited|i came across|i noticed your|partnership|collaborat\w*|sponsor\w*|unsubscribe|opt[- ]out|\(?usd\)?)\b/iu';
	if ( preg_match( $spam, $text ) || preg_match( '/\$\s?\d/', $text ) ) { $block(); return; }

	// 4) Max 3 submissions per IP per hour.
	$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? $_SERVER['REMOTE_ADDR'] : '';
	$key = 'jim_form_' . md5( $ip );
	$n   = (int) get_transient( $key );
	if ( $n >= 3 ) { $block(); return; }
	set_transient( $key, $n + 1, HOUR_IN_SECONDS );
}, 10, 2 );
