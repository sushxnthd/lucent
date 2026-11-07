#!/usr/bin/env python3
"""E002-510: one-shot source-clock triangulation on checksum-pinned S01.

Only aggregate metadata is emitted. No video frames, individual times or
source-frame indices leave the private temporary runner.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import tempfile
from statistics import median
import xml.etree.ElementTree as ET
import zipfile

EXPECTED_MD5 = "fb56109542a13aa7879778833fe4cbaa"
MAX_ARCHIVE = 650_000_000
MAX_VIDEO = 2_000_000_000
MAX_CSV = 30_000_000
MAX_XML = 10_000_000
MAX_ROWS = 2_000_000
FRAME_KEYS = {"phantom_frame", "phantom_frame_idx", "phantom_frame_index"}
TIME_KEYS = {
    "phantom_time_ms": 1.0,
    "phantom_timestamp_ms": 1.0,
    "phantom_time_us": 0.001,
    "phantom_timestamp_us": 0.001,
    "phantom_time_ns": 0.000001,
    "phantom_timestamp_ns": 0.000001,
    "phantom_time_s": 1000.0,
    "phantom_timestamp_s": 1000.0,
}
BASE = {
    "experiment": "E002-510",
    "subject": "S01_CALIBRATION_ONLY",
    "source": "zenodo.org/records/18970793",
    "paper_claimed_fps": 150,
    "rehost_claimed_approx_fps": 500,
    "human_anatomical_ratings": 0,
    "authenticated_physical_clock": False,
    "physical_shutter_calibrated": False,
    "continuous_time_speed_certified": False,
    "heldout_physical_predictions": 0,
    "product": "ABSTAIN_UNCALIBRATED",
    "release": "BLOCKED",
}

def safe_member(info):
    p = PurePosixPath(info.filename)
    mode = (info.external_attr >> 16) & 0xffff
    return (not p.is_absolute() and ".." not in p.parts
            and not re.match(r"^[A-Za-z]:", info.filename)
            and "\\" not in info.filename and "\x00" not in info.filename
            and not stat.S_ISLNK(mode))

def digest(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def percentile(sorted_values, q):
    k = (len(sorted_values) - 1) * q
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    return sorted_values[lo] * (hi - k) + sorted_values[hi] * (k - lo) if lo != hi else sorted_values[lo]

def validate_frame_clock(rows, headers):
    """Strictly select explicit Phantom frame and time columns; no guessing."""
    normalized = [x.strip().lower().replace(" ", "_") for x in headers]
    frame = [i for i, x in enumerate(normalized) if x in FRAME_KEYS]
    times = [(i, TIME_KEYS[x]) for i, x in enumerate(normalized) if x in TIME_KEYS]
    if len(frame) != 1 or len(times) != 1 or len(set(normalized)) != len(normalized):
        return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "AMBIGUOUS_OR_ABSENT_EXPLICIT_COLUMNS"}
    fi, (ti, scale) = frame[0], times[0]
    pairs = []
    for n, row in enumerate(rows):
        if n >= MAX_ROWS:
            return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "ROW_LIMIT"}
        if len(row) != len(headers):
            return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "ROW_WIDTH"}
        try:
            f = float(row[fi])
            t = float(row[ti]) * scale
        except (ValueError, TypeError, OverflowError):
            return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "INVALID_NUMERIC"}
        if not math.isfinite(f) or not f.is_integer() or f < 0 or not math.isfinite(t):
            return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "INVALID_FRAME_OR_TIME"}
        pairs.append((int(f), t))
    if len(pairs) < 100:
        return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "INSUFFICIENT_PAIRED_FRAMES"}
    steps = []
    for (fa, ta), (fb, tb) in zip(pairs, pairs[1:]):
        if fb != fa + 1 or tb <= ta:
            return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "NONCONTIGUOUS_OR_NONMONOTONIC"}
        steps.append(tb - ta)
    steps.sort()
    med = median(steps)
    if med <= 0:
        return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "NONPOSITIVE_MEDIAN"}
    large = sum(x > 1.5 * med for x in steps)
    discrepancy_150 = abs(med / (1000.0 / 150) - 1.0)
    discrepancy_500 = abs(med / (1000.0 / 500) - 1.0)
    consistent = discrepancy_150 <= 0.02 and large / len(steps) <= 0.01
    return {
        "status": ("SOURCE_TIMEBASE_CONSISTENT_UNAUTHENTICATED" if consistent
                   else "SOURCE_TIMEBASE_CONTRADICTS_CLEAN_150HZ"),
        "paired_frames": len(pairs),
        "median_frame_period_ms": round(med, 6),
        "p05_period_ms": round(percentile(steps, 0.05), 6),
        "p95_period_ms": round(percentile(steps, 0.95), 6),
        "large_gaps_gt_1_5x_median": large,
        "large_gap_fraction": round(large / len(steps), 6),
        "relative_period_error_150hz": round(discrepancy_150, 6),
        "relative_period_error_500hz": round(discrepancy_500, 6),
        "hardware_authenticated": False,
    }

def audit_csv(z, info):
    if info.file_size > MAX_CSV:
        return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "CSV_TOO_LARGE"}
    with z.open(info) as stream:
        with io.TextIOWrapper(stream, encoding="utf-8-sig", errors="strict", newline="") as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                return {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "EMPTY_CSV"}
            return validate_frame_clock(reader, headers)

def audit_xml(z, info):
    """Only inspect explicitly Phantom-scoped nominal FPS fields."""
    if info.file_size > MAX_XML:
        return {"xml_nominal_fps": None, "xml_status": "TOO_LARGE"}
    try:
        root = ET.fromstring(z.read(info))
    except ET.ParseError:
        return {"xml_nominal_fps": None, "xml_status": "UNPARSEABLE"}
    values = []
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        if "phantom" not in tag and not any("phantom" in k.lower() for k in node.attrib):
            continue
        for k, v in node.attrib.items():
            if k.lower() in ("fps", "framerate", "frame_rate"):
                try:
                    n = float(v)
                    if math.isfinite(n) and 0 < n < 100000:
                        values.append(n)
                except ValueError:
                    pass
    unique = sorted(set(values))
    return {"xml_nominal_fps": round(unique[0], 6) if len(unique) == 1 else None,
            "xml_status": "EXPLICIT_PHANTOM_NOMINAL_ONLY" if len(unique) == 1 else "NO_UNAMBIGUOUS_PHANTOM_RATE"}

def avi_metadata(z, info):
    if info.file_size > MAX_VIDEO:
        return {"status": "VIDEO_TOO_LARGE"}
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "source.avi"
        with z.open(info) as src, open(target, "wb") as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
        p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=avg_frame_rate,r_frame_rate,nb_frames,time_base",
                            "-of", "json", str(target)],
                           capture_output=True, text=True, timeout=180, check=True)
        streams = json.loads(p.stdout).get("streams", [])
        if len(streams) != 1:
            return {"status": "NO_UNIQUE_VIDEO_STREAM"}
        s = streams[0]
        return {"status": "CONTAINER_METADATA_ONLY",
                "avg_frame_rate": str(s.get("avg_frame_rate", "unknown"))[:40],
                "r_frame_rate": str(s.get("r_frame_rate", "unknown"))[:40],
                "time_base": str(s.get("time_base", "unknown"))[:40],
                "frame_count_claim": str(s.get("nb_frames", "unknown"))[:40]}

def inspect(archive):
    out = dict(BASE)
    path = Path(archive)
    if path.stat().st_size > MAX_ARCHIVE or digest(path) != EXPECTED_MD5:
        raise ValueError("SOURCE_CHECKSUM_OR_SIZE_FAIL")
    with zipfile.ZipFile(path) as z:
        members = z.infolist()
        if not all(safe_member(x) for x in members):
            raise ValueError("UNSAFE_ARCHIVE")
        def matches(suffix):
            return [x for x in members if x.filename.lower().endswith(suffix)]
        csvs, xmls, avis = matches("_sync.csv"), matches("_phantom.xml"), matches("_phantom.avi")
        out["metadata_file_counts"] = {"sync_csv": len(csvs), "phantom_xml": len(xmls), "phantom_avi": len(avis)}
        out["checksum_pinned_source"] = True
        if len(csvs) != 1:
            out["sync_timebase"] = {"status": "NO_VALID_PHANTOM_FRAME_TIME_MAP", "reason": "NONUNIQUE_SYNC_CSV"}
        else:
            out["sync_timebase"] = audit_csv(z, csvs[0])
        out["xml"] = audit_xml(z, xmls[0]) if len(xmls) == 1 else {"xml_status": "NONUNIQUE_XML"}
        out["avi"] = avi_metadata(z, avis[0]) if len(avis) == 1 else {"status": "NONUNIQUE_AVI"}
    out["physical_timing_claim_allowed"] = False
    out["evidence_tier"] = "AUTHENTIC_HUMAN_SOURCE_METADATA_ONLY"
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archive", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    try:
        out = inspect(a.archive)
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.SubprocessError, UnicodeError, ET.ParseError, json.JSONDecodeError) as exc:
        out = dict(BASE)
        out["status"] = "FAILED_OR_ABSTAINED"
        out["failure_type"] = type(exc).__name__
    Path(a.output).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps(out, sort_keys=True))
    return 0 if out.get("status") != "FAILED_OR_ABSTAINED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
