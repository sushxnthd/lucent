"""E002-737: simultaneous future-episode failure of one-shot maximum calibration.

Evidence tier: exact combinatorial synthetic verification, NOT human data.
Assumption: n+m exchangeable continuous trajectory maxima, fixed before observation.
For n calibration and m future trajectories, P(any future exceeds calibration max)
= m/(n+m), since the overall maximum is equally likely in each position.
Thus 1/(n+1) is only a one-future-trajectory guarantee; it cannot be
reused as a simultaneous deployment guarantee across repeated predictions.
Ties can only reduce the strict-exceedance probability under exchangeability.
"""
from fractions import Fraction
from itertools import permutations
from math import factorial

def exact_enumeration(n, m):
    assert n >= 1 and m >= 1
    total = n + m
    hits = 0
    for order in permutations(range(total)):
        if max(order[n:]) > max(order[:n]):
            hits += 1
    return Fraction(hits, factorial(total))

def run():
    checked = 0
    for n in range(1, 7):
        for m in range(1, 8-n):
            observed = exact_enumeration(n, m)
            expected = Fraction(m, n+m)
            assert observed == expected, (n, m, observed, expected)
            checked += 1
    assert Fraction(1, 21) == Fraction(1, 20+1)
    assert Fraction(20, 40) == Fraction(20, 20+20)
    print(f"PASS {checked} exact permutation cases")
    print("n=20: one future exceedance risk=1/21; twenty future risk=1/2")
    print("Product: do not reuse one-shot marginal speed calibration as a session-wide guarantee.")

if __name__ == "__main__":
    run()
