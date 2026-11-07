#!/usr/bin/env python3
"""E002-600 synthetic instrument regression. No human ratings."""
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from e002_600_phantom_rater_challenge import build, grade, blank_template

def ideal(truth, rater='A'):
    packet = blank_template(rater)
    for clip, rows in truth['clips'].items():
        for i, row in enumerate(rows):
            if row['clean']:
                packet['clips'][clip][i] = dict(frame=i,
                    upper_y=row['upper_at_x320'],
                    lower_y=row['lower_at_x320'], iris_diameter=None,
                    uncertainty_px=0.5, measurement_x=320, flags=[])
            else:
                packet['clips'][clip][i]['flags'] = ['OTHER']
    return packet

class ChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        build(cls.root / 'a', 'locked-e002-600')
        build(cls.root / 'b', 'locked-e002-600')
        build(cls.root / 'c', 'different-e002-600')
        cls.truth = json.loads((cls.root/'a/private/truth.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_packet_shape_and_private_truth(self):
        root = self.root/'a'
        imgs = sorted((root/'reviewer/clips').glob('clip_*/frame_*.png'))
        self.assertEqual(len(imgs), 190)
        for path in imgs:
            with Image.open(path) as im:
                self.assertEqual(im.size, (640,480))
            clip = path.parent.name
            idx = int(path.stem.split('_')[-1])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             self.truth['clips'][clip][idx]['sha256'])
        for r in ('A','B'):
            p = json.loads((root/f'reviewer/template_{r}.json').read_text())
            self.assertEqual(p, blank_template(r))
        self.assertFalse(any('truth' in str(p) for p in (root/'reviewer').rglob('*')))

    def test_seed_replay_and_independence(self):
        self.assertEqual((self.root/'a/private/truth.json').read_bytes(),
                         (self.root/'b/private/truth.json').read_bytes())
        self.assertNotEqual((self.root/'a/private/truth.json').read_bytes(),
                            (self.root/'c/private/truth.json').read_bytes())

    def test_ideal_rater_qualifies_but_not_physiology(self):
        out = grade(self.truth, ideal(self.truth))
        self.assertEqual(out['clean_frames'], 114)
        self.assertEqual(out['clean_measured'], 114)
        self.assertEqual(out['clean_interval_covered'], 114)
        self.assertEqual(out['nuisance_frames'], 76)
        self.assertEqual(out['nuisance_abstentions'], 76)
        self.assertTrue(out['qualified_on_synthetic_challenge'])
        self.assertFalse(out['human_validation_of_E002_371'])
        self.assertEqual(out['release'], 'BLOCKED')

    def test_blank_rater_fails_qualification(self):
        out = grade(self.truth, blank_template('B'))
        self.assertEqual(out['clean_measured'], 0)
        self.assertFalse(out['qualified_on_synthetic_challenge'])

    def test_wrong_closed_open_claims_fail(self):
        packet = ideal(self.truth)
        for clip in ('clip_0000','clip_0001'):
            packet['clips'][clip][0].update(upper_y=200, lower_y=202)
        out = grade(self.truth, packet)
        self.assertEqual(out['clean_false_closed'], 2)
        self.assertFalse(out['qualified_on_synthetic_challenge'])

    def test_independent_node_replay(self):
        for packet in (ideal(self.truth), blank_template('A')):
            file = self.root / 'replay_review.json'
            file.write_text(json.dumps(packet))
            out = subprocess.run(['node', str(Path(__file__).with_name('e002_600_independent_replay.cjs')),
                                  str(self.root/'a/private/truth.json'), str(file)],
                                 capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(out.stdout), grade(self.truth, packet))

    def test_bad_schema_abstains(self):
        p = ideal(self.truth)
        p['clips']['clip_0000'][0]['iris_diameter'] = 100
        with self.assertRaises(ValueError): grade(self.truth,p)
        p = ideal(self.truth)
        p['clips']['clip_0000'].pop()
        with self.assertRaises(ValueError): grade(self.truth,p)
        p = ideal(self.truth)
        p['clips']['clip_0000'][0]['measurement_x'] = float('nan')
        with self.assertRaises(ValueError): grade(self.truth,p)

if __name__ == '__main__':
    unittest.main(verbosity=2)
