# E002-429 — physical-aperture geometry alias falsifies fixed-view certification

**Date:** 2026-10-25. **Evidence tier:** original reproducible **synthetic counterexample** in a restricted orthographic forward model, supported by independent published human *aggregate* evidence of gaze-dependent eyelid morphology. **No human frames, real-camera calibration, independent human validation or new general theorem.**

The preregistered predictions are in [E002_429_FROZEN.md](E002_429_FROZEN.md). This experiment attacks the *measurement operator* feeding E002-371, rather than refining its already-sharp physical-aperture bound. It is not a counterexample to the theorem: it deliberately violates the premise that the input exposure averages are authenticated physical apertures.

## New falsification

Use `y(t)=H(t) cos(phi(t))`, where H is physical eyelid aperture in mm and phi is an **effective orthographic projection angle**. This cosine law is an intentionally restricted geometric model, **not a validated physiological model of gaze-dependent lid shape**. The units of y are projected-mm-like, not calibrated physical millimeters.

Two worlds are observationally identical **at every instant**, and therefore for any uniform shutter integration, virtual sampling rate, or even arbitrarily dense samples of this scalar observable:

| Quantity | World A: always open | World B: hidden threshold crossing |
|---|---:|---:|
| Physical H at the two frame centers (mm) | 2.040 | 2.010 |
| Physical minimum H between centers (mm) | 2.040 | **1.990** |
| Closure threshold (mm) | 2.000 | 2.000 |
| Effective phi at frame centers | 20.000° | 17.500° |
| Effective phi at interval midpoint | 20.000° | 15.570° |
| Continuous projected observable y | 1.9169729464 | **1.9169729464** |
| Physical aperture speed (mm/s) | 0 | **1.200** |

For World B, H decreases linearly from 2.01 to 1.99 mm over 1/60 s, then returns to 2.01 over 1/60 s; its effective angle is defined as `acos(2.04*cos(20°)/H(t))`. Thus `y_B(t)=y_A(t)` exactly in the mathematical model, although one physical trajectory crosses theta=2.00 mm and the other does not. No claim is made that this coupled angle trajectory has been observed in a human. Both satisfy the same **hypothetical** hard physical speed bound 1.2 mm/s.

**Decisive product falsification:** An analyst who incorrectly treats phi=20° as constant converts the two 4-ms shutter averages into m=2.04 mm. With d=1/30 s and V=1.2 mm/s, the sharp restricted equal-average formula yields `m-Vd/2=2.020 mm > 2.000 mm`, incorrectly authorizing a no-hidden-closure decision in World B. This does **not** disprove E002-421; the physical-aperture observation premise is false.

If an independent calibration instead authenticates an effective-angle interval [15°,20°] for the whole interval, the instantaneous lower envelope is `H >= y/cos(15°) = 1.98459643 mm`, which is below the threshold and forces abstention. This is only an **instantaneous** envelope given y(t); applying it to ordinary sampled video additionally requires a validated temporal observation model. A tighter verified interval [18°,20°] would exclude this specific World B geometry but is not claimed to be available physically.

## Numerical execution and independent verification

The standard-library-only [simulator](e002_429_geometry_alias.py) and [independent test suite](test_e002_429_geometry_alias.py) were executed locally. **Five test groups passed.** They cover finite-difference physical-speed checking, 1,201 projected-time comparisons including outside the gap, independently evaluated midpoint shutter integration at 24/30/60/120/500 Hz and three exposures, false fixed-geometry decision, interval-guard reversal, and malformed-input rejection. Maximum projected discrepancy on the declared dense grid was **0.0** in double precision. Both 4-ms shutter averages were **1.9169729464032532**. The false fixed-geometry lower bound was **2.02 mm**. These are synthetic arithmetic results, not a human error rate or evidence of physical angular dynamics.

Reproduce from repository root:

```bash
python research/observability/e002_429_geometry_alias.py
cd research/observability && python -m unittest -v test_e002_429_geometry_alias.py
```

## Primary-literature priority audit

Read, Collins, Carney and Iskander, *Optometry and Vision Science* **83** (2006), 715–722, DOI **10.1097/01.opx.0000236811.78177.97**, measured palpebral-fissure morphology in **76 human participants** at primary gaze and 20°/40° downward gaze. The reported average vertical aperture in one demographic group decreased from **9.7 ± 1.2 mm** in primary gaze to **6.4 ± 1.1 mm** at 40° downward gaze; dimensions and contour changed significantly. This establishes that gaze dependence is a **real anatomical nuisance**, but does **not** validate the synthetic cosine model or the particular 15.57°–20° effective-angle trajectory. [PubMed PMID 17041316](https://pubmed.ncbi.nlm.nih.gov/17041316/).

Classical perspective/projective ambiguity and measurement calibration long predate Lucent. E002-429 claims neither novelty of projective ambiguity nor a new physiological finding. Its contribution here is a *frozen, executable counterexample* that directly changes the authorization boundary for the E002-371 measurement pipeline.

## Concrete physical study to falsify the nuisance hypothesis

1. **Acquire and register:** At least two synchronized, independently calibrated camera views (one >=500 fps) or a validated 3D eyelid-margin reference; preserve raw timestamps and an external photodiode timing trace. Independently measure physical scale, camera pose and rolling-shutter row timing. Secure consent and deidentify; do not upload identifiable eye video to a public repository.
2. **Gaze and geometry intervention:** Pre-register primary/downward/side gaze targets, mild head-pose shifts, and camera distance; use independent target and head-pose tracking. Include controlled brightness, blur, glasses and occlusion conditions. Separate true lid-shape changes from projection; the synthetic cos(phi) should be replaced by a *measured*, uncertainty-bounded mapping.
3. **Blinded reference:** Two independent annotators trace central upper/lower anatomical lid margins on high-speed views without seeing Lucent's predictions. Preserve disagreements, missing landmarks and geometry-uncertain frames as unresolved. Use participant-disjoint training and holdout, and preseal predictions before reference review using E002-426.
4. **Prospective falsification:** Freeze each device/participant-stratum geometry interval, shutter/clock model, and independent physical velocity hypothesis. At 24/30/60/120 Hz predict conditional safe/unsafe/abstain intervals; test witnessed threshold crossings on unseen people and devices. Report *participant-level* failures, coverage, unresolved-reference worst-case error, and all nuisance strata.
5. **Release blocker:** Any physical certificate made with unverified fixed projection, unauthenticated aperture scale, unbounded geometry/gaze nuisance, or unverified physical velocity remains **rejected**. Do not silently replace physical mm with EAR, pixel distances, or normalized eye aspect ratios.

## Scientific status

**E002-371 remains physically unvalidated.** The strongest defensible product is a research/instrumentation pipeline with conditional theoretical bounds, explicit assumption diagnostics and `ABSTAIN_UNCALIBRATED`. No blink-duration, PERCLOS, fatigue or physical hidden-closure guarantee is authorized. This result cannot substitute for human aperture traces, independent shutter timing or externally reviewed calibration.
