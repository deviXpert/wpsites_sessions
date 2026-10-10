from PIL import Image, ImageDraw, ImageFont
import numpy as np, sys
def text_img(txt, font, cap_h, color, spacing=0):
    # render at large size, crop to ink, scale to cap height
    f = ImageFont.truetype(font, 400)
    W = 400*len(txt)
    im = Image.new('L', (W, 600), 0); d = ImageDraw.Draw(im)
    x = 20
    for ch in txt:
        d.text((x, 50), ch, font=f, fill=255); x += f.getlength(ch) + spacing*400
    bb = im.getbbox(); im = im.crop(bb)
    s = cap_h / im.height
    im = im.resize((round(im.width*s), cap_h), Image.LANCZOS)
    out = Image.new('RGBA', im.size, color + (0,)); out.putalpha(im)
    return out
