#!/usr/bin/env python3
"""E002-404: offline rater packager and independent CSV validator.

No network access or EEG marker/control linkage. Only manifest-listed PNGs are copied.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import struct
from pathlib import Path

COLUMNS = [
    "clip_id", "frame_in_clip",
    "left_upper_x", "left_upper_y", "left_lower_x", "left_lower_y",
    "center_upper_x", "center_upper_y", "center_lower_x", "center_lower_y",
    "right_upper_x", "right_upper_y", "right_lower_x", "right_lower_y",
    "occlusion", "glare", "glasses", "blur", "gaze_issue",
    "unresolved", "rater_id", "notes",
]
POINTS = [
    "left_upper", "left_lower", "center_upper", "center_lower",
    "right_upper", "right_lower",
]
FLAGS = ["occlusion", "glare", "glasses", "blur", "gaze_issue", "unresolved"]
FILENAME = re.compile(r"^[a-f0-9]{20}_[0-6]{2}\.png$")
CLIP_ID = re.compile(r"^[a-f0-9]{20}$")


def manifest_rows(manifest):
    if manifest.get("experiment") != "E002-398" or manifest.get("public_linkage_present") is not False:
        raise ValueError("Not a public-safe E002-398 manifest")
    width, height = manifest.get("crop_width"), manifest.get("crop_height")
    if (width, height) != (190, 130):
        raise ValueError("Unexpected crop dimensions")
    clips = manifest.get("clips")
    if not isinstance(clips, list) or not clips:
        raise ValueError("No clips")
    rows = []
    ids, names = set(), set()
    for clip in clips:
        clip_id = clip.get("clip_id")
        if not isinstance(clip_id, str) or not CLIP_ID.fullmatch(clip_id) or clip_id in ids:
            raise ValueError("Invalid or duplicate blinded clip ID")
        ids.add(clip_id)
        frames = clip.get("frames")
        if not isinstance(frames, list) or len(frames) != 7:
            raise ValueError("Each clip must contain exactly seven frames")
        seen = set()
        for frame in frames:
            n = frame.get("frame_in_clip")
            filename = frame.get("file")
            digest = frame.get("sha256")
            if not isinstance(n, int) or isinstance(n, bool) or n not in range(7) or n in seen:
                raise ValueError("Invalid or duplicate frame number")
            seen.add(n)
            if not isinstance(filename, str) or not FILENAME.fullmatch(filename) or filename != f"{clip_id}_{n:02d}.png" or filename in names:
                raise ValueError("Unsafe, unexpected or duplicate image name")
            names.add(filename)
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError("Invalid PNG digest")
            rows.append((clip_id, n, filename, digest))
    if len(rows) != manifest.get("frame_count") or len(clips) != manifest.get("clip_count"):
        raise ValueError("Manifest totals inconsistent")
    return rows


def png_dimensions(path):
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Invalid PNG header: {path.name}")
    return struct.unpack(">II", header[16:24])


def make_pack(public_dir, private_dir, output_dir):
    public_dir, private_dir, output_dir = map(lambda p: Path(p).resolve(), (public_dir, private_dir, output_dir))
    if output_dir.exists():
        raise ValueError("Output directory must not exist; never overwrite a rater pack")
    if output_dir == private_dir or private_dir in output_dir.parents or output_dir in private_dir.parents:
        raise ValueError("Output directory cannot overlap private source")
    manifest_path = public_dir / "blinded_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest_rows(manifest)
    source_images = []
    for _, _, filename, digest in rows:
        path = private_dir / filename
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Missing or symlinked PNG: {filename}")
        if png_dimensions(path) != (190, 130):
            raise ValueError(f"Wrong PNG dimensions: {filename}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"SHA256 mismatch: {filename}")
        source_images.append((path, filename))
    sheet = public_dir / "blank_annotation_sheet.csv"
    with sheet.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise ValueError("Unexpected annotation sheet columns")
        keys = [(r["clip_id"], int(r["frame_in_clip"])) for r in reader]
        if len(keys) != len(rows) or set(keys) != {(c, n) for c, n, _, _ in rows}:
            raise ValueError("Blank sheet does not match manifest")
    # Only copy whitelisted files; NEVER private linkage or source videos.
    annotator = Path(__file__).with_name("e002_404_offline_annotator.html")
    if not annotator.is_file():
        raise ValueError("Missing offline annotator HTML next to packager")
    output_dir.mkdir(parents=True)
    try:
        (output_dir / "images").mkdir()
        shutil.copyfile(manifest_path, output_dir / "blinded_manifest.json")
        shutil.copyfile(sheet, output_dir / "blank_annotation_sheet.csv")
        shutil.copyfile(annotator, output_dir / "annotate_offline.html")
        for path, filename in source_images:
            shutil.copyfile(path, output_dir / "images" / filename)
    except BaseException:
        shutil.rmtree(output_dir)
        raise
    return {"clips": len(manifest["clips"]), "frames": len(rows), "path": str(output_dir)}


def validate_sheet(manifest_path, sheet_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    expected = {(c, str(n)) for c, n, _, _ in manifest_rows(manifest)}
    with Path(sheet_path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise ValueError("Incorrect CSV columns/order")
        seen, raters, unresolved_count = set(), set(), 0
        for row in reader:
            if None in row:
                raise ValueError("Extra CSV columns")
            key = (row["clip_id"], row["frame_in_clip"])
            if key not in expected or key in seen:
                raise ValueError("Unexpected or duplicate frame")
            seen.add(key)
            rater = row["rater_id"].strip()
            if not rater or len(rater) > 80:
                raise ValueError("Missing or invalid rater ID")
            raters.add(rater)
            if len(row["notes"]) > 2000:
                raise ValueError("Excessive notes length")
            for flag in FLAGS:
                if row[flag] not in ("", "0", "1"):
                    raise ValueError(f"Invalid flag {flag}")
            unresolved = row["unresolved"] == "1"
            if unresolved:
                unresolved_count += 1
            for point in POINTS:
                x, y = row[point + "_x"].strip(), row[point + "_y"].strip()
                if not x and not y and unresolved:
                    continue
                if not x or not y:
                    raise ValueError("Incomplete landmark pair")
                a, b = float(x), float(y)
                if not math.isfinite(a) or not math.isfinite(b) or not (0 <= a < 190 and 0 <= b < 130):
                    raise ValueError("Nonfinite or out-of-bounds landmark")
        if seen != expected or len(raters) != 1:
            raise ValueError("Incomplete sheet or inconsistent rater ID")
    return {"frames": len(seen), "unresolved": unresolved_count, "rater_id": next(iter(raters))}


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    pack = sub.add_parser("pack")
    pack.add_argument("--public-dir", type=Path, required=True)
    pack.add_argument("--private-dir", type=Path, required=True)
    pack.add_argument("--output-dir", type=Path, required=True)
    check = sub.add_parser("check")
    check.add_argument("--manifest", type=Path, required=True)
    check.add_argument("--sheet", type=Path, required=True)
    args = p.parse_args()
    result = make_pack(args.public_dir, args.private_dir, args.output_dir) if args.command == "pack" else validate_sheet(args.manifest, args.sheet)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
