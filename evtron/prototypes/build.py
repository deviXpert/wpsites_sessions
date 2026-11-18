import re,pathlib
L=pathlib.Path('../assets/brand-source/evtron-web-assets/logo/evtron-horizontal-dark.svg').read_text()
L=re.sub(r'<metadata>.*?</metadata>','',L,flags=re.S).replace(' xmlns:c2pa="http://c2pa.org/manifest"','')
def logo(cls,mid,w):
    s=L.replace('id="x"',f'id="{mid}"').replace('url(#x)',f'url(#{mid})').replace('<title>EVTRON</title>','')
    return s.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 76"',f'<svg class="{cls}" width="{w}" height="{round(w*76/360)}" role="img" aria-label="EVTRON" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 76"',1)
for f in pathlib.Path('src').glob('*.html'):
    t=f.read_text().replace('<!--LOGO-->',logo('logo','lm1',124)).replace('<!--LOGO2-->',logo('logo','lm2',132))
    pathlib.Path(f.name).write_text(t);print(f.name,len(t))
