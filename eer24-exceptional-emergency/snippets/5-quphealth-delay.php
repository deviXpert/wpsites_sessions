/**
 * Perf: the QupHealth check-in widget (HFCM snippet #1) loads my-widget.js,
 * 1.3 MB served uncompressed, on page load. It costs ~6 s of mobile CPU and
 * pulls reCAPTCHA twice before anyone taps "Check-In Now". Load it on the
 * visitor's first scroll, tap, key press or mouse move instead. A tap on a
 * check-in button before the widget is ready is remembered (on pointerup,
 * because WP Rocket's delay-JS swallows that first click), and the widget's
 * own button is clicked for the visitor once it has rendered.
 *
 * The site's styling for the widget button lives in Additional CSS, but WP
 * Rocket's Remove Unused CSS drops it once the widget no longer renders during
 * its crawl, and the button falls back to QupHealth's uppercase red. Those
 * rules (copied from Additional CSS) are added back by script just before the
 * widget loads, so RUCSS never sees them.
 *
 * Until the widget renders, the mobile header shows Elementor's plain-text
 * "Check-in Now" placeholder (header widget 7ab4001). It is styled like the
 * widget's red button from a head script, so the header looks the same as
 * before and nothing shifts when the widget swaps its button in.
 */
function eer_qup_css() {
	return 'button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.health-widget-container.css-p55m0s{background-color:#dc271d;padding:12px 25px;width:auto!important;border-radius:8px;box-shadow:unset}.css-e5fs27{font-family:Satoshi!important;font-size:clamp(14px, 4vw, 20px)!important;font-weight:500!important;text-transform:capitalize}@media(max-width:768px){button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.health-widget-container.css-p55m0s{padding:9px 10px;width:100%!important;border-radius:7px}.css-e5fs27{font-size:15px!important}}';
}
function eer_qup_placeholder_css() {
	return '.elementor-element-7ab4001.widget-root .elementor-icon-list-items{background-color:#dc271d;border-radius:7px;padding:9px 10px!important;min-width:117px;box-sizing:border-box;justify-content:center}.elementor-element-7ab4001.widget-root .elementor-icon-list-item>.elementor-icon-list-text{color:#fff!important;font-size:15px!important;line-height:22.5px!important;text-transform:capitalize}';
}
function eer_qup_delay( $html ) {
	if ( false === strpos( $html, 'checkin.quphealth.com/static/js/my-widget.js' ) ) {
		return $html;
	}
	$head = '<script nowprocket data-nowprocket>(function(){var st=document.createElement("style");st.id="eer-qup-placeholder";st.textContent=' . wp_json_encode( eer_qup_placeholder_css() ) . ';document.head.appendChild(st);})();</script>';
	$pos  = stripos( $html, '</head>' );
	if ( false !== $pos ) {
		$html = substr_replace( $html, $head, $pos, 0 );
	}
	return preg_replace_callback(
		'/<script\b[^>]*\bsrc=(["\'])(https:\/\/checkin\.quphealth\.com\/static\/js\/my-widget\.js[^"\']*)\1[^>]*><\/script>/i',
		function ( $m ) {
			$src = wp_json_encode( $m[2] );
			return '<script nowprocket data-nowprocket>(function(){var src=' . $src . ',done=false,evs=["scroll","pointerdown","touchstart","keydown","mousemove","wheel"];'
				. 'function load(){if(done){return;}done=true;evs.forEach(function(e){window.removeEventListener(e,load,{passive:true});});var st=document.createElement("style");st.id="eer-qup-css";st.textContent=' . wp_json_encode( eer_qup_css() ) . ';document.head.appendChild(st);var s=document.createElement("script");s.src=src;s.async=true;document.head.appendChild(s);}'
				. 'evs.forEach(function(e){window.addEventListener(e,load,{passive:true});});'
				. 'function want(root){if(root.qupWant){return;}root.qupWant=1;load();root.style.cursor="progress";var n=0,t=setInterval(function(){var b=root.querySelector(".health-widget-container");if(b||++n>150){clearInterval(t);root.style.cursor="";if(b){b.click();}}},100);}'
				. 'function pending(e){var root=e.target.closest&&e.target.closest(".widget-root");return root&&!root.querySelector(".health-widget-container")?root:null;}'
				. 'var sx=0,sy=0;window.addEventListener("pointerdown",function(e){sx=e.clientX;sy=e.clientY;},{capture:true,passive:true});'
				. 'window.addEventListener("pointerup",function(e){var root=pending(e);if(root&&Math.abs(e.clientX-sx)<10&&Math.abs(e.clientY-sy)<10){want(root);}},{capture:true,passive:true});'
				. 'document.addEventListener("click",function(e){var root=pending(e);if(root){e.preventDefault();e.stopPropagation();want(root);}},true);'
				. '})();</script>';
		},
		$html,
		1
	);
}
add_action( 'template_redirect', function () {
	if ( is_admin() || wp_doing_ajax() || is_feed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return;
	}
	ob_start( 'eer_qup_delay' );
}, 0 );
