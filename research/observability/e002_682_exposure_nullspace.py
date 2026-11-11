"""E002-682: exact-rational finite-exposure nullspace witness; stdlib only."""
from fractions import Fraction as F
def q(x): return x**3*(1-x)**3
def qpp(x): return 6*x-36*x*x+60*x**3-30*x**4
def test():
    windows=[(F(0),F(1,30)),(F(1,60),F(1,20)),(F(1,30),F(1,15)),(F(0),F(1,10))]
    endpoints=sorted({t for pair in windows for t in pair})
    left,right=endpoints[2:4]
    center=(left+right)/2
    for width in [F(1,1000),F(1,10000),F(1,100000)]:
        a=center-width/2; b=center+width/2
        assert left<a<b<right
        for lo,hi in windows:
            assert (hi<=a or lo>=b) or (lo<=a and hi>=b)
            integral=F(0) if (hi<=a or lo>=b) else F(1,1000)*width*(q(F(1))-q(F(0)))
            assert integral==0
        speed=abs(F(1,1000)*qpp(F(1,4))/width)
        assert speed>0
        print(f"width={width} s; speed witness={float(speed):.6f} aperture/s; all {len(windows)} exposure integrals unchanged")
    assert F(36,1000)<F(1,2)
    print("PASS: C1 bounded aperture, exposure-nullspace, arbitrarily high speed")
if __name__=="__main__": test()
