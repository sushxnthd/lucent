#!/usr/bin/env python3
"""E002-404 deterministic fixture tests. Synthetic pixels only; no human images."""
import csv
import hashlib
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from e002_404_rater_pack import COLUMNS, make_pack, validate_sheet


def png(width=190, height=130):
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
    raw = b"".join(b"\x00" + b"\x80" * width for _ in range(height))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


class RaterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.public = self.root / "public"
        self.private = self.root / "private"
        self.public.mkdir()
        self.private.mkdir()
        self.clip = "1234567890abcdef1234"
        self.rows = []
        frames = []
        for n in range(7):
            name = f"{self.clip}_{n:02d}.png"
            payload = png()
            (self.private / name).write_bytes(payload)
            frames.append({"frame_in_clip": n, "file": name, "sha256": hashlib.sha256(payload).hexdigest()})
            self.rows.append((self.clip, str(n)))
        self.manifest = {
            "experiment": "E002-398", "public_linkage_present": False,
            "crop_width": 190, "crop_height": 130, "clip_count": 1,
            "frame_count": 7, "clips": [{"clip_id": self.clip, "frames": frames}],
        }
        (self.public / "blinded_manifest.json").write_text(json.dumps(self.manifest))
        self.sheet = self.public / "blank_annotation_sheet.csv"
        self.write_sheet(self.sheet, annotated=False)
        (self.private / "PRIVATE_DO_NOT_UPLOAD_linkage.json").write_text('{"arm":"marker","source_id":"SECRET"}')

    def write_sheet(self, path, annotated=True, unresolved=False):
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            for clip, n in self.rows:
                row = dict.fromkeys(COLUMNS, "")
                row.update(clip_id=clip, frame_in_clip=n, rater_id="independent_rater_A")
                if annotated:
                    for part in ("left", "center", "right"):
                        row[f"{part}_upper_x"] = "50.125"
                        row[f"{part}_upper_y"] = "35.25"
                        row[f"{part}_lower_x"] = "50.125"
                        row[f"{part}_lower_y"] = "46.25"
                    for flag in ("occlusion", "glare", "glasses", "blur", "gaze_issue"):
                        row[flag] = "0"
                    row["unresolved"] = "0"
                if unresolved and n == "3":
                    for k in COLUMNS:
                        if k.endswith("_x") or k.endswith("_y"):
                            row[k] = ""
                    row["unresolved"] = "1"
                writer.writerow(row)

    def test_pack_whitelist_and_hashes(self):
        result = make_pack(self.public, self.private, self.root / "rater_pack")
        self.assertEqual((result["clips"], result["frames"]), (1, 7))
        self.assertEqual(len(list((self.root / "rater_pack" / "images").glob("*.png"))), 7)
        self.assertFalse((self.root / "rater_pack" / "PRIVATE_DO_NOT_UPLOAD_linkage.json").exists())
        self.assertFalse((self.root / "rater_pack" / "images" / "PRIVATE_DO_NOT_UPLOAD_linkage.json").exists())

    def test_pack_rejects_tampered_pixels(self):
        path = self.private / f"{self.clip}_00.png"
        path.write_bytes(path.read_bytes() + b"tampered")
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            make_pack(self.public, self.private, self.root / "rater_pack")

    def test_pack_rejects_dimensions(self):
        path = self.private / f"{self.clip}_00.png"
        payload = png(189, 130)
        path.write_bytes(payload)
        self.manifest["clips"][0]["frames"][0]["sha256"] = hashlib.sha256(payload).hexdigest()
        (self.public / "blinded_manifest.json").write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError, "dimensions"):
            make_pack(self.public, self.private, self.root / "rater_pack")

    def test_pack_rejects_path_overlap(self):
        with self.assertRaises(ValueError):
            make_pack(self.public, self.private, self.private / "pack")

    def test_pack_rejects_duplicate_manifest(self):
        self.manifest["clips"][0]["frames"][1] = self.manifest["clips"][0]["frames"][0]
        (self.public / "blinded_manifest.json").write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError, "duplicate frame"):
            make_pack(self.public, self.private, self.root / "rater_pack")

    def test_valid_completed_sheet(self):
        path = self.root / "rater_A.csv"
        self.write_sheet(path)
        self.assertEqual(validate_sheet(self.public / "blinded_manifest.json", path)["frames"], 7)

    def test_unresolved_frame_permitted(self):
        path = self.root / "rater_A.csv"
        self.write_sheet(path, unresolved=True)
        self.assertEqual(validate_sheet(self.public / "blinded_manifest.json", path)["unresolved"], 1)

    def test_missing_landmark_rejected(self):
        path = self.root / "rater_A.csv"
        self.write_sheet(path)
        rows = list(csv.DictReader(path.open()))
        rows[0]["center_upper_x"] = ""
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(ValueError, "Incomplete landmark"):
            validate_sheet(self.public / "blinded_manifest.json", path)

    def test_missing_frame_rejected(self):
        path = self.root / "rater_A.csv"
        self.write_sheet(path)
        rows = list(csv.DictReader(path.open()))[:-1]
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(ValueError, "Incomplete sheet"):
            validate_sheet(self.public / "blinded_manifest.json", path)

    def test_out_of_bounds_rejected(self):
        path = self.root / "rater_A.csv"
        self.write_sheet(path)
        rows = list(csv.DictReader(path.open()))
        rows[0]["center_lower_y"] = "130"
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(ValueError, "out-of-bounds"):
            validate_sheet(self.public / "blinded_manifest.json", path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
