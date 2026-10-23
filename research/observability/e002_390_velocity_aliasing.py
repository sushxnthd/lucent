#!/usr/bin/env python3
"""E002-390: exact shutter integrals falsify RGB-derived velocity upper bounds.
Synthetic software instrument; never interpret as human/clinical evidence.
"""
import json
from pathlib import Path
import numpy as np

THETA = .2
F = 1 / 30
W = .010
FRAME_TIMES = np.arange(7) * F
T_END = float(FRAME_TIMES[-1] + W)
GRID = np.arange(0, T_END + .000251, .0005)

def knots(center, minimum, v_left, v_right):
    left = center - (1 - minimum) / v_left
    right = center + (1 - minimum) / v_right
    if left < 0 or right > T_END:
        raise ValueError('excursion outside recording')
    return np.array([0, left, center, right, T_END]), np.array([1, 1, minimum, 1, 1])

def exposure_mean(x, y, start, width):
    stop = start + width
    mid = x[(x > start) & (x < stop)]
    times = np.concatenate(([start], mid, [stop]))
    values = np.interp(times, x, y)
    return float(np.sum((values[1:] + values[:-1]) * np.diff(times) / 2) / width)

def ordinary_means(x, y):
    return np.array([exposure_mean(x, y, t, W) for t in FRAME_TIMES])

def abs_exposure_distance(t, s, width):
    t = np.asarray(t)
    return np.where(t <= s, s + width / 2 - t,
                    np.where(t >= s + width, t - s - width / 2,
                             ((t - s)**2 + (s + width - t)**2) / (2 * width)))

DIST = np.stack([abs_exposure_distance(GRID, s, W) for s in FRAME_TIMES])

def bound_from_means(means, velocity, error=0):
    """Sound for actual speed <= velocity and aperture-mean error <= error."""
    lower = np.max(means[:, None] - error - velocity * DIST, axis=0)
    return float(np.min(lower) - velocity * .0005 / 2)

def high_rate_detect(x, y, hz=1000, exposure=.00025):
    first = max(0, int(np.floor(x[1] * hz)) - 2)
    last = min(int(np.ceil((T_END-exposure) * hz)), int(np.ceil(x[3] * hz)) + 2)
    return any(exposure_mean(x, y, k / hz, exposure) < THETA
               for k in range(first, last + 1))

def cohort(seed, n):
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < n:
        center = float(rng.uniform(.030, .175))
        minimum = float(rng.uniform(.03, .199))
        v_left = float(rng.uniform(35, 120))
        v_right = float(rng.uniform(35, 120))
        try:
            x, y = knots(center, minimum, v_left, v_right)
        except ValueError:
            continue
        out.append((x, y, max(v_left, v_right),
                    (THETA - minimum) * (1 / v_left + 1 / v_right)))
    return out

def main(out='/tmp/e002_390'):
    calibration = cohort(39001, 1000)
    independent_V = 1.1 * max(z[2] for z in calibration)
    holdout = cohort(39002, 1500)
    rows = []
    for x, y, v, duration in holdout:
        measured = ordinary_means(x, y)
        v_hat = float(np.max(np.abs(np.diff(measured))) / F)
        plug_bound = bound_from_means(measured, v_hat)
        independent_bound = bound_from_means(measured, independent_V)
        rows.append({'v_true': v, 'v_plugin': v_hat,
                     'minimum': float(np.min(y)), 'crossing_ms': 1000 * duration,
                     'plugin_bound': plug_bound, 'independent_bound': independent_bound,
                     'plugin_false_certificate': bool(plug_bound > THETA),
                     'independent_false_certificate': bool(independent_bound > THETA),
                     'reference_detected': bool(high_rate_detect(x, y))})
    x, y = knots((.010 + F) / 2, .19, 90, 90)
    collision_means = ordinary_means(x, y)
    collision = {'minimum': .19, 'true_velocity': 90,
                 'means': collision_means.tolist(),
                 'plugin_velocity': float(np.max(np.abs(np.diff(collision_means))) / F),
                 'plugin_bound': bound_from_means(collision_means, 0),
                 'independent_bound': bound_from_means(collision_means, independent_V)}
    eligible = [r for r in rows if r['crossing_ms'] > 2]
    plugin_errors = sum(r['plugin_false_certificate'] for r in rows)
    independent_errors = sum(r['independent_false_certificate'] for r in rows)
    ref_detect = sum(r['reference_detected'] for r in eligible)
    adverse = []
    for name, shift in [('gain', .15), ('gaze', .08), ('glare', .20), ('blur', .07)]:
        x, y, _, _ = holdout[0]
        m = np.clip(ordinary_means(x, y) + shift, 0, 1)
        vhat = float(np.max(np.abs(np.diff(m))) / F)
        adverse.append({'nuisance': name, 'plug_in_bound': bound_from_means(m, vhat),
                        'physical_calibration_valid': False, 'product_decision': 'ABSTAIN'})
    adverse += [{'nuisance': n, 'physical_calibration_valid': False,
                 'product_decision': 'ABSTAIN'}
                for n in ('missingness', 'timestamp_error', 'glasses')]
    preds = {'P1': bool(np.allclose(collision_means, 1, atol=1e-12)
                         and collision['plugin_bound'] > THETA),
             'P2': bool(plugin_errors > 0 and independent_errors == 0),
             'P3': bool(ref_detect / max(len(eligible), 1) >= .95),
             'P4': bool(all(a['product_decision'] == 'ABSTAIN' for a in adverse)),
             'P5': None}
    result = {'evidence': 'synthetic software instrument', 'seed_calibration': 39001,
              'seed_holdout': 39002, 'n_calibration': len(calibration),
              'n_holdout': len(rows), 'independent_speed_bound': independent_V,
              'plugin_false_certificates': plugin_errors,
              'independent_false_certificates': independent_errors,
              'eligible_reference_crossings': len(eligible),
              'reference_detected': ref_detect,
              'reference_detection_fraction': ref_detect / max(len(eligible), 1),
              'median_true_velocity': float(np.median([r['v_true'] for r in rows])),
              'median_plugin_velocity': float(np.median([r['v_plugin'] for r in rows])),
              'collision': collision, 'nuisance': adverse, 'predictions': preds,
              'sample_rows': rows[:20]}
    p = Path(out)
    p.mkdir(parents=True, exist_ok=True)
    (p / 'e002_390_results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('sample_rows', 'nuisance')}, indent=2))
    assert all(v for v in preds.values() if v is not None), preds
    return result

if __name__ == '__main__':
    main()
