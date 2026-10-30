import copy
import unittest
from e002_548_witness import audit

H = "a" * 64

def fixture(origin="synthetic"):
    return {
        "schema": "lucent-e002-548-v1", "origin": origin,
        "predictions": [{"gap_id": "g1", "participant_id": "P01", "session_id": "S1", "roi_id": "left-eye", "eye": "left", "blind_start_ms": "100", "blind_end_ms": "110", "closure_threshold": "0.2", "prediction": "EXCLUDE", "lock_sha256": H}],
        "reference_frames": [{"gap_id": "g1", "frame_id": "f1", "participant_id": "P01", "session_id": "S1", "roi_id": "left-eye", "eye": "left", "quality": "valid", "timing_evidence": "independent_calibration", "transfer_evidence": "independent_calibration", "timing_certificate_id": "t1", "transfer_certificate_id": "x1", "rater_1": "closed", "rater_2": "closed", "frame_sha256": H, "support_earliest_ms": "102", "support_latest_ms": "105", "mean_aperture_upper": "0.15"}]
    }

class WitnessTests(unittest.TestCase):
    def test_synthetic_witness_not_physical(self):
        o = audit(fixture())
        self.assertEqual(o["counts"], {"SYNTHETIC_WITNESS_ONLY": 1})
        self.assertEqual(o["certified_exclusions"], 0)
        self.assertNotIn("P01", str(o))
    def test_human_only_candidate(self):
        self.assertEqual(audit(fixture("human"))["counts"], {"HUMAN_WITNESS_CANDIDATE_EXTERNAL_REVIEW": 1})
    def test_exact_threshold_positive(self):
        x = fixture(); x["reference_frames"][0]["mean_aperture_upper"] = "0.2"
        self.assertEqual(audit(x)["counts"], {"SYNTHETIC_WITNESS_ONLY": 1})
    def test_above_threshold_censored(self):
        x = fixture(); x["reference_frames"][0]["mean_aperture_upper"] = "0.2000000000000001"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_overlap_not_containment(self):
        x = fixture(); x["reference_frames"][0]["support_earliest_ms"] = "99"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_touch_boundary_censored(self):
        x = fixture(); x["reference_frames"][0]["support_earliest_ms"] = "100"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_uncertainty_spills(self):
        x = fixture(); x["reference_frames"][0]["support_latest_ms"] = "111"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_wrong_participant(self):
        x = fixture(); x["reference_frames"][0]["participant_id"] = "P02"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_wrong_session(self):
        x = fixture(); x["reference_frames"][0]["session_id"] = "S2"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_wrong_roi(self):
        x = fixture(); x["reference_frames"][0]["roi_id"] = "other"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_wrong_eye(self):
        x = fixture(); x["reference_frames"][0]["eye"] = "right"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_disagreeing_raters(self):
        x = fixture(); x["reference_frames"][0]["rater_2"] = "uncertain"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_unverified_transfer(self):
        x = fixture(); x["reference_frames"][0]["transfer_evidence"] = "video_fps_only"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_reference_negative_censored(self):
        x = fixture(); x["reference_frames"][0]["mean_aperture_upper"] = "0.9"
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_no_reference_censored(self):
        x = fixture(); x["reference_frames"] = []
        self.assertEqual(audit(x)["counts"], {"REFERENCE_CENSORED": 1})
    def test_abstain(self):
        x = fixture(); x["predictions"][0]["prediction"] = "ABSTAIN"
        self.assertEqual(audit(x)["counts"], {"ABSTAIN_NO_EXCLUSION": 1})
    def test_duplicate_gap(self):
        x = fixture(); x["predictions"].append(copy.deepcopy(x["predictions"][0]))
        with self.assertRaises(ValueError): audit(x)
    def test_duplicate_frame(self):
        x = fixture(); x["reference_frames"].append(copy.deepcopy(x["reference_frames"][0]))
        with self.assertRaises(ValueError): audit(x)
    def test_bad_hash(self):
        x = fixture(); x["predictions"][0]["lock_sha256"] = "fake"
        with self.assertRaises(ValueError): audit(x)
    def test_nan(self):
        x = fixture(); x["reference_frames"][0]["mean_aperture_upper"] = "NaN"
        with self.assertRaises(ValueError): audit(x)
    def test_no_floats(self):
        x = fixture(); x["reference_frames"][0]["mean_aperture_upper"] = 0.15
        with self.assertRaises(ValueError): audit(x)
    def test_inverted_support(self):
        x = fixture(); x["reference_frames"][0]["support_earliest_ms"] = "106"
        with self.assertRaises(ValueError): audit(x)
    def test_no_participant_identity_export(self):
        x = fixture(); x["predictions"][0]["participant_id"] = "sensitive-name"
        self.assertNotIn("sensitive-name", str(audit(x)))
    def test_multiple_same_participant_count_once(self):
        x = fixture(); p = copy.deepcopy(x["predictions"][0]); p["gap_id"] = "g2"; x["predictions"].append(p)
        f = copy.deepcopy(x["reference_frames"][0]); f["gap_id"] = "g2"; x["reference_frames"].append(f)
        o = audit(x)
        self.assertEqual(o["candidate_participant_count"], 1)
        self.assertEqual(o["counts"], {"SYNTHETIC_WITNESS_ONLY": 2})

if __name__ == "__main__": unittest.main()
