#!/usr/bin/env python3
"""E002-539: sharp joint velocity/acceleration hidden-closure law (research only).

Exact rational geometry; no empirical physiological or physical camera claims.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json

EVIDENCE = (
    "independent_hard_continuous_speed_bound",
    "independent_hard_continuous_acceleration_bound",
    "pointwise_anatomical_endpoint_intervals",
    "independent_blinded_anatomical_reference",
    "photodiode_authenticated_exposure",
    "authenticated_clock_and_conservative_gap",
    "native_frame_missingness_audited",
    "geometry_gaze_glasses_brightness_blur_controls",
)

def q(value):
    if value is None or isinstance(value, bool):
        raise ValueError("INVALID_RATIONAL")
    try:
        return F(str(value))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("INVALID_RATIONAL") from exc

def integral_min(h, speed, accel):
    """Integral_0^h min(speed, accel*s) ds; all inputs exact nonnegative."""
    if min(h, speed, accel) == 0:
        return F(0)
    if speed >= accel * h:
        return accel * h * h / 2
    return speed * h - speed * speed / (2 * accel)

def joint_dip(gap, speed, accel):
    return integral_min(gap / 2, speed, accel)

def witness_aperture(t, b, gap, speed, accel, scale=F(1)):
    """Symmetric C1,1 extremal, optionally scaled to a physical touching witness."""
    if not F(0) <= t <= gap or not F(0) <= scale <= 1:
        raise ValueError("INVALID_WITNESS_ARGUMENT")
    h = gap / 2
    return b - scale * (integral_min(h, speed, accel) -
                        integral_min(abs(t - h), speed, accel))

def evaluate(case):
    if not isinstance(case, dict):
        raise ValueError("INVALID_CASE")
    b, c, d, v, a = [q(case.get(k)) for k in (
        "equal_endpoint_aperture", "closure_threshold",
        "max_unobserved_gap_s", "hard_speed_s_inverse",
        "hard_acceleration_s_inverse2")]
    if not (F(0) <= c < b <= 1 and d > 0 and v >= 0 and a >= 0):
        raise ValueError("INVALID_GEOMETRY_OR_CEILINGS")
    if case.get("endpoint_observable") not in (
        "pointwise_anatomical_aperture", "exposure_average", "raw_pixel_brightness"):
        raise ValueError("INVALID_ENDPOINT_OBSERVABLE")
    if case.get("speed_source") not in (
        "independent_continuous_hard_bound", "sampled_peak", "cohort_mean"):
        raise ValueError("INVALID_SPEED_SOURCE")
    if case.get("acceleration_source") not in (
        "independent_continuous_hard_bound", "sampled_second_difference", "cohort_mean"):
        raise ValueError("INVALID_ACCELERATION_SOURCE")
    attest = case.get("attestations")
    if not isinstance(attest, dict) or any(type(attest.get(k)) is not bool for k in EVIDENCE):
        raise ValueError("MISSING_OR_MALFORMED_ATTESTATIONS")
    dip = joint_dip(d, v, a)
    margin = b - c
    speed_dip = v * d / 2
    accel_dip = a * d * d / 8
    blockers = []
    if case["endpoint_observable"] != "pointwise_anatomical_aperture":
        blockers.append("ENDPOINTS_NOT_POINTWISE_ANATOMY")
    if case["speed_source"] != "independent_continuous_hard_bound":
        blockers.append("SPEED_NOT_INDEPENDENT_HARD_CONTINUOUS_BOUND")
    if case["acceleration_source"] != "independent_continuous_hard_bound":
        blockers.append("ACCELERATION_NOT_INDEPENDENT_HARD_CONTINUOUS_BOUND")
    blockers.extend("MISSING_" + k.upper() for k in EVIDENCE if not attest[k])
    return {
        "experiment": "E002-539",
        "evidence_tier": "EXACT_CONDITIONAL_MATH_AND_SYNTHETIC_ONLY",
        "speed_only_dip": str(speed_dip),
        "acceleration_only_dip": str(accel_dip),
        "joint_dip": str(dip),
        "joint_dimensionless_ratio": str(dip / margin),
        "sharp_lower_aperture": str(b - dip),
        "speed_only_excludes": speed_dip < margin,
        "acceleration_only_excludes": accel_dip < margin,
        "joint_excludes_if_hard_bounds": dip < margin,
        "conditional_geometry": "NO_HIDDEN_CROSSING" if dip < margin else "CROSSING_OR_TOUCH_FEASIBLE",
        "evidence_decision": "CONDITIONAL_ONLY_NOT_PHYSICALLY_VERIFIED" if not blockers
                             else "ILLUSTRATIVE_NOT_CERTIFIED",
        "blockers": blockers,
        "physical_validated": False,
        "human_motion_ceilings_certified": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }

def frozen_case(speed, fps):
    return {
        "equal_endpoint_aperture": "9/10", "closure_threshold": "1/5",
        "max_unobserved_gap_s": f"1/{fps}",
        "hard_speed_s_inverse": str(speed), "hard_acceleration_s_inverse2": "6000",
        "endpoint_observable": "pointwise_anatomical_aperture",
        "speed_source": "sampled_peak", "acceleration_source": "sampled_second_difference",
        "attestations": {k: False for k in EVIDENCE},
    }

def run_frozen():
    cases = {
        "30fps_V45_joint_rescue": frozen_case(45, 30),
        "30fps_V60_touch": frozen_case(60, 30),
        "30fps_V65_cross": frozen_case(65, 30),
        "240fps_V45_accel_regime": frozen_case(45, 240),
        "15fps_V45_unsafe": frozen_case(45, 15),
    }
    out = {name: evaluate(case) for name, case in cases.items()}
    expected = {
        "30fps_V45_joint_rescue": ("93/160", "93/112", True),
        "30fps_V60_touch": ("7/10", "1", False),
        "30fps_V65_cross": ("117/160", "117/112", False),
        "240fps_V45_accel_regime": ("5/384", "25/1344", True),
    }
    for name, (dip, ratio, excludes) in expected.items():
        result = out[name]
        assert (result["joint_dip"], result["joint_dimensionless_ratio"],
                result["joint_excludes_if_hard_bounds"]) == (dip, ratio, excludes)
    assert not out["15fps_V45_unsafe"]["joint_excludes_if_hard_bounds"]
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--frozen", action="store_true")
    group.add_argument("--input")
    args = parser.parse_args()
    result = run_frozen() if args.frozen else evaluate(
        json.loads(open(args.input, encoding="utf-8").read()))
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
