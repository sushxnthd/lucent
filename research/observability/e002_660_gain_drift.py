"""E002-660: LED phase calibration nonidentifiability under phase-correlated gain.
Dependency-free deterministic counterexample. Run: python e002_660_gain_drift.py
"""
from fractions import Fraction as F

def normalize(xs):
    total = sum(xs)
    assert total > 0
    return [x / total for x in xs]

def observation(kernel, gain):
    return [k*g for k,g in zip(kernel,gain)]

def run():
    # Two distinct shutter kernels produce identical unsaturated phase scans
    # when per-phase illumination or detector gain is unobserved.
    rectangular = [F(1,4)]*4
    asymmetric = [F(1,10), F(1,10), F(2,5), F(2,5)]
    gain_a = [F(1)]*4
    gain_b = [a/b for a,b in zip(rectangular,asymmetric)]
    assert observation(rectangular,gain_a) == observation(asymmetric,gain_b)
    assert all(F(0)<x<=F(5,2) for x in gain_b)
    assert normalize(observation(asymmetric,gain_b)) == rectangular
    # Contemporaneous flat-field reference independently measures gain.
    assert normalize([y/g for y,g in zip(observation(asymmetric,gain_b),gain_b)]) == asymmetric
    y = observation(asymmetric,gain_b)
    low = [v/F(5,2) for v in y]
    high = [v/F(1,2) for v in y]
    assert all(lo<=k<=hi for lo,k,hi in zip(low,asymmetric,high))
    assert all(lo<=k<=hi for lo,k,hi in zip(low,rectangular,high))
    print('PASS E002-660: identical unsaturated phase scans, distinct kernels; flat-field disambiguates')
    print('gain drift:', [str(v) for v in gain_b])

if __name__ == '__main__':
    run()
