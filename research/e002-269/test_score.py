#!/usr/bin/env python3
"""Frozen synthetic controls; no human physiology is inferred."""
import csv, pathlib, sys, tempfile, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'research'/'e002-268'))
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from audit import make_rows, FIELDS
from score import score
from evaluate import load
MANIFEST=dict(reference_kind='native_time_same_eye_diameter',
 synchronization='independently_verified_exposure_clock',rgb_modality='visible_color',
 reference_interpolated=False,source_dataset_sha256='synthetic-not-human',
 participant_split_frozen=True,preoutcome_protocol='E002-261',camera_fps=60,
 data_type='synthetic',independent_clock_error_bound_s=0)
def parsed(rows):
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d)/'x.csv'
        with p.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
        return load(p)
class BlindScoreTest(unittest.TestCase):
    def test_complete_denominator(self):
        r=score(parsed(make_rows()),MANIFEST)
        self.assertEqual((r['test_participants'],r['test_windows'],r['blind_admitted'],
                          r['scorable_admitted'],r['passed']),(8,16,16,16,8))
        self.assertEqual(r['conditional_accuracy'],.5)
        self.assertFalse(r['product_certificate'])
        self.assertFalse(r['statistical_candidate'])
    def test_reference_mutation_does_not_change_admission(self):
        rows=make_rows();r1=score(parsed(rows),MANIFEST)
        for x in rows:
            if x['split']=='test' and x['session_id']=='b':x['reference_mm']=4.0
        r2=score(parsed(rows),MANIFEST)
        self.assertEqual([(x['participant'],x['session'],x['admitted']) for x in r1['windows']],
                         [(x['participant'],x['session'],x['admitted']) for x in r2['windows']])
        self.assertEqual(r2['unscorable_admitted'],8)
        self.assertEqual(r2['blind_admitted'],16)
    def test_no_clock_evidence_fails_closed(self):
        m=dict(MANIFEST);m.pop('independent_clock_error_bound_s')
        r=score(parsed(make_rows()),m)
        self.assertEqual(r['passed'],0)
        self.assertFalse(r['product_certificate'])
    def test_invalid_clock_bound_rejected(self):
        m=dict(MANIFEST,independent_clock_error_bound_s=-.1)
        with self.assertRaisesRegex(ValueError,'BAD_CLOCK_BOUND'):score(parsed(make_rows()),m)
    def test_reference_missing_still_in_denominator(self):
        rows=make_rows()
        for x in rows:
            if x['participant_id']=='p02' and x['session_id']=='a':x['valid_ref']='0'
        r=score(parsed(rows),MANIFEST)
        self.assertEqual(r['blind_admitted'],16)
        self.assertEqual(r['unscorable_admitted'],1)
        self.assertEqual(r['passed'],7)
if __name__=='__main__':unittest.main()
