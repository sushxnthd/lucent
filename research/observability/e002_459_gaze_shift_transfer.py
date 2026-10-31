#!/usr/bin/env python3
"""E002-459: preregistered participant-disjoint *gaze-shift* velocity transfer.

Uses published per-blink human peak estimates, not anatomical trajectories or
physiological hard speed bounds. Only nonidentifying aggregates may be exported.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from e002_457_directional_boundary import EXPECTED_SHA256, HOLDOUT, parse_csv

GAZES = ("bottom", "center", "top")
ABSTAIN = "ABSTAIN_UNCALIBRATED"


def _caps(rows):
    if not rows:
        raise ValueError("empty calibration stratum")
    return {"closing_mm_s": max(r["closing"] for r in rows),
            "opening_mm_s": max(r["opening"] for r in rows)}


def _decision(caps):
    c, o = caps["closing_mm_s"], caps["opening_mm_s"]
    if not all(math.isfinite(v) and v > 0 for v in (c, o)):
        raise ValueError("invalid speed cap")
    critical = 1000.0 * (1.0 / c + 1.0 / o)
    return {"critical_gap_ms_for_hypothetical_1mm_endpoints": critical,
            "240fps_conditional_exclusion_ideal_only": (1000.0 / 240.0) < critical}


def _test(rows, caps):
    over_c = [r for r in rows if r["closing"] > caps["closing_mm_s"]]
    over_o = [r for r in rows if r["opening"] > caps["opening_mm_s"]]
    over_any = [r for r in rows if (r["closing"] > caps["closing_mm_s"]
                                    or r["opening"] > caps["opening_mm_s"])]
    return {"blinks": len(rows), "participants": len({r["subject"] for r in rows}),
            "exceed_closing_blinks": len(over_c),
            "exceed_opening_blinks": len(over_o),
            "exceed_either_blinks": len(over_any),
            "exceed_either_participants": len({r["subject"] for r in over_any})}


def evaluate(rows, *, expected_count=None):
    if not isinstance(rows, list) or not rows:
        raise ValueError("empty source")
    if expected_count is not None and len(rows) != expected_count:
        raise ValueError("source row count mismatch")
    train, test = [], []
    for r in rows:
        if not isinstance(r, dict) or set(r) != {"subject", "gaze", "closing", "opening"}:
            raise ValueError("invalid source schema")
        sid, gaze = r["subject"], r["gaze"]
        if type(sid) is not int or sid <= 0 or gaze not in GAZES:
            raise ValueError("invalid participant or gaze")
        for k in ("closing", "opening"):
            v = r[k]
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0:
                raise ValueError("invalid peak speed")
        (test if sid in HOLDOUT else train).append(r)
    train_ids, test_ids = {r["subject"] for r in train}, {r["subject"] for r in test}
    if len(train_ids) != 12 or test_ids != HOLDOUT or train_ids & test_ids:
        raise ValueError("invalid participant-disjoint split")
    grouped = lambda arr: {g: [r for r in arr if r["gaze"] == g] for g in GAZES}
    tg, hg = grouped(train), grouped(test)
    if any(not tg[g] or not hg[g] for g in GAZES):
        raise ValueError("missing calibration or holdout gaze stratum")
    center = _caps(tg["center"])
    pooled = _caps(train)
    matched = {g: _caps(tg[g]) for g in GAZES}
    result = {}
    for g in GAZES:
        result[g] = {"calibration_blinks_in_gaze": len(tg[g]),
                     "heldout_blinks_in_gaze": len(hg[g]),
                     "heldout_participants_in_gaze": len({r["subject"] for r in hg[g]}),
                     "center_only_transfer": _test(hg[g], center),
                     "pooled_transfer": _test(hg[g], pooled),
                     "gaze_matched_transfer": _test(hg[g], matched[g])}
    noncenter = hg["bottom"] + hg["top"]
    primary = _test(noncenter, center)
    return {
        "experiment": "E002-459",
        "evidence_tier": "PUBLISHED_HUMAN_PER_BLINK_GAZE_SHIFT_NOT_PHYSICAL_APERTURE",
        "source_sha256": EXPECTED_SHA256,
        "participants": {"calibration": len(train_ids), "holdout": len(test_ids)},
        "blinks": {"calibration": len(train), "holdout": len(test)},
        "training_gaze_counts": {g: len(tg[g]) for g in GAZES},
        "center_only_training_caps": center,
        "pooled_training_caps": pooled,
        "gaze_matched_training_caps": matched,
        "hypothetical_1mm_ideal_camera": {
            "center_only": _decision(center), "pooled": _decision(pooled),
            "gaze_matched": {g: _decision(matched[g]) for g in GAZES}},
        "heldout_gaze_transfer": result,
        "primary_noncenter_center_trained": primary,
        "center_only_noncenter_falsified_in_sample":
            primary["exceed_either_blinks"] > 0,
        "statistical_warning": "Five held-out people, not independent blinks; sample maxima are not physiological hard caps.",
        "human_anatomical_trajectory_validation": "NOT_ESTABLISHED",
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows, signs = parse_csv(args.csv.read_bytes())
    if signs.get("negative", 0):
        raise ValueError("unexpected source opening sign convention")
    result = evaluate(rows, expected_count=2306)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
