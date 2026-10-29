# Sana Jewellers — 404 audit (29 Oct 2026)

Crawled every sitemap URL (EN + AR) plus every internal link on English pages: **3,459 URLs, 3,400 OK, 11 real 404s.**
Blog URLs were throttled by Shopify (429 / false 404); all were re-checked slowly and return 200.

## Real 404s

| Broken URL | Linked from | Redirect to |
|---|---|---|
| /collections/manual | sort menu on every collection page | /collections/all |
| /collections/best-selling | sort menu | /collections/all?sort_by=best-selling |
| /collections/title-ascending | sort menu | /collections/all?sort_by=title-ascending |
| /collections/price-descending | sort menu | /collections/all?sort_by=price-descending |
| /collections/price-ascending | sort menu | /collections/all?sort_by=price-ascending |
| /collections/created-ascending | sort menu | /collections/all?sort_by=created-ascending |
| /collections/created-descending | sort menu | /collections/all?sort_by=created-descending |
| /products/18k-yellow-gold-rope-chain | blog "10 stylish men's chain styles" | /collections/necklaces-chains |
| /products/18k-yellow-gold-rollo-chain | blog "10 stylish men's chain styles" | /collections/necklaces-chains |
| /products/18k-yellow-gold-snake-chain-1 | blog "10 stylish men's chain styles" | /products/real-18k-yellow-gold-maze-snake-chain |
| /products/18k-yellow-gold-italian-holo-necklace | blog "why 18K Italian gold is superior" | /collections/necklaces-chains |

Sort menu: `snippets/collection-sorting.liquid` uses `href="price-ascending"` etc. JS intercepts clicks (shoppers get `?sort_by=`), but crawlers follow the bare href to `/collections/<value>` → 404. Redirects cover it; AR equivalents added too.

Blog links: also edit those two articles to point at live products.

Ignored (false positives): `/{{url}}` and `*/{{url}}` — Handlebars placeholders inside the ajax cart `<script type="text/template">`, not real links.

## Files
- `redirects-shopify-import.csv` — Online Store → Navigation → URL Redirects → Import.
- `smart-404-redirect.html` — paste into the 404 template (Custom HTML section) to catch future 404s.
