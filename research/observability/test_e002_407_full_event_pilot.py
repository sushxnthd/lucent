#!/usr/bin/env python3
"""E002-407 independent synthetic privacy, integrity and rater-sheet tests."""
import csv
import hashlib
import json
import shutil
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import e002_407_full_event_pilot as pilot


def png(width=190, height=130):
    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))
    pixels = (b"\x00" + b"\x7f\x7f\x7f" * width) * height
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(pixels))
            + chunk(b"IEND", b""))


class FullEventPilotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.pub, self.priv, self.out = root / "public", root / "private", root / "pack"
        self.pub.mkdir()
        self.priv.mkdir()
        data = png()
        digest = hashlib.sha256(data).hexdigest()
        clips = []
        for c in range(4):
            cid = f"{c + 1:020x}"
            frames = []
            for n in range(30):
                name = f"{cid}_{n:03d}.png"
                (self.priv / name).write_bytes(data)
                frames.append({"frame_in_clip": n, "file": name, "sha256": digest})
            clips.append({"clip_id": cid, "frames": frames})
        self.manifest = {
            "experiment": "E002-407", "public_linkage_present": False,
            "crop_width": 190, "crop_height": 130,
            "clip_count": 4, "frame_count": 120, "clips": clips,
        }
        self.manifest_path = self.pub / "blinded_manifest.json"
        self.save_manifest()
        self.sheet = self.pub / "blank_annotation_sheet.csv"
        with self.sheet.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(pilot.COLUMNS)
            for clip in clips:
                for frame in clip["frames"]:
                    writer.writerow([clip["clip_id"], frame["frame_in_clip"]]
                                    + [""] * (len(pilot.COLUMNS) - 2))
        (self.priv / "PRIVATE_DO_NOT_UPLOAD_linkage.json").write_text(
            '{"arm":"marker","eeg_clock_times_s":[0.0]}')

    def save_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def filled_sheet(self):
        path = self.pub / "rater.csv"
        with self.sheet.open(newline="") as f:
            rows = list(csv.DictReader(f))
        for row in rows:
            for p in pilot.POINTS:
                row[p + "_x"] = "80.5"
                row[p + "_y"] = "60.0"
            row["rater_id"] = "blind_rater_A"
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=pilot.COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_01_valid_blinded_manifest_and_blank_sheet(self):
        self.assertEqual(len(pilot.validate_manifest(self.manifest)), 120)
        self.assertEqual(pilot.validate_sheet(self.manifest_path, self.sheet, blank=True)["frames"], 120)

    def test_02_pack_is_whitelist_only(self):
        result = pilot.make_pack(self.pub, self.priv, self.out)
        self.assertEqual(result["frames"], 120)
        self.assertEqual(len(list((self.out / "images").glob("*.png"))), 120)
        self.assertFalse(any("PRIVATE" in str(p) for p in self.out.rglob("*")))
        self.assertTrue((self.out / "annotate_offline.html").is_file())

    def test_03_detect_png_tampering(self):
        target = self.priv / self.manifest["clips"][0]["frames"][0]["file"]
        target.write_bytes(target.read_bytes() + b"tamper")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            pilot.make_pack(self.pub, self.priv, self.out)

    def test_04_reject_private_metadata(self):
        self.manifest["clips"][0]["arm"] = "marker"
        with self.assertRaises(ValueError):
            pilot.validate_manifest(self.manifest)

    def test_05_reject_duplicate_or_missing_frame(self):
        self.manifest["clips"][0]["frames"][0]["frame_in_clip"] = 1
        with self.assertRaises(ValueError):
            pilot.validate_manifest(self.manifest)

    def test_06_reject_unsafe_filename(self):
        self.manifest["clips"][0]["frames"][0]["file"] = "../../leak.png"
        with self.assertRaises(ValueError):
            pilot.validate_manifest(self.manifest)

    def test_07_completed_rater_sheet(self):
        rater = self.filled_sheet()
        self.assertEqual(pilot.validate_sheet(self.manifest_path, rater)["frames"], 120)

    def test_08_reject_bad_landmark(self):
        rater = self.filled_sheet()
        s = rater.read_text()
        rater.write_text(s.replace("80.5", "nan", 1))
        with self.assertRaises(ValueError):
            pilot.validate_sheet(self.manifest_path, rater)

    def test_09_reject_missing_sheet_row(self):
        rater = self.filled_sheet()
        lines = rater.read_text().splitlines()
        rater.write_text("\n".join(lines[:-1]) + "\n")
        with self.assertRaises(ValueError):
            pilot.validate_sheet(self.manifest_path, rater)

    def test_10_unresolved_without_points_allowed(self):
        rater = self.filled_sheet()
        with rater.open(newline="") as f:
            rows = list(csv.DictReader(f))
        rows[0]["unresolved"] = "1"
        for p in pilot.POINTS:
            rows[0][p + "_x"] = rows[0][p + "_y"] = ""
        with rater.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=pilot.COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        self.assertEqual(pilot.validate_sheet(self.manifest_path, rater)["unresolved"], 1)

    def test_11_reject_existing_pack_output(self):
        self.out.mkdir()
        with self.assertRaises(ValueError):
            pilot.make_pack(self.pub, self.priv, self.out)

    def test_12_reject_wrong_png_geometry(self):
        target = self.priv / self.manifest["clips"][0]["frames"][0]["file"]
        target.write_bytes(png(189, 130))
        with self.assertRaisesRegex(ValueError, "geometry"):
            pilot.make_pack(self.pub, self.priv, self.out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
