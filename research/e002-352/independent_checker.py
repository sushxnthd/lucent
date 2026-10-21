"""Independent phase-erasure checker; native RGB manual annotation only."""
from pathlib import Path
from collections import defaultdict
import json
p=Path(__file__).with_name("holdout_clean_frames.txt")
events={}
for line in p.read_text().splitlines():
    key, sep, values=line.partition(":")
    assert sep
    events[int(key)]=[int(v) for v in values.split(",") if v]
assert len(events)==38
eligible=[v for v in events.values() if v]
assert len(eligible)==32
assert sum(len(v)==1 for v in eligible)==1
assert sum(len(v)==2 for v in eligible)==7
assert all(b-a==1 for v in eligible for a,b in zip(v,v[1:]))
out={}
for m in (2,3,4,5,6):
    direct=sum(not any(x%m==phase for x in v) for v in eligible for phase in range(m))
    residue=sum(m-len(set(x%m for x in v)) for v in eligible)
    formula=sum(max(0,m-len(v)) for v in eligible)
    assert direct==residue==formula
    out[m]={"erased":direct,"total":m*len(eligible),"fraction":direct/(m*len(eligible))}
assert [out[m]["erased"] for m in out]==[1,9,27,53,82]
assert out[2]["fraction"]<=0.05 and out[3]["fraction"]<=0.15
print(json.dumps(out,indent=2))
