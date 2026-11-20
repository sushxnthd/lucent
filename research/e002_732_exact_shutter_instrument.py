"""E002-732: exact-integral shutter-gap adversarial instrument simulator.

Synthetic only. No independently calibrated eyelid speed or human evidence.
"""
from fractions import Fraction as Q

def integrate(knots, lo, hi):
    assert lo < hi
    xs = sorted(set([lo, hi] + [t for t, _ in knots if lo < t < hi]))
    def at(x):
        for (a, va), (b, vb) in zip(knots, knots[1:]):
            if a <= x <= b:
                return va + (vb-va)*(x-a)/(b-a)
        raise ValueError("outside knots")
    return sum((at(a)+at(b))*(b-a)/2 for a,b in zip(xs,xs[1:]))

def test():
    count = 0
    for g_int in range(1, 21):
        for w_int in range(1, 51):
            g = Q(g_int); width = Q(w_int,100)*g
            left = (g-width)/2; mid = g/2; right = (g+width)/2
            knots = [(Q(-1),Q(1)), (Q(0),Q(1)), (left,Q(1)),
                     (mid,Q(0)), (right,Q(1)), (g,Q(1)), (g+1,Q(1))]
            assert integrate(knots,Q(-1),Q(0)) == 1
            assert integrate(knots,g,g+1) == 1
            assert Q(2)/width > 0
            count += 1
    # Finite exposure integrates a V-shaped closure; endpoints are both open.
    v = [(Q(0),Q(1)),(Q(1),Q(0)),(Q(2),Q(1))]
    assert integrate(v,Q(0),Q(2))/2 == Q(1,2)
    print(f"PASS: {count} exact-integral hidden-closure shutter cases; V exposure")
    print("SYNTHETIC ONLY; physiological velocity and sensor timing uncalibrated")

if __name__ == "__main__":
    test()
