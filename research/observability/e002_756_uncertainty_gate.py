"""E002-756: exact-rational adversarial uncertainty gate; synthetic only."""
from fractions import Fraction as F

def possible_hidden_zero(a0,a1,v,dt):
    return a0+a1 <= v*dt

def robust_exclusion(lower0,lower1,vmax,dtmax):
    return lower0+lower1 > vmax*dtmax

def run():
    scenarios=[
      ('nominal_safe',F(3,5),F(3,5),F(1),F(1),F(3,5),F(3,5),F(1),F(1)),
      ('aperture_error',F(3,5),F(3,5),F(1),F(1),F(2,5),F(2,5),F(1),F(1)),
      ('clock_error',F(3,5),F(3,5),F(1),F(1),F(3,5),F(3,5),F(1),F(3,2)),
      ('velocity_error',F(3,5),F(3,5),F(1),F(1),F(3,5),F(3,5),F(3,2),F(1)),
      ('combined',F(3,5),F(3,5),F(1),F(1),F(2,5),F(2,5),F(3,2),F(3,2)),
    ]
    for name,a,b,v,dt,lo0,lo1,hi_v,hi_dt in scenarios:
        nominal=not possible_hidden_zero(a,b,v,dt)
        conservative=robust_exclusion(lo0,lo1,hi_v,hi_dt)
        witness=possible_hidden_zero(lo0,lo1,hi_v,hi_dt)
        assert not(conservative and witness)
        print(f'{name}: nominal_excludes={nominal}, robust_excludes={conservative}, admissible_hidden_zero={witness}')
    assert sum(robust_exclusion(*s[5:]) for s in scenarios)==1
    assert not robust_exclusion(F(1,2),F(1,2),F(1),F(1))
    print('PASS: all exact-rational assertions')

if __name__=='__main__': run()
