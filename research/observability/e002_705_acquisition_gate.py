#!/usr/bin/env python3
"""E002-705: prospective acquisition-manifest gate; no human validation claim.

Usage: python e002_705_acquisition_gate.py manifest.json
Outputs one JSON verdict; exit 0 only for structurally admissible records.
This does not authenticate provenance or establish physiological velocity bounds.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{64}$")
REQUIRED = ("participant_pseudonym", "session_id", "device_model",
            "camera_firmware", "acquisition_clock_id", "high_rate_file_sha256",
            "low_rate_file_sha256", "exposure_start_interval",
            "exposure_end_interval", "roi_row", "frame_drop_count",
            "aperture_scale_interval", "aperture_error_interval",
            "speed_ceiling_source", "clock_error_interval",
            "shutter_gap_upper", "closure_threshold", "nuisance_tags")
FORBIDDEN = ("reference_status", "adjudication_status", "reference_labels",
             "high_rate_aperture", "ground_truth", "outcome", "label")


def interval(v, nonnegative=False):
    return (isinstance(v, list) and len(v) == 2
            and all(type(x) in (int, float) and x == x and abs(x) != float("inf")
                    for x in v)
            and v[0] <= v[1] and (not nonnegative or v[0] >= 0))


def check(row):
    errors = []
    if not isinstance(row, dict):
        return ["record_not_object"]
    for k in REQUIRED:
        if k not in row:
            errors.append("missing:" + k)
    for k in FORBIDDEN:
        if k in row:
            errors.append("reference_leakage:" + k)
    for k in ("high_rate_file_sha256", "low_rate_file_sha256"):
        if k in row and (not isinstance(row[k], str) or not SHA.fullmatch(row[k])):
            errors.append("bad_sha256:" + k)
    for k in ("exposure_start_interval", "exposure_end_interval",
              "aperture_scale_interval", "aperture_error_interval",
              "clock_error_interval"):
        if k in row and not interval(row[k], k in ("aperture_scale_interval",
                                                  "aperture_error_interval")):
            errors.append("bad_interval:" + k)
    if all(k in row and interval(row[k]) for k in
           ("exposure_start_interval", "exposure_end_interval")):
        if row["exposure_start_interval"][1] > row["exposure_end_interval"][0]:
            errors.append("ambiguous_exposure_order")
    for k in ("shutter_gap_upper", "closure_threshold"):
        if k in row and (type(row[k]) not in (int, float) or
                         not 0 <= row[k] < float("inf")):
            errors.append("bad_numeric:" + k)
    if "frame_drop_count" in row and (type(row["frame_drop_count"]) is not int
                                      or row["frame_drop_count"] < 0):
        errors.append("bad_frame_drop_count")
    if "nuisance_tags" in row and (not isinstance(row["nuisance_tags"], list)
                                  or not all(isinstance(x, str) for x in row["nuisance_tags"])):
        errors.append("bad_nuisance_tags")
    for k in ("participant_pseudonym", "session_id", "device_model",
              "camera_firmware", "acquisition_clock_id", "speed_ceiling_source"):
        if k in row and (not isinstance(row[k], str) or not row[k].strip()):
            errors.append("bad_identifier:" + k)
    return errors


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python e002_705_acquisition_gate.py manifest.json")
    raw = Path(sys.argv[1]).read_bytes()
    obj = json.loads(raw)
    records = obj.get("records") if isinstance(obj, dict) else None
    if not isinstance(records, list) or not records:
        errors = [{"record": None, "errors": ["missing_nonempty_records"]}]
    else:
        errors = [{"record": i, "errors": e} for i, row in enumerate(records)
                  if (e := check(row))]
        ids = [(r.get("participant_pseudonym"), r.get("session_id"))
               for r in records if isinstance(r, dict)]
        if len(ids) != len(set(ids)):
            errors.append({"record": None, "errors": ["duplicate_participant_session"]})
    result = {"schema": "E002-705-v1", "manifest_sha256": hashlib.sha256(raw).hexdigest(),
              "records": len(records) if isinstance(records, list) else 0,
              "verdict": "ABSTAIN_INVALID_MANIFEST" if errors else "STRUCTURE_ONLY_PASS",
              "errors": errors,
              "provenance_authenticated": False, "human_validation": False,
              "production_release": "BLOCKED"}
    print(json.dumps(result, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
