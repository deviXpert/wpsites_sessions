/**
 * Perf: the QupHealth check-in widget (HFCM snippet #2) loads my-widget.js,
 * 1.3 MB served uncompressed, on page load. It costs ~6 s of mobile CPU and
 * pulls reCAPTCHA twice before anyone taps "Check-In Now". Load it on the
 * visitor's first scroll, tap, key press or mouse move instead. A tap on a
 * check-in button before the widget is ready is remembered (on pointerup,
 * because WP Rocket's delay-JS swallows that first click), and the widget's
 * own button is clicked for the visitor once it has rendered.
 */
function stat_qup_delay( $html ) {
	if ( false === strpos( $html, 'checkin.quphealth.com/static/js/my-widget.js' ) ) {
		return $html;
	}
	return preg_replace_callback(
		'/<script\b[^>]*\bsrc=(["\'])(https:\/\/checkin\.quphealth\.com\/static\/js\/my-widget\.js[^"\']*)\1[^>]*><\/script>/i',
		function ( $m ) {
			$src = wp_json_encode( $m[2] );
			return '<script nowprocket data-nowprocket>(function(){var src=' . $src . ',done=false,evs=["scroll","pointerdown","touchstart","keydown","mousemove","wheel"];'
				. 'function load(){if(done){return;}done=true;evs.forEach(function(e){window.removeEventListener(e,load,{passive:true});});var s=document.createElement("script");s.src=src;s.async=true;document.head.appendChild(s);}'
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
	ob_start( 'stat_qup_delay' );
}, 0 );
