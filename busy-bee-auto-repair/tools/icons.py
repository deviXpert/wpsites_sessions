"""Upload the Lucide icons used by the builders as SVG media (needs Elementor → Settings → Advanced →
'Enable Unfiltered File Uploads'), write icons.json, then rebuild every document so icons switch from the
Font Awesome fallback to the exact Lucide glyphs from the design.  Usage: python3 icons.py <lucide-static/icons dir>"""
import json, os, re, sys, tempfile
import el, wp

CUSTOM = {  # icons that are not plain stroked Lucide glyphs in the design
    'whatsapp': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="lucide bb-wa-icon"><path d="M20.5 11.6a8.5 8.5 0 0 1-12.6 7.5L3 20.5l1.4-4.8A8.5 8.5 0 1 1 20.5 11.6Z" stroke="currentColor" stroke-width="1.7"/><path d="M8.1 7.4c-.6.1-1.2 1-1 2.1.5 3 3.1 5.5 6.2 6 .9.1 2-.6 2.2-1.3l-2.3-1.3-.9 1c-1.3-.5-2.5-1.7-3-2.9l.8-1-1.1-2.6Z" fill="currentColor" class="bb-fill"/></svg>',
}
FILLED = {'star'}  # design uses these with fill-current


def collect():
    import build_header, build_footer, build_home, build_popups
    build_header.build(); build_footer.build(); build_home.build()
    for p in build_popups.POPUPS:
        build_popups.popup(*p)
    return sorted(el.USED_ICONS)


def upload_svg(path, filename):
    """Multipart upload flagged as an Elementor media upload – Elementor only allows SVG for those requests."""
    import subprocess
    r = subprocess.run(['curl', '-sS', '-u', f"{os.environ.get('BB_WP_USER') or os.environ['WP_USER']}:"
                        f"{os.environ.get('BB_WP_APP_PASSWORD') or os.environ['WP_APP_PASSWORD']}",
                        '-F', f'file=@{path};type=image/svg+xml;filename={filename}',
                        '-F', 'uploadTypeCaller=elementor-wp-media-upload', wp.U + '/wp-json/wp/v2/media'],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    if 'id' not in d:
        raise SystemExit(f'upload {filename} failed: {d}')
    return d


def svg_for(name, src):
    if name in CUSTOM:
        return CUSTOM[name]
    s = open(os.path.join(src, name + '.svg')).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S).strip()
    if name in FILLED:
        s = s.replace('fill="none"', 'fill="currentColor"').replace('class="lucide', 'class="lucide bb-filled')
    return s


if __name__ == '__main__':
    src = sys.argv[1]
    names = collect()
    have = json.load(open('icons.json')) if os.path.exists('icons.json') else {}
    for n in names:
        if n in have:
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.svg', delete=False) as f:
            f.write(svg_for(n, src))
        d = upload_svg(f.name, f'lucide-{n}.svg')
        have[n] = {'id': d['id'], 'url': d['source_url']}
        json.dump(have, open('icons.json', 'w'), indent=1)
        print('uploaded', n, d['id'])
    print(len(have), 'icons ready – now run: python3 build_all.py')
