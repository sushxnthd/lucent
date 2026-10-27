#!/usr/bin/env python3
"""Adversarial E002-485 tests; standard library only."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from e002_485_heldout_gap import (Frame, analyze, clean_pair, load_csv,
                                  synthetic_fixture)


class HeldoutGapTests(unittest.TestCase):
    def fixture(self):
        d = tempfile.TemporaryDirectory()
        p = Path(d.name) / 'annotations.csv'
        synthetic_fixture(p)
        self.addCleanup(d.cleanup)
        return p

    def test_synthetic_falsification_and_abstentions(self):
        result = analyze(load_csv(self.fixture()), synthetic=True)
        self.assertEqual(result['counts']['falsified_joint_assumptions'], 1)
        self.assertEqual(result['counts']['abstain_nuisance_or_missing'], 2)
        self.assertEqual(result['counts']['conditional_excluded'], 2)
        self.assertGreater(result['heldout_secant_proxy_exceedances'], 0)

    def test_never_claims_physical_release(self):
        result = analyze(load_csv(self.fixture()), synthetic=True)
        self.assertEqual(result['product_release'], 'BLOCKED')
        self.assertFalse(result['proxy_is_hard_velocity_bound'])
        self.assertEqual(result['physical_claims'], 'ABSTAIN_UNCALIBRATED')

    def test_real_mode_requires_prespecified_subjects(self):
        with self.assertRaisesRegex(ValueError, '20/11'):
            analyze(load_csv(self.fixture()), synthetic=False)

    def test_missing_frame_not_bridged(self):
        a = Frame('S21', 'Sess01', 0, 0.0, .8, .01, 'ok')
        b = Frame('S21', 'Sess01', 2, 13.3333, .8, .01, 'ok')
        self.assertFalse(clean_pair(a, b))

    def test_blur_not_interpreted_as_closure(self):
        a = Frame('S21', 'Sess01', 0, 0.0, .8, .01, 'ok')
        b = Frame('S21', 'Sess01', 1, 6.6667, .1, .01, 'blur')
        self.assertFalse(clean_pair(a, b))

    def test_bad_measurement_rejected(self):
        path = self.fixture()
        with path.open(newline='') as h:
            rows = list(csv.reader(h))
        rows[1][4] = 'nan'
        with path.open('w', newline='') as h:
            csv.writer(h).writerows(rows)
        with self.assertRaisesRegex(ValueError, 'nonfinite'):
            load_csv(path)

    def test_duplicate_frame_rejected(self):
        path = self.fixture()
        with path.open(newline='') as h:
            rows = list(csv.reader(h))
        rows[2][2] = rows[1][2]
        with path.open('w', newline='') as h:
            csv.writer(h).writerows(rows)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            load_csv(path)

    def test_zero_velocity_calibration_not_automatically_success(self):
        path = self.fixture()
        groups = load_csv(path)
        key = ('S01', 'Sess01')
        groups[key] = [Frame(f.subject, f.session, f.idx, f.t, .8, 0, 'ok') for f in groups[key]]
        result = analyze(groups, synthetic=True)
        self.assertGreaterEqual(result['counts']['falsified_joint_assumptions'], 1)
        json.dumps(result, allow_nan=False)  # Infinity must never leak into JSON numbers

    def test_every_heldout_subject_must_have_clean_window(self):
        groups = load_csv(self.fixture())
        cal = groups[('S01', 'Sess01')]
        good = groups[('S22', 'Sess01')]
        for i in range(2, 21):
            subject = f'S{i:02d}'
            groups[(subject, 'Sess01')] = [Frame(subject, f.session, f.idx, f.t, f.a, f.u, f.quality) for f in cal]
        for i in range(25, 32):
            subject = f'S{i:02d}'
            groups[(subject, 'Sess01')] = [Frame(subject, f.session, f.idx, f.t, f.a, f.u, 'blur' if i == 31 else f.quality) for f in good]
        with self.assertRaisesRegex(ValueError, 'clean-window coverage'):
            analyze(groups, synthetic=False)

    def test_invalid_clock_error_rejected(self):
        with self.assertRaisesRegex(ValueError, 'invalid threshold'):
            analyze(load_csv(self.fixture()), clock_ms=4, synthetic=True)

    def test_quality_unknown_fails_closed(self):
        path = self.fixture()
        groups = load_csv(path)
        key = ('S22', 'Sess01')
        groups[key] = [Frame(f.subject, f.session, f.idx, f.t, f.a, f.u, 'unknown') for f in groups[key]]
        result = analyze(groups, synthetic=True)
        self.assertEqual(result['counts']['abstain_nuisance_or_missing'], 3)


if __name__ == '__main__':
    unittest.main()
