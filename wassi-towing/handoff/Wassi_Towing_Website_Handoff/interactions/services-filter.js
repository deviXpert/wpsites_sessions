/* Services hub filter tabs.
   - Tab buttons: attribute data-wt-filter="all|emergency|towing|quick|planned" (wrap them in a container with role="tablist").
   - Each service card (Elementor Container/Loop item): attribute data-wt-cats="towing emergency" (space-separated).
   Categories per service are listed in CLAUDE.md. */
(function(){
  var tabs=document.querySelectorAll("[data-wt-filter]"), cards=document.querySelectorAll("[data-wt-cats]");
  if(!tabs.length) return;
  function apply(f){
    tabs.forEach(function(t){ t.setAttribute("aria-pressed", String(t.dataset.wtFilter===f)); });
    cards.forEach(function(c){ c.hidden = !(f==="all" || (" "+c.dataset.wtCats+" ").indexOf(" "+f+" ")>-1); });
  }
  tabs.forEach(function(t){ t.addEventListener("click",function(){ apply(t.dataset.wtFilter); }); });
  apply("all");
})();
