"""E002-734: falsify empirical speed quantiles as hard Lipschitz ceilings.
Synthetic only. No human or camera data. Standard-library deterministic simulation.
"""
import random
from statistics import mean

SEED=7342026
N_CAL=200
N_TEST=10000
A=1.0
GAP=0.12

def speed(rng):
    # Synthetic mixture: common slower and rare rapid closures, units/s.
    return rng.uniform(6,10) if rng.random()<0.98 else rng.uniform(25,35)

def experiment(seed):
    rng=random.Random(seed)
    cal=[speed(rng) for _ in range(N_CAL)]
    test=[speed(rng) for _ in range(N_TEST)]
    q95=sorted(cal)[int(.95*(N_CAL-1))]
    maximum=max(cal)
    # Piecewise linear full-open -> zero -> full-open trajectory.
    # Fits between point samples if 2*A/v <= GAP.
    hidden=[v for v in test if 2*A/v <= GAP]
    return {'q95':q95,'max':maximum,'hidden_count':len(hidden),
            'q95_false_exclusion':(2*A > q95*GAP) and bool(hidden),
            'max_false_exclusion':(2*A > maximum*GAP) and bool(hidden)}

def main():
    outcomes=[experiment(SEED+i) for i in range(100)]
    assert all(x['q95_false_exclusion'] for x in outcomes)
    assert all(x['hidden_count']>0 for x in outcomes)
    print('E002-734 synthetic speed-mixture falsification')
    print('100 seeded disjoint calibration/test replicates (synthetic only)')
    print('q95 false-exclusion replicates:',sum(x['q95_false_exclusion'] for x in outcomes))
    print('sample-maximum false-exclusion replicates:',sum(x['max_false_exclusion'] for x in outcomes))
    print('mean hidden closures in 10000 test trajectories:',round(mean(x['hidden_count'] for x in outcomes),2))
    print('Neither observed quantile nor observed maximum certifies a hard speed ceiling')

if __name__=='__main__': main()
