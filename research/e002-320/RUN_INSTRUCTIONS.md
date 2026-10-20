# Reproduction checklist

Python 3.10+ with scipy available.

1. python model.py
2. python independent_checker.py
3. python independent_lp_checker.py
4. python holdout_checker.py
5. python controls.py

All tests are synthetic; no human data or proprietary compute. Frozen prediction JSON must not be edited before running holdout_checker. The analytic module and independent exact-rational phase checker do not import one another. Independent LP tests are separately implemented.

Known limitations and failure gates are in FAILED_GATES.md. GitHub Actions remote CI has not been observed running; do not infer CI success from local tests.