#!/usr/bin/env python3
"""E002-263 deterministic synthetic geometry test; NOT human validation."""
import json
import math
import random
from fractions import Fraction
from pathlib import Path

SEED = 2632026
N = 4000
R = 0.35
K_VALUES = [0.0, 0.2, 0.35, 0.5, 0.7, 0.8]
PIXEL_IRIS_SPAN = 120.0
SIGMA_PX = 0.5


def transform(x, k):
    return x / (1.0 + k * x)


def cross_ratio(a, b, c, d):
    return ((a - b) * (c - d)) / ((a - c) * (b - d))


def inferred_radius_from_cr(a, b, c, d):
    cr = cross_ratio(a, b, c, d)
    if not 0.0 <= cr <= 1.0:
        return None
    root = math.sqrt(cr)
    return (1.0 - root) / (1.0 + root)


def naive_radius(a, b, c, d):
    return (c - b) / (d - a)


def endpoints(k, r=R, shift=0.0, nonlinear=0.0):
    def f(x):
        return transform(x, k) + nonlinear * x ** 3
    return (f(-1), f(shift-r), f(shift+r), f(1))


def rms(xs):
    return math.sqrt(sum(x*x for x in xs) / len(xs))


def main():
    # Independent exact-rational invariant check, not just floating point.
    exact_checks = 0
    for r in [Fraction(1, 5), Fraction(7, 20), Fraction(3, 5)]:
        for k in [Fraction(0), Fraction(1, 5), Fraction(7, 20), Fraction(1, 2), Fraction(4, 5)]:
            f = lambda x: x / (1 + k*x)
            a,b,c,d = [f(x) for x in (-1, -r, r, 1)]
            cr = ((a-b)*(c-d))/((a-c)*(b-d))
            assert cr == ((1-r)/(1+r))**2
            exact_checks += 1
    rng = random.Random(SEED)
    rows = []
    for k in K_VALUES:
        a,b,c,d = endpoints(k)
        base_cr = inferred_radius_from_cr(a,b,c,d)
        base_naive = naive_radius(a,b,c,d)
        assert abs(base_cr - R) < 1e-12
        assert abs(base_naive - R*(1-k*k)/(1-k*k*R*R)) < 1e-12
        # Normalize image span to fixed 120 pixels before adding detector noise.
        factor = PIXEL_IRIS_SPAN / (d-a)
        pix = [factor * v for v in (a,b,c,d)]
        err_cr, err_naive = [], []
        invalid_cr = 0
        for _ in range(N):
            noisy = [v + rng.gauss(0,SIGMA_PX) for v in pix]
            # Four correctly associated boundaries required: irisL,pupilL,pupilR,irisR.
            if not (noisy[0] < noisy[1] < noisy[2] < noisy[3]):
                invalid_cr += 1
                continue
            cr = inferred_radius_from_cr(*noisy)
            if cr is None:
                invalid_cr += 1
                continue
            err_cr.append(cr - R)
            err_naive.append(naive_radius(*noisy) - R)
        rows.append({
            "k":k, "exact_projective_cross_ratio_estimate":round(base_cr,9),
            "naive_projected_radius_ratio":round(base_naive,9),
            "naive_relative_bias_percent":round(100*(base_naive/R-1),3),
            "noise_sigma_px":SIGMA_PX, "fixed_iris_span_px":PIXEL_IRIS_SPAN,
            "n":N, "accepted":len(err_cr), "invalid":invalid_cr,
            "cr_rmse":round(rms(err_cr),6) if err_cr else None,
            "naive_rmse":round(rms(err_naive),6) if err_naive else None,
        })
    # Violate concentric assumption (a real physiological possibility).
    shifted = []
    for shift in [0.0, 0.03, 0.06, 0.12]:
        v = endpoints(0.35, shift=shift)
        shifted.append({"center_shift_over_iris_radius":shift,
                        "cr_estimate":round(inferred_radius_from_cr(*v),9),
                        "absolute_error":round(abs(inferred_radius_from_cr(*v)-R),9)})
    # A non-projective radial warp mimics a class of differential refraction effects,
    # but its coefficient has NO physiological calibration.
    nonlinear = []
    for q in [0.0, 0.01, 0.05, 0.10]:
        v = endpoints(0.35, nonlinear=q)
        nonlinear.append({"arbitrary_nonlinear_coefficient":q,
                          "cr_estimate":round(inferred_radius_from_cr(*v),9),
                          "absolute_error":round(abs(inferred_radius_from_cr(*v)-R),9)})
    out = {"run":"E002-263","type":"synthetic geometry only","seed":SEED,
           "n_per_k":N,"exact_fraction_checks":exact_checks,
           "true_pupil_over_iris_radius":R,"rows":rows,
           "off_center_probe":shifted,"nonprojective_probe":nonlinear,
           "human_validation":False,"product_certification":False}
    Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
