"""Independent exact-rational E002-300 boundary and collision checker."""
from fractions import Fraction as F

def upper(rho, mu=F(2,25), theta=F(4,5)):
    return 1-rho+rho*min(F(1),mu/theta)

def check():
    assert upper(F(7,8))==F(17,80)
    assert upper(F(8,9))==F(1,5)
    assert upper(F(9,10))==F(19,100)
    assert upper(F(4,5))>F(1,5) # reject mutated 80%-coverage claim
    assert F(4,5)*F(1,10)==F(2,25) # exact collision: 0.08 constant vs 0.8 for 10%
    # Optional independent finite-support linear program.
    try:
        import numpy as np
        from scipy.optimize import linprog
        levels=np.array([0.,0.08,0.8,1.])
        z=(levels>=0.8).astype(float)
        r=linprog(-z,A_eq=np.vstack([np.ones(4),levels]),
                  b_eq=np.array([1.,0.08]),bounds=(0,None),method="highs")
        assert r.success and abs(-r.fun-0.1)<1e-10
        print("independent LP passed")
    except ImportError:
        print("scipy not installed; rational checks passed")
    print("E002-300 rational checker PASSED")
if __name__=="__main__":check()
