import unittest
from dataclasses import asdict
from lucent.measurement_claim_gate import evaluate_claim, PHYSIOLOGICAL_CLAIMS


class ClaimGateTests(unittest.TestCase):
    def base(self, claim="NO_HIDDEN_CLOSURE", **kwargs):
        return {"claim": claim, "observed_frames": 100, "expected_frames": 100, **kwargs}

    def test_all_physiological_claims_abstain(self):
        for claim in PHYSIOLOGICAL_CLAIMS:
            with self.subTest(claim=claim):
                result = evaluate_claim(self.base(claim))
                self.assertEqual(result.decision, "ABSTAIN_UNCALIBRATED")
                self.assertIsNone(result.frame_completeness)
                self.assertEqual(result.release, "BLOCKED")

    def test_speed_floor_laundering_does_not_certify(self):
        evidence = {"velocity_upper_per_s": 24300 / 983,
                    "speed_floor_is_safe_upper_bound": True,
                    "certified": True, "independent_reviewers": 2}
        r = evaluate_claim(self.base(evidence=evidence))
        self.assertEqual(r.decision, "ABSTAIN_UNCALIBRATED")

    def test_all_fake_calibrations_do_not_certify(self):
        evidence = {k: True for k in ("clock", "shutter", "velocity", "human_raters", "reference")}
        r = evaluate_claim(self.base(nominal_fps="30", evidence=evidence))
        self.assertEqual(r.decision, "ABSTAIN_UNCALIBRATED")

    def test_missing_frames_remain_uncalibrated(self):
        r = evaluate_claim(self.base(observed_frames=98, expected_frames=100))
        self.assertEqual(r.decision, "ABSTAIN_UNCALIBRATED")

    def test_nuisances_never_upgrade(self):
        nuisances = ["rolling_shutter", "gaze", "glasses", "brightness", "blur", "clock_unknown"]
        r = evaluate_claim(self.base(nuisances=nuisances))
        self.assertEqual(r.decision, "ABSTAIN_UNCALIBRATED")

    def test_quality_complete_is_not_physiology(self):
        r = evaluate_claim(self.base("ACQUISITION_QUALITY"))
        self.assertEqual(r.decision, "ACQUISITION_QUALITY_ONLY")
        self.assertEqual(r.frame_completeness, 1)
        self.assertEqual(r.release, "BLOCKED")
        self.assertEqual(r.evidence_tier, "NOT_PHYSIOLOGICALLY_VALIDATED")

    def test_quality_missing_is_not_physiology(self):
        r = evaluate_claim(self.base("ACQUISITION_QUALITY", observed_frames=97))
        self.assertEqual(r.frame_completeness, 0.97)
        self.assertEqual(r.decision, "ACQUISITION_QUALITY_ONLY")

    def test_bad_counts_rejected(self):
        for bad in (-1, 1.5, True, None, "100", 10**20):
            with self.subTest(bad=bad):
                r = evaluate_claim(self.base(observed_frames=bad))
                self.assertEqual(r.decision, "INVALID_INPUT")
        self.assertEqual(evaluate_claim(self.base(expected_frames=0)).decision, "INVALID_INPUT")
        self.assertEqual(evaluate_claim(self.base(observed_frames=101)).decision, "INVALID_INPUT")

    def test_bad_fps_rejected(self):
        for fps in (0, -1, True, "NaN", "Infinity", float("nan"), float("inf"), "x"):
            with self.subTest(fps=fps):
                self.assertEqual(evaluate_claim(self.base(nominal_fps=fps)).decision, "INVALID_INPUT")

    def test_unknown_claim_rejected(self):
        for claim in ("EXCLUDE", "CERTIFIED", "BLINK", "", None, 42):
            with self.subTest(claim=claim):
                self.assertEqual(evaluate_claim(self.base(claim)).decision, "INVALID_INPUT")

    def test_malformed_request_rejected(self):
        for req in (None, [], "x", 4):
            self.assertEqual(evaluate_claim(req).decision, "INVALID_INPUT")

    def test_malformed_evidence_and_nuisance_rejected(self):
        self.assertEqual(evaluate_claim(self.base(evidence=True)).decision, "INVALID_INPUT")
        self.assertEqual(evaluate_claim(self.base(nuisances="glasses")).decision, "INVALID_INPUT")

    def test_result_schema_cannot_contain_exclusion(self):
        for claim in PHYSIOLOGICAL_CLAIMS | {"ACQUISITION_QUALITY"}:
            payload = asdict(evaluate_claim(self.base(claim)))
            self.assertNotIn(payload["decision"], {"EXCLUDE", "CERTIFIED", "NO_CLOSURE"})
            self.assertEqual(payload["release"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
