"""E002-681 finite-sample velocity ceiling non-identifiability.
Constructed C1 witnesses, not human physiology. Python 3 standard library.
"""
from fractions import Fraction

def witness(sample_times, amplitude=Fraction(1, 4), width=Fraction(1, 100)):
    ts = sorted(Fraction(t) for t in sample_times)
    assert len(ts) >= 2 and len(set(ts)) == len(ts)
    gap = ts[1] - ts[0]
    assert 0 < width < gap / 2 and 0 < amplitude <= Fraction(1, 2)
    c = (ts[0] + ts[1]) / 2
    def bump(t):
        z = (Fraction(t) - c) / width
        return amplitude * (1-z*z)**2 if abs(z) < 1 else Fraction(0)
    return bump, c

def test():
    ts = [Fraction(i, 30) for i in range(5)]
    for width in (Fraction(1,100), Fraction(1,1000), Fraction(1,10000)):
        b,c = witness(ts,width=width)
        assert all(b(t) == 0 for t in ts)
        assert b(c) == Fraction(1,4)
        assert all(Fraction(0) <= Fraction(1,2)+b(t) <= 1 for t in ts+[c])
    print("PASS: 3 C1 invisible bumps; exact sample equivalence")

if __name__ == "__main__":
    test()
