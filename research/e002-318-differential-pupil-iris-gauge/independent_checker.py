"""Independent exact-symbolic checker; does NOT import model.py."""
import json
import sympy as sp
import numpy as np
H=sp.Matrix([[sp.Rational(6,5),sp.Rational(1,5),sp.Rational(1,3)],
             [sp.Rational(1,7),sp.Rational(9,8),sp.Rational(-1,4)],
             [sp.Rational(1,11),sp.Rational(-1,13),1]])
q=sp.Rational(3,5)
Qp=sp.diag(1,1,-q*q)
Qi=sp.diag(1,1,-1)
Cp=H.inv().T*Qp*H.inv()
Ci=H.inv().T*Qi*H.inv()
poly=sp.factor((Ci.inv()*Cp).charpoly().as_expr())
lam=sp.Symbol("lambda")
assert sp.simplify(poly-(lam-1)**2*(lam-q*q))==0

p0=sp.Rational(1,2)
p1=sp.Rational(53,100)
rho=sp.Rational(47,50)
qA=p1/rho
qB=p1*rho
assert qA>p0>qB
assert qA*rho==qB/rho==p1
critical=p0/p1
assert rho<critical<sp.Rational(19,20)
assert rho*(p1/p0)<1<sp.Rational(19,20)*(p1/p0)

rng=np.random.default_rng(118)
lower_violation=0.
upper_violation=0.
for _ in range(30000):
    r=rng.uniform(.55,1)
    Q=rng.uniform(.7,1.4)
    drift=rng.uniform(r,1/r)
    true=Q/drift
    lower_violation=max(lower_violation,r*Q-true)
    upper_violation=max(upper_violation,true-Q/r)
assert lower_violation<=1e-12 and upper_violation<=1e-12
out={"checker":"independent symbolic + randomized feasibility",
     "symbolic_characteristic":str(poly),
     "exact_eigenvalue_multiset":["1","1","9/25"],
     "exact_critical_rho":str(critical),
     "frozen_prediction_passed":True,
     "exact_bounded_opposite_trend_collision":True,
     "randomized_envelope_trials":30000,
     "max_lower_violation":lower_violation,
     "max_upper_violation":upper_violation,
     "human_data":"NOT RUN",
     "prior_art_warning":"Wang et al. (2019) already derive conic ratio"}
with open("independent_results.json","w") as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
