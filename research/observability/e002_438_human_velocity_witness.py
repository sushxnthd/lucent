#!/usr/bin/env python3
"""E002-438: falsification-only velocity witness; no physical certification.

Published aggregates are evidence *against* certain candidate universal caps,
not evidence for any universal cap. Private traces must stay off public CI.
"""
import argparse
import json
import math
from pathlib import Path

PRODUCT = 'ABSTAIN_UNCALIBRATED'
NUISANCES = ('geometry', 'brightness', 'missingness', 'blur', 'gaze',
             'glasses', 'sampling', 'clock', 'occlusion', 'shutter')


class WitnessError(ValueError):
    pass


def number(value, name, strictly_positive=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise WitnessError('invalid ' + name)
    if (value <= 0 if strictly_positive else value < 0):
        raise WitnessError('out-of-range ' + name)
    return float(value)


def published_cap_audit(candidate_mm_s, metric='peak_closing_speed_mm_s'):
    """Audit candidate against a *reported cohort mean*, not individual data.

    Kwon et al. 2013, DOI 10.1098/rsif.2013.0227, 25 healthy adults,
    voluntary blinks at 600 fps, aperture measured at 5 ms increments.
    Reported mean peak closing speed 243 +/- 9 mm/s; +/-9 is NOT
    interpreted as a deterministic measurement error or a confidence bound.
    The half-unit margin below accounts only for reporting to nearest integer.
    """
    candidate = number(candidate_mm_s, 'candidate speed cap', True)
    result = {
        'evidence': 'PUBLISHED_HUMAN_AGGREGATE_NOT_RAW_TRACES',
        'source_doi': '10.1098/rsif.2013.0227',
        'cohort_n': 25,
        'reported_mean_peak_closing_mm_s': 243.0,
        'reported_plus_minus_mm_s': 9.0,
        'plus_minus_not_used_as_deterministic_error': True,
        'published_acquisition_fps': 600,
        'published_aperture_annotation_step_ms': 5.0,
        'candidate_mm_s': candidate,
        'metric': metric,
        'physical_certificate_authorized': False,
        'product': PRODUCT,
    }
    if metric != 'peak_closing_speed_mm_s':
        result['decision'] = 'UNRESOLVED_METRIC_MISMATCH'
    elif candidate < 242.5:
        # Arithmetic: maximum of per-participant peaks >= their mean.
        # This only rejects consistency with reported measured peak statistics.
        result['decision'] = 'INCOMPATIBLE_WITH_PUBLISHED_PEAK_MEAN'
    else:
        result['decision'] = 'NOT_FALSIFIED_BY_THIS_AGGREGATE'
    return result


def calibrated_pair_witness(record):
    """Necessary lower bound on sup|x'| from two calibrated sample intervals.

    With each aperture error <= eps and |true_t - nominal_t| <= delta,
    sup|x'| >= max(0, |y1-y0|-2eps)/(h+2delta). This can refute an
    externally proposed hard cap; it cannot establish an upper speed cap.
    """
    fields = {'trace_id', 'y0_mm', 'y1_mm', 't0_s', 't1_s',
              'aperture_error_mm', 'clock_error_s', 'candidate_cap_mm_s',
              'physical_scale_attested', 'sensor_timing_attested',
              'nuisance_flags', 'external_calibration_reference'}
    if type(record) is not dict or set(record) != fields:
        raise WitnessError('invalid record schema')
    if not isinstance(record['trace_id'], str) or not record['trace_id'].strip():
        raise WitnessError('invalid trace ID')
    if not isinstance(record['external_calibration_reference'], str) or not record['external_calibration_reference'].strip():
        raise WitnessError('missing calibration reference')
    y0 = number(record['y0_mm'], 'first aperture')
    y1 = number(record['y1_mm'], 'second aperture')
    t0 = number(record['t0_s'], 'first time')
    t1 = number(record['t1_s'], 'second time')
    eps = number(record['aperture_error_mm'], 'aperture error')
    delta = number(record['clock_error_s'], 'clock error')
    cap = number(record['candidate_cap_mm_s'], 'candidate cap', True)
    if t1 <= t0 or t1-t0 <= 2*delta:
        raise WitnessError('ambiguous sample order')
    for key in ('physical_scale_attested', 'sensor_timing_attested'):
        if type(record[key]) is not bool:
            raise WitnessError('invalid attestation flag')
    flags = record['nuisance_flags']
    if type(flags) is not dict or set(flags) != set(NUISANCES) or any(type(v) is not bool for v in flags.values()):
        raise WitnessError('invalid nuisance flags')
    result = {'experiment': 'E002-438', 'trace_id': record['trace_id'],
              'evidence': 'CONDITIONAL_PAIR_LOWER_WITNESS',
              'external_provenance_authenticated_by_code': False,
              'necessary_speed_lower_mm_s': None,
              'candidate_cap_mm_s': cap,
              'physical_certificate_authorized': False, 'product': PRODUCT}
    if not record['physical_scale_attested'] or not record['sensor_timing_attested'] or any(flags.values()):
        result['decision'] = 'ABSTAIN_UNCALIBRATED'
    else:
        lb = max(0.0, abs(y1-y0)-2*eps)/(t1-t0+2*delta)
        result['necessary_speed_lower_mm_s'] = lb
        result['decision'] = ('CONDITIONAL_CAP_FALSIFIED' if lb > cap + 1e-9
                              else 'CAP_NOT_FALSIFIED_BY_PAIR')
    return result


def equal_endpoint_scenario(aperture_mm, threshold_mm, fps,
                            scenario_speed_mm_s, aperture_error_mm=0,
                            clock_error_s=0):
    """A *scenario*, not an empirical or certified no-closure decision."""
    a = number(aperture_mm, 'aperture')
    theta = number(threshold_mm, 'threshold')
    f = number(fps, 'fps', True)
    v = number(scenario_speed_mm_s, 'scenario speed', True)
    e = number(aperture_error_mm, 'aperture error')
    d = number(clock_error_s, 'clock error')
    dt = 1/f + 2*d
    lower = a-e-v*dt/2
    rho = (a-e-theta)/(v*dt)
    return {'aperture_mm': a, 'threshold_mm': theta, 'fps': f,
            'scenario_speed_mm_s': v, 'scenario_not_hard_cap': True,
            'conditional_lower_mm': lower, 'dimensionless_margin': rho,
            'scenario_decision': ('CONDITIONAL_EXCLUSION_IF_PREMISES_TRUE'
                                  if lower > theta else 'UNRESOLVED'),
            'physical_certificate_authorized': False, 'product': PRODUCT}


def demonstration():
    return {'experiment': 'E002-438',
            'published_human_aggregate_audit': [published_cap_audit(v) for v in (120, 243, 300)],
            'equal_endpoint_scenarios': [equal_endpoint_scenario(6.0, 2.0, hz, 243.0)
                                         for hz in (25, 30, 60, 120, 250)],
            'independent_2026_context': {
                'doi_frame_rate': '10.1016/j.jtos.2026.01.003',
                '500_fps_participants_spontaneous': 20,
                '500_fps_participants_reflex': 10,
                'doi_reflex_comparison': '10.1080/08164622.2026.2619492',
                'reported_reflex_minus_spontaneous_closing_speed_mm_s': 177.7,
                'different_metric_or_cohort_not_combined_with_2013_mean': True},
            'physical_certificate_authorized': False, 'product': PRODUCT}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-pair', help='private calibrated two-frame JSON; do not upload')
    p.add_argument('--output', help='output JSON path')
    a = p.parse_args()
    result = calibrated_pair_witness(json.loads(Path(a.private_pair).read_text())) if a.private_pair else demonstration()
    rendered = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if a.output:
        Path(a.output).write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
