#!/usr/bin/env python3
"""E002-486: exact-rational shutter/reference-aliasing experiment (synthetic only)."""
import argparse
import json
import unittest
from fractions import Fraction as F

T = F(20, 3)  # ms, 150 fps
E = F(1)
B = F(7, 20)
C = F(1, 10)
V = F(1, 10)  # fraction per ms, illustrative hard cap
HALF = F(1, 2)


def aperture(t, closing=True, velocity=V, dip_min=C):
    if not closing:
        return B
    if velocity <= 0:
        raise ValueError('velocity must be positive')
    nearest = min((abs(t - (F(k) + HALF) * T) for k in range(-5, 6)))
    return B - max(F(0), B - dip_min - velocity * nearest)


def exposure_mean(center, closing=True, velocity=V, exposure=E, dip_min=C):
    if exposure <= 0 or exposure > T:
        raise ValueError('invalid exposure')
    lo, hi = center - exposure / 2, center + exposure / 2
    knots = [lo, hi]
    if closing:
        d = (B - dip_min) / velocity
        for k in range(-5, 6):
            m = (F(k) + HALF) * T
            knots += [q for q in (m - d, m, m + d) if lo < q < hi]
    knots = sorted(set(knots))
    integral = sum((knots[i+1]-knots[i]) *
                   (aperture(knots[i], closing, velocity, dip_min) + aperture(knots[i+1], closing, velocity, dip_min)) / 2
                   for i in range(len(knots)-1))
    return integral / exposure


def ratio(velocity=V, exposure=E):
    return velocity * (T-exposure) / (2 * (B-C))


def bound(phase_error, gain_error, additive_error, velocity=V):
    jitter_values = [-phase_error, F(0), phase_error]
    moving_means = [exposure_mean(T/2+j, True, velocity) for j in jitter_values]
    return {
        'moving_max': max(moving_means),
        'moving_observed_max': max(moving_means)*(1+gain_error)+additive_error,
        'stationary_observed_min': B*(1-gain_error)-additive_error,
    }


def fmt(x):
    return {'rational': str(x), 'decimal': round(float(x), 10)}


def aggregate():
    base = bound(F(1,4), F(1,10), F(1,100))
    improved = bound(F(1,4), F(1,20), F(1,200))
    degraded = bound(F(1,4), F(1,5), F(3,100))
    return {
        'protocol': 'E002-486',
        'evidence_tier': 'EXACT_RATIONAL_SYNTHETIC_INSTRUMENT',
        'acquisition_hz': 150, 'exposure_ms': fmt(E),
        'baseline_aperture': fmt(B), 'closure_threshold': fmt(C),
        'illustrative_velocity_fraction_per_ms': fmt(V),
        'dimensionless_hidden_closure_ratio': fmt(ratio()),
        'critical_velocity_fraction_per_ms': fmt(2*(B-C)/(T-E)),
        'stationary_nominal_exposure': fmt(exposure_mean(F(0), False)),
        'closing_nominal_exposure': fmt(exposure_mean(F(0), True)),
        'stationary_half_phase_exposure': fmt(exposure_mean(T/2, False)),
        'closing_half_phase_exposure': fmt(exposure_mean(T/2, True)),
        'strict_below_threshold_dip_min': fmt(F(2,25)),
        'strict_below_threshold_original_phase_exposure': fmt(exposure_mean(F(0), True, dip_min=F(2,25))),
        'moving_half_phase_jitter_max_0_25ms': fmt(base['moving_max']),
        'threshold_0_15_with_gain_10pct_additive_0_01': {
            'moving_upper': fmt(base['moving_observed_max']),
            'stationary_lower': fmt(base['stationary_observed_min']),
            'guaranteed_detection': base['moving_observed_max'] <= F(3,20),
        },
        'threshold_0_15_with_gain_5pct_additive_0_005': {
            'moving_upper': fmt(improved['moving_observed_max']),
            'stationary_lower': fmt(improved['stationary_observed_min']),
            'guaranteed_detection': improved['moving_observed_max'] <= F(3,20),
        },
        'threshold_0_15_with_gain_20pct_additive_0_03': {
            'moving_upper': fmt(degraded['moving_observed_max']),
            'stationary_lower': fmt(degraded['stationary_observed_min']),
            'guaranteed_detection': degraded['moving_observed_max'] <= F(3,20),
        },
        'low_velocity_control_ratio': fmt(ratio(F(2,25))),
        'low_velocity_hidden_closure_possible': ratio(F(2,25)) >= 1,
        'physical_human_sequences': 0,
        'physical_shutter_acquisitions': 0,
        'physical_claims': 'ABSTAIN_UNCALIBRATED',
        'product_release': 'BLOCKED',
    }


class Tests(unittest.TestCase):
    def test_ratio_exact(self): self.assertEqual(ratio(), F(17,15))
    def test_critical_speed(self): self.assertEqual(2*(B-C)/(T-E), F(3,34))
    def test_original_phase_indistinguishable(self):
        for k in range(-3,4):
            self.assertEqual(exposure_mean(k*T, True), B)
            self.assertEqual(exposure_mean(k*T, False), B)
    def test_closed_at_midpoint(self): self.assertEqual(aperture(T/2), C)
    def test_open_at_exposure_edges(self):
        self.assertEqual(aperture(E/2), B)
        self.assertEqual(aperture(T-E/2), B)
    def test_half_phase_probe(self): self.assertEqual(exposure_mean(T/2, True), F(1,8))
    def test_half_phase_control(self): self.assertEqual(exposure_mean(T/2, False), B)
    def test_strict_below_threshold_hidden(self):
        self.assertLess(F(2,25), C)
        self.assertEqual(aperture(T/2, dip_min=F(2,25)), F(2,25))
        self.assertEqual(exposure_mean(F(0), True, dip_min=F(2,25)), B)
        self.assertEqual(exposure_mean(T, True, dip_min=F(2,25)), B)
    def test_jitter_exact(self):
        self.assertEqual(exposure_mean(T/2+F(1,4), True), F(21,160))
        self.assertEqual(exposure_mean(T/2-F(1,4), True), F(21,160))
    def test_10pct_gain_falsifies_frozen_guarantee(self):
        self.assertEqual(bound(F(1,4),F(1,10),F(1,100))['moving_observed_max'],F(247,1600))
        self.assertGreater(F(247,1600),F(3,20))
    def test_5pct_gain_restores_threshold(self):
        self.assertLess(bound(F(1,4),F(1,20),F(1,200))['moving_observed_max'],F(3,20))
    def test_20pct_gain_fails(self):
        self.assertGreater(bound(F(1,4),F(1,5),F(3,100))['moving_observed_max'],F(3,20))
    def test_low_velocity_cannot_hide(self): self.assertLess(ratio(F(2,25)),1)
    def test_shutter_longer_reduces_ratio(self): self.assertLess(ratio(exposure=F(2)),ratio())
    def test_negative_phase_control(self):
        self.assertEqual(exposure_mean(F(0),True),exposure_mean(F(0),False))
    def test_product_fail_closed(self):
        self.assertEqual(aggregate()['product_release'],'BLOCKED')
        self.assertEqual(aggregate()['physical_claims'],'ABSTAIN_UNCALIBRATED')


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--aggregate',action='store_true')
    args=p.parse_args()
    if args.self_test:
        unittest.main(argv=['e002_486_reference_alias.py'],verbosity=2)
    elif args.aggregate:
        print(json.dumps(aggregate(),indent=2,sort_keys=True))
    else:
        p.print_help()
