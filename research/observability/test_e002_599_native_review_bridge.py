#!/usr/bin/env python3
"""E002-599 frozen synthetic regression. No human images or ratings."""
import copy
import json
import unittest
from e002_599_native_review_bridge import analyze, classify, validate_export

def packet(rater):
    clips = {}
    for c in range(10):
        name = f"clip_{c:04d}"
        clips[name] = [
            dict(frame=i, upper_y=None, lower_y=None, iris_diameter=None,
                 uncertainty_px=None, flags=["UNREVIEWED"])
            for i in range(19)
        ]
    return dict(experiment="E002-574", rater=rater, clips=clips)

def mark(p, i, upper, lower, x=320, uncertainty=0.5, clip="clip_0000"):
    p["clips"][clip][i] = dict(frame=i, upper_y=upper, lower_y=lower,
        iris_diameter=None, uncertainty_px=uncertainty, measurement_x=x, flags=[])

def cal():
    return dict(experiment="E002-599", independently_validated=True,
        frozen_before_review=True, external_reference_id="owner-only-study-reference",
        clips=[dict(blind_clip="clip_0000", iris_diameter_px=100,
                    iris_error_px=1, x_ref_px=320,
                    registration_tolerance_px=1,
                    max_lid_slope_px_per_px=10)])

class GeometryBridgeTests(unittest.TestCase):
    def setUp(self):
        self.a, self.b = packet("A"), packet("B")
        for p in (self.a, self.b):
            mark(p, 0, 200, 240)
            mark(p, 1, 200, 202)
            mark(p, 3, 200, 240)

    def test_positive_index_witness_is_conditional(self):
        out = analyze(self.a, self.b, cal())
        self.assertEqual(out["phase_positive_alias_pairs"], [1, 0, 0])
        self.assertEqual(out["windows_with_any_positive_alias"], 1)
        self.assertEqual(out["frame_states"]["OPEN"], 2)
        self.assertEqual(out["frame_states"]["CLOSED"], 1)
        self.assertFalse(out["physical_shutter_validated"])
        self.assertFalse(out["zero_witness_excludes_hidden_closure"])

    def test_missing_calibration_abstains(self):
        out = analyze(self.a, self.b)
        self.assertEqual(out["frame_states"]["UNCERTAIN"], 190)
        self.assertEqual(out["phase_positive_alias_pairs"], [0, 0, 0])

    def test_false_provenance_assertion_abstains(self):
        bad = cal(); bad["independently_validated"] = False
        self.assertEqual(analyze(self.a, self.b, bad)["frame_states"]["UNCERTAIN"], 190)

    def test_cross_column_false_closure_is_rejected(self):
        # Same synthetic lid shape: u(x)=100+0.5x, l(x)=130+0.5x.
        # True aperture is 30px everywhere, but mixing x=58 upper
        # with x=0 lower would create a 1px apparent aperture.
        a = copy.deepcopy(self.a)
        b = copy.deepcopy(self.b)
        for p in (a, b):
            mark(p, 1, 129, 130, x=58)
        self.assertEqual(classify(a["clips"]["clip_0000"][1],
                                  b["clips"]["clip_0000"][1],
                                  (100, 1, 320, 1, 10)), "UNCERTAIN")
        self.assertEqual(analyze(a, b, cal())["phase_positive_alias_pairs"], [0, 0, 0])

    def test_missing_slope_refuses_classification(self):
        bad = cal()
        del bad["clips"][0]["max_lid_slope_px_per_px"]
        self.assertEqual(analyze(self.a, self.b, bad)["frame_states"]["UNCERTAIN"], 190)

    def test_offset_slope_inflation_abstains(self):
        for p in (self.a, self.b):
            mark(p, 1, 200, 202, x=321)
        c = cal()
        self.assertEqual(analyze(self.a, self.b, c)["frame_states"]["UNCERTAIN"], 188)
        # With the same x as reference, the original closed interval remains.
        for p in (self.a, self.b):
            mark(p, 1, 200, 202, x=320)
        self.assertEqual(analyze(self.a, self.b, c)["frame_states"]["CLOSED"], 1)

    def test_cross_rater_columns_disagree(self):
        self.b["clips"]["clip_0000"][1]["measurement_x"] = 315
        self.assertEqual(analyze(self.a, self.b, cal())["frame_states"]["DISAGREEMENT"], 1)

    def test_threshold_straddling_abstains(self):
        for p in (self.a, self.b):
            mark(p, 1, 200, 220, uncertainty=2)
        self.assertEqual(analyze(self.a, self.b, cal())["frame_states"]["UNCERTAIN"], 188)

    def test_nuisance_is_not_forced_closed(self):
        self.a["clips"]["clip_0000"][1] = dict(frame=1, upper_y=None, lower_y=None,
            iris_diameter=None, uncertainty_px=None, flags=["BLUR"])
        self.assertEqual(analyze(self.a, self.b, cal())["phase_positive_alias_pairs"], [0, 0, 0])

    def test_missing_or_extra_frame_rejected(self):
        bad = copy.deepcopy(self.a)
        bad["clips"]["clip_0000"].pop()
        with self.assertRaises(ValueError):
            validate_export(bad, "A")
        bad = copy.deepcopy(self.a)
        bad["clips"]["clip_0000"][1]["extra"] = 1
        with self.assertRaises(ValueError):
            validate_export(bad, "A")

    def test_nonfinite_and_untrusted_iris_field_rejected(self):
        bad = copy.deepcopy(self.a)
        bad["clips"]["clip_0000"][1]["measurement_x"] = float("nan")
        with self.assertRaises(ValueError):
            validate_export(bad, "A")
        bad = copy.deepcopy(self.a)
        bad["clips"]["clip_0000"][1]["iris_diameter"] = 100
        with self.assertRaises(ValueError):
            validate_export(bad, "A")

    def test_output_minimizes_private_data(self):
        output = json.dumps(analyze(self.a, self.b, cal()), sort_keys=True)
        for key in ("blind_clip", "measurement_x", "upper_y", "lower_y",
                    "external_reference_id", "video_sha256", "participant_id"):
            self.assertNotIn(key, output)
        self.assertIn("ABSTAIN_UNCALIBRATED", output)

if __name__ == "__main__":
    unittest.main(verbosity=2)
