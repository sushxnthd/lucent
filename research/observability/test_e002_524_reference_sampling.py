"""Exact adversarial phase and evidence-gate controls for E002-524."""
import importlib.util
from pathlib import Path
from fractions import Fraction as F
import unittest

spec = importlib.util.spec_from_file_location('e002_524_reference_sampling', Path(__file__).with_name('e002_524_reference_sampling.py'))
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
P, E, U, EPS = F(25, 6), F(1), F(1, 10), F(1, 100000)


class ReferenceSampling(unittest.TestCase):
    def test_exact_frozen_thresholds(self):
        b = s.bounds(P, E)
        self.assertEqual(b['ideal_positive_overlap_strict_gt'], F(19, 6))
        self.assertEqual(b['ideal_full_witness_strict_gt'], F(31, 6))
        self.assertEqual(s.bounds(P, E, U)['robust_full_witness_strict_gt'], F(161, 30))
        self.assertEqual(s.bounds(F(1), F(1, 2))['ideal_full_witness_strict_gt'], F(3, 2))
        self.assertEqual(s.bounds(P, E, verified_gap=F(25, 3))['robust_full_witness_strict_gt'], F(28, 3))

    def test_adversarial_no_overlap_at_equality(self):
        d = P - E
        self.assertFalse(s.has_positive_overlap(P, E, d, s.phase_without_overlap(P, E, d)))

    def test_adversarial_no_overlap_below(self):
        d = P - E - EPS
        self.assertFalse(s.has_positive_overlap(P, E, d, s.phase_without_overlap(P, E, d)))

    def test_above_overlap_boundary_all_257_phases(self):
        for i in range(257):
            self.assertTrue(s.has_positive_overlap(P, E, P - E + EPS, P * i / 257))

    def test_full_witness_boundary_equality_has_bad_phase(self):
        d = P + E
        self.assertFalse(s.has_strict_full(P, E, d, s.phase_without_strict_full(P, E, d)))

    def test_full_witness_below_boundary_has_bad_phase(self):
        for d in (F(0), E, E + EPS, P + E - EPS):
            self.assertFalse(s.has_strict_full(P, E, d, s.phase_without_strict_full(P, E, d)))

    def test_above_full_boundary_all_257_phases(self):
        for i in range(257):
            self.assertTrue(s.has_strict_full(P, E, P + E + EPS, P * i / 257))

    def test_robust_full_boundary_equality_bad_phase(self):
        d = P + E + 2 * U
        self.assertFalse(s.has_strict_full(P, E, d, U, U))

    def test_robust_full_above_boundary_all_phases(self):
        for i in range(257):
            self.assertTrue(s.has_strict_full(P, E, P + E + 2 * U + EPS, P * i / 257, U))

    def test_overlap_does_not_imply_full_witness(self):
        d = P
        phi = s.phase_without_strict_full(P, E, d)
        self.assertTrue(s.has_positive_overlap(P, E, d, phi))
        self.assertFalse(s.has_strict_full(P, E, d, phi))

    def test_reject_invalid_acquisition(self):
        for p,e,u in ((F(0),E,F(0)), (P,F(0),F(0)), (P,P,F(0)), (P,P+EPS,F(0)), (P,E,-EPS)):
            with self.assertRaises(ValueError):
                s.bounds(p,e,u)

    def test_reject_bad_duration_or_phase(self):
        with self.assertRaises(ValueError):
            s.has_positive_overlap(P,E,F(-1),F(0))
        with self.assertRaises(ValueError):
            s.has_strict_full(P,E,F(1),P)
        with self.assertRaises(ValueError):
            s.phase_without_overlap(P,E,P)
        with self.assertRaises(ValueError):
            s.phase_without_strict_full(P,E,P+E+EPS)

    def test_reject_bad_gap(self):
        with self.assertRaises(ValueError):
            s.bounds(P,E,verified_gap=F(0))

    def test_real_claim_defaults_to_abstention(self):
        self.assertEqual(s.gate_reference_claim(P,E,P+E+F(100)), 'ABSTAIN_UNCALIBRATED')

    def test_missing_one_attestation_abstains(self):
        flags = dict(verified_gap=P,native_indices_authenticated=True,shutter_calibrated=True,
                     clock_calibrated=True,anatomy_two_independent_raters=True,
                     cross_camera_transport_calibrated=True,duration_independently_attested=True)
        for key in flags:
            if key == 'verified_gap':
                continue
            mutated = dict(flags)
            mutated[key] = False
            self.assertEqual(s.gate_reference_claim(P,E,P+E+F(100),**mutated), 'ABSTAIN_UNCALIBRATED')

    def test_conditional_not_product_release(self):
        flags = dict(verified_gap=P,native_indices_authenticated=True,shutter_calibrated=True,
                     clock_calibrated=True,anatomy_two_independent_raters=True,
                     cross_camera_transport_calibrated=True,duration_independently_attested=True)
        self.assertEqual(s.gate_reference_claim(P,E,P+E+2*U,U,**flags), 'REFERENCE_CENSORED_OR_PHASE_DEPENDENT')
        self.assertEqual(s.gate_reference_claim(P,E,P+E+2*U+EPS,U,**flags), 'CONDITIONAL_FULL_WITNESS_OPPORTUNITY')
        dropped = dict(flags, verified_gap=2*P)
        self.assertEqual(s.gate_reference_claim(P,E,P+E+2*U+EPS,U,**dropped), 'REFERENCE_CENSORED_OR_PHASE_DEPENDENT')
        self.assertEqual(s.gate_reference_claim(P,E,2*P+E+2*U+EPS,U,**dropped), 'CONDITIONAL_FULL_WITNESS_OPPORTUNITY')
        del flags['verified_gap']
        self.assertEqual(s.gate_reference_claim(P,E,2*P+E+2*U+EPS,U,**flags), 'ABSTAIN_UNCALIBRATED')

    def test_boolean_not_accepted_as_numeric(self):
        with self.assertRaises(TypeError):
            s.bounds(True, E)
        with self.assertRaises(ValueError):
            s.gate_reference_claim(P,E,P+E, native_indices_authenticated=1)


if __name__ == '__main__':
    unittest.main()
