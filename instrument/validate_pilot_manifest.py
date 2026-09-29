"""Validate an E002 nine-capture pilot directory before aggregate analysis.

The validator reads only Lucent capture-sidecar JSON files and protocol.json.
It does not inspect biological outcomes.

Usage:
    python instrument/validate_pilot_manifest.py path/to/captures \
        --output pilot_manifest.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


CAPTURE_SCHEMA = "lucent-e002-capture-v1"


def parse_iso(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def capture_sidecars(directory: Path):
    rows = []
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("schemaVersion") == CAPTURE_SCHEMA:
            rows.append((path, data))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    protocol_path = Path(__file__).resolve().parent / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    order = list(protocol["pilot"]["capture_order"])
    expected = {i + 1: condition for i, condition in enumerate(order)}

    rows = capture_sidecars(args.directory)
    errors = []
    warnings = []

    if not rows:
        errors.append("No Lucent E002 capture sidecars found.")

    records = []
    for path, meta in rows:
        number = meta.get("pilotCaptureNumber")
        retry = bool(meta.get("technicalRetry", False))
        condition = meta.get("condition")
        planned = meta.get("plannedCondition")
        stem = meta.get("captureFileStem")
        started = parse_iso(meta.get("startedAtIso"))

        if not isinstance(number, int) or number not in expected:
            errors.append(f"{path.name}: invalid pilotCaptureNumber={number!r}")
        else:
            if condition != expected[number]:
                errors.append(
                    f"{path.name}: condition {condition!r} does not match "
                    f"frozen order {expected[number]!r}"
                )

        if planned != condition:
            errors.append(
                f"{path.name}: plannedCondition {planned!r} "
                f"does not match condition {condition!r}"
            )

        if not stem or path.stem != stem:
            errors.append(
                f"{path.name}: filename stem does not match captureFileStem."
            )

        if started is None:
            errors.append(f"{path.name}: invalid/missing startedAtIso.")

        records.append(
            {
                "path": path.name,
                "captureNumber": number,
                "condition": condition,
                "retry": retry,
                "startedAtIso": meta.get("startedAtIso"),
                "participant": meta.get("participantPseudonym"),
                "session": meta.get("session"),
                "protocolVersion": meta.get("protocolVersion"),
                "brightness": (meta.get("userInputs") or {}).get(
                    "screenBrightnessPercent"
                ),
                "ambient": (meta.get("userInputs") or {}).get(
                    "ambientCategory"
                ),
                "distanceCm": (meta.get("userInputs") or {}).get(
                    "approximateDistanceCm"
                ),
                "cameraLabel": (meta.get("camera") or {}).get("label"),
                "_started": started,
            }
        )

    primaries = [record for record in records if not record["retry"]]
    retries = [record for record in records if record["retry"]]

    counts = Counter(record["captureNumber"] for record in primaries)
    for number in range(1, len(order) + 1):
        count = counts[number]
        if count == 0:
            errors.append(f"Missing primary capture {number}.")
        elif count > 1:
            errors.append(
                f"Capture {number} has {count} primary attempts; "
                "extra attempts must be marked technicalRetry=true."
            )

    if len(primaries) != len(order):
        errors.append(
            f"Expected {len(order)} primary captures; found {len(primaries)}."
        )

    primary_order = sorted(
        [record for record in primaries if record["_started"] is not None],
        key=lambda record: record["_started"],
    )
    chronological_numbers = [
        record["captureNumber"]
        for record in primary_order
    ]
    expected_numbers = list(range(1, len(order) + 1))
    if (
        len(primary_order) == len(order)
        and chronological_numbers != expected_numbers
    ):
        errors.append(
            "Primary captures were not collected in frozen chronological "
            f"order 1..{len(order)}: observed {chronological_numbers}."
        )

    def unique_non_null(field):
        return {
            record[field]
            for record in primaries
            if record.get(field) is not None
        }

    for field, label in [
        ("participant", "participant pseudonym"),
        ("session", "session"),
        ("protocolVersion", "protocol version"),
        ("brightness", "screen brightness"),
        ("ambient", "ambient category"),
        ("cameraLabel", "camera label"),
    ]:
        values = unique_non_null(field)
        if len(values) > 1:
            errors.append(
                f"Primary captures use multiple {label} values: "
                f"{sorted(map(str, values))}"
            )

    distances = [
        float(record["distanceCm"])
        for record in primaries
        if record.get("distanceCm") is not None
    ]
    if distances and max(distances) - min(distances) > 5.0:
        warnings.append(
            "Reported phone distance varies by more than 5 cm "
            f"({min(distances):.1f}..{max(distances):.1f})."
        )

    retry_counts = Counter(record["captureNumber"] for record in retries)
    for number, count in sorted(retry_counts.items()):
        if number not in expected:
            continue
        warnings.append(
            f"Capture {number} has {count} technical retry record(s). "
            "Confirm replacement is permitted by the frozen exclusion rule."
        )

    public_records = []
    for record in records:
        clean = dict(record)
        clean.pop("_started", None)
        public_records.append(clean)

    report = {
        "schemaVersion": "lucent-e002-manifest-v1",
        "directory": str(args.directory),
        "frozenOrder": order,
        "primaryCaptureCount": len(primaries),
        "retryCount": len(retries),
        "errors": errors,
        "warnings": warnings,
        "readyForOfflineAnalysis": len(errors) == 0,
        "records": public_records,
    }

    args.output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))

    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
