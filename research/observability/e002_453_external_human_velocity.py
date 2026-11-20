#!/usr/bin/env python3
"""E002-453: participant-disjoint transfer audit of *estimated* human peak blink velocities.

Input is the public Culemann et al. OSF Blinks.csv; raw data are never committed.
An observed training maximum is NOT a deterministic physiological upper bound.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
from statistics import median

SOURCE_URL = "https://osf.io/download/m34qd/"
EXPECTED_SHA256 = "6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43"
HOLDOUT_SUBJECTS = frozenset({3, 6, 9, 12, 15})
REQUIRED = ("subject", "target_pos", "peak_closing_velocity",
            "peak_opening_velocity", "closing_amplitude", "duration")


def parse_csv(raw: bytes):
    decoded = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames or any(key not in reader.fieldnames for key in REQUIRED):
        raise ValueError("required Culemann et al. schema absent")
    rows, exclusions = [], 0
    for rec in reader:
        try:
            subject_f = float(rec["subject"])
            if not math.isfinite(subject_f) or not subject_f.is_integer():
                raise ValueError("invalid subject")
            subject = int(subject_f)
            gaze = rec["target_pos"]
            if gaze not in ("top", "center", "bottom"):
                raise ValueError("unknown gaze")
            values = [float(rec[key]) for key in REQUIRED[2:]]
            if not all(math.isfinite(x) for x in values) or values[0] < 0:
                raise ValueError("invalid velocity or other measurement")
            rows.append({"subject": subject, "gaze": gaze, "v": values[0]})
        except (TypeError, ValueError, KeyError):
            exclusions += 1
    return rows, exclusions


def nearest_rank(xs, q):
    if not xs or not 0 < q <= 1:
        raise ValueError("invalid quantile")
    return sorted(xs)[math.ceil(q * len(xs)) - 1]


def transfer_audit(rows, exclusions=0):
    train = [r for r in rows if r["subject"] not in HOLDOUT_SUBJECTS]
    test = [r for r in rows if r["subject"] in HOLDOUT_SUBJECTS]
    train_subjects = {r["subject"] for r in train}
    test_subjects = {r["subject"] for r in test}
    if not train or not test or train_subjects & test_subjects:
        raise ValueError("participant-disjoint train/test both required")
    if test_subjects != HOLDOUT_SUBJECTS:
        raise ValueError("one or more frozen holdout subjects absent")
    for r in rows:
        if not math.isfinite(r["v"]) or r["v"] < 0:
            raise ValueError("nonfinite or negative velocity")
    v_train = [r["v"] for r in train]
    v_test = [r["v"] for r in test]
    max_cap = max(v_train)
    q99_cap = nearest_rank(v_train, .99)
    gazes = ("bottom", "center", "top")
    gaze_caps = {g: max([r["v"] for r in train if r["gaze"] == g], default=None)
                 for g in gazes}

    def violations(name, capfn):
        evaluable = [r for r in test if capfn(r) is not None]
        exceeded = [r for r in evaluable if r["v"] > capfn(r)]
        subject_counts = [sum(r["subject"] == s for r in exceeded)
                          for s in sorted(test_subjects)]
        return {
            "count": len(exceeded),
            "denominator": len(evaluable),
            "abstained": len(test) - len(evaluable),
            "max_exceedance_ratio": (max(r["v"] / capfn(r) for r in exceeded)
                                     if exceeded else None),
            "holdout_subjects_with_exceedance": sum(n > 0 for n in subject_counts),
            "max_exceedances_per_holdout_subject": max(subject_counts),
            "by_gaze": {g: {
                "count": sum(r["gaze"] == g for r in exceeded),
                "denominator": sum(r["gaze"] == g for r in evaluable),
            } for g in gazes},
        }

    gap_ms = 2000.0 / max_cap if max_cap else None
    return {
        "evidence_tier": "EXTERNAL_HUMAN_DERIVED_PEAK_ESTIMATES_NOT_HARD_CAP",
        "rows": {
            "valid": len(rows), "excluded": exclusions,
            "participants": len(train_subjects | test_subjects),
            "train_subjects": len(train_subjects), "holdout_subjects": len(test_subjects),
            "train": len(train), "holdout": len(test),
        },
        "train": {"min": min(v_train), "median": median(v_train),
                  "max": max_cap, "q99_nearest_rank": q99_cap},
        "holdout": {"min": min(v_test), "median": median(v_test), "max": max(v_test)},
        "gaze": {g: {
            "train_n": sum(r["gaze"] == g for r in train),
            "train_max": gaze_caps[g],
            "holdout_n": sum(r["gaze"] == g for r in test),
            "holdout_max": max([r["v"] for r in test if r["gaze"] == g], default=None),
        } for g in gazes},
        "tests": {
            "pooled_train_max": violations("max", lambda r: max_cap),
            "pooled_train_q99": violations("q99", lambda r: q99_cap),
            "gaze_train_max": violations("gaze", lambda r: gaze_caps[r["gaze"]]),
        },
        "illustrative": {
            "a0_mm": 3.0, "a1_mm": 3.0, "threshold_mm": 2.0,
            "train_max_mm_s": max_cap, "critical_gap_ms": gap_ms,
            "nominal_fps_gap_ms": {str(fps): 1000.0 / fps for fps in (30, 60, 240)},
            "nominal_gap_shorter_than_illustrative_threshold": {
                str(fps): (1000.0 / fps < gap_ms) if gap_ms is not None else False
                for fps in (30, 60, 240)
            },
        },
        "physical_release_authorized": False,
        "product_claim": "ABSTAIN_UNCALIBRATED",
    }


def analyze_file(path: Path):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError("OSF source SHA256 mismatch; refuse unverified human data")
    rows, exclusions = parse_csv(raw)
    result = transfer_audit(rows, exclusions)
    result["source"] = {"url": SOURCE_URL, "sha256_verified": True,
                        "sha256": digest, "bytes": len(raw)}
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", type=Path, required=True, help="local authorized Blinks.csv")
    p.add_argument("--out", type=Path, help="write deidentified aggregate JSON")
    a = p.parse_args()
    result = analyze_file(a.csv)
    rendered = json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if a.out:
        a.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
