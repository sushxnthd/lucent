"""Offline quality gate for Lucent E002 captures.

Usage:
    pip install opencv-python-headless
    python instrument/analyze_capture.py capture.webm capture.json --output quality.json

This script measures capture quality. It does not estimate fatigue.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def load_cascade(name: str):
    path = Path(cv2.data.haarcascades) / name
    cascade = cv2.CascadeClassifier(str(path))
    if cascade.empty():
        raise RuntimeError(f"Could not load OpenCV cascade: {path}")
    return cascade


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stride", type=int, default=1)
    args = parser.parse_args()

    meta = json.loads(args.metadata.read_text(encoding="utf-8"))

    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {args.video}")

    face_cascade = load_cascade("haarcascade_frontalface_default.xml")
    eye_cascade = load_cascade("haarcascade_eye_tree_eyeglasses.xml")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)

    rows = []
    frame_index = -1

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame_index += 1
        if frame_index % max(args.stride, 1):
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(max(40, width // 12), max(40, height // 12)),
        )

        detected = len(faces) > 0
        eye_count = 0
        area_fraction = 0.0
        centeredness = 0.0

        if detected:
            x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
            area_fraction = float((w * h) / max(width * height, 1))
            cx = (x + w / 2) / max(width, 1)
            cy = (y + h / 2) / max(height, 1)
            distance = float(np.hypot(cx - 0.5, cy - 0.5))
            centeredness = max(0.0, 1.0 - distance)

            roi = gray[y : y + max(1, int(h * 0.62)), x : x + w]
            eyes = eye_cascade.detectMultiScale(
                roi,
                scaleFactor=1.08,
                minNeighbors=4,
                minSize=(max(12, w // 12), max(8, h // 16)),
            )
            eye_count = int(len(eyes))

        face_component = min(1.0, area_fraction / 0.12) if detected else 0.0
        eye_component = min(1.0, eye_count / 2.0)
        sharp_component = min(1.0, sharpness / 180.0)

        quality = (
            0.35 * face_component
            + 0.30 * eye_component
            + 0.20 * centeredness
            + 0.15 * sharp_component
        )

        rows.append(
            {
                "frame": frame_index,
                "timeS": frame_index / fps if fps > 0 else None,
                "faceDetected": bool(detected),
                "eyeDetections": eye_count,
                "faceAreaFraction": area_fraction,
                "centeredness": centeredness,
                "sharpness": sharpness,
                "quality": float(quality),
            }
        )

    cap.release()

    qualities = np.asarray([row["quality"] for row in rows], dtype=float)
    face_rate = (
        float(np.mean([row["faceDetected"] for row in rows])) if rows else 0.0
    )
    two_eye_rate = (
        float(np.mean([row["eyeDetections"] >= 2 for row in rows]))
        if rows
        else 0.0
    )

    events = meta.get("stimulusEvents", [])
    timing_errors = [
        abs(float(event["actualOffsetMs"]) - float(event["scheduledOffsetMs"]))
        for event in events
    ]

    summary = {
        "schemaVersion": "lucent-e002-quality-v1",
        "sourceVideo": args.video.name,
        "sourceMetadata": args.metadata.name,
        "video": {
            "fpsReported": fps,
            "width": width,
            "height": height,
            "sampledFrames": len(rows),
        },
        "timing": {
            "maxStimulusSchedulingErrorMs": (
                max(timing_errors) if timing_errors else None
            ),
            "meanStimulusSchedulingErrorMs": (
                float(np.mean(timing_errors)) if timing_errors else None
            ),
            "browserFrameCadence": meta.get("frameCadence"),
        },
        "quality": {
            "faceDetectionRate": face_rate,
            "twoEyeDetectionRate": two_eye_rate,
            "medianQuality": (
                float(np.median(qualities)) if len(qualities) else 0.0
            ),
            "p10Quality": (
                float(np.quantile(qualities, 0.10)) if len(qualities) else 0.0
            ),
        },
        "frames": rows,
        "interpretation": (
            "Capture-quality diagnostics only. No biological state or fatigue "
            "estimate is produced."
        ),
    }

    args.output.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary["quality"], indent=2))
    print(json.dumps(summary["timing"], indent=2))


if __name__ == "__main__":
    main()
