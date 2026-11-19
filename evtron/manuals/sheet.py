"""Contact sheet of preview PNGs for quick visual QA. Usage: python3 sheet.py <prefix> <out.png> [cols]"""
import glob
import sys

from PIL import Image

prefix, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
files = sorted(glob.glob(f"preview/{prefix}-*.png"))
ims = [Image.open(f) for f in files]
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols + 10 * (cols - 1), h * rows + 10 * (rows - 1)), "#777")
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * (w + 10), (i // cols) * (h + 10)))
sheet.save(out)
print(len(ims), "pages", w, h)
