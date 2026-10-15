"""Convert the design's source images to WebP (resized to the largest size the design uses at 2x)."""
import os, sys
from PIL import Image
# source file -> (seo filename, max width, alt text)
MAP = {
 'busy-bee-workshop-hero-BWgzEgab.jpg': ('busy-bee-auto-repair-calgary-workshop-hero', 1920, 'Silver family SUV inside a clean professional mechanic shop'),
 'busy-bee-mobile-workshop-hero-BpEp6AbC.jpg': ('busy-bee-auto-repair-calgary-workshop-hero-mobile', 1024, 'Silver SUV inside a clean mechanic shop'),
 'truck-H1ANT7bA.jpg': ('pickup-truck-repair-calgary', 1920, 'Black pickup truck seen from a slight front angle in a dark mechanic shop'),
 'mercedes-BNKnk8qJ.jpg': ('mercedes-repair-calgary', 1920, 'Silver Mercedes-AMG sports car in side profile inside a dark mechanic shop'),
 'bmw-DNN6tMwq.jpg': ('bmw-repair-calgary', 1920, 'Blue BMW sedan seen from the front inside a dark mechanic shop'),
 'workshop-wide.png': ('busy-bee-repair-bay-calgary', 1672, 'Wide view of a full repair bay with a mechanic working beside a sedan'),
 'audi-workshop.png': ('engine-repair-audi-calgary', 1672, 'Mechanic working on an Audi engine in the workshop'),
 'busy-bee-original-logo.png': ('busy-bee-auto-repair-logo', 600, 'Busy Bee Auto Repair'),
 'diagnostic-indicator.png': ('computer-diagnostics-indicator', 96, ''),
 'reviewer-avatars-BOEPlixg.png': ('busy-bee-customer-avatars', 300, ''),
 'favicon.png': ('busy-bee-favicon', 64, ''),
 'napa-auto-parts-Bx_qg8GY.png': ('napa-auto-parts', 743, 'NAPA Auto Parts'),
 'lordco-auto-parts-Uk4USUl3.png': ('lordco-auto-parts', 660, 'Lordco Auto Parts'),
 'partsource-DV9h667p.png': ('partsource', 595, 'PartSource'),
 'auto-value-DQAzBDM4.png': ('auto-value-auto-parts', 751, 'Auto Value Auto Parts'),
 'winter-tires.png': ('winter-tire-change-calgary', 1536, 'Winter tires on a snowy mountain road'),
 'oil-service.png': ('mobil-1-synthetic-oil-change-calgary', 1200, 'Mechanic pouring Mobil 1 synthetic oil into an engine'),
 'battery-service.png': ('battery-alternator-service-calgary', 1200, 'Mechanic testing a car battery'),
 'brake-service-DAs--rV2.jpg': ('brake-repair-calgary', 1024, 'Mechanic inspecting a brake disc and caliper'),
 'diagnostics-service-Djl4l8sV.jpg': ('computer-diagnostics-calgary', 1024, 'Mechanic running a computer diagnostic scan'),
 'civic-studio.png': ('honda-civic-symptom-checker', 1200, 'White Honda Civic sedan, illustrative preview'),
 'busy-bee-storefront.png': ('busy-bee-auto-repair-storefront-calgary', 1360, 'Busy Bee Auto Repair storefront in NE Calgary'),
 'gmark.png': ('google-g-mark', 112, 'Google'), 'gmark_hero.png': ('google-g-mark-hero', 112, 'Google'),
 'audi.png': ('audi-logo', 320, 'Audi'), 'bmw.png': ('bmw-logo', 320, 'BMW'), 'mercedes-benz.png': ('mercedes-benz-logo', 480, 'Mercedes-Benz'),
 'porsche.png': ('porsche-logo', 320, 'Porsche'), 'toyota.png': ('toyota-logo', 320, 'Toyota'), 'ford.png': ('ford-logo', 320, 'Ford'),
 'workshop-services-wide.png': ('busy-bee-service-bays-calgary', 1672, 'Busy Bee service bays with vehicles on lifts'),
 'gmc.png': ('gmc-logo', 480, 'GMC'), 'hyundai.png': ('hyundai-logo', 320, 'Hyundai'), 'dodge.png': ('dodge-logo', 320, 'Dodge'),
}
if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    for f, (name, mw, alt) in MAP.items():
        if not os.path.exists(os.path.join(src, f)): continue
        im = Image.open(os.path.join(src, f))
        if im.width > mw:
            im = im.resize((mw, round(im.height * mw / im.width)), Image.LANCZOS)
        im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
        out = os.path.join(dst, name + '.webp')
        im.save(out, 'WEBP', quality=80, method=6)
        print(f'{name}.webp {im.size} {os.path.getsize(out)//1024}KB (was {os.path.getsize(os.path.join(src,f))//1024}KB)')
