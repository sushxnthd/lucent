#!/usr/bin/env python3
"""Adversarial tests for E002-514, synthetic-only evidence tier."""
import unittest
from e002_514_coded_optical import (
    CHANNELS, FRAMES, HELD_OUT, blind_gap_upper, compatible_intervals,
    cumulative, integrate, optical_code, physical_gate, run, synthetic_trial,
)

class CodedOpticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sums = cumulative(optical_code(101))

    def test_frozen_heldout_simulation(self):
        r = run()
        self.assertEqual(r['held_out_simulation_gate'], 'PASS')
        self.assertEqual(r['pre_registered_seeds'], list(HELD_OUT))
        self.assertEqual(r['total_evaluated_gaps'], 195)
        self.assertFalse(r['real_physical_instrument_used'])
        self.assertEqual(r['release'], 'BLOCKED')

    def test_all_truths_contained(self):
        for seed in HELD_OUT:
            r=synthetic_trial(seed)
            self.assertEqual(r['true_exposures_contained'], FRAMES)
            self.assertEqual(r['unsafe_gap_underbounds'], 0)

    def test_exhaustive_solver_has_no_nominal_clock_input(self):
        truth=(21,31)
        matches=compatible_intervals(self.sums, integrate(self.sums,21,10))
        self.assertIn(truth,matches)

    def test_missing_channel_rejected(self):
        with self.assertRaisesRegex(ValueError,'INVALID_OPTICAL_OBSERVATION'):
            compatible_intervals(self.sums,(0.5,)*(CHANNELS-1))

    def test_invalid_photometric_value_rejected(self):
        with self.assertRaisesRegex(ValueError,'INVALID_OPTICAL_OBSERVATION'):
            compatible_intervals(self.sums,(float('nan'),)*CHANNELS)

    def test_empty_feasible_abstains(self):
        possible=compatible_intervals(self.sums,(0.5,)*CHANNELS, envelope=0)
        if not possible:
            self.assertIsNone(blind_gap_upper(possible,[(20,30)]))
        else:
            self.assertIsNone(blind_gap_upper([],possible))

    def test_gap_envelope_not_point_estimate(self):
        self.assertEqual(blind_gap_upper([(0,10),(0,8)],[(20,30),(24,35)]),16)
        self.assertIsNone(blind_gap_upper([],[(20,30)]))

    def test_no_physical_clearance_from_synthetic(self):
        r=physical_gate({})
        self.assertEqual(r['status'],'ABSTAIN_UNCALIBRATED')
        self.assertEqual(r['release'],'BLOCKED')
        self.assertFalse(r['physical_validation_by_code'])

    def test_uncalibrated_gain_is_release_blocker(self):
        r=physical_gate({'independent_photodiode_clock':True})
        self.assertIn('bounded_gain_offset',r['missing_controls'])

    def test_rolling_shutter_mapping_is_release_blocker(self):
        r=physical_gate({'verified_exposure_geometry':True})
        self.assertIn('verified_scanline_mapping',r['missing_controls'])

    def test_missing_clock_error_bound_is_release_blocker(self):
        r=physical_gate({'independent_photodiode_clock':True,'measured_optical_code':True})
        self.assertIn('bounded_clock_error',r['missing_controls'])

    def test_missingness_blur_and_ambient_are_release_blockers(self):
        r=physical_gate({})
        for key in ('bounded_missingness_blur','bounded_ambient_brightness'):
            self.assertIn(key,r['missing_controls'])

    def test_all_claimed_controls_still_not_authenticated(self):
        keys=physical_gate({})['missing_controls']
        r=physical_gate({k:True for k in keys})
        self.assertEqual(r['status'],'INPUTS_REPORTED_NOT_INDEPENDENTLY_VERIFIED')
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')
        self.assertFalse(r['physical_validation_by_code'])

    def test_out_of_range_exposure_rejected(self):
        with self.assertRaisesRegex(ValueError,'EXPOSURE_OUT_OF_RANGE'):
            integrate(self.sums,-1,10)

if __name__=='__main__':
    unittest.main()
