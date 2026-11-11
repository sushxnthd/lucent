# E002-701 — Joint uncertainty stress of shutter-gap exclusion

**Evidence:** exact-rational deterministic synthetic stress, executed locally 2026-11-07 UTC; no human or physical data.

## Frozen construction
True endpoint apertures a,b are on {0,0.1,...,1}. Measured endpoints each have signed error in {-0.1,0,+0.1}, with measured values restricted to [0,1]. True Lipschitz ceiling v is 0.5 or 1, and actual gap d is 0.5, 0.6 or 0.7. Only endpoint pairs feasible under |a-b|<=vd are retained. Closure threshold is 0.5. The true attainable minimum is (a+b-vd)/2. The naive certificate assumes measured endpoints exact, v=0.5 and d=0.5. The robust certificate uses each measured endpoint minus 0.1, v_max=1 and d_max=0.7.

## Executed result
3,948 feasible synthetic configurations; naive certificates 842, of which **318 falsely exclude attainable threshold closures**. Joint-uncertainty certificates 24, with **zero false exclusions on the tested grid**. The robust rule withdraws 818 nominal certificates. Example: true endpoints 0.5 and 0.6, measured 0.6 and 0.7, v=0.5 and d=0.5 yield a true attainable minimum 0.425, despite the naive rule certifying exclusion.

This is not a human error rate, statistical safety guarantee or camera calibration. The robust inequality is conditional on *valid* simultaneous endpoint-error, timing and velocity envelopes; a finite empirical maximum is not a deterministic physiological ceiling. The robust rule is deliberately conservative, and the counts depend on the artificial grid. Code: `python3 research/observability/e002_701_joint_uncertainty.py`.

## Product consequence and next test
Lucent must not combine individually nominal aperture, clock and velocity estimates into a closure-exclusion claim. It must propagate their joint conservative envelopes or abstain. No evidence here establishes such envelopes for a phone. Product stays `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Execute E002-690 synchronized physical shutter/occluder acquisition and E002-695 blinded predictions before high-rate labels; obtain independent human velocity validation.
