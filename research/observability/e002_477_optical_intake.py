"""E002-477: fail-closed intake QA for independently timed optical pulse scans.

Does not authenticate shutter support, hardware provenance, physiology, or product claims.
Only standard library; safe to run on locally stored non-human optical data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

SCHEMA = "lucent-e002-477-optical-intake-v1"
CAMERA_FIELDS = {"row_stratum", "phase_index", "repeat_index", "response", "dark_reference", "gain", "saturated", "dropped"}
CLOCK_FIELDS = {"row_stratum", "phase_index", "repeat_index", "pulse_start_ms", "pulse_end_ms"}
BLOCKED = {"physical_shutter_support_authenticated": False, "physical_release_authorized": False, "product_claim": "ABSTAIN_UNCALIBRATED"}

class IntakeError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def require(condition: bool, code: str, detail: str) -> None:
    if not condition:
        raise IntakeError(code, detail)


def finite_positive(x: Any, label: str, *, allow_zero: bool = False) -> float:
    try:
        value = float(x)
    except (ValueError, TypeError):
        raise IntakeError("NONFINITE_OR_INVALID", label)
    require(math.isfinite(value) and (value >= 0 if allow_zero else value > 0), "NONFINITE_OR_INVALID", label)
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path, expected_fields: set[str]) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames is not None and set(reader.fieldnames) == expected_fields, "CSV_SCHEMA", path.name)
            return list(reader)
    except UnicodeError as e:
        raise IntakeError("CSV_SCHEMA", "invalid UTF-8") from e


def validate(manifest_path: str | Path, camera_path: str | Path, clock_path: str | Path, raw_path: str | Path) -> dict[str, Any]:
    """Reject malformed acquisition; PASS means ingestion QA only, never shutter certification."""
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        require(isinstance(manifest, dict) and manifest.get("schema") == SCHEMA, "MANIFEST_SCHEMA", "schema")
        period = finite_positive(manifest.get("frame_period_ms"), "frame_period_ms")
        step = finite_positive(manifest.get("phase_step_ms"), "phase_step_ms")
        require(step <= 0.05 + 1e-12, "PHASE_GRID_TOO_COARSE", "phase step exceeds 0.05 ms")
        require(type(manifest.get("scan_periods")) is int and manifest["scan_periods"] >= 2, "MANIFEST_SCHEMA", "scan_periods")
        require(type(manifest.get("repeats_per_phase")) is int and manifest["repeats_per_phase"] >= 20, "MANIFEST_SCHEMA", "repeats_per_phase")
        rows = manifest.get("row_strata")
        require(isinstance(rows, list) and len(rows) >= 2 and all(isinstance(x, str) and x.strip() for x in rows) and len(set(rows)) == len(rows), "ROW_STRATA", "two distinct rows required")
        width = finite_positive(manifest.get("pulse_width_ms"), "pulse_width_ms")
        width_tol = finite_positive(manifest.get("pulse_width_tolerance_ms"), "pulse_width_tolerance_ms", allow_zero=True)
        require(width_tol <= 0.01, "PULSE_WIDTH", "pulse width tolerance too permissive")
        clock_error = finite_positive(manifest.get("clock_error_bound_ms"), "clock_error_bound_ms")
        require(clock_error < step, "CLOCK_UNRESOLVED", "clock error must be smaller than phase step")
        expected_gain = finite_positive(manifest.get("expected_gain"), "expected_gain")
        require(manifest.get("camera_gain_locked") is True, "GAIN_DRIFT", "gain lock required")
        require(manifest.get("clock_source_type") == "independent_photodiode_logic_analyzer", "CLOCK_NOT_INDEPENDENT", "independent clock source required")
        camera_id = manifest.get("camera_device_id")
        clock_id = manifest.get("clock_device_id")
        require(isinstance(camera_id, str) and isinstance(clock_id, str) and camera_id.strip() and clock_id.strip() and camera_id != clock_id, "CLOCK_NOT_INDEPENDENT", "distinct declared devices required")
        for name, path in [("camera_csv_sha256", camera_path), ("clock_csv_sha256", clock_path), ("raw_video_sha256", raw_path)]:
            value = manifest.get(name)
            require(isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value), "MANIFEST_SCHEMA", name)
            require(Path(path).is_file() and Path(path).stat().st_size > 0 and sha256_file(Path(path)) == value, "SHA_MISMATCH", name)
        cam = read_csv(Path(camera_path), CAMERA_FIELDS)
        clock = read_csv(Path(clock_path), CLOCK_FIELDS)
        phase_count = math.ceil(period * manifest["scan_periods"] / step - 1e-10) + 1
        require(phase_count <= 100000, "MANIFEST_SCHEMA", "phase grid too large")
        require(phase_count * len(rows) * manifest["repeats_per_phase"] <= 2000000, "MANIFEST_SCHEMA", "intake size exceeds bounded validation capacity")
        expected_keys = {(row, phase, repeat) for row in rows for phase in range(phase_count) for repeat in range(manifest["repeats_per_phase"])}
        require(len(cam) == len(expected_keys) and len(clock) == len(expected_keys), "GRID_INCOMPLETE", "expected phase/repeat/row count")
        cam_map: dict[tuple[str, int, int], dict[str, str]] = {}
        for record in cam:
            try:
                key = (record["row_stratum"], int(record["phase_index"]), int(record["repeat_index"]))
            except (ValueError, TypeError):
                raise IntakeError("CSV_SCHEMA", "camera key")
            require(key not in cam_map, "DUPLICATE_KEY", "duplicate camera key")
            cam_map[key] = record
            finite_positive(record["response"], "response", allow_zero=True)
            finite_positive(record["dark_reference"], "dark_reference", allow_zero=True)
            gain = finite_positive(record["gain"], "gain")
            require(abs(gain - expected_gain) <= 1e-9 * expected_gain, "GAIN_DRIFT", "gain changed")
            require(record["saturated"] == "0" and record["dropped"] == "0", "SENSOR_NUISANCE", "saturation or dropped frame")
        require(set(cam_map) == expected_keys, "GRID_INCOMPLETE", "camera phase/repeat/row coverage")
        clock_map: dict[tuple[str, int, int], dict[str, str]] = {}
        for record in clock:
            try:
                key = (record["row_stratum"], int(record["phase_index"]), int(record["repeat_index"]))
            except (ValueError, TypeError):
                raise IntakeError("CSV_SCHEMA", "clock key")
            require(key not in clock_map, "DUPLICATE_KEY", "duplicate clock key")
            clock_map[key] = record
            start = finite_positive(record["pulse_start_ms"], "pulse_start_ms", allow_zero=True)
            end = finite_positive(record["pulse_end_ms"], "pulse_end_ms")
            require(abs((end - start) - width) <= width_tol + 1e-12, "PULSE_WIDTH", "measured pulse width outside bound")
            require(abs(start - key[1] * step) <= clock_error + 1e-12, "CLOCK_PHASE", "independent measured phase outside bound")
        require(set(clock_map) == expected_keys, "GRID_INCOMPLETE", "clock phase/repeat/row coverage")
        summary = {}
        for row in rows:
            contrasts = [float(cam_map[k]["response"]) - float(cam_map[k]["dark_reference"]) for k in expected_keys if k[0] == row]
            positive = [(k[1] * step, max(0.0, float(cam_map[k]["response"]) - float(cam_map[k]["dark_reference"]))) for k in expected_keys if k[0] == row]
            total = sum(v for _, v in positive)
            centroid = round(sum(t * v for t, v in positive) / total, 9) if total > 0 else None
            summary[row] = {"observations": len(contrasts), "min_contrast": round(min(contrasts), 9), "max_contrast": round(max(contrasts), 9), "descriptive_contrast_phase_centroid_ms": centroid}
        return {"qa_status": "PASS_INTAKE_ONLY", "phase_count": phase_count, "observations": len(expected_keys), "row_summaries": summary, "hardware_independence_authenticated": False, **BLOCKED}
    except (OSError, json.JSONDecodeError, KeyError) as e:
        raise IntakeError("MISSING_OR_INVALID_SOURCE", str(e)) from e


def evaluate(*paths: str | Path) -> dict[str, Any]:
    try:
        return validate(*paths)
    except IntakeError as exc:
        return {"qa_status": "REJECT", "reason": exc.code, "hardware_independence_authenticated": False, **BLOCKED}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("camera_csv")
    parser.add_argument("independent_clock_csv")
    parser.add_argument("raw_video_bundle")
    args = parser.parse_args()
    result = evaluate(args.manifest, args.camera_csv, args.independent_clock_csv, args.raw_video_bundle)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["qa_status"] == "PASS_INTAKE_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
