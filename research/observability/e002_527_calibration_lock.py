#!/usr/bin/env python3
"""E002-527: preregistered transport calibration bound, synthetic study gate.

Does not authenticate calibration provenance, camera clock, anatomy or humans.
"""
import argparse
import hashlib
import hmac
import json
import math
from pathlib import Path
import re

from e002_520_cross_camera import evaluate as evaluate_transport, FLAGS

VERSION = "E002-527-v1"
EVALUATOR = "E002-520-v1"
DOMAIN = b"LUCENT/E002-527/calibration-lock/v1\x00"
GAP_FIELDS = {
    "id", "participant", "session", "prediction",
    "left_end_max_ms", "right_start_min_ms", "ordinary_closure_threshold",
    "calibration_id", "transport_scale_upper", "transport_offset_upper",
}
REF_FIELDS = {
    "id", "start_min_ms", "end_max_ms", "anatomy", "two_independent_raters",
    "radiometry_linear_valid", "clock_valid", "native_provenance_valid",
    "geometry_transport_valid", "nuisance_clear",
    "reference_mean_aperture_upper", "transport_scale_upper",
    "transport_offset_upper", "calibration_id",
}


def finite(x):
    if type(x) not in (float, int):
        raise ValueError("INVALID_NUMBER")
    try:
        y = float(x)
    except OverflowError as exc:
        raise ValueError("INVALID_NUMBER") from exc
    if not math.isfinite(y) or abs(y) > 1e12:
        raise ValueError("INVALID_NUMBER")
    return y


def identifier(x):
    if not isinstance(x, str) or not x.strip() or len(x) > 128:
        raise ValueError("INVALID_IDENTIFIER")
    return x


def validate_manifest(m):
    if not isinstance(m, dict) or set(m) != {"version", "nonce_hex", "evaluator", "gaps"}:
        raise ValueError("INVALID_MANIFEST_SCHEMA")
    if m["version"] != VERSION or m["evaluator"] != EVALUATOR:
        raise ValueError("INVALID_VERSION")
    nonce = m["nonce_hex"]
    if not isinstance(nonce, str) or not re.fullmatch("[0-9a-f]{64}", nonce) or int(nonce, 16) == 0:
        raise ValueError("INVALID_NONCE")
    gaps = m["gaps"]
    if not isinstance(gaps, list) or not 0 < len(gaps) <= 20000:
        raise ValueError("INVALID_GAPS")
    ids = set()
    for g in gaps:
        if not isinstance(g, dict) or set(g) != GAP_FIELDS:
            raise ValueError("INVALID_GAP_SCHEMA")
        for key in ("id", "participant", "session", "calibration_id"):
            identifier(g[key])
        if g["id"] in ids:
            raise ValueError("DUPLICATE_GAP")
        ids.add(g["id"])
        if g["prediction"] not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("INVALID_PREDICTION")
        if finite(g["right_start_min_ms"]) <= finite(g["left_end_max_ms"]):
            raise ValueError("INVALID_INTERVAL")
        if not 0 < finite(g["ordinary_closure_threshold"]) < 1:
            raise ValueError("INVALID_THRESHOLD")
        if finite(g["transport_scale_upper"]) < 0 or finite(g["transport_offset_upper"]) < 0:
            raise ValueError("INVALID_CALIBRATION")
    return gaps


def commitment(m):
    validate_manifest(m)
    public = {k: m[k] for k in ("version", "evaluator", "gaps")}
    canonical = json.dumps(public, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(DOMAIN + bytes.fromhex(m["nonce_hex"]) + canonical).hexdigest()


def verify_and_evaluate(m, published_digest, evidence):
    gaps = validate_manifest(m)
    if not isinstance(published_digest, str) or not re.fullmatch("[0-9a-f]{64}", published_digest):
        raise ValueError("INVALID_PUBLISHED_DIGEST")
    if not hmac.compare_digest(commitment(m), published_digest):
        raise ValueError("COMMITMENT_MISMATCH")
    if not isinstance(evidence, dict) or set(evidence) != {"version", "gaps"} or evidence["version"] != EVALUATOR:
        raise ValueError("INVALID_EVIDENCE")
    observed = evidence["gaps"]
    if not isinstance(observed, list) or len(observed) != len(gaps):
        raise ValueError("CHANGED_DENOMINATOR")
    frozen = {g["id"]: g for g in gaps}
    seen = set()
    projected = []
    for g in observed:
        if not isinstance(g, dict) or set(g) != GAP_FIELDS | {"references"}:
            raise ValueError("INVALID_EVIDENCE_GAP_SCHEMA")
        gid = identifier(g["id"])
        if gid not in frozen or gid in seen:
            raise ValueError("UNREGISTERED_OR_DUPLICATE_GAP")
        seen.add(gid)
        f = frozen[gid]
        for key in ("id", "participant", "session", "prediction", "calibration_id"):
            if g[key] != f[key]:
                raise ValueError("POSTHOC_ATTRIBUTION_OR_CALIBRATION")
        for key in ("left_end_max_ms", "right_start_min_ms", "ordinary_closure_threshold",
                    "transport_scale_upper", "transport_offset_upper"):
            if finite(g[key]) != finite(f[key]):
                raise ValueError("POSTHOC_TIMING_PREDICATE_OR_CALIBRATION")
        refs = g["references"]
        if not isinstance(refs, list) or len(refs) > 20000:
            raise ValueError("INVALID_REFERENCES")
        clean_refs = []
        for ref in refs:
            if not isinstance(ref, dict) or set(ref) != REF_FIELDS:
                raise ValueError("INVALID_REFERENCE_SCHEMA")
            if ref["calibration_id"] != f["calibration_id"]:
                raise ValueError("POSTHOC_REFERENCE_CALIBRATION_ID")
            for key in ("transport_scale_upper", "transport_offset_upper"):
                if finite(ref[key]) != finite(f[key]):
                    raise ValueError("POSTHOC_REFERENCE_CALIBRATION_BOUND")
            if any(type(ref[flag]) is not bool for flag in FLAGS):
                raise ValueError("INVALID_FLAGS")
            clean_refs.append({k: v for k, v in ref.items() if k != "calibration_id"})
        clean_gap = {k: v for k, v in g.items()
                     if k not in ("calibration_id", "transport_scale_upper", "transport_offset_upper", "references")}
        clean_gap["references"] = clean_refs
        projected.append(clean_gap)
    if seen != set(frozen):
        raise ValueError("MISSING_GAP")
    result = evaluate_transport({"version": EVALUATOR, "gaps": projected})
    result["prelabel_digest_verified_by_code"] = True
    result["prelabel_publication_timestamp_authenticated_by_code"] = False
    result["physical_calibration_authenticated_by_code"] = False
    result["human_anatomy_authenticated_by_code"] = False
    result["product"] = "ABSTAIN_UNCALIBRATED"
    result["release"] = "BLOCKED"
    return result


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    d = sub.add_parser("digest")
    d.add_argument("--manifest", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--manifest", required=True)
    v.add_argument("--published-digest", required=True)
    v.add_argument("--evidence", required=True)
    args = parser.parse_args()
    try:
        m = load(args.manifest)
        if args.action == "digest":
            out = {"publish_digest_before_reference_review": commitment(m)}
        else:
            r = verify_and_evaluate(m, args.published_digest, load(args.evidence))
            out = {"counts": r["counts"], "prelabel_digest_verified_by_code": True,
                   "physical_calibration_authenticated_by_code": False}
        out.update(product="ABSTAIN_UNCALIBRATED", release="BLOCKED")
        print(json.dumps(out, sort_keys=True))
    except (ValueError, TypeError, KeyError, OverflowError, json.JSONDecodeError):
        parser.error("FAIL_CLOSED_INVALID_OR_UNLOCKED_STUDY")


if __name__ == "__main__":
    main()
