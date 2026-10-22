"""Independent exact-rational E002-377 RGB/shutter checker (stdlib only)."""
from fractions import Fraction as Q
from random import Random
import json
def overlap(a,b,c,d):
    return max(Q(0),min(b,d)-max(a,c))
def brute(D,F,w,n=2000):
    best=None
    for j in range(n):
        phase=F*Q(j,n)
        peak=max(overlap(phase+k*F,phase+k*F+w,Q(0),D) for k in range(-2,int(D//F)+4))
        if best is None or peak<best[0]:best=(peak,phase)
    return best
def analytic(D,F,w):
    return min(w,max(Q(0),(D-F+w)/2))
def collision(D,F,w,phase,c,eps):
    maxerr=Q(0);count=0
    for k in range(-1,3):
        s=phase+k*F
        frac=overlap(s,s+w,Q(0),D)/w
        for row in range(6):
            for col in range(8):
                for ch in range(3):
                    a=Q(1,4)+Q((row+2*col+ch)%7,70)
                    delta=(c*[Q(1),Q(2,3),Q(1,3)][ch]*frac if row in (2,3) and col in (2,3,4,5) else Q(0))
                    # The midpoint of no-closure and closure is an exact RGB collision.
                    mid=a+delta/2
                    maxerr=max(maxerr,abs(mid-a),abs(mid-(a+delta)))
                    count+=1
    return maxerr<=eps,maxerr,count
def run():
    D,F,w,eps=Q(42),Q(50),Q(10),Q(1,100)
    m,phi=brute(D,F,w)
    assert (m,phi)==(Q(1),Q(41))
    assert m==analytic(D,F,w)
    cases={}
    for c,expected in [(Q(3,20),True),(Q(1,5),True),(Q(3,10),False)]:
        col,err,n=collision(D,F,w,phi,c,eps)
        assert col==expected and n==576 and err==c/Q(20)
        cases[str(c)]={"collision":col,"midpoint_error":str(err),"Xi":str(c*m/(2*eps*w))}
    f30=Q(100,3)
    m30,p30=brute(D,f30,w)
    assert m30==Q(28,3)==analytic(D,f30,w)
    assert not collision(D,f30,w,p30,Q(3,20),eps)[0]
    rng=Random(377)
    for _ in range(60):
        ff=Q(rng.randint(15,60));ww=Q(rng.randint(1,int(ff)));dd=Q(rng.randint(1,3*int(ff)))
        empirical,_=brute(dd,ff,ww,200)
        exact=analytic(dd,ff,ww)
        assert exact<=empirical<=exact+ff/200
    print(json.dumps({"status":"PASS","human":False,"worst_overlap_ms":str(m),
       "worst_phase_ms":str(phi),"F30_overlap_ms":str(m30),
       "RGB_components_per_case":576,"random_phase_cases":60,"cases":cases},indent=2))
if __name__=="__main__":run()
