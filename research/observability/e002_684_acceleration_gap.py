"""E002-684: exact-rational extremal regression, not human calibration."""
from fractions import Fraction as F

def lower(x0, x1, h, a):
    x0, x1, h, a = map(F, (x0, x1, h, a))
    assert h > 0 and a >= 0
    d = x1 - x0
    if a == 0:
        return min(x0, x1)
    t = max(F(0), min(h, h / 2 - d / (a * h)))
    return x0 + d * t / h - a * t * (h - t) / 2

def check():
    n = 0
    for h in (F(1,100), F(1,30), F(1,10)):
        for a in (F(0), F(100), F(1000)):
            for x0 in (F(1,5), F(1,2), F(4,5)):
                for x1 in (F(1,5), F(1,2), F(4,5)):
                    bound = lower(x0,x1,h,a)
                    for k in range(101):
                        t = h * F(k,100)
                        extremal = x0 + (x1-x0)*t/h - a*t*(h-t)/2
                        assert extremal >= bound
                    n += 1
    assert lower(F(1,2),F(1,2),F(1,25),F(1000)) == F(3,10)
    print("PASS", n, "exact-rational cases; zero contradictions")

if __name__ == "__main__":
    check()
