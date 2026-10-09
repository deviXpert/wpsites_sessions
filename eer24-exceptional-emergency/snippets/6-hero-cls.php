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
