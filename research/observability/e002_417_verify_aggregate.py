#!/usr/bin/env python3
"""E002-417: independently audit all-frame human aggregate and fail-closed claims.

This verifies arithmetic and preregistered decisions, NOT anatomical ground truth.
"""
import argparse
import copy
import json
from pathlib import Path

VARIANTS = ("gain070", "gain130", "blur2", "translate8_6", "white_glare")
TRANSFER = VARIANTS[:4]


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def fraction_matches(observed, numerator, denominator):
    if denominator == 0:
        return observed is None
    return isinstance(observed, (int, float)) and abs(observed - numerator / denominator) <= 0.00000051


def verify(x):
    n = x["source_frame_occurrences"]
    clips = x["clips"]
    a = x["clean_A_valid"]
    b = x["clean_B_valid"]
    joint = x["clean_joint_valid"]
    agree = x["clean_joint_agree_within_5px"]
    require(isinstance(n, int) and n > 0 and isinstance(clips, int), "invalid source count")
    require(all(isinstance(v, int) and 0 <= v <= n for v in (a, b, joint, agree)), "invalid clean counts")
    require(agree <= joint <= min(a, b), "invalid agreement denominator")
    require(fraction_matches(x["clean_joint_agree_all_frame_fraction"], agree, n), "clean fraction not all-frame")
    nu = x["nuisance"]
    require(set(nu) == set(VARIANTS), "nuisance missing or extra")
    for v in VARIANTS:
        d = nu[v]
        allvalid = d["all_frame_joint_valid"]
        retained = d["retained_joint_valid"]
        stable = d["retained_and_stable"]
        bothabs = d["both_abstain"]
        require(d["clean_joint_valid_denominator"] == joint, v + " clean denominator mismatch")
        require(all(isinstance(k, int) for k in (allvalid, retained, stable, bothabs)), v + " noninteger count")
        require(0 <= stable <= retained <= joint <= n, v + " stability denominator corruption")
        require(0 <= allvalid <= n and 0 <= bothabs <= n, v + " all-frame corruption")
        require(retained <= allvalid, v + " retained cannot exceed all-valid")
        require(allvalid + bothabs <= n, v + " mutually exclusive counts violated")
        require(fraction_matches(d["all_frame_joint_valid_fraction"], allvalid, n), v + " all-frame fraction mismatch")
        require(fraction_matches(d["retained_and_stable_fraction"], stable, joint), v + " stability fraction mismatch")
        require(fraction_matches(d["both_abstain_fraction"], bothabs, n), v + " abstention fraction mismatch")
    h = x["hypotheses"]
    expected = {
        "H1_source_coverage": clips == 8 and n >= 600,
        "H2_joint_coverage_and_agreement": agree / n >= .60,
        "H3_all_four_transfer_conditions": joint > 0 and all(
            nu[v]["retained_and_stable"] / joint >= .95 for v in TRANSFER),
        "H4_white_glare_both_abstain": nu["white_glare"]["both_abstain"] / n >= .95,
        "H5_synthetic_control_and_no_product": True,
    }
    require(set(h) == set(expected), "hypothesis names changed")
    for key in expected:
        require(h[key] is expected[key], "frozen hypothesis mismatch: " + key)
    require(x["joint_transfer_gate_pass"] is all(expected.values()), "joint gate mismatch")
    require(x["human_raters"] == 0 and x["physical_aperture_validated"] is False,
            "unsupported human reference claim")
    require(x["independent_camera_exposure_calibrated"] is False and
            x["independent_hard_velocity_bound"] is False, "unsupported physical calibration")
    require(x["product_claim_authorized"] is False and x["product"] == "ABSTAIN_UNCALIBRATED",
            "product must fail closed")
    return expected


def self_test(x):
    verify(x)
    for key, value in (
        ("clean_joint_agree_all_frame_fraction", 0.95),
        ("clean_joint_agree_within_5px", x["source_frame_occurrences"] + 1),
    ):
        y = copy.deepcopy(x)
        y[key] = value
        try:
            verify(y)
        except ValueError:
            pass
        else:
            raise AssertionError("Adversarial aggregate accepted: " + key)
    y = copy.deepcopy(x)
    y["hypotheses"]["H2_joint_coverage_and_agreement"] = True
    try:
        verify(y)
    except ValueError:
        pass
    else:
        raise AssertionError("False success accepted")
    y = copy.deepcopy(x)
    y["nuisance"]["translate8_6"]["retained_and_stable"] = x["clean_joint_valid"] + 1
    try:
        verify(y)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid retention count accepted")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("aggregate", type=Path)
    p.add_argument("--reference", type=Path)
    args = p.parse_args()
    x = json.loads(args.aggregate.read_text())
    result = verify(x)
    self_test(x)
    if args.reference:
        reference = json.loads(args.reference.read_text())
        verify(reference)
        require(x == reference, "Human aggregate changed from independently persisted result")
    print("E002-417 independent aggregate arithmetic and adversarial integrity PASS")
    print("Frozen hypotheses:", result)
    print("Physical product: ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    main()
