#!/usr/bin/env python3
"""E002-398: construct *local-only* blinded eyelid landmark annotation frames.

EEG event/control linkage and source timebase remain PRIVATE. No physical aperture
ground truth or independent camera exposure calibration is claimed.
"""
import argparse
import csv
import hashlib
import hmac
import io
import json
import os
from pathlib import Path
import secrets
import tempfile
import zipfile

import cv2
import numpy as np

import e002_397_human_motion as prior

N_PAIRS = 20
CROP = (70, 260, 90, 220)  # x0, x1, y0, y1
SECRET_CONTEXT = b"lucent-e002-398-blind-v2"


def selected_pairs(pairs):
    n = len(pairs)
    if n < N_PAIRS:
        raise ValueError("Insufficient eligible event/control pairs")
    indices = [int((i + .5) * n / N_PAIRS) for i in range(N_PAIRS)]
    if len(set(indices)) != N_PAIRS:
        raise AssertionError("Nonunique deterministic pair selection")
    return [(idx, pairs[idx]) for idx in indices]


def image_metrics(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return {
        "laplacian_variance": round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 6),
        "saturation_fraction": round(float(np.mean((gray == 0) | (gray == 255))), 8),
        "contrast_p95_minus_p05": round(float(np.percentile(gray, 95) - np.percentile(gray, 5)), 6),
    }


def run(archive, person, public_dir, private_dir):
    if prior.prior.md5(archive) != prior.MD5[person]:
        raise RuntimeError("Source MD5 mismatch")
    public_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)
    key = secrets.token_bytes(32)
    with zipfile.ZipFile(archive) as z:
        video, frames, markers = prior.load_archive(z, person)
        pairs, rejected = prior.select_pairs(frames, markers, person)
        selected = selected_pairs(pairs)
        clips = {}
        mapping = {}
        needed = {}
        for index, (k, j) in selected:
            for arm, center in (("marker", k), ("control", j)):
                message = f"{person}:{index}:{arm}".encode()
                clip_id = hmac.new(key, SECRET_CONTEXT + message, hashlib.sha256).hexdigest()[:20]
                if clip_id in clips:
                    raise RuntimeError("Blind ID collision")
                clips[clip_id] = {}
                mapping[clip_id] = {
                    "participant": person, "source_archive_md5": prior.MD5[person],
                    "pair_index": index, "arm": arm,
                    "center_frame_index": center,
                    "center_phantom_frame_id": frames[center][0],
                    "center_eeg_clock_time": frames[center][1]}
                for rel in range(-3, 4):
                    needed.setdefault(center + rel, []).append((clip_id, rel + 3))
        if len(clips) != 40:
            raise AssertionError("Expected 40 blinded clips")
        with tempfile.TemporaryDirectory() as tmp:
            avi = Path(tmp) / "eye.avi"
            with z.open(video) as src, avi.open("wb") as dst:
                for chunk in iter(lambda: src.read(1 << 20), b""):
                    dst.write(chunk)
            cap = cv2.VideoCapture(str(avi))
            if not cap.isOpened():
                raise RuntimeError("Cannot decode Phantom video")
            if int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != len(frames):
                raise RuntimeError("Frame-count mismatch")
            count = 0
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                if count in needed:
                    if frame.shape[:2] != (288, 320):
                        raise RuntimeError("Unexpected frame dimensions")
                    crop = frame[CROP[2]:CROP[3], CROP[0]:CROP[1]]
                    for clip_id, rel in needed[count]:
                        name = f"{clip_id}_{rel:02d}.png"
                        path = private_dir / name
                        if not cv2.imwrite(str(path), crop):
                            raise RuntimeError("Cannot write crop")
                        clips[clip_id][rel] = {
                            "frame_in_clip": rel,
                            "file": name,
                            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            **image_metrics(crop)}
                count += 1
            cap.release()
            if count != len(frames):
                raise RuntimeError("Incomplete source video decode")
    if any(len(v) != 7 for v in clips.values()):
        raise RuntimeError("Missing frame in annotation clip")
    # Sort by HMAC, not source time, arm, or pair order.
    public_clips = [
        {"clip_id": clip_id, "frames": [clips[clip_id][q] for q in range(7)]}
        for clip_id in sorted(clips)]
    public = {
        "experiment": "E002-398",
        "evidence_tier": "previously inspected human video; annotation packet only",
        "crop_width": 190, "crop_height": 130,
        "clip_count": len(public_clips),
        "frame_count": sum(len(c["frames"]) for c in public_clips),
        "public_linkage_present": False,
        "physical_aperture_validated": False,
        "camera_exposure_independently_calibrated": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "clips": public_clips}
    (public_dir / "blinded_manifest.json").write_text(json.dumps(public, indent=2))
    with (public_dir / "blank_annotation_sheet.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["clip_id", "frame_in_clip",
                         "left_upper_x", "left_upper_y", "left_lower_x", "left_lower_y",
                         "center_upper_x", "center_upper_y", "center_lower_x", "center_lower_y",
                         "right_upper_x", "right_upper_y", "right_lower_x", "right_lower_y",
                         "occlusion", "glare", "glasses", "blur", "gaze_issue",
                         "unresolved", "rater_id", "notes"])
        for clip in public_clips:
            for frame in clip["frames"]:
                writer.writerow([clip["clip_id"], frame["frame_in_clip"]] + [""] * 20)
    (private_dir / "PRIVATE_DO_NOT_UPLOAD_linkage.json").write_text(json.dumps({
        "warning": "PRIVATE EVENT/CONTROL KEY. NEVER UPLOAD TO PUBLIC REPOSITORY OR CI ARTIFACT.",
        "key_hex": key.hex(), "source_md5": prior.MD5[person],
        "source_video": video, "eligible_pairs": len(pairs),
        "pair_rejections": rejected, "linkage": mapping}, indent=2))
    # Only descriptive, non-label data go to CI.
    vals = [frame for c in public_clips for frame in c["frames"]]
    summary = {
        "experiment": "E002-398", "participant": person,
        "source_md5_verified": True, "eligible_pairs": len(pairs),
        "selected_pairs": N_PAIRS, "blinded_clips": len(clips),
        "cropped_frames": len(vals), "private_linkage_not_published": True,
        "laplacian_variance_p10_p50_p90": np.percentile(
            [v["laplacian_variance"] for v in vals], [10, 50, 90]).tolist(),
        "saturation_fraction_p10_p50_p90": np.percentile(
            [v["saturation_fraction"] for v in vals], [10, 50, 90]).tolist(),
        "contrast_p95_p05_p10_p50_p90": np.percentile(
            [v["contrast_p95_minus_p05"] for v in vals], [10, 50, 90]).tolist(),
        "actual_aperture_annotations": 0, "release_decision": "ABSTAIN_UNCALIBRATED"}
    (public_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archive", type=Path, required=True)
    p.add_argument("--participant", choices=["S01", "S19"], required=True)
    p.add_argument("--public-dir", type=Path, required=True)
    p.add_argument("--private-dir", type=Path, required=True)
    args = p.parse_args()
    if args.private_dir.resolve() == args.public_dir.resolve():
        raise ValueError("Public and private directories must differ")
    run(args.archive, args.participant, args.public_dir, args.private_dir)


if __name__ == "__main__":
    main()
