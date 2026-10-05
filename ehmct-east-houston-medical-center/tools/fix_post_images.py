"""Blog posts were imported without their images: copy missing inline images from ehmct.com into the media library,
point the post content at the copies, and set the first image as featured image when the featured id is missing.
Only <img> src/class/srcset are touched in post content. Idempotent (map saved in post_images.json)."""
import json, os, re, subprocess, tempfile
from patch import _api

U = os.environ['WP_URL'].rstrip('/'); A = os.environ['WP_USER'] + ':' + os.environ['WP_APP_PASSWORD']
MAPF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'post_images.json')
done = json.load(open(MAPF)) if os.path.exists(MAPF) else {}

def code(u):
    return subprocess.run(['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', u], capture_output=True, text=True).stdout

def upload(src, alt):
    if src in done: return done[src]
    live = re.sub(r'https?://[^/]+', 'https://ehmct.com', src)
    fn = os.path.basename(src.split('?')[0]); tmp = os.path.join(tempfile.gettempdir(), fn)
    subprocess.run(['curl', '-sS', '-o', tmp, live], check=True)
    ctype = 'image/webp' if fn.endswith('.webp') else ('image/png' if fn.endswith('.png') else 'image/jpeg')
    r = json.loads(subprocess.run(['curl', '-sS', '-X', 'POST', '-u', A, '-H', 'Content-Disposition: attachment; filename=' + fn,
                                   '-H', 'Content-Type: ' + ctype, '--data-binary', '@' + tmp, U + '/wp-json/wp/v2/media'],
                                  capture_output=True, text=True).stdout)
    _api('POST', f"wp/v2/media/{r['id']}", {'alt_text': alt})
    done[src] = {'id': r['id'], 'url': r['source_url']}; json.dump(done, open(MAPF, 'w'), indent=1)
    return done[src]

posts = _api('GET', 'wp/v2/posts?per_page=100&status=publish,future,draft&context=edit&_fields=id,slug,featured_media,content')
for p in posts:
    c = p['content']['raw']; new = c; first = None
    for tag in re.findall(r'<img[^>]+>', c):
        src = re.search(r'src="([^"]+)"', tag).group(1)
        if src not in done and code(src) == '200':
            continue
        alt = (re.search(r'alt="([^"]*)"', tag) or [None, ''])[1]
        m = upload(src, alt)
        t2 = tag.replace(src, m['url'])
        t2 = re.sub(r'wp-image-\d+', 'wp-image-%d' % m['id'], t2)
        t2 = re.sub(r'\s(srcset|sizes)="[^"]*"', '', t2)
        new = new.replace(tag, t2); first = first or m
    body = {}
    if new != c: body['content'] = new
    if first and 'id' not in _api('GET', f"wp/v2/media/{p['featured_media']}?_fields=id"):
        body['featured_media'] = first['id']
    if body:
        r = _api('POST', f"wp/v2/posts/{p['id']}", body)
        print(p['id'], p['slug'], 'updated', list(body), 'ok' if 'id' in r else r)
