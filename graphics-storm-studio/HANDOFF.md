# Graphics Storm Studio – Glassmorphism Redesign Handoff

Site: **https://graphicsstormstudio.com** (WordPress, **Hello Elementor** theme, Elementor 4.4.2 + Pro 4.3.1, Hostinger).
Design: dark navy glassmorphism, brand blue `#0684C4` + violet CTA `#7052FF`, Sora + Inter. See `docs/01-design-spec.md`.

## ⚠️ Before doing anything in a new session
1. Credentials come from env vars only: `GSS_WP_URL/GSS_WP_USER/GSS_WP_APP_PASSWORD` (preferred) or `WP_URL/WP_USER/WP_APP_PASSWORD`. Never paste them in chat.
2. `tools/wp.py` **refuses to run unless the host is graphicsstormstudio.com** (other clients live in this repo).
3. The redesign is built as **drafts**. Never overwrite the original published pages until the user approves (`tools/launch.py --go`).
4. The site is behind the *Under Construction* plugin (user-enabled), which blocks anonymous front-end views, including CSS generation for drafts.

## Deliverables
| # | What | Where |
|---|---|---|
| 1 | Design spec mapped to Site Settings | `docs/01-design-spec.md` (applied, source `tools/kit.py`, export `templates/site-settings.json`) |
| 2 | Global CSS (one block) | `templates/gs-global.css` (applied in Site Settings → Custom CSS) |
| 3 | Homepage build guide | `docs/02-build-guide-homepage.md` |
| 4 | Header, Footer, About, Service template, Our Work, Contact | `docs/03-build-guide-other-pages.md` |
| 5 | Importable Elementor JSON (Container-based, native widgets) | `templates/gs-*.json` (Templates → Saved Templates → Import) |
| 6 | Pre-launch checklist, clean-up, images, SEO, security | `docs/04-checklist.md` |

## What exists on the site (IDs in `tools/created.json`)
| Item | ID | Status |
|---|---|---|
| Default Kit (Site Settings) | 17 | **live**: new globals + custom CSS; old colours kept as "Legacy – …" |
| GS – Header (Sticky Glass) | 5717 | published, conditions = redesign drafts only |
| GS – Footer | 5719 | published, conditions = redesign drafts only |
| GS – CTA Band (saved section, embedded by Template widget) | 5721 | published |
| Menu "GSS Main" | 9 | not assigned to a location (used by the Nav Menu widget) |
| Drafts: Home 5723, About 5725, Web 5727, SEO 5729, SMM 5731, Design 5733, Services 5735, Work 5737, Contact 5739 | | drafts → replace originals 21, 2738, 5429, 5607, 5516, 5562, 4213, 4569, 2802 |
| Flexbox Container experiment | | **activated** |

## How to rebuild / resume
```bash
cd graphics-storm-studio/tools
python3 kit.py            # re-apply Site Settings (merges into kit 17 via Elementor's document API, then publish-document)
python3 build.py          # regenerate templates/*.json only
python3 build.py --push   # update header/footer/CTA + all drafts on the site (refuses to touch published pages)
python3 launch.py         # dry run; --go after user approval
python3 backup.py         # fresh snapshot to ../backup/
```
- All copy is in `tools/content.py`; element builders are in `tools/el.py` (IDs seeded per page, so they stay stable between rebuilds).
- WP Abilities: read-only abilities need GET, destructive ones DELETE with `?input[...]` (handled in `wp.ability(name, params, method)`). Kit changes are *staged* and need `elementor/publish-document` (DELETE).
- `elementor/create-preview-link` and widget schemas need the Atomic Editor (V4), which is off, so we don't use them.

## Open items
- Visual QA screenshots are blocked by Under Construction plus draft status (see the session notes). The user reviews the drafts while logged in.
- Facebook/LinkedIn URLs unknown (placeholders in the footer). Our Work project names and results are placeholders.
- No SEO plugin installed. GTM (GTM-W59NCNT) was output by the old theme and is gone with Hello, so it needs re-adding.
- Privacy Policy and Terms pages don't exist (the footer links to them).
- Clean-up done 2026-11-27: Kirki and Meta Box deleted; 127 broken media entries deleted. The user still needs to delete the Astra/Astra Child (Onum) themes in Appearance → Themes.
- Visual QA done 2026-11-27 (pages temporarily published as `/gss-qa-*/`, then set back to draft). On all 9 pages at 1440/1024/768/390px: 0px horizontal overflow, exactly 1 H1, **0 axe-core WCAG 2 A/AA violations**. Screenshots are in `qa-screenshots/`.
  Fixes made during QA: violet CTA `#7C5CFF` → `#7052FF` (white text 4.35 → 4.84:1); container entrance animation key (`animation`, not `_animation`); Elementor's default 10px container padding set to 0; logo no-wrap; full-width buttons on mobile; footer column widths; FAQ content border.
  Re-run: `node tools/qa.js <outdir> <urls>` and `node tools/a11y-probe.js <url>` (needs `npm i axe-core` in the run directory).
- **The Under Construction plugin was removed by the user**, so the OLD pages are public again until launch (`tools/launch.py --go`).
