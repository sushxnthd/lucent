"""Exact exposure-averaging nonidentifiability witness. Synthetic, not human evidence."""
from fractions import Fraction as F

def area(points):
    return sum((y0+y1)*(t1-t0)/2 for (t0,y0),(t1,y1) in zip(points,points[1:]))

def max_speed(points):
    return max(abs((y1-y0)/(t1-t0)) for (t0,y0),(t1,y1) in zip(points,points[1:]))

def main():
    # Time in units of one exposure, aperture in units of 1 mm.
    no_blink = [(F(0),F(1)),(F(1),F(1))]
    hidden_blink = [(F(0),F(1)),(F(1,4),F(3,2)),
                    (F(1,2),F(0)),(F(3,4),F(3,2)),(F(1),F(1))]
    assert area(no_blink) == area(hidden_blink) == 1
    assert no_blink[0] == hidden_blink[0] and no_blink[-1] == hidden_blink[-1]
    assert max_speed(hidden_blink) == 6
    assert min(y for _,y in hidden_blink) == 0
    assert min(y for _,y in no_blink) == 1
    # Both satisfy any physical speed ceiling V with V*T >= 6 mm,
    # where T is the exposure duration in seconds.
    print("PASS: same endpoints and exact exposure average; opposite closure status; VT >= 6 mm")

if __name__ == "__main__":
    main()
