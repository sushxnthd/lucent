#!/usr/bin/env python3
"""E002-521: exact conditional exposure-mean to total closure-time witness.

No human ratings, camera clocks, or calibration are authenticated by this code.
The output is a conditional lower bound on TOTAL closure time in one exposure,
never a contiguous blink, fatigue measure, or no-hidden-blink certificate.
"""
import argparse
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import json
from pathlib import Path

VERSION = "E002-521-v1"
FLAGS = (
    "two_independent_raters",
    "radiometry_linear_valid",
    "integration_uniform_valid",
    "clock_valid",
    "native_provenance_valid",
    "geometry_transport_valid",
    "nuisance_clear",
    "ordinary_aperture_bounded_01",
)
ANATOMY = {"CLOSED_WITNESS", "OPEN_OBSERVED", "UNKNOWN"}
POSITIVE = "FALSIFIED_WITH_POSITIVE_CLOSURE_MEASURE"
CONTACT = "FALSIFIED_BY_THRESHOLD_CONTACT_ONLY"
CENSORED = "REFERENCE_CENSORED_NOT_FALSIFIED"
UNKNOWN = "UNKNOWN"
NOT_TESTABLE = "NOT_TESTABLE"
DECISIONS = (POSITIVE, CONTACT, CENSORED, UNKNOWN, NOT_TESTABLE)


def exact_number(value, name):
    """Interpret supplied finite-decimal JSON numbers exactly, not binary floats."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError("INVALID_" + name)
    try:
        d = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("INVALID_" + name) from exc
    if not d.is_finite() or len(d.as_tuple().digits) > 30 or abs(d.adjusted()) > 18:
        raise ValueError("INVALID_" + name)
    return Fraction(d)


def nonnegative(record, key):
    if key not in record or record[key] is None:
        return None
    n = exact_number(record[key], key.upper())
    if n < 0:
        raise ValueError("NEGATIVE_" + key.upper())
    return n


def evaluate(payload):
    if not isinstance(payload, dict) or payload.get("version") != VERSION:
        raise ValueError("INVALID_VERSION")
    gaps = payload.get("gaps")
    if not isinstance(gaps, list) or not 0 < len(gaps) <= 20000:
        raise ValueError("INVALID_GAPS")
    seen_gaps = set()
    results = []
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValueError("INVALID_GAP")
        gid = gap.get("id")
        if not isinstance(gid, str) or not gid or gid in seen_gaps:
            raise ValueError("INVALID_GAP_ID")
        seen_gaps.add(gid)
        if gap.get("prediction") not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("INVALID_PREDICTION")
        left = exact_number(gap.get("left_end_max_ms"), "LEFT_TIME")
        right = exact_number(gap.get("right_start_min_ms"), "RIGHT_TIME")
        if right <= left:
            raise ValueError("EMPTY_OR_NEGATIVE_GAP")
        theta = exact_number(gap.get("ordinary_closure_threshold"), "THRESHOLD")
        if not 0 < theta < 1:
            raise ValueError("INVALID_THRESHOLD")
        refs = gap.get("references")
        if not isinstance(refs, list) or len(refs) > 20000:
            raise ValueError("INVALID_REFERENCES")
        seen_refs = set()
        best = None
        contact = None
        unresolved = not refs
        for ref in refs:
            if not isinstance(ref, dict):
                raise ValueError("INVALID_REFERENCE")
            rid = ref.get("id")
            if not isinstance(rid, str) or not rid or rid in seen_refs:
                raise ValueError("INVALID_REFERENCE_ID")
            seen_refs.add(rid)
            start = exact_number(ref.get("start_min_ms"), "REFERENCE_START")
            end = exact_number(ref.get("end_max_ms"), "REFERENCE_END")
            if end <= start or ref.get("anatomy") not in ANATOMY:
                raise ValueError("INVALID_REFERENCE_RECORD")
            if any(not isinstance(ref.get(flag), bool) for flag in FLAGS):
                raise ValueError("INVALID_REFERENCE_FLAGS")
            duration = nonnegative(ref, "exposure_duration_lower_ms")
            upper = nonnegative(ref, "reference_mean_aperture_upper")
            scale = nonnegative(ref, "transport_scale_upper")
            offset = nonnegative(ref, "transport_offset_upper")
            if duration is not None and duration > end - start:
                raise ValueError("IMPOSSIBLE_EXPOSURE_DURATION_LOWER_BOUND")
            if ref["anatomy"] != "CLOSED_WITNESS":
                if ref["anatomy"] == "UNKNOWN" or not all(ref[f] for f in FLAGS):
                    unresolved = True
                continue
            if not all(ref[f] for f in FLAGS) or any(x is None for x in (duration, upper, scale, offset)):
                unresolved = True
                continue
            if duration <= 0 or not (start > left and end < right):
                unresolved = True
                continue
            mean_upper = scale * upper + offset
            if mean_upper > theta:
                unresolved = True
                continue
            if mean_upper == theta:
                contact = rid
                continue
            # Exact lower bound: p >= 1 - M/theta, |C| >= w_min * p.
            # No derivative ceiling is used; the bound is total measure only.
            fraction = 1 - mean_upper / theta
            lower_time = duration * fraction
            if best is None or lower_time > best[1]:
                best = (rid, lower_time, fraction)
        if gap["prediction"] == "ABSTAIN":
            decision = NOT_TESTABLE
        elif best is not None:
            decision = POSITIVE
        elif contact is not None:
            decision = CONTACT
        elif unresolved:
            decision = UNKNOWN
        else:
            decision = CENSORED
        results.append({
            "gap_id": gid,
            "decision": decision,
            "conditional_witness_reference_id": best[0] if decision == POSITIVE else (contact if decision == CONTACT else None),
            "total_closure_fraction_lower_bound_exact": str(best[2]) if decision == POSITIVE else None,
            "total_closure_time_ms_lower_bound_exact": str(best[1]) if decision == POSITIVE else None,
            "contiguous_blink_duration_certified": False,
        })
    return {
        "version": VERSION,
        "decisions": results,
        "counts": {k: sum(x["decision"] == k for x in results) for k in DECISIONS},
        "calibration_or_human_provenance_authenticated_by_code": False,
        "verified_no_hidden_closure": False,
        "contiguous_blink_certified": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.input.resolve() == args.output.resolve():
        ap.error("Input and output must differ")
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"), parse_float=Decimal)
        result = evaluate(payload)
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        ap.error("FAIL_CLOSED: " + str(exc))
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
