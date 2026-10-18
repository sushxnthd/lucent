"""Independent exact-rational checker, no import of experiment or scipy."""
import json
from fractions import Fraction as F
import sympy as sp
def model(g=F(2,5),l=F(1),gaze=True):
    r=[[1,g,1,0,1],[1,0,0,0,0],[1,1,1,0,0],
       [0,0,0,1,l],[0,0,0,1,0]]
    if gaze:r.append([0,1,0,0,0])
    return sp.Matrix(r)
def exact_d(M):
    ns=M.T.nullspace();assert len(ns)==1
    v=ns[0];return abs(v[0])/sum(abs(x) for x in v)
def check(x):
    assert model(gaze=False)*sp.Matrix([0,F(-5,3),F(5,3),0,0])==sp.Matrix([1,0,0,0,0])
    assert exact_d(model())==F(5,23)
    assert exact_d(model(F(31,50),F(27,20)))==F(1350,5213)
    assert abs(x['six_feature_d']-float(F(5,23)))<1e-10
    assert abs(x['heldout_d']-float(F(1350,5213)))<1e-10
    assert abs(x['five_feature_d'])<1e-10 and abs(x['unbounded_optical_d'])<1e-10
    assert abs(x['calibrated_critical_amplitude']-float(F(19,125)))<1e-10
    assert abs(x['heldout_critical_amplitude']-float(F(9263,67500)))<1e-10
    assert x['randomized_primal_dual_checks']>=200
    assert x['max_primal_dual_gap']<1e-8
if __name__=='__main__':
    x=json.load(open('results.json'));check(x)
    for key in ['six_feature_d','heldout_d','calibrated_critical_amplitude']:
        y=dict(x);y[key]=0.0
        try:check(y)
        except AssertionError:pass
        else:raise AssertionError('mutation accepted: '+key)
    print('EXACT_RATIONAL_CHECK_PASS; THREE_MUTATIONS_REJECTED')
