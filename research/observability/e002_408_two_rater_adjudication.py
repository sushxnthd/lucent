#!/usr/bin/env python3
"""E002-408: privacy-preserving two-rater E002-407 adjudication.

No human sheets are supplied by this repository. This tool never fabricates
ratings and never treats EEG synchronization as independent camera timing.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import statistics
from pathlib import Path

from e002_407_full_event_pilot import validate_manifest, validate_sheet, FLAGS
from e002_399_annotation_bridge import analyze as physical_analyze

def _read_rows(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return {(r["clip_id"], str(int(r["frame_in_clip"]))): r
                for r in csv.DictReader(handle)}

def _external_timing(document, manifest):
    if not isinstance(document, dict) or (
            document.get("clock_kind") != "independent_camera_hardware"
            or document.get("camera_clock_verified") is not True
            or len(str(document.get("provenance", "")).strip()) < 8
            or len(str(document.get("validity_domain", "")).strip()) < 8):
        raise ValueError("Independent camera-hardware clock evidence required; EEG timing prohibited")
    frames = document.get("frames")
    if not isinstance(frames, list):
        raise ValueError("Missing external camera frame timing")
    expected = {(c["clip_id"], str(f["frame_in_clip"]))
                for c in manifest["clips"] for f in c["frames"]}
    times = {}
    for item in frames:
        key = (item.get("clip_id"), str(item.get("frame_in_clip")))
        if key not in expected or key in times:
            raise ValueError("Duplicate or unexpected camera frame")
        vals = {}
        for field in ("nominal_time_s", "exposure_s", "clock_error_s"):
            try:
                v = float(item[field])
            except (KeyError, ValueError, TypeError) as exc:
                raise ValueError("Incomplete camera timing") from exc
            if not math.isfinite(v):
                raise ValueError("Nonfinite camera timing")
            vals[field] = v
        if vals["exposure_s"] <= 0 or vals["clock_error_s"] < 0:
            raise ValueError("Invalid camera exposure/clock uncertainty")
        times[key] = vals
    if set(times) != expected:
        raise ValueError("Missing independently timed frames")
    for clip in manifest["clips"]:
        seq = [times[(clip["clip_id"], str(f["frame_in_clip"]))]["nominal_time_s"]
               for f in clip["frames"]]
        if not all(b > a for a, b in zip(seq, seq[1:])):
            raise ValueError("Nonmonotone independent camera timing")
    return times

def adjudicate(manifest_path, sheet_a_path, sheet_b_path,
               external_timing_path=None, calibration_path=None):
    manifest_path, sheet_a_path, sheet_b_path = map(
        Path, (manifest_path, sheet_a_path, sheet_b_path))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    va = validate_sheet(manifest_path, sheet_a_path)
    vb = validate_sheet(manifest_path, sheet_b_path)
    if va["rater_id"] == vb["rater_id"]:
        raise ValueError("Independent rater IDs must differ")
    a, b = _read_rows(sheet_a_path), _read_rows(sheet_b_path)
    diffs = []
    excluded_nuisance = 0
    excluded_geometry = 0
    for clip in manifest["clips"]:
        for frame in clip["frames"]:
            key = (clip["clip_id"], str(frame["frame_in_clip"]))
            ra, rb = a[key], b[key]
            if any(ra[flag] == "1" or rb[flag] == "1" for flag in FLAGS):
                excluded_nuisance += 1
                continue
            gaps = []
            for row in (ra, rb):
                upper = float(row["center_upper_y"])
                lower = float(row["center_lower_y"])
                if lower < upper:
                    break
                gaps.append(lower - upper)
            if len(gaps) != 2:
                excluded_geometry += 1
                continue
            diffs.append(abs(gaps[0] - gaps[1]))
    total = manifest["frame_count"]
    assert len(diffs) + excluded_nuisance + excluded_geometry == total
    report = {
        "experiment": "E002-408",
        "evidence_tier": "two-rater annotation analysis; no physical truth without external review",
        "clips": manifest["clip_count"],
        "frames": total,
        "rater_count": 2,
        "usable_pairwise_frames": len(diffs),
        "excluded_nuisance_frames": excluded_nuisance,
        "excluded_inverted_geometry_frames": excluded_geometry,
        "median_abs_center_vertical_gap_disagreement_px":
            statistics.median(diffs) if diffs else None,
        "max_abs_center_vertical_gap_disagreement_px":
            max(diffs) if diffs else None,
        "physical_timing_provenance_authenticated": False,
        "physical_velocity_provenance_authenticated": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "decisions": {"ABSTAIN_UNCALIBRATED": manifest["clip_count"]},
        "warning": "Pixel-gap rater agreement is not physical aperture truth. "
                   "Calibration claims are never authenticated by this script."
    }
    if external_timing_path is None or calibration_path is None:
        return report
    timing_doc = json.loads(Path(external_timing_path).read_text(encoding="utf-8"))
    timing = _external_timing(timing_doc, manifest)
    cfg = json.loads(Path(calibration_path).read_text(encoding="utf-8"))
    # Reuse the complete existing optical/rolling-shutter/geometry/kernel/
    # hard-velocity gates. Adapt only the blinded manifest version marker.
    adapted = dict(manifest)
    adapted["experiment"] = "E002-398"
    try:
        result = physical_analyze(adapted, a, b, timing, cfg)
    except (KeyError, TypeError, ValueError):
        report["warning"] += " Incomplete/invalid physical calibration; abstaining."
        return report
    report["decisions"] = result["decisions"]
    report["physical_calibration_gates_asserted"] = result["calibration_gates_passed"]
    report["hard_velocity_gate_asserted"] = result["hard_velocity_bound_gate"]
    report["warning"] += (" Any non-abstaining decision is conditional on externally "
                          "verified calibration; the provided strings/booleans are NOT proof.")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--rater-a", type=Path, required=True)
    p.add_argument("--rater-b", type=Path, required=True)
    p.add_argument("--external-camera-timing", type=Path)
    p.add_argument("--physical-calibration", type=Path)
    args = p.parse_args()
    result = adjudicate(args.manifest, args.rater_a, args.rater_b,
                        args.external_camera_timing, args.physical_calibration)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
