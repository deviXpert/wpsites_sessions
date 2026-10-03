import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
f=sys.argv[1]; h=int(sys.argv[2]) if len(sys.argv)>2 else 1800
im=Image.open(f); w,H=im.size
for i,y in enumerate(range(0,H,h)):
    im.crop((0,y,w,min(H,y+h))).save(f.replace('.png',f'_s{i:02d}.png'))
print(f, (H+h-1)//h)
