"""E002-664: phase-locked hidden closures; synthetic, not human evidence.
Run: python3 research/observability/e002_664_phase_lock.py
"""
from fractions import Fraction as F

def aperture(t, hz):
    phase = (t * hz) % 1
    return 1 - 2 * min(phase, 1 - phase)

def certificate(a, b, hz, velocity_ceiling, threshold):
    gap = F(1, hz)
    lower = (a + b - velocity_ceiling * gap) / 2
    return lower > threshold, lower

def test():
    threshold = F(3, 10)
    for hz in (24, 30, 60, 120):
        for count in (2, 30, 300):
            observed = [aperture(F(i, hz), hz) for i in range(count)]
            hidden = [aperture(F(2*i+1, 2*hz), hz) for i in range(count-1)]
            assert all(x == 1 for x in observed)
            assert all(x == 0 for x in hidden)
            # True velocity is 2*hz. It is not estimable from sampled frame differences.
            assert max(abs(observed[i+1]-observed[i])*hz for i in range(count-1)) == 0
            unsafe, lower = certificate(F(1), F(1), hz, F(0), threshold)
            safe, correct_lower = certificate(F(1), F(1), hz, F(2*hz), threshold)
            assert unsafe and lower == 1
            assert not safe and correct_lower == 0
    # At a fixed acquisition rate, a shifted sampling phase reveals the closure.
    for hz in (30, 60):
        shifted = [aperture(F(2*i+1, 2*hz), hz) for i in range(12)]
        assert all(x == 0 for x in shifted)
    print("PASS: 12 phase-locked cases and two phase-shift controls; synthetic only")

if __name__ == "__main__":
    test()
