#!/usr/bin/env python3
"""E002-525 prospective lock for owner-private E002-519 reference evidence.

This checks a published *commitment*, not its publication timestamp, human
independence, camera provenance or physical closure. No images or labels are
uploaded; CLI prints aggregate counts only.
"""
import argparse
import hashlib
import hmac
import json
import math
from pathlib import Path
import re

from e002_519_reference_censoring import evaluate as evaluate_519

VERSION = "E002-525-v1"
DOMAIN = b"LUCENT/E002-525/v1\x00"


def finite_number(x):
    if type(x) not in (int, float) or not math.isfinite(x):
        raise ValueError("INVALID_FINITE_BOUND")
    return x


def validate_manifest(m):
    if not isinstance(m, dict) or set(m) != {"version", "nonce_hex", "gaps"} or m["version"] != VERSION:
        raise ValueError("INVALID_MANIFEST")
    nonce = m["nonce_hex"]
    if not isinstance(nonce, str) or re.fullmatch(r"[0-9a-f]{64}", nonce) is None or int(nonce, 16) == 0:
        raise ValueError("INVALID_PRIVATE_NONCE")
    gaps = m["gaps"]
    if not isinstance(gaps, list) or not 0 < len(gaps) <= 20000:
        raise ValueError("INVALID_MANIFEST_GAPS")
    ids = set()
    for g in gaps:
        if not isinstance(g, dict) or set(g) != {
            "id", "participant", "session", "prediction", "left_end_max_ms", "right_start_min_ms"
        }:
            raise ValueError("INVALID_MANIFEST_GAP_SCHEMA")
        for key in ("id", "participant", "session"):
            if not isinstance(g[key], str) or not g[key].strip() or len(g[key]) > 128:
                raise ValueError("INVALID_PRIVATE_IDENTIFIER")
        if g["id"] in ids:
            raise ValueError("DUPLICATE_FROZEN_GAP")
        ids.add(g["id"])
        if g["prediction"] not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("INVALID_FROZEN_PREDICTION")
        if finite_number(g["right_start_min_ms"]) <= finite_number(g["left_end_max_ms"]):
            raise ValueError("INVALID_FROZEN_GAP_INTERVAL")
    return gaps


def commitment(m):
    gaps = validate_manifest(m)
    canonical = json.dumps({"version": VERSION, "gaps": gaps}, sort_keys=True,
                           separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(DOMAIN + bytes.fromhex(m["nonce_hex"]) + canonical).hexdigest()


def verify_and_evaluate(m, published_digest, evidence):
    """Fail closed before the historical E002-519 evaluator sees any labels."""
    expected = commitment(m)
    if not isinstance(published_digest, str) or re.fullmatch(r"[0-9a-f]{64}", published_digest) is None:
        raise ValueError("INVALID_PUBLISHED_COMMITMENT")
    if not hmac.compare_digest(expected, published_digest):
        raise ValueError("FROZEN_MANIFEST_COMMITMENT_MISMATCH")
    if not isinstance(evidence, dict) or evidence.get("version") != "E002-519-v1":
        raise ValueError("INVALID_REFERENCE_EVIDENCE")
    observed = evidence.get("gaps")
    if not isinstance(observed, list) or len(observed) != len(m["gaps"]):
        raise ValueError("CHANGED_FROZEN_DENOMINATOR")
    frozen = {g["id"]: g for g in m["gaps"]}
    seen = set()
    for g in observed:
        if not isinstance(g, dict) or not isinstance(g.get("id"), str):
            raise ValueError("INVALID_EVIDENCE_GAP")
        gid = g["id"]
        if gid in seen or gid not in frozen:
            raise ValueError("UNREGISTERED_OR_DUPLICATE_GAP")
        seen.add(gid)
        f = frozen[gid]
        for k in ("participant", "session", "prediction"):
            if g.get(k) != f[k]:
                raise ValueError("POSTHOC_PREDICTION_OR_ATTRIBUTION")
        for k in ("left_end_max_ms", "right_start_min_ms"):
            if finite_number(g.get(k)) != f[k]:
                raise ValueError("POSTHOC_TIMING_CHANGE")
    if seen != set(frozen):
        raise ValueError("MISSING_FROZEN_GAP")
    result = evaluate_519(evidence)
    result["prospective_manifest_digest_verified"] = True
    result["prospective_timestamp_authenticated_by_code"] = False
    result["reference_attribution_authenticated_by_code"] = False
    result["human_independence_authenticated_by_code"] = False
    result["product"] = "ABSTAIN_UNCALIBRATED"
    result["release"] = "BLOCKED"
    return result


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    d = sub.add_parser("digest", help="Compute private manifest digest BEFORE reference review")
    d.add_argument("--manifest", required=True)
    v = sub.add_parser("verify", help="Check published digest and evaluate private evidence")
    v.add_argument("--manifest", required=True)
    v.add_argument("--published-digest", required=True)
    v.add_argument("--evidence", required=True)
    args = p.parse_args()
    try:
        manifest = load_json(args.manifest)
        if args.action == "digest":
            print(json.dumps({"version": VERSION, "publish_digest_before_reference_review": commitment(manifest),
                              "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}, sort_keys=True))
        else:
            result = verify_and_evaluate(manifest, args.published_digest, load_json(args.evidence))
            # Aggregate only; no participant IDs, individual predictions, reference IDs or nonce.
            print(json.dumps({"version": VERSION, "counts": result["counts"],
                              "prospective_manifest_digest_verified": True,
                              "prospective_timestamp_authenticated_by_code": False,
                              "human_evidence_authenticated_by_code": False,
                              "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}, sort_keys=True))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        p.error("FAIL_CLOSED_INVALID_OR_UNLOCKED_STUDY")


if __name__ == "__main__":
    main()
