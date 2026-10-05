#!/bin/bash
# usage: qa.sh tag  -> screenshot page 41 at 3 widths and slice
D=$(dirname "$0"); cd $D
python3 -c "from el import regen; regen(41)" && ./shot.sh 41 $1 && python3 -c "
from PIL import Image
for w in (1440,1024,390):
  im=Image.open(f'qa/$1_{w}.png'); W,H=im.size; s=720/W if W>720 else 1
  im=im.resize((int(W*s),int(H*s)))
  for i in range(0,im.height,1100): im.crop((0,i,im.width,min(im.height,i+1100))).save(f'qa/$1_{w}_{i//1100}.png')"
