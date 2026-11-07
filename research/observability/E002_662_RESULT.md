# E002-662 | Velocity-tail calibration is not a deterministic ceiling (2026-11-05 UTC)

## Falsification question
Can the largest observed eyelid velocity in a finite calibration set justify the *deterministic* E002-371 shutter-gap absence-of-closure certificate? **No.** The code constructs an unobserved high-velocity triangular closure with open endpoints. A velocity bound learned from slower calibration samples incorrectly certifies an open eye; a genuine externally validated upper bound abstains.

## Exact synthetic result
At 30 Hz, endpoints are aperture 1 and the midpoint reaches 0, with true Lipschitz constant 60 normalized-aperture units/s. Substituting an unverified calibration ceiling 12 yields lower bound 0.8, incorrectly above closure threshold 0.3. The correct bound using 60 is 0. This is an adversarial *possibility* result, not a claim that human eyelids attain this speed.

If a high-velocity subpopulation/transition occurs with iid probability 1%, 100 independent calibration transitions miss it with probability (0.99)^100 > 1/3. Even 299 iid transitions only give >=95% probability of observing at least one such event, *conditional on the 1% tail assumption*. Neither sample size nor the observed maximum establishes a physical speed ceiling. Correlated within-subject transitions further invalidate iid transition counts.

## Frozen human validation protocol
1. Acquire source-authenticated >=200 Hz human eye videos with actual timestamps, acquisition metadata, exposure/rolling-shutter calibration and permission to process. Split **by participant** before calibration; never infer independence from adjacent frames.
2. Annotate aperture and closure threshold with two blinded raters; report disagreements and occlusions. Independently bound aperture scaling and timebase errors. Derive a conservative velocity ceiling only from externally justified biomechanics/instrument limits; otherwise mark the certificate *probabilistic* or abstain.
3. Before seeing held-out outcomes, predeclare 30/60 Hz downsampling phases, exposure kernels, timestamp jitter and missingness; compute certificates from endpoints only. Ground truth is high-rate minimum aperture with rater uncertainty.
4. Stratify nuisance conditions: gaze, glasses, illumination, geometry, blur, occlusion and rolling shutter. Treat any false 'closure impossible' certificate as a critical falsification; count abstentions and interval coverage with participant-clustered uncertainty.
5. If recordings cannot support independent velocity ceilings, execute synchronized motorized aperture/LED pulse instrument validation, labeling the evidence **instrument**, not human physiology. Never use the synthetic test as human evidence.

## Release decision
The existing point-sample theorem is conditional on a **verified upper bound** V. Empirical sample maxima, even on high-frame-rate videos, are not such a bound. Block deterministic no-blink/no-closure product claims until physical assumptions and timing/kernel/measurement uncertainties are independently established. Keep `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.

Run: `python3 research/observability/e002_662_velocity_tail.py`. Python stdlib only. Synthetic adversarial test; no human data, physical measurements or independent replay.
