"""E002-668: exact shutter-integration counterexample to point-phase grid guarantees.
Stdlib only: python3 research/observability/e002_668_exposure_dilution.py
"""
from fractions import Fraction as F

def overlap(a,b,c,d):
    return max(F(0),min(b,d)-max(a,c))

def exposure_average(start, width, closure_start, closure_width):
    """Unit-open aperture; zero on closure; rectangular exposure; no wrap."""
    return F(1)-overlap(start,start+width,closure_start,closure_start+closure_width)/width

def detected(start,width,closure_start,closure_width,threshold):
    return exposure_average(start,width,closure_start,closure_width)<=threshold

def run():
    # Prior phase-grid experiment: c=.30, epsilon=.05, six commands.
    # A commanded point inside the robust closure core does NOT ensure that
    # its finite exposure average crosses a closed-eye detector threshold.
    c=F(3,10); eps=F(1,20); n=6
    closure_start=F(1,3)-F(3,20)
    closure_end=closure_start+c
    center=F(1,3)
    assert closure_start+eps<center<closure_end-eps
    # A 0.60-cycle exposure centred on a fully closed instant:
    width=F(3,5); start=center-width/2
    avg=exposure_average(start,width,closure_start,c)
    assert avg==F(1,2)
    assert not detected(start,width,closure_start,c,F(3,10))
    # All six commanded phases: circular periodic exposure averaging.
    def circular_avg(phase,width,lo,c):
        # Integrate periodic closure intervals over shutter window.
        a=phase-width/2; b=phase+width/2
        closed=sum((overlap(a,b,lo+k,lo+c+k) for k in (-2,-1,0,1,2)),F(0))
        return F(1)-closed/width
    values=[circular_avg(F(k,n),width,closure_start,c) for k in range(n)]
    assert all(v>F(3,10) for v in values)
    # Independent optical calibration: if width is narrow, a hit becomes observable.
    narrow=F(1,20)
    assert circular_avg(center,narrow,closure_start,c)==0
    # Exposure-fraction detection law: aperture <= tau requires
    # closed overlap fraction >= 1-tau; if width > c/(1-tau),
    # even perfect alignment cannot trigger detector.
    tau=F(3,10)
    assert width>c/(1-tau)
    print("PASS E002-668")
    print("closure_width",c,"exposure_width",width,"threshold",tau)
    print("central_exposure_average",avg,"six_phase_averages",values)
    print("critical_width",c/(1-tau))
if __name__=="__main__":
    run()
