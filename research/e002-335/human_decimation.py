"""E002-335: frame-index decimation of manually annotated EyeBlink8 RGB videos.
Usage: python human_decimation.py <clip-id> <path-to-tag>
This is NOT independently synchronized high-speed eye-reference validation.
"""
import csv, json, pathlib, sys
def mask(rows, test):
    return sum(1<<p for p in range(3) if any(r[0]%3==p and test(r) for r in rows))
def parse(path):
    out=[]
    for line in pathlib.Path(path).read_text().splitlines():
        a=line.split(":")
        if len(a)>=7 and a[0].isdigit():
            out.append((int(a[0]),int(a[1]),a[2]==a[4]==a[6]=="X",a[3]=="C" or a[5]=="C"))
    return out
def groups(rows):
    cur=[]
    for r in rows:
        if r[1]<0:
            if cur: yield cur
            cur=[]
        elif cur and (r[1]!=cur[-1][1] or r[0]!=cur[-1][0]+1):
            yield cur;cur=[r]
        else:cur.append(r)
    if cur:yield cur
def analyze(clip,path):
    rows=parse(path);results=[]
    for g in groups(rows):
        fc=[r[0] for r in g if r[2] and r[3]]
        c=mask(g,lambda r:r[2] and r[3])
        assert c==sum(1<<p for p in set(n%3 for n in fc))
        for p in range(3):
            assert bool(c&(1<<p))==any(n%3==p for n in fc)
        if any(fc[i:i+3]==list(range(fc[i],fc[i]+3)) for i in range(len(fc)-2)):
            assert c==7
        results.append(dict(clip=clip,blink=g[0][1],start=g[0][0],end=g[-1][0],
            native_frames=len(g),clean_fc_frames=len(fc),
            blink_mask=mask(g,lambda r:True),fc_mask=c))
    return dict(clip=clip,frames=len(rows),events=len(results),
       closure_eligible=sum(x["clean_fc_frames"]>0 for x in results),
       lost_closure_phase_event_pairs=sum(3-x["fc_mask"].bit_count() for x in results if x["clean_fc_frames"]>0),
       events_data=results)
if __name__=="__main__":
    z=analyze(int(sys.argv[1]),sys.argv[2])
    print(json.dumps(z,indent=2))
