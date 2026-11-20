"""E002-626: time-local asymmetric velocity budgets. Exact rational synthetic witness.
No physiological envelope is asserted. Run: python e002_626_local_velocity_budget.py
"""
from fractions import Fraction as F

def integrate(segments):
    """segments are (duration, nonnegative certified speed ceiling)."""
    assert all(d >= 0 and v >= 0 for d,v in segments)
    return sum((d*v for d,v in segments), F(0))

def closure_possible(a, b, c, closing_segments, opening_segments):
    """Necessary budget test for a specified candidate closure time.
    A false result excludes closure at that candidate time, not at every time.
    """
    return integrate(closing_segments) >= max(F(0),a-c) and integrate(opening_segments) >= max(F(0),b-c)

def any_candidate_possible(a,b,c,windows):
    return any(closure_possible(a,b,c,left,right) for left,right in windows)

def test():
    # 20ms gap, 2mm aperture at both ends, closure at 0mm.
    # A global 300mm/s envelope yields 6mm travel capacity per half-gap,
    # hence cannot exclude. Local 100mm/s each half gives 1mm, excluding.
    a=b=F(2); c=F(0)
    half=F(1,100)
    assert closure_possible(a,b,c,[(half,F(300))],[(half,F(300))])
    assert not closure_possible(a,b,c,[(half,F(100))],[(half,F(100))])
    # Sharpness: piecewise-linear trajectory reaches c at midpoint
    # exactly when both budgets equal the required travel.
    assert closure_possible(a,b,c,[(half,F(200))],[(half,F(200))])
    # Candidate times must be swept: rejection at one candidate
    # does not establish rejection at another.
    assert any_candidate_possible(a,b,c,[
        ([(half,F(100))],[(half,F(100))]),
        ([(half,F(200))],[(half,F(200))])
    ])
    print("E002-626: 4 exact-rational assertions PASS (synthetic conditional model)")
if __name__ == "__main__": test()
