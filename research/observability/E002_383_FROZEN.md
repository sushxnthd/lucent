# E002-383 frozen end-to-end synthetic RGB falsification protocol
Frozen 2026-10-23 before evaluation. One kernel: E002-371/373/382 shutter-gap no-hidden-closure certificate. This is NOT human validation.

## Instrument and labels
Generate continuous piecewise-linear eyelid aperture trajectories with independently known speed bound V, expose the left/right intervals by numerical quadrature, and use a 24x40x3 synthetic RGB eye patch (closed/open templates) with shutter averaging. Label hidden closure from the **latent continuous trajectory**, never from RGB predictions. The RGB extractor is a fixed template-projection estimator trained only on synthetic open/closed templates. Include independently randomized exposure means, shutter gaps, velocity, closure depth, and nuisance amplitudes. Random seed 383; hold out the random trials from all calibration choices.

## Prespecified hypotheses
1. Correct scalar timing, speed and bounded aperture error must produce zero certified hidden closures; any counterexample invalidates implementation.
2. A naive RGB estimator using nominal timing and zero error allowance will produce at least one false no-hidden-closure certificate under either photometric gain drift or timestamp underestimation.
3. With measured timing upper bounds, correct V, and a conservative **deterministic** RGB error envelope, every in-envelope trial will avoid false certification; abstention rate is a first-class output, not hidden.
4. A deliberately out-of-domain photometric/geometry/missingness/blur/gaze/glasses stress suite must either be explicitly rejected by the gate or invalidate the certificate. Do not claim robust certification for uncalibrated nuisance.
5. Report exact counts and Wilson confidence intervals for selective false-certification rates, but do not infer a human error rate or distribution-free reliability from synthetic zero failures.

## Ablations
Run clean, in-envelope photometric, timestamp-jitter, gain/offset, spatial-gradient, gaze shift, blur, glasses/glare, missingness, and out-of-domain mixed nuisance. Preserve all failures. Compare ideal scalar certificate, naive RGB certificate, bounded RGB certificate, and domain-gated certificate.

## Claim freeze
Only calibrated synthetic-camera gap qualification is eligible. Unconditional PERCLOS, blink count, pupil reconstruction, or five-second fatigue diagnosis are not supported. Human paired-RGB/high-speed validation remains required. No further dataset archaeology in this run: two targeted dataset attempts were already exhausted in earlier runs.
