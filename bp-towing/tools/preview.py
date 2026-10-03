"""Build a local preview of a draft: live <head> + draft's rendered Elementor content + live footer scripts."""
import wp, re, sys, json, urllib.request, random
E = 'https://bptowingservice.ca/wp-content/plugins/elementor'
EP = 'https://bptowingservice.ca/wp-content/plugins/elementor-pro'
EXTRA = [f'{E}/assets/lib/animations/styles/{a}.min.css' for a in ('fadeInUp', 'fadeInLeft', 'fadeInRight', 'zoomIn', 'fadeIn')] + \
        [f'{EP}/assets/css/widget-nav-menu.min.css', f'{EP}/assets/css/modules/motion-fx.min.css', f'{E}/assets/css/conditionals/e-swiper.min.css',
         f'{E}/assets/css/widget-social-icons.min.css', f'{E}/assets/css/widget-counter.min.css', f'{E}/assets/css/widget-nested-accordion.min.css']
def shell():
    import subprocess
    return subprocess.run(['curl', '-s', f'https://bptowingservice.ca/?nc={random.random()}'], capture_output=True, text=True).stdout
def build(pid, out, kind='pages', tpl_ids=()):
    h = shell()
    head = h[:h.index('<body')]
    body = re.search(r'<body[^>]*>', h).group(0)
    body = re.sub(r'page-id-\d+', f'page-id-{pid}', body).replace('class="', 'class="elementor-template-canvas elementor-page-%d ' % pid, 1)
    tail_start = h.find('</footer>', h.find('class="site-footer"')) + 9
    tail = h[tail_start:]
    css = ''.join(f'<link rel="stylesheet" href="{u}">' for u in EXTRA) + f'<script src="{EP}/assets/lib/smartmenus/jquery.smartmenus.min.js"></script>'
    css += ''.join(f'<link rel="stylesheet" href="https://bptowingservice.ca/wp-content/uploads/elementor/css/post-{i}.css?v={random.random()}">' for i in (pid, *tpl_ids))
    content = wp.req(f'wp/v2/{kind}/{pid}?context=edit')['content']['rendered']
    open(out, 'w').write(head.replace('</head>', css + '</head>') + body + f'<div data-elementor-type="wp-page" data-elementor-id="{pid}" class="elementor elementor-{pid}">' + content + '</div>' + tail)
if __name__ == '__main__':
    st = json.load(open('created.json'))
    key = sys.argv[1]
    build(st['drafts'][key], f'prev/{key}.html', tpl_ids=tuple(st['templates'].values()))
    print('ok')
