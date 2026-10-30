import unittest

from e002_541_coded_light import light, simulate
from e002_542_crossed_stimulus import (
    AMPLITUDES, EDGE_FAIL, RADIOMETRY_FAIL, TRUTH, blur,
    edge_challenge, edge_pulses, frozen_fit, radiometry_challenge, run,
)


class CrossedStimulusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = run()
        cls.signal = light('coded')

    def test_linear_control_passes(self):
        self.assertFalse(self.results['linear']['heldout_falsified'])
        self.assertAlmostEqual(self.results['linear']['heldout_rmse'], 0, places=7)

    def test_gamma_training_false_reassurance(self):
        self.assertEqual(self.results['gamma']['training']['decision'], 'SYNTHETIC_IDENTIFIED')
        self.assertEqual(self.results['gamma']['training']['best'], list(TRUTH))
        self.assertLess(self.results['gamma']['training']['rmse'], RADIOMETRY_FAIL)

    def test_gamma_heldout_rejects_frozen_transfer(self):
        self.assertTrue(self.results['gamma']['heldout_falsified'])
        self.assertAlmostEqual(self.results['gamma']['heldout_rmse'], 0.02630673, places=6)
        self.assertEqual(tuple(AMPLITUDES), (0.25, 0.5))

    def test_instantaneous_control_passes(self):
        self.assertFalse(self.results['instantaneous']['heldout_falsified'])
        self.assertAlmostEqual(self.results['instantaneous']['heldout_max_abs'], 0, places=7)

    def test_blur_training_false_reassurance(self):
        self.assertEqual(self.results['temporal_blur']['training']['decision'], 'SYNTHETIC_IDENTIFIED')
        self.assertEqual(self.results['temporal_blur']['training']['best'], list(TRUTH))
        self.assertLess(self.results['temporal_blur']['training']['rmse'], RADIOMETRY_FAIL)

    def test_blur_heldout_rejects_frozen_transfer(self):
        self.assertTrue(self.results['temporal_blur']['heldout_falsified'])
        self.assertGreater(self.results['temporal_blur']['heldout_max_abs'], EDGE_FAIL)
        self.assertAlmostEqual(self.results['temporal_blur']['heldout_max_abs'], 0.017679, places=5)

    def test_edge_pulses_are_outside_row0_exposure(self):
        pulses = edge_pulses()
        self.assertEqual(len(pulses), 800)
        self.assertEqual(sum(pulses), 40)
        for frame in range(20):
            t = frame * 33 + TRUTH[0]
            self.assertEqual(sum(pulses[t:t + TRUTH[1]]), 0)

    def test_blur_preserves_constant_signal(self):
        self.assertEqual(blur([1.0] * 30), [1.0] * 30)

    def test_wrong_source_fails_closed(self):
        self.assertEqual(self.results['wrong_source'], 'ABSTAIN')

    def test_duplicate_identity_fails_closed(self):
        self.assertEqual(self.results['duplicate_frame'], 'ABSTAIN')

    def test_missing_frames_fail_closed(self):
        self.assertEqual(self.results['missing_frames'], 'ABSTAIN')

    def test_saturation_fails_closed(self):
        self.assertEqual(self.results['saturated'], 'ABSTAIN')

    def test_unmatched_reference_cannot_freeze(self):
        with self.assertRaises(AssertionError):
            frozen_fit(light('coded', 20261031), simulate(self.signal))

    def test_no_physical_or_human_certification(self):
        self.assertEqual(self.results['evidence_tier'], 'SYNTHETIC_INSTRUMENT_ONLY')
        self.assertEqual(self.results['physical_capture_count'], 0)
        self.assertEqual(self.results['human_anatomical_rating_count'], 0)
        self.assertEqual(self.results['continuous_time_human_motion_bounds'], 0)
        self.assertEqual(self.results['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(self.results['release'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
