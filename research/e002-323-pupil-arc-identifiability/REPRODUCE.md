# Reproduce E002-323

Python 3.9+ standard library, no GPU/API/network. Run python independent_checker.py.

The checker independently computes circle centers from three points, evaluates 400 randomized feasible intervals and 501 witness points per interval, bisects both frozen transition angles, and checks geometry scaling, photometric error inflation, missing arc and temporal-smoothness controls. It does not import model.py. checker_results.json is derived output; FROZEN_PREDICTION.json predates checker evaluation.

All data are synthetic. Human evidence and RGB calibration remain open.