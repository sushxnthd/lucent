"""E002-450 frozen adversarial synthetic fixtures; no human evidence."""
import copy
import json
import unittest
from e002_448_blind_annotation import adjudicate
from e002_450_reference_gate import assess


def row(vid, ap=.10, flags=None):
    return {'view_id':vid, 'status':'abstain' if flags else 'valid', 'flags':flags or [],
            'points': {'L':[50,120], 'R':[250,120], 'U':[160,110], 'D':[160,110+200*ap]}}


def fixture():
    views = [{'view_id':f'v{i}', 'frame_index':i, 'repeat':False} for i in range(6)]
    views += [{'view_id':'v1r', 'frame_index':1, 'repeat':True}]
    master = {'experiment':'E002-448', 'pilot':'S19', 'views':views,
              'medium_intervals':[1,3], 'control_intervals':[2,5], 'private_blind_key':'DO_NOT_EXPORT'}
    r1 = {'rater_id':'A', 'annotations':[row(v['view_id']) for v in views]}
    r2 = {'rater_id':'B', 'annotations':[row(v['view_id']) for v in views]}
    return master,r1,r2


def replace(doc,vid,ap=None,flags=None):
    for i,r in enumerate(doc['annotations']):
        if r['view_id']==vid:
            doc['annotations'][i]=row(vid,ap=ap if ap is not None else .1,flags=flags)
            return
    raise ValueError(vid)


class TestReferenceGate(unittest.TestCase):
    def setUp(self):self.master,self.a,self.b=fixture()

    def test_original_cross_rater_mean_masks_repeat_failure(self):
        replace(self.a,'v1',.10);replace(self.a,'v1r',.14)
        replace(self.b,'v1',.12);replace(self.b,'v1r',.12)
        old=adjudicate(self.master,self.a,self.b)
        new=assess(self.master,self.a,self.b)
        self.assertEqual(old['eligible_consensus_frames'],6)
        self.assertEqual(new['eligible_consensus_frames'],5)
        self.assertEqual(new['rater_repeat_failure_frames'],1)
        self.assertEqual(new['eligible_medium_pairs'],1)
        self.assertFalse(new['physical_release_authorized'])

    def test_original_partial_annotations_false_readiness(self):
        self.a['annotations']=[row('v0')]
        self.b['annotations']=[row('v0')]
        self.assertEqual(adjudicate(self.master,self.a,self.b)['annotation_status'],'PILOT_2D_CONSENSUS_ONLY')
        result=assess(self.master,self.a,self.b)
        self.assertEqual(result['annotation_status'],'NOT_EVALUABLE_INCOMPLETE')
        self.assertEqual(result['eligible_consensus_frames'],0)

    def test_full_fixture_image_space_only(self):
        out=assess(self.master,self.a,self.b)
        self.assertEqual(out['eligible_consensus_frames'],6)
        self.assertEqual(out['eligible_medium_pairs'],2)
        self.assertEqual(out['eligible_short_pairs'],2)
        self.assertEqual(out['annotation_status'],'PILOT_IMAGE_SPACE_REFERENCE_ONLY')
        self.assertEqual(out['product_claim'],'ABSTAIN_UNCALIBRATED')
        self.assertFalse(out['physical_timing_authenticated'])
        self.assertNotIn('v1',json.dumps(out))
        self.assertNotIn('DO_NOT_EXPORT',json.dumps(out))

    def test_one_rater_repeat_fail(self):
        replace(self.a,'v1r',.15)
        out=assess(self.master,self.a,self.b)
        self.assertEqual(out['rater_repeat_failure_frames'],1)
        self.assertEqual(out['eligible_consensus_frames'],5)

    def test_both_raters_repeat_fail(self):
        replace(self.a,'v1r',.14);replace(self.b,'v1r',.14)
        self.assertEqual(assess(self.master,self.a,self.b)['rater_repeat_failure_frames'],1)

    def test_between_rater_disagreement(self):
        replace(self.b,'v4',.20)
        self.assertEqual(assess(self.master,self.a,self.b)['between_rater_failure_frames'],1)

    def test_nuisance_abstain(self):
        replace(self.a,'v0',flags=['motion_blur'])
        out=assess(self.master,self.a,self.b)
        self.assertEqual(out['rater1_explicit_abstentions'],1)
        self.assertEqual(out['eligible_consensus_frames'],5)

    def test_invalid_geometry_abstains(self):
        self.a['annotations'][0]['points']['L']=[150,120]
        self.a['annotations'][0]['points']['R']=[160,120]
        self.assertEqual(assess(self.master,self.a,self.b)['rater1_invalid_geometry'],1)

    def test_missing_independent_rater(self):
        out=assess(self.master,None,None)
        self.assertEqual(out['annotation_status'],'NOT_EVALUABLE_NO_INDEPENDENT_RATERS')
        self.assertRaises(ValueError,assess,self.master,self.a,{'rater_id':'A','annotations':self.b['annotations']})

    def test_duplicate_and_unknown_ids(self):
        self.a['annotations'].append(copy.deepcopy(self.a['annotations'][0]))
        self.assertRaises(ValueError,assess,self.master,self.a,self.b)
        self.a['annotations'][-1]['view_id']='not-a-view'
        self.assertRaises(ValueError,assess,self.master,self.a,self.b)

    def test_bad_status_and_abstain_reason(self):
        self.a['annotations'][0]['status']='abstain'
        self.assertRaises(ValueError,assess,self.master,self.a,self.b)
        self.a['annotations'][0]['flags']=['not_anatomical']
        self.assertEqual(assess(self.master,self.a,self.b)['rater1_explicit_abstentions'],1)

    def test_invalid_master_intervals(self):
        self.master['medium_intervals']=[100]
        self.assertRaises(ValueError,assess,self.master,self.a,self.b)

    def test_output_aggregates_only(self):
        result=assess(self.master,self.a,self.b)
        serialized=json.dumps(result)
        for secret in ('frame_index','view_id','private_blind_key','rater_id','DO_NOT_EXPORT','v1r','points'):
            self.assertNotIn(secret,serialized)

    def test_missing_one_view_is_not_success(self):
        self.b['annotations'].pop()
        self.assertEqual(assess(self.master,self.a,self.b)['eligible_medium_pairs'],0)

    def test_bad_flag_and_nonfinite(self):
        self.a['annotations'][0]['flags']=['unknown']
        self.assertRaises(ValueError,assess,self.master,self.a,self.b)
        self.a['annotations'][0]['flags']=[]
        self.a['annotations'][0]['points']['D'][1]=float('nan')
        self.assertEqual(assess(self.master,self.a,self.b)['rater1_invalid_geometry'],1)


if __name__=='__main__':unittest.main()
