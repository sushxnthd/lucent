import unittest
from e002_462_reference_aliasing import (C,O,THRESHOLD,exposure_mean,
                                          fixture,reference_observation,safe_reference,run)

class ReferenceAliasing(unittest.TestCase):
    def test_frozen_400fps_indistinguishable(self):
        p=safe_reference(fixture())
        self.assertTrue(p['indistinguishable_exact'])
        self.assertLess(p['max_deviation_mm'],1e-12)
        self.assertTrue(p['threshold_only_missed'])

    def test_frozen_1000fps_indistinguishable(self):
        p=safe_reference(fixture(1000,2.1,0.4))
        self.assertTrue(p['indistinguishable_exact'])

    def test_negative_constant_control(self):
        p=safe_reference(fixture())
        self.assertTrue(all(abs(x-2.3)<1e-12 for x in p['means_mm']))

    def test_analytic_critical_gaps(self):
        self.assertAlmostEqual(.3*(1/C+1/O),1.621,places=2)
        self.assertAlmostEqual(.1*(1/C+1/O),.540,places=2)

    def test_exposure_overlap_abstains(self):
        p=safe_reference(fixture(2000,2.1,.4,.8))
        self.assertEqual(p['decision'],'ABSTAIN_UNCALIBRATED')

    def test_shutter_integral_monotonicity(self):
        for t in (-2,0,.3,1,1.7,2.3,4):
            m=exposure_mean(2.3,1.0,t,.3)
            self.assertTrue(2.0<=m<=2.3+1e-12)

    def test_missing_nuisance_abstains(self):
        for key in fixture()['nuisance']:
            r=fixture();del r['nuisance'][key]
            self.assertEqual(safe_reference(r)['decision'],'ABSTAIN_UNCALIBRATED')

    def test_unauthenticated_physical_abstains(self):
        r=fixture();r['synthetic_instrument_only']=False
        self.assertEqual(safe_reference(r)['decision'],'ABSTAIN_UNCALIBRATED')

    def test_invalid_inputs_abstain(self):
        for change in ({'fps':0},{'fps':240.5},{'width_ms':0},
                       {'tau_ms':float('nan')},{'baseline_mm':2.0}):
            r=fixture();r.update(change)
            self.assertEqual(safe_reference(r)['decision'],'ABSTAIN_UNCALIBRATED')

    def test_seeded_sweep_nontrivial(self):
        out=run()
        cells={(c['fps'],c['baseline_mm'],c['width_ms']):c for c in out['cells']}
        self.assertGreater(cells[(400,2.3,.3)]['indistinguishable'],0)
        self.assertEqual(cells[(2000,2.1,.3)]['indistinguishable'],0)
        self.assertEqual(cells[(2000,2.1,.8)]['decision'],'ABSTAIN_UNCALIBRATED')
        self.assertEqual(out['product'],'ABSTAIN_UNCALIBRATED')

if __name__=='__main__':unittest.main()
