"""Create/update the Code Snippets snippet that runs form_spam_filter.php (global scope, active). ID stored in created.json."""
import json, os, wp
D = os.path.dirname(os.path.abspath(__file__))
code = open(os.path.join(D, 'form_spam_filter.php')).read()
c = json.load(open(os.path.join(D, 'created.json')))
body = {'name': 'AAD – Block sales pitches in Elementor forms', 'desc': 'Rejects Elementor form submissions that pitch SEO, marketing, web design etc. or contain links. Source: aad-transport-recovery/tools/form_spam_filter.php',
        'code': code, 'scope': 'global', 'active': True, 'priority': 10}
sid = c.get('spam_snippet')
r = wp.req(f'code-snippets/v1/snippets/{sid}' if sid else 'code-snippets/v1/snippets', 'POST', body)
if '_err' in r: raise SystemExit(r)
c['spam_snippet'] = r['id']; json.dump(c, open(os.path.join(D, 'created.json'), 'w'), indent=1)
print('snippet', r['id'], 'active:', r.get('active'), 'scope:', r.get('scope'), 'error:', r.get('code_error'))
