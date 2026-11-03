#!/usr/bin/env python3
"""E002-632: fail-closed, exact-rational prospective trial scorer.
Usage: python research/observability/e002_632_blind_trial_scorer.py trials.csv
No external dependencies. Does NOT validate calibration declarations. closure_hi_mm MUST be an independently certified upper threshold bound; point estimates are invalid.
"""
import csv
import sys
from fractions import Fraction as F

REQUIRED = ("trial_id", "calibration_hash", "gap_hi_s", "aperture0_lo_mm",
            "aperture1_lo_mm", "closure_hi_mm", "v_close_mm_s", "v_open_mm_s",
            "independent_velocity_certified", "exposure_timing_certified",
            "geometry_certified", "reference_crossing_state")

def yes(value):
    return value.strip().upper() == "YES"

def decide(row):
    if any(not row.get(k, "").strip() for k in REQUIRED):
        return "ABSTAIN_UNCALIBRATED", "missing_required_field"
    if any(not yes(row[k]) for k in ("independent_velocity_certified",
                                    "exposure_timing_certified", "geometry_certified")):
        return "ABSTAIN_UNCALIBRATED", "uncertified"
    try:
        gap = F(row["gap_hi_s"])
        a = F(row["aperture0_lo_mm"]) - F(row["closure_hi_mm"])
        b = F(row["aperture1_lo_mm"]) - F(row["closure_hi_mm"])
        vc = F(row["v_close_mm_s"])
        vo = F(row["v_open_mm_s"])
    except (ValueError, ZeroDivisionError):
        return "ABSTAIN_UNCALIBRATED", "invalid_numeric"
    if gap < 0 or a <= 0 or b <= 0 or vc <= 0 or vo <= 0:
        return "ABSTAIN_UNCALIBRATED", "invalid_domain"
    if a / vc + b / vo > gap:
        return "EXCLUDE", "strict_reachability"
    return "ABSTAIN_REACHABLE", "reachable_or_equality"

def score(rows):
    outputs = []
    false_exclusions = 0
    seen_ids = set()
    for row in rows:
        trial_id = row.get("trial_id", "").strip()
        if not trial_id or trial_id in seen_ids:
            raise ValueError("missing_or_duplicate_trial_id")
        seen_ids.add(trial_id)
    for row in rows:
        verdict, reason = decide(row)
        label = row.get("reference_crossing_state", "").strip().upper()
        if label not in ("YES", "NO", "UNKNOWN"):
            label = "UNKNOWN"
        false_exclusion = verdict == "EXCLUDE" and label == "YES"
        false_exclusions += int(false_exclusion)
        outputs.append(dict(trial_id=row.get("trial_id", ""), verdict=verdict,
                            reason=reason, reference_crossing_state=label,
                            false_exclusion=str(false_exclusion).lower()))
    return outputs, false_exclusions

def selftest():
    base = dict(zip(REQUIRED, ("t1", "sha256:example", "1/100",
        "2", "2", "0", "100", "100", "YES", "YES", "YES", "YES")))
    assert decide(base)[0] == "EXCLUDE"  # 40ms reachability > 10ms gap
    x = dict(base, gap_hi_s="1/25")
    assert decide(x)[0] == "ABSTAIN_REACHABLE"  # exact equality
    x = dict(base, gap_hi_s="1/20")
    assert decide(x)[0] == "ABSTAIN_REACHABLE"
    x = dict(base, independent_velocity_certified="NO")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    x = dict(base, closure_hi_mm="3/2", gap_hi_s="1/50")
    assert decide(x)[0] == "ABSTAIN_REACHABLE"  # E002-635 threshold counterexample
    x = dict(base, closure_hi_mm="0", gap_hi_s="1/50")
    assert decide(x)[0] == "EXCLUDE"  # certified zero threshold
    x = dict(base, closure_hi_mm="")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    x = dict(base, aperture0_lo_mm="0")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    x = dict(base, gap_hi_s="-1")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    x = dict(base, exposure_timing_certified="NO")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    x = dict(base, geometry_certified="NO")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    x = dict(base, aperture0_lo_mm="n/a")
    assert decide(x)[0] == "ABSTAIN_UNCALIBRATED"
    try:
        score([base, base])
        raise AssertionError("duplicate trial ID accepted")
    except ValueError as exc:
        assert str(exc) == "missing_or_duplicate_trial_id"
    out, failures = score([base])
    assert failures == 1 and out[0]["false_exclusion"] == "true"
    # This deliberate contradictory reference label tests the release blocker,
    # NOT the theorem; the stipulated physical bound and label cannot both hold.
    return "14 prospective scorer assertions passed"

def main():
    print(selftest(), file=sys.stderr)
    if len(sys.argv) == 1:
        return
    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)) or any(not h for h in headers):
            raise ValueError("duplicate_or_empty_csv_header")
        if not set(REQUIRED).issubset(headers):
            raise ValueError("missing_required_csv_header")
        rows = list(reader)
        if any(None in row for row in rows):
            raise ValueError("extra_csv_columns")
    try:
        outputs, failures = score(rows)
    except ValueError as exc:
        print(f"RELEASE_BLOCKED=True INPUT_ERROR={exc}", file=sys.stderr)
        sys.exit(3)
    writer = csv.DictWriter(sys.stdout, fieldnames=("trial_id", "verdict",
        "reason", "reference_crossing_state", "false_exclusion"))
    writer.writeheader()
    writer.writerows(outputs)
    print(f"TRIALS={len(outputs)} FALSE_EXCLUSIONS={failures} RELEASE_BLOCKED={failures > 0}",
          file=sys.stderr)
    if failures:
        sys.exit(2)

if __name__ == "__main__":
    main()
