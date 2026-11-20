"""Independent adversarial checks for E002-426 preregistered study control."""
import copy
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e002_426_prospective_lock as m


def trial(i, participant, pred="NO_CROSSING_CONDITIONAL", **flags):
    return {"trial_id": f"trial_{i}", "participant_id": participant, "device_id": "camera_1",
            "interval_start_s": float(i), "interval_end_s": float(i) + 0.01,
            "prediction": pred,
            "nuisance_flags": {k: flags.get(k, False) for k in m.NUISANCES},
            "model_input_sha256": "a" * 64, "camera_calibration_ref": "camera_record_1",
            "velocity_bound_ref": "velocity_audit_1"}


def registry():
    return {"study_id": "prospective_pilot_1", "training_participants": ["train_1"],
            "holdout_participants": ["hold_1", "hold_2"], "device_ids": ["camera_1"],
            "trials": [*[trial(i, "hold_1") for i in range(99)], trial(99, "hold_2", blur=True)]}


class FrozenGates(unittest.TestCase):
    def test_imbalance_and_participant_macro(self):
        r = registry()
        labels = {f"trial_{i}": "NEGATIVE_CONDITIONAL" for i in range(99)}
        labels["trial_99"] = "WITNESSED_CROSSING"
        report = m.score(r, m.seal(r), labels)
        self.assertEqual(report["pooled"]["finite_set_false_certificate_lower"], 0.01)
        self.assertEqual(report["participant_macro"]["finite_set_false_certificate_lower"], 0.5)
        self.assertEqual(report["nuisance_strata"]["blur"]["true"]["witnessed_failures"], 1)
        self.assertFalse(report["product_claim_authorized"])
        self.assertFalse(report["external_physical_provenance_authenticated"])

    def test_unresolved_and_missing_are_never_negative(self):
        r = registry()
        labels = {f"trial_{i}": "NEGATIVE_CONDITIONAL" for i in range(100)}
        labels["trial_1"] = "UNRESOLVED"
        labels["trial_2"] = "MISSING"
        labels["trial_99"] = "WITNESSED_CROSSING"
        s = m.score(r, m.seal(r), labels)
        self.assertEqual(s["pooled"]["finite_set_false_certificate_lower"], .01)
        self.assertEqual(s["pooled"]["finite_set_false_certificate_upper"], .03)
        del labels["trial_2"]
        with self.assertRaisesRegex(m.RegistryError, "exactly"):
            m.score(r, m.seal(r), labels)

    def test_seal_detects_all_material_changes(self):
        r = registry()
        fixed = m.seal(r)
        for name, value in [("prediction", "ABSTAIN"), ("interval_end_s", 1.5),
                            ("camera_calibration_ref", "camera_record_2")]:
            changed = copy.deepcopy(r)
            changed["trials"][0][name] = value
            with self.assertRaises(m.RegistryError):
                m.verify_seal(changed, fixed)
        changed = copy.deepcopy(r)
        changed["trials"][0]["nuisance_flags"]["gaze"] = True
        with self.assertRaises(m.RegistryError):
            m.verify_seal(changed, fixed)
        changed = copy.deepcopy(r)
        changed["trials"].pop()
        with self.assertRaises(m.RegistryError):
            m.verify_seal(changed, fixed)

    def test_leakage_duplicates_and_nuisance_missing_rejected(self):
        r = registry()
        r["training_participants"].append("hold_1")
        with self.assertRaisesRegex(m.RegistryError, "leakage"):
            m.seal(r)
        r = registry()
        r["trials"][1]["trial_id"] = r["trials"][0]["trial_id"]
        with self.assertRaisesRegex(m.RegistryError, "duplicate trial"):
            m.seal(r)
        r = registry()
        del r["trials"][0]["nuisance_flags"]["clock"]
        with self.assertRaisesRegex(m.RegistryError, "nuisance"):
            m.seal(r)
        r = registry()
        r["trials"][0]["interval_end_s"] = float("nan")
        with self.assertRaisesRegex(m.RegistryError, "interval"):
            m.seal(r)

    def test_all_abstain_is_undefined(self):
        r = registry()
        for t in r["trials"]:
            t["prediction"] = "ABSTAIN"
        labels = {f"trial_{i}": "UNRESOLVED" for i in range(100)}
        s = m.score(r, m.seal(r), labels)
        self.assertIsNone(s["pooled"]["finite_set_false_certificate_lower"])
        self.assertIsNone(s["participant_macro"]["finite_set_false_certificate_lower"])
        self.assertEqual(s["pooled"]["abstentions"], 100)

    def test_csv_duplicate_unknown_and_missing(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "refs.csv"
            path.write_text("trial_id,reference_label\ntrial_1,WITNESSED_CROSSING\ntrial_1,UNRESOLVED\n")
            with self.assertRaisesRegex(m.RegistryError, "duplicate reference"):
                m.read_reference_csv(path)
            path.write_text("trial_id,reference_label\ntrial_1,NOT_A_LABEL\n")
            with self.assertRaisesRegex(m.RegistryError, "invalid reference"):
                m.read_reference_csv(path)
            path.write_text("trial_id,reference_label\ntrial_1,MISSING\n")
            self.assertEqual(m.read_reference_csv(path)["trial_1"], "MISSING")


if __name__ == "__main__":
    unittest.main()
