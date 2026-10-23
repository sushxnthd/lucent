#!/usr/bin/env python3
"""E002-397: frozen cross-participant motion proxy test. EEG labels != physical aperture."""
import argparse
import bisect
import json
import pathlib
import tempfile
import zipfile

import cv2
import numpy as np

import e002_395_human_proxy as prior
import e002_396_unseen_s19 as s19

MD5 = {"S01": "fef02cb7ebf62e4f3efb6303284fd6cb",
       "S19": "8a16cf12526f7558b4e49926c4bc5e8e"}
VARIANTS = ("clean", "gain_070", "gain_130", "blur_sigma2",
            "translation_8_6", "glare")


def load_archive(z, person):
    if person == "S01":
        frames, markers = prior.load_sync(z)
        videos = sorted(n for n in z.namelist()
                        if n.lower().endswith("_phantom.avi"))
        if len(videos) != 1:
            raise RuntimeError("S01 must have one paired Phantom video")
        return videos[0], frames, markers
    _, video, frames, markers = s19.load(z)
    return video, frames, markers


def select_pairs(frames, markers, person):
    times = [t for _, t in frames]
    ids = [fid for fid, _ in frames]
    def near(t):
        k = bisect.bisect_left(times, t)
        candidates = [q for q in (k - 1, k)
                      if 4 <= q < len(times) - 4]
        if not candidates:
            return None
        k = min(candidates, key=lambda q: abs(times[q] - t))
        if abs(times[k] - t) > .0100001:
            return None
        if any(times[q+1] - times[q] > .0200001
               for q in range(k-4, k+3)):
            return None
        return k
    pairs = []
    rejected = {"gap_or_missing": 0, "previously_inspected": 0,
                "no_control": 0}
    for t in markers:
        k = near(t)
        if k is None:
            rejected["gap_or_missing"] += 1
            continue
        if person == "S01" and ids[k] in prior.EXCLUDED:
            rejected["previously_inspected"] += 1
            continue
        control = None
        for offset in prior.OFFSETS:
            candidate = t + offset
            if min(abs(candidate - m) for m in markers) < .35:
                continue
            j = near(candidate)
            if j is not None and abs(j - k) > 6:
                control = j
                break
        if control is None:
            rejected["no_control"] += 1
            continue
        pairs.append((k, control))
    if len(pairs) < (50 if person == "S01" else 15):
        raise RuntimeError("Too few marker/control pairs")
    return pairs, rejected


def motion_score(prev, current):
    flow = cv2.calcOpticalFlowFarneback(
        prev, current, None, .5, 3, 15, 3, 5, 1.2, 0)
    if flow.shape[:2] != (288, 320):
        raise RuntimeError("Unexpected camera geometry")
    background = np.concatenate((
        flow[20:100, 30:290].reshape(-1, 2),
        flow[200:270, 30:290].reshape(-1, 2)), axis=0)
    global_motion = np.median(background, axis=0)
    residual = flow[118:190, 100:230] - global_motion
    magnitude = np.hypot(residual[..., 0], residual[..., 1])
    return float(np.percentile(magnitude, 80))


def evaluate(archive, person):
    if prior.md5(archive) != MD5[person]:
        raise RuntimeError("Source MD5 mismatch")
    with zipfile.ZipFile(archive) as z:
        video, frames, markers = load_archive(z, person)
        pairs, rejected = select_pairs(frames, markers, person)
        needed = set()
        for k, j in pairs:
            needed.update(range(k-3, k+4))
            needed.update(range(j-3, j+4))
        with tempfile.TemporaryDirectory() as tmp:
            local = pathlib.Path(tmp) / "eye.avi"
            with z.open(video) as src, local.open("wb") as dst:
                for chunk in iter(lambda: src.read(1 << 20), b""):
                    dst.write(chunk)
            cap = cv2.VideoCapture(str(local))
            if not cap.isOpened():
                raise RuntimeError("Cannot open video")
            declared = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if declared != len(frames):
                raise RuntimeError("Video/EEG frame-count disagreement")
            scores = {}
            previous = None
            i = 0
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                if i in needed:
                    if previous is None:
                        raise RuntimeError("Missing previous frame")
                    gray0 = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
                    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    scores[i] = {
                        v: motion_score(prior.transform(gray0, v),
                                        prior.transform(gray1, v))
                        for v in VARIANTS}
                previous = frame
                i += 1
            cap.release()
            if i != len(frames) or len(scores) != len(needed):
                raise RuntimeError("Incomplete video/score decode")
    rows = []
    for k, j in pairs:
        rows.append({v: {
            "positive": max(scores[q][v] for q in range(k-3, k+4)),
            "control": max(scores[q][v] for q in range(j-3, j+4))}
            for v in VARIANTS})
    aucs = {}
    for v in VARIANTS:
        positives = [r[v]["positive"] for r in rows]
        controls = [r[v]["control"] for r in rows]
        aucs[v] = prior.auc(positives, controls)
    clean = aucs["clean"]
    hypotheses = {
        "H1_clean_auc_ge_070": clean >= .70,
        "H2_clean_auc_ge_050": clean >= .50,
        "H3_brightness_drop_le_010": all(
            clean - aucs[v] <= .10 for v in ("gain_070", "gain_130")),
        "H4_translation_drop_le_010":
            clean - aucs["translation_8_6"] <= .10,
        "H5_glare_drop_le_010": clean - aucs["glare"] <= .10}
    summary = {
        "experiment": "E002-397", "participant": person,
        "source_md5": MD5[person], "session": video,
        "frames": len(frames), "eeg_markers": len(markers),
        "pairs": len(pairs), "rejected": rejected,
        "feature": "background-median-subtracted Farneback eye-flow p80",
        "auc": aucs, "hypotheses": hypotheses,
        "previously_used_participants": True,
        "ground_truth": "EEG markers, not aperture",
        "physical_aperture_validated": False,
        "actual_exposure_known": False,
        "independent_velocity_bound": False,
        "product": "ABSTAIN_UNCALIBRATED"}
    return summary, rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archive", required=True)
    p.add_argument("--participant", choices=sorted(MD5), required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    output = pathlib.Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    result, rows = evaluate(args.archive, args.participant)
    (output / "summary.json").write_text(json.dumps(result, indent=2))
    (output / "anonymous_scores.json").write_text(
        json.dumps(rows, separators=(",", ":")))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
