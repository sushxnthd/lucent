#!/usr/bin/env python3
"""E002-497: static offline-interface and E002-492 schema integration tests.

These tests do NOT constitute real human ratings or browser usability testing.
"""
import copy
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from e002_492_anatomical_review import build_manifest, template, validate_frame, adjudicate

HERE = Path(__file__).resolve().parent
HTML = HERE / "e002_497_offline_rater.html"


class OfflineRaterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML.read_text(encoding="utf-8")

    def test_no_network_or_external_resource(self):
        h = self.html
        self.assertIn("connect-src 'none'", h)
        self.assertIn("default-src 'none'", h)
        self.assertIn("img-src blob:", h)
        self.assertNotRegex(h, r"<script[^>]+src=|<link[^>]+href=")
        self.assertNotRegex(h, r"\b(fetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon)\b")

    def test_one_inline_script_parses_in_node(self):
        scripts = re.findall(r"<script>([\s\S]*?)</script>", self.html)
        self.assertEqual(len(scripts), 1)
        if not shutil.which("node"):
            self.skipTest("Node not available")
        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "rater.js"
            script.write_text(scripts[0], encoding="utf-8")
            result = subprocess.run(["node", "--check", str(script)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_strict_blinded_template_schema(self):
        a = template(build_manifest(), "A")
        self.assertEqual(a["experiment"], "E002-492")
        self.assertEqual(len(a["clips"]), 20)
        self.assertEqual(sum(map(len, a["clips"].values())), 260)
        self.assertTrue(all(
            frame["flags"] == ["UNREVIEWED"] and
            all(frame[k] is None for k in
                ("upper_y", "lower_y", "iris_diameter", "uncertainty_px"))
            for frames in a["clips"].values() for frame in frames))
        for token in ("UNREVIEWED", "E002-492", "iris_diameter",
                      "uncertainty_px", "clip_", "320", "288"):
            self.assertIn(token, self.html)

    def test_valid_exported_geometry_accepted_by_existing_adjudicator(self):
        manifest = build_manifest()
        a, b = template(manifest, "A"), template(manifest, "B")
        key = sorted(a["clips"])[0]
        for t in (a, b):
            t["clips"][key][0] = {
                "frame": 0, "upper_y": 80.0, "lower_y": 94.0,
                "iris_diameter": 48.0, "uncertainty_px": 1.0,
                "flags": [],
            }
        result = adjudicate(manifest, a, b)
        self.assertEqual(result["dual_measurable"], 1)
        self.assertEqual(result["unreviewed"], 259)
        self.assertEqual(result["interval_disagreement"], 0)
        self.assertEqual(result["release"], "BLOCKED")
        self.assertFalse(result["physical_hidden_closure_certified"])

    def test_nuisance_flag_abstains_in_existing_adjudicator(self):
        manifest = build_manifest()
        a, b = template(manifest, "A"), template(manifest, "B")
        key = sorted(a["clips"])[0]
        for t in (a, b):
            t["clips"][key][0]["flags"] = ["MISSING_ANATOMY"]
        result = adjudicate(manifest, a, b)
        self.assertEqual(result["dual_measurable"], 0)
        self.assertEqual(result["nuisance_abstention"], 1)
        self.assertEqual(result["release"], "BLOCKED")

    def test_invalid_geometry_does_not_silently_become_measurement(self):
        f = {"frame": 0, "upper_y": 100, "lower_y": 90,
             "iris_diameter": 48, "uncertainty_px": 1, "flags": []}
        measurement, reason = validate_frame(f, 0)
        self.assertIsNone(measurement)
        self.assertEqual(reason, "INVALID_GEOMETRY")

    def test_export_requires_explicit_260_frame_completion(self):
        self.assertIn("progress()!==260", self.html)
        self.assertIn("Exactly 260 private PNGs required", self.html)
        self.assertIn("Duplicate filename", self.html)
        self.assertIn("Missing expected frame", self.html)
        self.assertIn("Two ordered same-column lid points", self.html)

    def test_owner_mapping_not_read_by_interface(self):
        self.assertNotIn("OWNER_ONLY_MAPPING", self.html)
        self.assertIn("Wrong E002-492 template", self.html)
        self.assertIn("private", self.html.lower())


if __name__ == "__main__":
    unittest.main()
