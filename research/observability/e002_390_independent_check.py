#!/usr/bin/env python3
"""Independent oracle for E002-390; does not import tested certificate."""
import json
import numpy as np

F = 1 / 30
W = .010
N = 7
T = 6 * F + W
THETA = .2

def make(seed, n):
    rng = np.random.default_rng(seed)
    rows = []
    while len(rows) < n:
        c = rng.uniform(.030, .175)
        m = rng.uniform(.03, .199)
        vl, vr = rng.uniform(35, 120, 2)
        a, b = c - (1 - m) / vl, c + (1 - m) / vr
        if a >= 0 and b <= T:
            rows.append((np.array([0, a, c, b, T]),
                         np.array([1, 1, m, 1, 1]), max(vl, vr)))
    return rows

def quadrature_mean(knots, values, a, b):
    t = a + (np.arange(4000) + .5) * (b-a) / 4000
    return np.mean(np.interp(t, knots, values))

def alternate_lower(means, speed):
    ts = np.arange(0, T + .000251, .0005)
    candidate = []
    for k, mu in enumerate(means):
        a = k * F
        b = a + W
        d = ((b-ts) * np.abs(b-ts) - (a-ts) * np.abs(a-ts)) / (2 * W)
        candidate.append(mu - speed*d)
    return np.max(np.stack(candidate), axis=0).min() - speed*.00025

def main():
    calibration = make(39001, 1000)
    speed = 1.1 * max(row[2] for row in calibration)
    held = make(39002, 1500)
    for x, y, v in held[:100]:
        means = np.array([quadrature_mean(x, y, k*F, k*F+W)
                          for k in range(N)])
        assert speed >= v
        assert alternate_lower(means, speed) <= y.min() + 1e-6
    c = (.010 + F) / 2
    a, b = c - .81 / 90, c + .81 / 90
    assert .010 < a < c < b < F
    x = np.array([0, a, c, b, T])
    y = np.array([1, 1, .19, 1, 1])
    means = np.array([quadrature_mean(x, y, k*F, k*F+W)
                      for k in range(N)])
    assert np.max(np.abs(means-1)) < 1e-12
    assert alternate_lower(means, 0) > THETA
    assert alternate_lower(means, speed) <= .19
    eligible = 0
    for x, y, v in held:
        crossing = (.2 - y[2]) / ((1-y[2])/(x[2]-x[1])) + (.2-y[2])/((1-y[2])/(x[3]-x[2]))
        if crossing > .002:
            eligible += 1
            lo = x[2] - (.2-y[2]) * (x[2]-x[1]) / (1-y[2])
            hi = x[2] + (.2-y[2]) * (x[3]-x[2]) / (1-y[2])
            assert any(k/1000 >= lo and k/1000 + .00025 <= hi
                       for k in range(int(lo*1000)-2, int(hi*1000)+2))
    result = {'independent_check': 'PASS', 'dense_quadrature_cases': 100,
              'collision': 'verified', 'eligible_reference_cases': eligible,
              'bound_method': 'absolute-value antiderivative',
              'no_import_from_primary': True}
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    main()
