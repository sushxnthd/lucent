#!/usr/bin/env python3
"""E002-522: conservative physical closure-time inference with bounded shutter weighting.

An independently calibrated shutter-response concentration R replaces the
uniform-integration assumption. This program does not authenticate calibration,
human raters, or native camera timing. It never certifies a blink or release.
"""
import argparse
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import json
from pathlib import Path

VERSION = "E002-522-v1"
FLAGS = (
    "two_independent_raters",
    "radiometry_linear_valid",
    "shutter_response_nonnegative_valid",
    "shutter_response_normalized_valid",
    "shutter_response_envelope_calibrated",
    "clock_valid",
    "native_provenance_valid",
    "geometry_transport_valid",
    "nuisance_clear",
    "ordinary_aperture_bounded_01",
)
POSITIVE = "FALSIFIED_WITH_CONDITIONAL_WEIGHTED_SHUTTER_DURATION"
CENSORED = "REFERENCE_CENSORED_NOT_FALSIFIED"
UNKNOWN = "UNKNOWN"
NOT_TESTABLE = "NOT_TESTABLE"
DECISIONS = (POSITIVE, CENSORED, UNKNOWN, NOT_TESTABLE)


def rational(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError("INVALID_" + label)
    try:
        d = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("INVALID_" + label) from exc
    if not d.is_finite() or len(d.as_tuple().digits) > 30 or abs(d.adjusted()) > 18:
        raise ValueError("INVALID_" + label)
    return Fraction(d)


def optional_nonnegative(record, field):
    if record.get(field) is None:
        return None
    v = rational(record[field], field.upper())
    if v < 0:
        raise ValueError("NEGATIVE_" + field.upper())
    return v


def evaluate(payload):
    if not isinstance(payload, dict) or payload.get("version") != VERSION:
        raise ValueError("INVALID_VERSION")
    gaps = payload.get("gaps")
    if not isinstance(gaps, list) or not 0 < len(gaps) <= 20000:
        raise ValueError("INVALID_GAPS")
    out, seen_gaps = [], set()
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValueError("INVALID_GAP")
        gid = gap.get("id")
        if not isinstance(gid, str) or not gid or gid in seen_gaps:
            raise ValueError("INVALID_GAP_ID")
        seen_gaps.add(gid)
        if gap.get("prediction") not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("INVALID_PREDICTION")
        left = rational(gap.get("left_end_max_ms"), "LEFT_TIME")
        right = rational(gap.get("right_start_min_ms"), "RIGHT_TIME")
        if right <= left:
            raise ValueError("EMPTY_GAP")
        theta = rational(gap.get("ordinary_closure_threshold"), "THRESHOLD")
        if not 0 < theta < 1:
            raise ValueError("INVALID_THRESHOLD")
        refs = gap.get("references")
        if not isinstance(refs, list) or len(refs) > 20000:
            raise ValueError("INVALID_REFERENCES")
        seen_refs, best, unresolved = set(), None, not refs
        for ref in refs:
            if not isinstance(ref, dict):
                raise ValueError("INVALID_REFERENCE")
            rid = ref.get("id")
            if not isinstance(rid, str) or not rid or rid in seen_refs:
                raise ValueError("INVALID_REFERENCE_ID")
            seen_refs.add(rid)
            start = rational(ref.get("start_min_ms"), "START")
            end = rational(ref.get("end_max_ms"), "END")
            if end <= start or ref.get("anatomy") not in ("CLOSED_WITNESS", "OPEN_OBSERVED", "UNKNOWN"):
                raise ValueError("INVALID_REFERENCE_RECORD")
            if any(not isinstance(ref.get(f), bool) for f in FLAGS):
                raise ValueError("INVALID_FLAGS")
            duration = optional_nonnegative(ref, "exposure_duration_lower_ms")
            mean = optional_nonnegative(ref, "reference_weighted_mean_aperture_upper")
            scale = optional_nonnegative(ref, "transport_scale_upper")
            offset = optional_nonnegative(ref, "transport_offset_upper")
            R = optional_nonnegative(ref, "shutter_weight_concentration_upper")
            if duration is not None and duration > end - start:
                raise ValueError("IMPOSSIBLE_DURATION")
            if R is not None and R < 1:
                raise ValueError("INVALID_CONCENTRATION_CAP")
            if ref["anatomy"] != "CLOSED_WITNESS":
                if ref["anatomy"] == "UNKNOWN" or not all(ref[f] for f in FLAGS):
                    unresolved = True
                continue
            if not all(ref[f] for f in FLAGS) or any(x is None for x in (duration, mean, scale, offset, R)):
                unresolved = True
                continue
            if duration <= 0 or not (left < start and end < right):
                unresolved = True
                continue
            M = scale * mean + offset
            if M >= theta:
                unresolved = True
                continue
            fraction = (1 - M / theta) / R
            time_lower = duration * fraction
            if best is None or time_lower > best[1]:
                best = (rid, time_lower, fraction)
        if gap["prediction"] == "ABSTAIN":
            decision = NOT_TESTABLE
        elif best is not None:
            decision = POSITIVE
        elif unresolved:
            decision = UNKNOWN
        else:
            decision = CENSORED
        out.append({
            "gap_id": gid, "decision": decision,
            "conditional_witness_reference_id": best[0] if decision == POSITIVE else None,
            "total_closure_fraction_lower_bound_exact": str(best[2]) if decision == POSITIVE else None,
            "total_closure_time_ms_lower_bound_exact": str(best[1]) if decision == POSITIVE else None,
            "contiguous_blink_certified": False,
        })
    return {
        "version": VERSION, "decisions": out,
        "counts": {d: sum(x["decision"] == d for x in out) for d in DECISIONS},
        "instrument_or_human_provenance_authenticated_by_code": False,
        "verified_no_hidden_closure": False,
        "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.input.resolve() == args.output.resolve():
        p.error("Input and output must differ")
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"), parse_float=Decimal)
        result = evaluate(payload)
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        p.error("FAIL_CLOSED: " + str(exc))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
