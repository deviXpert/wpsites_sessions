"""Build the SEO-optimised KTC home page Elementor data from the backup.

Reads wp-backup/page-1729.json (original), writes built_home.json.
Changes: de-duplicated headings/content, mobile-visible areas, heading
hierarchy, new sections from KTC_Towing_Homepage_Content_Final_Order.docx,
section order from that doc.
"""
import json, copy, random, re

random.seed("ktc-home")
SRC = json.load(open("wp-backup/page-1729.json"))
data = json.loads(SRC["meta"]["_elementor_data"])
idx = {}
def index(els):
    for e in els:
        idx[e["id"]] = e
        index(e.get("elements", []))
index(data)

def nid():
    while True:
        i = "%07x" % random.getrandbits(28)
        if i not in idx:
            idx[i] = None
            return i

def clone(el):
    c = copy.deepcopy(el)
    def re_id(e):
        e["id"] = nid()
        for k in e.get("elements", []): re_id(k)
    re_id(c)
    return c

S = lambda i: idx[i]["settings"]
TEL = {"url": "tel:+15874350770", "is_external": "", "nofollow": "", "custom_attributes": ""}
FONT = "Generel Sans"

# ---------- generic builders (styled like the existing page) ----------
def eyebrow(text, align="center"):
    e = clone(idx["bc088c7"]); e["settings"]["title"] = text; e["settings"]["align"] = align; return e

def h2(text, align="center"):
    e = clone(idx["c04edba"]); e["settings"]["title"] = text; e["settings"]["align"] = align
    e["settings"].pop("header_size", None)  # default h2
    if align == "start":
        for k in ("_element_width", "_element_custom_width"): e["settings"].pop(k, None)
        e["settings"]["_flex_align_self"] = "flex-start"
    return e

def para(html, align="center", width=760):
    e = clone(idx["9bb2e12"]); s = e["settings"]
    s["editor"] = html; s["align"] = align
    if width: s["_element_custom_width"] = {"unit": "px", "size": width, "sizes": []}; s["_element_custom_width_tablet"] = {"unit": "%", "size": 100, "sizes": []}; s["_element_custom_width_mobile"] = {"unit": "%", "size": 100, "sizes": []}
    else:
        for k in ("_element_width", "_element_custom_width", "_element_custom_width_tablet", "_flex_align_self"): s.pop(k, None)
    s["_margin"] = {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "0", "isLinked": False}
    return e

def call_btn(text="Call Now: (587) 435-0770", width=None, align="center"):
    e = clone(idx["0f4641c"]); s = e["settings"]; s["text"] = text; s["link"] = dict(TEL)
    s["_flex_align_self"] = align; s["_flex_align_self_mobile"] = align
    if width: s["_element_custom_width"] = {"unit": "px", "size": width, "sizes": []}; s["_element_custom_width_mobile"] = {"unit": "%", "size": 100, "sizes": []}
    return e

def card(icon, title, desc, title_tag="h3", link=None):
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "title_text": title, "description_text": desc, "title_size": title_tag,
        "position": "top", "text_align": "start",
        "icon_size": {"unit": "px", "size": 22, "sizes": []},
        "icon_padding": {"unit": "px", "size": 14, "sizes": []},
        "view": "stacked", "shape": "rounded",
        "primary_color": "#FFF4DD",
        "secondary_color": "#000000",
        "__globals__": {"secondary_color": "globals/colors?id=primary", "title_color": "globals/colors?id=secondary"},
        "icon_space": {"unit": "px", "size": 16, "sizes": []},
        "title_bottom_space": {"unit": "px", "size": 8, "sizes": []},
        "title_typography_typography": "custom", "title_typography_font_family": FONT,
        "title_typography_font_size": {"unit": "px", "size": 19, "sizes": []},
        "title_typography_font_weight": "700", "title_typography_line_height": {"unit": "em", "size": 1.3, "sizes": []},
        "description_typography_typography": "custom", "description_typography_font_family": FONT,
        "description_typography_font_size": {"unit": "px", "size": 15, "sizes": []},
        "description_typography_line_height": {"unit": "em", "size": 1.6, "sizes": []},
        "description_color": "#4A4A4A",
        "_background_background": "classic", "_background_color": "#FFFFFF",
        "_border_border": "solid", "_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
        "_border_color": "#0000001A",
        "_border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True},
        "_padding": {"unit": "px", "top": "26", "right": "24", "bottom": "26", "left": "24", "isLinked": False},
        "_element_width": "", "_flex_size": "",
    }
    if link: s["link"] = {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""}
    return {"id": nid(), "elType": "widget", "settings": s, "elements": [], "widgetType": "icon-box"}

def grid(children, cols=4, cols_tab=2):
    return {"id": nid(), "elType": "container", "isInner": True, "elements": children, "settings": {
        "container_type": "grid", "content_width": "full",
        "grid_columns_grid": {"unit": "fr", "size": cols, "sizes": []},
        "grid_columns_grid_tablet": {"unit": "fr", "size": cols_tab, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": 1, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 1, "sizes": []},
        "grid_auto_flow": "row",
        "grid_gaps": {"column": "20", "row": "20", "isLinked": True, "unit": "px"},
        "margin": {"unit": "px", "top": "30", "right": "0", "bottom": "10", "left": "0", "isLinked": False},
    }}

def section(children, bg="#FFFFFF", width=1240):
    return {"id": nid(), "elType": "container", "isInner": False, "elements": children, "settings": {
        "flex_direction": "column", "flex_align_items": "center", "boxed_width": {"unit": "px", "size": width, "sizes": []},
        "flex_gap": {"column": "10", "row": "10", "isLinked": True, "unit": "px", "size": 10},
        "background_background": "classic", "background_color": bg,
        "padding": {"unit": "px", "top": "90", "right": "20", "bottom": "90", "left": "20", "isLinked": False},
        "padding_tablet": {"unit": "px", "top": "60", "right": "20", "bottom": "60", "left": "20", "isLinked": False},
        "padding_mobile": {"unit": "px", "top": "50", "right": "20", "bottom": "50", "left": "20", "isLinked": False},
        "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
    }}

# ===================== 1. fixes to existing content =====================
# Hero form note: "Unsubscribe anytime" is meaningless on a tow-quote form.
S("7befa62")["title"] = "Available 24/7, including holidays. Upfront quote before dispatch."

# About: big eyebrow-styled "About KTC Towing" is not a heading; doc H2 = "Calgary Towing Done Right".
S("1876f8c")["header_size"] = "p"
S("f3bdde0")["header_size"] = "h2"

# Towing Calgary main keyword section: one H2 with the full doc heading.
S("431309a")["header_size"] = "h2"
S("431309a")["title"] = "Towing <span>Calgary</span>: Fast Tow Truck Service Across the Whole City"
S("431309a")["typography_font_size"] = {"unit": "custom", "size": "clamp(28px, 3vw, 40px)", "sizes": []}
idx["6b09d59"]["elements"] = [e for e in idx["6b09d59"]["elements"] if e["id"] != "5a92880"]
idx["6b09d59"]["elements"].append(call_btn("Call for a Tow Truck in Calgary: (587) 435-0770", width=480, align="flex-start"))

# Services heading per doc.
S("c04edba")["title"] = "Towing and Roadside Services in Calgary"

# Flip boxes: back side repeated the front title as a second <h3> (32 headings for 16 services).
# Keep the title once (front, h3); back side shows description + button only.
for fb in [e for e in idx.values() if e and e.get("widgetType") == "flip-box"]:
    s = fb["settings"]
    s["title_text_a"] = s["title_text_a"].strip()
    s["title_text_b"] = ""
    if not s.get("link", {}).get("url"):
        # Condo & Parkade card had a dead "Explore Service" button; send it to the closest real page.
        s["link"] = {"url": "https://ktctowing.ca/underground-parkade-towing-calgary/", "is_external": "", "nofollow": "", "custom_attributes": ""}

# "Why the right truck" cards duplicated the service-card headings word for word.
for i, t in (("7fbbcb9", "Flatbed Tow Trucks"), ("b69e5b9", "Wheel-Lift Tow Trucks"),
             ("595b8f7", "Winch &amp; Recovery Gear"), ("b4ae591", "Heavy-Duty Tow Trucks")):
    S(i)["title_text"] = t
S("2922b34")["title"] = S("2922b34")["title"].replace("Why The Right Truck", "Why The Right Tow Truck")

# Service areas: card was hidden on tablet + mobile (desktop-only content). Show it everywhere.
for k in ("hide_mobile", "hide_tablet"): S("1573c35").pop(k, None)
S("1573c35")["width_mobile"] = {"unit": "%", "size": 100, "sizes": []}
S("1573c35")["min_height_mobile"] = {"unit": "px", "size": 0, "sizes": []}
S("cc7e129")["title"] = "Calgary &amp; Surrounding Areas"
S("8fcc16d")["title_text"] = "Towing Across Calgary and Surrounding Areas"
S("8fcc16d")["title_size"] = "h2"
S("8fcc16d")["title_typography_font_size"] = {"unit": "px", "size": 34, "sizes": []}
S("8fcc16d")["title_typography_font_size_mobile"] = {"unit": "px", "size": 24, "sizes": []}
S("8fcc16d")["description_text"] = "We dispatch from Calgary to all four quadrants, 24 hours a day. Wherever you're stranded, from downtown gridlock to an icy back road, the nearest available truck comes straight to you."
S("e700e38")["min_height_mobile"] = {"unit": "px", "size": 0, "sizes": []}
S("e700e38")["background_size_mobile"] = "cover"
S("da66e82")["description_text"] = "Falconridge, Martindale, Saddle Ridge, Marlborough, Skyview, near the airport"
S("65fe968")["description_text"] = "McKenzie Towne, Forest Lawn, Seton, Douglasdale, Inglewood"
S("7882c1e")["description_text"] = "Signal Hill, Mount Royal, Glenmore, Bridgeland, Beltline"
S("260fdcb")["description_text"] = ("Chestermere, Airdrie, Cochrane, Okotoks and High River, plus long-distance towing across Alberta. "
                                     "Not sure we cover your spot? <a href=\"tel:+15874350770\">Call us</a> and we will confirm.")

# Second marquee repeated the first one word for word -> show service areas instead.
def marquee_fix(html, items=None):
    # top-level `const track` in two <script>s = SyntaxError in the second one; scope it.
    html = re.sub(r"<script>.*?</script>", """<script>
(function(){
  document.querySelectorAll('.opal-roll-track').forEach(function(track){
    function adjustSpeed(){ track.style.animationDuration = window.innerWidth < 768 ? "25s" : "35s"; }
    adjustSpeed(); window.addEventListener('resize', adjustSpeed);
  });
})();
</script>""", html, flags=re.S)
    if items:
        spans = "\n".join(f'      <span>{t} <a href="tel:+15874350770" class="call-pill">Call Now! (587) 435-0770</a></span>' for t in items)
        html = re.sub(r'(<div class="opal-roll-content">).*?(\n    </div>)', lambda m: m.group(1) + "\n" + spans + m.group(2), html, count=1, flags=re.S)
    return html
S("a948605")["html"] = marquee_fix(S("a948605")["html"])
S("a274611")["html"] = marquee_fix(S("a274611")["html"], [
    "Towing NE Calgary", "Towing NW Calgary", "Towing SE Calgary", "Towing SW Calgary",
    "Airdrie", "Chestermere", "Cochrane", "Okotoks", "High River"])
# script is identical in both; only the first needs it
S("a274611")["html"] = re.sub(r"<script>.*?</script>", "", S("a274611")["html"], flags=re.S)

# FAQ: doc heading + 2 missing questions (Elementor builds FAQPage schema from these items).
S("9cb21cb")["title"] = "Towing Calgary: Frequently Asked Questions"
acc = idx["ed0808e"]
new_faq = [
    ("Do I need a flatbed for my AWD car?",
     "<p>Usually yes. AWD and 4x4 drivetrains can be damaged when only some wheels roll, so a flatbed is the safer choice. Mention your vehicle when you call.</p>"),
    ("Can you tow from an underground parkade?",
     "<p>Yes. We use low-profile equipment and trained operators for underground and multi-level parkades.</p>"),
]
tpl = acc["elements"][0]
for q, a in new_faq:
    c = clone(tpl); c["settings"]["_title"] = q; c["elements"][0]["settings"]["editor"] = a
    acc["elements"].insert(6, c)
    acc["settings"]["items"].insert(6, {"item_title": q, "_id": nid()})

# ===================== 2. new sections from the doc =====================
how = section([
    eyebrow("How It Works"),
    h2("How to Get a Tow in Calgary in 4 Steps"),
    grid([
        card("fas fa-phone-alt", "1. Call or WhatsApp", "Call or WhatsApp <a href=\"tel:+15874350770\">(587) 435-0770</a> and share your location.", "h3"),
        card("fas fa-car-crash", "2. Describe the Vehicle", "Tell us the vehicle and what happened, so we send the right truck.", "h3"),
        card("fas fa-file-invoice-dollar", "3. Get Your Quote and ETA", "You get your price and arrival time before the truck is dispatched.", "h3"),
        card("fas fa-truck-pickup", "4. We Arrive and Deliver", "We arrive, load your vehicle and deliver it to your chosen destination.", "h3"),
    ]),
], bg="#F8F8F8")

price = section([
    eyebrow("Pricing"),
    h2("How Much Does Towing Cost in Calgary?"),
    para("<p>Light-duty tows within Calgary start at $50. The final price depends on:</p>"),
    grid([
        card("fas fa-route", "Distance", "How far your vehicle is going.", "div"),
        card("fas fa-truck-monster", "Vehicle Type and Size", "Car, SUV, truck, motorcycle or RV.", "div"),
        card("fas fa-cloud-moon", "Time of Day and Weather", "Night calls and storm conditions can affect the price.", "div"),
        card("fas fa-tools", "Special Needs", "Winching, parkade access or flatbed loading.", "div"),
    ]),
    para("<p>We quote you before the truck is dispatched. Long-distance tows are flat-rate, and impound and daily storage fees are charged separately by the impound lot.</p>"),
    call_btn(width=260),
], bg="#FFFFFF")

situ = section([
    eyebrow("Towing Calgary by Situation"),
    h2("Need Towing in Calgary? Here Is Who to Call and What to Do"),
    grid([
        card("fas fa-road", "My car broke down on a Calgary highway",
             "Move to the shoulder if you can, turn on your hazards, and stay buckled in if traffic is heavy. Call KTC at (587) 435-0770 and tell us the highway, direction and nearest exit or cross street. We send the nearest truck and confirm your arrival time.", "h3", "https://ktctowing.ca/emergency-towing/"),
        card("fas fa-car-crash", "I was in an accident in Calgary",
             "Check that everyone is safe and call 911 if anyone is hurt. Once the scene is safe, we handle accident towing in Calgary to the body shop or storage yard you or your insurer choose.", "h3", "https://ktctowing.ca/accident-recovery/"),
        card("fas fa-car-battery", "My car will not start in the cold",
             "Calgary winters drain batteries quickly. We can usually jump start the vehicle on the spot. If it still will not start, we tow it to a shop of your choice.", "h3", "https://ktctowing.ca/battery-boost-jump-start/"),
        card("fas fa-snowflake", "My vehicle is stuck in snow or a ditch",
             "Do not keep spinning the wheels. Call us for winch-out and recovery, and we pull the vehicle out without causing extra damage.", "h3", "https://ktctowing.ca/winch-out-recovery/"),
        card("fas fa-warehouse", "My car was towed to the impound lot",
             "Gather your photo ID, proof of ownership and insurance, and confirm the lot's fees and hours. After it is released, KTC transports your vehicle wherever it needs to go.", "h3", "https://ktctowing.ca/impound-lot-recovery-calgary/"),
        card("fas fa-wrench", "I need a tow to my mechanic or dealership",
             "Give us the shop address and tell us if your car is AWD, lowered or damaged. We send a flatbed or wheel-lift truck to match.", "h3", "https://ktctowing.ca/flatbed-towing-calgary/"),
        card("fas fa-key", "I am locked out or out of fuel",
             "We come to you with lockout tools or fuel delivery so you can keep driving, with no tow needed.", "h3", "https://ktctowing.ca/roadside-assistance/"),
        {"id": nid(), "elType": "widget", "widgetType": "html", "elements": [], "settings": {"_css_classes": "ktc-sit-cta-w", "html":
            '<div class="ktc-sit-cta"><p class="ktc-sit-cta__t">Not sure which service you need?</p>'
            '<p class="ktc-sit-cta__d">Describe what happened. Our Calgary dispatcher will tell you the right fix and the right truck.</p>'
            '<a class="ktc-sit-cta__b" href="tel:+15874350770">Call (587) 435-0770</a></div>'}},
    ], cols=4, cols_tab=2),
], bg="#F8F8F8")

# Winter: clone the About layout (image + text), image on the right.
winter = clone(idx["c0c4479"])
winter["settings"]["flex_direction"] = "row-reverse"
winter["settings"]["flex_direction_mobile"] = "column"
winter["settings"]["margin"] = {"unit": "px", "top": "90", "right": "0", "bottom": "90", "left": "0", "isLinked": False}
w_img_col, w_txt_col = winter["elements"]
img = w_img_col["elements"][0]["settings"]
img["image"] = {"url": "https://ktctowing.ca/wp-content/uploads/2025/05/IMG-20250414-WA0053.jpg", "id": 969, "size": "", "alt": "", "source": "library"}
w_txt_col["elements"] = [
    eyebrow("Calgary Winter Towing", "start"),
    h2("Winter Towing in Calgary: What to Expect", "start"),
    para("<p>Calgary cold snaps drain batteries fast, and snow-packed streets and parking lots lead to slide-offs and stuck vehicles. In winter our most common calls are jump starts and winch-outs.</p>"
         "<p>If you are stuck: turn on your hazards, stay in the vehicle if you are on a busy road, and call us with your nearest cross streets. Keep a winter kit (blanket, jumper cables, phone charger) in your car.</p>"
         "<p>Read more: <a href=\"https://ktctowing.ca/what-to-do-if-youre-stuck-in-snow-in-calgary/\">What to Do If You Are Stuck in Snow in Calgary</a></p>", "start", None),
    call_btn(width=260, align="flex-start"),
]

# ===================== 2b. fleet section ("Why the right tow truck matters") styling =====================
fleet = idx["116cc96"]
fleet["settings"]["css_classes"] = "ktc-fleet"
fleet["settings"]["background_overlay_opacity"] = {"unit": "px", "size": 0.82, "sizes": []}
FLEET_CARDS = {  # card container -> (icon-box, number label, pill, icon)
    "9fd2c60": ("7fbbcb9", "0598369", "ac83084", None),  # flatbed keeps its big SVG tile
    "ac99c6c": ("b69e5b9", "29d77f1", "085d3cb", "fas fa-truck-pickup"),
    "d93bc5a": ("595b8f7", "5b1b780", "fe5df0f", "fas fa-link"),
    "781a9e9": ("b4ae591", "d4aab57", "9edb2f7", "fas fa-truck-moving"),
    "04bd782": ("59724ae", "b6a832c", "4cc466e", "fas fa-headset"),
}
for c, (box, num, pill, icon) in FLEET_CARDS.items():
    S(c)["css_classes"] = "ktc-fc"
    S(num)["_css_classes"] = "ktc-num"   # widgets use _css_classes, containers css_classes
    S(pill)["_css_classes"] = "ktc-pill"
    S(box)["_css_classes"] = "ktc-fbox"
    S(c)["min_height_mobile"] = {"unit": "px", "size": 0, "sizes": []}
    if icon:
        S(box).update({"selected_icon": {"value": icon, "library": "fa-solid"}, "position": "top", "position_mobile": "top",
                       "icon_size": {"unit": "px", "size": 20, "sizes": []}, "icon_space": {"unit": "px", "size": 14, "sizes": []}})
S("62b68e1")["css_classes"] = "ktc-tile"
S("c9239d0")["css_classes"] = "ktc-strip"
S("2922b34")["typography_font_size"] = {"unit": "custom", "size": "clamp(32px, 3.8vw, 52px)", "sizes": []}

FLEET_CSS = """<style>
.ktc-fleet .ktc-fc{background:rgba(18,18,20,.88)!important;border:1px solid rgba(255,255,255,.14)!important;
  transition:transform .3s ease,border-color .3s ease}
.ktc-fleet .ktc-fc:hover{transform:translateY(-4px);border-color:rgba(255,163,0,.7)!important}
.ktc-fleet .ktc-fc{display:flex!important;flex-direction:column}
.ktc-fleet .ktc-num .elementor-heading-title{color:#FFA300!important;font-size:12px!important;letter-spacing:1.2px;text-transform:uppercase}
.ktc-fleet .ktc-fbox{margin-bottom:16px!important}
.ktc-fleet .ktc-fbox .elementor-icon{border:1px solid rgba(255,163,0,.55);border-radius:10px;padding:9px;background:transparent}
.ktc-fleet .ktc-fbox .elementor-icon svg{fill:#FFA300!important;width:18px;height:18px}
.ktc-fleet .ktc-fbox .elementor-icon-box-title{font-size:20px!important}
.ktc-fleet .ktc-fbox .elementor-icon-box-description{color:rgba(255,255,255,.78)!important}
.ktc-fleet .ktc-pill{position:relative!important;left:auto!important;right:auto!important;bottom:auto!important;top:auto!important;
  width:auto!important;max-width:100%!important;margin-top:auto!important;align-self:flex-start}
.ktc-fleet .ktc-pill,.ktc-fleet .ktc-pill>.elementor-widget-container{background:rgba(255,163,0,.1)!important;
  border-color:rgba(255,163,0,.45)!important;border-radius:50px!important}
.ktc-fleet .ktc-pill .elementor-heading-title{color:#fff!important}
.ktc-fleet .ktc-pill .elementor-heading-title span{color:#FFA300!important}
.ktc-fleet .ktc-tile{border:1px solid rgba(255,163,0,.25);border-radius:15px}
@media (min-width:768px){.ktc-fleet .ktc-strip .elementor-widget-icon-box,.ktc-fleet .ktc-strip .elementor-widget-icon-box>.elementor-widget-container{border-bottom:0!important}}
@media (prefers-reduced-motion:reduce){.ktc-fleet .ktc-fc{transition:none}.ktc-fleet .ktc-fc:hover{transform:none}}
</style>"""
fleet["elements"].insert(0, {"id": nid(), "elType": "widget", "widgetType": "html", "elements": [],
                             "settings": {"html": FLEET_CSS, "_element_width": "initial",
                                          "_element_custom_width": {"unit": "px", "size": 0, "sizes": []},
                                          "_position": "absolute"}})

# ===================== 2c. FAQ: two-column layout, numbered question cards =====================
faq = idx["8427113"]
fs = faq["settings"]
fs.update({"css_classes": "ktc-faq", "flex_direction": "row", "flex_direction_tablet": "column", "flex_wrap": "nowrap",
           "flex_align_items": "flex-start", "flex_gap": {"column": "50", "row": "30", "isLinked": False, "unit": "px", "size": 50},
           "boxed_width": {"unit": "px", "size": 1240, "sizes": []},
           "padding": {"unit": "px", "top": "40", "right": "20", "bottom": "40", "left": "20", "isLinked": False}})
S("4453e2a")["align"] = "start"
S("9cb21cb")["align"] = "start"; S("9cb21cb")["align_tablet"] = "start"
S("ed0808e")["_margin"] = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
S("ed0808e")["_css_classes"] = "ktc-acc"
faq_intro = {"id": nid(), "elType": "container", "isInner": True, "elements": [
    idx["4453e2a"], idx["9cb21cb"],
    para("<p>Straight answers about towing costs, arrival times, impound recovery and the areas we cover. Still not sure? Our dispatcher picks up 24/7.</p>", "start", None),
    {"id": nid(), "elType": "widget", "widgetType": "html", "elements": [], "settings": {"html":
        '<div class="ktc-faq-card"><span class="ktc-faq-card__tag">24/7 Dispatch</span>'
        '<p class="ktc-faq-card__title">Talk to a real dispatcher now</p>'
        '<a class="ktc-faq-card__phone" href="tel:+15874350770">(587) 435-0770</a>'
        '<p class="ktc-faq-card__note">Quote and ETA before we dispatch. Average arrival about 20 minutes.</p>'
        '<a class="ktc-faq-card__wa" href="https://api.whatsapp.com/send/?phone=15874350770&amp;text=Hi+KTC+Towing%2C+I+need+help+with+my+vehicle.">Message us on WhatsApp</a></div>'}},
], "settings": {"content_width": "full", "flex_direction": "column", "width": {"unit": "%", "size": 38, "sizes": []},
                "width_tablet": {"unit": "%", "size": 100, "sizes": []}, "css_classes": "ktc-faq-intro",
                "flex_gap": {"column": "12", "row": "12", "isLinked": True, "unit": "px", "size": 12}}}
faq_list = {"id": nid(), "elType": "container", "isInner": True, "elements": [idx["ed0808e"]],
            "settings": {"content_width": "full", "flex_direction": "column", "width": {"unit": "%", "size": 62, "sizes": []},
                         "width_tablet": {"unit": "%", "size": 100, "sizes": []}}}
FAQ_CSS = """<style>
.ktc-faq{position:relative}
.ktc-faq-intro{position:sticky;top:110px;align-self:flex-start!important}
.ktc-faq,.ktc-faq>.e-con-inner{--align-items:flex-start;align-items:flex-start!important}
.ktc-faq-intro{--align-self:flex-start;--justify-content:flex-start;justify-content:flex-start!important}
.ktc-faq-card{margin-top:14px;background:#111;border-radius:18px;padding:28px;color:#fff;position:relative;overflow:hidden;
  box-shadow:0 20px 45px rgba(0,0,0,.18)}
.ktc-faq-card:before{content:"";position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,163,0,.45),rgba(255,163,0,0) 70%)}
.ktc-faq-card__tag{display:inline-block;background:#FFA300;color:#000;font-weight:700;font-size:12px;letter-spacing:1px;
  text-transform:uppercase;border-radius:50px;padding:5px 12px}
.ktc-faq-card__title{font-size:20px;font-weight:700;margin:14px 0 6px;color:#fff}
.ktc-faq-card a.ktc-faq-card__phone{display:block;font-size:32px!important;font-weight:800!important;color:#FFA300!important;letter-spacing:.5px;line-height:1.2;text-decoration:none}
.ktc-faq-card__note{font-size:14px;color:rgba(255,255,255,.75);margin:10px 0 18px}
.ktc-faq-card a.ktc-faq-card__wa{display:inline-block;background:#25D366;color:#fff!important;font-weight:700!important;font-size:14px!important;border-radius:10px;padding:12px 18px;text-decoration:none}
.ktc-acc .e-n-accordion{counter-reset:q}
.ktc-acc .e-n-accordion-item{counter-increment:q;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:16px;
  margin-bottom:12px;overflow:hidden;transition:box-shadow .25s,border-color .25s}
.ktc-acc .e-n-accordion-item:hover{box-shadow:0 10px 28px rgba(0,0,0,.08)}
.ktc-acc .e-n-accordion-item[open]{border-color:#FFA300;box-shadow:0 14px 34px rgba(255,163,0,.18)}
.ktc-acc .e-n-accordion-item-title{padding:20px 22px!important;border:0!important;background:transparent!important;align-items:center;gap:14px}
.ktc-acc .e-n-accordion-item-title-header{display:flex;align-items:center;gap:14px}
.ktc-acc .e-n-accordion-item-title-header:before{content:counter(q,decimal-leading-zero);flex:0 0 auto;width:40px;height:40px;border-radius:12px;
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;background:#FFF4DD;color:#C77E00}
.ktc-acc .e-n-accordion-item[open] .e-n-accordion-item-title-header:before{background:#FFA300;color:#000}
.ktc-acc .e-n-accordion-item-title-text{font-size:17px!important;line-height:1.4!important}
.ktc-acc .e-n-accordion-item-title-icon{flex:0 0 auto;width:34px;height:34px;border-radius:50%;background:#111;
  display:flex!important;align-items:center;justify-content:center}
.ktc-acc .e-n-accordion-item-title-icon svg{fill:#fff!important;width:12px;height:12px}
.ktc-acc .e-n-accordion-item[open] .e-n-accordion-item-title-icon{background:#FFA300}
.ktc-acc .e-n-accordion-item[open] .e-n-accordion-item-title-icon svg{fill:#000!important}
.ktc-acc .e-n-accordion-item>[role=region]{border:0!important;padding:0 22px 18px 76px!important;color:#4A4A4A;min-height:0!important}
.ktc-acc [role=region] .elementor-widget-text-editor,.ktc-acc [role=region] .elementor-widget-container{margin:0!important;padding:0!important}
.ktc-acc [role=region] p:last-child{margin-bottom:0!important}
.ktc-acc [role=region]>.e-con-inner,.ktc-acc [role=region].e-con{--padding-top:0px;--padding-bottom:0px;--padding-left:0px;--padding-right:0px}
@media (max-width:1024px){.ktc-faq-intro{position:static}}
@media (max-width:767px){
  .ktc-acc .e-n-accordion-item-title{padding:16px!important}
  .ktc-acc .e-n-accordion-item-title-header:before{width:32px;height:32px;font-size:12px;border-radius:10px}
  .ktc-acc .e-n-accordion-item-title-text{font-size:15px!important}
  .ktc-acc .e-n-accordion-item>[role=region]{padding:0 16px 16px!important}
  .ktc-faq-card{padding:22px}.ktc-faq-card a.ktc-faq-card__phone{font-size:26px!important}}
</style>"""
faq["elements"] = [faq_intro, faq_list,
    {"id": nid(), "elType": "widget", "widgetType": "html", "elements": [],
     "settings": {"html": FAQ_CSS, "_position": "absolute", "_element_width": "initial",
                  "_element_custom_width": {"unit": "px", "size": 0, "sizes": []}}}]

# ===================== 2d. mobile optimisation (home page only) =====================
for g in (how["elements"][2], price["elements"][3]):  # phones: compact rows, icon on the left
    g["settings"]["grid_columns_grid_mobile"] = {"unit": "fr", "size": 1, "sizes": []}
    g["settings"]["grid_gaps_mobile"] = {"column": "10", "row": "10", "isLinked": True, "unit": "px"}
    for w in g["elements"]:
        w["settings"]["position_mobile"] = "inline-start"
        w["settings"]["_padding_mobile"] = {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True}
for g in (situ["elements"][2],):
    g["settings"]["grid_gaps_mobile"] = {"column": "12", "row": "12", "isLinked": True, "unit": "px"}
    for w in g["elements"]:
        if w.get("widgetType") == "icon-box":
            w["settings"]["_padding_mobile"] = {"unit": "px", "top": "20", "right": "18", "bottom": "20", "left": "18", "isLinked": False}
# centred section on phones -> centred button
S("0f4641c")["_flex_align_self_mobile"] = "center"
for c, n in (("d3f9148", 3), ("7574378", 4), ("07567ad", 3)):
    S(c)["css_classes"] = f"ktc-flips ktc-flips-{n}"
    S(c)["boxed_width"] = {"unit": "px", "size": 1240, "sizes": []}
S("07567ad")["content_width"] = "boxed"   # was full-width: wider than the other two rows
for c in ("c0c4479", "0ab9485", winter["id"]):  # image + text sections: same 1240px box as the rest of the page
    idx[c] = idx.get(c) or winter
    (winter if c == winter["id"] else idx[c])["settings"].update({"content_width": "boxed", "boxed_width": {"unit": "px", "size": 1240, "sizes": []},
        "flex_gap": {"column": "60", "row": "30", "isLinked": False, "unit": "px", "size": 60}})
S("93f3140")["border_border"] = "none"
S("9e21e2a")["padding"] = {"unit": "px", "top": "80", "right": "20", "bottom": "80", "left": "20", "isLinked": False}
S("d746a44")["grid_columns_grid_mobile"] = {"unit": "fr", "size": 2, "sizes": []}
S("d746a44")["css_classes"] = "ktc-stats"
S("a948605")["_margin_mobile"] = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
S("a274611")["_margin_mobile"] = dict(S("a948605")["_margin_mobile"])
for c in ("056494d", "d21c473"):  # sticky image columns overlapped the text once the columns stack
    for k in ("sticky", "sticky_on", "sticky_offset_tablet", "sticky_parent"): S(c).pop(k, None)
data[0]["settings"]["padding_mobile"] = {"unit": "px", "top": "40", "right": "20", "bottom": "30", "left": "20", "isLinked": False}
MOBILE_CSS = """<style>
.ktc-card a,.ktc-card-sm a{font-size:inherit!important;font-weight:600;color:inherit}
/* service cards: each row stretches to the full width (no orphan cards / side gaps) */
.ktc-flips>.e-con-inner,.ktc-flips{flex-wrap:wrap!important}
.ktc-flips .elementor-widget-flip-box{flex:1 1 calc(33.333% - 19px)!important;width:auto!important;max-width:none!important}
.ktc-flips-4 .elementor-widget-flip-box{flex-basis:calc(25% - 19px)!important}
.ktc-flips .elementor-flip-box{height:330px!important}
@media (max-width:1024px){.ktc-flips .elementor-widget-flip-box,.ktc-flips-4 .elementor-widget-flip-box{flex-basis:calc(50% - 14px)!important}}
.ktc-sit-cta-w{height:100%}
.ktc-sit-cta-w>.elementor-widget-container{height:100%}
.ktc-sit-cta{height:100%;box-sizing:border-box;background:#111;border-radius:16px;padding:26px 24px;display:flex;flex-direction:column;gap:10px;
  position:relative;overflow:hidden}
.ktc-sit-cta:before{content:"";position:absolute;right:-50px;top:-50px;width:160px;height:160px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,163,0,.4),rgba(255,163,0,0) 70%)}
.ktc-sit-cta p.ktc-sit-cta__t{color:#fff;font-size:19px;font-weight:700;line-height:1.3;margin:0}
.ktc-sit-cta p.ktc-sit-cta__d{color:rgba(255,255,255,.75);font-size:15px;line-height:1.6;margin:0}
.ktc-sit-cta a.ktc-sit-cta__b{margin-top:auto;align-self:flex-start;background:#FFA300;color:#000!important;font-weight:700;font-size:15px;
  border-radius:10px;padding:12px 18px;text-decoration:none}
@media (max-width:767px){
  .ktc-stats>.e-con:last-child{grid-column:1/-1}
  .ktc-stats>.e-con{background:#fff;border:1px solid rgba(0,0,0,.08)!important;border-radius:14px;padding:16px 8px!important}
  .ktc-stats .elementor-counter-number-wrapper{font-size:30px!important}
  .ktc-stats .elementor-widget-counter,.ktc-stats .elementor-widget-counter>.elementor-widget-container{border:0!important;padding:0!important}
  /* service flip cards: 2 per row instead of 16 full-width 380px cards */
  .ktc-flips,.ktc-flips>.e-con-inner{gap:12px!important}
  .ktc-flips .elementor-widget-flip-box,.ktc-flips-4 .elementor-widget-flip-box{flex-basis:calc(50% - 6px)!important}
  .ktc-flips .elementor-flip-box{height:230px!important}
  .ktc-flips .elementor-flip-box__layer__title{font-size:14px!important;line-height:1.25!important}
  .ktc-flips .elementor-flip-box__back .elementor-flip-box__layer__description{font-size:11.5px!important;line-height:1.45!important;
     display:-webkit-box;-webkit-line-clamp:7;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:10px!important}
  .ktc-flips .elementor-flip-box__layer__overlay{padding:14px!important}
  /* compact info cards */
  .ktc-card .elementor-icon-box-title{font-size:16px!important}
  .ktc-card .elementor-icon-box-description{font-size:14px!important}
  .ktc-card-sm .elementor-icon-box-wrapper{gap:14px}
  .ktc-card-sm .elementor-icon-box-icon{margin:0!important}
  .ktc-card-sm .elementor-icon-box-title{font-size:16px!important;margin-bottom:4px!important}
  .ktc-card-sm .elementor-icon-box-description{font-size:14px!important;line-height:1.5!important}
  .ktc-card-sm .elementor-icon{padding:11px!important}
  .ktc-card-sm .elementor-icon svg{width:18px!important;height:18px!important}
  /* readable body copy */
  .elementor-widget-text-editor p{font-size:15px;line-height:1.65}
}
</style>"""
data[0]["elements"].insert(0, {"id": nid(), "elType": "widget", "widgetType": "html", "elements": [],
                               "settings": {"html": MOBILE_CSS, "_position": "absolute", "_element_width": "initial",
                                            "_element_custom_width": {"unit": "px", "size": 0, "sizes": []}}})
for sec, cls in ((how, "ktc-card-sm"), (price, "ktc-card-sm"), (situ, "ktc-card")):
    for g in sec["elements"]:
        for w in g.get("elements", []):
            if w.get("widgetType") == "icon-box":
                w["settings"]["_css_classes"] = cls

# ===================== 3. order (per doc) =====================
top = {e["id"]: e for e in data}
order = ["678e4f8", "447526f", "c0c4479", "863aceb", "9e21e2a", "0ab9485", "116cc96",
         how, price, situ,
         "b7d5300", "e700e38", "93f3140", "f9c0150",
         winter, "0ac5450", "5d18d64", "8427113", "cc482fb", "c6b2cd9", "b02de70"]
new = [top[x] if isinstance(x, str) else x for x in order]
assert len({e["id"] for e in new}) == len(new) and set(top) <= {e["id"] for e in new}
# ---- one vertical rhythm for every section (was a mix of margins + paddings, 0 to 160px) ----
BG = {"9e21e2a", "116cc96", how["id"], price["id"], situ["id"]}
KEEP = {"678e4f8", "447526f", "b7d5300", "e700e38", "93f3140"}  # hero, marquees, map + its area grid
PAD = {"": 50, "_tablet": 40, "_mobile": 32}       # plain sections: neighbours add up to 100/80/64
PAD_BG = {"": 90, "_tablet": 64, "_mobile": 52}     # sections with their own background
ZERO = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
for e in new:
    if e["id"] in KEEP:
        continue
    st = e["settings"]
    for bp, v in (PAD_BG if e["id"] in BG else PAD).items():
        st["margin" + bp] = dict(ZERO)
        old = st.get("padding" + bp) or st.get("padding") or {}
        lr = old.get("left") or "20"
        st["padding" + bp] = {"unit": "px", "top": str(v), "right": old.get("right") or lr, "bottom": str(v), "left": lr, "isLinked": False}
# towns box sits right under the area grid
S("f9c0150")["padding"]["top"] = "40"

json.dump(new, open("built_home.json", "w"))
print("sections", len(new))
