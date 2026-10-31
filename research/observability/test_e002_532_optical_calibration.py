"""Adversarial checks for E002-532, synthetic instrument only."""
import copy
import unittest

from e002_532_optical_calibration import evaluate, synthetic_input


class OpticalCalibrationTests(unittest.TestCase):
    def setUp(self):
        self.x=synthetic_input()

    def test_frozen_training_identifies_truth_and_heldout(self):
        out=evaluate(self.x)
        self.assertEqual(out['candidate_count'],36)
        self.assertEqual(out['feasible_train_count'],1)
        self.assertEqual(out['fit_grid_only'],{'delta_ms':'1','exposure_ms':'2','row_delay_ms':'1/2'})
        self.assertEqual(out['heldout_max_abs_error'],'0')
        self.assertEqual(out['decision'],'UNVERIFIED_PHYSICAL_INPUT')
        self.assertEqual(out['product'],'ABSTAIN_UNCALIBRATED')

    def test_phase_locked_steady_led_is_unidentifiable(self):
        self.x['pulses']=[dict(start_ms='-5',end_ms='205')]
        for f in self.x['frames']: f['brightness']='1'
        out=evaluate(self.x)
        self.assertEqual(out['feasible_train_count'],36)
        self.assertEqual(out['decision'],'AMBIGUOUS_GRID')

    def test_wrong_global_shutter_model_is_falsified(self):
        self.x['grid']['row_delay_ms']=['0']
        self.assertEqual(evaluate(self.x)['decision'],'MODEL_FALSIFIED')

    def test_heldout_corruption_is_not_refit(self):
        self.x['frames'][30]['brightness']='1/10'
        self.assertEqual(evaluate(self.x)['decision'],'FALSIFIED_HELDOUT')

    def test_heldout_not_used_to_select_candidate(self):
        out=evaluate(self.x)
        self.x['frames'][30]['brightness']='1/10'
        bad=evaluate(self.x)
        self.assertEqual(out['feasible_train_count'],bad['feasible_train_count'])

    def test_missing_rows_count_and_abstain(self):
        f=self.x['frames'][31]
        f.pop('brightness'); f['valid']=False
        out=evaluate(self.x)
        self.assertEqual(out['missing_rows'],1)
        self.assertEqual(out['holdout_rows'],29)

    def test_unverified_photometry_prevents_certificate(self):
        self.x['attestations']={k:True for k in self.x['attestations']}
        out=evaluate(self.x)
        self.assertEqual(out['decision'],'SYNTHETIC_GRID_FIT_ONLY')
        self.assertEqual(out['release'],'BLOCKED')

    def test_self_asserted_physical_flags_do_not_certify(self):
        self.x['evidence_tier']='physical_input_unverified'
        self.x['attestations']={k:True for k in self.x['attestations']}
        self.assertEqual(evaluate(self.x)['decision'],'GRID_FIT_ONLY_NOT_PHYSICAL_CERTIFICATE')

    def test_duplicate_native_frame_row_refused(self):
        self.x['frames'].append(copy.deepcopy(self.x['frames'][0]))
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_missing_train_or_holdout_refused(self):
        self.x['frames']=[f for f in self.x['frames'] if f['partition']=='train']
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_nonmonotone_pulses_refused(self):
        self.x['pulses'][1]['start_ms']='0'
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_zero_exposure_refused(self):
        self.x['grid']['exposure_ms']=['0']
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_negative_delay_refused(self):
        self.x['grid']['row_delay_ms']=['-1']
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_out_of_range_brightness_refused(self):
        self.x['frames'][0]['brightness']='11/10'
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_nonfinite_brightness_refused(self):
        self.x['frames'][0]['brightness']='NaN'
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_missing_row_must_not_supply_brightness(self):
        self.x['frames'][0]['valid']=False
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_unknown_evidence_tier_refused(self):
        self.x['evidence_tier']='physically_certified'
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_no_heldout_coverage_refused(self):
        for f in self.x['frames']:
            if f['partition']=='holdout':
                f.pop('brightness'); f['valid']=False
        with self.assertRaises(ValueError):evaluate(self.x)


if __name__=='__main__':unittest.main()
