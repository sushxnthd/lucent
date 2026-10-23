#!/usr/bin/env python3
"""Independent public/private separation and frame integrity oracle for E002-398."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import cv2

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--public-dir", type=Path, required=True)
    p.add_argument("--private-dir", type=Path, required=True)
    args = p.parse_args()
    data = json.loads((args.public_dir / "blinded_manifest.json").read_text())
    summary = json.loads((args.public_dir / "summary.json").read_text())
    assert data["clip_count"] == 40 and data["frame_count"] == 280
    assert summary["selected_pairs"] == 20 and summary["cropped_frames"] == 280
    assert summary["actual_aperture_annotations"] == 0
    assert not data["public_linkage_present"]
    ids = set()
    expected = set()
    for clip in data["clips"]:
        ident = clip["clip_id"]
        assert re.fullmatch(r"[a-f0-9]{20}", ident)
        assert ident not in ids
        ids.add(ident)
        assert len(clip["frames"]) == 7
        for i, rec in enumerate(clip["frames"]):
            assert rec["frame_in_clip"] == i
            assert rec["file"] == f"{ident}_{i:02d}.png"
            expected.add(rec["file"])
            path = args.private_dir / rec["file"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == rec["sha256"]
            img = cv2.imread(str(path))
            assert img is not None and img.shape[:2] == (130, 190)
            assert all(0 <= rec[k] for k in (
                "laplacian_variance", "saturation_fraction", "contrast_p95_minus_p05"))
            assert rec["saturation_fraction"] <= 1
    assert {x.name for x in args.private_dir.glob("*.png")} == expected
    with (args.public_dir / "blank_annotation_sheet.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 280
    assert {(r["clip_id"], int(r["frame_in_clip"])) for r in rows} == {
        (c["clip_id"], i) for c in data["clips"] for i in range(7)}
    assert all(not any(v for k, v in row.items() if k not in
                       ("clip_id", "frame_in_clip")) for row in rows)
    public_text = "".join(p.read_text() for p in args.public_dir.iterdir() if p.is_file())
    for forbidden in ("PRIVATE_DO_NOT_UPLOAD", "key_hex", "center_phantom_frame_id",
                      "center_eeg_clock_time", '"arm":', '"pair_index":',
                      "fef02cb7ebf62e4f3efb6303284fd6cb",
                      "8a16cf12526f7558b4e49926c4bc5e8e"):
        assert forbidden not in public_text, f"Public linkage leak: {forbidden}"
    linkage = json.loads((args.private_dir / "PRIVATE_DO_NOT_UPLOAD_linkage.json").read_text())
    assert len(linkage["key_hex"]) == 64
    assert set(linkage["linkage"]) == ids
    assert sum(v["arm"] == "marker" for v in linkage["linkage"].values()) == 20
    assert sum(v["arm"] == "control" for v in linkage["linkage"].values()) == 20
    print(json.dumps({"independent_checks_passed": True, "clips": 40,
                      "frames": 280, "no_public_linkage": True,
                      "physical_validation": False}))

if __name__ == "__main__":
    main()
