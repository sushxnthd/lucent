#!/usr/bin/env python3
"""E002-504: fail-closed, RESEARCH-ONLY static-aperture evaluator.

Uses a separately supplied iris-scale interval, not the two raters' nominal
diameters. Input provenance is asserted, NOT independently authenticated here.
Never licenses blink, hidden-closure, PERCLOS, fatigue, or medical claims.
No human data or images required; --self-test uses synthetic fixtures.
"""
import json
import math
import sys
import unittest
from decimal import Decimal

C = 0.10
NATIVE_HEIGHT = 288
REQUIRED_METHOD = "INDEPENDENT_OPTICAL_CALIBRATION"


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def base(reason):
    return {
        "experiment": "E002-504",
        "evidence_tier": "CONDITIONAL_STATIC_GEOMETRY_ONLY",
        "decision": reason,
        "physical_hidden_closure_certified": False,
        "blink_duration_certified": False,
        "perclos_certified": False,
        "fatigue_certified": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def frame_interval(frame, d_lo, d_hi):
    if not isinstance(frame, dict):
        return None
    if set(frame) != {"frame", "upper_y", "lower_y", "iris_diameter", "uncertainty_px", "flags"}:
        return None
    if not isinstance(frame["frame"], int) or isinstance(frame["frame"], bool) or not 0 <= frame["frame"] <= 12:
        return None
    if not isinstance(frame["flags"], list) or frame["flags"]:
        return None
    vals = [frame[k] for k in ("upper_y", "lower_y", "iris_diameter", "uncertainty_px")]
    if not all(finite(v) for v in vals):
        return None
    upper, lower, nominal_d, error = vals
    if not (0 <= upper <= lower <= NATIVE_HEIGHT and 0 < nominal_d <= NATIVE_HEIGHT and 0 <= error <= 30):
        return None
    # Use decimal-text arithmetic: 4.2 - 0.1 must not round ABOVE 4.1,
    # which would turn a boundary-touching uncertainty interval into a claim.
    gap = Decimal(str(lower)) - Decimal(str(upper))
    e = Decimal(str(error))
    return (max(Decimal(0), gap - 2 * e) / Decimal(str(d_hi)),
            (gap + 2 * e) / Decimal(str(d_lo)))


def evaluate(a, b, reference, threshold=C):
    """Return a conditional static classification or a conservative abstention.

    Reference flags are *claims by the input supplier*, not independent proof.
    The original rater schema lacks measured x coordinates and reference-scale
    uncertainty; an independent reviewer must separately verify both.
    """
    if not finite(threshold) or not 0 < threshold < 1:
        return base("ABSTAIN_INVALID_THRESHOLD")
    if not isinstance(a, dict) or not isinstance(b, dict) or a.get("rater") != "A" or b.get("rater") != "B":
        return base("ABSTAIN_RATER_IDENTITY")
    if not isinstance(a.get("frame"), dict) or not isinstance(b.get("frame"), dict):
        return base("ABSTAIN_INVALID_GEOMETRY")
    if a["frame"].get("frame") != b["frame"].get("frame"):
        return base("ABSTAIN_FRAME_MISMATCH")
    if not isinstance(reference, dict):
        return base("ABSTAIN_MISSING_INDEPENDENT_SCALE")
    if (reference.get("method") != REQUIRED_METHOD
            or reference.get("independent_of_raters") is not True
            or reference.get("same_session") is not True
            or reference.get("fixed_column_x160_verified") is not True):
        return base("ABSTAIN_UNVERIFIED_SCALE_PROVENANCE")
    d_lo, d_hi = reference.get("diameter_lower_px"), reference.get("diameter_upper_px")
    if not finite(d_lo) or not finite(d_hi) or not (0 < d_lo <= d_hi <= NATIVE_HEIGHT):
        return base("ABSTAIN_INVALID_SCALE_BOUNDS")
    if a["frame"].get("flags") or b["frame"].get("flags"):
        return base("ABSTAIN_NUISANCE")
    ia = frame_interval(a["frame"], d_lo, d_hi)
    ib = frame_interval(b["frame"], d_lo, d_hi)
    if ia is None or ib is None:
        return base("ABSTAIN_INVALID_GEOMETRY")
    if max(ia[0], ib[0]) > min(ia[1], ib[1]):
        return base("ABSTAIN_RATER_DISAGREEMENT")
    t = Decimal(str(threshold))
    if ia[1] < t and ib[1] < t:
        decision = "RESEARCH_STATIC_BELOW"
    elif ia[0] > t and ib[0] > t:
        decision = "RESEARCH_STATIC_ABOVE"
    else:
        decision = "ABSTAIN_THRESHOLD_CROSSED"
    result = base(decision)
    # Only a conditional aggregate interval; no raw landmarks or participant data.
    result["conservative_interval_union"] = [
        float(round(min(ia[0], ib[0]), 9)), float(round(max(ia[1], ib[1]), 9))
    ]
    result["reference_provenance_independently_authenticated_by_software"] = False
    return result


def fixture(gap, nominal_d=40, error=0.05, frame=0):
    return {"frame": frame, "upper_y": 100.0, "lower_y": 100.0 + gap,
            "iris_diameter": nominal_d, "uncertainty_px": error, "flags": []}


def ref():
    return {"method": REQUIRED_METHOD, "independent_of_raters": True,
            "same_session": True, "fixed_column_x160_verified": True,
            "diameter_lower_px": 39, "diameter_upper_px": 41}


def pair(gap, nominal_d=40, error=0.05):
    f = fixture(gap, nominal_d, error)
    return {"rater": "A", "frame": dict(f)}, {"rater": "B", "frame": dict(f)}


class FrozenControls(unittest.TestCase):
    def check(self, a, b, r, expected):
        x = evaluate(a, b, r)
        self.assertEqual(x["decision"], expected)
        self.assertEqual(x["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(x["release"], "BLOCKED")
        self.assertFalse(x["physical_hidden_closure_certified"])
        self.assertFalse(x["fatigue_certified"])
        return x

    def test_missing_reference_rejects_perfect_consensus(self):
        a, b = pair(4.2, 44)
        self.check(a, b, None, "ABSTAIN_MISSING_INDEPENDENT_SCALE")

    def test_false_closed_nominal_503(self):
        a, b = pair(4.2, 44)
        self.check(a, b, ref(), "ABSTAIN_THRESHOLD_CROSSED")

    def test_false_open_nominal_503(self):
        a, b = pair(3.8, 36)
        self.check(a, b, ref(), "ABSTAIN_THRESHOLD_CROSSED")

    def test_decimal_boundary_touch_is_unresolved(self):
        a, b = pair(4.2, 44, error=0.05)
        self.check(a, b, ref(), "ABSTAIN_THRESHOLD_CROSSED")
        # The numerator's lower bound is exactly 4.1 and D_hi exactly 41.
        self.assertEqual(Decimal("4.1") / Decimal("41"), Decimal("0.1"))

    def test_clear_above(self):
        a, b = pair(8)
        self.check(a, b, ref(), "RESEARCH_STATIC_ABOVE")

    def test_clear_below(self):
        a, b = pair(1)
        self.check(a, b, ref(), "RESEARCH_STATIC_BELOW")

    def test_no_provenance_fails(self):
        a, b = pair(8)
        r = ref()
        r["independent_of_raters"] = False
        self.check(a, b, r, "ABSTAIN_UNVERIFIED_SCALE_PROVENANCE")

    def test_column_unverified_fails(self):
        a, b = pair(8)
        r = ref()
        r["fixed_column_x160_verified"] = False
        self.check(a, b, r, "ABSTAIN_UNVERIFIED_SCALE_PROVENANCE")

    def test_bad_scale_fails(self):
        a, b = pair(8)
        for lo, hi in [(0, 40), (40, 39), (39, float("nan")), (True, 40), (39, 289)]:
            r = ref()
            r["diameter_lower_px"], r["diameter_upper_px"] = lo, hi
            self.check(a, b, r, "ABSTAIN_INVALID_SCALE_BOUNDS")

    def test_nuisance_fails(self):
        a, b = pair(8)
        b["frame"]["flags"] = ["GAZE"]
        self.check(a, b, ref(), "ABSTAIN_NUISANCE")

    def test_frame_mismatch_fails(self):
        a, b = pair(8)
        b["frame"]["frame"] = 1
        self.check(a, b, ref(), "ABSTAIN_FRAME_MISMATCH")

    def test_bad_geometry_fails(self):
        a, b = pair(8)
        b["frame"]["upper_y"] = float("inf")
        self.check(a, b, ref(), "ABSTAIN_INVALID_GEOMETRY")

    def test_disagreement_fails(self):
        a, b = pair(1, error=0)
        b["frame"]["lower_y"] = 108
        self.check(a, b, ref(), "ABSTAIN_RATER_DISAGREEMENT")

    def test_threshold_equality_abstains(self):
        a, b = pair(4, error=0)
        r = ref()
        r["diameter_lower_px"] = r["diameter_upper_px"] = 40
        self.check(a, b, r, "ABSTAIN_THRESHOLD_CROSSED")

    def test_nominal_diameter_never_controls_decision(self):
        a, b = pair(8, nominal_d=44)
        original = evaluate(a, b, ref())["decision"]
        a["frame"]["iris_diameter"] = 36
        b["frame"]["iris_diameter"] = 60
        self.assertEqual(evaluate(a, b, ref())["decision"], original)

    def test_invalid_threshold_fails(self):
        a, b = pair(8)
        self.check(a, b, ref(), "RESEARCH_STATIC_ABOVE")
        self.assertEqual(evaluate(a, b, ref(), float("nan"))["decision"], "ABSTAIN_INVALID_THRESHOLD")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        print(json.dumps({
            "experiment": "E002-504",
            "usage": "Import evaluate(a,b,reference); no human data or images are bundled.",
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"
        }, sort_keys=True))
