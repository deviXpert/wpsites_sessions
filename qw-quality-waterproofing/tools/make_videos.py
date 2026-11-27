"""Builds 1280x720 muted hero background loops from the client's phone clips (sources live in the session scratchpad).
Landscape clips are scaled/cropped to fill; portrait clips are shown sharp in the centre over a blurred, enlarged copy of themselves
(cropping a 576px-wide portrait clip to 16:9 would mean a 2x+ zoom and a blurry picture)."""
import subprocess, sys, os
SRC = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LOOPS = {  # name: [(file, start, seconds, 'l'|'p')]
 'hero-general':   [('vframes/v6.mp4', 2, 3.5, 'l'), ('zext2/ext.mp4', 1, 3.5, 'p'), ('upv/u3.mp4', 0.3, 3.2, 'l'), ('vframes/v2.mp4', 0.5, 3.0, 'l'), ('vframes/v3.mp4', 0, 3.5, 'l')],
 'hero-exterior':  [('zext2/ext.mp4', 0, 9.0, 'p')],
 'hero-interior':  [('vframes/v2.mp4', 0.3, 4.0, 'l'), ('vframes/v1.mp4', 2, 4.0, 'p')],
 'hero-sump':      [('zsump/sump.mp4', 2, 7.0, 'p'), ('vframes/v8.mp4', 3, 4.0, 'p')],
 'hero-interlock': [('vframes/v6.mp4', 2, 4.0, 'l'), ('vframes/v3.mp4', 0, 3.5, 'l'), ('vframes/v7.mp4', 2, 3.5, 'p'), ('vframes/v4.mp4', 2, 3.0, 'l')],
}
FILL = 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1,fps=25'
for name, segs in LOOPS.items():
    args, parts = ['ffmpeg', '-nostdin', '-v', 'error', '-y'], []
    for i, (f, ss, t, kind) in enumerate(segs):
        args += ['-ss', str(ss), '-t', str(t), '-i', os.path.join(SRC, f)]
        if kind == 'l':
            parts.append(f'[{i}:v]{FILL}[s{i}]')
        else:
            parts.append(f'[{i}:v]split[a{i}][b{i}];[a{i}]{FILL},boxblur=24:2,eq=brightness=-0.08[bg{i}];'
                         f'[b{i}]scale=-2:720,setsar=1,fps=25[fg{i}];[bg{i}][fg{i}]overlay=(W-w)/2:0[s{i}]')
    chain = ';'.join(parts) + ';' + ''.join(f'[s{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=0[v]'
    out = os.path.join(OUT, f'qw-{name}.mp4')
    subprocess.run(args + ['-filter_complex', chain, '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '27', '-preset', 'slow',
                           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', '1.5', '-i', out, '-frames:v', '1', '-vf', 'scale=640:-1', out[:-4] + '.jpg'], check=True)
    print(name, os.path.getsize(out) // 1024, 'KB')
