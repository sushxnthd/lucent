"""Virtual shutter instrument benchmark. Synthetic only; not human validation."""
from fractions import Fraction as F

def aperture(t, knots):
    for (t0,a0),(t1,a1) in zip(knots,knots[1:]):
        if t0 <= t <= t1:
            return a0+(a1-a0)*(t-t0)/(t1-t0)
    raise ValueError("outside trajectory")

def mean(knots,left,right):
    ts=[left]+[t for t,_ in knots if left<t<right]+[right]
    return sum((aperture(x,knots)+aperture(y,knots))*(y-x)/2 for x,y in zip(ts,ts[1:]))/(right-left)

def predict(m0,m1,e0,e1,g,v,c=F(0)):
    a0=m0-v*e0/2
    a1=m1-v*e1/2
    return "EXCLUDE_MATHEMATICALLY" if a0>c and a1>c and a0+a1-2*c>v*g else "DO_NOT_EXCLUDE"

def run():
    e=F(1,100);g=F(4,100);v=F(100)
    t0=F(0);t1=e;t2=e+g;t3=t2+e
    cases={
        "always_open":[(t0,F(2)),(t3,F(2))],
        "hidden_closure":[(t0,F(2)),(t1,F(2)),(t1+F(2,100),F(0)),(t2,F(2)),(t3,F(2))],
        "edge_closure":[(t0,F(2)),(t1,F(1)),(t1+F(1,100),F(0)),(t2,F(2)),(t3,F(2))],
    }
    for name,knots in cases.items():
        speed=max(abs((b-a)/(tb-ta)) for (ta,a),(tb,b) in zip(knots,knots[1:]))
        assert speed<=v,(name,speed)
        m0=mean(knots,t0,t1);m1=mean(knots,t2,t3)
        truth=min(a for _,a in knots)==0
        verdict=predict(m0,m1,e,e,g,v)
        assert not(truth and verdict=="EXCLUDE_MATHEMATICALLY")
        print(name,m0,m1,truth,verdict)
    # Timing/exposure nuisance can reverse a nominal exclusion.
    m=F(2);short_gap=F(29,1000)
    assert predict(m,m,e,e,short_gap,v)=="EXCLUDE_MATHEMATICALLY"
    assert predict(m,m,e,e,short_gap+F(2,1000),v)=="DO_NOT_EXCLUDE"
    assert predict(m,m,e+F(2,1000),e+F(2,1000),short_gap,v)=="DO_NOT_EXCLUDE"
    print("PASS: three trajectories and two adversarial nuisance checks")

if __name__=="__main__":run()
