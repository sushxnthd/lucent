#!/usr/bin/env python3
"""E002-413: conservative end-to-end audit of E002-412 nuisance survivorship.

Retrospective audit of a frozen human-video experiment. NOT a new preregistered
experiment, physical eyelid calibration, or clinical performance assessment.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

TRANSFER = ("gain_070", "gain_130", "blur_sigma2", "translation_8_6")
MIN_COVERAGE = 0.95
MIN_STABILITY = 0.95


def finite_fraction(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: expected numeric fraction")
    v = float(value)
    if not math.isfinite(v) or not 0 <= v <= 1:
        raise ValueError(f"{name}: out-of-range fraction")
    return v


def positive_count(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}: expected nonnegative integer")
    return value


def audit(d):
    if d.get("experiment") != "E002-412" or d.get("product") != "ABSTAIN_UNCALIBRATED":
        raise ValueError("Wrong experiment or unsafe upstream product state")
    if d.get("physical_aperture_validated") is not False or d.get("camera_exposure_calibrated") is not False:
        raise ValueError("Physical calibration flags inconsistent with this audit")
    n = positive_count(d["total_frames"], "total_frames")
    clean = positive_count(d["clean_valid_frames"], "clean_valid_frames")
    if not (0 < clean <= n):
        raise ValueError("Invalid frame counts")
    report = {}
    for variant in TRANSFER:
        item = d["nuisance"][variant]
        joint = positive_count(item["joint_valid_frames"], variant + " joint")
        rejected = positive_count(item["rejected_frames"], variant + " rejected")
        p = finite_fraction(item["fraction_abs_change_le_008"], variant + " conditional stability")
        if joint > clean or joint + rejected > n or rejected > n:
            raise ValueError("Inconsistent nuisance counts for " + variant)
        # Only paired frames can support a repeatability claim. Missing transformed
        # measurements are failures, never silently dropped from the denominator.
        clean_coverage = joint / clean
        unconditional_stable_lower = (joint / n) * p
        conditional_stability = p
        transfer_pass = (clean_coverage >= MIN_COVERAGE and
                         unconditional_stable_lower >= MIN_STABILITY)
        report[variant] = {
            "joint_valid": joint,
            "clean_coverage": round(clean_coverage, 6),
            "conditional_stability": round(conditional_stability, 6),
            "conservative_all_frame_stability": round(unconditional_stable_lower, 6),
            "transfer_pass": transfer_pass,
        }
    glare = d["nuisance"]["glare"]
    glare_rejected = positive_count(glare["rejected_frames"], "glare rejected")
    if glare_rejected > n:
        raise ValueError("Impossible glare rejection count")
    glare_fail_closed = glare_rejected / n >= MIN_COVERAGE
    rejects = [v for v in TRANSFER if not report[v]["transfer_pass"]]
    return {
        "audit": "E002-413",
        "source": "E002-412 verified aggregate, retrospective denominator audit",
        "total_frames": n,
        "clean_valid_frames": clean,
        "variants": report,
        "glare_fail_closed": glare_fail_closed,
        "transfer_rejected": bool(rejects),
        "rejected_variants": rejects,
        "evidence_tier": "human-video optical proxy; not eyelid aperture",
        "product": "ABSTAIN_UNCALIBRATED",
        "hidden_closure_certification": "NOT_AUTHORIZED",
        "blink_duration_perclos_fatigue": "NOT_AUTHORIZED",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = audit(json.loads(args.input.read_text()))
    out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(out)
    print(out, end="")


if __name__ == "__main__":
    main()
