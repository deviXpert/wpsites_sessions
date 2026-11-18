# Design directions (Phase 3, Checkpoint 3)

Three dark homepage concepts. They share the brand inputs (ink `#0B0F14`, warm-white `#F2EFE9`, charge-green `#3BE37F` accent, Manrope + IBM Plex Mono, the supplied logo) and differ in layout, typography, imagery and interactions. All three are throwaway prototypes. Product images are **placeholder drawings**, and prices and specs are unconfirmed.

| | Prototype (private link) | Source |
|---|---|---|
| A: Spec Sheet | https://claude.ai/artifact/6L1r4JwgViDfoEK84ScWzg | `prototypes/a-spec-sheet.html` |
| B: Showroom | https://claude.ai/artifact/KTfaKV7Vveu8asneSPKAHL | `prototypes/b-showroom.html` |
| C: Guided | https://claude.ai/artifact/9DmaCzJGKqjvgUVjpztYeT | `prototypes/c-guided.html` |

All three were checked at 1440px and 390px: no horizontal scrolling and no script errors.

---

## A: Spec Sheet (precise, technical, numbers-led)
- **Concept:** the honest price is the hero. It reads like a well-made datasheet: calm, exact, nothing hidden.
- **Layout:** asymmetric two-column editorial grid. Hairline-bordered panels, flat surfaces, no imagery needed above the fold.
- **Typography:** Manrope 600 for headings with a light (300) second line, and **IBM Plex Mono for every number, price and label**.
- **Colour on dark:** near-black with two lifted surfaces. Green only on primary buttons, "Included" lines and "Yes" cells.
- **Imagery:** product cut-outs on flat dark tiles, graded to the surface. Small, consistent, catalogue-like.
- **Motion:** almost none. Instant state changes; numbers update in place.
- **Signature interactions:**
  1. **Live installed-price receipt:** pick a charger, finish and cable, and an itemised receipt updates. Unavailable 5m is shown disabled; the CT clamp shows as included.
  2. **Need-based comparison datasheet:** tap "I have solar panels", "I want a cable attached" or "Looks matter" to highlight the relevant rows.
  3. **Home charging cost calculator:** your battery size, your own p/kWh rate and charge range give a cost and charging time, with no invented tariffs.
- **Best for:** trust, transparency and SEO (lots of real text and tables). The least "showy".

## B: Showroom (object-first, premium, design-led)
- **Concept:** the charger as a beautiful object on your house. Colour choice is the emotional hook.
- **Layout:** large stages and big soft-cornered tiles. Each product gets room to breathe. Generous whitespace.
- **Typography:** Manrope **200/300 at very large sizes** with a 600 contrast word, plus wide-tracked mono eyebrows.
- **Colour on dark:** deeper staged surfaces with a vignette. Green buttons as pills.
- **Imagery:** needs the **best photography** (high-res cut-outs of each finish). It's the most dependent on the client's photos.
- **Motion:** gentle colour and backdrop cross-fades (opacity only).
- **Signature interactions:**
  1. **Finish switcher:** recolours the hero charger (Mythos Black / Red / Space Grey / Midnight Green).
  2. **"See it on your wall":** render, brick or timber cladding behind the charger.
  3. **Cable-reach visualiser:** pick 7.5m or 10m, slide the distance to your car's port, and it says whether it reaches.
- **Best for:** desirability and premium feel, closest in spirit to the brief's Hypervolt reference without its look. Weaker until real photos arrive.

## C: Guided (conversational, reassuring, first-time-buyer friendly)
- **Concept:** a knowledgeable friend walks you through it. The homepage *starts* with a question rather than a sales pitch.
- **Layout:** left progress rail with one question at a time, and big rounded answer tiles (88px+ tap targets).
- **Typography:** Manrope 800 for headings (bolder and warmer), body at 17px.
- **Colour on dark:** green for progress and "selected"; amber for "may need extra work" states.
- **Imagery:** minimal. Product images appear only in the recommendation card.
- **Motion:** step transitions and a progress meter.
- **Signature interactions:**
  1. **3-question charger finder as the hero:** solar → cable → style, then a recommendation with reasons and price.
  2. **"Is my home ready?" checker:** 5 yes/no questions with a live verdict (standard install, or extra work likely).
  3. **Order journey timeline + FAQ accordion:** what happens after you pay.
- **Best for:** conversion of nervous first-time EV owners and fewer non-standard surprises. Less impact as a brand statement.

## Elementor feasibility (native-first)
| | Native Elementor coverage | Needs Custom Code (global) |
|---|---|---|
| A | Headings, text, buttons, Table (or HTML), Loop Grid for product cards, Icon List | Receipt configurator and calculator (small JS, ~3KB), highlight toggle |
| B | Headings, buttons, Loop Grid, image hotspots/tabs | Finish switcher (can be native Tabs with images), wall preview and reach visualiser (small JS) |
| C | Accordion, Icon List, Loop Grid, Elementor Form (multi-step form exists natively in Elementor Pro) | Finder result logic and checker verdict (small JS) |

All three are buildable with mostly native widgets. The interactive pieces are small, self-contained scripts in Custom Code, with no frameworks.

## Contrast checks (WCAG 2.2)
Text and icons on each surface (ratio, AA needs 4.5:1 for body text and 3:1 for large text and UI):

| Foreground | ink #0B0F14 | s1 #11161D | s2 #171E27 | s3 #1F2833 |
|---|---|---|---|---|
| Heading text #F2EFE9 | 16.75 | 15.82 | 14.62 | 12.98 |
| Body text #C3C7CD | 11.32 | 10.70 | 9.89 | 8.78 |
| Muted text #939CA8 | 6.92 | 6.54 | 6.04 | 5.36 |
| Accent #3BE37F (text/icons) | 11.42 | 10.79 | 9.97 | 8.85 |
| Warning #F2C14E | 11.45 | 10.82 | 10.00 | 8.88 |
| Control border #3A4655 | **2.00 ❌** | 1.89 ❌ | 1.75 ❌ | 1.55 ❌ |

- Button text: dark ink `#06210F` on green `#3BE37F` = **10.13:1** (hover `#5CEB97` = 11.19:1). ✅
- ⚠️ **Fix for the build:** in the prototypes, the outlines on ghost buttons, inputs and swatches are below the **3:1** needed for control boundaries (WCAG 1.4.11). The design system will raise the control border to about `#5B6778` (≥3:1 on all surfaces). Decorative dividers can stay subtle.
- Focus ring: 2px green outline with a 3px offset (11.4:1 against ink). ✅

## What's next
Once you pick a direction (or a mix, e.g. "A's layout with C's finder"), I'll write `design-system.md`: tokens as CSS variables (mapped to Elementor Global Colours and Fonts), surface and elevation scale, type scale, spacing, components, motion rules and the full contrast table.
