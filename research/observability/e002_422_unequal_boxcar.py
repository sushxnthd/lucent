#!/usr/bin/env python3
"""E002-422: conditional unequal-boxcar full-horizon bound; NOT a human measurement."""
from __future__ import annotations
import argparse
import json
import math


def conditional_full_horizon(a: float, b: float, velocity: float,
                             center_dt: float, exposure: float,
                             closure_threshold: float) -> dict:
    """Sharp bound only in the explicitly qualified balanced-slope regime.

    a,b must be independently calibrated *physical-aperture* boxcar means.
    No supplied parameter is authenticated here. Product output always abstains.
    """
    vals = (a, b, velocity, center_dt, exposure, closure_threshold)
    if any(isinstance(z, bool) or not isinstance(z, (int, float))
           or not math.isfinite(z) for z in vals):
        raise ValueError("All six inputs must be finite numeric scalars")
    V, d, E, theta = velocity, center_dt, exposure, closure_threshold
    if not (V > 0 and 0 < E < d and 0 < theta < min(a, b) < 1
            and max(a, b) < 1):
        raise ValueError("Invalid exposure geometry or aperture/threshold range")
    balance_margin = V * (d - E) - abs(a - b)
    L = (a + b - V * d) / 2
    if (balance_margin <= 1e-12 or L <= 1e-12
            or max(a, b) + V * E / 2 >= 1 - 1e-12):
        return {"experiment": "E002-422", "research_decision": "UNRESOLVED_MODEL",
                "sharp_lower_bound": None, "product_decision": "ABSTAIN_UNCALIBRATED",
                "physical_calibration_authenticated": False}
    tstar = d / 2 + (a - b) / (2 * V)
    if not E / 2 < tstar < d - E / 2:
        raise AssertionError("Balanced regime did not place valley in gap")
    margin = L - theta
    research = ("CONDITIONAL_NO_CLOSURE" if margin > 1e-12
                else "AMBIGUOUS_OR_NUMERICALLY_BORDERLINE")
    return {"experiment": "E002-422", "research_decision": research,
            "sharp_lower_bound": L, "valley_time": tstar,
            "dimensionless_ratio": V * d / (a + b - 2 * theta),
            "target_interval": [-E / 2, d + E / 2],
            "product_decision": "ABSTAIN_UNCALIBRATED",
            "physical_calibration_authenticated": False}


def witness(t: float, a: float, b: float, V: float, d: float) -> float:
    """The admissible V-valley witness for a balanced, interior configuration."""
    L = (a + b - V * d) / 2
    tstar = d / 2 + (a - b) / (2 * V)
    return L + V * abs(t - tstar)


def open_world(t: float, a: float, b: float, d: float, E: float) -> float:
    """Distinct always-open path: constant in shutters, linear in their gap."""
    left, right = E / 2, d - E / 2
    if t <= left:
        return a
    if t >= right:
        return b
    return a + (b - a) * (t - left) / (right - left)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--a", type=float, default=.4)
    p.add_argument("--b", type=float, default=.3)
    p.add_argument("--velocity", type=float, default=50.)
    p.add_argument("--dt", type=float, default=.006)
    p.add_argument("--exposure", type=float, default=.002)
    p.add_argument("--threshold", type=float, default=.2)
    args = p.parse_args()
    print(json.dumps(conditional_full_horizon(
        args.a, args.b, args.velocity, args.dt, args.exposure, args.threshold),
        indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
