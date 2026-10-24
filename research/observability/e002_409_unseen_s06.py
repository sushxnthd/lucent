#!/usr/bin/env python3
"""E002-409 frozen S06 untouched-participant transfer of E002-397 image-motion proxy.

Human video + EEG marker association only. Not eyelid aperture or physical ground truth.
Do not upload images, source timestamps, or source frame IDs.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import io
import json
import math
import shutil
import tempfile
import zipfile
from pathlib import Path

import cv2
import numpy as np

import e002_395_human_proxy as prior
import e002_397_human_motion as motion

SOURCE_MD5 = "8217203472f7393b03aa56102dbc9adc"
VARIANTS = ("clean", "gain_070", "gain_130", "blur_sigma2",
            "translation_8_6", "glare")
OFFSETS = (.55, -.55, .75, -.75, 1.05, -1.05)


def select_session(z):
    """Deterministically select first complete video/sync session; no outcome selection."""
    names = z.namelist()
    videos = sorted(n for n in names if n.lower().endswith("_phantom.avi"))
    candidates = [(v, v[:-len("_phantom.avi")] + "_sync.csv") for v in videos]
    eligible = [(v, s) for v, s in candidates if s in names]
    if not eligible:
        raise ValueError("No paired Phantom AVI and synchronization CSV")
    return eligible[0]


def read_sync(z, path):
    with z.open(path) as src:
        reader = csv.DictReader(io.TextIOWrapper(src, encoding="utf-8-sig"))
        if not {"Time", "PhanFrame", "Blinks"}.issubset(reader.fieldnames or []):
            raise ValueError("Missing required sync columns")
        frames, markers = [], []
        for row in reader:
            t = prior.num(row.get("Time"))
            fid = prior.num(row.get("PhanFrame"))
            blink = prior.num(row.get("Blinks"))
            if t is None:
                continue
            if fid is not None:
                if not fid.is_integer():
                    raise ValueError("Fractional video frame ID")
                frames.append((int(fid), t))
            if blink is not None and blink > 0:
                markers.append(t)
    if len(frames) < 1000 or not markers:
        raise ValueError("Inadequate frame/marker coverage")
    if any(b[0] != a[0] + 1 or b[1] <= a[1]
           for a, b in zip(frames, frames[1:])):
        raise ValueError("Noncontiguous frame IDs or nonmonotone sync clock")
    return frames, markers


def select_pairs(frames, markers):
    times = [t for _, t in frames]
    ids = [i for i, _ in frames]

    def near(t):
        j = bisect.bisect_left(times, t)
        candidates = [q for q in (j - 1, j) if 4 <= q < len(times) - 4]
        if not candidates:
            return None
        k = min(candidates, key=lambda q: abs(times[q] - t))
        if abs(times[k] - t) > .0100001:
            return None
        if any(ids[q+1] != ids[q] + 1 or
               times[q+1] - times[q] > .0200001
               for q in range(k-3, k+3)):
            return None
        return k

    pairs = []
    rejected = {"event_uncovered_or_gap": 0, "no_clean_control": 0}
    for t in markers:
        k = near(t)
        if k is None:
            rejected["event_uncovered_or_gap"] += 1
            continue
        j = None
        for delta in OFFSETS:
            candidate = t + delta
            if min(abs(candidate - m) for m in markers) < .35:
                continue
            q = near(candidate)
            if q is not None and abs(q - k) > 6:
                j = q
                break
        if j is None:
            rejected["no_clean_control"] += 1
        else:
            pairs.append((k, j))
    return pairs, rejected


def compute_scores(z, video, frames, pairs):
    needed = set()
    for k, j in pairs:
        needed.update(range(k - 3, k + 4))
        needed.update(range(j - 3, j + 4))
    scores = {}
    with tempfile.TemporaryDirectory(prefix="lucent-e002-409-") as tmp:
        local = Path(tmp) / "human.avi"
        with z.open(video) as src, local.open("wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 20)
        cap = cv2.VideoCapture(str(local))
        if not cap.isOpened():
            raise ValueError("Cannot decode source AVI")
        if int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != len(frames):
            raise ValueError("Source video/sync frame-count mismatch")
        previous = None
        index = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                if index in needed:
                    if previous is None or frame.shape[:2] != (288, 320):
                        raise ValueError("Invalid source video geometry")
                    gray0 = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
                    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    scores[index] = {
                        v: motion.motion_score(prior.transform(gray0, v),
                                               prior.transform(gray1, v))
                        for v in VARIANTS
                    }
                previous = frame
                index += 1
        finally:
            cap.release()
        if index != len(frames) or set(scores) != needed:
            raise ValueError("Incomplete frame decode")
    return scores


def summarize(rows, rejected, frame_count, marker_count, session):
    aucs = {}
    for variant in VARIANTS:
        pos = [r[variant]["positive"] for r in rows]
        neg = [r[variant]["control"] for r in rows]
        aucs[variant] = prior.auc(pos, neg)
    clean = aucs["clean"]
    h = {
        "H1_clean_auc_ge_070": clean >= .70,
        "H2_blur_auc_loss_le_010": clean - aucs["blur_sigma2"] <= .10,
        "H3_glare_auc_loss_le_010": clean - aucs["glare"] <= .10,
        "H4_gains_auc_loss_le_010": all(
            clean - aucs[v] <= .10 for v in ("gain_070", "gain_130")),
        "H5_translation_auc_loss_le_010":
            clean - aucs["translation_8_6"] <= .10,
    }
    return {
        "experiment": "E002-409", "participant": "S06",
        "source_md5": SOURCE_MD5, "session": session,
        "source_frame_count": frame_count, "eeg_marker_count": marker_count,
        "paired_windows": len(rows), "rejected": rejected,
        "feature": "frozen E002-397 background-subtracted Farneback eye-flow p80",
        "auc": aucs, "hypotheses": h, "all_hypotheses_pass": all(h.values()),
        "previously_evaluated_participant": False,
        "physical_aperture_validated": False,
        "independent_camera_clock": False, "hard_velocity_bound": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "evidence_tier": "untouched human participant; EEG marker association, not physical aperture"
    }


def run(archive, output):
    if prior.md5(archive) != SOURCE_MD5:
        raise ValueError("S06 archive checksum mismatch")
    with zipfile.ZipFile(archive) as z:
        video, sync = select_session(z)
        frames, markers = read_sync(z, sync)
        pairs, rejected = select_pairs(frames, markers)
        if len(pairs) < 15:
            raise ValueError(f"Frozen feasibility failure: only {len(pairs)} pairs")
        scores = compute_scores(z, video, frames, pairs)
    rows = [{
        v: {"positive": max(scores[q][v] for q in range(k-3, k+4)),
            "control": max(scores[q][v] for q in range(j-3, j+4))}
        for v in VARIANTS
    } for k, j in pairs]
    summary = summarize(rows, rejected, len(frames), len(markers), video)
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output / "anonymous_scores.json").write_text(json.dumps(rows, separators=(",", ":")) + "\n")
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archive", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    summary = run(a.archive, a.output)
    # No frame imagery, EEG times, or per-pair linkage in stdout.
    print(json.dumps({k: summary[k] for k in
                      ("experiment", "paired_windows", "auc", "hypotheses",
                       "all_hypotheses_pass", "product")}, indent=2))


if __name__ == "__main__":
    main()
