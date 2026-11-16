import sys
from PIL import Image
src, pre, w = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 720
im = Image.open(src); im = im.resize((w, int(im.height * w / im.width))); H = 1800
n = 0
for i in range(0, im.height, H): im.crop((0, i, w, min(i + H, im.height))).save(f'{pre}_{i // H}.png'); n += 1
print(n)
