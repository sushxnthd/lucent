import unittest
from e002_551_curvature_exclusion import exclude, parabola_min, simulation, REQUIRED_GATES

G = {k:True for k in REQUIRED_GATES}
class CurvatureExclusionTests(unittest.TestCase):
    def test_sharp_5ms_exclusion(self):
        r=exclude(.25,.25,.005,0,0,8000,instantaneous=True,gates=G)
        self.assertEqual(r.decision,'CONDITIONAL_EXCLUSION_ONLY')
        self.assertAlmostEqual(r.lower_bound,.225)
    def test_10ms_counterexample(self):
        r=exclude(.25,.25,.01,0,0,8000,instantaneous=True,gates=G)
        self.assertEqual(r.decision,'POSSIBLE_CLOSURE_OR_UNRESOLVED')
        self.assertAlmostEqual(r.lower_bound,.15)
        self.assertAlmostEqual(parabola_min(.25,.25,.01,8000),.15)
    def test_model_misspecification_kills(self):
        r=exclude(.25,.25,.01,0,0,1000,instantaneous=True,gates=G)
        self.assertEqual(r.decision,'CONDITIONAL_EXCLUSION_ONLY')
        self.assertLessEqual(parabola_min(.25,.25,.01,8000),.2)
    def test_more_clock_uncertainty_never_raises_lower(self):
        a=exclude(.3,.3,.01,0,0,1000,instantaneous=True,gates=G)
        b=exclude(.3,.3,.01,0,.0003,1000,instantaneous=True,gates=G)
        self.assertLessEqual(b.lower_bound,a.lower_bound)
    def test_more_localization_error_never_raises_lower(self):
        a=exclude(.3,.3,.01,0,0,1000,instantaneous=True,gates=G)
        b=exclude(.3,.3,.01,.03,0,1000,instantaneous=True,gates=G)
        self.assertLessEqual(b.lower_bound,a.lower_bound)
    def test_missing_acceleration_abstains(self):
        self.assertEqual(exclude(.3,.3,.01,0,0,None,instantaneous=True,gates=G).decision,'ABSTAIN')
    def test_clock_failure_abstains(self):
        self.assertEqual(exclude(.3,.3,.01,0,.005,1000,instantaneous=True,gates=G).decision,'ABSTAIN')
    def test_exposure_averaging_abstains(self):
        self.assertEqual(exclude(.3,.3,.01,0,0,1000,instantaneous=False,gates=G).decision,'ABSTAIN')
    def test_every_nuisance_gate_abstains(self):
        for k in REQUIRED_GATES:
            g=dict(G);g[k]=False
            with self.subTest(k=k):
                self.assertEqual(exclude(.3,.3,.01,0,0,1000,instantaneous=True,gates=g).decision,'ABSTAIN')
    def test_invalid_values_abstain(self):
        for v in [float('nan'),float('inf'),-1]:
            self.assertEqual(exclude(.3,.3,.01,0,0,v,instantaneous=True,gates=G).decision,'ABSTAIN')
    def test_linear_interpolation(self):
        r=exclude(.25,.4,.01,0,0,0,instantaneous=True,gates=G)
        self.assertAlmostEqual(r.lower_bound,.25)
    def test_10000_randomized_trials(self):
        s=simulation()
        self.assertGreater(s['accepted'],7000)
        self.assertEqual(s['false_exclusions'],0)
if __name__=='__main__':unittest.main()
