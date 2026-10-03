# WP Sites — instructions for Claude sessions

This repo holds **one folder per client WordPress site** (redesign toolkits, backups, notes).

## When the user names a website (e.g. "continue pak-translations")
1. The site's work lives on a **git branch named after the website** (user preference), e.g. `pak-translations`.
   If the folder isn't in your checkout: `git fetch origin <site> && git checkout <site>` (or merge/check out its files onto your working branch).
2. Open `<site>/HANDOFF.md` first (current state, rules, how to publish), then `<site>/SESSION_LOG.md` (history).
3. Credentials come only from environment variables (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`, optionally site-prefixed). Each site's `tools/wp.py` refuses to run against the wrong host — if the env points at a different site, stop and ask the user.
4. Sites are LIVE: preview risky changes, ask before deleting anything, and when the user sends a batch of comments, list them back and wait for "go".
5. When you create a branch for a site, name it after the website. Commit + push after each round of changes.

## Sites
| Folder / branch | Site | Notes |
|---|---|---|
| `pak-translations/` (branch `pak-translations`) | https://pak-translations.com | Elementor redesign LIVE (Oct 2026). Core Elementor + Pro only, Outfit/Figtree. |
| `aad-transport-recovery/` | AAD Transport & Recovery (Hostinger staging) | Earlier Elementor redesign handoff. |
