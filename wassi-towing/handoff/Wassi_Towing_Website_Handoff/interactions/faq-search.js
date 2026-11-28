/* FAQ search + category chips for Elementor's (nested) Accordion widget.
   - Search input: id="wt-faq-search".
   - Category chips: buttons with data-wt-faq-cat="All|Pricing and payment|Arrival and timing|Your vehicle|Accidents and insurance|Safety while you wait".
   - Each FAQ group: a Container with data-wt-faq-group="<category name>" holding one Accordion.
   - Empty-state message element: id="wt-faq-empty" (hidden by default).
   Works with .e-n-accordion-item (nested accordion) and falls back to <details>. */
(function(){
  var input=document.getElementById("wt-faq-search"); if(!input) return;
  var chips=document.querySelectorAll("[data-wt-faq-cat]"), groups=document.querySelectorAll("[data-wt-faq-group]"), empty=document.getElementById("wt-faq-empty");
  var cat="All";
  function items(g){ return g.querySelectorAll(".e-n-accordion-item, details"); }
  function apply(){
    var q=input.value.trim().toLowerCase(), any=false;
    groups.forEach(function(g){
      var shown=0, catOk = cat==="All" || g.dataset.wtFaqGroup===cat;
      items(g).forEach(function(it){
        var ok = catOk && (!q || it.textContent.toLowerCase().indexOf(q)>-1);
        it.hidden=!ok; if(ok){ shown++; if(q.length>1) it.setAttribute("open",""); }
      });
      g.hidden = shown===0; if(shown) any=true;
    });
    if(empty) empty.hidden=any;
  }
  input.addEventListener("input",apply);
  chips.forEach(function(c){ c.addEventListener("click",function(){ cat=c.dataset.wtFaqCat;
    chips.forEach(function(x){ x.setAttribute("aria-pressed", String(x===c)); }); apply(); }); });
})();
