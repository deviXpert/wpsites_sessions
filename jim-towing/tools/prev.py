"""python3 prev.py <key> [mobile]  -> preview-link screenshot of a draft, split into JPG chunks in ../shots/"""
import sys, json, subprocess, os
from PIL import Image
from wp import ability
c = json.load(open('created.json'))
key = sys.argv[1]; mob = len(sys.argv) > 2
pid = c['pages'].get(key) if key in c.get('pages', {}) else int(key)
u = ability('elementor/create-preview-link', {'post_id': pid})['url']
os.makedirs('../shots', exist_ok=True); out = f'../shots/{key}_{"m" if mob else "d"}'
env = dict(os.environ, NODE_PATH=subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
print(subprocess.run(['node', 'shot.js', u, out] + (['390', '844'] if mob else []), capture_output=True, text=True, env=env).stdout)
im = Image.open(out + '.png'); W, H = im.size; step = 1700 if mob else 2200; k = 0
for y in range(0, H, step):
    c2 = im.crop((0, y, W, min(H, y + step))).convert('RGB')
    if not mob: c2 = c2.resize((W // 2, c2.size[1] // 2))
    else: c2 = c2.resize((int(W * .8), int(c2.size[1] * .8)))
    c2.save(f'{out}_{k:02d}.jpg', quality=70); k += 1
os.remove(out + '.png'); print(k, 'chunks', W, H)
