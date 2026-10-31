#!/usr/bin/env python3
"""E002-539 independent discretized adversarial optimization (SciPy HiGHS).

Does not import the exact-rational boundary implementation. This is a numerical
synthetic instrument surrogate, NOT a human or hardware measurement.
"""
from __future__ import annotations
import json
import numpy as np
from scipy.optimize import linprog


def adversarial_minimum(n, speed, accel, gap=1/30, endpoint=0.9):
    if n < 4 or n % 2 or speed < 0 or accel < 0 or gap <= 0:
        raise ValueError("INVALID_DISCRETE_PROBLEM")
    dt = gap / n
    rows, limits = [], []
    for i in range(n):
        row = np.zeros(n + 1)
        row[i] = -1.
        row[i+1] = 1.
        rows.extend((row, -row))
        limits.extend((speed*dt, speed*dt))
    for i in range(1, n):
        row = np.zeros(n + 1)
        row[i-1] = 1.
        row[i] = -2.
        row[i+1] = 1.
        rows.extend((row, -row))
        limits.extend((accel*dt*dt, accel*dt*dt))
    eq = np.zeros((2, n + 1))
    eq[0, 0] = 1.
    eq[1, n] = 1.
    objective = np.zeros(n + 1)
    objective[n//2] = 1.
    result = linprog(objective, A_ub=np.asarray(rows),
                     b_ub=np.asarray(limits), A_eq=eq,
                     b_eq=[endpoint, endpoint], bounds=(0., 1.),
                     method="highs")
    if not result.success:
        raise RuntimeError("LP_FAILED: " + result.message)
    path = result.x
    slopes = np.diff(path)/dt
    accelerations = np.diff(slopes)/dt
    if (max(abs(slopes)) > speed+1e-7 or
            max(abs(accelerations)) > accel+1e-5 or
            min(path) < -1e-8 or max(path) > 1+1e-8):
        raise AssertionError("DISCRETE_CONSTRAINT_VIOLATION")
    return float(result.fun)


def run_frozen():
    expected = {45: 51/160, 60: 1/5}
    output = {}
    for v, truth in expected.items():
        output[str(v)] = {}
        for n in (120, 240):
            observed = adversarial_minimum(n, v, 6000)
            if abs(observed-truth) > 0.025:
                raise AssertionError(f"FROZEN_LP_DISAGREEMENT V={v} N={n}: {observed}")
            output[str(v)][str(n)] = {"minimum": observed,
                                       "analytic_prediction": truth,
                                       "absolute_error": abs(observed-truth)}
    return {"experiment": "E002-539",
            "evidence_tier": "DISCRETE_SYNTHETIC_OPTIMIZATION_NOT_HUMAN",
            "frozen_tolerance": 0.025,
            "cases": output,
            "physical_validated": False,
            "product": "ABSTAIN_UNCALIBRATED",
            "release": "BLOCKED"}


if __name__ == "__main__":
    print(json.dumps(run_frozen(), indent=2, sort_keys=True))
