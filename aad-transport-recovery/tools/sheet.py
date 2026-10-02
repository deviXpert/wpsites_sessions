from PIL import Image
import glob,sys,re
for base in sorted(set(re.sub(r'_[dm]_\d+\.png$','',f) for f in glob.glob('prev/*_d_*.png'))):
  for n,cols in (('d',3),('m',8)):
    fs=sorted(glob.glob(f'{base}_{n}_*.png'))
    if not fs: continue
    ims=[Image.open(f) for f in fs];w,h=ims[0].size;s=Image.new('RGB',(w*cols,h*((len(ims)+cols-1)//cols)),'white')
    for i,im in enumerate(ims): s.paste(im,((i%cols)*w,(i//cols)*h))
    s.thumbnail((2000,3000));s.save(f'{base}_{n.upper()}S.png')
