import csv
import importlib.util
import pathlib
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location('e002_515_physical_replay', HERE / 'e002_515_physical_replay.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PhysicalReplay(unittest.TestCase):
    def setUp(self):
        self.wave = []
        for i in range(30):
            self.wave.append((float(i), float(i+1), tuple(float((i >> k) & 1) for k in range(8))))
        self.truth = {'f0': (2., 12., 0.), 'f1': (16., 26., 0.)}
        self.camera = []
        for name, (a,b,u) in self.truth.items():
            values = tuple(sum(row[2][k] for row in self.wave[int(a):int(b)]) / (b-a) for k in range(8))
            self.camera.append((name, values))

    def test_fixture_is_not_physical_evidence(self):
        r = m.replay(self.wave, self.camera, self.truth, 0.0, 0.0)
        self.assertEqual(r['reference_exposures_not_covered'], 0)
        self.assertEqual(r['unsafe_gap_underbounds_vs_reference_envelope'], 0)
        self.assertFalse(r['independent_instrument_identity_verified_by_code'])
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_reference_shift_falsifies_claim(self):
        tampered = dict(self.truth)
        tampered['f1'] = (17., 27., 0.)
        r = m.replay(self.wave, self.camera, tampered, 0., 0.)
        self.assertGreater(r['reference_exposures_not_covered'], 0)
        self.assertEqual(r['instrument_validation_result'], 'FAIL_REFERENCE_COVERAGE')

    def test_missing_candidate_abstains(self):
        wrong = [('f0', tuple([0.333333]*8)), self.camera[1]]
        r = m.replay(self.wave, wrong, self.truth, 0., 0.)
        self.assertGreater(r['empty_candidate_frames'], 0)
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_duplicate_camera_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'camera.csv'
            with p.open('w', newline='') as f:
                w = csv.writer(f); w.writerow(['frame_id', *m.CHANNELS])
                w.writerow(['x', *([0.]*8)]); w.writerow(['x', *([0.]*8)])
            with self.assertRaisesRegex(ValueError, 'DUPLICATE_FRAME_ID'):
                m.observations(p)

    def test_gap_in_photodiode_time_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'wave.csv'
            with p.open('w', newline='') as f:
                w = csv.writer(f); w.writerow(['start_ms', 'end_ms', *m.CHANNELS])
                w.writerow([0, 1, *([0.]*8)]); w.writerow([2, 3, *([0.]*8)])
            with self.assertRaisesRegex(ValueError, 'WAVEFORM_CLOCK_DISCONTINUITY'):
                m.waveform(p)

    def test_nonfinite_and_boolean_not_trusted(self):
        with self.assertRaisesRegex(ValueError, 'NONFINITE'):
            m.finite_float('nan', 'TIME')
        with self.assertRaises(ValueError):
            m.replay(self.wave, self.camera, self.truth, 0., float('nan'))

    def test_mismatched_reference_rejected(self):
        with self.assertRaisesRegex(ValueError, 'REFERENCE_FRAME_SET_MISMATCH'):
            m.replay(self.wave, self.camera, {'f0': self.truth['f0']}, 0., 0.)

    def test_out_of_range_truth_rejected(self):
        with self.assertRaisesRegex(ValueError, 'REFERENCE_OUTSIDE_WAVEFORM'):
            m.replay(self.wave, self.camera, {'f0': (2.,12.,0.), 'f1':(22.,32.,0.)}, 0., 0.)

    def test_timing_envelope_widens_gap_bound(self):
        a = m.replay(self.wave, self.camera, self.truth, 0., 0.)
        b = m.replay(self.wave, self.camera, self.truth, 0., 1.)
        self.assertGreaterEqual(b['worst_gap_margin_ms'], a['worst_gap_margin_ms'])

    def test_reference_uncertainty_makes_gap_test_stricter(self):
        r = m.replay(self.wave, self.camera, {'f0':(2.,12.,0.5),'f1':(16.,26.,0.5)},0.,0.)
        self.assertGreater(r['reference_exposures_not_covered'], 0)
        self.assertEqual(r['instrument_validation_result'], 'FAIL_REFERENCE_COVERAGE')
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_unbounded_residual_rejected(self):
        with self.assertRaisesRegex(ValueError, 'INVALID_RESIDUAL_ENVELOPE'):
            m.candidates(self.wave, self.camera[0][1], -0.1)

    def test_no_nominal_fps_dependency(self):
        r = m.replay(self.wave, self.camera, self.truth, 0., 0.)
        self.assertNotIn('fps', r)


if __name__ == '__main__':
    unittest.main()
