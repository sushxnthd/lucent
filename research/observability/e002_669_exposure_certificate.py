"""E002-669: sharp finite-exposure mean-aperture exclusion bound.

Assumptions: normalized aperture in [0,1], V-Lipschitz, uniform rectangular
exposure, threshold tau in [0,1], and deterministic mean measurement error.
No empirical physiological velocity ceiling is asserted.
"""
from fractions import Fraction as F

def deficit_floor(width, velocity, tau):
    assert width > 0 and velocity > 0 and 0 <= tau <= 1
    depth = 1 - tau
    reach = min(width, depth / velocity)
    return depth * reach - velocity * reach * reach / 2

def max_mean_if_closure(width, velocity, tau):
    return 1 - deficit_floor(width, velocity, tau) / width

def boundary_witness_mean(width, velocity, tau):
    # a(t)=min(1,tau+V*t), closure exactly at the left exposure edge
    return max_mean_if_closure(width, velocity, tau)

def certify_no_closure(measured_mean, error, width, velocity, tau):
    assert 0 <= error and 0 <= measured_mean <= 1
    return measured_mean - error > max_mean_if_closure(width, velocity, tau)

def test():
    w, v, tau = F(1, 30), F(60), F(3, 10)
    # d/V=7/600 < 1/30; integral deficit=49/12000
    floor = deficit_floor(w, v, tau)
    assert floor == F(49, 12000), floor
    limit = max_mean_if_closure(w, v, tau)
    assert limit == F(351, 400), limit
    assert boundary_witness_mean(w,v,tau) == limit
    assert certify_no_closure(F(9,10), F(1,100), w,v,tau)
    assert not certify_no_closure(F(9,10), F(3,100), w,v,tau)
    # Short exposure, where the ramp cannot recover to fully open.
    assert deficit_floor(F(1,1000),v,tau) == F(67,100000)
    assert max_mean_if_closure(F(1,1000),v,tau) == F(33,100)
    # A zero-velocity limit is excluded by API; this is an independent case.
    for width in (F(1,1000), F(1,30), F(1,5)):
        assert 0 <= deficit_floor(width,v,tau) <= width
        assert 0 <= max_mean_if_closure(width,v,tau) <= 1

if __name__ == "__main__":
    test()
    print("E002-669 exact rational tests PASS")
