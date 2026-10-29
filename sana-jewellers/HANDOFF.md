# Sana Jewellers — Live Gold Rate page

Site: https://sanajewellers.com (Shopify, theme "Fazhop", brand gold `#B7813B`).
Reference: https://ar.ae.fkjewellers.com/pages/today-gold-price-in-uae-gold-rate-in-uae

## File
`gold-rate-page.html` — self-contained HTML/CSS/JS, scoped under `#sj-gold`.

- Live spot price from `https://api.gold-api.com/price/XAU` (free, no key, CORS `*`), refreshed every 60 s, retries every 10 s on failure.
- AED per gram = spot USD/oz ÷ 31.1035 × 3.6725 (AED peg). 22K/21K/18K = 0.916 / 0.875 / 0.750 of 24K.
- Sections: live hero, karat cards with unit toggle (g / 10 g / tola / oz), rate table, calculator (making charges + 5% VAT), CTA, FAQ.
- `CONFIG.premiumPercent` / `CONFIG.premiumPerGram` in the script add a markup so the page matches the shop's own rate (spot-based rates run a few AED below retail-board rates such as FK's).

## Install
Preferred: Online Store → Pages → Add page "Gold Rate" → create a page template → in the theme editor add a **Custom Liquid** section to that template and paste the file.
Alternative: paste into the page content editor's **Show HTML** (`<>`) view.
