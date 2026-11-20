#!/usr/bin/env python3
"""E002-457: directional closure boundary and external human two-phase velocity audit.

The mathematics assumes HARD signed speed bounds; observed human peak velocities
are NOT hard physiological limits. This module never authorizes physical claims.
Only aggregate results may be written or printed.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path

SOURCE_URL = "https://osf.io/download/m34qd/"
EXPECTED_SHA256 = "6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43"
HOLDOUT = frozenset({3, 6, 9, 12, 15})
FPS = (30, 60, 120, 240, 480, 1000)
NUISANCES = ("geometry", "brightness", "missingness", "blur", "gaze",
             "glasses", "sampling", "clock", "rolling_shutter")
ABSTAIN = "ABSTAIN_UNCALIBRATED"


def finite(x, *, positive=False):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError("numeric input required")
    v = float(x)
    if not math.isfinite(v) or (positive and v <= 0):
        raise ValueError("invalid numeric input")
    return v


def exact_boundary(a0, a1, threshold, closing, opening, gap_s):
    """Exact conditional instantaneous-endpoint feasibility under -C <= a' <= O."""
    a0, a1, threshold = finite(a0), finite(a1), finite(threshold)
    C, O = finite(closing, positive=True), finite(opening, positive=True)
    dt = finite(gap_s)
    if dt < 0 or min(a0, a1, threshold) < 0:
        raise ValueError("negative time or aperture")
    tol = 1e-12 * max(1.0, abs(a0), abs(a1), C * dt, O * dt)
    if a1 - a0 > O * dt + tol or a0 - a1 > C * dt + tol:
        return {"decision": "ABSTAIN", "reason": "INFEASIBLE_ENDPOINTS"}
    if min(a0, a1) <= threshold:
        return {"decision": "NOT_EXCLUDED", "critical_gap_s": 0.0}
    critical = (a0 - threshold) / C + (a1 - threshold) / O
    return {"decision": "EXCLUDED_CONDITIONALLY" if dt < critical - 1e-12 else
            "NOT_EXCLUDED", "critical_gap_s": critical,
            "dimensionless_gap_ratio": dt / critical}


def shutter_gate(case):
    """Conservative sufficient exclusion for averaged, uncertain endpoints."""
    try:
        if not isinstance(case, dict) or any(case.get("nuisance", {}).get(k) != "PASS"
                                              for k in NUISANCES):
            return {"decision": "ABSTAIN", "reason": "NUISANCE_NOT_CLEARED"}
        if case.get("hard_directional_bound_verified") is not True:
            return {"decision": "ABSTAIN", "reason": "HARD_BOUND_NOT_VERIFIED"}
        C = finite(case["closing_mm_s"], positive=True)
        O = finite(case["opening_mm_s"], positive=True)
        c = finite(case["threshold_mm"])
        a0, a1 = (finite(x) for x in case["apertures_mm"])
        u0, u1 = (finite(x) for x in case["uncertainties_mm"])
        t0, t1 = (finite(x) for x in case["times_ms"])
        e = finite(case["exposure_ms"])
        err = finite(case["clock_error_ms"])
        if min(c, a0, a1, u0, u1, e, err) < 0 or t1 <= t0:
            return {"decision": "ABSTAIN", "reason": "INVALID_MEASUREMENT"}
        if e + 2 * err >= t1 - t0:
            return {"decision": "ABSTAIN", "reason": "EXPOSURE_CLOCK_OVERLAP"}
        kernel = case["kernel"]
        if kernel == "uniform_symmetric":
            s = (C + O) * e / 8000.0
        elif kernel == "support_symmetric":
            s = max(C, O) * e / 2000.0
        else:
            return {"decision": "ABSTAIN", "reason": "UNKNOWN_SHUTTER"}
        b0, b1 = a0 - u0 - s, a1 - u1 - s
        dt = (t1 - t0 + 2 * err) / 1000.0
        if min(b0, b1) <= c:
            return {"decision": "NOT_EXCLUDED", "reason": "ENDPOINT_UNCERTAIN",
                    "physical_release_authorized": False, "product_claim": ABSTAIN}
        critical = (b0 - c) / C + (b1 - c) / O
        return {"decision": "EXCLUDED_CONDITIONALLY" if dt < critical - 1e-12
                else "NOT_EXCLUDED", "reason": "CONDITIONAL_MATH_ONLY",
                "critical_gap_ms": critical * 1000,
                "dimensionless_gap_ratio": dt / critical,
                "physical_release_authorized": False, "product_claim": ABSTAIN}
    except (KeyError, TypeError, ValueError, OverflowError, AttributeError):
        return {"decision": "ABSTAIN", "reason": "INVALID_SCHEMA"}


def parse_csv(raw):
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("source SHA256 mismatch")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    keys = {"subject", "target_pos", "peak_closing_velocity",
            "peak_opening_velocity"}
    if not reader.fieldnames or not keys.issubset(reader.fieldnames):
        raise ValueError("missing columns")
    rows = []
    signs = Counter()
    for rec in reader:
        try:
            sid = float(rec["subject"])
            C = float(rec["peak_closing_velocity"])
            raw_O = float(rec["peak_opening_velocity"])
            if not sid.is_integer() or not all(math.isfinite(x) for x in (sid, C, raw_O)):
                raise ValueError("invalid row")
            if C <= 0 or raw_O == 0:
                raise ValueError("zero/negative closing or zero opening")
            if rec["target_pos"] not in ("bottom", "center", "top"):
                raise ValueError("unknown gaze")
            signs["negative" if raw_O < 0 else "positive"] += 1
            rows.append({"subject": int(sid), "gaze": rec["target_pos"],
                         "closing": C, "opening": abs(raw_O)})
        except (TypeError, KeyError, ValueError, OverflowError) as exc:
            raise ValueError("invalid human source row") from exc
    if not rows:
        raise ValueError("empty human source")
    return rows, dict(signs)


def audit_rows(rows, signs):
    train = [r for r in rows if r["subject"] not in HOLDOUT]
    test = [r for r in rows if r["subject"] in HOLDOUT]
    train_ids = {r["subject"] for r in train}
    test_ids = {r["subject"] for r in test}
    if test_ids != HOLDOUT or train_ids & test_ids or len(train_ids) != 12:
        raise ValueError("participant split invalid")
    C = max(r["closing"] for r in train)
    O = max(r["opening"] for r in train)
    V = max(C, O)
    exceeds_C = [r for r in test if r["closing"] > C]
    exceeds_O = [r for r in test if r["opening"] > O]
    exceeds_any = [r for r in test if r["closing"] > C or r["opening"] > O]
    critical_directional = 1000.0 * (1.0 / C + 1.0 / O)
    critical_symmetric = 2000.0 / V
    decisions = {}
    for fps in FPS:
        dt = 1000.0 / fps
        decisions[str(fps)] = {
            "nominal_gap_ms": dt,
            "directional_conditional_exclusion": dt < critical_directional,
            "symmetric_conditional_exclusion": dt < critical_symmetric,
        }
    return {
        "experiment": "E002-457",
        "source_sha256": EXPECTED_SHA256,
        "evidence_tier": "PUBLISHED_HUMAN_PER_BLINK_ESTIMATES_NOT_HARD_BOUNDS",
        "participants": {"calibration": len(train_ids), "holdout": len(test_ids)},
        "blinks": {"calibration": len(train), "holdout": len(test)},
        "opening_velocity_original_signs": signs,
        "calibration_estimated_peaks_mm_s": {
            "closing_max": C, "opening_abs_max": O, "symmetric_max": V},
        "holdout_exceedances": {
            "closing": len(exceeds_C), "opening": len(exceeds_O),
            "either": len(exceeds_any),
            "participants_either": len({r["subject"] for r in exceeds_any})},
        "illustrative_1mm_equal_endpoint_margin": {
            "directional_critical_gap_ms": critical_directional,
            "symmetric_critical_gap_ms": critical_symmetric,
            "relative_increase": critical_directional / critical_symmetric - 1.0,
            "fps_decisions": decisions,
        },
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
        "human_anatomical_trajectory_validation": "NOT_ESTABLISHED",
        "caution": "Per-blink sample peaks cannot certify hard directional limits."
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    result = audit_rows(*parse_csv(args.csv.read_bytes()))
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2,
                                   allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
