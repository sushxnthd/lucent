"""E002-666: robust phase-dither detection under timing error and dependence.
Synthetic periodic triangle ONLY; no human blink claim. Python standard library.
"""
from fractions import Fraction as F

def guaranteed_closed_width(threshold, phase_error):
    assert F(0) <= threshold <= F(1)
    assert F(0) <= phase_error <= F(1,2)
    return max(F(0), threshold - 2 * phase_error)

def iid_detection(n, width):
    assert n >= 0 and 0 <= width <= 1
    return 1 - (1 - width) ** n

def conditional_coverage_lower(n, q):
    """Sharp if P(hit at k | prior misses) >= q for every k."""
    return 1 - (1 - q) ** n

def main():
    c = F(3,10)
    e = F(1,20)
    core = guaranteed_closed_width(c,e)
    assert core == F(1,5)
    assert iid_detection(10,core) == 1 - F(4,5)**10
    assert iid_detection(10,c) == 1 - F(7,10)**10
    assert guaranteed_closed_width(c,F(3,20)) == 0
    # Fully correlated uniform phase: 10 probes detect only with probability core.
    assert core < iid_detection(10,core)
    # Conditional lower bound is attained by independent Bernoulli hit events.
    assert conditional_coverage_lower(10,core) == iid_detection(10,core)
    # Marginal-only lower bound cannot improve with n: all probes identical.
    print("closure_fraction", c)
    print("phase_error", e)
    print("guaranteed_core_fraction", core)
    print("iid_10_detection_lower", float(iid_detection(10,core)))
    print("perfect_correlation_10_detection", float(core))
    print("uncertain_phase_error_0.15_core", guaranteed_closed_width(c,F(3,20)))
    print("PASS: exact rational synthetic assertions")

if __name__ == "__main__":
    main()
