"""E002-531: exact native-marker missingness identifiability falsifier.

Synthetic instrument experiment only. Does not load human subject data.
"""
from __future__ import annotations

import json
from fractions import Fraction as F

HZ = 400
N = 80
C = F(1, 4)
MISSING = frozenset(range(30, 39))
TRIANGLE = [F(i, 5) for i in (4, 3, 2, 1, 0, 1, 2, 3, 4)]


def worlds():
    a = [F(1)] * N
    b = a.copy()
    for i, v in zip(sorted(MISSING), TRIANGLE):
        b[i] = v
    return a, b


def observed(series, missing=MISSING):
    return tuple(None if i in missing else x for i, x in enumerate(series))


def fill_linear(samples):
    """Fill missing interior samples by exact linear interpolation of observed brackets."""
    out = list(samples)
    i = 0
    while i < len(out):
        if out[i] is not None:
            i += 1
            continue
        left = i - 1
        j = i
        while j < len(out) and out[j] is None:
            j += 1
        if left < 0 or j >= len(out):
            raise ValueError("cannot fill unbracketed missing samples")
        x0, x1 = out[left], out[j]
        assert x0 is not None and x1 is not None
        for k in range(i, j):
            out[k] = x0 + (x1 - x0) * F(k - left, j - left)
        i = j
    return tuple(out)


def dwell_samples(series, threshold=C):
    """Exact time at/below threshold under piecewise-linear native-frame interpolation."""
    count = 0
    for x, y in zip(series[:-1], series[1:]):
        if x <= threshold and y <= threshold:
            count += F(1)
        elif x > threshold and y > threshold:
            continue
        elif x > threshold:
            count += (threshold - y) / (x - y)
        else:
            count += (threshold - x) / (y - x)
    return count / HZ


def sample_25fps(series, phase):
    if not 0 <= phase < 16:
        raise ValueError("phase must be native index 0..15")
    return tuple(series[i] for i in range(phase, len(series), 16))


def reference_decision(samples, threshold=C):
    if any(x is not None and x <= threshold for x in samples):
        return "POSITIVE_NATIVE_WITNESS"
    if any(x is None for x in samples):
        return "UNKNOWN_MISSING_NATIVE"
    return "NO_SAMPLED_WITNESS_NOT_CERTIFIED_NEGATIVE"


def max_slope(series):
    return max(abs(y-x)*HZ for x, y in zip(series[:-1], series[1:]))


def experiment():
    a, b = worlds()
    obs_a, obs_b = observed(a), observed(b)
    imp_a, imp_b = fill_linear(obs_a), fill_linear(obs_b)
    assert obs_a == obs_b
    assert imp_a == imp_b == tuple(a)
    assert dwell_samples(a) == F(0)
    assert dwell_samples(b) == F(1, 160)
    assert max_slope(b) == F(80)
    assert sum(x <= C for x in b) == 3
    assert sum(x <= C for x in sample_25fps(b, 0)) == 0
    assert sum(x <= C for x in sample_25fps(b, 1)) == 1
    assert reference_decision(obs_b) == "UNKNOWN_MISSING_NATIVE"
    return {
        "evidence_tier": "synthetic_instrument_counterexample_not_human_data",
        "native_hz": HZ,
        "threshold": str(C),
        "missing_indices": [min(MISSING), max(MISSING)],
        "missing_sample_span_ms": "22.5",
        "observed_bracket_ms": "25",
        "complete_world_a_closed_native_frames": 0,
        "complete_world_b_closed_native_frames": 3,
        "complete_world_b_piecewise_linear_dwell_s": str(dwell_samples(b)),
        "complete_world_b_max_slope_per_s": str(max_slope(b)),
        "identical_observed": obs_a == obs_b,
        "identical_imputed": imp_a == imp_b,
        "imputed_closed_native_frames": sum(x <= C for x in imp_b),
        "complete_25fps_phase0_closed_frames": sum(x <= C for x in sample_25fps(b, 0)),
        "complete_25fps_phase1_closed_frames": sum(x <= C for x in sample_25fps(b, 1)),
        "imputed_25fps_phase1_closed_frames": sum(x <= C for x in sample_25fps(imp_b, 1)),
        "reference_decision": reference_decision(obs_b),
        "product_release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
