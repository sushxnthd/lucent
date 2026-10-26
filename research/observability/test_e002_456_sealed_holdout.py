#!/usr/bin/env python3
"""E002-456 sealed-prediction adversarial tests; synthetic data only."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e002_456_sealed_holdout import freeze, score
from test_e002_456_prospective_gate import fixture


def study():
    c = fixture()
    c["reference"] = []
    return {"schema_version": "E002-456-v1", "intervals": [c]}


class SealedHoldoutTests(unittest.TestCase):
    def test_freeze_has_no_reference(self):
        manifest, public = freeze(study())
        self.assertEqual(len(manifest["predictions"]), 1)
        self.assertEqual(len(public["commitment_sha256"]), 64)
        self.assertFalse(public["physical_release_authorized"])

    def test_witness_after_unsealing_falsifies(self):
        p = study()
        manifest, _ = freeze(p)
        p["intervals"][0]["reference"] = [{
            "time_ms": 5, "aperture_mm": 1.7,
            "uncertainty_mm": 0.1, "quality": "PASS"}]
        result = score(p, manifest)
        self.assertEqual(result["counts"]["development"][
            "FALSIFIED_JOINT_ASSUMPTIONS"], 1)
        self.assertFalse(result["physical_release_authorized"])

    def test_changed_velocity_rejected(self):
        p = study()
        manifest, _ = freeze(p)
        p["intervals"][0]["velocity"]["limit_mm_s"] = 200
        with self.assertRaises(ValueError):
            score(p, manifest)

    def test_changed_nuisance_rejected(self):
        p = study()
        manifest, _ = freeze(p)
        p["intervals"][0]["nuisance"]["blur"] = "UNKNOWN"
        with self.assertRaises(ValueError):
            score(p, manifest)

    def test_changed_split_rejected(self):
        p = study()
        manifest, _ = freeze(p)
        p["intervals"][0]["split"] = "holdout"
        with self.assertRaises(ValueError):
            score(p, manifest)

    def test_manifest_tamper_rejected(self):
        p = study()
        manifest, _ = freeze(p)
        manifest["predictions"][0]["decision"] = "NOT_EXCLUDED"
        with self.assertRaises(ValueError):
            score(p, manifest)

    def test_freeze_refuses_unblinded_reference(self):
        p = study()
        p["intervals"][0]["reference"] = [{
            "time_ms": 5, "aperture_mm": 1,
            "uncertainty_mm": 0, "quality": "PASS"}]
        with self.assertRaises(ValueError):
            freeze(p)

    def test_no_private_ids_in_public_artifact(self):
        p = study()
        manifest, public = freeze(p)
        p["intervals"][0]["reference"] = []
        result = score(p, manifest)
        for public_artifact in (public, result):
            rendered = json.dumps(public_artifact)
            self.assertNotIn("opaque-A", rendered)
            self.assertNotIn("synthetic-1", rendered)


if __name__ == "__main__":
    unittest.main()
