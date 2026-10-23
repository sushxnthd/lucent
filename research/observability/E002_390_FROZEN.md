# E002-390 frozen protocol — circular velocity calibration from aliased RGB

Frozen before running the experiment. Date: 2026-10-23. Evidence tier: software-instrument/synthetic; not human data or physical camera.

## Question
Can an ordinary RGB camera's own exposure-averaged aperture differences be used to upper-bound eyelid velocity for E002-371? A sharp conditional theorem requires a true independent velocity bound, not a velocity estimate derived from the same temporally aliased observations.

## Acquisition and preregistered cohorts
- Piecewise-linear aperture excursions, continuous in time, range [0,1], with a known per-trace maximum slope. Generate disjoint deterministic calibration and holdout cohorts from fixed seeds 39001 and 39002.
- Synthetic ordinary camera: 30 Hz, 10-ms rectangular exposures, exact integral aperture means. Synthetic high-rate reference: 1000 Hz with 0.25-ms exposures.
- Independently determine the admissible speed envelope from the calibration generator/reference; holdout speeds must be at or below the frozen envelope. A separate out-of-envelope shift must abstain.
- Define crossing as a continuous-time minimum aperture strictly below 0.2. Report crossing duration, including very short crossings; do not call these human blinks.
- Self-calibrated speed: maximum difference of consecutive ordinary-camera exposure means divided by frame interval. Do not label it a valid physical upper bound.
- Compute a conservative E002-371 exposure-integral lower bound on aperture over the recording. Evaluate at all observation times and account for grid interpolation and optical measurement error.
- Controls: no-event traces, independently bounded velocities, reference exposure averaging, brightness, gaze, blur, glare, missingness, timestamp perturbation and out-of-envelope motion. Distinguish model soundness from nuisance robustness.
- A product certificate is permitted only when velocity, timing and optical calibration are independently bounded and all relevant nuisance gates pass; otherwise abstain.

## Frozen falsifiable predictions
P1: There exist exact exposure-integral collisions/near-collisions in which ordinary-camera self-calibration underestimates the true velocity and falsely certifies no threshold crossing.
P2: On the clean held-out synthetic crossing cohort, plug-in self-calibration yields at least one false certificate, while a mathematically valid independent speed envelope yields zero false certificates.
P3: A 1000-Hz reference with 0.25-ms exposure detects at least 95% of crossings whose physical below-threshold duration exceeds 2 ms; unresolved shorter events must not be relabeled negatives.
P4: At least one nuisance-shift condition produces a false plug-in certificate or makes the physical measurement assumptions unavailable; fail-closed policy abstains rather than transferring the clean certificate.
P5: An independent checker recomputes continuous-time minima, exposure integrals, speed envelopes and certificate soundness without reusing the production certificate function.

## Precommitted interpretation
A counterexample falsifies self-calibration as a deterministic velocity upper bound, not the E002-371 theorem. An absence of observed false certificates does not prove plug-in safety. Synthetic success does not imply physiological validity. Do not claim human validation, clinical fatigue measurement or novelty. Next gate is synchronized human high-rate/ordinary-RGB acquisition with independent timing and kinematic calibration.
