"""Fetch live _elementor_data, patch it in place, write it back (refuses if the post changed meanwhile).

usage in a script:
    from patch import fetch, save, find
    doc = fetch(32)                      # pages; fetch(33, 'elementor_library') for templates
    w = find(doc['data'], lambda e: e['settings'].get('_title') == '...')
    w['settings']['text'] = '...'
    save(doc)
"""
import json, os, subprocess, datetime
import el  # host guard

D = os.path.dirname(os.path.abspath(__file__))
TYPES = {'pages': 'pages', 'elementor_library': 'elementor_library'}


def _api(method, path, body=None):
    args = ['curl', '-sS', '-X', method, '-u', os.environ['WP_USER'] + ':' + os.environ['WP_APP_PASSWORD'],
            os.environ['WP_URL'].rstrip('/') + '/wp-json/' + path]
    if body is not None:
        f = os.path.join(D, 'payload.json'); open(f, 'w').write(json.dumps(body))
        args[6:6] = ['-H', 'Content-Type: application/json', '--data-binary', '@' + f]
    return json.loads(subprocess.run(args, capture_output=True, text=True).stdout)


def fetch(pid, kind='pages', backup=True):
    r = _api('GET', f'wp/v2/{kind}/{pid}?context=edit&_fields=id,modified,meta')
    data = json.loads(r['meta']['_elementor_data'] or '[]')
    if backup:
        os.makedirs(os.path.join(D, 'backups'), exist_ok=True)
        stamp = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        json.dump(data, open(os.path.join(D, 'backups', f'{pid}-{stamp}.json'), 'w'))
    return {'id': pid, 'kind': kind, 'modified': r['modified'], 'data': data}


def save(doc, regen=True):
    now = _api('GET', f"wp/v2/{doc['kind']}/{doc['id']}?context=edit&_fields=modified")['modified']
    if now != doc['modified']:
        raise SystemExit(f"{doc['id']} changed since fetch ({doc['modified']} -> {now}); re-run to patch the newer version")
    r = _api('POST', f"wp/v2/{doc['kind']}/{doc['id']}", {'meta': {'_elementor_data': json.dumps(doc['data'])}})
    print(doc['id'], 'saved' if 'id' in r else r)
    if regen and 'id' in r:
        el.regen(doc['id'])
    return r


def walk(els):
    for e in els:
        yield e
        yield from walk(e['elements'])


def find(els, pred, many=False):
    hits = [e for e in walk(els) if pred(e)]
    if many:
        return hits
    if len(hits) != 1:
        raise SystemExit(f'expected 1 match, got {len(hits)}')
    return hits[0]


def titled(t):
    return lambda e: e['settings'].get('_title') == t
