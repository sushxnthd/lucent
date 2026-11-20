#!/usr/bin/env python3
"""E002-735: finite-sample distribution-free *marginal* speed calibration.

For exchangeable calibration trajectory maxima V_1,...,V_n and one future
trajectory maximum V*, the maximum of n calibration maxima is exceeded by
V* with probability at most 1/(n+1) (ties handled conservatively).
This is NOT a physiological speed ceiling, conditional guarantee, or
simultaneous guarantee over unlimited predictions.
"""
from fractions import Fraction
from itertools import product

def exceedance_rate(n, alphabet=(0, 1, 2)):
    total = 0
    exceeded = 0
    for sample in product(alphabet, repeat=n + 1):
        total += 1
        exceeded += sample[-1] > max(sample[:-1])
    return Fraction(exceeded, total)

def main():
    for n in range(1, 8):
        rate = exceedance_rate(n)
        assert rate <= Fraction(1, n + 1), (n, rate)
        print(f"n={n} exact discrete exceedance={rate}; upper={Fraction(1,n+1)}")
    # A non-exchangeable rare-fast test population defeats this bound.
    calibration = [1] * 100
    future = 2
    assert future > max(calibration)
    print("Non-exchangeable drift witness: calibration max 1, future 2")
    print("Interpretation: rank guarantee only for one exchangeable future trajectory;")
    print("do not certify deterministic hidden-closure exclusion from sample maxima.")

if __name__ == "__main__":
    main()
