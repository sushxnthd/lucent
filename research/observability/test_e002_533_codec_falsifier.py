"""E002-533 frozen predictions and release-gate tests (actual ffmpeg codecs)."""
from __future__ import annotations

import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from e002_533_codec_falsifier import run_suite


class CodecInstrumentFalsifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='lucent533_test_')
        cls.results = run_suite(Path(cls.temp.name))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_lossless_linear_identifies_grid_candidate(self):
        r = self.results['lossless_linear']
        self.assertEqual(r['feasible_train_count'], 1)
        self.assertEqual(r['fit_grid_only'], {'delta_ms':'1','exposure_ms':'2','row_delay_ms':'1/2'})
        self.assertLessEqual(float(Fraction(r['heldout_max_abs_error'])), .02)

    def test_h264_linear_identifies_grid_candidate(self):
        r = self.results['h264_linear']
        self.assertEqual(r['feasible_train_count'], 1)
        self.assertEqual(r['fit_grid_only']['exposure_ms'], '2')
        self.assertLessEqual(float(Fraction(r['heldout_max_abs_error'])), .02)

    def test_gamma_without_photometry_falsifies_model(self):
        r = self.results['h264_gamma_uncorrected']
        self.assertIn(r['decision'], ('MODEL_FALSIFIED', 'FALSIFIED_HELDOUT'))
        self.assertGreater(r['observed_max_abs_deviation_from_truth'], .1)

    def test_independently_specified_gamma_inverse_recovers(self):
        r = self.results['h264_gamma_corrected']
        self.assertEqual(r['fit_grid_only'], {'delta_ms':'1','exposure_ms':'2','row_delay_ms':'1/2'})
        self.assertLessEqual(float(Fraction(r['heldout_max_abs_error'])), .02)

    def test_heldout_glare_does_not_refit(self):
        r = self.results['h264_heldout_glare']
        self.assertEqual(r['feasible_train_count'], 1)
        self.assertEqual(r['decision'], 'FALSIFIED_HELDOUT')
        self.assertEqual(r['holdout_rows'], 30)

    def test_missing_native_censored_not_interpolated(self):
        r = self.results['h264_missing_native']
        self.assertEqual(r['missing_rows'], 1)
        self.assertEqual(r['holdout_rows'], 29)
        self.assertEqual(r['feasible_train_count'], 1)

    def test_second_decoder_agrees(self):
        for name, r in self.results.items():
            if name.startswith('_'):
                continue
            self.assertLessEqual(r['independent_decoder_max_abs_delta'], .02)

    def test_no_physical_or_human_claim(self):
        for name, r in self.results.items():
            if name.startswith('_'):
                continue
            self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')
            self.assertEqual(r['release'], 'BLOCKED')
            self.assertEqual(r['evidence_tier'], 'SYNTHETIC_OPTICAL_SCENE_REAL_CODEC_NOT_CAMERA')
        self.assertEqual(self.results['_environment']['physical_measurements'], 0)
        self.assertEqual(self.results['_environment']['human_measurements'], 0)


if __name__ == '__main__':
    unittest.main()
