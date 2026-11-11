"""Adversarial, independent checks for the E002-436 reference instrument."""
import copy
import importlib.util
import math
import random
import unittest
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location('m', Path(__file__).with_name('e002_436_dual_rater.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def case(apertures=(3.0,3.0,3.0), velocity=50., delta=0.0001):
    frames = [dict(frame_id=i, time_s=i*.01, nuisance_ok=True,
                   rater_a=[ap-.01,ap+.01], rater_b=[ap-.02,ap+.02])
              for i,ap in enumerate(apertures)]
    return dict(trial_id='synthetic_1', interval_start_s=0., interval_end_s=.02,
                threshold_mm=2., clock_error_s=delta,
                max_reference_step_s=.01001, velocity_upper_mm_s=velocity,
                velocity_bound_attested=True, sensor_timing_attested=True,
                physical_scale_attested=True, rater_blinding_attested=True,
                frames=frames)


class TestReferenceInstrument(unittest.TestCase):
    def test_wide_open_negative_and_no_product_claim(self):
        r=m.adjudicate(case())
        self.assertEqual(r['reference_label'], 'NEGATIVE_CONDITIONAL')
        self.assertFalse(r['product_claim_authorized'])
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertAlmostEqual(r['lower_envelope_mm'], 2.735, places=8)

    def test_between_sample_lipschitz_valley_is_unresolved(self):
        # At t=5ms, x=1.85mm is compatible with x(0)=x(10ms)=2.10mm
        # under V=50mm/s; all three observed frames remain >2mm.
        c=case((2.1,2.1,2.1))
        r=m.adjudicate(c)
        self.assertEqual(r['reference_label'],'UNRESOLVED')
        self.assertLess(r['lower_envelope_mm'],2.)
        self.assertGreater(min(f['rater_a'][0] for f in c['frames']),2.)

    def test_dual_rater_witness_and_conflict(self):
        c=case()
        c['frames'][1]['rater_a']=[1.85,1.95]
        c['frames'][1]['rater_b']=[1.90,1.98]
        r=m.adjudicate(c)
        self.assertEqual(r['reference_label'],'WITNESSED_CROSSING')
        self.assertEqual(r['witnessed_frame_ids'],[1])
        c['frames'][1]['rater_b']=[2.2,2.3]
        r=m.adjudicate(c)
        self.assertEqual(r['reference_label'],'UNRESOLVED')
        self.assertEqual(r['reason'],'missing_nuisance_or_rater_disagreement')

    def test_single_rater_witness_is_not_sufficient(self):
        c=case()
        c['frames'][1]['rater_a']=[1.85,1.95]
        c['frames'][1]['rater_b']=None
        self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')

    def test_partial_witness_with_overlapping_intervals_is_unresolved(self):
        c=case()
        c['frames'][1]['rater_a']=[1.85,1.95]
        c['frames'][1]['rater_b']=[1.90,2.05]
        r=m.adjudicate(c)
        self.assertEqual(r['reference_label'],'UNRESOLVED')
        self.assertEqual(r['reason'],'single_rater_crossing_not_corroborated')

    def test_missingness_and_nuisance_cannot_improve_negative(self):
        c=case()
        self.assertEqual(m.adjudicate(c)['reference_label'],'NEGATIVE_CONDITIONAL')
        c['frames'][1]['nuisance_ok']=False
        self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')
        c=case()
        c['frames'].pop(1)
        self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')
        self.assertEqual(m.adjudicate(c)['reason'],'reference_gap_exceeds_protocol')

    def test_provenance_and_velocity_gate(self):
        for key in ('sensor_timing_attested','physical_scale_attested','rater_blinding_attested'):
            c=case(); c[key]=False
            self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')
        c=case(); c['velocity_bound_attested']=False
        self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')
        c=case(); c['velocity_upper_mm_s']=None
        self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')

    def test_clock_uncertainty_monotone_and_endpoint_positive(self):
        small=m.adjudicate(case(delta=0))['lower_envelope_mm']
        large=m.adjudicate(case(delta=.002))['lower_envelope_mm']
        self.assertLessEqual(large,small)
        c=case(); c['frames'][0]['rater_a']=[1.8,1.9];c['frames'][0]['rater_b']=[1.8,1.9]
        self.assertEqual(m.adjudicate(c)['reference_label'],'UNRESOLVED')
        c['clock_error_s']=0
        self.assertEqual(m.adjudicate(c)['reference_label'],'WITNESSED_CROSSING')

    def test_exact_envelope_matches_independent_dense_time_oracle(self):
        rng=random.Random(436)
        for _ in range(80):
            n=rng.randint(2,8)
            ts=[i*.006 for i in range(n)]
            lows=[rng.uniform(1.5,5) for _ in ts]
            v=rng.uniform(1,100)
            delta=rng.uniform(0,.0003)
            a=ts[0];b=ts[-1]
            exact=m.exact_lipschitz_lower(ts,lows,v,a,b,delta)['lower_envelope_mm']
            dense=min(max(0.,max(l-v*(abs(t-ti)+delta) for ti,l in zip(ts,lows)))
                      for t in (a+(b-a)*k/20000 for k in range(20001)))
            self.assertLessEqual(exact,dense+1e-10)
            self.assertLess(dense-exact,0.0006)

    def test_seeded_benchmark_has_no_synthetic_false_certificates(self):
        sys.path.insert(0,str(Path(__file__).parent))
        import e002_436_benchmark as bench
        a=bench.run(n=120,seed=436)
        b=bench.run(n=120,seed=436)
        self.assertEqual(a,b)
        self.assertEqual(a['false_conditional_negative_against_synthetic_truth'],0)
        self.assertEqual(a['counts']['NEGATIVE_CONDITIONAL']+a['counts']['UNRESOLVED']+a['counts']['WITNESSED_CROSSING'],120)

    def test_inconsistent_physical_speed_and_clock_overlap_abstain(self):
        c=case(velocity=1.)
        c['frames'][1]['rater_a']=[2.5,2.5]
        c['frames'][1]['rater_b']=[2.5,2.5]
        self.assertEqual(m.adjudicate(c)['reason'],'reference_intervals_incompatible_with_velocity')
        c=case(delta=.005)
        self.assertEqual(m.adjudicate(c)['reason'],'reference_clock_order_unresolved')

    def test_invalid_and_malformed_rejected(self):
        for bad in (float('nan'),float('inf'),-1):
            c=case();c['clock_error_s']=bad
            with self.assertRaises(m.ReferenceError):m.adjudicate(c)
        c=case();c['frames'][1]['frame_id']=0
        with self.assertRaises(m.ReferenceError):m.adjudicate(c)
        c=case();c['frames'][1]['time_s']=0
        with self.assertRaises(m.ReferenceError):m.adjudicate(c)
        c=case();c['frames'][1]['rater_a']=[4,3]
        with self.assertRaises(m.ReferenceError):m.adjudicate(c)
        c=case();c['sensor_timing_attested']='yes'
        with self.assertRaises(m.ReferenceError):m.adjudicate(c)
        c=case();c['frames'][1]['rater_a']=[float('nan'),4]
        with self.assertRaises(m.ReferenceError):m.adjudicate(c)


if __name__=='__main__':unittest.main()
