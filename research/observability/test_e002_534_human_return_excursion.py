import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e002_534_human_return_excursion as module
from e002_534_human_return_excursion import (measurements, candidate, quality_ok,
    analyze_stream, transform)

class ReturnExcursionTests(unittest.TestCase):
    def setUp(self):
        self.frames = [np.full((288,320), 100, dtype=np.uint8) for _ in range(6)]
        self.ids = list(range(6))
        self.times = [0.007*i for i in range(6)]

    def test_localized_return(self):
        self.frames[2][118:190,100:230] = 20
        m = measurements(self.frames)
        self.assertTrue(candidate(m))
        self.assertAlmostEqual(m['eye'][0], 0)
        self.assertGreater(m['eye'][1], 70)

    def test_global_flash_rejected(self):
        self.frames[2][:] = 180
        self.assertFalse(candidate(measurements(self.frames)))

    def test_linear_interpolation_rejected(self):
        for i, f in enumerate(self.frames):
            f[118:190,100:230] = 100 + 10*i
        self.assertFalse(candidate(measurements(self.frames)))

    def test_time_and_id_censor(self):
        self.assertTrue(quality_ok(self.ids, self.times))
        self.assertFalse(quality_ok(self.ids, [0,.007,.014,.050,.057,.064]))
        self.assertFalse(quality_ok([0,1,2,4,5,6], self.times))

    def test_nuisance_transform(self):
        self.frames[2][118:190,100:230] = 20
        self.assertTrue(candidate(measurements(transform(self.frames, 'blur_sigma2'))))
        self.assertTrue(candidate(measurements(transform(self.frames, 'gain_120'))))

    def test_stream_counts(self):
        imgs = [np.full((288,320),100,dtype=np.uint8) for _ in range(16)]
        imgs[2][118:190,100:230] = 20
        ids = list(range(16))
        times = [0.007*i for i in ids]
        with patch.object(module, "LIMIT", 16):
            result = analyze_stream(imgs, ids, times)
        self.assertEqual(result['0']['eye_specific'], 1)
        self.assertEqual(result['0']['rejected_time_or_id'], 0)
        self.assertEqual(result['0']['eligible'], 3)
        self.assertEqual(result['2']['eligible'], 2)
        self.assertEqual(result['0']['blur_survivors'], 1)
        self.assertEqual(result['0']['gain_survivors'], 1)

if __name__=='__main__': unittest.main()
