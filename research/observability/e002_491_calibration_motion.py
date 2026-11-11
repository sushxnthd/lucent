#!/usr/bin/env python3
"""E002-491: aggregate-only S01 calibration video motion screening, not blink inference."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

from e002_488_avi_header import md5_file, safe_member

EXPECTED_MD5 = "fb56109542a13aa7879778833fe4cbaa"
SIZE = 64 * 64
MAX_FRAMES = 12000
CENTER = tuple(y * 64 + x for y in range(16, 48) for x in range(16, 48))
BORDER = tuple(y * 64 + x for y in range(64) for x in range(64)
               if x < 8 or x >= 56 or y < 8 or y >= 56)


def mean_std(frame):
    avg = sum(frame) / SIZE
    var = sum(v * v for v in frame) / SIZE - avg * avg
    return avg, math.sqrt(max(0, var))


def motion_pair(previous, current):
    if len(previous) != SIZE or len(current) != SIZE:
        raise ValueError("INVALID_FRAME_SIZE")
    if previous == current:
        return {"status": "DUPLICATE", "candidate": False, "center": 0.0, "border": 0.0}
    pm, ps = mean_std(previous)
    cm, cs = mean_std(current)
    offset = cm - pm
    center = sum(abs(current[i] - previous[i] - offset) for i in CENTER) / (len(CENTER) * 255)
    border = sum(abs(current[i] - previous[i] - offset) for i in BORDER) / (len(BORDER) * 255)
    ratio = center / (border + 0.01)
    bad = (abs(offset) > 15 or min(ps, cs) < 10 or
           cs > 1.2 * ps or ps > 1.2 * cs)
    candidate = not bad and center >= 0.035 and ratio >= 1.7
    return {"status": "NUISANCE" if bad else "ELIGIBLE",
            "candidate": candidate, "center": center, "border": border,
            "ratio": ratio}


def percentile(values, p):
    if not values:
        return None
    a = sorted(values)
    return round(a[min(len(a) - 1, int(p * (len(a) - 1)))], 7)


def analyze(frames):
    previous = None
    n = duplicate = nuisance = eligible = 0
    centers, borders, candidates = [], [], []
    for frame in frames:
        if len(frame) != SIZE:
            raise ValueError("TRUNCATED_FRAME")
        if previous is not None:
            pair = motion_pair(previous, frame)
            if pair["status"] == "DUPLICATE":
                duplicate += 1
            elif pair["status"] == "NUISANCE":
                nuisance += 1
            else:
                eligible += 1
                centers.append(pair["center"])
                borders.append(pair["border"])
                if pair["candidate"]:
                    candidates.append((n, pair["center"], pair["ratio"]))
        previous = frame
        n += 1
        if n > MAX_FRAMES:
            raise ValueError("FRAME_LIMIT")
    if n < 3:
        raise ValueError("INSUFFICIENT_DECODED_FRAMES")
    top = []
    for idx, score, ratio in sorted(candidates, key=lambda v: (-v[1], v[0])):
        if all(abs(idx - old) >= 5 for old in top):
            top.append(idx)
            if len(top) == 20:
                break
    confounded_fraction = nuisance / max(1, n - 1 - duplicate)
    return {
        "experiment": "E002-491",
        "subject": "S01_CALIBRATION_ONLY",
        "evidence_tier": "AUTHENTIC_VIDEO_IMAGE_CONTENT_PROXY_NOT_ANATOMY",
        "decoded_native_frames": n,
        "analyzed_pairs": n - 1,
        "exact_duplicate_pairs": duplicate,
        "photometric_or_contrast_confounded_pairs": nuisance,
        "eligible_pairs": eligible,
        "localized_motion_candidate_pairs": len(candidates),
        "top_candidate_native_frame_indices": top,
        "eligible_center_l1_quantiles": {str(q): percentile(centers, q) for q in (0.5, 0.9, 0.99)},
        "eligible_border_l1_quantiles": {str(q): percentile(borders, q) for q in (0.5, 0.9, 0.99)},
        "nuisance_unstable_gt_20pct": confounded_fraction > 0.20,
        "candidate_screen_positive": len(candidates) > 0,
        "anatomical_closure_labels": 0,
        "physical_hidden_closure_certified": False,
        "independent_hardware_clock_authenticated": False,
        "acquisition_fps_authenticated": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def read_frames(video):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFMPEG_MISSING")
    command = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(video),
               "-vf", "scale=64:64:flags=area,format=gray",
               "-frames:v", str(MAX_FRAMES), "-vsync", "0",
               "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        while True:
            chunks = bytearray()
            while len(chunks) < SIZE:
                part = proc.stdout.read(SIZE - len(chunks))
                if not part:
                    break
                chunks.extend(part)
            if not chunks:
                break
            if len(chunks) != SIZE:
                raise ValueError("PARTIAL_DECODED_FRAME")
            yield bytes(chunks)
        if proc.wait(timeout=120) != 0:
            raise RuntimeError("FFMPEG_DECODE_FAILED")
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def inspect(archive):
    archive = Path(archive)
    if archive.stat().st_size > 600_000_000:
        raise ValueError("ARCHIVE_TOO_LARGE")
    if md5_file(archive) != EXPECTED_MD5:
        raise ValueError("CHECKSUM_MISMATCH")
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if not all(safe_member(x) for x in infos):
            raise ValueError("UNSAFE_ARCHIVE")
        videos = sorted((x for x in infos if x.filename.lower().endswith("_phantom.avi")),
                        key=lambda x: x.filename)
        if not videos or videos[0].file_size > 1_000_000_000:
            raise ValueError("NO_BOUNDED_VIDEO")
        with tempfile.TemporaryDirectory(prefix="lucent491_") as td:
            dest = Path(td) / "calibration.avi"
            with z.open(videos[0]) as src, dest.open("wb") as out:
                shutil.copyfileobj(src, out, 1024 * 1024)
            if dest.stat().st_size != videos[0].file_size:
                raise ValueError("VIDEO_SIZE_MISMATCH")
            return analyze(read_frames(dest))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = inspect(args.archive)
        rc = 0
    except Exception as exc:
        result = {"experiment": "E002-491", "status": "FAILED_OR_ABSTAINED",
                  "reason": str(exc)[:160], "subject": "S01_CALIBRATION_ONLY",
                  "anatomical_closure_labels": 0,
                  "physical_hidden_closure_certified": False,
                  "independent_hardware_clock_authenticated": False,
                  "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}
        rc = 2
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return rc


if __name__ == "__main__":
    sys.exit(main())
