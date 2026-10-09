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
