#!/usr/bin/env python3
"""E002-407: local-only full-event human rater pilot. NEVER publish human frames/linkage.

The public manifest and rater pack are *locally* blinded; they are not
anonymized data and must not be uploaded to CI artifacts or public GitHub.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import hmac
import json
import math
import re
import secrets
import shutil
import struct
import tempfile
import zipfile
from pathlib import Path

COLUMNS = [
    "clip_id", "frame_in_clip",
    "left_upper_x", "left_upper_y", "left_lower_x", "left_lower_y",
    "center_upper_x", "center_upper_y", "center_lower_x", "center_lower_y",
    "right_upper_x", "right_upper_y", "right_lower_x", "right_lower_y",
    "occlusion", "glare", "glasses", "blur", "gaze_issue",
    "unresolved", "rater_id", "notes",
]
POINTS = ["left_upper", "left_lower", "center_upper", "center_lower",
          "right_upper", "right_lower"]
FLAGS = ["occlusion", "glare", "glasses", "blur", "gaze_issue", "unresolved"]
CLIP_ID = re.compile(r"[a-f0-9]{20}\Z")
PNG_NAME = re.compile(r"([a-f0-9]{20})_([0-9]{3})\.png\Z")
DIGEST = re.compile(r"[a-f0-9]{64}\Z")
N_PAIRS = 2
WIDTH, HEIGHT = 190, 130


def validate_manifest(manifest):
    if (manifest.get("experiment") != "E002-407"
            or manifest.get("public_linkage_present") is not False
            or manifest.get("crop_width") != WIDTH
            or manifest.get("crop_height") != HEIGHT):
        raise ValueError("Invalid or unsafe E002-407 manifest")
    clips = manifest.get("clips")
    if not isinstance(clips, list) or len(clips) != 2 * N_PAIRS:
        raise ValueError("Expected exactly four pilot clips")
    rows, seen_ids, seen_files = [], set(), set()
    for clip in clips:
        cid, frames = clip.get("clip_id"), clip.get("frames")
        if not isinstance(cid, str) or not CLIP_ID.fullmatch(cid) or cid in seen_ids:
            raise ValueError("Invalid or duplicate blinded clip ID")
        seen_ids.add(cid)
        if not isinstance(frames, list) or not 30 <= len(frames) <= 200:
            raise ValueError("Invalid full-event frame count")
        indices = set()
        for frame in frames:
            n, name, digest = (frame.get("frame_in_clip"), frame.get("file"),
                               frame.get("sha256"))
            if (not isinstance(n, int) or isinstance(n, bool)
                    or n < 0 or n >= len(frames) or n in indices):
                raise ValueError("Duplicate or invalid frame index")
            indices.add(n)
            if (not isinstance(name, str) or not PNG_NAME.fullmatch(name)
                    or name != f"{cid}_{n:03d}.png" or name in seen_files):
                raise ValueError("Unsafe or duplicate PNG filename")
            seen_files.add(name)
            if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
                raise ValueError("Invalid PNG digest")
            if set(frame) != {"frame_in_clip", "file", "sha256"}:
                raise ValueError("Unexpected frame metadata in blinded manifest")
            rows.append((cid, n, name, digest))
        if indices != set(range(len(frames))):
            raise ValueError("Missing frame index")
        if set(clip) != {"clip_id", "frames"}:
            raise ValueError("Unexpected clip metadata in blinded manifest")
    if manifest.get("clip_count") != len(clips) or manifest.get("frame_count") != len(rows):
        raise ValueError("Manifest totals inconsistent")
    forbidden = ("participant", "marker", "control", "arm", "source_time",
                 "eeg", "source_frame", "pair_index", "linkage", "key_hex")
    # Check keys, not string values such as 'no EEG linkage'.
    def walk(v):
        if isinstance(v, dict):
            for k, val in v.items():
                if k != "public_linkage_present" and any(term in k.lower() for term in forbidden):
                    raise ValueError(f"Forbidden private manifest key: {k}")
                walk(val)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(manifest)
    return rows


def png_dimensions(path):
    with path.open("rb") as f:
        header = f.read(24)
    if (len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n"
            or header[12:16] != b"IHDR"):
        raise ValueError("Invalid PNG header")
    return struct.unpack(">II", header[16:24])


def validate_sheet(manifest_path, sheet_path, *, blank=False):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    expected = {(cid, str(n)) for cid, n, _, _ in validate_manifest(manifest)}
    with Path(sheet_path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise ValueError("Unexpected CSV columns")
        seen, raters, unresolved = set(), set(), 0
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError("Malformed CSV row")
            key = (row["clip_id"], row["frame_in_clip"])
            if key not in expected or key in seen:
                raise ValueError("Missing/duplicate/unexpected frame")
            seen.add(key)
            if blank:
                if any(row[k] for k in COLUMNS[2:]):
                    raise ValueError("Nonblank template")
                continue
            rater = row["rater_id"].strip()
            if not rater or len(rater) > 80:
                raise ValueError("Missing or invalid rater ID")
            raters.add(rater)
            if len(row["notes"]) > 2000:
                raise ValueError("Oversized notes")
            for flag in FLAGS:
                if row[flag] not in ("", "0", "1"):
                    raise ValueError("Invalid nuisance flag")
            is_unresolved = row["unresolved"] == "1"
            unresolved += is_unresolved
            for p in POINTS:
                x, y = row[p + "_x"].strip(), row[p + "_y"].strip()
                if not x and not y and is_unresolved:
                    continue
                if not x or not y:
                    raise ValueError("Incomplete landmark")
                a, b = float(x), float(y)
                if not (math.isfinite(a) and math.isfinite(b)
                        and 0 <= a < WIDTH and 0 <= b < HEIGHT):
                    raise ValueError("Nonfinite/out-of-bounds landmark")
        if seen != expected or (not blank and len(raters) != 1):
            raise ValueError("Incomplete sheet or inconsistent rater ID")
    return {"frames": len(seen), "unresolved": unresolved,
            "rater_id": next(iter(raters)) if raters else None}


def make_pack(public_dir, private_dir, output_dir):
    public_dir, private_dir, output_dir = (
        Path(p).resolve() for p in (public_dir, private_dir, output_dir))
    if output_dir.exists():
        raise ValueError("Output exists; no overwrites")
    if (output_dir == private_dir or output_dir == public_dir
            or private_dir in output_dir.parents or output_dir in private_dir.parents
            or public_dir in output_dir.parents or output_dir in public_dir.parents):
        raise ValueError("Output must be isolated from private/public source")
    manifest = public_dir / "blinded_manifest.json"
    rows = validate_manifest(json.loads(manifest.read_text(encoding="utf-8")))
    sheet = public_dir / "blank_annotation_sheet.csv"
    validate_sheet(manifest, sheet, blank=True)
    sources = []
    for _, _, name, digest in rows:
        source = private_dir / name
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Missing or symlinked PNG {name}")
        if png_dimensions(source) != (WIDTH, HEIGHT):
            raise ValueError(f"Wrong image geometry {name}")
        if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
            raise ValueError(f"PNG SHA-256 mismatch {name}")
        sources.append((source, name))
    html = Path(__file__).with_name("e002_407_offline_annotator.html")
    if not html.is_file():
        raise ValueError("Missing E002-407 offline UI")
    output_dir.mkdir(parents=True)
    try:
        (output_dir / "images").mkdir()
        shutil.copyfile(manifest, output_dir / "blinded_manifest.json")
        shutil.copyfile(sheet, output_dir / "blank_annotation_sheet.csv")
        shutil.copyfile(html, output_dir / "annotate_offline.html")
        for source, name in sources:
            shutil.copyfile(source, output_dir / "images" / name)
    except BaseException:
        shutil.rmtree(output_dir)
        raise
    return {"clips": 4, "frames": len(rows), "local_only": True}


def generate(archive, participant, public_dir, private_dir):
    import cv2
    import e002_397_human_motion as prior
    import e002_398_blinded_annotation as blind
    import e002_406_human_window_adequacy as windows

    archive, public_dir, private_dir = map(Path, (archive, public_dir, private_dir))
    if public_dir.exists() or private_dir.exists():
        raise ValueError("Output directories must not exist; do not overwrite evidence")
    if public_dir.resolve() == private_dir.resolve():
        raise ValueError("Public and private output must differ")
    if prior.prior.md5(archive) != prior.MD5[participant]:
        raise ValueError("Source archive checksum mismatch")
    with zipfile.ZipFile(archive) as z:
        video, frames, markers = prior.load_archive(z, participant)
        pairs, _ = prior.select_pairs(frames, markers, participant)
        selected = blind.selected_pairs(pairs)
        times, ids = [t for _, t in frames], [f for f, _ in frames]
        complete = []
        for pair_index, (k, j) in selected:
            if (windows.evaluate_window(times, ids, k)["eligible"]
                    and windows.evaluate_window(times, ids, j)["eligible"]):
                complete.append((pair_index, k, j))
        if len(complete) < N_PAIRS:
            raise ValueError("Insufficient complete event/control pairs")
        chosen = complete[:N_PAIRS]
        secret = secrets.token_bytes(32)
        needed, linkage, clips = {}, {}, {}
        for pair_index, k, j in chosen:
            for arm, center in (("marker", k), ("control", j)):
                left = bisect.bisect_right(times, times[center] - .25) - 1
                right = bisect.bisect_left(times, times[center] + .25)
                assert windows.evaluate_window(times, ids, center)["eligible"]
                assert times[right] - times[left] >= .5
                cid = hmac.new(secret, f"e002-407:{participant}:{pair_index}:{arm}".encode(),
                               hashlib.sha256).hexdigest()[:20]
                if cid in clips:
                    raise RuntimeError("Blinded clip ID collision")
                clips[cid] = {}
                linkage[cid] = {
                    "participant": participant, "pair_index": pair_index,
                    "arm": arm, "center_frame_index": center,
                    "source_frame_indices": list(range(left, right + 1)),
                    "source_frame_ids": ids[left:right + 1],
                    "eeg_clock_times_s": times[left:right + 1],
                }
                for n, idx in enumerate(range(left, right + 1)):
                    needed.setdefault(idx, []).append((cid, n))
        public_dir.mkdir(parents=True)
        private_dir.mkdir(parents=True)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                avi = Path(tmp) / "eye.avi"
                with z.open(video) as src, avi.open("wb") as dst:
                    shutil.copyfileobj(src, dst, 1 << 20)
                cap = cv2.VideoCapture(str(avi))
                if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != len(frames):
                    raise RuntimeError("Video decode/frame-count mismatch")
                count = 0
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break
                    if count in needed:
                        if frame.shape[:2] != (288, 320):
                            raise RuntimeError("Unexpected source frame geometry")
                        crop = frame[90:220, 70:260]
                        for cid, n in needed[count]:
                            name = f"{cid}_{n:03d}.png"
                            path = private_dir / name
                            if not cv2.imwrite(str(path), crop):
                                raise RuntimeError("Cannot save cropped frame")
                            clips[cid][n] = {"frame_in_clip": n, "file": name,
                                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                    count += 1
                cap.release()
                if count != len(frames):
                    raise RuntimeError("Incomplete source decode")
            public_clips = [
                {"clip_id": cid, "frames": [clips[cid][i] for i in range(len(clips[cid]))]}
                for cid in sorted(clips)
            ]
            manifest = {
                "experiment": "E002-407", "public_linkage_present": False,
                "crop_width": WIDTH, "crop_height": HEIGHT,
                "clip_count": len(public_clips),
                "frame_count": sum(len(c["frames"]) for c in public_clips),
                "clips": public_clips,
            }
            validate_manifest(manifest)
            (public_dir / "blinded_manifest.json").write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            with (public_dir / "blank_annotation_sheet.csv").open(
                    "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(COLUMNS)
                for c in public_clips:
                    for frame in c["frames"]:
                        writer.writerow([c["clip_id"], frame["frame_in_clip"]]
                                        + [""] * (len(COLUMNS) - 2))
            validate_sheet(public_dir / "blinded_manifest.json",
                           public_dir / "blank_annotation_sheet.csv", blank=True)
            (private_dir / "PRIVATE_DO_NOT_UPLOAD_linkage.json").write_text(
                json.dumps({"source_md5": prior.MD5[participant],
                            "key_hex": secret.hex(), "linkage": linkage}, indent=2))
        except BaseException:
            shutil.rmtree(public_dir, ignore_errors=True)
            shutil.rmtree(private_dir, ignore_errors=True)
            raise
    return {"experiment": "E002-407", "participant": participant,
            "complete_pairs_available": len(complete), "pilot_pairs": N_PAIRS,
            "blinded_clips": 2 * N_PAIRS, "frames": manifest["frame_count"],
            "source_checksum_verified": True, "local_only": True,
            "physical_aperture_ground_truth": False,
            "product": "ABSTAIN_UNCALIBRATED"}


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate")
    gen.add_argument("--archive", type=Path, required=True)
    gen.add_argument("--participant", choices=["S01", "S19"], required=True)
    gen.add_argument("--public-dir", type=Path, required=True)
    gen.add_argument("--private-dir", type=Path, required=True)
    pack = sub.add_parser("pack")
    pack.add_argument("--public-dir", type=Path, required=True)
    pack.add_argument("--private-dir", type=Path, required=True)
    pack.add_argument("--output-dir", type=Path, required=True)
    check = sub.add_parser("check")
    check.add_argument("--manifest", type=Path, required=True)
    check.add_argument("--sheet", type=Path, required=True)
    a = p.parse_args()
    if a.command == "generate":
        result = generate(a.archive, a.participant, a.public_dir, a.private_dir)
    elif a.command == "pack":
        result = make_pack(a.public_dir, a.private_dir, a.output_dir)
    else:
        result = validate_sheet(a.manifest, a.sheet)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
