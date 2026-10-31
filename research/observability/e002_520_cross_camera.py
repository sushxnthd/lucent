#!/usr/bin/env python3
"""E002-520: conservative cross-camera closure-predicate witness intake.

This is an offline logical evaluator, NOT a camera calibrator or human rater.
All booleans and numeric calibration bounds require independent provenance.
"""
import argparse
import json
import math
from pathlib import Path

VERSION = "E002-520-v1"
FLAGS = (
    "two_independent_raters",
    "radiometry_linear_valid",
    "clock_valid",
    "native_provenance_valid",
    "geometry_transport_valid",
    "nuisance_clear",
)
ANATOMY = {"CLOSED_WITNESS", "OPEN_OBSERVED", "UNKNOWN"}
DECISIONS = (
    "FALSIFIED_BY_TRANSPORTED_REFERENCE_WITNESS",
    "REFERENCE_CENSORED_NOT_FALSIFIED",
    "UNKNOWN",
    "NOT_TESTABLE",
)


def finite(value, field):
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError("INVALID_" + field)
    if not math.isfinite(value):
        raise ValueError("INVALID_" + field)
    return float(value)


def optional_bound(record, field):
    if field not in record or record[field] is None:
        return None
    value = finite(record[field], field.upper())
    if value < 0:
        raise ValueError("NEGATIVE_" + field.upper())
    return value


def evaluate(payload):
    if not isinstance(payload, dict) or payload.get("version") != VERSION:
        raise ValueError("INVALID_VERSION")
    gaps = payload.get("gaps")
    if not isinstance(gaps, list) or not 0 < len(gaps) <= 20000:
        raise ValueError("INVALID_GAPS")
    decisions = []
    gap_ids = set()
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValueError("INVALID_GAP")
        gid = gap.get("id")
        if not isinstance(gid, str) or not gid or gid in gap_ids:
            raise ValueError("INVALID_GAP_ID")
        gap_ids.add(gid)
        if gap.get("prediction") not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("INVALID_PREDICTION")
        left = finite(gap.get("left_end_max_ms"), "LEFT_TIME")
        right = finite(gap.get("right_start_min_ms"), "RIGHT_TIME")
        theta = finite(gap.get("ordinary_closure_threshold"), "THRESHOLD")
        if not 0 <= theta <= 1:
            raise ValueError("INVALID_THRESHOLD")
        refs = gap.get("references")
        if not isinstance(refs, list) or len(refs) > 20000:
            raise ValueError("INVALID_REFERENCES")
        ref_ids = set()
        witness = None
        unresolved = not refs
        for ref in refs:
            if not isinstance(ref, dict):
                raise ValueError("INVALID_REFERENCE")
            rid = ref.get("id")
            if not isinstance(rid, str) or not rid or rid in ref_ids:
                raise ValueError("INVALID_REFERENCE_ID")
            ref_ids.add(rid)
            start = finite(ref.get("start_min_ms"), "REFERENCE_START")
            end = finite(ref.get("end_max_ms"), "REFERENCE_END")
            if end <= start or ref.get("anatomy") not in ANATOMY:
                raise ValueError("INVALID_REFERENCE_RECORD")
            if any(not isinstance(ref.get(flag), bool) for flag in FLAGS):
                raise ValueError("INVALID_REFERENCE_FLAGS")
            upper = optional_bound(ref, "reference_mean_aperture_upper")
            scale = optional_bound(ref, "transport_scale_upper")
            offset = optional_bound(ref, "transport_offset_upper")
            if ref["anatomy"] != "CLOSED_WITNESS":
                if ref["anatomy"] == "UNKNOWN" or not all(ref[f] for f in FLAGS):
                    unresolved = True
                continue
            if not all(ref[f] for f in FLAGS):
                unresolved = True
                continue
            if upper is None or scale is None or offset is None:
                unresolved = True
                continue
            if not (start > left and end < right):
                unresolved = True
                continue
            # Nonnegative aperture, linear exposure integration, and independently
            # validated pointwise transport imply mean(a_o) <= K*U_r+B.
            # Thus K*U_r+B <= theta implies existence of at least one closed instant.
            transported_upper = scale * upper + offset
            if not math.isfinite(transported_upper):
                raise ValueError("INVALID_TRANSPORT_PRODUCT")
            if transported_upper <= theta:
                witness = rid
            else:
                unresolved = True
        if gap["prediction"] != "EXCLUDE" or right <= left:
            decision = "NOT_TESTABLE"
        elif witness is not None:
            decision = DECISIONS[0]
        elif unresolved:
            decision = "UNKNOWN"
        else:
            decision = DECISIONS[1]
        decisions.append({
            "gap_id": gid,
            "decision": decision,
            "conditional_witness_reference_id": witness if decision == DECISIONS[0] else None,
        })
    return {
        "version": VERSION,
        "decisions": decisions,
        "counts": {d: sum(x["decision"] == d for x in decisions) for d in DECISIONS},
        "verified_no_hidden_closure": False,
        "human_or_instrument_provenance_authenticated_by_code": False,
        "legacy_e002_519_witness_admissible_without_transport": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must differ")
    try:
        result = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        parser.error("FAIL_CLOSED: " + str(exc))
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
