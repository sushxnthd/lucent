"""E002-164 deterministic source-operator test; synthetic fixtures, no human physiology."""
from fractions import Fraction
from pathlib import Path
import json,math
N=90
def fold(x):
    assert len(x)==270
    return [(x[i]+x[i+90]+x[i+180])/3 for i in range(N)]
def main():
    b=Fraction(9,10)
    x=[Fraction(3)+b*Fraction(k,90) for k in range(270)]
    y=fold(x)
    slope=(y[-1]-y[0])/Fraction(89,30)
    assert slope==b/3 and y[0]==Fraction(39,10)
    a=[Fraction(4)]*270;c=a[:]
    for i in range(N):
        h=Fraction(i,90)
        a[i]+=h;a[i+90]-=h
        c[i]-=h;c[i+90]+=h
    assert a!=c and fold(a)==fold(c)==[Fraction(4)]*90
    harmonic={}
    for f in (1/3,2/3,1/2,1.0):
        xx=[math.sin(2*math.pi*f*k/90) for k in range(270)]
        yy=fold(xx)
        harmonic[str(f)]={"max_abs":max(map(abs,yy)),"rms":math.sqrt(sum(z*z for z in yy)/90)}
    assert harmonic[str(1/3)]["max_abs"]<1e-12
    assert harmonic[str(2/3)]["max_abs"]<1e-12
    assert sum(x)/270==sum(y)/90
    out={"id":"E002-164","kind":"EXACT_OPERATOR_NOT_HUMAN","rank":90,"nullity":180,
         "true_slope":float(b),"folded_slope_per_rgb_second":float(slope),
         "slope_retention":float(slope/b),"harmonics":harmonic,
         "opposite_trends_same_output":True,"equal_length_session_mean_preserved":True,
         "released_csv_lineage":"UNVERIFIED","five_second_human_waveform":"NOT_RUN"}
    Path(__file__).with_name("RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
