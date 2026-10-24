#!/usr/bin/env python3
"""E002-416: conditional physical-reference gap labels, NEVER product certificates.

External evidence declarations are NOT authenticated by this script. A sampled
velocity maximum, EEG timestamp, exposure mean, or image-intensity proxy is not
an independently calibrated instantaneous physical aperture reference.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

ABSTAIN = "ABSTAIN_UNCALIBRATED"
UNRESOLVED = "REFERENCE_UNRESOLVED"
NEGATIVE = "REFERENCE_NEGATIVE_CONDITIONAL"
POSITIVE = "REFERENCE_POSITIVE_CONDITIONAL"
NUISANCES = ("missing", "blur", "glare", "occlusion", "gaze", "glasses",
             "geometry", "brightness", "saturation", "clock", "rolling_shutter")


def _finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name}: expected finite numeric value")
    return float(value)


def _frame(raw, label):
    if not isinstance(raw, dict):
        raise ValueError(f"{label}: expected frame object")
    t = _finite(raw.get("time_s"), f"{label}.time_s")
    lo = _finite(raw.get("aperture_lower"), f"{label}.aperture_lower")
    hi = _finite(raw.get("aperture_upper"), f"{label}.aperture_upper")
    if not 0 <= lo <= hi <= 1:
        raise ValueError(f"{label}: invalid normalized physical aperture interval")
    flags = raw.get("nuisance_flags", [])
    if not isinstance(flags, list) or any(x not in NUISANCES for x in flags):
        raise ValueError(f"{label}: unknown nuisance flag")
    return t, lo, hi, bool(flags)


def sharp_lower_envelope(lo0, lo1, speed, gap):
    """Exact minimum of two backwards Lipschitz cones on [0,gap]."""
    if speed == 0:
        return max(lo0, lo1, 0.)
    meeting = (lo0 - lo1 + speed * gap) / (2 * speed)
    meeting = min(max(meeting, 0.), gap)
    return max(0., lo0 - speed * meeting,
               lo1 - speed * (gap - meeting))


def classify(payload):
    """Conditional reference-label triage; no physical evidence authentication."""
    if not isinstance(payload, dict):
        raise ValueError("Expected object")
    a = _frame(payload.get("frame0"), "frame0")
    b = _frame(payload.get("frame1"), "frame1")
    theta = _finite(payload.get("closure_threshold"), "closure_threshold")
    err = _finite(payload.get("clock_error_per_endpoint_s"), "clock_error_per_endpoint_s")
    if not 0 <= theta < 1 or err < 0 or not b[0] > a[0]:
        raise ValueError("Invalid threshold, clock uncertainty or nonmonotone timestamps")
    result = {
        "experiment": "E002-416", "conditional_reference_label": UNRESOLVED,
        "product": ABSTAIN, "product_claim_authorized": False,
        "physical_provenance_authenticated_by_tool": False,
        "reference_label_research_only": True,
        "sharp_lower_envelope": None, "dimensionless_sampling_ratio": None,
        "reason": "missing independent physical reference evidence",
    }
    evidence = payload.get("evidence", {})
    if not isinstance(evidence, dict):
        raise ValueError("Evidence must be object")
    required = ("independent_physical_aperture_review",
                "independent_camera_hardware_timing",
                "instantaneous_not_exposure_mean", "independent_geometry_review")
    if not all(evidence.get(k) is True for k in required):
        return result
    if a[3] or b[3]:
        result["reason"] = "nuisance or missingness invalidates physical reference"
        return result
    if a[2] <= theta or b[2] <= theta:
        result["conditional_reference_label"] = POSITIVE
        result["reason"] = "sampled physical closure, conditional on external evidence review"
        return result
    speed = payload.get("velocity_bound_per_s")
    if speed is None or payload.get("velocity_bound_kind") != "independent_deterministic_hard":
        result["reason"] = "no independent deterministic hard velocity envelope"
        return result
    v = _finite(speed, "velocity_bound_per_s")
    if v < 0:
        raise ValueError("Negative velocity bound")
    if evidence.get("independent_hard_velocity_review") is not True:
        result["reason"] = "hard velocity bound has no external review assertion"
        return result
    gap = b[0] - a[0] + 2 * err
    if a[1] > b[2] + v * gap or b[1] > a[2] + v * gap:
        result["reason"] = "reference aperture intervals inconsistent with velocity envelope"
        return result
    bound = sharp_lower_envelope(a[1], b[1], v, gap)
    result["sharp_lower_envelope"] = bound
    margin = min(a[1], b[1]) - theta
    result["dimensionless_sampling_ratio"] = v * gap / (2 * margin) if margin > 0 else None
    if bound > theta:
        result["conditional_reference_label"] = NEGATIVE
        result["reason"] = "no crossing possible under externally unverified input assumptions"
    else:
        result["reason"] = "hidden threshold crossing remains feasible"
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(classify(json.loads(args.input.read_text())), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
