# E002-462 — frozen reference-camera aliasing challenge (2026-10-26)

**Frozen before evaluator and data generation.** Evidence target: independently reproducible **synthetic instrument** challenge, not human acquisition. Existing E002-371/457/460 conditional speed laws are *inputs*, not newly discovered mathematics.

## Question and prospective prediction

Can an apparently open 400-fps *reference* recording be used as unquestioned anatomical ground truth for ordinary-camera hidden-closure validation? Test the failure mode in which the reference camera itself misses a true closure. Do not call high-speed frames an oracle without an independently certified bound.

- Physical aperture threshold c=2.0 mm, baseline open aperture b in {2.3, 2.1} mm.
- Hypothetical directional velocity limits C=567.103928 mm/s and O=274.616337 mm/s (published *sample* maxima, **not** physiological hard bounds).
- Reference frame rates: 400, 1000, 2000 fps. Centered shutter width 0.30 ms, instantaneous row/eye-plane aperture, perfect static scale, zero noise/clock error for primary counterexample. These ideal conditions favor the reference camera.
- Reference shutter output is the true linear aperture mean, integrated over its exposure support. Ground-truth aperture is the exact piecewise-linear trajectory, not the shutter mean.
- Positive adversarial trajectory: start from constant b, descend at speed C to c at tau, reopen at speed O to b, with flat baseline elsewhere. Negative control: a(t)=b for all t. A reference *false negative* occurs if every reference shutter mean is strictly above c although the positive trajectory reaches c; a stronger *indistinguishable* failure occurs when the entire positive closure excursion lies between shutter supports and all recorded frames equal the negative control exactly.
- Primary frozen examples: b=2.3, 400 fps, tau=1.0 ms, and b=2.1, 1000 fps, tau=0.4 ms. Predict indistinguishable negative/positive reference frames at 400 fps for b=2.3 with width 0.3 ms, and at 1000 fps for b=2.1 if the event is wholly in the dark gap. The latter prediction is deliberately falsifiable; if the event overlaps shutter support, report that honestly.
- Exact critical sample separation is (b-c)/C + (b-c)/O. For b=2.3 this is ~1.621 ms; for b=2.1 ~0.540 ms. Distinguish *sample-time* aliasing from shutter-mean thresholding and from an independently witnessed physical crossing.

## Execution and failure criteria

1. Implement analytic piecewise-affine integration (no image synthesis masquerading as human data) and evaluate exact primary/negative controls.
2. Sweep held-out event phase (fixed seed 462, 1000 draws per (fps,b) cell), plus shutter widths 0.30 and 0.80 ms where supports remain nonoverlapping; preserve counts and parameters, not selected successes.
3. Include independent JS arithmetic replay of the primary cases and Python adversarial tests for timing, phase, shutter support, units, and nuisance abstention.
4. Treat any indistinguishable positive/negative pair as **falsification of reference-frame completeness**, not falsification of E002-371's conditional theorem. Count no new human evidence.
5. If frozen 1000-fps primary is not indistinguishable, report the failure rather than retuning tau or thresholds after seeing results.
6. Product/study consequence: reference labels must be interval-censored or independently witnessed with continuous encoder/event timing. A reference label of OPEN from sparse frames is not a proof that no closure occurred.

## Nuisance / claim discipline

Unknown anatomy-to-mm scale, brightness/transfer, gaze, glasses, blur, missing frames, clock drift, sampling phase, rolling shutter, and exposure kernel must **abstain**. The synthetic idealized experiment intentionally holds these fixed to isolate temporal reference aliasing. Do not claim the hypothetical velocity maxima are physiological bounds, or that a physical camera, patient, or participant was measured. Do not modify S21/S22, release code, or Hush's separate branch/PR. Preserve draft PR #26 and all negative results.
