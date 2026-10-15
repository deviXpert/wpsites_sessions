"""Hand-built side-view vehicle illustrations for the symptom checker (one per body style, no third-party images or watermarks).
Each shape is a list of outline points; corners are rounded automatically.  The body colour is a CSS variable so bb.js can tint it.
code.py injects window.BB_CARSVG = {sedan: '<svg…>', …} in front of bb.js."""
import json

W, H, GROUND = 640, 280, 236

# body outline (front of the car on the right), window outline, wheel centres x, wheel radius, corner radius
SHAPES = {
    'sedan': dict(body=[(52, 214), (44, 182), (58, 152), (150, 140), (212, 100), (318, 88), (392, 92), (462, 138), (548, 150),
                        (588, 170), (594, 204), (576, 218)],
                  win=[(204, 136), (232, 106), (316, 96), (384, 100), (436, 136)], pillar=328, wheels=(158, 482), r=40, rad=16),
    'hatch': dict(body=[(120, 214), (112, 172), (124, 118), (160, 96), (316, 88), (384, 94), (450, 138), (522, 150), (556, 170),
                        (560, 204), (544, 218)],
                  win=[(140, 132), (160, 106), (310, 98), (374, 102), (422, 134)], pillar=280, wheels=(206, 466), r=38, rad=16),
    'coupe': dict(body=[(50, 214), (44, 180), (62, 154), (176, 140), (262, 104), (352, 98), (446, 146), (556, 158), (596, 178),
                        (598, 206), (580, 218)],
                  win=[(250, 138), (276, 112), (346, 106), (418, 140)], pillar=None, wheels=(156, 486), r=40, rad=14),
    'suv': dict(body=[(56, 214), (50, 170), (62, 104), (110, 82), (334, 76), (402, 84), (472, 134), (552, 146), (588, 168),
                      (592, 206), (574, 220)],
                win=[(84, 130), (100, 96), (330, 88), (392, 94), (444, 132)], pillar=230, wheels=(160, 476), r=44, rad=16),
    'bigsuv': dict(body=[(46, 216), (42, 168), (50, 92), (78, 70), (372, 66), (420, 74), (486, 128), (566, 140), (600, 162),
                         (602, 208), (584, 222)],
                   win=[(70, 126), (82, 86), (368, 78), (410, 86), (458, 128)], pillar=250, wheels=(154, 486), r=46, rad=14),
    'pickup': dict(body=[(40, 214), (38, 140), (250, 140), (262, 76), (378, 72), (414, 78), (470, 130), (566, 140), (604, 160),
                         (606, 208), (588, 222)],
                   win=[(276, 128), (282, 86), (372, 82), (404, 88), (448, 128)], pillar=330, wheels=(150, 492), r=46, rad=10),
    'van': dict(body=[(56, 214), (52, 120), (66, 70), (110, 58), (404, 58), (456, 70), (520, 128), (580, 146), (598, 172),
                      (598, 208), (580, 220)],
                win=[(82, 122), (92, 80), (398, 72), (444, 84), (488, 126)], pillar=300, wheels=(164, 470), r=42, rad=14),
}


def rounded(points, r):
    """Closed path through points with each corner rounded by up to r px."""
    n, out = len(points), []
    for i in range(n):
        p0, p1, p2 = points[i - 1], points[i], points[(i + 1) % n]
        def toward(a, b, d):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
            d = min(d, L / 2)
            return (a[0] + dx / L * d, a[1] + dy / L * d)
        a, b = toward(p1, p0, r), toward(p1, p2, r)
        out.append(('M' if i == 0 else 'L') + f'{a[0]:.1f},{a[1]:.1f} Q{p1[0]},{p1[1]} {b[0]:.1f},{b[1]:.1f}')
    return ' '.join(out) + ' Z'


def wheel(cx, r):
    cy = GROUND - r
    spokes = ''.join(f'<rect x="{cx - 3}" y="{cy - r * 0.55:.1f}" width="6" height="{r * 1.1:.1f}" rx="3" fill="#9aa3a6" '
                     f'transform="rotate({a} {cx} {cy})"/>' for a in (0, 72, 144, 216, 288))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="#11171a"/>'            # wheel well
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1d2427"/>'                # tyre
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="#c9cfd1"/>'     # rim
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62:.1f}" fill="none" stroke="#e9eced" stroke-width="2"/>'
            + spokes +
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.16:.1f}" fill="#5d686c"/>')


def svg(kind):
    s = SHAPES[kind]
    body, win = s['body'], s['win']
    xs = [p[0] for p in body]
    front, rear = max(xs), min(xs)
    ys = [p[1] for p in body]
    belt = max(p[1] for p in win) + 4                                   # shoulder line just under the windows
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">',
             '<defs><linearGradient id="bbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/>'
             '<stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/>'
             '</linearGradient><linearGradient id="bbw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b474c"/>'
             '<stop offset="1" stop-color="#151b1e"/></linearGradient></defs>',
             f'<ellipse cx="{(front + rear) / 2:.0f}" cy="{GROUND + 6}" rx="{(front - rear) / 2 + 20:.0f}" ry="12" fill="#000" opacity=".14"/>',
             f'<path d="{rounded(body, s["rad"])}" fill="var(--car,#d8dde0)"/>',
             f'<path d="{rounded(win, 10)}" fill="url(#bbw)"/>']
    if s['pillar']:
        parts.append(f'<rect x="{s["pillar"] - 5}" y="{min(p[1] for p in win) - 2}" width="10" height="{belt - min(p[1] for p in win)}" '
                     'fill="var(--car,#d8dde0)"/>')
    if kind == 'pickup':  # cab / bed split and tailgate seam
        parts.append(f'<path d="M256,142 L256,{GROUND - 44}" stroke="#000" stroke-opacity=".28" stroke-width="3"/>'
                     f'<path d="M46,150 L240,150" stroke="#000" stroke-opacity=".15" stroke-width="4"/>')
    parts.append(f'<path d="{rounded(body, s["rad"])}" fill="url(#bbg)"/>')
    # shoulder highlight + rocker shade + door line + handle
    parts += [f'<path d="M{rear + 14},{belt + 8} L{front - 30},{belt + 8}" stroke="#fff" stroke-opacity=".45" stroke-width="3" '
              'stroke-linecap="round"/>',
              f'<path d="M{rear + 30},{GROUND - 30} L{front - 40},{GROUND - 30}" stroke="#000" stroke-opacity=".18" stroke-width="10" '
              'stroke-linecap="round"/>']
    if s['pillar']:
        parts.append(f'<path d="M{s["pillar"]},{belt} L{s["pillar"] + 2},{GROUND - 46}" stroke="#000" stroke-opacity=".22" '
                     'stroke-width="2"/>')
        parts.append(f'<rect x="{s["pillar"] - 46}" y="{belt + 16}" width="22" height="6" rx="3" fill="#000" fill-opacity=".25"/>')
    # lights: headlamp at the front, tail lamp at the rear
    fy = [p[1] for p in body if p[0] > front - 60]
    ry = [p[1] for p in body if p[0] < rear + 40]
    parts += [f'<rect x="{front - 34}" y="{min(fy) + 6}" width="30" height="11" rx="5" fill="#fff6c8" stroke="#00000033"/>',
              f'<rect x="{rear - 2}" y="{min(ry) + 8}" width="18" height="12" rx="4" fill="#c8262c"/>',
              f'<rect x="{front - 22}" y="{GROUND - 46}" width="20" height="10" rx="4" fill="#1d2427" fill-opacity=".55"/>']
    for x in s['wheels']:
        parts.append(wheel(x, s['r']))
    parts.append('</svg>')
    return ''.join(parts)


def js_data():
    return 'window.BB_CARSVG=' + json.dumps({k: svg(k) for k in SHAPES}, separators=(',', ':')) + ';'


if __name__ == '__main__':  # preview sheet
    html = '<body style="background:#f3f5f5;display:grid;grid-template-columns:repeat(2,640px);gap:20px;padding:20px">' + ''.join(
        f'<div style="--car:{c}">{svg(k)}<p style="font:14px sans-serif">{k}</p></div>'
        for k, c in zip(SHAPES, ['#c8102e', '#f2f4f5', '#1f3a5f', '#8a9399', '#2b2f33', '#e9eef0', '#6b1d1d']))
    open('/tmp/claude-0/-home-user-wpsites-sessions/e05ccdd5-0131-544e-b7dd-0be6172163c1/scratchpad/cars.html', 'w').write(html)
