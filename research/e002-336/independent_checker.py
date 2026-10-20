"""Independent exhaustive 32-corner oracle and 2000 randomized tests."""
import itertools,math,random
from clock_gate import ClockGate
def oracle(g,t):
    u=(t-g.t0)/(g.t1-g.t0)
    terms=((1-u)*g.anchor_error0,u*g.anchor_error1,
      g.drift_lipschitz*min(t-g.t0,g.t1-t),
      g.rgb_event_error,g.reference_event_error)
    return [sum(s*x for s,x in zip(signs,terms))
      for signs in itertools.product((-1,1),repeat=5)]
def run():
    rng=random.Random(336)
    for i in range(2000):
        T=rng.uniform(.1,100)
        g=ClockGate(0,T,*(rng.uniform(0,.04) for _ in range(5)))
        t=rng.uniform(0,T)
        arr=oracle(g,t);B=g.bound(t)
        assert math.isclose(max(arr),B,rel_tol=1e-12,abs_tol=1e-12)
        assert math.isclose(min(arr),-B,rel_tol=1e-12,abs_tol=1e-12)
        assert g.classify(B+1e-5,t)=="positive"
        assert g.classify(-B-1e-5,t)=="negative"
    g=ClockGate(0,10,.004,.004,.001,.006,.010)
    assert math.isclose(g.bound(5),.025,abs_tol=1e-14)
    assert g.classify(.024,5)=="abstain"
    assert g.classify(.026,5)=="positive"
    try:
        g.bound(11);raise AssertionError("outside anchor gate failed")
    except ValueError: pass
    return {"randomized_corner_trials":2000,"frozen_midpoint_bound_s":g.bound(5),
      "lag_24ms":g.classify(.024,5),"lag_26ms":g.classify(.026,5),
      "outside_anchor_gate":"passed"}
if __name__=="__main__":
    import json
    print(json.dumps(run(),indent=2))
