import tempfile
from pathlib import Path
import unittest
import zipfile
import e002_492_anatomical_review as m

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.man=m.build_manifest()
        self.a=m.template(self.man,'A')
        self.b=m.template(self.man,'B')
        self.clip=self.man['review_clips'][0]['clip']
    def fill(self, t, upper=50,lower=80,diameter=100,error=2,flags=None):
        t['clips'][self.clip][0].update(upper_y=upper,lower_y=lower,
             iris_diameter=diameter,uncertainty_px=error,flags=flags or [])
    def test_frozen_selection(self):
        centers=[c['center_native_frame'] for c in self.man['review_clips']]
        self.assertEqual(len(set(centers)),20)
        self.assertEqual(sum(c['candidate'] for c in self.man['review_clips']),1)
        self.assertTrue(all(abs(i-j)>=20 for k,i in enumerate(centers) for j in centers[k+1:]))
        self.assertTrue(all(6<=i<=11993 for i in centers))
    def test_unreviewed_fail_closed(self):
        r=m.adjudicate(self.man,self.a,self.b)
        self.assertEqual(r['unreviewed'],260)
        self.assertEqual(r['dual_measurable'],0)
        self.assertFalse(r['human_reference_validated'])
    def test_interval_agreement(self):
        self.fill(self.a);self.fill(self.b,lower=82)
        r=m.adjudicate(self.man,self.a,self.b)
        self.assertEqual(r['agreement_intervals'],1)
        self.assertEqual(r['interval_disagreement'],0)
        self.assertEqual(r['absolute_normalized_aperture_difference_median'],.02)
    def test_disagreement_is_not_averaged(self):
        self.fill(self.a,error=0);self.fill(self.b,lower=90,error=0)
        r=m.adjudicate(self.man,self.a,self.b)
        self.assertEqual(r['interval_disagreement'],1)
        self.assertTrue(r['falsification_disagreement_gt_20pct'])
    def test_nuisance_abstains(self):
        self.fill(self.a);self.fill(self.b,flags=['GAZE'])
        r=m.adjudicate(self.man,self.a,self.b)
        self.assertEqual(r['nuisance_abstention'],1)
        self.assertEqual(r['dual_measurable'],0)
    def test_invalid_geometry_abstains(self):
        self.fill(self.a);self.fill(self.b,upper=80,lower=50)
        r=m.adjudicate(self.man,self.a,self.b)
        self.assertEqual(r['geometry_abstention'],1)
    def test_nan_abstains(self):
        self.fill(self.a);self.fill(self.b,lower=float('nan'))
        self.assertEqual(m.adjudicate(self.man,self.a,self.b)['geometry_abstention'],1)
    def test_same_rater_rejected(self):
        self.b['rater']='A'
        with self.assertRaises(ValueError):m.adjudicate(self.man,self.a,self.b)
    def test_malformed_index_rejected(self):
        self.a['clips'][self.clip][0]['frame']=12
        with self.assertRaises(ValueError):m.adjudicate(self.man,self.a,self.b)
    def test_flags_rejected(self):
        self.a['clips'][self.clip][0]['flags']=['CLOSURE']
        with self.assertRaises(ValueError):m.adjudicate(self.man,self.a,self.b)
    def test_private_packet_templates(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'private';m.make_packet(p)
            self.assertTrue((p/'OWNER_ONLY_MAPPING.json').exists())
            self.assertTrue((p/'RATER_A_TEMPLATE.json').exists())
            self.assertFalse((p/'PRIVATE_FRAMES_DO_NOT_UPLOAD').exists())
            with self.assertRaises(ValueError):m.make_packet(p)
    def test_archive_member_safety(self):
        safe=zipfile.ZipInfo('S01/eye_phantom.avi')
        self.assertTrue(m.safe_member(safe))
        self.assertTrue(m.safe_member(zipfile.ZipInfo('S01/')))
        self.assertFalse(m.safe_member(zipfile.ZipInfo('../evil.avi')))
        self.assertFalse(m.safe_member(zipfile.ZipInfo('C:/evil.avi')))
        self.assertFalse(m.safe_member(zipfile.ZipInfo('a\\b.avi')))
    def test_interval_zero_floor(self):
        self.fill(self.a,upper=70,lower=70,error=2)
        self.fill(self.b,upper=70,lower=70,error=2)
        r=m.adjudicate(self.man,self.a,self.b)
        self.assertEqual(r['agreement_intervals'],1)
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')

if __name__=='__main__':unittest.main()
