/* Wassi Towing: Stranded mode (from interactions/stranded-mode.js) + keyboard support for checklist.
   Install: Elementor > Custom Code > Add new, location "</body> - End", all pages. */
/* Wassi "Stranded mode": full-screen, high-contrast emergency overlay.
   Elementor setup:
   - Build the overlay as a Container with CSS ID "wt-stranded" and CSS class "wt-stranded" (content: see design/html/home--state-stranded-mode.html).
   - Any button/link with attribute data-wt-stranded="open" opens it (header strip button, hero button). data-wt-stranded="close" closes it.
   - Checklist items: buttons with class "wt-check" inside the overlay.
   - "Text my exact location" link: give it attribute data-wt-sms-location.
   Enqueue in the footer (child theme functions.php or a code-snippets plugin). */
(function(){
  var SMS = "+10000000000"; // [SMS NUMBER]
  var css = ".wt-stranded{position:fixed;inset:0;z-index:99999;overflow:auto;background:#0B1424;display:none}" +
            ".wt-stranded.is-open{display:block}body.wt-no-scroll{overflow:hidden}" +
            ".wt-check[aria-pressed=true]{color:#8FA0B8}.wt-check[aria-pressed=true] .wt-box{background:#FF6B00;border-color:#FF6B00}";
  var st=document.createElement("style"); st.textContent=css; document.head.appendChild(st);
  var ov=document.getElementById("wt-stranded"); if(!ov) return;
  var last=null;
  function track(e,p){ (window.dataLayer=window.dataLayer||[]).push(Object.assign({event:e},p||{})); }
  function open(){ last=document.activeElement; ov.classList.add("is-open"); ov.setAttribute("role","dialog"); ov.setAttribute("aria-modal","true");
    ov.setAttribute("aria-label","Stranded mode"); document.body.classList.add("wt-no-scroll"); var f=ov.querySelector("a,button"); if(f) f.focus(); track("wt_stranded_open"); }
  function close(){ ov.classList.remove("is-open"); document.body.classList.remove("wt-no-scroll"); if(last) last.focus(); }
  document.addEventListener("click",function(e){
    var t=e.target.closest("[data-wt-stranded]"); if(t){ e.preventDefault(); t.dataset.wtStranded==="close"?close():open(); }
    var c=e.target.closest(".wt-check"); if(c){ c.setAttribute("aria-pressed", String(c.getAttribute("aria-pressed")!=="true")); }
    var s=e.target.closest("[data-wt-sms-location]"); if(s && navigator.geolocation){ e.preventDefault();
      navigator.geolocation.getCurrentPosition(function(p){
        var body="I need help. My location: https://maps.google.com/?q="+p.coords.latitude.toFixed(5)+","+p.coords.longitude.toFixed(5);
        track("wt_sms_click",{source:"stranded"}); window.location.href="sms:"+SMS+"?&body="+encodeURIComponent(body);
      }, function(){ window.location.href="sms:"+SMS; }, {enableHighAccuracy:true,timeout:8000}); }
    if(e.target.closest('a[href^="tel:"]')) track("wt_call_click",{source: ov.contains(e.target)?"stranded":"page"});
  });
  document.addEventListener("keydown",function(e){ if(e.key==="Escape" && ov.classList.contains("is-open")) close(); });
  ov.querySelectorAll(".wt-check").forEach(function(b){ if(!b.hasAttribute("aria-pressed")) b.setAttribute("aria-pressed","false"); });
})();
(function(){
  document.addEventListener("keydown",function(e){
    var c=e.target.closest&&e.target.closest(".wt-check");
    if(c&&(e.key==="Enter"||e.key===" ")){e.preventDefault();c.click();}
  });
})();
