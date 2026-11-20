"""E002-620: conservative shutter-gap certificate; conditional scalar model only.
No camera frames or human physiology are validated by this module.
Run: python e002_620_exposure_certificate.py
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Exposure:
    mean_lower: float  # independently certified LOWER bound on scalar aperture mean (mm)
    duration_upper: float  # upper bound on exposure length (s)

@dataclass(frozen=True)
class Gap:
    duration_upper: float  # upper bound on exposure-free interval (s)
    closure_threshold_upper: float  # conservative threshold (mm)
    velocity_upper: float  # independently validated max |da/dt| (mm/s)

def certificate(left: Exposure, right: Exposure, gap: Gap):
    vals = (left.mean_lower, left.duration_upper, right.mean_lower,
            right.duration_upper, gap.duration_upper,
            gap.closure_threshold_upper, gap.velocity_upper)
    if not all(isfinite(v) for v in vals) or min(vals) < 0:
        return {"decision": "ABSTAIN_INVALID_INPUT"}
    # A Lipschitz path with mean m over duration T has endpoint >= m - V*T/2.
    a = max(0.0, left.mean_lower - gap.velocity_upper * left.duration_upper / 2)
    b = max(0.0, right.mean_lower - gap.velocity_upper * right.duration_upper / 2)
    required = max(0.0, a - gap.closure_threshold_upper) + max(
        0.0, b - gap.closure_threshold_upper)
    budget = gap.velocity_upper * gap.duration_upper
    # Strict inequality essential: equality permits a closure at one instant.
    return {"decision": "NO_HIDDEN_CLOSURE_CONDITIONAL" if required > budget
            else "ABSTAIN_HIDDEN_CLOSURE_POSSIBLE",
            "endpoint_lower_mm": [a,b], "required_mm": required,
            "velocity_budget_mm": budget}

def self_test():
    l = Exposure(5.0, .010)
    r = Exposure(5.0, .010)
    g = Gap(.010, .5, 100.0)
    assert certificate(l,r,g)["decision"] == "NO_HIDDEN_CLOSURE_CONDITIONAL"
    assert certificate(l,r,Gap(.080,.5,100))["decision"] == "ABSTAIN_HIDDEN_CLOSURE_POSSIBLE"
    assert certificate(l,r,Gap(.070,.5,100))["decision"] == "ABSTAIN_HIDDEN_CLOSURE_POSSIBLE"
    assert certificate(l,r,Gap(.010,.5,100))["endpoint_lower_mm"] == [4.5,4.5]
    assert certificate(l,r,Gap(.070,.5,100))["required_mm"] == 8.0
    assert certificate(l,r,Gap(.080,.5,100))["velocity_budget_mm"] == 8.0
    assert certificate(Exposure(float("nan"),.01),r,g)["decision"] == "ABSTAIN_INVALID_INPUT"
    assert certificate(Exposure(5,-.01),r,g)["decision"] == "ABSTAIN_INVALID_INPUT"
    # Increased exposure duration weakens certificate.
    assert certificate(Exposure(5,.10),r,g)["decision"] == "ABSTAIN_HIDDEN_CLOSURE_POSSIBLE"
    print("E002-620 synthetic conditional checks passed (9 assertions)")

if __name__ == "__main__":
    self_test()
