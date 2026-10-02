import json,sys;sys.path.insert(0,'.');from wp import *
bp=json.load(open('built_pages.json'));c=json.load(open('created.json'))
for pid,data in bp.items():
    r=req(f"wp/v2/pages/{c['drafts'][pid]}",'POST',{'meta':{'_elementor_data':json.dumps(data)}});print(pid,r.get('id'),r.get('_err'))
