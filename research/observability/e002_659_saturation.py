"""E002-659: saturation destroys pulse-phase shutter identifiability.

Synthetic exact-arithmetic adversarial instrument test; not physical calibration.
Run: python3 research/observability/e002_659_saturation.py
"""
from fractions import Fraction as F

N = 20
times = [(F(i, 1) + F(1, 2)) / N * F(1, 5) - F(1, 10) for i in range(N)]
rect = [F(1, N)] * N
early = [F(1, 5) if i < 5 else F(0) for i in range(N)]
aperture = [F(1, 5) + 4 * abs(t) for t in times]
def moment(weights):
    return sum((w * abs(t) for w, t in zip(weights, times)), F(0))
def exposure(weights):
    return sum((w * a for w, a in zip(weights, aperture)), F(0))
def pulse_scan(weights, baseline, ceiling):
    return [min(ceiling, baseline + w) for w in weights]
def infer(scan, baseline):
    signal = [max(F(0), y - baseline) for y in scan]
    total = sum(signal)
    return [v / total for v in signal] if total else None

# Unsaturated scan identifies both different shutter kernels.
assert infer(pulse_scan(rect, F(0), F(1)), F(0)) == rect
assert infer(pulse_scan(early, F(0), F(1)), F(0)) == early

# All pulse phases saturate: two physically different kernels become indistinguishable.
scan_a = pulse_scan(rect, F(1, 10), F(1, 10))
scan_b = pulse_scan(early, F(1, 10), F(1, 10))
assert scan_a == scan_b
assert infer(scan_a, F(1, 10)) is None
assert exposure(early) - 4 * moment(rect) > F(7, 25)
assert min(aperture) < F(7, 25)
assert exposure(early) - 4 * moment(early) <= F(7, 25)
print("PASS: saturated phase scans cannot identify shutter weights; rectangular assumption falsely certifies open")
print("early exposure", exposure(early), "naive lower", exposure(early)-4*moment(rect),
      "true-kernel lower", exposure(early)-4*moment(early), "sampled min", min(aperture))
