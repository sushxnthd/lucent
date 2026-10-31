"""E002-525 adversarial prospective prediction-lock regression.

All fixtures synthetic. No human images, participants or real reference labels.
"""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import e002_519_reference_censoring as old
import e002_525_prediction_lock as lock

NONCE = "0123456789abcdef" * 4


def frozen():
    return {"version": "E002-525-v1", "nonce_hex": NONCE, "gaps": [
        {"id": "g1", "participant": "synthetic_p1", "session": "s1",
         "prediction": "EXCLUDE", "left_end_max_ms": 10, "right_start_min_ms": 30},
        {"id": "g2", "participant": "synthetic_p2", "session": "s2",
         "prediction": "EXCLUDE", "left_end_max_ms": 40, "right_start_min_ms": 60}
    ]}


def ref(rid, start, end, anatomy):
    return {"id": rid, "start_min_ms": start, "end_max_ms": end, "anatomy": anatomy,
            "two_independent_raters": True, "photometry_valid": True,
            "clock_valid": True, "native_provenance_valid": True, "nuisance_clear": True}


def evidence(m=None):
    m = m or frozen()
    gaps = [dict(g, references=[]) for g in m["gaps"]]
    gaps[0]["references"] = [ref("r1", 12, 20, "CLOSED_WITNESS")]
    gaps[1]["references"] = [ref("r2", 42, 50, "OPEN_OBSERVED")]
    return {"version": "E002-519-v1", "gaps": gaps}


class ProspectiveLock(unittest.TestCase):
    def setUp(self):
        self.m = frozen()
        self.d = lock.commitment(self.m)
        self.e = evidence(self.m)

    def test_valid_locked_replay_keeps_falsification(self):
        out = lock.verify_and_evaluate(self.m, self.d, self.e)
        self.assertEqual(out["counts"]["FALSIFIED_BY_REFERENCE_WITNESS"], 1)
        self.assertEqual(out["counts"]["REFERENCE_CENSORED_NOT_FALSIFIED"], 1)
        self.assertFalse(out["prospective_timestamp_authenticated_by_code"])
        self.assertFalse(out["human_independence_authenticated_by_code"])
        self.assertEqual(out["product"], "ABSTAIN_UNCALIBRATED")

    def test_historical_unlocked_evaluator_accepts_posthoc_abstain(self):
        self.assertEqual(old.evaluate(self.e)["counts"]["FALSIFIED_BY_REFERENCE_WITNESS"], 1)
        changed = copy.deepcopy(self.e)
        changed["gaps"][0]["prediction"] = "ABSTAIN"
        self.assertEqual(old.evaluate(changed)["counts"]["FALSIFIED_BY_REFERENCE_WITNESS"], 0)
        self.assertEqual(old.evaluate(changed)["counts"]["NOT_TESTABLE"], 1)

    def test_historical_unlocked_evaluator_accepts_omission(self):
        changed = copy.deepcopy(self.e)
        changed["gaps"].pop(0)
        self.assertEqual(old.evaluate(changed)["counts"]["FALSIFIED_BY_REFERENCE_WITNESS"], 0)

    def test_lock_rejects_posthoc_abstain(self):
        changed = copy.deepcopy(self.e)
        changed["gaps"][0]["prediction"] = "ABSTAIN"
        with self.assertRaisesRegex(ValueError, "POSTHOC"):
            lock.verify_and_evaluate(self.m, self.d, changed)

    def test_lock_rejects_missing_or_added_gap(self):
        changed = copy.deepcopy(self.e)
        changed["gaps"].pop(0)
        with self.assertRaisesRegex(ValueError, "DENOMINATOR"):
            lock.verify_and_evaluate(self.m, self.d, changed)
        changed = copy.deepcopy(self.e)
        changed["gaps"].append(dict(changed["gaps"][0], id="g3"))
        with self.assertRaisesRegex(ValueError, "DENOMINATOR"):
            lock.verify_and_evaluate(self.m, self.d, changed)

    def test_lock_rejects_timing_expansion(self):
        changed = copy.deepcopy(self.e)
        changed["gaps"][0]["right_start_min_ms"] = 31
        with self.assertRaisesRegex(ValueError, "TIMING"):
            lock.verify_and_evaluate(self.m, self.d, changed)

    def test_lock_rejects_changed_participant_and_session(self):
        for field in ("participant", "session"):
            changed = copy.deepcopy(self.e)
            changed["gaps"][0][field] = "different"
            with self.assertRaisesRegex(ValueError, "ATTRIBUTION"):
                lock.verify_and_evaluate(self.m, self.d, changed)

    def test_lock_rejects_commitment_mismatch(self):
        with self.assertRaisesRegex(ValueError, "COMMITMENT_MISMATCH"):
            lock.verify_and_evaluate(self.m, "a"*64, self.e)
        with self.assertRaisesRegex(ValueError, "INVALID_PUBLISHED"):
            lock.verify_and_evaluate(self.m, "not-a-digest", self.e)

    def test_private_nonce_and_frozen_metadata_cannot_change(self):
        for key, value in (("nonce_hex", "f"*64), ("version", "E002-524")):
            m = copy.deepcopy(self.m)
            m[key] = value
            with self.assertRaises(ValueError):
                lock.verify_and_evaluate(m, self.d, self.e)
        m = copy.deepcopy(self.m)
        m["gaps"][0]["participant"] = "other"
        with self.assertRaisesRegex(ValueError, "COMMITMENT_MISMATCH"):
            lock.verify_and_evaluate(m, self.d, self.e)

    def test_reject_invalid_or_zero_nonce(self):
        for n in ("0"*64, "a"*63, "G"*64, "", 123):
            m = copy.deepcopy(self.m)
            m["nonce_hex"] = n
            with self.assertRaises(ValueError):
                lock.commitment(m)

    def test_canonical_key_order_independent(self):
        m = copy.deepcopy(self.m)
        m["gaps"] = [dict(reversed(list(g.items()))) for g in m["gaps"]]
        m = dict(reversed(list(m.items())))
        self.assertEqual(lock.commitment(m), self.d)

    def test_frozen_enrollment_order_is_committed(self):
        m = copy.deepcopy(self.m)
        m["gaps"].reverse()
        self.assertNotEqual(lock.commitment(m), self.d)

    def test_reject_duplicate_or_invalid_gap(self):
        m = copy.deepcopy(self.m)
        m["gaps"][1]["id"] = "g1"
        with self.assertRaisesRegex(ValueError, "DUPLICATE"):
            lock.commitment(m)
        m = copy.deepcopy(self.m)
        m["gaps"][0]["left_end_max_ms"] = True
        with self.assertRaisesRegex(ValueError, "FINITE"):
            lock.commitment(m)
        m = copy.deepcopy(self.m)
        m["gaps"][0]["right_start_min_ms"] = 10
        with self.assertRaisesRegex(ValueError, "INTERVAL"):
            lock.commitment(m)

    def test_censored_reference_is_not_clean_success(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"][0]["anatomy"] = "UNKNOWN"
        out = lock.verify_and_evaluate(self.m, self.d, e)
        self.assertEqual(out["counts"]["UNKNOWN"], 1)
        self.assertEqual(out["counts"]["FALSIFIED_BY_REFERENCE_WITNESS"], 0)
        self.assertFalse(out["verified_no_hidden_closure"])

    def test_missing_reference_does_not_pass(self):
        e = copy.deepcopy(self.e)
        e["gaps"][0]["references"] = []
        out = lock.verify_and_evaluate(self.m, self.d, e)
        self.assertEqual(out["counts"]["UNKNOWN"], 1)
        self.assertEqual(out["release"], "BLOCKED")

    def test_no_personal_data_in_fixture(self):
        self.assertEqual(set(self.m), {"version", "nonce_hex", "gaps"})
        self.assertTrue(all(g["participant"].startswith("synthetic_") for g in self.m["gaps"]))


if __name__ == "__main__":
    unittest.main()
