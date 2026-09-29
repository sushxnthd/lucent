"""Extract visible-light pupil dynamics from a Lucent E002 capture.

This is a research-quality heuristic, not a medical measurement pipeline.

Dependencies:
    pip install opencv-python-headless mediapipe

The algorithm uses MediaPipe refined face landmarks to locate the iris, then
segments the darkest compact region near the iris center and reports pupil
diameter normalized by iris diameter. Confidence is based on geometry,
circularity, center proximity, and local contrast.

Always inspect traces and quality scores before using them in an experiment.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np
import mediapipe as mp


RIGHT_IRIS_CENTER = 468
RIGHT_IRIS_BORDER = (469, 470, 471, 472)
LEFT_IRIS_CENTER = 473
LEFT_IRIS_BORDER = (474, 475, 476, 477)


def point(landmarks, index: int, width: int, height: int) -> np.ndarray:
    lm = landmarks[index]
    return np.array([lm.x * width, lm.y * height], dtype=float)


def nearest_video_callback(meta: dict, media_time_s: float):
    frames = meta.get("videoFrames") or []
    candidates = [
        frame
        for frame in frames
        if frame.get("mediaTimeS") is not None
        and frame.get("callbackNowMs") is not None
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda frame: abs(float(frame["mediaTimeS"]) - media_time_s),
    )


def stimulus_state(meta: dict, offset_ms: float):
    events = meta.get("stimulusEvents") or []
    active = None
    for event in events:
        if float(event.get("actualOffsetMs", 0.0)) <= offset_ms:
            active = event
        else:
            break
    if active is None:
        return None, None
    return int(active["segment"]), bool(active["high"])


def estimate_pupil(
    gray: np.ndarray,
    landmarks,
    center_index: int,
    border_indices: tuple[int, ...],
):
    height, width = gray.shape[:2]
    center = point(landmarks, center_index, width, height)
    border = np.stack(
        [point(landmarks, i, width, height) for i in border_indices],
        axis=0,
    )

    iris_radius = float(
        np.median(np.linalg.norm(border - center.reshape(1, 2), axis=1))
    )
    if not np.isfinite(iris_radius) or iris_radius < 3.0:
        return None

    crop_radius = max(5, int(round(1.15 * iris_radius)))
    cx, cy = map(int, np.round(center))

    x0 = max(0, cx - crop_radius)
    x1 = min(width, cx + crop_radius + 1)
    y0 = max(0, cy - crop_radius)
    y1 = min(height, cy + crop_radius + 1)

    crop = gray[y0:y1, x0:x1]
    if crop.size < 100:
        return None

    local_center = np.array([center[0] - x0, center[1] - y0], dtype=float)

    yy, xx = np.mgrid[: crop.shape[0], : crop.shape[1]]
    iris_mask = (
        (xx - local_center[0]) ** 2
        + (yy - local_center[1]) ** 2
        <= (0.92 * iris_radius) ** 2
    )

    values = crop[iris_mask]
    if values.size < 30:
        return None

    # Dark-pupil candidate. The percentile threshold is deliberately simple
    # and is quality-gated rather than assumed correct.
    threshold = float(np.quantile(values, 0.28))
    binary = np.zeros_like(crop, dtype=np.uint8)
    binary[(crop <= threshold) & iris_mask] = 255

    kernel = np.ones((3, 3), dtype=np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    iris_area = np.pi * iris_radius**2
    best = None

    for contour in contours:
        area = float(cv2.contourArea(contour))
        if area <= 0:
            continue

        area_fraction = area / iris_area
        if area_fraction < 0.03 or area_fraction > 0.80:
            continue

        moments = cv2.moments(contour)
        if abs(moments["m00"]) < 1e-9:
            continue

        px = moments["m10"] / moments["m00"]
        py = moments["m01"] / moments["m00"]
        center_distance = float(
            np.linalg.norm(
                np.array([px, py], dtype=float) - local_center
            )
        ) / iris_radius

        if center_distance > 0.65:
            continue

        perimeter = float(cv2.arcLength(contour, True))
        circularity = (
            4.0 * np.pi * area / (perimeter**2)
            if perimeter > 0
            else 0.0
        )
        circularity = float(np.clip(circularity, 0.0, 1.0))

        mask = np.zeros_like(crop, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=-1)
        pupil_pixels = crop[mask > 0]

        surround_mask = iris_mask & (mask == 0)
        surround_pixels = crop[surround_mask]

        if pupil_pixels.size < 10 or surround_pixels.size < 10:
            continue

        contrast = (
            float(np.median(surround_pixels))
            - float(np.median(pupil_pixels))
        ) / 255.0
        contrast = float(np.clip(contrast / 0.18, 0.0, 1.0))

        center_score = float(np.clip(1.0 - center_distance / 0.65, 0.0, 1.0))
        quality = 0.45 * contrast + 0.30 * circularity + 0.25 * center_score

        equivalent_diameter = 2.0 * np.sqrt(area / np.pi)
        pupil_to_iris = equivalent_diameter / (2.0 * iris_radius)

        candidate = {
            "ratio": float(pupil_to_iris),
            "quality": float(quality),
            "irisRadiusPx": iris_radius,
            "centerDistance": center_distance,
            "circularity": circularity,
            "contrastScore": contrast,
        }

        if best is None or candidate["quality"] > best["quality"]:
            best = candidate

    return best


def summarize(trace: list[dict], meta: dict):
    ratios = np.asarray(
        [
            row["pupilRatio"]
            for row in trace
            if row["pupilRatio"] is not None
            and row["quality"] is not None
            and row["quality"] >= 0.45
        ],
        dtype=float,
    )

    valid_rate = (
        len(ratios) / len(trace)
        if trace
        else 0.0
    )

    result = {
        "framesAnalyzed": len(trace),
        "validPupilFrames": int(len(ratios)),
        "validPupilRate": float(valid_rate),
        "medianPupilToIris": (
            float(np.median(ratios)) if len(ratios) else None
        ),
        "condition": meta.get("condition"),
    }

    first_high = None
    for event in meta.get("stimulusEvents", []):
        if event.get("high"):
            first_high = float(event["actualOffsetMs"]) / 1000.0
            break

    if first_high is None:
        result["dynamicResponse"] = None
        return result

    good = [
        row
        for row in trace
        if row["pupilRatio"] is not None
        and row["quality"] is not None
        and row["quality"] >= 0.45
    ]

    pre = np.asarray(
        [
            row["pupilRatio"]
            for row in good
            if 0.05 <= row["offsetS"] <= max(0.10, first_high - 0.05)
        ],
        dtype=float,
    )

    post = [
        row
        for row in good
        if first_high <= row["offsetS"] <= first_high + 1.6
    ]

    if len(pre) < 3 or len(post) < 3:
        result["dynamicResponse"] = None
        return result

    baseline = float(np.median(pre))
    minimum_row = min(post, key=lambda row: row["pupilRatio"])
    minimum = float(minimum_row["pupilRatio"])

    result["dynamicResponse"] = {
        "baselineRatio": baseline,
        "minimumRatio": minimum,
        "constrictionAmplitude": baseline - minimum,
        "timeToMinimumS": float(minimum_row["offsetS"] - first_high),
    }

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace-output", type=Path)
    args = parser.parse_args()

    meta = json.loads(args.metadata.read_text(encoding="utf-8"))

    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {args.video}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)

    mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    trace = []
    frame_index = -1

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame_index += 1
        media_time_s = frame_index / fps if fps > 0 else 0.0
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = mesh.process(rgb_frame)

        callback = nearest_video_callback(meta, media_time_s)
        if callback is not None:
            offset_s = (
                float(callback["callbackNowMs"])
                - float(meta.get("captureStartNowMs", 0.0))
            ) / 1000.0
        else:
            offset_s = media_time_s

        segment, high = stimulus_state(meta, offset_s * 1000.0)

        row = {
            "frame": frame_index,
            "mediaTimeS": media_time_s,
            "offsetS": offset_s,
            "segment": segment,
            "high": high,
            "leftRatio": None,
            "rightRatio": None,
            "pupilRatio": None,
            "quality": None,
        }

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark
            if len(landmarks) >= 478:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                right = estimate_pupil(
                    gray,
                    landmarks,
                    RIGHT_IRIS_CENTER,
                    RIGHT_IRIS_BORDER,
                )
                left = estimate_pupil(
                    gray,
                    landmarks,
                    LEFT_IRIS_CENTER,
                    LEFT_IRIS_BORDER,
                )

                estimates = [
                    item
                    for item in (left, right)
                    if item is not None and item["quality"] >= 0.25
                ]

                if left is not None:
                    row["leftRatio"] = left["ratio"]
                if right is not None:
                    row["rightRatio"] = right["ratio"]

                if estimates:
                    weights = np.asarray(
                        [item["quality"] for item in estimates],
                        dtype=float,
                    )
                    values = np.asarray(
                        [item["ratio"] for item in estimates],
                        dtype=float,
                    )
                    row["pupilRatio"] = float(
                        np.average(values, weights=np.maximum(weights, 1e-3))
                    )
                    row["quality"] = float(np.mean(weights))

        trace.append(row)

    cap.release()
    mesh.close()

    stimulus_errors = [
        abs(float(event.get("actualOffsetMs", 0.0)) - float(event.get("scheduledOffsetMs", 0.0)))
        for event in meta.get("stimulusEvents", [])
    ]

    summary = {
        "schemaVersion": "lucent-e002-pupil-v1",
        "participantPseudonym": meta.get("participantPseudonym"),
        "session": meta.get("session"),
        "condition": meta.get("condition"),
        "protocolVersion": meta.get("protocolVersion"),
        "video": {
            "fpsReported": fps,
            "width": width,
            "height": height,
        },
        "summary": summarize(trace, meta),
        "captureTiming": {
            "actualDurationMs": meta.get("actualDurationMs"),
            "maxStimulusSchedulingErrorMs": max(stimulus_errors) if stimulus_errors else None,
            "frameCadence": meta.get("frameCadence"),
        },
        "warning": (
            "Visible-light pupil segmentation is heuristic and must be "
            "quality-checked. This output is not a clinical measurement."
        ),
    }

    args.output.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    if args.trace_output:
        fields = list(trace[0].keys()) if trace else []
        with args.trace_output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(trace)

    print(json.dumps(summary["summary"], indent=2))


if __name__ == "__main__":
    main()
