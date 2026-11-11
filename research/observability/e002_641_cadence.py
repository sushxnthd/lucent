"""E002-641 exact-rational minimax cadence calculation; synthetic only."""
from fractions import Fraction as F

def ceiling(delta_obs, eps, acceleration, h):
    if h <= 0 or eps < 0 or acceleration < 0:
        raise ValueError("invalid certificate")
    return (abs(delta_obs) + 2*eps)/h + acceleration*h/2

def penalty(eps, acceleration, h):
    return ceiling(F(0), eps, acceleration, h)

def test():
    e, A = F(1,20), F(10000)  # mm, mm/s^2
    rows = [(F(ms,1000), penalty(e,A,F(ms,1000))) for ms in range(1,21)]
    assert min(rows,key=lambda x:x[1]) == (F(4,1000), F(45))
    assert penalty(e,A,F(2,1000)) == F(60)
    assert penalty(e,A,F(10,1000)) == F(60)
    assert ceiling(F(0),F(1,20),F(0),F(1,100)) == F(10)
    print("PASS: 20 cadence points; best grid 4 ms, 45 mm/s; 2 and 10 ms 60 mm/s")
if __name__ == "__main__":
    test()
