#!/usr/bin/env python3
"""E002-647: fail-closed analysis of physical LED shutter trials.

Input CSV follows E002-644; no generated/synthetic rows count as physical evidence.
This instrument deliberately never infers guaranteed optical detection from exposure overlap.
E002-650 correction: an unenumerated second exposure invalidates a single-interval\nmiss certificate; require an explicit complete-single-exposure declaration.\nE002-648 correction: a generic visibility flag cannot establish source-specific
causation, so apparent signals during certified misses abstain rather than falsify.
"""
import argparse
import csv
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = (
    "trial_id", "raw_video_sha256", "reference_sha256", "camera_mode",
    "exposure_interval_lo_us", "exposure_interval_hi_us", "row_index",
    "pulse_start_lo_us", "pulse_start_hi_us", "pulse_end_lo_us",
    "pulse_end_hi_us", "measured_visibility", "visibility_floor",
    "sync_status", "exclusion_verdict", "adjudication_notes",
    "exposure_coverage_status"
)

def number(value):
    try:
        x = Decimal(value)
        return x if x.is_finite() else None
    except (InvalidOperation, TypeError, ValueError):
        return None

def analyze(row):
    if any(not row.get(k, "").strip() for k in REQUIRED if k != "adjudication_notes"):
        return "ABSTAIN", "missing_required_field"
    # A single row interval cannot establish a miss if additional exposures,
    # rolling-shutter rows, or retained sensor integrations are unaccounted for.
    # This is a declaration only, NOT independent authentication.
    if row["exposure_coverage_status"].strip().lower() != "complete_single_exposure":
        return "ABSTAIN", "exposure_coverage_unverified"
    if row["sync_status"].strip().lower() not in ("ok", "calibrated"):
        return "ABSTAIN", "uncalibrated_clock"
    for k in ("raw_video_sha256", "reference_sha256"):
        digest = row[k].strip().lower()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            return "ABSTAIN", "invalid_evidence_digest"
    keys = ("exposure_interval_lo_us", "exposure_interval_hi_us",
            "pulse_start_lo_us", "pulse_start_hi_us", "pulse_end_lo_us", "pulse_end_hi_us")
    vals = [number(row[k]) for k in keys]
    if any(v is None for v in vals):
        return "ABSTAIN", "invalid_timing"
    e0, e1, s0, s1, t0, t1 = vals
    if not (e0 < e1 and s0 <= s1 and t0 <= t1 and s1 <= t0):
        return "ABSTAIN", "inconsistent_timing"
    # Certified miss requires pulse support disjoint from the exposure,
    # for every allowed realization of the uncertain endpoints.
    miss = t1 < e0 or s0 > e1
    if not miss:
        return "ABSTAIN", "overlap_or_uncertain"
    seen = row["measured_visibility"].strip().lower()
    if seen in ("true", "1", "visible", "yes"):
        # E002-648: a generic visibility flag cannot attribute the signal to
        # the randomized LED source. Ambient light and sensor persistence are
        # observationally confounded with timing-model leakage in this CSV.
        return "ABSTAIN", "unattributed_signal_despite_certified_miss"
    if seen in ("false", "0", "invisible", "no"):
        return "NON_FALSIFYING", "miss_not_seen_does_not_validate_timing"
    return "ABSTAIN", "unadjudicated_visibility"

def run(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            raise ValueError("E002-644 CSV columns missing")
        rows = list(reader)
    ids = [r["trial_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate trial IDs; cannot count independent trials")
    decisions = [{"trial_id": r["trial_id"], "camera_mode": r["camera_mode"],
                  "classification": c, "reason": reason}
                 for r in rows for c, reason in [analyze(r)]]
    return {"evidence_tier": "USER_SUPPLIED_UNVERIFIED_INSTRUMENT_ROWS",
            "n_rows": len(rows),
            "counts": dict(Counter(d["classification"] for d in decisions)),
            "decisions": decisions,
            "warning": "No physiological or human inference; SHA strings are not independently verified file contents."}

def selftest():
    base = dict.fromkeys(REQUIRED, "")
    base.update(trial_id="t", raw_video_sha256="a"*64, reference_sha256="b"*64,
                camera_mode="m", exposure_interval_lo_us="10",
                exposure_interval_hi_us="20", row_index="0",
                pulse_start_lo_us="1", pulse_start_hi_us="2",
                pulse_end_lo_us="3", pulse_end_hi_us="4",
                measured_visibility="no", visibility_floor="1",
                sync_status="ok", exclusion_verdict="EXCLUDE",
                exposure_coverage_status="complete_single_exposure")
    assert analyze(base)[0] == "NON_FALSIFYING"
    assert analyze({**base, "measured_visibility": "yes"}) == ("ABSTAIN", "unattributed_signal_despite_certified_miss")
    assert analyze({**base, "pulse_end_hi_us": "11"})[0] == "ABSTAIN"
    assert analyze({**base, "sync_status": "failed"})[0] == "ABSTAIN"
    assert analyze({**base, "raw_video_sha256": ""})[0] == "ABSTAIN"
    assert analyze({**base, "exposure_interval_hi_us": "9"})[0] == "ABSTAIN"
    assert analyze({**base, "exposure_coverage_status": ""}) == ("ABSTAIN", "missing_required_field")
    assert analyze({**base, "exposure_coverage_status": "multiple_exposures"}) == ("ABSTAIN", "exposure_coverage_unverified")
    assert analyze({**base, "exposure_interval_lo_us": "1000", "exposure_interval_hi_us": "2000"})[0] == "NON_FALSIFYING"
    print("9 fail-closed self-tests passed (synthetic; NOT physical validation)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="?", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    if args.csv:
        print(json.dumps(run(args.csv), indent=2))
    elif not args.selftest:
        parser.error("provide CSV or --selftest")
