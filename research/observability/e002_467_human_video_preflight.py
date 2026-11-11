#!/usr/bin/env python3
"""E002-467: image-level human-frame preflight; NEVER a physical closure certificate.

CSV schema: participant_id,sequence_id,frame_index,timestamp_ms,aperture_mm,
aperture_error_mm,quality_ok,annotation_ok,geometry_ok,sync_ok,shutter_ok,
nuisance_ok. All booleans 0/1 or true/false. Geometry/shutter flags are
declarations, NOT authenticated calibrations. No participant-level output.
"""
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

SUBJECTS = tuple(f"S{i:02d}" for i in range(1, 32))
SALT = "lucent-e002-467-v1|"
ORDER = sorted(SUBJECTS, key=lambda s: (hashlib.sha256((SALT+s).encode()).hexdigest(), s))
CALIBRATION = frozenset(ORDER[:23])
HOLDOUT = frozenset(ORDER[23:])
REQUIRED = ("participant_id", "sequence_id", "frame_index", "timestamp_ms",
            "aperture_mm", "aperture_error_mm", "quality_ok", "annotation_ok",
            "geometry_ok", "sync_ok", "shutter_ok", "nuisance_ok")
FLAGS = ("quality_ok", "annotation_ok", "geometry_ok", "sync_ok",
         "shutter_ok", "nuisance_ok")
FRAME_MS = 1000.0 / 150.0

def flag(value):
    v = str(value).strip().lower()
    if v in ("1", "true"):
        return True
    if v in ("0", "false"):
        return False
    return None

def finite(value):
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None

def analyze(rows, threshold_mm, tolerance_ms=1.5):
    if not math.isfinite(threshold_mm) or threshold_mm <= 0:
        raise ValueError("positive finite threshold required")
    if not math.isfinite(tolerance_ms) or tolerance_ms < 0 or tolerance_ms >= FRAME_MS:
        raise ValueError("invalid timestamp tolerance")
    groups = defaultdict(list)
    for row in rows:
        if not all(k in row for k in REQUIRED):
            raise ValueError("CSV missing required columns")
        subject = row["participant_id"]
        seq = row["sequence_id"]
        if subject not in SUBJECTS or not seq or len(seq) > 256:
            raise ValueError("invalid subject/sequence")
        groups[(subject, seq)].append(row)
    counts = {split: {"sequences":0, "frames":0, "image_subthreshold_candidates":0,
                      "unresolved_frames":0, "invalid_sequences":0}
              for split in ("calibration", "holdout")}
    for (subject, _seq), group in sorted(groups.items()):
        split = "calibration" if subject in CALIBRATION else "holdout"
        c = counts[split]
        c["sequences"] += 1
        c["frames"] += len(group)
        # Never sort bad timestamps into validity. Missing, repeated or jittered
        # samples invalidate the whole sequence for this preflight.
        valid_timing = True
        last_idx, last_t = None, None
        for row in group:
            try:
                idx = int(row["frame_index"])
                if str(idx) != str(row["frame_index"]).strip() or idx < 0:
                    raise ValueError()
            except (ValueError, TypeError):
                valid_timing = False
                break
            t = finite(row["timestamp_ms"])
            if t is None or (last_idx is not None and
               (idx != last_idx+1 or not (t > last_t) or
                abs(t-last_t-FRAME_MS) > tolerance_ms)):
                valid_timing = False
                break
            last_idx, last_t = idx, t
        if not valid_timing:
            c["invalid_sequences"] += 1
            c["unresolved_frames"] += len(group)
            continue
        for row in group:
            a = finite(row["aperture_mm"])
            err = finite(row["aperture_error_mm"])
            ok = (a is not None and a >= 0 and err is not None and err >= 0
                  and all(flag(row[k]) is True for k in FLAGS))
            if ok and a + err < threshold_mm:
                c["image_subthreshold_candidates"] += 1
            else:
                c["unresolved_frames"] += 1
    return {
        "protocol": "E002-467-v1",
        "dataset_expected": "Eye-BCI video 150fps, not eye-tracker 300Hz",
        "split_algorithm": "sha256('lucent-e002-467-v1|'+subject); lowest 23 calibration",
        "calibration_subject_count": len(CALIBRATION),
        "holdout_subject_count": len(HOLDOUT),
        "threshold_mm": threshold_mm,
        "timestamp_tolerance_ms": tolerance_ms,
        "counts": counts,
        "physical_hidden_closure_exclusion": "ABSTAIN_UNCALIBRATED",
        "anatomical_negative_labels": 0,
        "physical_release_authorized": False,
        "note": "Candidates are image-derived only. Missing shutter, reference and velocity validation precludes physical claims."
    }

def run(path, threshold_mm, tolerance_ms=1.5):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(REQUIRED).issubset(reader.fieldnames):
            raise ValueError("CSV schema invalid")
        result = analyze(reader, threshold_mm, tolerance_ms)
    result["input_sha256"] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--threshold-mm", required=True, type=float)
    parser.add_argument("--tolerance-ms", type=float, default=1.5)
    args = parser.parse_args()
    print(json.dumps(run(args.csv, args.threshold_mm, args.tolerance_ms),
                     sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
