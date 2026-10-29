# SH Silver Collection — Live Silver Rate page

Site: https://shsilvercollection.com (Shopify, theme "Horizon" 4.3.0).
Brand: ivory `#F9F7F3`, charcoal `#2A2A2A`; fonts Instrument Serif (headings), Jost (body), Pinyon Script (accent).

## File
`silver-rate-page.html` — self-contained, scoped under `#shs-rate`, no `{{ }}`/`{% %}` sequences (pastes into Custom HTML).

- Live spot from `https://api.gold-api.com/price/XAG`, refreshed every 60 s, retry every 10 s on failure.
- 999 AED/g = spot USD/oz ÷ 31.1035 × 3.6725; 925 = 999 × 0.925/0.999.
- Sections: ticker bar, editorial hero, 999/925 price board, price-by-weight list (g, 10 g, tola, oz, 100 g, kg), "Know your silver" columns, calculator, shop strip linking collections, FAQ, JSON-LD (WebPage, BreadcrumbList, FAQPage).
- `CONFIG.premiumPercent` / `premiumPerGram` to add the shop's markup.
- Theme scrolls inside `.page-wrapper`, not the window (matters only for screenshot tooling).

## SEO (page → Search engine listing)
- Page title: `Silver Rate Today in UAE`
- SEO title: `Silver Rate Today in UAE – 999 & 925 Silver Price per Gram`
- Meta description: `Live silver rate today in UAE & Dubai. Check 999 fine silver and 925 sterling silver price per gram, tola and kg in AED, updated every minute. Shop 925 silver jewellery.`
- URL handle: `silver-rate-today-uae` (JSON-LD URLs assume this handle)
