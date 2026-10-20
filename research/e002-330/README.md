# Lucent E002-330: exposure-occupancy quotient (2026-10-20)
Uniform global-shutter RGB exposure can preserve the distribution of pupil radii but cannot recover their within-exposure temporal order, even from every noise-free pixel. This is a model-conditional impossibility, not a new mathematical invention or human evidence.

A perfect concentric disk with fixed center, illumination and known pupil/iris contrast permits recovering the radius occupancy survival function from the radial intensity profile. Under separately calibrated common visibility weights, the unweighted mean is sharply interval-identified. Full derivation in THEOREM.md.

Synthetic results: 3 exact full-RGB collisions (64 subframes each; at quarter exposure the hidden radius differs by 8, 6 and 4 pixels), 300 random permutation tests, 9,900 exact-rational extremizers, 5,000 random weighted-bound checks and 4 nuisance controls. Human test NOT RUN; publication novelty NOT ESTABLISHED; remote CI NOT VERIFIED.

Run: python instrument.py; python independent_checker.py; python controls.py (NumPy required). Full local archive also produced as lucent_e002_330_exposure_occupancy.zip.

Product: reject sub-exposure pupil phase and five-second fatigue claims. Calibrated occupancy/intervals only as research, with abstention; if pupil optical calibration fails, test eyelid occupancy.