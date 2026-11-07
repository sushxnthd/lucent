"""E002-428 independent binomial oracle and adversarial accounting."""
import importlib.util
import math
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('e002_428_velocity_tail',Path(__file__).with_name('e002_428_velocity_tail.py'))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def independent_cdf(k,n,p):
    # Separate combinatorial implementation, not calling the production CDF.
    return sum(math.comb(n,j)*p**j*(1-p)**(n-j) for j in range(k+1))


class VelocityTailTests(unittest.TestCase):
    def test_frozen_zero_violation_power(self):
        expected={8:0.312344,25:0.112928,100:0.029513,299:0.009969}
        for n,value in expected.items():
            self.assertAlmostEqual(m.upper_exact(n,0),value,delta=0.00001)
        self.assertGreater(m.upper_exact(298,0),0.01)
        self.assertLess(m.upper_exact(299,0),0.01)

    def test_independent_exact_oracle(self):
        for n in [3,8,10,25,100]:
            for k in [0,1,n//2,n-1]:
                bound=m.upper_exact(n,k)
                self.assertAlmostEqual(independent_cdf(k,n,bound),0.05,delta=1e-9)
        for n in [2,8,25]:
            self.assertEqual(m.upper_exact(n,n),1)

    def test_monotonicity(self):
        for n in [5,25,100]:
            bs=[m.upper_exact(n,k) for k in range(n+1)]
            self.assertTrue(all(a < b for a,b in zip(bs,bs[1:])))

    def test_missingness_and_no_hard_certificate(self):
        a=m.evaluate(25,0,5,400,'independent-archive:2026-10-25',iid_participant_assumption=True)
        self.assertLess(a['best_case_tail_upper'],a['worst_case_tail_upper'])
        self.assertFalse(a['physical_certificate_authorized'])
        self.assertFalse(a['hard_velocity_bound_authorized'])
        self.assertEqual(a['product'],'ABSTAIN_UNCALIBRATED')
        b=m.evaluate(25,0,25,400,'independent-archive:2026-10-25')
        self.assertEqual(b['worst_case_tail_upper'],1)
        self.assertFalse(b['population_tail_inference_eligible'])

    def test_frozen_provenance_and_bad_counts_rejected(self):
        base=(25,0,0,400,'independent-archive:2026-10-25')
        for params in [(0,0,0,400,base[4]),(25,-1,0,400,base[4]),
                       (25,0,26,400,base[4]),(25,1,25,400,base[4]),
                       (25,0,0,float('nan'),base[4]),(25,0,0,400,'not')]:
            with self.assertRaises(ValueError):m.evaluate(*params)
        with self.assertRaises(ValueError):m.upper_exact(25,0,0)
        with self.assertRaises(ValueError):m.upper_exact(25,0,1)
        with self.assertRaises(ValueError):m.evaluate(*base,iid_participant_assumption='yes')


if __name__=='__main__':unittest.main()
