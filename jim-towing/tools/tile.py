import sys,glob
from PIL import Image
pre=sys.argv[1]; per=int(sys.argv[2]) if len(sys.argv)>2 else 4
fs=sorted(glob.glob(f'../shots/{pre}_[0-9][0-9].jpg'))
for g in range(0,len(fs),per):
    ims=[Image.open(f) for f in fs[g:g+per]];h=max(i.size[1] for i in ims);w=sum(i.size[0] for i in ims)+10*(len(ims)-1)
    s=Image.new('RGB',(w,h),'#888');x=0
    for i in ims: s.paste(i,(x,0));x+=i.size[0]+10
    s.save(f'../shots/{pre}_tile{g//per}.jpg',quality=65);print(f'../shots/{pre}_tile{g//per}.jpg',s.size)
