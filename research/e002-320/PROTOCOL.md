# E002-320 frozen synthetic verification

1. Analytic minimax bound derived independently of experiment.
2. Independent exact-rational breakpoint/envelope minimization over 600 random period/exposure/duration geometries; maximum discrepancy 0.
3. 400 null/event bounded-noise collision tests.
4. 90 independent linear programs for closure-burden bounds, including missing exposures; maximum discrepancy 5.551115123125783e-16.
5. 500 two-point moment witnesses and 300 random threshold-occupancy checks; no violations.
6. Frozen held-out SYNTHETIC instrument: P=1/24, E=1/80, a=1, η=7/100; predicted dcrit=49/1500 seconds, 31ms abstain and 35ms certify; both passed an independent phase search.
7. Negative controls: geometry-only (artifact 0.30 > η=0.05), brightness-only (artifact 0.25 uncalibrated), missingness-only (one dropped frame yields 56.667ms gap and invisible 40ms event), smoothness-only (C-infinity event fully inside shutter gap).
8. No human evaluation or calibration was performed. Future paired protocol in HUMAN_PROTOCOL.md. Dataset access/provenance limited to at most two substantive attempts per path.

Run the local reproducibility package with Python and SciPy; do not confuse synthetic tests with clinical validation.