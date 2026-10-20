"""E002-320 restricted shutter-duty observability: stdlib only."""
from fractions import Fraction as F
def worst_phase_overlap(P,E,d):
    assert 0<E<=P and 0<=d<=P
    return max(F(0),d-(P-E))/2
def detect(P,E,d,a,eta):
    return a*worst_phase_overlap(P,E,d)>2*eta*E
def burden_bounds(y,E,T,eta):
    assert len(y)*E<=T
    return (E*sum(max(F(0),z-eta) for z in y)/T,
            (T-len(y)*E+E*sum(min(F(1),z+eta) for z in y))/T)
def threshold_bounds(y,E,T,eta,theta):
    assert 0<theta<1 and len(y)*E<=T
    return (E*sum(max(F(0),(max(F(0),z-eta)-theta)/(1-theta)) for z in y)/T,
            (T-len(y)*E+E*sum(min(F(1),min(F(1),z+eta)/theta) for z in y))/T)
if __name__=="__main__":
    P,E,eta=F(1,30),F(1,60),F(1,10)
    assert not detect(P,E,F(1,50),F(1),eta)
    assert detect(P,E,F(1,40),F(1),eta)
    print("PASS",float((P-E+4*eta*E)*1000),"ms")
