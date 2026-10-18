#!/usr/bin/env python3
"""E002-275: event-lag identifiability and EVE camera eligibility, no human data.

The conditional interval applies to a lag estimator with a *separately justified*
absolute estimator error bound and a verified exposure/reference clock error bound.
It is not a bound for arbitrary cross-correlation peak estimators.
"""
import argparse, hashlib, json, math, random
from pathlib import Path

LAG_GATE_S = .067
CAMERAS = {
    'basler': {'fps': 60, 'device_model': 'Basler acA1920-150uc', 'consumer_webcam': False,
               'author_sync': 'reliable_to_eye_tracker', 'clock_error_bound_s': None},
    'webcam_l': {'fps': 30, 'device_model': 'Logitech C922', 'consumer_webcam': True,
                 'author_sync': 'best_effort_imprecise', 'clock_error_bound_s': None},
    'webcam_c': {'fps': 30, 'device_model': 'Logitech C922', 'consumer_webcam': True,
                 'author_sync': 'best_effort_imprecise', 'clock_error_bound_s': None},
    'webcam_r': {'fps': 30, 'device_model': 'Logitech C922', 'consumer_webcam': True,
                 'author_sync': 'best_effort_imprecise', 'clock_error_bound_s': None},
}

def certificate(observed_lag_s, clock_error_bound_s, estimator_error_bound_s, limit_s=LAG_GATE_S):
    if not math.isfinite(observed_lag_s):
        raise ValueError('NONFINITE_OBSERVED_LAG')
    if not math.isfinite(limit_s) or limit_s < 0:
        raise ValueError('INVALID_GATE')
    if clock_error_bound_s is None or estimator_error_bound_s is None:
        return {'decision': 'UNCERTIFIED', 'true_lag_interval_s': None,
                'min_abs_lag_s': 0.0, 'max_abs_lag_s': None,
                'reason': 'MISSING_INDEPENDENT_CLOCK_OR_ESTIMATOR_ERROR_BOUND'}
    if any(not math.isfinite(x) or x < 0 for x in (clock_error_bound_s, estimator_error_bound_s)):
        raise ValueError('INVALID_ERROR_BOUND')
    radius = clock_error_bound_s + estimator_error_bound_s
    lo, hi = observed_lag_s - radius, observed_lag_s + radius
    min_abs = max(0.0, abs(observed_lag_s) - radius)
    max_abs = abs(observed_lag_s) + radius
    decision = ('CERTIFIED_PASS' if max_abs <= limit_s + 1e-12 else
                'CERTIFIED_FAIL' if min_abs > limit_s + 1e-12 else 'INDETERMINATE')
    return {'decision': decision, 'true_lag_interval_s': [lo, hi],
            'min_abs_lag_s': min_abs, 'max_abs_lag_s': max_abs,
            'reason': 'CONDITIONAL_SHARP_ADDITIVE_INTERVAL'}

def eligibility(cameras=CAMERAS):
    # Documented 'reliable' is not a measured numeric error budget.
    return {
        'basler_positive_control_candidate': cameras['basler']['author_sync']=='reliable_to_eye_tracker',
        'quantitative_lag_certified_from_documentation': any(
            v['clock_error_bound_s'] is not None for v in cameras.values()),
        'consumer_device_holdout_certified': len({v['device_model'] for v in cameras.values()
            if v['consumer_webcam'] and v['clock_error_bound_s'] is not None}) >= 2,
        'same_participant_four_views_not_independent_device_models': True,
        'required_next_evidence': 'Independent exposure-to-reference clock bounds plus distinct consumer device model holdout',
    }

def run():
    # Deterministic exact endpoint constructions, not a physiological simulation.
    cases = [
        ('unbounded_webcam', .020, None, .005),
        ('tight_calibrated_pass', .020, .010, .005),
        ('boundary_ambiguous', .060, .010, .005),
        ('far_lag_fail', .100, .010, .005),
        ('zero_observed_no_clock', 0.0, None, 0.0),
    ]
    results = {name: certificate(lag, j, e) for name,lag,j,e in cases}
    rng = random.Random(275)
    covered = 0
    sharp_endpoints = 0
    for _ in range(2400):
        true_lag = rng.uniform(-.25,.25)
        clock_error_bound = rng.uniform(0,.05)
        estimator_error_bound = rng.uniform(0,.02)
        clock_error = rng.uniform(-clock_error_bound,clock_error_bound)
        estimator_error = rng.uniform(-estimator_error_bound,estimator_error_bound)
        observed = true_lag + clock_error + estimator_error
        c = certificate(observed,clock_error_bound,estimator_error_bound)
        lo,hi = c['true_lag_interval_s']
        if lo-1e-12 <= true_lag <= hi+1e-12:
            covered += 1
        else:
            raise AssertionError('INTERVAL_VIOLATION')
        # Independent endpoint construction: choose both errors at their extrema.
        if abs((observed-(clock_error_bound+estimator_error_bound))-lo)<1e-12 and abs((observed+(clock_error_bound+estimator_error_bound))-hi)<1e-12:
            sharp_endpoints += 1
    return {
        'run':'E002-275', 'kind':'conditional_clock_bound_and_dataset_eligibility',
        'source_dataset':'EVE ECCV 2020', 'raw_human_data_loaded':False,
        'human_waveform_measured':False,
        'frozen_lag_gate_s':LAG_GATE_S, 'camera_sources':CAMERAS,
        'eligibility':eligibility(), 'cases':results,
        'deterministic_trials':2400, 'interval_covered':covered,
        'algebraic_endpoint_checks':sharp_endpoints,
        'independent_numeric_clock_bound_in_EVE_documentation':False,
        'strongest_supported_claim':'Without an independently bounded RGB/reference clock error, no finite physiological lag can be certified from an observed lag; EVE Basler is a synchronization positive-control candidate, but EVE documentation alone cannot certify 67-ms lag or consumer device holdout.',
        'product_decision':'Two-tier validation: Basler synchronized physiological positive control first, independently synchronized consumer RGB device transfer second. Fail closed on unknown clock error.'
    }

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='RESULTS.json');args=p.parse_args()
    output=run();Path(args.output).write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'trials':output['deterministic_trials'],'covered':output['interval_covered'],
                      'eligibility':output['eligibility']},sort_keys=True))
