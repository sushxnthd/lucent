import unittest
from e002_462_finite_dwell import run, witness

class FiniteDwell(unittest.TestCase):
    def test_frozen_witnesses_exactly_indistinguishable(self):
        for r in run():
            self.assertTrue(r['identical_to_constant_open'],r)
            self.assertEqual(r['max_shutter_mean_difference_mm'],0.0)
            self.assertGreater(r['subthreshold_duration_ms'],0)
            self.assertGreater(r['excursion_support_ms'][0],r['shutter_dark_gap_ms'][0])
            self.assertLess(r['excursion_support_ms'][1],r['shutter_dark_gap_ms'][1])

    def test_moving_phase_detects_excursion(self):
        r=witness(400,2.3,1.95,.1,.2)
        self.assertFalse(r['identical_to_constant_open'])
        self.assertGreater(r['max_shutter_mean_difference_mm'],0)

    def test_invalid_model_rejected(self):
        for args in [(400,2.3,2.0,.1,.9),(400,2.3,1.95,-.1,.9),
                     (2000,2.3,1.95,.1,.9,.8)]:
            with self.assertRaises(ValueError):witness(*args)

if __name__=='__main__':unittest.main()
