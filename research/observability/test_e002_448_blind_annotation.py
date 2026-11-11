"""E002-448 independent synthetic adversarial tests; not human validation."""
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from e002_448_blind_annotation import (WIDTH, HEIGHT, FIXED_WINDOW, select_indices,
    grayscale_png, build_pack, aperture, adjudicate)


def times():
    t = [0.0]
    for i in range(1,FIXED_WINDOW):
        t.append(t[-1] + (.025 if i in (50,500,2500,6500) else .007))
    return t


def row(vid,ap=0.1,flags=None):
    return {'view_id':vid,'status':'abstain' if flags else 'valid','flags':flags or [],
            'points':{'L':[50,120],'R':[250,120],'U':[160,110],
                      'D':[160,110+ap*200]}}


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        self.sel=select_indices(times(),blind_key='0a'*24)
        self.master={'experiment':'E002-448','pilot':'S19',
                     'views':self.sel['views'],'medium_intervals':self.sel['medium_intervals'],
                     'control_intervals':self.sel['control_intervals']}
        self.r1={'rater_id':'A','annotations':[row(v['view_id']) for v in self.sel['views']]}
        self.r2={'rater_id':'B','annotations':[row(v['view_id']) for v in self.sel['views']]}

    def test_frozen_strata_and_seal(self):
        self.assertEqual(self.sel['medium_intervals'],[50,500,2500,6500])
        self.assertEqual(len(self.sel['control_intervals']),4)
        self.assertEqual(len(self.sel['views'])-len(self.sel['unique_frame_indices']),12)
        self.assertTrue(all(0<=i<12000 for i in self.sel['unique_frame_indices']))

    def test_hmac_blinding(self):
        other=select_indices(times(),blind_key='0b'*24)
        self.assertNotEqual([v['view_id'] for v in self.sel['views']],[v['view_id'] for v in other['views']])
        self.assertEqual(self.sel['control_intervals'],other['control_intervals'])
        self.assertNotIn('50',self.sel['views'][0]['view_id'])

    def test_bad_clock(self):
        t=times();t[3]=t[2];self.assertRaises(ValueError,select_indices,t)
        t=times();t[2]=float('nan');self.assertRaises(ValueError,select_indices,t)
        self.assertRaises(ValueError,select_indices,[i*.007 for i in range(12000)],'bad')

    def test_no_positive_stratum(self):
        self.assertRaises(ValueError,select_indices,[i*.007 for i in range(12000)],'0a'*24)

    def test_png_real_encoding(self):
        raw=bytes([17,18,19,20,21,22]);png=grayscale_png(raw,3,2)
        self.assertTrue(png.startswith(b'\x89PNG\r\n\x1a\n'))
        self.assertEqual(struct.unpack('>II',png[16:24]),(3,2))
        n=struct.unpack('>I',png[33:37])[0]
        self.assertEqual(zlib.decompress(png[41:41+n]),b'\x00\x11\x12\x13\x00\x14\x15\x16')
        self.assertRaises(ValueError,grayscale_png,b'123',3,2)

    def test_build_pack_blinds_mapping_and_keeps_master_private(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'pack';blank=bytes([128])*(WIDTH*HEIGHT)
            result=build_pack((blank for _ in range(FIXED_WINDOW)),self.sel,root)
            self.assertEqual(result['human_labels_collected'],0)
            self.assertEqual(result['blinded_views'],len(self.sel['views']))
            manifest=(root/'rater_pack/manifest.json').read_text()
            self.assertNotIn('frame_index',manifest)
            self.assertNotIn('medium_intervals',manifest)
            self.assertNotIn('private_blind_key',manifest)
            self.assertTrue((root/'PRIVATE_MASTER_DO_NOT_SHARE.json').exists())
            self.assertTrue((root/'rater_pack/rater.html').exists())
            self.assertEqual(len(list((root/'rater_pack/frames').glob('*.png'))),len(self.sel['views']))
            self.assertRaises(FileExistsError,build_pack,[],self.sel,root)

    def test_geometry(self):
        self.assertAlmostEqual(aperture(row('x')),0.1)
        self.assertIsNone(aperture(row('x',flags=['motion_blur'])))
        r=row('x');r['points']['L']=[150,120];r['points']['R']=[160,120]
        self.assertIsNone(aperture(r))
        r=row('x');r['points']['D']=[319,130]
        self.assertIsNone(aperture(r))
        r=row('x');r['points']['D']=[160,109]
        self.assertIsNone(aperture(r))
        r=row('x');r['points']['U']=[float('nan'),110]
        self.assertIsNone(aperture(r))

    def test_two_rater_consensus_is_only_2d(self):
        out=adjudicate(self.master,self.r1,self.r2)
        self.assertEqual(out['eligible_consensus_frames'],len(self.sel['unique_frame_indices']))
        self.assertEqual(out['eligible_candidate_pairs'],8)
        self.assertAlmostEqual(out['consensus_aperture_p50'],.1)
        self.assertFalse(out['physical_release_authorized'])
        self.assertEqual(out['product_claim'],'ABSTAIN_UNCALIBRATED')

    def test_unlabeled_abstains(self):
        out=adjudicate(self.master)
        self.assertEqual(out['annotation_status'],'ZERO_HUMAN_LABELS')
        self.assertIsNone(out['consensus_aperture_p50'])

    def test_independent_raters(self):
        self.assertRaises(ValueError,adjudicate,self.master,self.r1,{**self.r2,'rater_id':'A'})

    def test_disagreement_abstains(self):
        self.r2['annotations'][0]=row(self.r2['annotations'][0]['view_id'],ap=.25)
        out=adjudicate(self.master,self.r1,self.r2)
        self.assertEqual(out['between_rater_disagreements'],1)
        self.assertLess(out['eligible_consensus_frames'],len(self.sel['unique_frame_indices']))

    def test_hidden_repeat_self_consistency(self):
        repeated=next(v for v in self.sel['views'] if v['repeat'])
        vid=repeated['view_id']
        for rat in (self.r1,self.r2):
            for j,r in enumerate(rat['annotations']):
                if r['view_id']==vid:rat['annotations'][j]=row(vid,ap=.14)
        out=adjudicate(self.master,self.r1,self.r2)
        self.assertEqual(out['repeat_disagreements'],1)

    def test_missing_rater_records_abstain(self):
        self.r2['annotations']=[]
        out=adjudicate(self.master,self.r1,self.r2)
        self.assertEqual(out['eligible_consensus_frames'],0)
        self.assertEqual(out['annotation_status'],'ABSTAIN_REFERENCE_UNRESOLVED')

    def test_duplicate_and_unknown_ids_rejected(self):
        self.r1['annotations'].append(self.r1['annotations'][0])
        self.assertRaises(ValueError,adjudicate,self.master,self.r1,self.r2)
        self.r1['annotations']=[row('invented')]
        self.assertRaises(ValueError,adjudicate,self.master,self.r1,self.r2)

    def test_nuisance_and_unknown_flags_abstain(self):
        self.r1['annotations'][0]=row(self.r1['annotations'][0]['view_id'],flags=['glare_brightness'])
        out=adjudicate(self.master,self.r1,self.r2)
        self.assertLess(out['eligible_consensus_frames'],len(self.sel['unique_frame_indices']))
        self.assertIsNone(aperture(row('x',flags=['secret_unknown_flag'])))


if __name__=='__main__':unittest.main()
