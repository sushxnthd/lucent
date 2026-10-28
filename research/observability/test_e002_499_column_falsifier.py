#!/usr/bin/env python3
"""E002-499 preregistered geometric falsification and rater column checks."""
import re
import shutil
import subprocess
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path
from e002_499_column_falsifier import aperture, interval, frame, run

HTML=Path(__file__).with_name("e002_497_offline_rater.html")

class FrozenColumnTests(unittest.TestCase):
    def test_exact_intervals(self):
        self.assertEqual(interval(160),(F(11,40),F(13,40)))
        self.assertEqual(interval(170),(F(14,40),F(16,40)))
        self.assertLess(interval(160)[1],interval(170)[0])
    def test_actual_adjudicator_false_disagreement(self):
        self.assertEqual(run()["same_image_different_column_disagreements"],1)
        self.assertEqual(run()["same_image_fixed_column_disagreements"],0)
    def test_false_temporal_change_with_static_anatomy(self):
        self.assertEqual((aperture(170)-aperture(160))/40,F(3,40))
        self.assertFalse(run()["physical_motion_present"])
    def test_schema_compatible_static_coordinates(self):
        self.assertEqual(frame(170)["lower_y"],105.0)
        self.assertEqual(frame(160)["lower_y"],102.0)
        self.assertEqual(frame(170)["flags"],[])
    def test_fixed_column_rater_implemented(self):
        h=HTML.read_text()
        for token in ("function nativeColumn(x)","if(!nativeColumn(x))",
                      "pts.push([160,","pts.some(p=>p[0]!==160)",
                      "ctx.moveTo(160,0)","POOR_GEOMETRY","x=160"):
            self.assertIn(token,h)
    def test_executable_column_predicate(self):
        h=HTML.read_text()
        m=re.search(r"function nativeColumn\(x\)\{[^}]+\}",h)
        self.assertIsNotNone(m)
        if not shutil.which("node"):self.skipTest("Node missing")
        js=m.group(0)+"""
if (!nativeColumn(160) || !nativeColumn(159.5) || !nativeColumn(160.5) ||
    nativeColumn(159.49) || nativeColumn(160.51) ||
    nativeColumn(NaN) || nativeColumn(Infinity)) process.exit(1);
"""
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"test.cjs";p.write_text(js)
            r=subprocess.run(["node",str(p)],capture_output=True,text=True,timeout=10)
            self.assertEqual(r.returncode,0,r.stderr)
    def test_offline_security_and_js_syntax(self):
        h=HTML.read_text()
        for token in ("connect-src 'none'","default-src 'none'","progress()!==260"):
            self.assertIn(token,h)
        self.assertNotIn("OWNER_ONLY_MAPPING",h)
        self.assertNotRegex(h,r"<script[^>]+src=|<link[^>]+href=")
        if shutil.which("node"):
            m=re.search(r"<script>([\s\S]*?)</script>",h)
            self.assertIsNotNone(m)
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/"rater.cjs";p.write_text(m.group(1))
                r=subprocess.run(["node","--check",str(p)],capture_output=True,text=True,timeout=10)
                self.assertEqual(r.returncode,0,r.stderr)
    def test_no_product_claim(self):
        d=run()
        self.assertEqual(d["release"],"BLOCKED")
        self.assertEqual(d["product"],"ABSTAIN_UNCALIBRATED")
        self.assertEqual(d["anatomical_human_ratings"],0)
        self.assertFalse(d["physical_hidden_closure_certified"])

if __name__=="__main__":unittest.main()
