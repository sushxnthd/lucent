"""E002-661: robust shutter-kernel certificate under phase-gain ambiguity.

Dependency-free exact arithmetic. Run: python research/observability/e002_661_kernel_set.py
Synthetic instrument test only; no human or physical measurements.
"""
from fractions import Fraction as F
from itertools import product

def compatible_kernels(observed, gain_options):
    out = set()
    for gains in product(gain_options, repeat=len(observed)):
        unnormalized = [y / g for y, g in zip(observed, gains)]
        total = sum(unnormalized)
        k = tuple(x / total for x in unnormalized)
        out.add(k)
    return sorted(out)

def first_moment(kernel, phase_times, center=F(0)):
    return sum(w * abs(t - center) for w, t in zip(kernel, phase_times))

def lower_certificate(observed_aperture, speed, kernels, phase_times):
    # Lipschitz aperture; response-weighted temporal samples; exact worst-case bound.
    return min(observed_aperture - speed * first_moment(k, phase_times)
               for k in kernels)

def run():
    # Four shutter phases centered at 0, with a linear unsaturated phase scan.
    times = (F(-3, 2), F(-1, 2), F(1, 2), F(3, 2))
    observed_scan = (F(1),) * 4
    gains = (F(1, 2), F(1), F(2))
    kernels = compatible_kernels(observed_scan, gains)
    rectangular = (F(1, 4),) * 4
    assert rectangular in kernels
    # At a measured aperture 0.60, rectangular calibration certifies >0.30,
    # while gain-ambiguous calibration cannot.
    aperture, speed, threshold = F(3, 5), F(1, 4), F(3, 10)
    naive = aperture - speed * first_moment(rectangular, times)
    robust = lower_certificate(aperture, speed, kernels, times)
    assert naive > threshold and robust <= threshold
    # Ground truth construction for any compatible kernel: a(t)=A-V|t|,
    # shifted to reproduce measured exposure exactly.
    worst = max(kernels, key=lambda k: first_moment(k, times))
    center_aperture = aperture - speed * first_moment(worst, times)
    assert center_aperture == robust
    reconstructed = sum(w * (center_aperture + speed * abs(t))
                        for w, t in zip(worst, times))
    assert reconstructed == aperture
    # If independently known constant gain collapses the ambiguity, the
    # robust certificate coincides with the rectangular correction.
    identified = compatible_kernels(observed_scan, (F(1),))
    assert identified == [rectangular]
    assert lower_certificate(aperture, speed, identified, times) == naive
    print("PASS E002-661")
    print("compatible kernels:", len(kernels))
    print("naive lower:", naive, "robust lower:", robust, "threshold:", threshold)
    print("worst kernel:", worst)
    print("synthetic only; no physical/human validation")

if __name__ == "__main__":
    run()
