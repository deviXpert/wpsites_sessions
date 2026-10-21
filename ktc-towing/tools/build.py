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
    ], cols=3, cols_tab=2),
    para("<p><strong>Not sure which service you need?</strong> Call (587) 435-0770 and describe what happened. Our Calgary dispatcher will tell you the right fix and the right truck.</p>"),
    call_btn(width=260),
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

# ===================== 3. order (per doc) =====================
top = {e["id"]: e for e in data}
order = ["678e4f8", "447526f", "c0c4479", "863aceb", "9e21e2a", "0ab9485", "116cc96",
         how, price, situ,
         "b7d5300", "e700e38", "93f3140", "f9c0150",
         winter, "0ac5450", "5d18d64", "8427113", "cc482fb", "c6b2cd9", "b02de70"]
new = [top[x] if isinstance(x, str) else x for x in order]
assert len({e["id"] for e in new}) == len(new) and set(top) <= {e["id"] for e in new}
json.dump(new, open("built_home.json", "w"))
print("sections", len(new))
