import csv
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('e002_427', HERE/'e002_427_human_kinematics.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def cfg(**kw):
    base = dict(training_participants=['TRAIN'], holdout_participants=['HOLD'], period_s=1/30,
                exposure_s=1/120, threshold_mm=1, velocity_hypothesis_mm_s=80,
                reference_speed_hypothesis_mm_s=500, aperture_error_mm=0.02,
                clock_error_s=0.0001, max_reference_step_s=0.00251,
                physical_aperture_registration_ref='independent_geometry_protocol',
                source_access_ref='synthetic_test_fixture')
    base.update(kw)
    return base


def trace(func=lambda t: 8):
    blank = {n:False for n in m.NUISANCES}
    rows = [(i/400, func(i/400), dict(blank)) for i in range(201)]
    return {'TRAIN':[(t,a,dict(n)) for t,a,n in rows],
            'HOLD':[(t,a,dict(n)) for t,a,n in rows]}


class TestHumanAdapter(unittest.TestCase):
    def test_no_certificates_with_no_margin(self):
        result = m.analyze(trace(lambda t: 1.1), cfg())
        self.assertEqual(result['pooled']['conditional'], 0)
        self.assertIsNone(result['pooled']['finite_set_false_fraction_interval'])
        self.assertFalse(result['physical_certificate_authorized'])

    def test_wide_open_eligible_conditional_but_not_physical(self):
        result = m.analyze(trace(), cfg())
        self.assertGreater(result['pooled']['conditional'], 0)
        self.assertEqual(result['pooled']['witnessed_failures'], 0)
        self.assertEqual(result['product'], 'ABSTAIN_UNCALIBRATED')

    def test_false_certificate_when_velocity_hypothesis_wrong(self):
        # Actual 400 mm/s closure can hide between 30-Hz virtual exposures.
        def gap(t):
            return min(8.0, 400*abs(t - 1/60))
        out = m.analyze(trace(gap), cfg(velocity_hypothesis_mm_s=180,
                                      reference_speed_hypothesis_mm_s=500))
        self.assertGreater(out['pooled']['witnessed_failures'], 0)
        self.assertTrue(out['participants']['HOLD']['secant_exceeds_hypothesis'])
        self.assertFalse(out['physical_certificate_authorized'])

    def test_missing_and_nuisance_never_interpolated(self):
        tr = trace()
        t,a,n = tr['HOLD'][4]
        tr['HOLD'][4] = (t, None, n)
        t,a,n = tr['HOLD'][30]
        n['glasses'] = True
        tr['HOLD'][30] = (t,a,n)
        out = m.analyze(tr, cfg())
        self.assertGreater(out['participants']['HOLD']['abstain'], 0)

    def test_reject_leaky_split_and_invalid_bounds(self):
        with self.assertRaises(ValueError):
            m.analyze(trace(), cfg(holdout_participants=['TRAIN']))
        with self.assertRaises(ValueError):
            m.analyze(trace(), cfg(velocity_hypothesis_mm_s=float('nan')))
        with self.assertRaises(ValueError):
            m.analyze(trace(), cfg(exposure_s=1/10))

    def test_definite_crossing_survives_other_missing_samples(self):
        tr = trace(lambda t: min(8, 400*abs(t-1/60)))
        rows = tr['HOLD']
        t,a,n = rows[2]
        rows[2] = (t,None,n)
        self.assertEqual(m._reference_label(rows,0,1/30+1/120,cfg()), 'WITNESSED_CROSSING')

    def test_reference_endpoint_coverage_is_conservative(self):
        rows = trace(lambda t: 1.3)['HOLD']
        self.assertEqual(m._reference_label(rows,0.0,0.051,cfg(reference_speed_hypothesis_mm_s=500)), 'UNRESOLVED')

    def test_csv_schema_and_nonfinite_rejection(self):
        headers = ['participant_id','time_s','aperture_mm','valid'] + ['nuisance_'+n for n in m.NUISANCES]
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td,'input.csv')
            with open(path,'w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=headers);w.writeheader()
                for i in range(3):
                    w.writerow(dict(participant_id='P',time_s=i/400,aperture_mm=8,valid=1,
                                    **{'nuisance_'+n:'0' for n in m.NUISANCES}))
            self.assertEqual(len(m.load_trace(path)['P']),3)
            with open(path,'a') as f:
                f.write('P,nan,8,1,'+','.join(['0']*len(m.NUISANCES))+'\n')
            with self.assertRaises(ValueError):
                m.load_trace(path)

    def test_reference_400hz_cannot_exclude_subframe_closure_without_cap(self):
        rows = trace(lambda t: 1.25)['HOLD'][:20]
        start, end = 0, 0.0475
        self.assertEqual(m._reference_label(rows,start,end,cfg(reference_speed_hypothesis_mm_s=500)), 'UNRESOLVED')
        self.assertGreater(500*(1/400)/2, 0.25)


if __name__=='__main__':
    unittest.main()
