"""E002-426: prospective participant-disjoint human-reference evaluation.

Research registry and descriptive scorer, NOT physical calibration or authorization
for real-world no-hidden-closure product claims.
"""
import argparse
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

PREDICTIONS = {"NO_CROSSING_CONDITIONAL", "POSSIBLE_CROSSING", "ABSTAIN"}
REFERENCES = {"WITNESSED_CROSSING", "NEGATIVE_CONDITIONAL", "UNRESOLVED", "MISSING"}
NUISANCES = ("brightness", "blur", "gaze", "glasses", "occlusion", "missingness", "clock")
ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")


class RegistryError(ValueError):
    pass


def _ident(value, name):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise RegistryError(f"invalid {name}: require 1-64 alphanumeric/_/- characters")
    return value


def _ids(values, name):
    if not isinstance(values, list) or not values:
        raise RegistryError(f"{name} must be a nonempty list")
    parsed = [_ident(v, name) for v in values]
    if len(set(parsed)) != len(parsed):
        raise RegistryError(f"duplicate {name}")
    return set(parsed)


def validate_registry(data):
    if not isinstance(data, dict) or set(data) != {"study_id", "training_participants", "holdout_participants", "device_ids", "trials"}:
        raise RegistryError("invalid registry top-level schema")
    _ident(data["study_id"], "study_id")
    train = _ids(data["training_participants"], "training_participants")
    holdout = _ids(data["holdout_participants"], "holdout_participants")
    devices = _ids(data["device_ids"], "device_ids")
    if train & holdout:
        raise RegistryError("training/holdout participant leakage")
    trials = data["trials"]
    if not isinstance(trials, list) or not trials:
        raise RegistryError("trials must be nonempty")
    seen, seen_participants, seen_devices = set(), set(), set()
    for trial in trials:
        keys = {"trial_id", "participant_id", "device_id", "interval_start_s", "interval_end_s", "prediction", "nuisance_flags", "model_input_sha256", "camera_calibration_ref", "velocity_bound_ref"}
        if not isinstance(trial, dict) or set(trial) != keys:
            raise RegistryError("invalid trial schema")
        tid = _ident(trial["trial_id"], "trial_id")
        if tid in seen:
            raise RegistryError("duplicate trial_id")
        seen.add(tid)
        pid = _ident(trial["participant_id"], "participant_id")
        dev = _ident(trial["device_id"], "device_id")
        if pid not in holdout or dev not in devices:
            raise RegistryError("unknown/non-holdout participant or device")
        seen_participants.add(pid)
        seen_devices.add(dev)
        a, b = trial["interval_start_s"], trial["interval_end_s"]
        if any(type(x) not in (int, float) or not math.isfinite(x) for x in (a, b)) or not (0 <= a < b):
            raise RegistryError("invalid interval")
        if trial["prediction"] not in PREDICTIONS:
            raise RegistryError("invalid prediction")
        flags = trial["nuisance_flags"]
        if not isinstance(flags, dict) or set(flags) != set(NUISANCES) or any(type(v) is not bool for v in flags.values()):
            raise RegistryError("all nuisance flags must be explicit booleans")
        if not isinstance(trial["model_input_sha256"], str) or not DIGEST.fullmatch(trial["model_input_sha256"]):
            raise RegistryError("invalid model input hash")
        for name in ("camera_calibration_ref", "velocity_bound_ref"):
            _ident(trial[name], name)
    if seen_participants != holdout or seen_devices != devices:
        raise RegistryError("every preregistered holdout participant and device must have a trial")
    return data


def canonical_bytes(data):
    validate_registry(data)
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def seal(data):
    return {"schema": "E002-426-SEAL-v1", "sha256": hashlib.sha256(canonical_bytes(data)).hexdigest(), "trial_count": len(data["trials"])}


def verify_seal(data, archived_seal):
    if not isinstance(archived_seal, dict) or set(archived_seal) != {"schema", "sha256", "trial_count"}:
        raise RegistryError("invalid seal schema")
    if archived_seal != seal(data):
        raise RegistryError("prediction registry differs from separately archived seal")


def read_reference_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != ["trial_id", "reference_label"]:
            raise RegistryError("reference CSV must have exactly trial_id,reference_label columns")
        out = {}
        for row in reader:
            if None in row or set(row) != {"trial_id", "reference_label"}:
                raise RegistryError("malformed reference row")
            tid = _ident(row["trial_id"], "reference trial_id")
            if tid in out:
                raise RegistryError("duplicate reference trial_id")
            if row["reference_label"] not in REFERENCES:
                raise RegistryError("invalid reference label")
            out[tid] = row["reference_label"]
    return out


def _bounds(trials, references):
    eligible = len(trials)
    selected = [t for t in trials if t["prediction"] == "NO_CROSSING_CONDITIONAL"]
    n = len(selected)
    failures = sum(references[t["trial_id"]] == "WITNESSED_CROSSING" for t in selected)
    unresolved = sum(references[t["trial_id"]] in {"UNRESOLVED", "MISSING"} for t in selected)
    return {"eligible": eligible, "conditional_predictions": n,
            "abstentions": sum(t["prediction"] == "ABSTAIN" for t in trials),
            "witnessed_failures": failures, "unresolved_references": unresolved,
            "conditional_prediction_fraction": n / eligible if eligible else None,
            "finite_set_false_certificate_lower": failures / n if n else None,
            "finite_set_false_certificate_upper": (failures + unresolved) / n if n else None}


def score(data, archived_seal, references):
    verify_seal(data, archived_seal)
    expected = {t["trial_id"] for t in data["trials"]}
    if set(references) != expected:
        raise RegistryError("reference rows must match every frozen trial exactly; no silent dropping")
    if any(v not in REFERENCES for v in references.values()):
        raise RegistryError("invalid reference label")
    trials = data["trials"]
    groups = defaultdict(list)
    for t in trials:
        groups[t["participant_id"]].append(t)
    by_participant = {pid: _bounds(items, references) for pid, items in sorted(groups.items())}
    selected_groups = [b for b in by_participant.values() if b["conditional_predictions"] > 0]
    macro = {"participants_with_conditional_predictions": len(selected_groups),
             "finite_set_false_certificate_lower": (sum(x["finite_set_false_certificate_lower"] for x in selected_groups) / len(selected_groups) if selected_groups else None),
             "finite_set_false_certificate_upper": (sum(x["finite_set_false_certificate_upper"] for x in selected_groups) / len(selected_groups) if selected_groups else None)}
    nuisance = {key: {str(flag).lower(): _bounds([t for t in trials if t["nuisance_flags"][key] is flag], references)
                      for flag in (False, True)} for key in NUISANCES}
    return {"experiment": "E002-426", "evidence_tier": "registry-and-reference-label accounting only; externally unverified",
            "study_id": data["study_id"], "registry_sha256": archived_seal["sha256"],
            "pooled": _bounds(trials, references), "participant_macro": macro,
            "participant_groups": by_participant, "nuisance_strata": nuisance,
            "external_physical_provenance_authenticated": False,
            "human_rater_independence_authenticated": False,
            "population_guarantee": False,
            "product": "ABSTAIN_UNCALIBRATED", "product_claim_authorized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fr = sub.add_parser("freeze", help="validate and print an externally archivable seal")
    fr.add_argument("--registry", required=True)
    sc = sub.add_parser("score", help="score independent reference CSV against frozen seal")
    sc.add_argument("--registry", required=True)
    sc.add_argument("--seal", required=True)
    sc.add_argument("--reference", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    if args.command == "freeze":
        print(json.dumps(seal(data), indent=2, sort_keys=True))
    else:
        archived_seal = json.loads(Path(args.seal).read_text(encoding="utf-8"))
        print(json.dumps(score(data, archived_seal, read_reference_csv(args.reference)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
