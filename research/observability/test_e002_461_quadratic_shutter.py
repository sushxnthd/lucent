"""E002-461 synthetic shutter falsification; zero human/physical evidence."""
import copy
import math
import random
import unittest

from e002_461_quadratic_shutter import NUISANCES, evaluate, example
from e002_460_exposure_centroid import evaluate as linear_evaluate
from e002_460_exposure_centroid import example as linear_example


def naive_static_inverse(x):
    """Deliberately WRONG observation assumption for the preregistered control."""
    d = linear_example(
        gap_ms=x["exposures"][1]["centroid_ms"],
        shutter_ms=x["exposures"][0]["support_end_ms"] -
                   x["exposures"][0]["support_start_ms"])
    d.update(mean0_mm=math.sqrt(x["q0_mm2"]),
             mean1_mm=math.sqrt(x["q1_mm2"]),
             closure_mm=x["closure_mm"],
             closing_mm_s=x["closing_mm_s"],
             opening_mm_s=x["opening_mm_s"])
    return linear_evaluate(d)


class E002461Tests(unittest.TestCase):
    def test_frozen_99pct_false_exclusion(self):
        x = example(0.99)
        self.assertLess(x["exposures"][0]["support_end_ms"],
                        x["synthetic_witness_tau_ms"])
        self.assertLess(x["synthetic_witness_tau_ms"],
                        x["exposures"][1]["support_start_ms"])
        self.assertEqual(naive_static_inverse(x)["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(evaluate(x)["decision"], "NOT_EXCLUDED")

    def test_frozen_95pct_negative_control(self):
        x = example(0.95)
        self.assertNotEqual(naive_static_inverse(x)["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertEqual(evaluate(x)["decision"], "NOT_EXCLUDED")

    def test_uncertainty_never_strengthens_exclusion(self):
        x = example(0.99)
        original = evaluate(x)
        x["uncertainty0_mm2"] = 0.4
        x["uncertainty1_mm2"] = 0.5
        d = evaluate(x)
        self.assertLessEqual(d["mean0_lower_mm"], original["mean0_lower_mm"])
        self.assertLessEqual(d["mean1_lower_mm"], original["mean1_lower_mm"])
        self.assertEqual(d["decision"], "NOT_EXCLUDED")

    def test_clear_large_aperture_excluded_conditionally(self):
        x = example(0.99)
        x["q0_mm2"] = 25
        x["q1_mm2"] = 25
        d = evaluate(x)
        self.assertEqual(d["decision"], "EXCLUDED_CONDITIONALLY")
        self.assertFalse(d["physical_certification"])

    def test_unknown_nuisance_always_abstains(self):
        for name in NUISANCES:
            x = example()
            x["nuisance"][name] = "UNKNOWN"
            self.assertEqual(evaluate(x)["decision"], "ABSTAIN_UNCALIBRATED", name)

    def test_static_only_or_nonquadratic_abstains(self):
        for k, value in (("transfer_calibrated", False),
                         ("uniform_kernel_calibrated", False),
                         ("velocity_caps_assumed_for_research", False),
                         ("synthetic_uncertainty_authenticated", False),
                         ("observable", "PIXEL_CONTRAST")):
            x = example()
            x[k] = value
            self.assertEqual(evaluate(x)["decision"], "ABSTAIN_UNCALIBRATED", k)

    def test_kernel_clock_and_geometry_metadata(self):
        for key, value in (("kernel_normalized", False),
                           ("centroid_authenticated", False),
                           ("support_authenticated", False),
                           ("clock_uncertainty_ms", 0.001),
                           ("centroid_ms", 0.4),
                           ("support_end_ms", 3.8)):
            x = example()
            x["exposures"][0][key] = value
            self.assertEqual(evaluate(x)["decision"], "ABSTAIN_UNCALIBRATED", key)

    def test_invalid_numerics_and_units(self):
        for key, value in (("q0_mm2", -1), ("q0_mm2", float("nan")),
                           ("q1_mm2", float("inf")), ("uncertainty0_mm2", -0.1),
                           ("closure_mm", -1), ("closing_mm_s", 0),
                           ("opening_mm_s", -1)):
            x = example()
            x[key] = value
            self.assertEqual(evaluate(x)["decision"], "ABSTAIN_UNCALIBRATED", key)

    def test_10000_random_affine_dark_gap_witnesses(self):
        rng = random.Random(461)
        naive_false_exclusions = 0
        for _ in range(10000):
            D = rng.uniform(3.5, 10)
            w = rng.uniform(0.2, min(3.0, 0.7 * D))
            tau = rng.uniform(w / 2 + 0.01, D - w / 2 - 0.01)
            C = rng.uniform(0.15, 0.8)
            O = rng.uniform(0.1, 0.5)
            a = rng.uniform(0.65, 1.0)
            b = rng.uniform(0.65, 1.0)
            c = rng.uniform(0.5, 3)
            m0 = c + a * C * tau
            m1 = c + b * O * (D - tau)
            x = example(0.99, D, w)
            x.update(q0_mm2=m0*m0+(a*C*w)**2/12,
                     q1_mm2=m1*m1+(b*O*w)**2/12,
                     closing_mm_s=1000*C, opening_mm_s=1000*O,
                     closure_mm=c, synthetic_witness_tau_ms=tau)
            d = evaluate(x)
            self.assertNotEqual(d["decision"], "EXCLUDED_CONDITIONALLY", (x,d))
            self.assertFalse(d["physical_certification"])
            if naive_static_inverse(x)["decision"] == "EXCLUDED_CONDITIONALLY":
                naive_false_exclusions += 1
        print("E002-461 10000 synthetic witnessed closures; naive false exclusions:",
              naive_false_exclusions, "; repaired false exclusions: 0")
        self.assertGreater(naive_false_exclusions, 0)


if __name__ == "__main__":
    unittest.main()
