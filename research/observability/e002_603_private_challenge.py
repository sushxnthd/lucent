#!/usr/bin/env python3
"""E002-603: private-answer synthetic rater challenge; not human evidence.

The seed and owner truth must remain private. Public self-test seeds are NOT
suitable for human qualification. Images and reviewer exports stay off GitHub.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import secrets
import tempfile

from e002_600_phantom_rater_challenge import (
    N_CLIPS, N_FRAMES, W, H, IRIS_PX, THRESHOLD,
    blank_template, frame_png, grade, json_write,
)
from e002_602_public_answer_attack import make_public_only_export

KINDS = ("BRIGHTNESS", "BLUR", "OCCLUSION", "GAZE_GEOMETRY")


def make_schedule(rng):
    order = list(range(N_CLIPS))
    rng.shuffle(order)
    nuisance = dict(zip(order[:4], rng.sample(list(KINDS), len(KINDS))))
    clean = order[4:]
    closed = {c: {rng.randrange(N_FRAMES)} for c in clean}
    remaining = [(c, i) for c in clean for i in range(N_FRAMES)
                 if i not in closed[c]]
    for c, i in rng.sample(remaining, 5):
        closed[c].add(i)
    assert sum(map(len, closed.values())) == 11
    return nuisance, closed


def build_private(output, seed):
    if output.exists() and any(output.iterdir()):
        raise ValueError("OUTPUT_DIRECTORY_NOT_EMPTY")
    rng = random.Random(int.from_bytes(hashlib.sha256(seed.encode()).digest(), "big"))
    nuisance, closed = make_schedule(rng)
    truth_clips = {}
    for c in range(N_CLIPS):
        clip = f"clip_{c:04d}"
        rows = []
        kind = nuisance.get(c, "CLEAN")
        for i in range(N_FRAMES):
            upper = 190 + rng.randrange(-15, 16)
            slope = rng.choice((0.0, 0.05, -0.05, 0.12, -0.12))
            gap = 4 if i in closed.get(c, set()) else 34
            raw = frame_png(upper, gap, slope, kind, i, rng)
            path = output / "reviewer" / "clips" / clip / f"frame_{i:02d}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            rows.append({
                "frame": i, "upper_at_x320": upper,
                "lower_at_x320": upper + gap, "slope": slope,
                "gap_px": gap, "clean": c not in nuisance,
                "nuisance": kind, "sha256": hashlib.sha256(raw).hexdigest(),
            })
        truth_clips[clip] = rows
    for rater in ("A", "B"):
        json_write(output / "reviewer" / f"template_{rater}.json", blank_template(rater))
    json_write(output / "private" / "truth.json", {
        "experiment": "E002-600", "evidence_tier": "PRIVATE_SEED_SYNTHETIC_ONLY",
        "challenge_version": "E002-603", "iris_diameter_px": IRIS_PX,
        "threshold": THRESHOLD, "seed_sha256": hashlib.sha256(seed.encode()).hexdigest(),
        "clips": truth_clips,
    })
    return {"experiment": "E002-603", "frames": N_CLIPS*N_FRAMES,
            "private_schedule": True, "seed_disclosed": False,
            "human_raters": 0, "physical_camera_validation": False,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}


def verify_images(output, truth):
    if truth.get("challenge_version") != "E002-603":
        raise ValueError("WRONG_CHALLENGE_VERSION")
    if set(truth["clips"]) != {f"clip_{c:04d}" for c in range(N_CLIPS)}:
        raise ValueError("INVALID_CLIP_SET")
    for clip, rows in truth["clips"].items():
        if len(rows) != N_FRAMES:
            raise ValueError("INVALID_FRAME_COUNT")
        for i, row in enumerate(rows):
            if row["frame"] != i:
                raise ValueError("FRAME_ORDER_MISMATCH")
            path = output / "reviewer" / "clips" / clip / f"frame_{i:02d}.png"
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError("SOURCE_FRAME_HASH_MISMATCH")
    return True


def ideal_review(truth):
    out = blank_template("A")
    for clip, rows in truth["clips"].items():
        for i, g in enumerate(rows):
            if not g["clean"]:
                continue
            out["clips"][clip][i].update({
                "upper_y": g["upper_at_x320"],
                "lower_y": g["lower_at_x320"],
                "iris_diameter": None, "uncertainty_px": 0.5,
                "measurement_x": 320, "flags": [],
            })
    return out


def selftest():
    fingerprints = []
    schedules = []
    for seed in ("PUBLIC_TEST_SEED_ALPHA_NOT_FOR_HUMANS",
                 "PUBLIC_TEST_SEED_BETA_NOT_FOR_HUMANS"):
        with tempfile.TemporaryDirectory(prefix="e002_603_private_") as td:
            output = Path(td) / "packet"
            build_private(output, seed)
            truth = json.loads((output / "private" / "truth.json").read_text())
            assert verify_images(output, truth)
            ideal = grade(truth, ideal_review(truth))
            assert ideal["qualified_on_synthetic_challenge"]
            attack = grade(truth, make_public_only_export())
            assert not attack["qualified_on_synthetic_challenge"], attack
            schedule = tuple((clip, tuple(i for i,g in enumerate(rows) if g["clean"] and g["gap_px"] <= 20),
                              rows[0]["nuisance"]) for clip,rows in sorted(truth["clips"].items()))
            schedules.append(schedule)
            fingerprints.append(tuple(row["sha256"] for rows in truth["clips"].values() for row in rows))
            replay_output = Path(td) / "replay"
            build_private(replay_output, seed)
            replay_truth = json.loads((replay_output / "private" / "truth.json").read_text())
            assert replay_truth == truth, "same-seed truth replay mismatch"
            assert verify_images(replay_output, replay_truth)
            # A modified image must be rejected before any grade can be issued.
            path = output / "reviewer" / "clips" / "clip_0000" / "frame_00.png"
            path.write_bytes(path.read_bytes() + b"tamper")
            try:
                verify_images(output, truth)
            except ValueError as e:
                assert str(e) == "SOURCE_FRAME_HASH_MISMATCH"
            else:
                raise AssertionError("TAMPER_ACCEPTED")
    assert schedules[0] != schedules[1]
    assert fingerprints[0] != fingerprints[1]
    print(json.dumps({"experiment":"E002-603", "public_development_seed_trials":2,
                      "private_schedule_differs":True, "image_hashes_differ":True,
                      "public_answer_attack_rejected":True,
                      "ideal_synthetic_reviewer_passes":True,
                      "tampered_image_rejected":True, "human_raters":0,
                      "product":"ABSTAIN_UNCALIBRATED", "release":"BLOCKED"},
                     sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--output", type=Path, required=True)
    b.add_argument("--seed", help="Owner-private high-entropy seed; omit to generate securely.")
    g = sub.add_parser("grade")
    g.add_argument("--output", type=Path, required=True)
    g.add_argument("--review", type=Path, required=True)
    sub.add_parser("selftest")
    args = parser.parse_args()
    try:
        if args.cmd == "selftest":
            selftest()
        elif args.cmd == "build":
            print(json.dumps(build_private(args.output, args.seed or secrets.token_hex(32)),
                             sort_keys=True))
        else:
            truth = json.loads((args.output / "private" / "truth.json").read_text())
            verify_images(args.output, truth)
            review = json.loads(args.review.read_text())
            result = grade(truth, review)
            result["source_images_verified"] = True
            result["challenge_version"] = "E002-603"
            print(json.dumps(result, sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(json.dumps({"experiment":"E002-603","status":"ABSTAIN",
                          "error_type":type(e).__name__, "release":"BLOCKED"}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
