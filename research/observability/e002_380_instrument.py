"""E002-380 independent synthetic shutter instrument, not human data."""
from math import floor
import json
F=1/30;w=.010;D=.015;m=.004
def overlap(a,b,c,d):return max(0.,min(b,d)-max(a,c))
def sample(phase,offsets):
    best=0.
    for delta in offsets:
        for n in range(-2,5):
            start=n*F+delta
            best=max(best,overlap(phase,phase+D,start,start+w))
    return best
def run():
    cases={
      "five_rows":[0,.005,.010,.015,.020],
      "center_three":[.005,.010,.015],
      "narrow_1ms":[0,.00025,.0005,.00075,.001],
      "adversarial_2ms":[.002,.005,.010,.015,.018],
    }
    out={}
    for name,offsets in cases.items():
        vals=[sample(i*F/5000,offsets) for i in range(5000)]
        out[name]={"phase_fraction":sum(x+1e-12>=m for x in vals)/5000,
                   "worst_overlap_ms":1000*min(vals)}
    assert out["five_rows"]["phase_fraction"]==1
    assert out["center_three"]["phase_fraction"]<1
    assert out["narrow_1ms"]["phase_fraction"]<1
    assert out["adversarial_2ms"]["phase_fraction"]<1
    print(json.dumps(out,indent=2))
if __name__=="__main__":run()
