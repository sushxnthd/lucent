#!/usr/bin/env python3
"""E002-447: sharp single-measurement Lipschitz bounds for idealized aperture averages.

NOT a pixel-to-aperture calibration, human velocity estimate or release authority.
"""
import json
import math

def finite_nonnegative(name, value):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return float(value)

def inputs(y, velocity, target, clock_error):
    y = finite_nonnegative("aperture mean", y)
    velocity = finite_nonnegative("velocity", velocity)
    clock_error = finite_nonnegative("clock error", clock_error)
    if isinstance(target, bool) or not isinstance(target, (float, int)) or not math.isfinite(target):
        raise ValueError("target time must be finite")
    return y, velocity, float(target), clock_error

def mean_distance_boxcar(target, center, width):
    """Exact E|U-target| for U uniform on [center-width/2,center+width/2]."""
    finite_nonnegative("width", width)
    if width == 0:
        raise ValueError("exposure width must be positive")
    if not isinstance(center, (int, float)) or isinstance(center, bool) or not math.isfinite(center):
        raise ValueError("center must be finite")
    if not isinstance(target, (int, float)) or isinstance(target, bool) or not math.isfinite(target):
        raise ValueError("target must be finite")
    d = abs(target-center)
    return width/4 + d*d/width if d < width/2 else d

def lower_boxcar(y, velocity, target, center, width, clock_error=0):
    y, velocity, target, clock_error = inputs(y, velocity, target, clock_error)
    # Worst offset of a convex shutter-distance function lies at the uncertainty boundary.
    distance = mean_distance_boxcar(abs(target-center)+clock_error, 0., width)
    return max(0., y-velocity*distance)

def lower_known_kernel(y, velocity, target, times, weights, clock_error=0):
    y, velocity, target, clock_error = inputs(y, velocity, target, clock_error)
    if not times or len(times) != len(weights):
        raise ValueError("nonempty aligned kernel times and weights required")
    if any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in times):
        raise ValueError("invalid kernel time")
    ws = [finite_nonnegative("kernel weight", w) for w in weights]
    if not math.isclose(sum(ws), 1., rel_tol=0., abs_tol=1e-10):
        raise ValueError("kernel weights must sum to one")
    def distance(t):
        return sum(w*abs(u-t) for u,w in zip(times,ws))
    d = max(distance(target-clock_error),distance(target+clock_error))
    return max(0., y-velocity*d)

def lower_support_only(y, velocity, target, center, width, clock_error=0):
    y, velocity, target, clock_error = inputs(y, velocity, target, clock_error)
    finite_nonnegative("width", width)
    if width == 0:
        raise ValueError("exposure width must be positive")
    if not isinstance(center, (int, float)) or isinstance(center, bool) or not math.isfinite(center):
        raise ValueError("center must be finite")
    # Sharp worst case over nonnegative normalized kernels supported in this interval.
    return max(0., y-velocity*(abs(target-center)+clock_error+width/2))

def shutter_average_piecewise_witness(y, velocity, width, t):
    """Equal-mean V-shaped witness, defined only on the exposure interval."""
    y = finite_nonnegative("aperture mean", y)
    velocity = finite_nonnegative("velocity", velocity)
    finite_nonnegative("width", width)
    if width <= 0:
        raise ValueError("exposure width must be positive")
    if not math.isfinite(t) or abs(t)>width/2:
        raise ValueError("witness time outside exposure")
    correction=velocity*width/4
    if y>=correction:
        return y-correction+velocity*abs(t)
    return (4*y/width)*abs(t)

def product_gate(*, physical_aperture=False, calibrated_shutter=False,
                 calibrated_clock=False, independently_bounded_velocity=False,
                 nuisance_validated=False):
    all_ready=all((physical_aperture,calibrated_shutter,calibrated_clock,
                   independently_bounded_velocity,nuisance_validated))
    return {"instrument_model_ready": all_ready,
            "status": "CONDITIONAL_MODEL_ONLY_EXTERNAL_REVIEW_REQUIRED" if all_ready else "ABSTAIN_UNCALIBRATED",
            "physical_release_authorized": False,
            "blink_duration_authorized": False,
            "perclos_authorized": False,
            "fatigue_authorized": False}

def experiment():
    y,v,w,threshold=3.,240.,0.010,2.8
    box=lower_boxcar(y,v,0.,0.,w)
    unknown=lower_support_only(y,v,0.,0.,w)
    delta=lower_boxcar(y,v,0.,0.,w,.001)
    return {"experiment":"E002-447", "evidence":"SYNTHETIC_IDEALIZED_APERTURE_INTEGRATION_ONLY",
            "aperture_mean_mm":y,"velocity_assumed_mm_s":v,"shutter_width_s":w,
            "closure_threshold_mm":threshold,
            "constant_world_aperture_at_center_mm":y,
            "v_world_aperture_at_center_mm":shutter_average_piecewise_witness(y,v,w,0.),
            "equal_shutter_mean_mm":y,
            "boxcar_sharp_center_lower_mm":box,
            "unknown_kernel_support_only_lower_mm":unknown,
            "boxcar_clock_1ms_lower_mm":delta,
            "point_substitution_claims_open":y>threshold,
            "witness_has_hidden_closure":box<=threshold,
            "observation_identifies_closure_status":False,
            "human_eyelid_aperture_measured":False,
            "physiological_speed_cap_validated":False,
            "physical_shutter_calibrated":False,
            "S21_S22_holdouts_inspected":False,
            "e002_371_physical_validation":"NOT_ESTABLISHED",
            "product":product_gate()}

if __name__ == "__main__":
    print(json.dumps(experiment(),sort_keys=True,indent=2))
