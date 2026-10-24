#!/usr/bin/env python3
"""E002-418: local-only synthetic rater challenge; never treat as human aperture truth."""
from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import json
import math
import random
import secrets
import shutil
import struct
import zlib
from pathlib import Path

import e002_407_full_event_pilot as base

CONDITIONS = ("clean", "dark", "bright", "blur", "shift", "gaze",
              "glare", "occlusion", "glasses")
VISIBLE = set(CONDITIONS[:6])
COLUMNS_X = (45, 95, 145)
N = 144
W, H = base.WIDTH, base.HEIGHT


def edge(x, p):
    bend = p["bend"] * (x - 95) ** 2
    return (round(p["upper"] + bend), round(p["lower"] - bend))


def png_gray(pixels):
    """Dependency-free 8-bit grayscale PNG, with no identifying metadata."""
    raw = b"".join(b"\x00" + bytes(row) for row in pixels)
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def render(condition, p):
    out = []
    for y in range(H):
        row = []
        for x in range(W):
            upper, lower = edge(x, p)
            inside = upper <= y <= lower
            v = (65 if inside else 186) + (x + y) % 3
            if inside and (x - (95 + (18 if condition == "gaze" else 0))) ** 2 + (y - 62) ** 2 < 100:
                v = 24
            row.append(v)
        out.append(row)
    if condition == "blur":
        old = out
        out = [[sum(old[yy][xx] for yy in range(max(0, y-1), min(H, y+2))
                    for xx in range(max(0, x-1), min(W, x+2))) //
                ((min(H, y+2)-max(0, y-1)) * (min(W, x+2)-max(0, x-1)))
                for x in range(W)] for y in range(H)]
    if condition in ("dark", "bright"):
        gain = 0.70 if condition == "dark" else 1.30
        out = [[min(255, round(v * gain)) for v in row] for row in out]
    if condition in ("glare", "occlusion"):
        for y in range(28, 101):
            for x in range(20, 171):
                out[y][x] = 255 if condition == "glare" else 0
    if condition == "glasses":
        for y in list(range(33, 55)) + list(range(70, 94)):
            for x in range(20, 171):
                out[y][x] = 22
    return png_gray(out)


def generate(pack_dir, truth_dir, seed=20261024):
    pack_dir, truth_dir = Path(pack_dir).resolve(), Path(truth_dir).resolve()
    if pack_dir.exists() or truth_dir.exists() or pack_dir == truth_dir:
        raise ValueError("New, separate pack and private truth directories required")
    if pack_dir in truth_dir.parents or truth_dir in pack_dir.parents:
        raise ValueError("Private truth must not be inside blinded pack")
    rng = random.Random(seed)
    conditions = list(CONDITIONS) * 16
    rng.shuffle(conditions)
    secret = secrets.token_bytes(32)
    truth, clips = {}, []
    pack_dir.mkdir(parents=True)
    truth_dir.mkdir(parents=True)
    try:
        (pack_dir / "images").mkdir()
        for i in range(4):
            cid = hmac.new(secret, ("E002-418:" + str(i)).encode(), hashlib.sha256).hexdigest()[:20]
            frames = []
            for j in range(36):
                condition = conditions[36*i+j]
                p = {"upper": rng.randint(40, 48), "lower": rng.randint(77, 85),
                     "bend": rng.choice((0.0006, 0.0009, 0.0012))}
                if condition == "shift":
                    p["upper"] += 7
                    p["lower"] += 7
                name = f"{cid}_{j:03d}.png"
                data = render(condition, p)
                (pack_dir / "images" / name).write_bytes(data)
                frames.append({"frame_in_clip": j, "file": name,
                               "sha256": hashlib.sha256(data).hexdigest()})
                truth[f"{cid}:{j}"] = {"condition": condition, "geometry": p}
            clips.append({"clip_id": cid, "frames": frames})
        manifest = {"experiment": "E002-407", "public_linkage_present": False,
                    "crop_width": W, "crop_height": H, "clip_count": 4,
                    "frame_count": N, "clips": clips}
        assert len(base.validate_manifest(manifest)) == N
        manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
        (pack_dir / "blinded_manifest.json").write_bytes(manifest_bytes)
        with (pack_dir / "blank_annotation_sheet.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(base.COLUMNS)
            for clip in clips:
                for frame in clip["frames"]:
                    w.writerow([clip["clip_id"], frame["frame_in_clip"]]
                               + [""] * (len(base.COLUMNS)-2))
        base.validate_sheet(pack_dir / "blinded_manifest.json",
                            pack_dir / "blank_annotation_sheet.csv", blank=True)
        shutil.copyfile(Path(base.__file__).with_name("e002_407_offline_annotator.html"),
                        pack_dir / "annotate_offline.html")
        (truth_dir / "PRIVATE_DO_NOT_SHARE_truth.json").write_text(json.dumps({
            "experiment": "E002-418", "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "cases": truth}, indent=2) + "\n")
    except BaseException:
        shutil.rmtree(pack_dir, ignore_errors=True)
        shutil.rmtree(truth_dir, ignore_errors=True)
        raise
    return {"synthetic_frames": N, "conditions": {c: 16 for c in CONDITIONS},
            "blinded": True, "private_truth_separate": True,
            "human_ratings": 0, "product": "ABSTAIN_UNCALIBRATED"}


def read_truth(pack_dir, truth_file):
    pack_dir = Path(pack_dir)
    raw = (pack_dir / "blinded_manifest.json").read_bytes()
    truth = json.loads(Path(truth_file).read_text())
    if truth.get("experiment") != "E002-418" or hashlib.sha256(raw).hexdigest() != truth.get("manifest_sha256"):
        raise ValueError("Truth and immutable manifest mismatch")
    manifest = json.loads(raw)
    rows = base.validate_manifest(manifest)
    if len(rows) != N or set(truth["cases"]) != {f"{cid}:{i}" for cid, i, _, _ in rows}:
        raise ValueError("Truth coverage mismatch")
    return rows, truth["cases"]


def make_oracle(pack_dir, truth_file, sheet, rater_id="SYNTHETIC_ORACLE", attack="none"):
    rows, cases = read_truth(pack_dir, truth_file)
    with Path(sheet).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=base.COLUMNS)
        w.writeheader()
        for cid, i, _, _ in rows:
            c = cases[f"{cid}:{i}"]
            unresolved = c["condition"] not in VISIBLE
            row = dict.fromkeys(base.COLUMNS, "")
            row.update(clip_id=cid, frame_in_clip=i, rater_id=rater_id,
                       unresolved="1" if unresolved else "0")
            if not unresolved or attack == "overconfident":
                for prefix, x in zip(("left", "center", "right"), COLUMNS_X):
                    upper, lower = edge(x, c["geometry"])
                    for which, y in (("upper", upper), ("lower", lower)):
                        row[f"{prefix}_{which}_x"] = x
                        row[f"{prefix}_{which}_y"] = y + (7 if attack == "shifted" else 0)
                if attack == "overconfident":
                    row["unresolved"] = "0"
            w.writerow(row)
    return base.validate_sheet(Path(pack_dir) / "blinded_manifest.json", sheet)


def score_one(pack_dir, cases, sheet):
    base.validate_sheet(Path(pack_dir) / "blinded_manifest.json", sheet)
    counts = {c: {"total": 0, "pass": 0, "false_confident": 0} for c in CONDITIONS}
    with Path(sheet).open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        c = cases[f'{row["clip_id"]}:{int(row["frame_in_clip"])}']
        condition = c["condition"]
        counts[condition]["total"] += 1
        unresolved = row["unresolved"] == "1"
        if condition not in VISIBLE:
            good = unresolved
            if not good:
                counts[condition]["false_confident"] += 1
        else:
            good = not unresolved
            if good:
                for prefix, target_x in zip(("left", "center", "right"), COLUMNS_X):
                    for which in ("upper", "lower"):
                        x = float(row[f"{prefix}_{which}_x"])
                        y = float(row[f"{prefix}_{which}_y"])
                        expected = edge(x, c["geometry"])[0 if which == "upper" else 1]
                        good = good and abs(x - target_x) <= 5 and abs(y - expected) <= 3
        counts[condition]["pass"] += int(good)
    visible_pass = sum(counts[c]["pass"] for c in VISIBLE)
    hidden_pass = sum(counts[c]["pass"] for c in CONDITIONS if c not in VISIBLE)
    result = {"rater_id": rows[0]["rater_id"], "synthetic_visible_pass": visible_pass,
              "synthetic_visible_total": 96, "obscured_abstain": hidden_pass,
              "obscured_total": 48, "by_condition": counts,
              "qualified_on_synthetic": visible_pass >= 87 and hidden_pass >= 46
              and all(counts[c]["pass"] >= 12 for c in VISIBLE),
              "physical_human_aperture_validated": False,
              "product": "ABSTAIN_UNCALIBRATED"}
    return result


def score(pack_dir, truth_file, sheet_a, sheet_b):
    _, cases = read_truth(pack_dir, truth_file)
    a, b = score_one(pack_dir, cases, sheet_a), score_one(pack_dir, cases, sheet_b)
    if a["rater_id"] == b["rater_id"]:
        raise ValueError("Rater IDs must be distinct; independence must be checked externally")
    return {"raters": [a, b], "joint_synthetic_qualification":
            a["qualified_on_synthetic"] and b["qualified_on_synthetic"],
            "actual_independent_human_raters_authenticated": False,
            "physical_reference_validated": False,
            "product": "ABSTAIN_UNCALIBRATED"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--pack-dir", required=True)
    g.add_argument("--truth-dir", required=True)
    o = sub.add_parser("oracle")
    o.add_argument("--pack-dir", required=True)
    o.add_argument("--truth-file", required=True)
    o.add_argument("--sheet", required=True)
    o.add_argument("--rater-id", default="SYNTHETIC_ORACLE")
    o.add_argument("--attack", choices=("none", "shifted", "overconfident"), default="none")
    s = sub.add_parser("score")
    s.add_argument("--pack-dir", required=True)
    s.add_argument("--truth-file", required=True)
    s.add_argument("--rater-a", required=True)
    s.add_argument("--rater-b", required=True)
    args = p.parse_args()
    if args.command == "generate":
        result = generate(args.pack_dir, args.truth_dir)
    elif args.command == "oracle":
        result = make_oracle(args.pack_dir, args.truth_file, args.sheet, args.rater_id, args.attack)
    else:
        result = score(args.pack_dir, args.truth_file, args.rater_a, args.rater_b)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
