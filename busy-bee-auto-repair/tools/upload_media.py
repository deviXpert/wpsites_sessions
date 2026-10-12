"""Upload the converted WebP images to the media library; records key -> {id,url} in media.json (idempotent)."""
import json, os, sys
import wp
from to_webp import MAP
d = sys.argv[1]
mf = 'media.json'
media = json.load(open(mf)) if os.path.exists(mf) else {}
for name, mw, alt in MAP.values():
    if name in media: continue
    r = wp.upload(os.path.join(d, name + '.webp'), name + '.webp', 'image/webp', alt)
    media[name] = {'id': r['id'], 'url': r['source_url'], 'w': r['media_details'].get('width'), 'h': r['media_details'].get('height')}
    print(name, r['id'])
    json.dump(media, open(mf, 'w'), indent=1)
