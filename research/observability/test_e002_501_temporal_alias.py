#!/usr/bin/env python3
"""Frozen synthetic adversaries for E002-501, not authentic human outcomes."""
import unittest
from unittest.mock import patch
import numpy as np
from e002_501_temporal_alias import (N, classify_window, transform, screen, analyze,
                                      MAX_FRAMES)


def base():
    yy, xx = np.mgrid[0:N, 0:N]
    return np.uint8(np.clip(45 + xx * 1.8 + yy * 0.8 + ((xx+yy) % 5) * 3, 0, 255))


def six(pulse=False, monotone=False):
    b = base()
    frames = []
    for i in range(6):
        f = b.astype(np.int16).copy()
        f[24:32, 24:32] += i % 2
        if pulse and i in (2, 3):
            f[16:48,16:48] += 38
        if monotone:
            f[16:48,16:48] += i * 9
        frames.append(np.clip(f, 0, 255).astype(np.uint8))
    return np.stack(frames)


class TestE002501(unittest.TestCase):
    def test_reversible_pulse_is_visible_between_matching_endpoints(self):
        self.assertEqual(classify_window(six(pulse=True)), 'IMAGE_ALIAS_CANDIDATE')

    def test_monotone_change_not_hidden(self):
        self.assertEqual(classify_window(six(monotone=True)), 'ENDPOINT_DIFFERENT')

    def test_static_duplicate_abstains(self):
        self.assertEqual(classify_window(np.stack([base()]*6)), 'ABSTAIN_DUPLICATE')

    def test_global_brightness_corrected(self):
        a = six(pulse=True)
        self.assertEqual(classify_window(transform(a,'brightness_plus8')), 'IMAGE_ALIAS_CANDIDATE')

    def test_large_global_brightness_abstains(self):
        a = six(pulse=True)
        a[2] = np.minimum(a[2].astype(np.uint16)+30,255).astype(np.uint8)
        self.assertEqual(classify_window(a), 'ABSTAIN_PHOTOMETRIC')

    def test_border_nuisance_abstains(self):
        a = six(pulse=True)
        a[2,:8,:] = np.minimum(a[2,:8,:].astype(np.uint16)+50,255).astype(np.uint8)
        self.assertIn(classify_window(a), ('ABSTAIN_BORDER','ABSTAIN_PHOTOMETRIC'))

    def test_blur_is_a_real_transformation(self):
        a = six(pulse=True)
        b = transform(a,'blur_3x3')
        self.assertEqual(b.shape,a.shape)
        self.assertFalse(np.array_equal(a,b))

    def test_jitter_is_a_real_transformation(self):
        a = six(pulse=True)
        b = transform(a,'alternating_jitter_1px')
        self.assertEqual(b.shape,a.shape)
        self.assertFalse(np.array_equal(a,b))

    def test_screen_reports_only_counts_and_internal_candidate_set(self):
        a = np.concatenate([six(pulse=True), six(monotone=True)])
        counts, indices = screen(a, [0,6])
        self.assertEqual(indices,{0})
        self.assertEqual(sum(counts.values()),2)

    def test_reject_invalid_window(self):
        with self.assertRaisesRegex(ValueError,'INVALID_WINDOW'):
            classify_window(np.zeros((5,N,N),dtype=np.uint8))

    def test_reject_invalid_condition(self):
        with self.assertRaisesRegex(ValueError,'UNKNOWN_CONDITION'):
            transform(six(),'unlisted')

    def test_reject_out_of_bounds(self):
        with self.assertRaisesRegex(ValueError,'INVALID_WINDOW_START'):
            screen(six(),[1])

    def test_full_aggregate_never_promotes_product(self):
        a = np.tile(six(), (MAX_FRAMES//6,1,1))
        with patch('e002_501_temporal_alias.STARTS',np.array([0,5],dtype=np.int32)):
            out=analyze(a)
        self.assertEqual(out['anatomical_closure_labels'],0)
        self.assertFalse(out['physical_hidden_closure_certified'])
        self.assertEqual(out['release'],'BLOCKED')
        self.assertEqual(out['surrogate_windows'],2)
        self.assertNotIn('candidate_native_frame_indices',out)


if __name__=='__main__':
    unittest.main()
