#!/usr/bin/env python3
"""E002-456 sealed prospective holdout harness.

Private manifest contains interval identifiers and must NEVER be committed.
Public commitment is a SHA256 digest, not a trusted timestamp or privacy guarantee.
Independent timestamp escrow must precede unsealing anatomical references.
"""
import argparse
import hashlib
import json
from pathlib import Path

from e002_456_prospective_gate import evaluate_dataset, evaluate_interval


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def core(case):
    return {key: value for key, value in case.items() if key != "reference"}


def freeze(payload):
    cases = payload.get("intervals", [])
    if not cases or any(case.get("reference") != [] for case in cases):
        raise ValueError("freeze requires reference=[] for every interval")
    evaluate_dataset(payload)  # validates unique IDs and participant-disjoint splits
    predictions = []
    for case in cases:
        result = evaluate_interval(case)
        predictions.append({
            "interval_id": case["interval_id"],
            "split": case["split"],
            "input_sha256": digest(core(case)),
            "decision": result["decision"],
        })
    predictions.sort(key=lambda x: x["interval_id"])
    manifest = {"schema_version": "E002-456-private-v1",
                "predictions": predictions,
                "commitment_sha256": digest(predictions)}
    public = {"experiment": "E002-456",
              "evidence_tier": "FROZEN_PREDICTIONS_NO_HUMAN_REFERENCE",
              "commitment_sha256": manifest["commitment_sha256"],
              "intervals": len(predictions),
              "external_timestamp_escrow_verified": False,
              "physical_release_authorized": False,
              "product_claim": "ABSTAIN_UNCALIBRATED"}
    return manifest, public


def score(payload, manifest):
    if manifest.get("schema_version") != "E002-456-private-v1":
        raise ValueError("private manifest schema mismatch")
    preds = manifest.get("predictions")
    if not isinstance(preds, list) or digest(preds) != manifest.get("commitment_sha256"):
        raise ValueError("frozen commitment tampered")
    cases = payload.get("intervals", [])
    if len(cases) != len(preds):
        raise ValueError("holdout intervals added or removed")
    pred_by_id = {p["interval_id"]: p for p in preds}
    if len(pred_by_id) != len(preds):
        raise ValueError("duplicate frozen interval")
    for case in cases:
        p = pred_by_id.get(case.get("interval_id"))
        if p is None or p["split"] != case.get("split"):
            raise ValueError("unknown or changed holdout interval")
        if p["input_sha256"] != digest(core(case)):
            raise ValueError("frozen measurement, nuisance, or bound changed")
        if p["decision"] != evaluate_interval(case)["decision"]:
            raise ValueError("prediction no longer matches frozen evaluator")
    result = evaluate_dataset(payload)
    result["commitment_sha256"] = manifest["commitment_sha256"]
    result["external_timestamp_escrow_verified"] = False
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase", choices=("freeze", "score"))
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path,
                   help="public commitment or deidentified aggregate")
    a = p.parse_args()
    payload = json.loads(a.input.read_text(encoding="utf-8"))
    if a.phase == "freeze":
        manifest, result = freeze(payload)
        if a.manifest.exists():
            raise ValueError("refusing to overwrite existing frozen manifest")
        a.manifest.write_text(json.dumps(manifest, indent=2,
                                          sort_keys=True) + "\n", encoding="utf-8")
        try:
            a.manifest.chmod(0o600)
        except OSError:
            pass
    else:
        manifest = json.loads(a.manifest.read_text(encoding="utf-8"))
        result = score(payload, manifest)
    a.output.write_text(json.dumps(result, indent=2,
                                   sort_keys=True) + "\n", encoding="utf-8")
    print("E002-456:", a.phase, "complete; no physical release authorized")


if __name__ == "__main__":
    main()
