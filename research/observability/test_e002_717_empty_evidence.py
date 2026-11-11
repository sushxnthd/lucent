"""E002-717: adversarial negative-control regression for the E002-716 replay summary.

Run from repository root: python -m unittest research.observability.test_e002_717_empty_evidence
This is deliberately a failing regression until the replay gate refuses evidence-free success.
"""
import unittest
from research.observability.e002_716_blinded_replay import evaluate

FLAGS = ('geometry_valid','photometry_valid','clock_valid','exposure_valid','missingness_valid','blur_valid','gaze_valid','glasses_valid','velocity_independent')
def row(tid, split='heldout', reference_valid='0', velocity='1', delta='1'):
    r = {k:'1' for k in FLAGS}
    r.update(trial_id=tid,participant_id='person-'+tid,split=split,
             reference_closure='0',reference_valid=reference_valid,
             aperture0_lower='1',aperture1_lower='1',
             velocity_upper=velocity,delta_upper=delta)
    return r

class EvidenceFreeReplayMustAbstain(unittest.TestCase):
    def test_zero_heldout_cannot_pass(self):
        result=evaluate([row('cal','calibration')])
        self.assertNotEqual(result['status'],'NO_OBSERVED_FALSIFICATION',
                            'zero held-out cases must not look like evidence')
    def test_all_reference_indeterminate_cannot_pass(self):
        result=evaluate([row('unknown')])
        self.assertNotEqual(result['status'],'NO_OBSERVED_FALSIFICATION',
                            'zero scored reference labels must not look like evidence')
    def test_all_uncertified_cannot_pass(self):
        result=evaluate([row('uncertified',reference_valid='1',velocity='2',delta='2')])
        self.assertNotEqual(result['status'],'NO_OBSERVED_FALSIFICATION',
                            'zero issued exclusions must not look like evidence')

if __name__=='__main__':
    unittest.main()
