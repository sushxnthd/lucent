"""Independent E002-431 synthetic photometric alias and release-gate tests."""
import unittest
from e002_431_photometric_alias import (
    D,E,V,THETA,TARGET,G_BROAD,G_NARROW,
    conditional_lower,study_only_decision,hidden_aperture,gain_hidden,
    integrate_product_piecewise,stress,experiment,
)

class PhotometricAliasTests(unittest.TestCase):
    def test_frozen_hidden_closure_and_velocity(self):
        dt=D/10000
        a=[hidden_aperture(i*dt) for i in range(10001)]
        self.assertAlmostEqual(min(a),1.99,places=10)
        self.assertAlmostEqual(a[0],2.01,places=10)
        self.assertAlmostEqual(a[-1],2.01,places=10)
        self.assertLessEqual(max(abs(y-x)/dt for x,y in zip(a,a[1:])),V+1e-8)
        self.assertLess(min(a),THETA)
        self.assertGreater(TARGET,THETA)

    def test_continuous_and_shutter_observation_alias(self):
        # Independent 997-point midpoint quadrature across rates and exposures.
        for rate in (24,30,60,120,500):
            for exposure in (0.0005,0.002,0.004):
                for center in (0,1/rate,2/rate):
                    n=997
                    vals=[hidden_aperture(center+exposure*((k+.5)/n-.5))*gain_hidden(center+exposure*((k+.5)/n-.5)) for k in range(n)]
                    self.assertLess(abs(sum(vals)/n-TARGET),1e-11)
        self.assertGreater(gain_hidden(D/2),G_NARROW[1])
        self.assertLessEqual(gain_hidden(D/2),G_BROAD[1])
        self.assertGreaterEqual(gain_hidden(0),G_BROAD[0])

    def test_decisive_naive_failure_and_bounded_rescue(self):
        naive=conditional_lower(TARGET,TARGET,1,V,D)
        broad=conditional_lower(TARGET,TARGET,G_BROAD[1],V,D)
        narrow=conditional_lower(TARGET,TARGET,G_NARROW[1],V,D)
        self.assertAlmostEqual(naive,2.02)
        self.assertGreater(naive,THETA)
        self.assertLess(broad,THETA)
        self.assertGreater(narrow,THETA)
        self.assertGreater(gain_hidden(D/2),G_NARROW[1])
        for authenticated,nuisances in ((False,True),(True,False),(True,True)):
            result=study_only_decision(TARGET,TARGET,G_NARROW[1],V,D,authenticated,nuisances)
            self.assertFalse(result['physical_certificate_authorized'])
            self.assertEqual(result['product'],'ABSTAIN_UNCALIBRATED')
            self.assertEqual(result['study_only']=='CONDITIONAL_CANDIDATE',authenticated and nuisances)

    def test_independent_exact_integration_oracle(self):
        # a(t)=2+t and g(t)=3-2t => a*g=6-t-2t^2 on [0,1].
        val=integrate_product_piecewise([0,1],[2,3],[3,1],0,1)
        self.assertAlmostEqual(val,6-1/2-2/3,places=12)
        t=[0,.25,.5,.75,1]
        a=[2,2.1,2.15,2.12,2.05]
        g=[.97,1.01,1.03,.98,1.02]
        exact=integrate_product_piecewise(t,a,g,.1,.9)
        n=100000
        def interp(t0,vs):
            j=min(int(t0*4),3)
            x=(t0-t[j])/(t[j+1]-t[j])
            return vs[j]*(1-x)+vs[j+1]*x
        approx=sum(interp(.1+.8*(i+.5)/n,a)*interp(.1+.8*(i+.5)/n,g) for i in range(n))*.8/n
        self.assertAlmostEqual(exact,approx,delta=1e-9)

    def test_frozen_adversarial_stress(self):
        result=stress()
        self.assertEqual(result['n'],2000)
        self.assertEqual(result['seed'],431)
        self.assertEqual(result['false_certificates'],0)
        self.assertGreater(result['candidates'],100)
        self.assertGreater(result['witnessed_closures'],100)
        self.assertGreaterEqual(result['min_true_minus_bound_mm'],-1e-10)
        self.assertGreaterEqual(result['observed_gain_range'][0],G_BROAD[0])
        self.assertLessEqual(result['observed_gain_range'][1],G_BROAD[1])

    def test_reject_invalid_inputs_and_preserve_abstention(self):
        for args in [(-1,2,1,1,.01),(2,2,0,1,.01),(2,2,1,-1,.01),
                     (2,2,1,1,0),(2,2,1,1,float('nan')),
                     (2,2,float('inf'),1,.01),(2,2,1,1,.01,.02)]:
            with self.assertRaises(ValueError):conditional_lower(*args)
        with self.assertRaises(ValueError):study_only_decision(2,2,1,1,.01,'yes',True)
        with self.assertRaises(ValueError):stress(0)
        with self.assertRaises(ValueError):integrate_product_piecewise([0,1],[2],[3,1],0,1)
        e=experiment()
        self.assertFalse(e['physical_certificate_authorized'])
        self.assertEqual(e['product'],'ABSTAIN_UNCALIBRATED')
        self.assertAlmostEqual(e['hidden_velocity_peak_mm_s'],V)

if __name__=='__main__':
    unittest.main()
