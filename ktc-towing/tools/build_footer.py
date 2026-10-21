"""Enhanced site-wide footer (template 3713) from wp-backup/tpl-3713.json -> built_footer.json."""
import json, random

random.seed("ktc-footer")
data = json.loads(json.load(open("wp-backup/tpl-3713.json"))["meta"]["_elementor_data"])
idx = {}
def index(els):
    for e in els:
        idx[e["id"]] = e
        index(e.get("elements", []))
index(data)
S = lambda i: idx[i]["settings"]
def nid():
    while True:
        i = "%07x" % random.getrandbits(28)
        if i not in idx:
            idx[i] = None
            return i
LINK = lambda u: {"url": u, "is_external": "", "nofollow": "", "custom_attributes": ""}

# CTA card: bold orange instead of the muddy brown photo gradient
cta = S("cb02ac9")
cta["css_classes"] = "cta-container ktc-fcta"
cta.update({"background_color": "#FFA300", "background_color_b": "#FF7A00", "background_color_stop": {"unit": "%", "size": 0, "sizes": []},
            "background_color_b_stop": {"unit": "%", "size": 100, "sizes": []}, "border_color": "#FFFFFF00"})
S("50648d7")["header_size"] = "h2"  # it already rendered as h2 (default); keep explicit

# Brand row: logo + text left, trust badges right (fills the empty half)
brand = idx["aae4949"]
logo, title, text = brand["elements"]
S("c3f7ea4")["_element_custom_width"] = {"unit": "px", "size": 150}
S("c3f7ea4")["_element_custom_width_mobile"] = {"unit": "px", "size": 120}
S("503bb17")["typography_font_size"] = {"unit": "px", "size": 28, "sizes": []}
badges = {"id": nid(), "elType": "widget", "widgetType": "icon-list", "elements": [], "settings": {
    "_css_classes": "ktc-badges", "view": "inline",
    "icon_list": [{"_id": nid(), "text": t, "selected_icon": {"value": ic, "library": "fa-solid"}} for t, ic in (
        ("24/7 Dispatch, 365 Days", "fas fa-clock"), ("Licensed & Insured", "fas fa-shield-alt"),
        ("Upfront Quote Before Dispatch", "fas fa-file-invoice-dollar"), ("Authorized Impound Recovery Partner", "fas fa-check-circle"))]}}
call_big = {"id": nid(), "elType": "widget", "widgetType": "html", "elements": [], "settings": {"html":
    '<a class="ktc-fcall" href="tel:+15874350770"><span class="ktc-fcall__lbl">Call dispatch 24/7</span>'
    '<span class="ktc-fcall__num">(587) 435-0770</span></a>'}}
brand["elements"] = [
    {"id": nid(), "elType": "container", "isInner": True, "elements": [logo, title, text],
     "settings": {"content_width": "full", "flex_direction": "column", "width": {"unit": "%", "size": 55, "sizes": []},
                  "width_tablet": {"unit": "%", "size": 100, "sizes": []}, "flex_gap": {"column": "14", "row": "14", "isLinked": True, "unit": "px", "size": 14}}},
    {"id": nid(), "elType": "container", "isInner": True, "elements": [call_big, badges],
     "settings": {"content_width": "full", "flex_direction": "column", "flex_justify_content": "center",
                  "width": {"unit": "%", "size": 45, "sizes": []}, "width_tablet": {"unit": "%", "size": 100, "sizes": []},
                  "flex_gap": {"column": "18", "row": "18", "isLinked": True, "unit": "px", "size": 18}}},
]
bs = S("aae4949")
bs.update({"flex_direction": "row", "flex_direction_tablet": "column", "flex_align_items": "center", "css_classes": "ktc-fbrand",
           "boxed_width": {"unit": "px", "size": 1240, "sizes": []},
           "flex_gap": {"column": "40", "row": "30", "isLinked": False, "unit": "px", "size": 40},
           "padding": {"unit": "px", "top": "140", "right": "20", "bottom": "40", "left": "20", "isLinked": False}})

# Link columns
S("df00284")["icon_list"] = [
    {"_id": nid(), "text": t, "link": LINK(u), "selected_icon": {"value": "fas fa-angle-right", "library": "fa-solid"}}
    for t, u in (("About Us", "https://ktctowing.ca/about-us/"), ("Services", "https://ktctowing.ca/services/"),
                 ("Blog", "https://ktctowing.ca/blogs/"), ("Contact Us", "https://ktctowing.ca/contact-us/"))]
for it in S("d67f917")["social_icon_list"]:
    u = it.get("link", {}).get("url", "")
    if u.startswith("maps.google.com"):  # was a relative (broken) link
        it["link"]["url"] = "https://" + u
S("d67f917")["align"] = "left"
S("d67f917")["_css_classes"] = "ktc-social"
for c in ("733e966",):
    S(c)["css_classes"] = "ktc-fnews"
S("3045c89")["css_classes"] = "ktc-fcols"
S("3045c89")["boxed_width"] = {"unit": "px", "size": 1240, "sizes": []}
for h in ("a7b183c", "9944878", "a5a5ba7"):
    S(h)["_css_classes"] = "ktc-fhead"
S("9944878")["title"] = "Our Services"

# Giant wordmark: outlined + gradient instead of flat white
S("0896f11")["_css_classes"] = "ktc-wordmark"
S("36ef24e")["editor"] = "<p>Copyright © 2026 KTC Towing. All Rights Reserved.</p>"

CSS = """<style>
.ktc-fcta{border:0!important;box-shadow:0 30px 60px rgba(255,122,0,.35)!important;overflow:hidden;position:relative}
.ktc-fcta:after{content:"";position:absolute;right:-80px;bottom:-120px;width:360px;height:360px;border-radius:50%;
  background:rgba(255,255,255,.14);pointer-events:none}
.ktc-fcta .elementor-heading-title,.ktc-fcta .elementor-heading-title span,.ktc-fcta p{color:#111!important}
.ktc-fcta .elementor-widget-heading:first-child .elementor-heading-title{display:inline-block;background:#111;color:#FFA300!important;
  border-radius:50px;padding:6px 14px;font-size:13px!important;letter-spacing:1px}
.ktc-fcta .elementor-button{box-shadow:0 10px 24px rgba(0,0,0,.18)}
.ktc-fcta .elementor-widget-global:first-of-type .elementor-button,.ktc-fcta .elementor-widget-button:first-of-type .elementor-button{background:#111!important;color:#fff!important}
.ktc-fbrand .elementor-heading-title{line-height:1.25!important}
.ktc-fcall{display:block;background:linear-gradient(135deg,#1b1b1b,#0c0c0c);border:1px solid rgba(255,163,0,.45);border-radius:18px;
  padding:22px 26px;text-decoration:none;transition:transform .25s,box-shadow .25s}
.ktc-fcall:hover{transform:translateY(-3px);box-shadow:0 16px 40px rgba(255,163,0,.2)}
.ktc-fcall__lbl{display:block;color:rgba(255,255,255,.7);font-size:14px;text-transform:uppercase;letter-spacing:1.2px}
.ktc-fcall__num{display:block;color:#FFA300;font-size:34px;font-weight:800;line-height:1.2}
.ktc-badges .elementor-icon-list-items{display:flex;flex-wrap:wrap;gap:10px}
.ktc-badges .elementor-icon-list-item{margin:0!important;padding:9px 14px!important;border:1px solid rgba(255,255,255,.18);border-radius:50px;
  background:rgba(255,255,255,.04)}
.ktc-badges .elementor-icon-list-item:after{display:none!important}
.ktc-badges .elementor-icon-list-text{color:#fff!important;font-size:13.5px}
.ktc-badges .elementor-icon-list-icon svg{fill:#FFA300!important;width:14px}
.ktc-fcols{border-top:1px solid rgba(255,255,255,.12)}
.ktc-fhead .elementor-heading-title{position:relative;padding-bottom:10px}
.ktc-fhead .elementor-heading-title:after{content:"";position:absolute;left:0;bottom:0;width:34px;height:3px;border-radius:3px;background:#FFA300}
.ktc-fcols .elementor-icon-list-item a{transition:padding-left .2s,color .2s}
.ktc-fcols .elementor-icon-list-item a:hover{padding-left:4px}
.ktc-fnews{border-color:rgba(255,163,0,.5)!important;background:linear-gradient(160deg,#1c1c1c,#121212)!important}
.ktc-social .elementor-social-icons-wrapper{display:flex!important;gap:10px;justify-content:flex-start}
.ktc-social .elementor-grid-item{margin:0!important}
.ktc-wordmark .elementor-heading-title{background:linear-gradient(180deg,rgba(255,255,255,.95) 0%,rgba(255,163,0,.85) 55%,rgba(255,163,0,.1) 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent!important;letter-spacing:-2px}
@media (max-width:767px){
  .ktc-fcall__num{font-size:28px}
  .ktc-badges .elementor-icon-list-item{padding:8px 12px!important}
  .ktc-badges .elementor-icon-list-text{font-size:12.5px}
  .ktc-fcols .elementor-icon-list-item{padding:4px 0}
}
</style>"""
data[-1]["elements"].append({"id": nid(), "elType": "widget", "widgetType": "html", "elements": [],
                             "settings": {"html": CSS, "_position": "absolute", "_element_width": "initial",
                                          "_element_custom_width": {"unit": "px", "size": 0, "sizes": []}}})
json.dump(data, open("built_footer.json", "w"))
print("footer built")
