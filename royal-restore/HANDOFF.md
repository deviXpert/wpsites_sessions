# Royal Restore (formerly Rapid Restore) — rebrand handoff

Site: https://mediumpurple-mule-193176.hostingersite.com/ (Astra Pro + Elementor/Pro + Header Footer Elementor, LiteSpeed Cache)
Scope: rename "Rapid Restore" → "Royal Restore" site-wide + logo. Nothing else.

## Done (via REST, `tools/`)
- `tools/backup/` = pre-change export of all REST post types, settings, media list.
- `tools/replace.py --apply`: replaced Rapid Restore→Royal Restore in content + `_elementor_data` of pages 4462, 4394, 4388, 4384, 4380, 4368, 3275, 2696.
- New logo (same artwork, text redrawn in Rajdhani Regular, colour #04509B): media 4799 (full), 4800 (cropped). `site_logo` setting → 4800 (was 4100).

## Needs wp-admin (not reachable via REST)
- Header template 2700 and footer template 3024 (Appearance → Elementor Header & Footer Builder): swap logo image to "Royal Restore logo", and edit footer text ("Rapid Restore is your trusted partner…", copyright "Rapid Restore").
- Elementor → Tools → Clear Files & Data, then LiteSpeed → Purge All (live site serves cached old text until then).
- Left as-is pending owner decision: "Rapid Response Restoration" (commercial copy), Instagram URL instagram.com/rapidrestorenow.
