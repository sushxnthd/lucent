#!/usr/bin/env python3
"""E002-452: conditional gaze-stratified Lipschitz boundary and fail-closed release gate.

Velocity caps here are hypothetical inputs, NOT empirical human bounds.
No physical certification or product claim can be obtained from this module.
"""
import argparse
import json
import math

GAZE = frozenset(('upward', 'neutral', 'downward'))
BEHAVIOR = frozenset(('spontaneous', 'voluntary', 'reflexive', 'soft_closure', 'forced_closure'))


def _finite_nonnegative(value, name):
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ValueError(f'{name} must be finite and nonnegative')
    return float(value)


def conditional_boundary(*, a0_mm, a1_mm, threshold_mm, gap_s, velocity_cap_mm_s,
                         gaze_stratum, behavior, clock_uncertainty_s=0.0,
                         aperture_source='instantaneous', evidence_tier='hypothetical'):
    """Sharp endpoint lower envelope under an *assumed* global Lipschitz bound.

    Camera exposure averages and group mean velocities are NOT certified
    instantaneous points or physiological upper bounds.
    """
    if gaze_stratum not in GAZE or behavior not in BEHAVIOR:
        raise ValueError('explicit supported gaze and behavior strata required')
    if aperture_source != 'instantaneous':
        raise ValueError('shutter-averaged or unknown aperture cannot be used as an endpoint')
    if evidence_tier != 'hypothetical':
        raise ValueError('this simulator cannot validate physical evidence or claims')
    a0 = _finite_nonnegative(a0_mm, 'a0_mm')
    a1 = _finite_nonnegative(a1_mm, 'a1_mm')
    c = _finite_nonnegative(threshold_mm, 'threshold_mm')
    gap = _finite_nonnegative(gap_s, 'gap_s')
    v = _finite_nonnegative(velocity_cap_mm_s, 'velocity_cap_mm_s')
    clock = _finite_nonnegative(clock_uncertainty_s, 'clock_uncertainty_s')
    if c > max(a0, a1):
        raise ValueError('threshold above both observed endpoints')
    upper_gap = gap + 2 * clock
    if not math.isfinite(upper_gap) or not math.isfinite(v * upper_gap):
        raise ValueError('overflow in uncertain time or travel budget')
    if abs(a0-a1) > v * upper_gap + 1e-12:
        raise ValueError('endpoint observations inconsistent with assumed speed cap')
    # a(t) >= max(a0-v*t, a1-v*(T-t)); intersection is the sharp lower envelope.
    lower = (a0 + a1 - v * upper_gap) / 2
    denom = a0 + a1 - 2*c
    if min(a0,a1) <= c or denom <= 0:
        outcome = 'THRESHOLD_ALREADY_OBSERVED_AT_ENDPOINT'
        ratio = None
    else:
        ratio = v * upper_gap / denom
        outcome = ('HIDDEN_CROSSING_FEASIBLE_UNDER_ASSUMPTIONS'
                   if lower <= c + 1e-12 else 'HIDDEN_CROSSING_EXCLUDED_UNDER_ASSUMPTIONS')
    return {'gaze_stratum': gaze_stratum, 'behavior': behavior,
            'conditional_min_aperture_mm': round(lower, 10),
            'dimensionless_travel_ratio': None if ratio is None else round(ratio, 10),
            'gap_upper_s': round(upper_gap, 10), 'conditional_outcome': outcome,
            'evidence_tier': 'SYNTHETIC_CONDITIONAL_ONLY',
            'physical_release_authorized': False,
            'product_claim': 'ABSTAIN_UNCALIBRATED'}


def physical_release_gate(_record=None):
    """Fail closed: caller-supplied attestations cannot replace independent review."""
    return {'decision': 'ABSTAIN_UNCALIBRATED',
            'reason': 'NO_INDEPENDENT_PHYSICAL_EVIDENCE_VERIFIER',
            'requires': ['authenticated_shutter_and_clock', 'calibrated_anatomical_scale',
                         'independent_stratum_valid_upper_velocity_bound',
                         'nuisance_envelope_and_gaze_tracking',
                         'participant_disjoint_prospective_validation',
                         'independent_external_review'],
            'physical_release_authorized': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--conditional-fixture', action='store_true',
                   help='print two explicitly hypothetical gaze-stratified scenarios')
    a = p.parse_args()
    if a.conditional_fixture:
        base = dict(a0_mm=3.0, a1_mm=3.0, threshold_mm=2.0, gap_s=.0095,
                    behavior='voluntary')
        result = {'upward_hypothetical': conditional_boundary(**base, gaze_stratum='upward', velocity_cap_mm_s=200),
                  'downward_hypothetical': conditional_boundary(**base, gaze_stratum='downward', velocity_cap_mm_s=221),
                  'release_gate': physical_release_gate()}
    else:
        result = physical_release_gate()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
