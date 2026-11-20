"""E002-430: finite-rate human-reference alias; synthetic, no human trials.

A high-speed acquisition rate is not a continuous-time closure oracle. The
reference margin is conditional on a *hard* physical speed bound, authenticated
sample timing and independently bounded aperture measurement error.
"""
from __future__ import annotations
import json
import math

THRESHOLD_MM = 2.0
SAMPLED_APERTURE_MM = 2.15
HIDDEN_MINIMUM_MM = 1.95
ILLUSTRATIVE_SPEED_MM_S = 243.0  # Published group mean, NOT a hard bound.


def _positive_finite(x, name, allow_zero=False):
    if not isinstance(x, (int, float)) or not math.isfinite(x) or (x < 0 if allow_zero else x <= 0):
        raise ValueError(f"{name} must be {'nonnegative' if allow_zero else 'positive'} finite")


def envelope_lower(left_mm, right_mm, interval_s, speed_cap_mm_s, aperture_error_mm=0.0, clock_jitter_s=0.0):
    """Conservative Lipschitz lower envelope between two physical aperture samples.

    Each sample has absolute error <= aperture_error_mm; each timestamp has
    absolute error <= clock_jitter_s. This is a mathematical conditional bound.
    A published average/peak velocity is not an authenticated speed cap.
    """
    for name, value in [('left_mm',left_mm),('right_mm',right_mm),('interval_s',interval_s),('speed_cap_mm_s',speed_cap_mm_s)]:
        _positive_finite(value,name)
    _positive_finite(aperture_error_mm,'aperture_error_mm',True)
    _positive_finite(clock_jitter_s,'clock_jitter_s',True)
    a, b = left_mm-aperture_error_mm, right_mm-aperture_error_mm
    d = interval_s + 2*clock_jitter_s
    v = speed_cap_mm_s
    return max((a+b-v*d)/2, a-v*d, b-v*d, 0.0)


def synthetic_alias(sample_rate_hz, aperture_at_samples_mm=SAMPLED_APERTURE_MM, minimum_mm=HIDDEN_MINIMUM_MM):
    """Two continuous traces identical at all sampling instants, one closing.

    World B is triangular in one sample interval, constant elsewhere.
    """
    _positive_finite(sample_rate_hz, 'sample_rate_hz')
    _positive_finite(aperture_at_samples_mm, 'aperture_at_samples_mm')
    _positive_finite(minimum_mm, 'minimum_mm', True)
    if minimum_mm >= aperture_at_samples_mm:
        raise ValueError('minimum must be lower than sample aperture')
    dt = 1.0/sample_rate_hz
    slope = 2*(aperture_at_samples_mm-minimum_mm)/dt
    def hidden(t):
        if t <= 0 or t >= dt:
            return aperture_at_samples_mm
        return aperture_at_samples_mm-(aperture_at_samples_mm-minimum_mm)*(1-abs(2*t/dt-1))
    return {
        'reference_rate_hz': sample_rate_hz,
        'reference_step_ms': 1000*dt,
        'sampled_aperture_mm': aperture_at_samples_mm,
        'open_world_minimum_mm': aperture_at_samples_mm,
        'hidden_world_minimum_mm': minimum_mm,
        'hidden_world_peak_speed_mm_s': slope,
        'sampled_worlds_equal': all(abs(hidden(i*dt)-aperture_at_samples_mm)<1e-12 for i in range(-5,6)),
        'reference_samples_naively_no_closure': aperture_at_samples_mm > THRESHOLD_MM,
        'continuous_hidden_world_crosses_threshold': minimum_mm <= THRESHOLD_MM,
        'illustrative_speed_envelope_mm': envelope_lower(aperture_at_samples_mm,aperture_at_samples_mm,dt,ILLUSTRATIVE_SPEED_MM_S),
        'illustrative_speed_cap_is_authenticated': False,
        'reference_negative_authorized': False,
        'product': 'ABSTAIN_UNCALIBRATED',
    }


def experiment():
    return {
        'evidence_tier': 'SYNTHETIC_HIGH_RATE_REFERENCE_ALIAS',
        'published_velocity_mm_s_used_for_sensitivity_only': ILLUSTRATIVE_SPEED_MM_S,
        'source_doi': '10.1098/rsif.2013.0227',
        'note': '2013 study acquired at 600 fps but annotated central aperture every 5 ms; neither sample rate nor group-mean speed is a hard physical guarantee.',
        'cases': [synthetic_alias(rate) for rate in (200,400,500,600)],
        'five_ms_annotation_case': synthetic_alias(200),
        'physical_certificate_authorized': False,
        'product': 'ABSTAIN_UNCALIBRATED',
    }

if __name__ == '__main__':
    print(json.dumps(experiment(), indent=2, sort_keys=True))
