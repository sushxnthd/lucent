"""E002-429: adversarial geometry/physical-aperture alias in a restricted orthographic model.

Synthetic, not a human study or a real-camera certificate. Standard library only.
The factor cos(phi) represents a deliberately simplified effective projection
factor, not a physiological gaze-to-aperture calibration.
"""
import json
import math

FRAME_PERIOD_S = 1 / 30
EXPOSURE_S = 0.004
THRESHOLD_MM = 2.0
VELOCITY_CAP_MM_S = 1.2
OPEN_MM = 2.04
ALIased_ENDPOINT_MM = 2.01
ALIased_MIN_MM = 1.99
REFERENCE_ANGLE_DEG = 20.0


def hidden_aperture(t):
    """Physical V-shaped aperture; flat before/after the shutter-center interval."""
    if t <= 0 or t >= FRAME_PERIOD_S:
        return ALIased_ENDPOINT_MM
    u = t / FRAME_PERIOD_S
    return ALIased_ENDPOINT_MM - (ALIased_ENDPOINT_MM - ALIased_MIN_MM) * (1 - abs(2 * u - 1))


def effective_angle_deg(h):
    ratio = OPEN_MM * math.cos(math.radians(REFERENCE_ANGLE_DEG)) / h
    if not (0 <= ratio <= 1):
        raise ValueError('geometry factor outside physical cosine range')
    return math.degrees(math.acos(ratio))


def pixel_observable(h, phi_deg):
    return h * math.cos(math.radians(phi_deg))


def boxcar_average(func, center, exposure=EXPOSURE_S, n=2000):
    if n < 2 or n % 2 or exposure <= 0:
        raise ValueError('even n>=2 and positive exposure required')
    # Composite midpoint quadrature independent of the analytical identity.
    step = exposure / n
    return sum(func(center - exposure / 2 + (j + .5) * step) for j in range(n)) / n


def projected_lower_bound(observed_projected_mm, angle_min_deg, angle_max_deg):
    """Instantaneous physical lower bound for y=H*cos(phi), NOT a temporal bound."""
    if not (math.isfinite(observed_projected_mm) and observed_projected_mm >= 0
            and 0 <= angle_min_deg <= angle_max_deg < 90):
        raise ValueError('invalid projected measurement or independently calibrated angle interval')
    return observed_projected_mm / math.cos(math.radians(angle_min_deg))


def experiment():
    open_projected = pixel_observable(OPEN_MM, REFERENCE_ANGLE_DEG)
    def open_trace(t):
        return pixel_observable(OPEN_MM, REFERENCE_ANGLE_DEG)
    def hidden_trace(t):
        h = hidden_aperture(t)
        return pixel_observable(h, effective_angle_deg(h))
    samples = [i * FRAME_PERIOD_S / 1000 for i in range(1001)]
    mismatch = max(abs(open_trace(t) - hidden_trace(t)) for t in samples)
    max_velocity = (ALIased_ENDPOINT_MM - ALIased_MIN_MM) * 2 / FRAME_PERIOD_S
    a = boxcar_average(hidden_trace, 0)
    b = boxcar_average(hidden_trace, FRAME_PERIOD_S)
    # Incorrect if y is converted to mm with an unauthenticated fixed phi.
    fixed_angle_estimate = (a + b) / (2 * math.cos(math.radians(REFERENCE_ANGLE_DEG)))
    naive_sharp_lower = fixed_angle_estimate - VELOCITY_CAP_MM_S * FRAME_PERIOD_S / 2
    # Independently validated 15..20 deg effective-angle interval changes the decision.
    geometry_lower = projected_lower_bound(open_projected, 15, 20)
    return {
        'tier': 'SYNTHETIC_ORTHOGRAPHIC_COUNTEREXAMPLE',
        'physical_certificate_authorized': False,
        'product': 'ABSTAIN_UNCALIBRATED',
        'period_s': FRAME_PERIOD_S,
        'exposure_s': EXPOSURE_S,
        'threshold_mm': THRESHOLD_MM,
        'physical_speed_cap_mm_s': VELOCITY_CAP_MM_S,
        'witness_physical_speed_mm_s': max_velocity,
        'world_a_physical_min_mm': OPEN_MM,
        'world_b_physical_min_mm': ALIased_MIN_MM,
        'world_a_projection_deg': REFERENCE_ANGLE_DEG,
        'world_b_projection_deg_at_end': effective_angle_deg(ALIased_ENDPOINT_MM),
        'world_b_projection_deg_at_min': effective_angle_deg(ALIased_MIN_MM),
        'projected_measurement_mm_like': open_projected,
        'continuous_projected_trace_max_difference': mismatch,
        'first_exposure_average': a,
        'second_exposure_average': b,
        'naive_fixed_angle_aperture_estimate_mm': fixed_angle_estimate,
        'naive_fixed_angle_sharp_lower_mm': naive_sharp_lower,
        'naive_would_claim_no_closure': naive_sharp_lower > THRESHOLD_MM,
        'independent_angle_interval_deg': [15, 20],
        'instantaneous_geometry_lower_mm': geometry_lower,
        'interval_guard_rejects': geometry_lower <= THRESHOLD_MM,
    }


if __name__ == '__main__':
    print(json.dumps(experiment(), indent=2, sort_keys=True))
