import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from e002_574_lpw_plan import plan, write_private


def fixture():
    return {'videos':[{'participant_id':f'p{p:02d}','video_id':f'v{v}',
                       'video_sha256':hashlib.sha256(f'{p}-{v}'.encode()).hexdigest(),
                       'native_frame_count':190 if v==0 else 380}
                      for p in range(22) for v in range(3)]}


class TestLPWPlan(unittest.TestCase):
    def test_split_and_count(self):
        x=plan(fixture())
        self.assertEqual(len(x['development_participants']),11)
        self.assertEqual(len(x['heldout_participants']),11)
        self.assertEqual(x['window_count'],330)
        self.assertEqual(len(x['rater_templates']['A']['clips']),330)
        self.assertEqual(set(x['development_participants'])&set(x['heldout_participants']),set())
        self.assertTrue(all(len(c)==19 for c in x['rater_templates']['B']['clips'].values()))
        self.assertEqual(x['product'],'ABSTAIN_UNCALIBRATED')

    def test_order_independent(self):
        x=fixture(); y=copy.deepcopy(x); y['videos'].reverse()
        self.assertEqual(plan(x),plan(y))

    def test_no_overlap(self):
        x=plan(fixture())
        by_video={}
        for w in x['owner_mapping']:
            key=(w['participant_id'],w['video_id'])
            by_video.setdefault(key,[]).append(set(w['native_frames']))
        self.assertTrue(all(not a&b for sets in by_video.values() for i,a in enumerate(sets) for b in sets[i+1:]))

    def test_blind_templates(self):
        x=plan(fixture())
        t=json.dumps(x['rater_templates'])
        self.assertNotIn('participant_id',t)
        self.assertNotIn('video_sha256',t)
        self.assertNotIn('native_frames',t)
        self.assertNotIn('start_native_frame',t)
        self.assertNotIn('CLOSED',t)
        self.assertNotEqual(x['rater_templates']['A']['rater'],x['rater_templates']['B']['rater'])

    def test_reject_duplicate(self):
        x=fixture();x['videos'][1]['video_sha256']=x['videos'][0]['video_sha256']
        with self.assertRaises(ValueError):plan(x)

    def test_reject_unsafe_ids(self):
        x=fixture();x['videos'][0]['participant_id']='../p00'
        with self.assertRaises(ValueError):plan(x)

    def test_reject_noninteger_count(self):
        x=fixture();x['videos'][0]['native_frame_count']=True
        with self.assertRaises(ValueError):plan(x)

    def test_reject_short_video(self):
        x=fixture();x['videos'][0]['native_frame_count']=18
        with self.assertRaises(ValueError):plan(x)

    def test_reject_missing_participant(self):
        x=fixture();x['videos'][0]['participant_id']='p22'
        with self.assertRaises(ValueError):plan(x)

    def test_reject_missing_video(self):
        x=fixture();x['videos'].pop()
        with self.assertRaises(ValueError):plan(x)

    def test_reject_extra_field(self):
        x=fixture();x['videos'][0]['source_path']='/private'
        with self.assertRaises(ValueError):plan(x)

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'inventory.json';p.write_text(json.dumps(fixture()))
            link=Path(d)/'link.json';link.symlink_to(p)
            with self.assertRaises(ValueError):write_private(link,Path(d)/'out')

    def test_private_output(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'inventory.json';p.write_text(json.dumps(fixture()))
            out=Path(d)/'out'
            y=write_private(p,out)
            self.assertEqual(y['blind_windows'],330)
            self.assertEqual(set(x.name for x in out.iterdir()),{'OWNER_PRIVATE_MAPPING.json','RATER_A_BLANK.json','RATER_B_BLANK.json'})
            with self.assertRaises(ValueError):write_private(p,out)


if __name__=='__main__':
    unittest.main()
