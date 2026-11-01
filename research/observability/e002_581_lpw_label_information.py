#!/usr/bin/env python3
"""E002-581: frozen real-LPW annotation temporal-information audit.

Never interprets pupil-center labels as eyelid aperture, blink or shutter truth.
Only aggregate counts leave the process. Source is development LPW/1/1.txt.
"""
import argparse
import hashlib
import json
import numpy as np
import e002_580_lpw_label_alias as source

EXPERIMENT = "E002-581"
LABEL_SHA = "12f60068317a341809babb7c2cbce90b8ba299ad877d75186687b0d521f6d5d2"
EXACT = 1e-6
NEAR = 1e-3
MOVING = 0.1
BLOCK = 50
SEED = 581
REPS = 499


def increments(points):
    x = np.asarray(points, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != 2 or len(x) < 4 or not np.all(np.isfinite(x)):
        raise ValueError("INVALID_COORDINATES")
    return np.diff(x, axis=0)


def junctions(d):
    d = np.asarray(d, dtype=np.float64)
    if d.ndim != 2 or d.shape[1] != 2 or len(d) < 3 or not np.all(np.isfinite(d)):
        raise ValueError("INVALID_INCREMENTS")
    residual = np.linalg.norm(np.diff(d, axis=0), axis=1)
    speed = np.linalg.norm(d, axis=1)
    exact = residual <= EXACT
    moving = exact & (np.minimum(speed[:-1], speed[1:]) >= MOVING)
    return exact, residual <= NEAR, moving


def run_stats(flags):
    # A run is a consecutive series of qualifying acceleration junctions.
    z = np.r_[False, np.asarray(flags, dtype=bool), False].astype(np.int8)
    begins = np.flatnonzero(np.diff(z) == 1)
    ends = np.flatnonzero(np.diff(z) == -1)
    lengths = ends - begins
    return {"junctions": int(np.sum(flags)),
            "runs_ge_3": int(np.sum(lengths >= 3)),
            "longest_junction_run": int(np.max(lengths)) if len(lengths) else 0}


def permute_blocks(d, rng):
    out = np.array(d, copy=True)
    for start in range(0, len(d), BLOCK):
        stop = min(start + BLOCK, len(d))
        out[start:stop] = d[start:stop][rng.permutation(stop - start)]
    return out


def audit(points, reps=REPS, seed=SEED):
    d = increments(points)
    exact, near, moving = junctions(d)
    observed = run_stats(moving)
    rng = np.random.default_rng(seed)
    null_count = np.empty(reps, dtype=np.int64)
    null_longest = np.empty(reps, dtype=np.int64)
    for i in range(reps):
        _, _, m = junctions(permute_blocks(d, rng))
        stats = run_stats(m)
        null_count[i] = stats["junctions"]
        null_longest[i] = stats["longest_junction_run"]
    def describe(v, observed_value):
        return {"median": float(np.median(v)), "p95": float(np.percentile(v, 95)),
                "max": int(v.max()),
                "add_one_upper_tail": float((1 + np.sum(v >= observed_value)) / (reps + 1))}
    return {
        "source_annotation_rows": int(len(points)),
        "increment_count": int(len(d)),
        "junction_count": int(len(exact)),
        "all_exact_linear_junctions_including_stationary": int(exact.sum()),
        "all_near_linear_junctions_including_stationary": int(near.sum()),
        "moving_exact_linear": observed,
        "null": {"replicates": reps, "seed": seed, "increment_block": BLOCK,
                 "moving_junction_count": describe(null_count, observed["junctions"]),
                 "longest_moving_junction_run": describe(null_longest, observed["longest_junction_run"])},
    }


def self_test():
    stationary = np.repeat([[3.0, 4.0]], 20, axis=0)
    r = audit(stationary, reps=9)
    assert r["all_exact_linear_junctions_including_stationary"] == 18
    assert r["moving_exact_linear"]["junctions"] == 0
    linear = np.c_[np.arange(20, dtype=float), np.zeros(20)]
    a = audit(linear, reps=9)
    assert a["moving_exact_linear"]["junctions"] == 18
    assert a["moving_exact_linear"]["longest_junction_run"] == 18
    assert a["moving_exact_linear"]["runs_ge_3"] == 1
    assert a == audit(linear + [14, -7], reps=9)
    rotation = np.array([[0, -1], [1, 0]], dtype=float)
    assert a == audit(linear @ rotation, reps=9)
    kink = linear.copy()
    kink[10:] += [0, 4]
    assert audit(kink, reps=9)["moving_exact_linear"]["longest_junction_run"] < 18
    tiny = linear * 0.01
    assert audit(tiny, reps=9)["moving_exact_linear"]["junctions"] == 0
    d = increments(linear)
    p = permute_blocks(d, np.random.default_rng(SEED))
    assert np.array_equal(np.sort(p, axis=0), np.sort(d, axis=0))
    for bad in (np.ones((3, 2)), np.ones((20, 3)),
                np.array([[1, 2], [3, 4], [5, 6], [float("nan"), 0]])):
        try:
            increments(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Malformed input was accepted")
    print(json.dumps({"experiment": EXPERIMENT, "self_test": "PASS",
                      "checks": ["stationary-vs-moving", "linear", "kink",
                                 "translation", "rotation", "tiny-motion",
                                 "seed", "permutation-multiset", "invalid-input"]},
                     sort_keys=True))


def execute():
    raw, provenance = source.fetch_labels()
    if hashlib.sha256(raw).hexdigest() != LABEL_SHA:
        raise ValueError("FROZEN_SOURCE_SHA_MISMATCH")
    points = source.parse_labels(raw)
    return {"experiment": EXPERIMENT,
            "evidence_tier": "AUTHENTIC_INVESTIGATOR_PUPIL_CENTER_LABEL_ORDER_ONLY",
            "source_label_member": source.LABEL, "source_label_sha256": LABEL_SHA,
            "video_sha256_previously_verified_not_rechecked": source.VIDEO_SHA_PREVIOUSLY_VERIFIED,
            "reported_source_fps_not_shutter_calibrated": 95,
            "thresholds_px": {"exact_acceleration": EXACT, "near_acceleration": NEAR,
                              "minimum_adjacent_displacement": MOVING},
            "result": audit(points),
            "interpretation": "DESCRIPTIVE_LABEL_ORDER_CONTROL_NOT_INTERPOLATION_PROOF",
            "anatomical_closure_labels": 0, "independent_human_rater_pairs": 0,
            "physical_shutter_authenticated": False,
            "continuous_time_velocity_certified": False,
            "heldout_physical_predictions": 0,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    try:
        print(json.dumps(execute(), sort_keys=True))
    except Exception as exc:
        print(json.dumps({"experiment": EXPERIMENT, "status": "ABSTAIN",
                          "reason": type(exc).__name__ + ":" + str(exc)[:100],
                          "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"},
                         sort_keys=True))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
