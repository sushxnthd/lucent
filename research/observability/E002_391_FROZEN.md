# E002-391 frozen prospective instrument protocol — phase-locked aliasing versus independently randomized acquisition

Frozen 2026-10-23, before running E002-391 code. This is an **instrument/simulation study**, not human evidence, and not a new general theorem. Primary scientific kernel remains E002-371 shutter-gap/eyelid-velocity observability.

## Motivation and precise hypothesis
E002-390 showed that same-camera self-estimated eyelid velocity can miss hidden closures. A separate acquisition-design question is whether repeating a controlled event while varying **sensor sampling phase** can expose otherwise phase-locked aliases. This tests calibration-instrument design, **not** a single-blink certification method. Randomizing exposure phase only helps when the physical event is independent of the randomized phase and sufficiently reproducible. An adaptive subject/event can invalidate the result.

## Fixed instrument and analysis
- Physical aperture: continuous triangular event a(t)=max(0, min(1, 40*abs(t-t0))) over an otherwise open aperture of 1. Its trough is 0, max slope 40/s, threshold theta=0.2, and full excursion width 50 ms. Repeat every 400 ms (12 frames at 30 Hz) for N=12 cycles. No physiological generality is claimed.
- Ordinary camera: F=1/30 s, 5-ms rectangular exposure, exact integral of the aperture over each exposure, nominal aperture response. A closure is **detected** only if at least one exposure mean is strictly below theta. A negative camera detection is not a no-closure certificate.
- Three policies: (A) locked phase common to all 12 cycles; (B) independently randomized uniform phase each cycle; (C) bounded +/-1-ms phase jitter around a single random phase. No adaptive event timing. For the same 12-cycle cohort use 12,000 independent trial sets, seeded 39111. Independently compute the single-cycle capture fraction p from a deterministic 12,000-point phase grid, then compare empirical any-event detection to p for A and 1-(1-p)^12 for B. The jitter outcome is descriptive, not a preregistered success.
- Independent checker must use numerical quadrature rather than the closed-form integral. Validate at least 100 random phases. Reference: 1000-fps, 0.25-ms exposures over each event; report adequacy only within the simulated model.
- Nuisance controls: bounded additive optical error +/-0.03; strict positive detection requires observed mean + 0.03 < theta. Also simulate an unbounded negative optical offset of -0.30 as an adversarial glare/transfer counterexample and force abstention when error bound is not independently justified. Timing uncertainty +/-0.5ms and shutter duration +/-0.5ms must be treated as unresolved unless measured; no hard certification. Gaze, glasses, blur, geometry and missingness are external optical gates, not assumed solved by timing randomization.

## Frozen predictions and falsification
P1: Single-cycle detection fraction satisfies 0.05 < p < 0.5.
P2: Locked-phase 12-cycle any-detection fraction is approximately p (within 0.02).
P3: Independent uniform phase across 12 cycles gives any-detection >0.9 and agrees with 1-(1-p)^12 within 0.02.
P4: With correctly bounded optical error, a conservative positive-detection rule produces zero false detections on always-open controls (no probability guarantee beyond the synthetic bound).
P5: With unbounded optical bias and no optical gate, false positive events are possible; fail-closed policy abstains.

Negative outcomes and all code/data must be preserved. Do not tune frozen thresholds, N, or seeds to obtain a pass. A product may recommend controlled phase-sweep acquisition for instrument qualification, but cannot infer a single-event no-hidden-closure guarantee from multi-event detection. Next decisive milestone remains paired human ordinary RGB/high-speed recordings with independently measured velocity, shutter timing and optical response, plus untouched participant/device holdouts.
