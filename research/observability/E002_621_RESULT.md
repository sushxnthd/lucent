# E002-621 | Adversarial scalar exposure-boundary surrogate (2026-11-03)

## Question and evidence tier
Does E002-620's exposure-aware exclusion certificate ever exclude a closure on an admissible piecewise-linear Lipschitz aperture trajectory when its measurement uncertainty envelopes are conservative? This is a **synthetic falsification attempt**, not physical validation, independent replication, or a new physiological speed estimate.

## Frozen synthetic model
Seed 621, 100,000 trajectories. Draw velocity V in [1,300] mm/s, first/second exposures in [2,50] ms, dark gap in [0,70] ms, closure threshold in [0,2] mm. Seven nodes span exposure endpoints, exposure midpoints and dark-gap midpoint. Each successive node differs by at most V times elapsed time and aperture is nonnegative. Compute exposure means by exact trapezoidal integration. Independently weaken observed means by up to 0.4 mm; increase assumed speed by up to 50%, exposure lengths by up to 3 ms, dark-gap upper bound by up to 3 ms and closure threshold by up to 0.3 mm. Compare the conditional certificate with the actual piecewise-linear minimum in the dark gap.

## Local result (not hosted CI)
Executed `python research/observability/e002_621_adversarial_surrogate.py` locally before pushing. Results: 100,000 trials; 21,038 conditional exclusions; 34,394 hidden trajectories; **0 false exclusions**; 78,962 abstentions. This is a finite randomized consistency check, not proof. Seed and code are committed for independent replay. It does not test realistic image formation, correlated miscalibration, clock drift, acceleration spikes, rolling shutter or human eyelid geometry.

## Negative-control and release consequence
Replacing exposure-average aperture with instantaneous endpoints changes a strict inequality: for m1=m2=3 mm, T1=T2=20 ms, G=20 ms, V=100 mm/s and closure threshold 1 mm, naive zero-exposure substitution excludes, while the exposure-aware conservative certificate abstains at equality. This is an analytic decision counterexample, not an observed human event.

**Product gate remains ABSTAIN_UNCALIBRATED / BLOCKED.** No physical shutter or independently certified human velocity inputs have been obtained. Next scientific step: calibrated synchronized acquisition and held-out human predictions; further synthetic polishing cannot satisfy that gate.
