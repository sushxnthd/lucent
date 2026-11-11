import unittest
from fractions import Fraction as F
from e002_612_velocity_envelope import (
    interval_bound, scenario_rows, certify_observed_span, ATTESTATIONS, NUISANCES)

def fixture():
    return {'experiment':'E002-612',
            'observations':[{'z_mm':'4','error_mm':'0.1','point_observation':True,'missing':False},
                            {'z_mm':'4','error_mm':'0.1','point_observation':True,'missing':False}],
            'intervals':[{'dt_lower_s':'1/120','dt_upper_s':'1/120'}],
            'acceleration_upper_mm_s2':'5000',
            'attestations':{k:True for k in ATTESTATIONS},
            'nuisances':{k:False for k in NUISANCES}}

class EnvelopeTests(unittest.TestCase):
    def test_frozen_four(self):
        expect={30:F(268,3),120:F(269,6),240:F(701,12),1000:F(405,2)}
        for f,v in expect.items():
            self.assertEqual(interval_bound(0,0,'0.1','0.1',F(1,f),F(1,f),5000),v)
    def test_grid(self):
        self.assertEqual(len(list(scenario_rows())),12)
    def test_noise_monotone(self):
        self.assertLess(interval_bound(0,0,'0.05','0.05','0.01','0.01',5000),interval_bound(0,0,'0.1','0.1','0.01','0.01',5000))
    def test_accel_monotone(self):
        self.assertLess(interval_bound(0,0,0,0,'0.01','0.01',4000),interval_bound(0,0,0,0,'0.01','0.01',5000))
    def test_time_uncertainty(self):
        self.assertLess(interval_bound(0,0,'0.1','0.1','0.01','0.01',5000),interval_bound(0,0,'0.1','0.1','0.009','0.011',5000))
    def test_sharpness(self):
        dt=F(1,120); m=F(5000); eps=F('0.1'); y0=F(4)-eps; y1=F(4)+eps
        secant=(y1-y0)/dt
        terminal=secant+m*dt/2
        self.assertEqual(terminal,interval_bound(4,4,eps,eps,dt,dt,m))
        self.assertEqual(y0+secant*dt+m*dt*(dt-dt)/2,y1)
    def test_zero_and_negative_time_rejected(self):
        for lo in ('0','-0.01'):
            with self.assertRaises(ValueError): interval_bound(0,0,0,0,lo,'0.01',5000)
    def test_invalid_acceleration_rejected(self):
        with self.assertRaises(ValueError): interval_bound(0,0,0,0,'0.01','0.01',-1)
    def test_nonfinite_rejected(self):
        for v in ('nan','inf',float('inf')):
            with self.assertRaises(ValueError): interval_bound(0,0,v,0,'0.01','0.01',5000)
    def test_valid_is_conditional(self):
        r=certify_observed_span(fixture())
        self.assertEqual(r['status'],'CONDITIONAL_OBSERVED_SPAN_VELOCITY_BOUND')
        self.assertFalse(r['human_speed_certified'])
        self.assertEqual(r['release'],'BLOCKED')
    def test_no_independent_acceleration(self):
        d=fixture(); d['attestations']['independent_acceleration_bound']=False
        self.assertEqual(certify_observed_span(d)['status'],'ABSTAIN_UNCALIBRATED')
    def test_exposure_averages_abstain(self):
        d=fixture(); d['observations'][0]['point_observation']=False
        self.assertEqual(certify_observed_span(d)['status'],'ABSTAIN_UNCALIBRATED')
    def test_missing_abstains(self):
        d=fixture(); d['observations'][0]['missing']=True
        self.assertEqual(certify_observed_span(d)['status'],'ABSTAIN_UNCALIBRATED')
    def test_nuisances_abstain(self):
        for k in NUISANCES:
            d=fixture(); d['nuisances'][k]=True
            self.assertEqual(certify_observed_span(d)['status'],'ABSTAIN_UNCALIBRATED')
    def test_missing_interval_rejected(self):
        d=fixture(); d['intervals']=[]
        with self.assertRaises(ValueError): certify_observed_span(d)
    def test_not_a_universal_bound(self):
        d=fixture(); d['observations'].append({'z_mm':'4','error_mm':'0.1','point_observation':True,'missing':False})
        d['intervals'].append({'dt_lower_s':'1/120','dt_upper_s':'1/120'})
        self.assertEqual(certify_observed_span(d)['scope'],'ONLY_CONTIGUOUS_OBSERVED_SPAN_AND_STIPULATED_PREMISES')
    def test_boolean_numeric_rejected(self):
        with self.assertRaises(ValueError): interval_bound(True,0,0,0,'0.01','0.01',5000)

if __name__ == '__main__': unittest.main()
