# E002-280: shutter-aware blink observability

**SCIENCE:** Exact conditional shutter/contrast detection boundary. Synthetic only, no human validation.

**PRODUCT:** Conditional blink-event detection/rejection; no pupil physiology, fatigue, or APST-5 claim.

## Active kernel

Signal/reference: RGB rank flip between tracked eye patch and stable comparison patch / synchronized high-speed annotated eyelid aperture. Literature: rank/census invariance is established (Zabih and Woodfill, ECCV 1994); blink sampling limits are known. Metric: worst-case rank contrast and all-phase event duration. Nuisance: local illumination, specular reflection, gaze, clipping, rolling shutter.

Model: event duration d, shutter interval [a,b], exposure fraction lambda; observed pixels g(R0+Delta*lambda)+e1 and g(Rref)+e2. Common increasing g has slope >=m; each error <=eta. Define q=(Rref-R0+2eta/m)/Delta. An event is guaranteed detectable in some frame at every phase exactly when d>P-T+2qT, for periodic period P and exposure T, provided 0<q<1 and a strict rank-flip threshold. The bound is sharp; an event centered in the shutter gap is a counterexample below threshold.

Falsification: prospectively predicted boundary fails on unseen synchronized human/device regime, or nuisance-only negative control produces a rank flip. Human test: >=8 untouched participants, >=2 camera models, glasses/lighting/gaze strata, calibrated error/slope, reference-blind admission and nuisance baselines. Publication: independent checker, prior-art audit, prospective human boundary and explicit limits. Not achieved.

Product rule: no certified short-blink completeness without shutter timing, non-saturation, global-transfer checks and contrast calibration. Otherwise abstain.

Run: python3 experiment.py && python3 checker.py. Results and lossless phase bitsets are in results.json and raw_phase_runs.json. Parent: E002-279 commit a137c91053845dc3a6d6901335a654542e1b83e0.
