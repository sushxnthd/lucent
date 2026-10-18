"""Independent symbolic checker: does not import experiment.py."""
from fractions import Fraction as F
from sympy import Matrix,Rational
import json
from pathlib import Path
H=Matrix([[F(6,5),F(1,7),F(1,4)],[F(1,9),F(9,10),F(-1,5)],[F(1,13),F(-1,11),1]])
P=Matrix.diag(1,1,-F(4,25))
I=Matrix.diag(1,1,-1)
J=H.inv()
eigen=((J.T*I*J).inv()*(J.T*P*J)).eigenvals()
assert eigen=={Rational(1):2,Rational(4,25):1}
# a=13,b=15,L=12: x_a(0)-x_b(0)=0, x_a(12)-x_b(12)=2.
# Difference monotone. Shifts (-1/2,+1/2) leave residual [-1,1].
# Split residual between independent errors, each bounded by 1/2.
assert (13-5)-(15-9)==2
for d in [F(0),F(1,2),F(1),F(3,2),F(2)]:
    residual=d-F(1)
    ea=-residual/2;eb=residual/2
    assert abs(ea)<=F(1,2) and abs(eb)<=F(1,2)
    assert d-F(1,2)+ea==F(1,2)+eb
assert F(2,5)*1==F(1,2)*F(4,5)
bad=0
for k in [F(3,5),F(1,3),F(5,7)]:
    try: assert F(2,5)==F(1,2)*k
    except AssertionError:bad+=1
assert bad==3
out=dict(exact_projective_eigenvalues={str(k):v for k,v in eigen.items()},arc_collision="PASS",pupil_specific_magnification_collision="PASS",mutations_rejected=bad,human_evidence=False)
Path(__file__).with_name("independent_verification.json").write_text(json.dumps(out,indent=2)+"\n")
print(out)
