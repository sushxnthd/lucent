import unittest
from fractions import Fraction
from e002_610_photometric_bound import evaluate,fixture,synthetic_sweep

class TestE610(unittest.TestCase):
    def test_tight(self):
        r=evaluate(fixture())
        self.assertEqual(r['status'],'MEAN_WITNESS_CONDITIONAL')
        self.assertEqual(Fraction(r['aperture_mean_upper']),Fraction(25,147))
        self.assertEqual(r['release'],'BLOCKED')
    def test_wide_flux(self):
        d=fixture();d['flux_lower']='0.5'
        r=evaluate(d)
        self.assertEqual(r['status'],'NO_MEAN_WITNESS')
        self.assertEqual(Fraction(r['aperture_mean_upper']),Fraction(15,49))
    def test_zero_flux(self):
        d=fixture();d['flux_lower']='0'
        self.assertTrue(evaluate(d)['status'].startswith('ABSTAIN'))
    def test_missing_attestation(self):
        d=fixture();d['attestations']['raw_linear_light']=False
        self.assertEqual(evaluate(d)['status'],'ABSTAIN_ATTESTATION')
    def test_missing_digest(self):
        d=fixture();d['evidence_sha256']['sensor_transfer']='fake'
        self.assertEqual(evaluate(d)['status'],'ABSTAIN_DIGEST')
    def test_all_nuisances(self):
        for k in fixture()['nuisances']:
            d=fixture();d['nuisances'][k]=True
            self.assertEqual(evaluate(d)['status'],'ABSTAIN_NUISANCE',k)
    def test_monotonic(self):
        d=fixture();d['signal_upper']='0.25'
        self.assertGreaterEqual(Fraction(evaluate(d)['aperture_mean_upper']),Fraction(25,147))
        d=fixture();d['gain_lower']='0.5'
        self.assertGreaterEqual(Fraction(evaluate(d)['aperture_mean_upper']),Fraction(25,147))
    def test_infeasible(self):
        d=fixture();d['signal_lower']='2';d['signal_upper']='2'
        self.assertEqual(evaluate(d)['status'],'ABSTAIN_INFEASIBLE_MEASUREMENT')
    def test_gamma_unknown(self):
        d=fixture();d['attestations']['raw_linear_light']=False
        self.assertEqual(evaluate(d)['status'],'ABSTAIN_ATTESTATION')
    def test_two_worlds(self):
        self.assertEqual(Fraction('0.2')*Fraction('1'),Fraction('0.5')*Fraction('0.4'))
        d=fixture();d.update(signal_lower='0.2',signal_upper='0.2',background_lower='0',background_upper='0',gain_lower='1',gain_upper='1',flux_lower='0.4',flux_upper='1')
        self.assertEqual(evaluate(d)['status'],'NO_MEAN_WITNESS')
        self.assertEqual(Fraction(evaluate(d)['aperture_mean_upper']),Fraction('0.5'))
    def test_seeded_sweep(self):
        r=synthetic_sweep()
        self.assertEqual(r['bound_violations'],0)
        self.assertEqual(r['tight_false_witness'],0)
        self.assertEqual(r['loose_false_witness'],0)
        self.assertGreater(r['tight_witness'],r['loose_witness'])

if __name__=='__main__':unittest.main()
