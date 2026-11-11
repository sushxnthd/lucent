# E002-458 — Hosted human two-phase transfer and shutter-fragility result

**Date:** 2026-10-26. **Evidence tier:** checksum-verified published human *per-blink peak estimates* plus an independently executed arithmetic nuisance challenge. **Not** physical anatomical trajectory validation, a population hard velocity bound, or a new mathematical theorem.

## New empirical result (E002-457 frozen protocol, now executed)

The previously queued [E002-457 hosted run 40271077293](https://github.com/sushxnthd/lucent/actions/runs/40271077293) **completed successfully**. Its actual Python tests, independent 140,000-trial JavaScript witness suite, SHA256 verification and external human CSV stage all succeeded. The full machine-readable nonidentifying result is [E002_457_HUMAN_AGGREGATE.json](E002_457_HUMAN_AGGREGATE.json), transcribed from the successful hosted job. Source: Culemann et al., *Behavior Research Methods* (2026), [DOI 10.3758/s13428-026-02984-4](https://doi.org/10.3758/s13428-026-02984-4), [author-supplied OSF data](https://osf.io/m34qd). CSV SHA256: `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43`.

Original prespecified split: **12 calibration participants (1,657 blinks)** and **five held-out participants (649 blinks)**. All 2,306 opening-velocity values have a positive sign in this source. Calibration maximum estimated closing peak: **567.103928 mm/s**. Calibration maximum estimated opening peak magnitude: **274.616337 mm/s**. Holdout exceedances: **0 closing, 0 opening, 0 either**, across five held-out participants. This is descriptive same-study transfer, *not* independent certification of physiological upper limits. Per E002-454, zero exceedances in five people is weak evidence for a universal maximum; do not count 649 blinks as independent subjects.

For *hypothetical instantaneous, millimeter-calibrated* endpoint apertures 1 mm above the closure threshold and treating these sample maxima as **assumed hard caps**, the sharp directional closure threshold is

`T_dir = 1/C + 1/O = 5.404789 ms`,

versus `T_sym = 2/max(C,O) = 3.526690 ms`. The conditional critical gap is **53.2539% longer** with separate closing/opening limits. At nominal 240 fps (4.166667 ms), the symmetric rule does **not** exclude a hidden closure while the directional rule **would exclude it under the assumptions**. Both rules fail to exclude at 30/60/120 fps; both exclude at 480/1000 fps under the same idealized assumptions.

## Exploratory, independently executable nuisance challenge

[E002-458 JS replay](e002_458_human_shutter_sensitivity.js) recomputes the 240-fps decision from the committed human aggregate without importing the E002-457 Python evaluator. This is a *post-hoc sensitivity check*, not a preregistered new human experiment.

Under an assumed **uniform, centered shutter** of duration e milliseconds, each observed 1-mm endpoint clearance is pessimistically reduced by `(C+O)*e/8000` mm. With independent clock uncertainty `±q` ms at each endpoint, the worst-case center gap is `1000/240 + 2q` ms. The resulting conservative exclusion condition is

`1000/240 + 2q < (1 - (C+O)*e/8000) * 1000 * (1/C + 1/O)`,

provided the reduced clearance is positive and every other calibration/nuisance gate passes.

| Assumed shutter e | Clock error q per endpoint | Conditional 240-fps result |
| --- | --- | --- |
| 0 ms | 0 ms | EXCLUDED_CONDITIONALLY |
| 1 ms | 0 ms | EXCLUDED_CONDITIONALLY |
| 2 ms | 0 ms | EXCLUDED_CONDITIONALLY, only 0.10079-ms gap margin |
| 2 ms | 0.1 ms | NOT_EXCLUDED |
| 2.2 ms | 0 ms | NOT_EXCLUDED |

At zero clock error, the shutter break-even is **2.177244 ms**; even that idealized conditional advantage vanishes at longer uniform exposures. At 2-ms exposure, per-endpoint clock error of about **0.0504 ms** is sufficient to erase the exclusion. This is a consequential nuisance boundary, **not** evidence that any actual camera has these parameters or that the sample velocity maxima are safe hard limits. Rolling shutter, variable exposure, frame drops, blur, gaze, geometry, glasses and brightness remain independent abstention conditions.

## Falsification and product decision

This successful real-human *velocity-table* analysis strengthens a **conditional** observability model, but cannot establish a physical guarantee. Its strongest product implication is that **directional speed modeling can alter an idealized 240-fps decision yet the gain is extremely sensitive to shutter and clock calibration**. Thus a product must not label such decisions physically certified without independently bounded directional speeds, anatomical millimeter calibration, authenticated shutter/clock behavior, and unseen participant trajectory labels. **E002-371 physical status: NOT_ESTABLISHED.** All physical hidden-closure, blink-duration, PERCLOS, fatigue and medical claims: `ABSTAIN_UNCALIBRATED`.

**Next decisive experiment:** obtain independently annotated high-rate anatomical eyelid-margin trajectories and authenticated exposure timing (restricted 400-fps FaceBase data if permission is granted, or a prospective calibrated capture), freeze C/O and camera-nuisance limits on disjoint calibration participants, then evaluate sealed predictions on unseen participants. Preserve negative results; do not rerun the same dataset or polish the theorem in place of new evidence. S21/S22 remain sealed; no private video or human rows were committed. PR #26 stays draft/unmerged; Hush PR #45 unchanged.
