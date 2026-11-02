"""E002-608 adversarial controls; no human data are used."""
import copy
from fractions import Fraction
import unittest

from e002_608_exposure_gate import evaluate, example, q


class ExposureGateTest(unittest.TestCase):
    def test_hidden_closure_at_exact_boundary(self):
        d=example()
        r=evaluate(d)
        self.assertEqual(r['status'], 'ABSTAIN_HIDDEN_CLOSURE_POSSIBLE')
        self.assertEqual(q(r['strict_margin']), 0)
        # Naive instantaneous endpoint interpretation would exclude incorrectly.
        self.assertGreater(Fraction(3,5), Fraction(1,5))

    def test_conditional_open(self):
        d=example()
        d['left']['aperture_lower']='0.6'
        d['right']['aperture_lower']='0.6'
        r=evaluate(d)
        self.assertEqual(r['status'], 'MODEL_EXCLUDE_CONDITIONAL')
        self.assertEqual(q(r['strict_margin']), Fraction(1,5))
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(r['release'], 'BLOCKED')

    def test_missing_evidence(self):
        d=example()
        d['evidence_sha256']['velocity']='unverified'
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_MISSING_EVIDENCE_DIGEST')

    def test_missing_physical_premise(self):
        d=example()
        d['attestations']['shutter_boxcar_calibrated']=False
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_UNVERIFIED_PREMISE')

    def test_nuisance_fail_closed(self):
        for flag in example()['nuisances']:
            d=example()
            d['nuisances'][flag]=True
            self.assertEqual(evaluate(d)['status'], 'ABSTAIN_NUISANCE')

    def test_uncertainty_monotonic(self):
        d=example()
        d['left']['aperture_lower']='0.6'
        d['right']['aperture_lower']='0.6'
        self.assertEqual(evaluate(d)['status'],'MODEL_EXCLUDE_CONDITIONAL')
        for field in d['uncertainty_ms']:
            x=copy.deepcopy(d)
            x['uncertainty_ms'][field]='20'
            self.assertNotEqual(evaluate(x)['status'], 'MODEL_EXCLUDE_CONDITIONAL')
        x=copy.deepcopy(d)
        x['velocity_upper_per_ms']='0.03'
        self.assertNotEqual(evaluate(x)['status'], 'MODEL_EXCLUDE_CONDITIONAL')
        x=copy.deepcopy(d)
        x['left']['aperture_lower']='0.3'
        self.assertNotEqual(evaluate(x)['status'], 'MODEL_EXCLUDE_CONDITIONAL')

    def test_reject_geometry(self):
        for key,value in [('end_ms',15),('start_ms',0)]:
            d=example()
            d['left'][key]=value
            with self.assertRaises(ValueError):
                evaluate(d)
        d=example()
        d['right']['start_ms']=-1
        with self.assertRaises(ValueError):
            evaluate(d)

    def test_reject_bad_values(self):
        for value in ('nan', 'inf', '-0.1', True):
            d=example()
            d['velocity_upper_per_ms']=value
            with self.assertRaises(ValueError):
                evaluate(d)
        d=example()
        d['left']['aperture_lower']='1.1'
        with self.assertRaises(ValueError):
            evaluate(d)

    def test_zero_velocity(self):
        d=example()
        d['velocity_upper_per_ms']=0
        self.assertEqual(evaluate(d)['status'],'MODEL_EXCLUDE_CONDITIONAL')
        self.assertIsNone(evaluate(d)['dimensionless_ratio'])


if __name__ == '__main__':
    unittest.main()
