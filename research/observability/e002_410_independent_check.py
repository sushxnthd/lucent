#!/usr/bin/env python3
"""Independent E002-410 exchangeable-rank oracle; does not import primary code."""
import itertools
import json
import numpy as np

N = 20
TRIALS = 40000
rng = np.random.default_rng(910410)
values = rng.random((TRIALS, N + 1))
future_wins = int(np.count_nonzero(values[:, -1] > np.max(values[:, :-1], axis=1)))
rate = future_wins / TRIALS
target = 1 / (N + 1)

# Exhaustive finite rank enumeration with n=3 calibration, m=2 future.
wins = 0
total = 0
for perm in itertools.permutations(range(5)):
    total += 1
    if max(perm[3:]) > max(perm[:3]):
        wins += 1
exact_small = wins / total
report = {
    "experiment": "E002-410",
    "independent_oracle": True,
    "rank_simulation_trials": TRIALS,
    "rank_simulation_exceedances": future_wins,
    "rank_simulation_rate": rate,
    "rank_theory": target,
    "small_enumeration": {"n": 3, "m": 2, "permutations": total,
                          "future_exceedance_count": wins, "rate": exact_small},
    "pass": abs(rate - target) <= 0.006 and total == 120 and abs(exact_small - 0.4) < 1e-12,
}
print(json.dumps(report, indent=2, sort_keys=True))
if not report["pass"]:
    raise SystemExit(1)
