#!/usr/bin/env python3
"""E002-579: preregistered, non-anatomical motion-proxy falsification on real LPW.

Outputs aggregate statistics only; no private images, indices, or per-frame scores.
Not a blink detector or E002-371 physiological validation.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np

import e002_577_lpw_range_probe as source
import e002_578_real_lpw_packet as frozen

EXPERIMENT = "E002-579"
H, W = 60, 80
STEP = 3
HIGH = 0.05
LOW = 0.02
EXPECTED_FRAMES = 2000


def normalize(frames):
    if frames.ndim != 3 or frames.shape[1:] != (H, W):
        raise ValueError("INVALID_FRAME_GEOMETRY")
    flat = frames.astype(np.float64).reshape(len(frames), -1)
    centered = flat - flat.mean(axis=1, keepdims=True)
    norms = np.linalg.norm(centered, axis=1)
    valid = np.isfinite(norms) & (norms >= 1e-6)
    z = np.zeros_like(centered)
    z[valid] = centered[valid] / norms[valid, None]
    return z, valid


def distances(z, step):
    d = 1.0 - np.einsum("ij,ij->i", z[:-step], z[step:], optimize=True)
    return np.clip(d, 0.0, 2.0)


def features(frames, missing=None):
    z, valid = normalize(frames)
    if missing is not None:
        if len(missing) != len(valid):
            raise ValueError("MISSINGNESS_LENGTH_MISMATCH")
        valid &= ~missing
    d1 = distances(z, 1)
    d3 = distances(z, STEP)
    m = np.maximum(np.maximum(d1[:-2], d1[1:-1]), d1[2:])
    n = len(m)
    eligible = valid[:-3] & valid[1:-2] & valid[2:-1] & valid[3:]
    flagged = eligible & (m >= HIGH) & (d3 <= LOW)
    return m, d3, eligible, flagged


def report_condition(frames, missing=None):
    m, e, valid, flags = features(frames, missing)
    phases = []
    for p in range(STEP):
        idx = np.arange(p, len(m), STEP)
        use = idx[valid[idx]]
        if len(use):
            percentiles = lambda v: [round(float(x), 6) for x in np.percentile(v, [50, 90, 99])]
            summary = {"m_p50_p90_p99": percentiles(m[use]),
                       "endpoint_p50_p90_p99": percentiles(e[use])}
        else:
            summary = {"m_p50_p90_p99": None, "endpoint_p50_p90_p99": None}
        phases.append({"phase": p, "quadruples": int(len(idx)),
                       "eligible": int(len(use)), "flagged": int(flags[idx].sum()),
                       **summary})
    return {"native_frames": int(len(frames)), "quadruples": int(len(m)),
            "eligible": int(valid.sum()), "abstained": int((~valid).sum()),
            "flagged": int(flags.sum()), "phase": phases}, flags


def apply_jitter(frames):
    out = frames.copy()
    out[1::2, :, 1:] = frames[1::2, :, :-1]
    out[1::2, :, 0] = frames[1::2, :, 0]
    return out


def apply_blur(frames):
    pad = np.pad(frames.astype(np.float64),
                 ((0, 0), (1, 1), (1, 1)), mode="edge")
    out = np.zeros_like(frames, dtype=np.float64)
    for dy in range(3):
        for dx in range(3):
            out += pad[:, dy:dy+H, dx:dx+W] / 9.0
    return out


def stability(base, other):
    intersection = int((base & other).sum())
    union = int((base | other).sum())
    return {"both_flagged": intersection, "union_flagged": union,
            "jaccard": round(intersection / union, 6) if union else None}


def analyze_frames(frames):
    if frames.shape != (EXPECTED_FRAMES, H, W):
        raise ValueError("FROZEN_FRAME_COUNT_OR_GEOMETRY_MISMATCH")
    baseline, baseflags = report_condition(frames)
    photometric = frames.astype(np.float64)
    photometric[1::2] = 1.3 * photometric[1::2] + 20.0
    light, lightflags = report_condition(photometric)
    # Positive affine invariance is an implementation requirement.
    base_m, base_e, _, _ = features(frames)
    light_m, light_e, _, _ = features(photometric)
    photometric_error = max(float(np.max(np.abs(base_m - light_m))),
                            float(np.max(np.abs(base_e - light_e))))
    if photometric_error > 1e-4 or not np.array_equal(baseflags, lightflags):
        raise ValueError("PHOTOMETRIC_INVARIANCE_FALSIFIED")
    jitter, jitterflags = report_condition(apply_jitter(frames))
    blur, blurflags = report_condition(apply_blur(frames))
    missing = np.zeros(len(frames), dtype=bool)
    missing[::20] = True
    dropout, dropflags = report_condition(frames, missing)
    return {"experiment": EXPERIMENT,
            "evidence_tier": "AUTHENTIC_HUMAN_VIDEO_NONANATOMICAL_PROXY_ONLY",
            "source": "LPW/1/1.avi", "source_sha256": frozen.VIDEO_SHA,
            "reported_fps_not_physically_authenticated": "95/1",
            "thresholds": {"native_step_dissimilarity_min": HIGH,
                           "endpoint_dissimilarity_max": LOW},
            "baseline": baseline, "positive_affine_light": light,
            "photometric_max_distance_error": round(photometric_error, 10),
            "one_pixel_alternating_jitter": jitter,
            "jitter_flag_stability": stability(baseflags, jitterflags),
            "three_by_three_blur": blur,
            "blur_flag_stability": stability(baseflags, blurflags),
            "every_twentieth_frame_missing": dropout,
            "dropout_flag_stability": stability(baseflags, dropflags),
            "human_anatomical_rater_pairs": 0, "anatomical_closure_labels": 0,
            "physical_shutter_authenticated": False,
            "velocity_ceiling_certified": False,
            "heldout_physical_predictions": 0,
            "proxy_cannot_establish_blink_or_fatigue": True,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}


def decode_frames(video):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(video),
           "-map", "0:v:0", "-vf", "scale=80:60:flags=area,format=gray",
           "-vsync", "0", "-pix_fmt", "gray", "-f", "rawvideo", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=180, check=True)
    if len(p.stdout) != EXPECTED_FRAMES * H * W:
        raise ValueError("DECODED_FRAME_BYTES_MISMATCH")
    return np.frombuffer(p.stdout, dtype=np.uint8).reshape(EXPECTED_FRAMES, H, W).copy()


def execute():
    total = source.remote_size(source.URL)
    get = source.remote_getter(source.URL, total)
    entry, eligible = source.archive_entries(total, get)
    if entry["name"] != frozen.VIDEO or eligible != 66:
        raise ValueError("SOURCE_ARCHIVE_CHANGED")
    data = source.extract_member(total, get, entry)
    if hashlib.sha256(data).hexdigest() != frozen.VIDEO_SHA:
        raise ValueError("SOURCE_HASH_CHANGED")
    with tempfile.TemporaryDirectory(prefix="lucent-e002-579-private-") as td:
        video = Path(td) / "source.avi"
        video.write_bytes(data)
        del data
        frozen.probe_stream(video)
        frames = decode_frames(video)
        result = analyze_frames(frames)
        if hashlib.sha256(video.read_bytes()).hexdigest() != frozen.VIDEO_SHA:
            raise ValueError("SOURCE_CHANGED_AFTER_ANALYSIS")
    return result


def self_test():
    rng = np.random.default_rng(579)
    x = rng.uniform(10, 240, (EXPECTED_FRAMES, H, W)).astype(np.float32)
    # Test invariance on arbitrary nonconstant frames.
    y = x.astype(np.float64)
    y[1::2] = y[1::2] * 1.3 + 20
    _, fx = report_condition(x)
    _, fy = report_condition(y)
    assert np.array_equal(fx, fy)
    a, b = features(x), features(y)
    assert max(float(np.max(np.abs(a[0] - b[0]))),
               float(np.max(np.abs(a[1] - b[1])))) < 1e-8
    # A-B-A-A image pattern has an endpoint-invisible native excursion.
    q = np.zeros((4, H, W), dtype=np.float64)
    q[0] = x[0]
    q[1] = x[1]
    q[2] = x[0]
    q[3] = x[0]
    _, _, eligible, flags = features(q)
    assert bool(eligible[0]) and bool(flags[0])
    # Flat images must abstain.
    _, _, eligible, flags = features(np.ones((4, H, W)))
    assert not bool(eligible[0]) and not bool(flags[0])
    # Missing frames cannot create a positive.
    missing = np.zeros(4, dtype=bool)
    missing[1] = True
    _, _, eligible, flags = features(q, missing)
    assert not bool(eligible[0]) and not bool(flags[0])
    assert apply_jitter(x).shape == x.shape
    assert apply_blur(x).shape == x.shape
    print(json.dumps({"experiment": EXPERIMENT, "self_test": "PASS",
                      "controls": ["affine invariance", "hidden-proxy positive",
                                   "flat abstention", "missingness abstention",
                                   "jitter and blur geometry"]}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    try:
        result = execute()
        print(json.dumps(result, sort_keys=True))
    except Exception as exc:
        print(json.dumps({"experiment": EXPERIMENT, "status": "ABSTAIN",
                          "failure_type": type(exc).__name__,
                          "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"},
                         sort_keys=True))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
