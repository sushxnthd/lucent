"""Independent time-domain overlap oracle, distinct from cyclic arc union."""
from fractions import Fraction as Q
from random import Random
from e002_381_exact import certify,frozen

def direct(s,F,w,m,rows):
    for r in rows:
        start=s+Q(r["tau"]);stop=start+Q(r["D"])
        for k in range(-5,8):
            a=k*F+Q(r["delta"]);b=a+w
            if max(Q(0),min(stop,b)-max(start,a))>=m:return True
    return False

def oracle(F,w,m,rows):
    cuts={Q(0),F}
    for r in rows:
        for k in range(-5,8):
            t=k*F+Q(r["delta"]);u=Q(r["tau"]);D=Q(r["D"])
            for p in (t+m-u-D,t+w-m-u):
                if 0<=p<=F:cuts.add(p)
    cuts=sorted(cuts)
    probes=cuts+[(a+b)/2 for a,b in zip(cuts,cuts[1:])]
    misses=[p for p in probes if not direct(p,F,w,m,rows)]
    return not misses,misses[0] if misses else None

def run(n=2500):
    rng=Random(381)
    for i in range(n):
        F=Q(rng.randint(18,50),1000)
        w=F*Q(rng.randint(2,8),10)
        m=w*Q(rng.randint(1,10),10)
        rows=[dict(delta=F*Q(rng.randrange(1000),1000),
                   tau=F*Q(rng.randrange(-800,800),1000),
                   D=F*Q(rng.randrange(1,2000),1000))
              for _ in range(rng.randint(1,8))]
        yes,witness=certify(F,w,m,rows)
        independent,_=oracle(F,w,m,rows)
        assert yes==independent,(i,yes,independent)
        if not yes:assert not direct(witness,F,w,m,rows)
    F,w,m=Q(1,30),Q(1,100),Q(4,1000)
    for alpha,yes in [(Q(0),True),(Q(18,100),True),(Q(11,60),True),
                      (Q(19,100),False),(Q(20,100),False),(Q(1),False)]:
        assert oracle(F,w,m,frozen(alpha))[0]==yes
    print("PASS: 2500 randomized heterogeneous-row exact oracle tests and six frozen predictions")
if __name__=="__main__":run()
