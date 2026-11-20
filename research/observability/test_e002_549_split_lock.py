import json
import unittest

from e002_548_witness import audit as legacy_audit
from e002_549_split_lock import audit_locked, prediction_digest, EXPLORATORY, HELDOUT


def example(pid="S-24", origin="human", gap="g1", frame="f1"):
    p = dict(gap_id=gap, participant_id=pid, session_id="session-1", roi_id="left-eye",
             eye="left", blind_start_ms="100", blind_end_ms="110", closure_threshold="0.2",
             prediction="EXCLUDE", lock_sha256="a" * 64)
    f = dict(gap_id=gap, frame_id=frame, participant_id=pid, session_id="session-1",
             roi_id="left-eye", eye="left", quality="valid",
             timing_evidence="independent_calibration", transfer_evidence="independent_calibration",
             timing_certificate_id="t1", transfer_certificate_id="x1",
             rater_1="closed", rater_2="closed", frame_sha256="b" * 64,
             support_earliest_ms="102", support_latest_ms="105", mean_aperture_upper="0.15")
    return dict(schema="lucent-e002-548-v1", origin=origin, predictions=[p], reference_frames=[f])


def run(bundle):
    return audit_locked(bundle, prediction_digest(bundle["predictions"]))


class SplitLockTests(unittest.TestCase):
    def test_original_accepts_exploratory_without_split_label(self):
        self.assertEqual(legacy_audit(example())["counts"]["HUMAN_WITNESS_CANDIDATE_EXTERNAL_REVIEW"], 1)

    def test_new_gate_keeps_exploratory_out_of_heldout(self):
        x = run(example())
        self.assertEqual(x["groups"]["exploratory"]["candidate_participants"], 1)
        self.assertEqual(x["groups"]["heldout"]["candidate_participants"], 0)
        self.assertEqual(x["groups"]["heldout"]["participants_with_predictions"], 0)

    def test_heldout_candidate_separate(self):
        x = run(example("S-08"))
        self.assertEqual(x["groups"]["heldout"]["candidate_participants"], 1)
        self.assertEqual(x["groups"]["exploratory"]["candidate_participants"], 0)

    def test_prediction_mutation_fails_lock(self):
        b = example()
        digest = prediction_digest(b["predictions"])
        b["predictions"][0]["prediction"] = "ABSTAIN"
        with self.assertRaisesRegex(ValueError, "differs"):
            audit_locked(b, digest)

    def test_threshold_mutation_fails_lock(self):
        b = example()
        digest = prediction_digest(b["predictions"])
        b["predictions"][0]["closure_threshold"] = "0.99"
        with self.assertRaisesRegex(ValueError, "differs"):
            audit_locked(b, digest)

    def test_participant_substitution_fails_lock(self):
        b = example()
        digest = prediction_digest(b["predictions"])
        b["predictions"][0]["participant_id"] = "S-08"
        with self.assertRaisesRegex(ValueError, "differs"):
            audit_locked(b, digest)

    def test_unknown_subject_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            run(example("S-99"))

    def test_frame_participant_mismatch_rejected(self):
        b = example()
        b["reference_frames"][0]["participant_id"] = "S-08"
        with self.assertRaisesRegex(ValueError, "contamination"):
            run(b)

    def test_frame_session_mismatch_rejected(self):
        b = example()
        b["reference_frames"][0]["session_id"] = "session-2"
        with self.assertRaisesRegex(ValueError, "contamination"):
            run(b)

    def test_reference_negative_censored(self):
        b = example()
        b["reference_frames"][0]["mean_aperture_upper"] = "0.25"
        x = run(b)
        self.assertEqual(x["groups"]["exploratory"]["counts"], {"REFERENCE_CENSORED": 1})
        self.assertEqual(x["certified_exclusions"], 0)

    def test_abstain_never_candidate(self):
        b = example()
        b["predictions"][0]["prediction"] = "ABSTAIN"
        x = run(b)
        self.assertEqual(x["groups"]["exploratory"]["counts"], {"ABSTAIN_NO_EXCLUSION": 1})

    def test_mixed_partitions_distinct(self):
        a = example()
        b = example("S-08", gap="g2", frame="f2")
        a["predictions"] += b["predictions"]
        a["reference_frames"] += b["reference_frames"]
        x = run(a)
        self.assertEqual(x["groups"]["exploratory"]["candidate_participants"], 1)
        self.assertEqual(x["groups"]["heldout"]["candidate_participants"], 1)

    def test_repeated_participant_counted_once(self):
        a = example()
        b = example("S-24", gap="g2", frame="f2")
        a["predictions"] += b["predictions"]
        a["reference_frames"] += b["reference_frames"]
        x = run(a)
        self.assertEqual(x["groups"]["exploratory"]["candidate_participants"], 1)
        self.assertEqual(x["groups"]["exploratory"]["counts"]["HUMAN_WITNESS_CANDIDATE_EXTERNAL_REVIEW"], 2)

    def test_synthetic_not_human_validation(self):
        x = run(example(origin="synthetic"))
        self.assertEqual(x["evidence_tier"], "SYNTHETIC_PROVENANCE_TEST_ONLY")
        self.assertFalse(x["human_physical_validation"])

    def test_digest_match_not_precommit_authentication(self):
        x = run(example())
        self.assertEqual(x["precommit_provenance"], "EXTERNAL_PRECOMMIT_TIMESTAMP_UNVERIFIED")
        self.assertEqual(x["release"], "BLOCKED")

    def test_invalid_expected_digest_rejected(self):
        with self.assertRaisesRegex(ValueError, "external expected"):
            audit_locked(example(), "bad")

    def test_digest_is_key_order_invariant_but_array_order_sensitive(self):
        a = example()
        p = a["predictions"][0]
        self.assertEqual(prediction_digest([p]), prediction_digest([dict(reversed(list(p.items())))]))
        b = example("S-08", gap="g2", frame="f2")
        self.assertNotEqual(prediction_digest([p, b["predictions"][0]]), prediction_digest([b["predictions"][0], p]))

    def test_all_frozen_ids_cover_31_without_overlap(self):
        self.assertEqual(len(EXPLORATORY), 15)
        self.assertEqual(len(HELDOUT), 16)
        self.assertFalse(set(EXPLORATORY) & set(HELDOUT))

    def test_no_private_ids_in_output(self):
        s = json.dumps(run(example("S-08")))
        self.assertNotIn("S-08", s)
        self.assertNotIn("session-1", s)
        self.assertNotIn("left-eye", s)


if __name__ == "__main__":
    unittest.main()
