"""E002-480: bounded-jitter phase-dither falsification (SYNTHETIC ONLY).

A passed geometric test does not authenticate a camera, anatomical eyelid
velocity, or a hidden-closure product claim.
"""
from __future__ import annotations
import json
import math

T = 1000.0 / 240.0
STEP = 0.05
W = 0.006
U = 0.004
CENTER = 2.01525
ISLAND_WIDTH = 0.0005
AMPLITUDE = 0.20
BASE = (0.4, 1.4)
THRESHOLD = 0.04
NOISE = 0.002
ABSTAIN = "ABSTAIN_UNCALIBRATED"

def nonnegative(name, x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0:
        raise ValueError(name + " must be finite and nonnegative")
    return float(x)

def overlap(a, b, c, d):
    return max(0., min(b, d) - max(a, c))

def periodic_overlap(a, b, center=CENTER, width=ISLAND_WIDTH):
    if b <= a:
        raise ValueError("nonpositive interval")
    lo = math.floor((a - center - width/2)/T)-1
    hi = math.ceil((b - center + width/2)/T)+1
    return sum(overlap(a, b, center-width/2+k*T, center+width/2+k*T)
               for k in range(lo, hi+1))

def response(start, island):
    if not math.isfinite(start):
        raise ValueError("invalid start")
    base = periodic_overlap(start, start+W, sum(BASE)/2, BASE[1]-BASE[0])
    extra = periodic_overlap(start, start+W)
    return (base + (AMPLITUDE*extra if island else 0))/W

def avoid_island(nominal, u=U):
    nonnegative("timing uncertainty", u)
    for delta in (-u, u):
        if periodic_overlap(nominal+delta, nominal+delta+W) <= 1e-13:
            return delta
    return None

def grid(n):
    if type(n) is not int or n < 1:
        raise ValueError("invalid dither factor")
    step = STEP/n
    return [i*step for i in range(math.ceil(2*T/step-1e-12)+1)]

def adversarial_grid(n):
    starts = grid(n)
    missed = 0
    difference = 0.
    used = set()
    for nominal in starts:
        shift = avoid_island(nominal)
        if shift is None:
            missed += 1
            continue
        used.add(shift)
        actual = nominal + shift
        difference = max(difference, abs(response(actual, True)-response(actual, False)))
    return {"offset_count": n, "nominal_phase_starts": len(starts),
            "unavoidable_island_intersections": missed,
            "max_optical_response_difference": round(difference, 12),
            "adversarial_timing_schedule_exists": missed == 0,
            "timing_errors_used_ms": sorted(used)}

def core_width(w, u):
    return max(0., nonnegative("pulse width", w)-2*nonnegative("uncertainty", u))

def coverage(starts, w, u, period=T):
    """Guaranteed covered phase circle, using intersection of allowed supports."""
    w = nonnegative("pulse width", w)
    u = nonnegative("uncertainty", u)
    period = nonnegative("period", period)
    if not period or not starts or any(not math.isfinite(t) for t in starts):
        raise ValueError("invalid phase circle")
    core = core_width(w, u)
    if core == 0:
        return {"core_width_ms": 0., "covered_fraction": 0.,
                "maximum_uncovered_gap_ms": period, "guaranteed_full_phase_coverage": False}
    if core >= period:
        return {"core_width_ms": core, "covered_fraction": 1.,
                "maximum_uncovered_gap_ms": 0., "guaranteed_full_phase_coverage": True}
    intervals = []
    for m in starts:
        a = (m+u) % period
        b = a+core
        if b <= period:
            intervals.append((a,b))
        else:
            intervals.extend(((a,period),(0.,b-period)))
    intervals.sort()
    cursor = 0.
    gaps = []
    for a,b in intervals:
        if a > cursor+1e-12:
            gaps.append(a-cursor)
        cursor = max(cursor,b)
    if cursor < period-1e-12:
        gaps.append(period-cursor)
    return {"core_width_ms": core, "covered_fraction": max(0.,1-sum(gaps)/period),
            "maximum_uncovered_gap_ms": max(gaps,default=0.),
            "guaranteed_full_phase_coverage": not gaps}

def even_starts(n):
    if type(n) is not int or n < 1:
        raise ValueError("invalid count")
    return [i*T/n for i in range(n)]

def threshold_ceiling(amplitude=AMPLITUDE, width=ISLAND_WIDTH, w=W, noise=NOISE):
    amplitude = nonnegative("amplitude", amplitude)
    width = nonnegative("island width", width)
    w = nonnegative("pulse width", w)
    noise = nonnegative("noise", noise)
    if w == 0:
        raise ValueError("zero pulse")
    upper = amplitude*min(width,w)/w
    return {"max_noise_free_contrast": upper,
            "max_contrast_with_positive_noise": upper+noise,
            "threshold_can_be_crossed": upper+noise > THRESHOLD,
            "minimum_width_for_worst_case_detection_ms":
                (THRESHOLD+noise)*w/amplitude if amplitude else None}

def experiment():
    improved_u = .001
    c = core_width(W, improved_u)
    n = math.ceil(T/c)
    yes = coverage(even_starts(n),W,improved_u)
    no = coverage(even_starts(n-1),W,improved_u)
    return {"experiment": "E002-480", "evidence_tier": "SYNTHETIC_INSTRUMENT_COUNTEREXAMPLE_ONLY",
            "frame_period_ms": T, "pulse_width_ms": W,
            "original_clock_uncertainty_ms": U, "island_width_ms": ISLAND_WIDTH,
            "island_amplitude": AMPLITUDE,
            "nominal_dither_grids": [adversarial_grid(k) for k in (1,2,4,8)],
            "original_robust_core_width_ms": core_width(W,U),
            "improved_clock_uncertainty_ms": improved_u,
            "improved_robust_core_width_ms": c,
            "minimum_even_phase_count_per_period": n,
            "minimum_even_phase_count_covers": yes["guaranteed_full_phase_coverage"],
            "one_fewer_even_phases_covers": no["guaranteed_full_phase_coverage"],
            "one_fewer_maximum_uncovered_gap_ms": no["maximum_uncovered_gap_ms"],
            "threshold_stress": threshold_ceiling(),
            "physical_shutter_acquisitions": 0, "new_anatomical_human_sequences": 0,
            "e002_371_physical_validation": "NOT_ESTABLISHED",
            "physical_release_authorized": False, "product_claim": ABSTAIN}

if __name__ == "__main__":
    print(json.dumps(experiment(),indent=2,sort_keys=True))
