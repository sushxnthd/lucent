#!/usr/bin/env python3
"""E002-597: real LPW development footage nuisance attack on image proxies.

No anatomical labels, physiological claims, or persisted imagery.
"""
import argparse
import hashlib
import json
import statistics
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

import e002_575_lpw_packet as packet
import e002_577_lpw_range_probe as source
import e002_578_real_lpw_packet as base

ROI = (160, 120, 480, 360)
NAMES = ("brightness_plus30", "brightness_minus30", "gamma_07",
         "gamma_14", "gaussian_blur2", "roi_right24", "roi_down24",
         "black_occlusion", "white_occlusion")
PROXIES = ("dark_fraction", "vertical_edge_energy")


def measure(img, roi=ROI):
    arr = np.asarray(img.crop(roi).convert("L"), dtype=np.uint8)
    if arr.ndim != 2 or arr.shape[0] < 2 or arr.shape[1] < 1:
        raise ValueError("BAD_ROI")
    dark = float(np.mean(arr < 80))
    edges = float(np.mean(np.abs(np.diff(arr.astype(np.int16), axis=0)))) / 255.0
    return dark, edges


def variants(img):
    g = img.convert("L")
    lut_plus = [min(255, v + 30) for v in range(256)]
    lut_minus = [max(0, v - 30) for v in range(256)]
    gamma07 = [round(255 * (v / 255) ** 0.7) for v in range(256)]
    gamma14 = [round(255 * (v / 255) ** 1.4) for v in range(256)]
    yield "brightness_plus30", g.point(lut_plus), ROI
    yield "brightness_minus30", g.point(lut_minus), ROI
    yield "gamma_07", g.point(gamma07), ROI
    yield "gamma_14", g.point(gamma14), ROI
    yield "gaussian_blur2", g.filter(ImageFilter.GaussianBlur(2)), ROI
    yield "roi_right24", g, (184, 120, 504, 360)
    yield "roi_down24", g, (160, 144, 480, 384)
    # Synthetic opaque obstruction covers 25% of central ROI.
    for name, color in (("black_occlusion", 0), ("white_occlusion", 255)):
        occluded = g.copy()
        occluded.paste(color, (240, 180, 400, 300))
        yield name, occluded, ROI


def independent_small_oracle(rows):
    """Separate stdlib implementation for small arrays; no numpy or Pillow."""
    h = len(rows)
    w = len(rows[0])
    dark = sum(1 for row in rows for x in row if x < 80) / (h * w)
    total = sum(abs(rows[y + 1][x] - rows[y][x])
                for y in range(h - 1) for x in range(w))
    edge = total / ((h - 1) * w * 255)
    return dark, edge


def self_test():
    arrays = (
        [[0, 79, 80], [255, 80, 79], [20, 20, 20]],
        [[0, 255, 0, 255]] * 4,
        [[i * 20 + j * 4 for j in range(5)] for i in range(4)],
        [[255] * 5, [0] * 5, [255] * 5, [0] * 5],
    )
    for rows in arrays:
        h, w = len(rows), len(rows[0])
        im = Image.fromarray(np.asarray(rows, dtype=np.uint8), "L")
        a = measure(im, (0, 0, w, h))
        b = independent_small_oracle(rows)
        if any(abs(x - y) > 1e-12 for x, y in zip(a, b)):
            raise AssertionError("INDEPENDENT_ORACLE_MISMATCH")
    flat = Image.new("L", (640, 480), 79)
    changed = {name: measure(im, roi) for name, im, roi in variants(flat)}
    assert measure(flat)[0] == 1
    assert changed["brightness_plus30"][0] == 0
    assert changed["brightness_minus30"][0] == 1
    assert changed["gamma_07"][0] == 0
    assert changed["black_occlusion"][0] == 1
    assert changed["white_occlusion"][0] < 1
    stripes = Image.fromarray(np.tile(np.asarray([0, 255], dtype=np.uint8)[:, None],
                                      (240, 640)), "L")
    assert measure(stripes)[1] > 0.99
    assert measure(stripes.filter(ImageFilter.GaussianBlur(2)))[1] < 0.2
    assert set(changed) == set(NAMES)
    return {"experiment": "E002-597", "self_test": "PASS",
            "independent_oracle_arrays": len(arrays),
            "adversarial_controls": 8,
            "human_labels": 0, "release": "BLOCKED"}


def evaluate_packet(root, owner):
    # Do not print any per-frame values, clip identifiers, or private indices.
    counts = {name: {p: 0 for p in PROXIES} for name in NAMES}
    delta = {name: {p: [] for p in PROXIES} for name in NAMES}
    ranges = {p: [] for p in PROXIES}
    n = 0
    for row in owner["owner_mapping"]:
        folder = root / "RATER_A" / "clips" / row["blind_clip"]
        native = []
        per_nuisance = {name: [] for name in NAMES}
        for i in range(19):
            f = folder / f"frame_{i:02d}.png"
            if not f.is_file() or f.is_symlink() or packet.png_dimensions(f) != (640, 480):
                raise RuntimeError("SOURCE_FRAME_GEOMETRY_FAILED")
            with Image.open(f) as original:
                original.load()
                native.append(measure(original))
                altered = {}
                for name, im, roi in variants(original):
                    altered[name] = measure(im, roi)
                if set(altered) != set(NAMES):
                    raise RuntimeError("MISSING_NUISANCE")
                for name in NAMES:
                    per_nuisance[name].append(altered[name])
            n += 1
        span = [max(v[j] for v in native) - min(v[j] for v in native)
                for j in range(2)]
        for j, proxy in enumerate(PROXIES):
            ranges[proxy].append(span[j])
        for name in NAMES:
            for i in range(19):
                for j, proxy in enumerate(PROXIES):
                    d = abs(per_nuisance[name][i][j] - native[i][j])
                    delta[name][proxy].append(d)
                    if d > span[j]:
                        counts[name][proxy] += 1
    if n != 190:
        raise RuntimeError("SOURCE_FRAME_COUNT_FAILED")
    summary = {}
    for name in NAMES:
        summary[name] = {}
        for proxy in PROXIES:
            d = delta[name][proxy]
            summary[name][proxy] = {
                "nuisance_dominance_frames": counts[name][proxy],
                "median_absolute_change": round(statistics.median(d), 8),
                "maximum_absolute_change": round(max(d), 8),
                "stability_gate": "FAIL" if counts[name][proxy] > 19 else "PASS_NECESSARY_ONLY",
            }
    return {"source_frames": n, "development_windows": len(owner["owner_mapping"]),
            "baseline_median_temporal_range": {
                p: round(statistics.median(ranges[p]), 8) for p in PROXIES},
            "nuisance_results": summary,
            "any_necessary_stability_failure": any(
                counts[name][p] > 19 for name in NAMES for p in PROXIES)}


def execute():
    owner, a, b, _ = base.make_plan()
    total = source.remote_size(source.URL)
    get = source.remote_getter(source.URL, total)
    entry, eligible = source.archive_entries(total, get)
    if entry["name"] != base.VIDEO or eligible != 66:
        raise RuntimeError("SOURCE_ENTRY_MISMATCH")
    data = source.extract_member(total, get, entry)
    if hashlib.sha256(data).hexdigest() != base.VIDEO_SHA:
        raise RuntimeError("SOURCE_DIGEST_MISMATCH")
    with tempfile.TemporaryDirectory(prefix="lucent-e002-597-private-") as td:
        folder = Path(td)
        video = folder / "source.avi"
        video.write_bytes(data)
        del data
        base.probe_stream(video)
        manifest = {"videos": [{
            "participant_id": "1", "video_id": "1",
            "video_sha256": base.VIDEO_SHA,
            "native_frame_count": base.NATIVE_FRAMES,
            "absolute_path": str(video),
        }]}
        root = folder / "private_review_packets"
        packet.build_packet(owner, manifest, a, b, root)
        if base.verify_packet(root, owner, a, b) != 190:
            raise RuntimeError("NATIVE_SOURCE_AUDIT_FAILED")
        result = evaluate_packet(root, owner)
        if packet.sha256(video) != base.VIDEO_SHA:
            raise RuntimeError("SOURCE_CHANGED")
    return {"experiment": "E002-597", "status": "AUTHENTIC_SOURCE_NUISANCE_AUDIT_COMPLETE",
            "evidence_tier": "REAL_HUMAN_DEVELOPMENT_IMAGES_NONANATOMICAL_PROXY_ONLY",
            "source_sha256": base.VIDEO_SHA,
            "private_source_retained": False,
            "anatomical_labels": 0, "human_rater_pairs": 0,
            "physical_shutter_calibrations": 0,
            "held_out_physical_predictions": 0,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED",
            **result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
    else:
        print(json.dumps(execute(), sort_keys=True))
