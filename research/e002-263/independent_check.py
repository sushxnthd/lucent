#!/usr/bin/env python3
"""Independent algebraic oracle + tamper negative control for E002-263."""
import copy
import json
from fractions import Fraction
from pathlib import Path


def verify(result):
    assert result['run'] == 'E002-263'
    assert result['type'] == 'synthetic geometry only'
    assert result['human_validation'] is False
    assert result['product_certification'] is False
    r = Fraction('0.35')
    assert result['true_pupil_over_iris_radius'] == float(r)
    assert result['exact_fraction_checks'] == 15
    assert len(result['rows']) == 6
    for row in result['rows']:
        k = Fraction(str(row['k']))
        expected = r * (1-k*k) / (1-k*k*r*r)
        assert abs(row['exact_projective_cross_ratio_estimate']-float(r)) < 1e-8
        assert abs(row['naive_projected_radius_ratio']-float(expected)) < 1e-8
        assert abs(row['naive_relative_bias_percent'] - (float(expected/r)-1)*100) < 0.00051
        assert row['accepted'] + row['invalid'] == row['n'] == 4000
        assert row['noise_sigma_px'] == 0.5
        assert row['fixed_iris_span_px'] == 120.0
        assert row['cr_rmse'] is not None and row['cr_rmse'] >= 0
        assert row['naive_rmse'] is not None and row['naive_rmse'] >= 0
    assert len(result['off_center_probe']) == 4
    assert len(result['nonprojective_probe']) == 4
    return True


def main():
    path = Path(__file__).with_name('RESULTS.json')
    results = json.loads(path.read_text())
    verify(results)
    tampered = copy.deepcopy(results)
    tampered['rows'][2]['naive_relative_bias_percent'] = 0.0
    rejected = False
    try:
        verify(tampered)
    except AssertionError:
        rejected = True
    assert rejected, 'adversarial corruption must be rejected'
    print('PASS: exact rational independent oracle, accounting, and tamper rejection')

if __name__ == '__main__':
    main()
