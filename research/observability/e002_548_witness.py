#!/usr/bin/env python3
"""E002-548 one-sided, exposure-aware reference-witness audit.

Consumes private local JSON; prints aggregate-only output. A syntactically complete
record is NOT independent physical authentication or human validation.
"""
import argparse
import json
import re
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

HEX = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_ORIGINS = {"synthetic", "human"}


def decimal(value, name):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError(f"{name}: decimal string required")
    try:
        out = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{name}: invalid decimal") from exc
    if not out.is_finite():
        raise ValueError(f"{name}: nonfinite")
    return out


def sha(value, name):
    if not isinstance(value, str) or HEX.fullmatch(value) is None:
        raise ValueError(f"{name}: require lowercase SHA-256 hex")
    return value


def audit(bundle):
    if not isinstance(bundle, dict) or bundle.get("schema") != "lucent-e002-548-v1":
        raise ValueError("unsupported schema")
    origin = bundle.get("origin")
    if origin not in ALLOWED_ORIGINS:
        raise ValueError("origin must be synthetic or human")
    predictions = bundle.get("predictions")
    frames = bundle.get("reference_frames")
    if not isinstance(predictions, list) or not isinstance(frames, list):
        raise ValueError("predictions and reference_frames must be arrays")
    if len(predictions) > 100000 or len(frames) > 1000000:
        raise ValueError("bundle too large")
    by_gap = {}
    for p in predictions:
        if not isinstance(p, dict):
            raise ValueError("prediction not object")
        gap = p.get("gap_id")
        if not isinstance(gap, str) or not 1 <= len(gap) <= 128 or gap in by_gap:
            raise ValueError("missing/duplicate gap_id")
        sha(p.get("lock_sha256"), "lock_sha256")
        start = decimal(p.get("blind_start_ms"), "blind_start_ms")
        end = decimal(p.get("blind_end_ms"), "blind_end_ms")
        threshold = decimal(p.get("closure_threshold"), "closure_threshold")
        if start >= end or not (Decimal(0) < threshold < Decimal(1)):
            raise ValueError("invalid gap/threshold")
        if p.get("prediction") not in ("EXCLUDE", "ABSTAIN"):
            raise ValueError("prediction must be EXCLUDE or ABSTAIN")
        eye = p.get("eye")
        if eye not in ("left", "right"):
            raise ValueError("eye invalid")
        by_gap[gap] = (p, start, end, threshold)
    grouped = {g: [] for g in by_gap}
    seen_frame = set()
    for f in frames:
        if not isinstance(f, dict) or f.get("gap_id") not in by_gap:
            raise ValueError("frame references missing gap")
        identity = (f.get("gap_id"), f.get("frame_id"))
        if not isinstance(f.get("frame_id"), str) or not f["frame_id"] or identity in seen_frame:
            raise ValueError("missing/duplicate frame identity")
        seen_frame.add(identity)
        grouped[f["gap_id"]].append(f)
    counts = Counter()
    participant_candidate_ids = set()
    for gap, (p, start, end, threshold) in by_gap.items():
        if p["prediction"] != "EXCLUDE":
            counts["ABSTAIN_NO_EXCLUSION"] += 1
            continue
        candidate = False
        for f in grouped[gap]:
            if f.get("eye") != p["eye"] or f.get("quality") != "valid":
                continue
            # Certificates are ASSERTED by input, not authenticated by parser.
            if f.get("timing_evidence") != "independent_calibration" or f.get("transfer_evidence") != "independent_calibration":
                continue
            if f.get("rater_1") != "closed" or f.get("rater_2") != "closed":
                continue
            if not all(isinstance(f.get(k), str) and f[k] for k in ("timing_certificate_id", "transfer_certificate_id")):
                continue
            sha(f.get("frame_sha256"), "frame_sha256")
            lower = decimal(f.get("support_earliest_ms"), "support_earliest_ms")
            upper = decimal(f.get("support_latest_ms"), "support_latest_ms")
            mean_hi = decimal(f.get("mean_aperture_upper"), "mean_aperture_upper")
            if lower >= upper or not (Decimal(0) <= mean_hi <= Decimal(1)):
                raise ValueError("invalid support/aperture")
            # Entire possible exposure support must lie STRICTLY inside
            # the guaranteed ordinary-camera blind interval.
            if start < lower and upper < end and mean_hi <= threshold:
                candidate = True
                break
        if candidate:
            counts["SYNTHETIC_WITNESS_ONLY" if origin == "synthetic" else "HUMAN_WITNESS_CANDIDATE_EXTERNAL_REVIEW"] += 1
            pid = p.get("participant_id")
            if isinstance(pid, str) and pid:
                participant_candidate_ids.add(pid)
        else:
            counts["REFERENCE_CENSORED"] += 1
    return {
        "schema": "lucent-e002-548-aggregate-v1",
        "origin": origin,
        "gap_count": len(by_gap),
        "counts": dict(sorted(counts.items())),
        "candidate_participant_count": len(participant_candidate_ids),
        "certified_exclusions": 0,
        "release_status": "ABSTAIN_UNCALIBRATED",
        "note": "No raw identifiers, frames or individual decisions exported. Candidate evidence is not independently authenticated by this tool; reference-negative observations are censored.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    with args.bundle.open(encoding="utf-8") as f:
        obj = json.load(f, parse_float=str)
    print(json.dumps(audit(obj), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
