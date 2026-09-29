"""Run the complete offline E002 processing stack for one capture.

Usage:
    python instrument/process_capture.py capture.webm capture.json

Outputs beside the input files:
    <stem>.quality.json
    <stem>.pupil.json
    <stem>.trace.csv

Dependencies:
    pip install opencv-python-headless mediapipe
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite derived outputs if they already exist",
    )
    args = parser.parse_args()

    meta = json.loads(args.metadata.read_text(encoding="utf-8"))
    if meta.get("schemaVersion") != "lucent-e002-capture-v1":
        raise RuntimeError("Metadata is not a Lucent E002 capture sidecar.")

    stem = meta.get("captureFileStem")
    if not stem:
        raise RuntimeError("Capture metadata is missing captureFileStem.")

    if args.metadata.stem != stem:
        raise RuntimeError(
            f"Metadata filename stem {args.metadata.stem!r} "
            f"does not match frozen captureFileStem {stem!r}."
        )

    if args.video.stem != stem:
        raise RuntimeError(
            f"Video filename stem {args.video.stem!r} "
            f"does not match frozen captureFileStem {stem!r}."
        )

    root = Path(__file__).resolve().parent
    out_dir = args.metadata.parent

    quality = out_dir / f"{stem}.quality.json"
    pupil = out_dir / f"{stem}.pupil.json"
    trace = out_dir / f"{stem}.trace.csv"

    for path in (quality, pupil, trace):
        if path.exists() and not args.force:
            raise RuntimeError(
                f"{path.name} already exists; use --force to regenerate."
            )

    subprocess.run(
        [
            sys.executable,
            str(root / "analyze_capture.py"),
            str(args.video),
            str(args.metadata),
            "--output",
            str(quality),
        ],
        check=True,
    )

    subprocess.run(
        [
            sys.executable,
            str(root / "extract_pupil_dynamics.py"),
            str(args.video),
            str(args.metadata),
            "--output",
            str(pupil),
            "--trace-output",
            str(trace),
        ],
        check=True,
    )

    result = {
        "captureFileStem": stem,
        "condition": meta.get("condition"),
        "pilotCaptureNumber": meta.get("pilotCaptureNumber"),
        "technicalRetry": meta.get("technicalRetry"),
        "quality": quality.name,
        "pupil": pupil.name,
        "trace": trace.name,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
