#!/usr/bin/env python3
"""E002-526: prelabel commitment to a quantitative cross-camera closure predicate.

Software-only, owner-private study gate. Does not authenticate timestamps,
calibration, human ratings, or a physiological velocity ceiling.
"""
import argparse
import hashlib
import hmac
import json
import math
from pathlib import Path
import re

from e002_520_cross_camera import evaluate as evaluate_transport

VERSION = "E002-526-v1"
EVALUATOR = "E002-520-v1"
DOMAIN = b"LUCENT/E002-526/transport-lock/v1\x00"
GAP_FIELDS = {"id", "participant", "session", "prediction",
              "left_end_max_ms", "right_start_min_ms", "ordinary_closure_threshold"}


def number(value):
    if type(value) not in (int, float):
        raise ValueError("INVALID_NUMERIC_FIELD")
    try:
        n = float(value)
    except OverflowError as exc:
        raise ValueError("INVALID_NUMERIC_FIELD") from exc
    if not math.isfinite(n) or abs(n) > 1e12:
        raise ValueError("INVALID_NUMERIC_FIELD")
    return n


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) != {"version", "nonce_hex", "evaluator", "gaps"}:
        raise ValueError("INVALID_MANIFEST_SCHEMA")
    if manifest["version"] != VERSION or manifest["evaluator"] != EVALUATOR:
        raise ValueError("INVALID_EVALUATOR_VERSION")
    nonce = manifest["nonce_hex"]
    if not isinstance(nonce, str) or re.fullmatch("[0-9a-f]{64}", nonce) is None or int(nonce, 16) == 0:
        raise ValueError("INVALID_NONCE")
    gaps = manifest["gaps"]
    if not isinstance(gaps, list) or not 0 < len(gaps) <= 20000:
        raise ValueError("INVALID_GAPS")
    ids = set()
    for g in gaps:
        if not isinstance(g, dict) or set(g) != GAP_FIELDS:
            raise ValueError("INVALID_GAP_SCHEMA")
        for key in ("id", "participant", "session"):
            v = g[key]
            if not isinstance(v, str) or not v.strip() or len(v) > 128:
                raise ValueError("INVALID_IDENTIFIER")
        if g["id"] in ids:
            raise ValueError("DUPLICATE_GAP")
        ids.add(g["id"])
        if g["prediction"] not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("INVALID_PREDICTION")
        if number(g["right_start_min_ms"]) <= number(g["left_end_max_ms"]):
            raise ValueError("INVALID_INTERVAL")
        theta = number(g["ordinary_closure_threshold"])
        if not 0 < theta < 1:
            raise ValueError("INVALID_THRESHOLD")
    return gaps


def commitment(manifest):
    validate_manifest(manifest)
    public = {k: manifest[k] for k in ("version", "evaluator", "gaps")}
    canonical = json.dumps(public, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(DOMAIN + bytes.fromhex(manifest["nonce_hex"]) + canonical).hexdigest()


def verify_and_evaluate(manifest, published_digest, evidence):
    gaps = validate_manifest(manifest)
    if not isinstance(published_digest, str) or re.fullmatch("[0-9a-f]{64}", published_digest) is None:
        raise ValueError("INVALID_PUBLISHED_DIGEST")
    if not hmac.compare_digest(commitment(manifest), published_digest):
        raise ValueError("COMMITMENT_MISMATCH")
    if not isinstance(evidence, dict) or set(evidence) != {"version", "gaps"} or evidence["version"] != EVALUATOR:
        raise ValueError("INVALID_EVIDENCE_VERSION")
    observed = evidence["gaps"]
    if not isinstance(observed, list) or len(observed) != len(gaps):
        raise ValueError("CHANGED_DENOMINATOR")
    by_id = {g["id"]: g for g in gaps}
    seen = set()
    for g in observed:
        if not isinstance(g, dict) or set(g) != GAP_FIELDS | {"references"}:
            raise ValueError("INVALID_EVIDENCE_GAP_SCHEMA")
        gid = g["id"]
        if not isinstance(gid, str) or gid not in by_id or gid in seen:
            raise ValueError("UNREGISTERED_OR_DUPLICATE_GAP")
        seen.add(gid)
        frozen = by_id[gid]
        for k in ("id", "participant", "session", "prediction"):
            if g[k] != frozen[k]:
                raise ValueError("POSTHOC_PREDICTION_OR_ATTRIBUTION")
        for k in ("left_end_max_ms", "right_start_min_ms", "ordinary_closure_threshold"):
            if number(g[k]) != number(frozen[k]):
                raise ValueError("POSTHOC_TIMING_OR_THRESHOLD")
    if seen != set(by_id):
        raise ValueError("MISSING_GAP")
    result = evaluate_transport(evidence)
    result["prelabel_digest_verified_by_code"] = True
    result["prelabel_publication_timestamp_authenticated_by_code"] = False
    result["human_or_camera_provenance_authenticated_by_code"] = False
    result["product"] = "ABSTAIN_UNCALIBRATED"
    result["release"] = "BLOCKED"
    return result


def load_json(path):
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
        manifest = load_json(args.manifest)
        if args.action == "digest":
            result = {"publish_digest_before_reference_review": commitment(manifest),
                      "release": "BLOCKED", "product": "ABSTAIN_UNCALIBRATED"}
        else:
            out = verify_and_evaluate(manifest, args.published_digest, load_json(args.evidence))
            result = {"counts": out["counts"], "prelabel_digest_verified_by_code": True,
                      "prelabel_publication_timestamp_authenticated_by_code": False,
                      "human_or_camera_provenance_authenticated_by_code": False,
                      "release": "BLOCKED", "product": "ABSTAIN_UNCALIBRATED"}
        print(json.dumps(result, sort_keys=True))
    except (ValueError, TypeError, KeyError, OverflowError, json.JSONDecodeError):
        parser.error("FAIL_CLOSED_INVALID_OR_UNLOCKED_STUDY")


if __name__ == "__main__":
    main()
