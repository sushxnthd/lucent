"""Adversarial E002-460 synthetic checks; no human evidence or physical certification."""
import copy
import math
import random
import unittest
from e002_460_exposure_centroid import NUISANCES, evaluate, example

class E002460Tests(unittest.TestCase):
    def test_nominal_240_fps_dark_gap_excluded(self):
        for shutter in (0.1,1.0,2.0,2.3,4.0):
            d=evaluate(example(1000/240,shutter))
            self.assertEqual(d["decision"],"EXCLUDED_CONDITIONALLY",d)
            self.assertFalse(d["physical_certification"])

    def test_6ms_dark_gap_witness(self):
        d=evaluate(example(6.0,2.0))
        self.assertEqual(d["decision"],"POSSIBLE_CONDITIONALLY")
        w=d["witness"]
        self.assertTrue(1.0<w["tau_ms"]<5.0)
        self.assertLessEqual(abs(w["left_slope_mm_ms"]),.567103928+1e-12)
        self.assertLessEqual(w["right_slope_mm_ms"],.274616337+1e-12)

    def test_support_restricts_witness(self):
        self.assertEqual(evaluate(example(6.0,5.0))["decision"],
                         "EXCLUDED_CONDITIONALLY")

    def test_exact_timing_equality_never_excluded(self):
        x=example()
        gap=1000/567.103928+1000/274.616337
        x["exposures"][1].update(
            support_start_ms=gap-1,support_end_ms=gap+1,centroid_ms=gap)
        self.assertNotEqual(evaluate(x)["decision"],"EXCLUDED_CONDITIONALLY")

    def test_nonuniform_kernel_centroid_only(self):
        x=example(6.0,2.0)
        x["exposures"][0]["centroid_ms"]=-.25
        x["exposures"][1]["centroid_ms"]=6.25
        self.assertEqual(evaluate(x)["decision"],"POSSIBLE_CONDITIONALLY")

    def test_no_raw_pixels(self):
        x=example()
        x["observable"]="PIXEL_CONTRAST"
        self.assertEqual(evaluate(x)["decision"],"ABSTAIN_UNCALIBRATED")

    def test_uncertainties_and_nuisances_abstain(self):
        for key in NUISANCES:
            x=example();x["nuisance"][key]="UNKNOWN"
            self.assertEqual(evaluate(x)["decision"],"ABSTAIN_UNCALIBRATED",key)
        for key in ("kernel_normalized","centroid_authenticated","support_authenticated"):
            x=example();x["exposures"][0][key]=False
            self.assertEqual(evaluate(x)["decision"],"ABSTAIN_UNCALIBRATED",key)
        x=example();x["exposures"][1]["clock_uncertainty_ms"]=0.01
        self.assertEqual(evaluate(x)["decision"],"ABSTAIN_UNCALIBRATED")

    def test_overlap_bad_units_and_nonfinite_abstain(self):
        for mutate in (
            lambda x: x["exposures"][0].update(support_end_ms=3.5),
            lambda x: x.update(closing_mm_s=0),
            lambda x: x.update(opening_mm_s=float("nan")),
            lambda x: x.update(mean0_mm=1.0),
            lambda x: x.update(linear_mean_calibrated=False),
            lambda x: x.update(velocity_caps_assumed_for_research=False),
        ):
            x=example();mutate(x)
            self.assertEqual(evaluate(x)["decision"],"ABSTAIN_UNCALIBRATED")

    def test_1000_random_constructive_witnesses(self):
        rng=random.Random(460)
        for _ in range(1000):
            delta=rng.uniform(4,12)
            shutter=rng.uniform(.1,1)
            tau=rng.uniform(shutter/2+.1,delta-shutter/2-.1)
            C=rng.uniform(.05,.8)
            O=rng.uniform(.05,.8)
            alpha=rng.uniform(.1,.99)
            beta=rng.uniform(.1,.99)
            c=rng.uniform(.1,3)
            x=example(delta,shutter)
            x.update(closing_mm_s=C*1000,opening_mm_s=O*1000,closure_mm=c,
                     mean0_mm=c+alpha*C*tau,
                     mean1_mm=c+beta*O*(delta-tau))
            d=evaluate(x)
            self.assertEqual(d["decision"],"POSSIBLE_CONDITIONALLY",d)
            w=d["witness"]
            # Exact independent exposure quadrature for affine witness:
            for exposure,expected in zip(x["exposures"],(x["mean0_mm"],x["mean1_mm"])):
                L,R=exposure["support_start_ms"],exposure["support_end_ms"]
                f=lambda t: c+w["left_slope_mm_ms"]*(t-w["tau_ms"]) if t<=w["tau_ms"] else c+w["right_slope_mm_ms"]*(t-w["tau_ms"])
                avg=(f(L)+f(R))/2
                self.assertAlmostEqual(avg,expected,places=8)

if __name__=="__main__":
    unittest.main()
