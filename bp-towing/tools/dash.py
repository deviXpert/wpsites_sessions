import re
D='—–'
TOK=re.compile(r'(<!--.*?-->|<(style|script)\b.*?</\2>|<[^>]+>|\[[^\]]*\])',re.S|re.I)
BLOCK=re.compile(r'<(/?(p|li|h[1-6]|br|div|td|th|tr|ul|ol)\b)[^>]*>',re.I)
WS='[ \t ]'
DASH=re.compile(WS+'*(?:['+D+r']|(?<![\w-])--(?![-\w>]))'+WS+'*')
PRON=r"(we|you|they|it|i|that|this|there|just|so|ours|our|these|those|he|she|here)\b"
def plain(s):
    s=BLOCK.sub('\n',s);s=re.sub(r'<[^>]+>','',s);return s
def fix(s):
    if not any(c in s for c in D) and '--' not in s: return s
    full=s
    def proc_text(text,start):
        r=[];i=0;cap=set()
        for m in DASH.finditer(text):
            r.append(text[i:m.start()]);i=m.end()
            before=text[:m.start()];after=text[m.end():]
            nxt=after if after.strip() else plain(full[start+m.end():]).lstrip('  ')
            bfull=plain(full[:start])+before
            if re.search(r'\d$',before) and re.match(r'\d',nxt): r.append(' to ');continue
            seg=re.split(r'[.!?|:\n]',bfull)[-1]; words=len(seg.split())
            if words==0 or nxt=='' or re.match(r'[)\]\n:,.;]',nxt):
                r.append(' ' if m.group(0)[:1].isspace() and nxt[:1] not in (')',']',',','.',';',':') and words else ('' if words else (' ' if m.group(0)[:1].isspace() else '')));continue
            if 'SERVICE' in seg and nxt.upper().startswith('IN CALGARY'): r.append(' ');continue
            if seg.strip().lower() in ('yes','no','possibly','absolutely') or re.match(r'but\b',nxt): r.append(', ');continue
            if nxt[0].isupper(): r.append(': ');continue
            if words>5 and re.match(PRON,nxt,re.I) and after:
                r.append('. ');cap.add(m.end());continue
            r.append(': ' if words<=5 else ', ')
        r.append(text[i:]);out=''.join(r)
        # capitalise after inserted periods
        return re.sub(r'(?<=[a-z0-9]\. )('+PRON+')',lambda mm:mm.group(1)[0].upper()+mm.group(1)[1:],out) if cap else out
    res=[];last=0
    for m in TOK.finditer(s):
        res.append(proc_text(s[last:m.start()],last));res.append(m.group(0));last=m.end()
    res.append(proc_text(s[last:],last))
    return ''.join(res)
if __name__=='__main__':
    for t in ['WELCOME TO BP TOWING SERVICE —in Calgary','About BP Towing Service — <span>Calgary\'s Local</span>','<li><strong>Breakdown towing</strong> – dead battery</li>','Very heavy (800–1,000 lbs)','Nights, weekends, Christmas Day, Canada Day – we never close.','Special Vehicle Towing in Calgary | BP Towing – Expert','Stranded? Get a free tow quote in under 60 seconds – no obligation.','Pull over as far as possible – Onto the shoulder','(over 5,000 lbs – ask us)','Possibly – but heavy','might be flimsy or missing – ours are pro','.x{--bp:1} a::after']:
        print(repr(fix(t)))
