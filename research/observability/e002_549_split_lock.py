#!/usr/bin/env python3
"""E002-549: prospective participant-split + prediction-lock gate.

A digest match establishes only byte-level consistency with the digest supplied
by the caller. It does NOT authenticate the digest's publication time, camera,
anatomy, rater independence, or the human origin of supplied records.
"""
import argparse
import hashlib
import hmac
import json
import re
from pathlib import Path

from e002_548_witness import audit as legacy_witness_audit

EXPLORATORY = (
    "S-24", "S-22", "S-27", "S-17", "S-23", "S-01", "S-18", "S-04",
    "S-19", "S-29", "S-14", "S-12", "S-05", "S-11", "S-25",
)
HELDOUT = (
    "S-08", "S-28", "S-16", "S-21", "S-31", "S-07", "S-10", "S-02",
    "S-15", "S-20", "S-30", "S-06", "S-26", "S-09", "S-03", "S-13",
)
SPLITS = {"exploratory": frozenset(EXPLORATORY), "heldout": frozenset(HELDOUT)}
assert len(SPLITS["exploratory"]) == 15 and len(SPLITS["heldout"]) == 16
assert not SPLITS["exploratory"] & SPLITS["heldout"]
assert SPLITS["exploratory"] | SPLITS["heldout"] == {f"S-{i:02d}" for i in range(1, 32)}
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def prediction_digest(predictions):
    if not isinstance(predictions, list):
        raise ValueError("predictions must be array")
    # Order is deliberately retained: the entire locked prediction manifest matters.
    canonical = json.dumps({"schema": "lucent-e002-549-v1", "predictions": predictions},
                           sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                           allow_nan=False).encode("utf-8")
    return hashlib.sha256(b"lucent-e002-549-v1\n" + canonical).hexdigest()


def audit_locked(bundle, expected_digest):
    if not isinstance(bundle, dict) or bundle.get("schema") != "lucent-e002-548-v1":
        raise ValueError("unsupported witness bundle")
    if not isinstance(expected_digest, str) or not HEX64.fullmatch(expected_digest):
        raise ValueError("external expected prediction digest required")
    predictions = bundle.get("predictions")
    frames = bundle.get("reference_frames")
    if not isinstance(predictions, list) or not isinstance(frames, list):
        raise ValueError("predictions and frames must be arrays")
    # Caller must obtain this expected digest from an independently retained precommit.
    if not hmac.compare_digest(prediction_digest(predictions), expected_digest):
        raise ValueError("prediction manifest differs from externally supplied digest")
    if bundle.get("origin") not in ("human", "synthetic"):
        raise ValueError("origin invalid")
    known = SPLITS["exploratory"] | SPLITS["heldout"]
    by_gap = {}
    for p in predictions:
        if not isinstance(p, dict) or p.get("participant_id") not in known:
            raise ValueError("unknown or missing participant in frozen split")
        if p.get("gap_id") in by_gap:
            raise ValueError("duplicate gap identity")
        by_gap[p.get("gap_id")] = p
    for f in frames:
        if not isinstance(f, dict) or f.get("gap_id") not in by_gap:
            raise ValueError("reference frame lacks locked prediction")
        p = by_gap[f["gap_id"]]
        for key in ("participant_id", "session_id", "eye", "roi_id"):
            if f.get(key) != p.get(key):
                raise ValueError("cross-participant/session/eye/ROI reference contamination")
    # Existing witness audit enforces exposure containment and censors negatives.
    legacy_witness_audit(bundle)
    groups = {}
    for name, members in SPLITS.items():
        selected = [p for p in predictions if p["participant_id"] in members]
        gap_ids = {p["gap_id"] for p in selected}
        subset = {"schema": bundle["schema"], "origin": bundle["origin"],
                  "predictions": selected,
                  "reference_frames": [f for f in frames if f["gap_id"] in gap_ids]}
        a = legacy_witness_audit(subset)
        groups[name] = {
            "participants_with_predictions": len({p["participant_id"] for p in selected}),
            "participants_with_exclusions": len({p["participant_id"] for p in selected if p["prediction"] == "EXCLUDE"}),
            "candidate_participants": a["candidate_participant_count"],
            "counts": a["counts"],
        }
    return {
        "schema": "lucent-e002-549-aggregate-v1",
        "evidence_tier": "SYNTHETIC_PROVENANCE_TEST_ONLY" if bundle["origin"] == "synthetic" else "HUMAN_INPUT_UNAUTHENTICATED",
        "prediction_digest_consistent": True,
        "precommit_provenance": "EXTERNAL_PRECOMMIT_TIMESTAMP_UNVERIFIED",
        "groups": groups,
        "certified_exclusions": 0,
        "human_physical_validation": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--expected-prediction-sha256", required=True)
    args = parser.parse_args()
    with args.bundle.open(encoding="utf-8") as handle:
        bundle = json.load(handle, parse_float=str)
    print(json.dumps(audit_locked(bundle, args.expected_prediction_sha256), sort_keys=True))


if __name__ == "__main__":
    main()
