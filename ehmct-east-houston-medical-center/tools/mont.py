import sys
from PIL import Image
tag,w,per=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
im=Image.open(f'qa/{tag}_{w}.png'); s=float(sys.argv[4]) if len(sys.argv)>4 else 1
im=im.resize((int(im.width*s),int(im.height*s)))
H=1400; cols=[im.crop((0,i,im.width,min(im.height,i+H))) for i in range(0,im.height,H)]
for g in range(0,len(cols),per):
    grp=cols[g:g+per]; out=Image.new('RGB',(sum(c.width+10 for c in grp),H),'black')
    x=0
    for c in grp: out.paste(c,(x,0)); x+=c.width+10
    out.save(f'qa/{tag}_{w}_m{g//per}.png'); print(f'qa/{tag}_{w}_m{g//per}.png')
