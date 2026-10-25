#!/usr/bin/env python3
"""E002-444: aggregate optical changes from actual S19 video, not physical aperture.
S21/S22 sealed; outputs never include images or participant-identifying time series.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import statistics
import subprocess
import tempfile
import zipfile
from pathlib import Path

import numpy as np

from e002_441_human_acquisition import SOURCES, download
from e002_442_sync_timebase import _num, percentile

EXPECTED_FRAMES = 56911
WIDTH, HEIGHT = 320, 288
FIXED_WINDOW = 12000
SHIFT_CONTROL = 137


def verify_and_extract(archive, target):
    expected, size = SOURCES["S19"]
    if archive.stat().st_size != size:
        raise ValueError("published archive size mismatch")
    digest = hashlib.md5()
    with archive.open("rb") as source:
        for chunk in iter(lambda: source.read(1048576), b""):
            digest.update(chunk)
    if digest.hexdigest() != expected:
        raise ValueError("published archive MD5 mismatch")
    with zipfile.ZipFile(archive) as z:
        members = [x for x in z.infolist() if not x.is_dir()]
        for member in members:
            p = Path(member.filename)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError("unsafe ZIP member")
        video = [x for x in members if x.filename.lower().endswith("_phantom.avi")]
        sync = [x for x in members if x.filename.lower().endswith("_sync.csv")]
        if len(video) != 1 or len(sync) != 1:
            raise ValueError("expected exactly one Phantom AVI and sync CSV")
        times = []
        with z.open(sync[0]) as raw:
            rows = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline=""))
            if not rows.fieldnames or not {"Time", "RelTime"}.issubset(rows.fieldnames):
                raise ValueError("missing synchronization columns")
            for row in rows:
                if _num(row.get("RelTime")) is not None:
                    t = _num(row.get("Time"))
                    if t is None:
                        raise ValueError("nonfinite event time")
                    times.append(t)
        if len(times) != EXPECTED_FRAMES:
            raise ValueError("event/frame count mismatch")
        if any(b <= a for a, b in zip(times, times[1:])):
            raise ValueError("nonmonotone candidate event times")
        with z.open(video[0]) as source, target.open("wb") as output:
            for chunk in iter(lambda: source.read(1048576), b""):
                output.write(chunk)
    return times


def grayscale_frames(video, count=FIXED_WINDOW):
    if count < 2:
        raise ValueError("need two or more frames")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
           "-map", "0:v:0", "-frames:v", str(count), "-f", "rawvideo",
           "-pix_fmt", "gray", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for _ in range(count):
            raw = bytearray()
            while len(raw) < WIDTH * HEIGHT:
                part = proc.stdout.read(WIDTH * HEIGHT - len(raw))
                if not part:
                    raise ValueError("truncated or undecodable video frame")
                raw.extend(part)
            yield np.frombuffer(raw, dtype=np.uint8).reshape((HEIGHT, WIDTH))
        proc.stdout.close()
        stderr = proc.stderr.read().decode("utf-8", "replace")
        if proc.wait(timeout=60) != 0:
            raise ValueError("FFmpeg decode failure: " + stderr[:200])
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def summarize(changes, changed_fractions, exact_duplicates, gaps):
    n = len(changes)
    if n < 2 or len(changed_fractions) != n or len(exact_duplicates) != n or len(gaps) != n:
        raise ValueError("mismatched or short optical measurements")
    if any(not math.isfinite(float(v)) or v < 0 for v in changes + changed_fractions + gaps):
        raise ValueError("nonfinite or negative measurement")
    if any(g <= 0 for g in gaps):
        raise ValueError("nonpositive event gap")
    if any(c > 1 or f > 1 for c, f in zip(changes, changed_fractions)):
        raise ValueError("optical change outside normalized range")
    def bins(values):
        selections = [
            [v for v, g in zip(values, gaps) if g <= .01000001],
            [v for v, g in zip(values, gaps) if .01000001 < g <= .10000001],
            [v for v, g in zip(values, gaps) if g > .10000001],
        ]
        return {name: {"n": len(arr), "median": statistics.median(arr) if arr else None,
                       "p90": percentile(arr, .90)}
                for name, arr in zip(("le_10ms", "10_to_100ms", "gt_100ms"), selections)}
    actual = bins(changes)
    shifted = bins(changes[SHIFT_CONTROL % n:] + changes[:SHIFT_CONTROL % n])
    low = actual["le_10ms"]["median"]
    long = [c for c, g in zip(changes, gaps) if g > .10000001]
    return {
        "pair_count": n,
        "exact_duplicate_pairs": sum(bool(x) for x in exact_duplicates),
        "exact_duplicate_fraction": sum(bool(x) for x in exact_duplicates) / n,
        "mean_absolute_gray_change_normalized": {
            "p01": percentile(changes, .01), "median": statistics.median(changes),
            "p90": percentile(changes, .90), "p99": percentile(changes, .99),
            "max": max(changes)},
        "fraction_pixels_change_ge_16": {
            "median": statistics.median(changed_fractions),
            "p90": percentile(changed_fractions, .90)},
        "event_gap_binned_optical_change": actual,
        "shift_137_control_event_gap_binned_change": shifted,
        "long_gap_fraction_above_short_gap_median": (
            sum(c > low for c in long) / len(long) if long and low is not None else None),
        "long_gap_evidence": "INSUFFICIENT_LONG_GAPS" if len(long) < 5 else "DESCRIPTIVE_ONLY",
        "duplicate_warning": sum(bool(x) for x in exact_duplicates) / n > .05,
        "independent_frame_information_rejected": statistics.median(changes) == 0,
        "event_frame_alignment_authenticated": False,
        "physical_shutter_timing_authenticated": False,
        "anatomical_aperture_measured": False,
        "e002_371_physical_validation": "NOT_ESTABLISHED",
        "product_claim": "ABSTAIN_UNCALIBRATED",
    }


def evaluate_frames(frames, event_times, limit=FIXED_WINDOW):
    if len(event_times) < limit or limit < 3:
        raise ValueError("not enough candidate event times")
    prev = None
    changes, fractions, duplicates, gaps = [], [], [], []
    count = 0
    for frame in frames:
        if count >= limit:
            break
        arr = np.asarray(frame)
        if arr.shape != (HEIGHT, WIDTH) or arr.dtype != np.uint8:
            raise ValueError("invalid decoded frame shape or dtype")
        if prev is not None:
            delta = np.abs(arr.astype(np.int16) - prev.astype(np.int16))
            changes.append(float(delta.mean() / 255.0))
            fractions.append(float(np.mean(delta >= 16)))
            duplicates.append(bool(np.array_equal(arr, prev)))
            gaps.append(float(event_times[count] - event_times[count - 1]))
        prev = arr.copy()
        count += 1
    if count != limit:
        raise ValueError("decoded frame count below frozen window")
    return summarize(changes, fractions, duplicates, gaps)


def run(archive):
    with tempfile.TemporaryDirectory() as directory:
        video = Path(directory) / "s19.avi"
        times = verify_and_extract(archive, video)
        metrics = evaluate_frames(grayscale_frames(video), times)
    return {
        "experiment": "E002-444",
        "source": "published hash-verified human S19 Phantom AVI",
        "frozen_frame_window": FIXED_WINDOW,
        "decoded_frame_count": FIXED_WINDOW,
        "candidate_event_count": len(times),
        "human_video_optical_measurement": metrics,
        "participant_holdouts_inspected": False,
        "physical_release_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        archive = args.zip or Path(directory) / "S19.zip"
        if args.zip is None:
            download("S19", archive)
        result = run(archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"experiment": "E002-444", "pairs": result["human_video_optical_measurement"]["pair_count"],
                      "duplicates": result["human_video_optical_measurement"]["exact_duplicate_pairs"],
                      "release_authorized": False}))


if __name__ == "__main__":
    main()
