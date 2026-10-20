"""Independent synthetic checker; no human recordings."""
from fractions import Fraction
import numpy as np
from instrument import circle,transform,conic_ratio,area_ratio,qcritical,sign_gate
rng=np.random.default_rng(20261020)
worst_conic=0.
for _ in range(1000):
    rho=float(rng.uniform(.15,.75))
    H=np.eye(3)
    H[:2,:2]=rng.normal(size=(2,2))*.25+np.eye(2)
    H[:2,2]=rng.normal(size=2)*.1
    H[2,:2]=rng.normal(size=2)*.08
    if abs(np.linalg.det(H))<.25:continue
    Cp=transform(circle(rho),H)*float(rng.uniform(.2,5))
    Ci=transform(circle(1),H)*float(rng.uniform(.2,5))
    e=abs(conic_ratio(Cp,Ci)-rho)
    worst_conic=max(worst_conic,e)
    assert e<1e-9
worst_area=0.
for _ in range(1000):
    rho=float(rng.uniform(.1,.9));q=float(rng.uniform(-.95,.95))
    Ap=np.pi*rho*rho/(1-q*q*rho*rho)**1.5
    Ai=np.pi/(1-q*q)**1.5
    e=abs(area_ratio(rho,q)-np.sqrt(Ap/Ai))
    worst_area=max(worst_area,e)
    assert e<1e-12
q=qcritical(.4,.05)
assert abs(1-area_ratio(.4,q)/.4-.05)<1e-12
assert 1-area_ratio(.4,q-1e-4)/.4<.05
assert 1-area_ratio(.4,q+1e-4)/.4>.05
assert Fraction(2,5)/10==Fraction(1,2)/Fraction(25,2)
assert Fraction(11,10)==Fraction(9,10)*Fraction(11,9)
assert sign_gate(.06,.05)=="DILATION"
assert sign_gate(.05,.05)=="ABSTAIN"
assert sign_gate(-.06,.05)=="CONSTRICTION"
print(dict(projective_tests=1000,area_tests=1000,
           max_conic_error=worst_conic,max_area_error=worst_area,
           critical_q=q,human_validation="NOT RUN"))
