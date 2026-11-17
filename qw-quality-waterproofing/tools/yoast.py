"""Push Yoast SEO title / meta description / focus keyphrase / social for every page (Yoast bulk-editor REST)."""
import json, wp
P = json.load(open('pages.json'))
SEP = ' | Quality Waterproofing'
SEO = {  # slug: (focus keyphrase, seo title, meta description)
 'home': ('basement waterproofing GTA', 'Basement Waterproofing GTA & North Bay' + SEP, 'Basement waterproofing across the GTA & North Bay – exterior & interior systems, sump pumps, foundation crack repair and interlocking. Free estimates.'),
 'services': ('waterproofing services Toronto', 'Waterproofing Services Toronto & GTA' + SEP, 'Exterior & interior basement waterproofing, sump pump installation, foundation crack repair and interlocking across the GTA and North Bay. Free estimates.'),
 'about-us': ('waterproofing contractor GTA', 'About Us – GTA Waterproofing Contractor' + SEP, 'Quality Waterproofing protects basements across Toronto, Mississauga, Brampton & North Bay with 10+ years of residential & commercial experience.'),
 'projects': ('waterproofing projects Toronto', 'Waterproofing & Interlocking Projects' + SEP, 'See real exterior & interior waterproofing, sump pump, crack repair and interlocking projects completed across Toronto, the GTA and North Bay.'),
 'contact': ('free waterproofing estimate', 'Contact Us – Free Waterproofing Estimate' + SEP, 'Call (437) 264-2664 or request a free on-site basement waterproofing estimate in Toronto, Mississauga, Brampton or North Bay.'),
 'exterior-waterproofing': ('exterior waterproofing Toronto', 'Exterior Waterproofing Toronto & GTA' + SEP, 'Exterior basement waterproofing in Toronto & the GTA: excavation, foundation sealing, drainage membrane and new weeping tile. Book a free estimate.'),
 'interior-waterproofing': ('interior basement waterproofing Toronto', 'Interior Basement Waterproofing Toronto' + SEP, 'Interior basement waterproofing in Toronto & the GTA – interior weeping tile, wall membrane and sump pump. A dry basement without digging up your yard.'),
 'sump-pump-installation': ('sump pump installation Toronto', 'Sump Pump Installation & Replacement Toronto' + SEP, 'Sump pump installation, replacement and battery backup systems in Toronto, Mississauga, Brampton & North Bay. Protect your basement from flooding.'),
 'foundation-crack-repair': ('foundation crack repair Toronto', 'Foundation Crack Repair Toronto & GTA' + SEP, 'Leaking foundation crack? We repair cracks from the outside – excavate, seal and membrane – across Toronto & the GTA. Free on-site inspection.'),
 'interlocking': ('interlocking Toronto', 'Interlocking Patios, Walkways & Driveways Toronto' + SEP, 'Interlocking patios, pool decks, walkways, steps and driveways in Toronto & the GTA – built on a compacted base and graded away from your home.'),
 'basement-waterproofing-toronto': ('basement waterproofing Toronto', 'Basement Waterproofing Toronto' + SEP, 'Wet basement in Toronto? Exterior & interior waterproofing, sump pumps, foundation crack repair and interlocking across the GTA. Free estimates.'),
 'basement-waterproofing-mississauga': ('basement waterproofing Mississauga', 'Basement Waterproofing Mississauga' + SEP, 'Basement waterproofing in Mississauga – exterior & interior waterproofing, sump pumps and foundation crack repair from Port Credit to Meadowvale.'),
 'basement-waterproofing-brampton': ('basement waterproofing Brampton', 'Basement Waterproofing Brampton' + SEP, 'Basement waterproofing in Brampton – exterior & interior systems, sump pumps, crack repair and interlocking. Protect your basement or second unit.'),
 'basement-waterproofing-north-bay': ('basement waterproofing North Bay', 'Basement Waterproofing North Bay' + SEP, 'Basement waterproofing in North Bay – exterior & interior waterproofing, sump pumps with battery backup and foundation crack repair. Free estimates.'),
}
if __name__ == '__main__':
    for s, (k, t, d) in SEO.items(): assert len(d) <= 160, (s, len(d))
    items = [{'id': P[s], 'focus_keyphrase': k, 'seo_title': t, 'meta_description': d} for s, (k, t, d) in SEO.items()]
    r = wp.req('yoast/v1/bulk_editor/update_search', 'POST', {'items': items})
    print([(x['id'], x['success']) for x in r.get('results', [])] or r)
    soc = [{'id': P[s], 'social_title': t.replace(SEP, ''), 'social_description': d} for s, (k, t, d) in SEO.items()]
    r = wp.req('yoast/v1/bulk_editor/update_social', 'POST', {'items': soc})
    print([(x['id'], x['success']) for x in r.get('results', [])] or r)
    # the bulk editor writes post meta but Yoast's indexables (what the front end outputs) only refresh on save_post
    for s in SEO:
        cur = wp.req(f'wp/v2/pages/{P[s]}?_fields=status')['status']
        wp.req(f'wp/v2/pages/{P[s]}', 'POST', {'status': cur})  # re-save without changing status
        j = wp.req(f'wp/v2/pages/{P[s]}?_fields=yoast_head_json')['yoast_head_json']
        print(s, '|', j.get('title'), '|', (j.get('description') or 'MISSING')[:50], '|', j.get('robots', {}).get('index'))
