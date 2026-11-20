# E002-586 | Frozen optical phase-scan shutter-support falsification

**Freeze:** 2026-11-01 UTC, before implementation or inspecting any new camera measurements. Primary kernel E002-371; existing research branch and draft PR #26. This is a **synthetic instrument-validation substitute**, not a physical measurement or new calibration-method priority claim.

## Question and preregistered model

Does a camera's nominal frame period suffice to identify the actual unobserved shutter gap used by E002-371? **No** without imaging-path exposure/row timing. Test a calibrated optical step edge swept across exposure phase. In the deliberately restricted *linear, global/affine-rolling, rectangular integration* model, a row at sensor index r integrates on [s0 + r*d, s0 + r*d + E], and a bright-to-dark step at independently timed phase p produces normalized response y = clip((s0+r*d+E-p)/E,0,1).

Each observation has measured normalized intensity interval [y-eps,y+eps] and independently bounded optical step/clock phase error ±delta. Candidate (s0,E,d) grid points survive only when the predicted interval over phase uncertainty intersects the observation interval. The instrument reports the **union of all feasible exposure supports** for each observed row, not a fitted midpoint or point estimate. A gap may only be reported relative to this outer support. Finite grid coverage is NOT a continuous-parameter certificate.

## Fixed tests, before running implementation

1. Exact synthetic ground truth (s0=2 ms, E=4 ms, d=0.1 ms/row) must be feasible using row 0 and row 20 and phase scans; both the ground-truth shutter supports and a zero-drift control must be exercised.
2. A deliberately weak/saturated phase scan must yield a wider support or abstain, never false confidence.
3. Increased phase/brightness uncertainty must never shrink the feasible candidate set or outer support.
4. Nonlinear response, clipped pixels, uncalibrated LED rise time, missing phase samples, insufficient row geometry, and unknown rolling-shutter mode must force explicit abstention (not calibration).
5. A known non-affine row-time perturbation must be rejected by an overdetermined third-row control under zero noise.
6. Deliberately inconsistent observations must fail closed rather than emit a camera calibration.
7. Under finite grid discretization, no numerical output may be called an authenticated shutter/clock or eyelid-velocity certificate.

## Physical handoff and kill criteria

Independently log the LED optical edge with a photodiode/oscilloscope, not merely its command timestamp. Acquire a randomized phase sweep of optical step responses at multiple rows in the *same imaging path and exposure settings* as the eyelid recordings; calibrate dark/bright reference, linearity, gain, LED rise/fall, rolling direction, phase uncertainty, and row mapping. Repeat after autofocus/exposure/HDR/thermal changes and under brightness, motion blur, gaze/occlusion, glasses, dropped frames and timestamp drift. A holdout phase sweep must land within preregistered support intervals; any failure kills the current camera timing certificate. Preserve raw data privately with hashes; no human images in GitHub.

The method is **not novel as camera timing metrology**: compare Huai et al., *Optics Letters* 48, 847–850 (2023), DOI 10.1364/OL.474375, and Kurosawa et al., *Japanese Journal of Forensic Science and Technology* 29, 135–153 (2024), DOI 10.3408/jafst.875. Lucent's scientific question is whether calibrated supports and independently bounded human eyelid velocity make prospective hidden-closure exclusions valid.

**Product:** no upgrade from ABSTAIN_UNCALIBRATED; release BLOCKED. No independent human anatomical rater pairs, physical shutter captures, certified continuous-time velocity ceilings or held-out physical predictions are claimed.
