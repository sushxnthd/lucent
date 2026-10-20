# E002-321 — Temporal sampling calibration

This research note studies whether a camera exposure-average can rule out an unobserved threshold crossing between exposures.

For a bounded nonnegative L-Lipschitz signal with calibrated per-exposure integral error eta, exposure E and period P, two adjacent zero measurements imply the sharp upper bound

M = min(1, b + L(P-E)/2),

where b=min(1,sqrt(2 L E eta)) if eta<=L E/2, otherwise b=min(1,eta+L E/2).

The bound is attained by a piecewise-linear witness. A threshold strictly above M cannot be reached; one at or below M can be reached without contradicting the observed averages.

A synthetic 24fps/8ms configuration with L=10/s and eta=0.005 has M=0.19661760458079525. This is a mathematical test, not an empirical camera result.

Run model.py and independent_checker.py with Python, NumPy and SciPy. The independent checker tests six discretized LP cases and 500 randomized feasible witnesses.

Limitations: this does not establish that commodity RGB data can be calibrated to the assumed signal or error bound. The speed limit must be independently justified. Classical optimal recovery precedes this specialization.