# E002-470 FROZEN — integrated moving-aperture blind instrument surrogate

Frozen 2026-10-27 before executing the new evaluator or viewing aggregate outcomes. Primary E002-371 empirical gate remains **NOT_ESTABLISHED**. This is a reproducible **synthetic physical-aperture surrogate**, not human/physical acquisition, and does not supersede E002-469's stop on S19 timing archaeology.

## Question and independent oracle
Does the *existing* E002-456 conditional camera exclusion decision remain sound when fed independently generated, exactly shutter-integrated, piecewise-linear moving-aperture trajectories satisfying its declared symmetric Lipschitz speed cap? Can small, independently specified calibration faults cause false exclusions if a nuisance PASS is self-attested, and do explicit nuisance FAIL flags force abstention?

Generate a continuous nonnegative V-shaped aperture a(t)=m+s|t-p| with slope s<=0.25 mm/ms (250 mm/s), c=2.0 mm. Its shutter means are **independently** computed as exact analytic boxcar integrals, not from E002-456's lower-envelope formula. The ground-truth minimum in the unexposed interval [e/2, dt-e/2] is m+s*distance(p, interval). Truth is STRICTLY BELOW c. No negative human labels, hardware timestamps, or anatomical physiology are inferred.

## Prespecified clean stress
Seed 470371; 1,500 cases for each of 30/60/120/240 fps crossed with e=0.5/1.5 ms (12,000 cases). Sample s uniformly in [0.01,0.25] mm/ms; m in [1.5,2.8] mm; p in [-dt/4,5dt/4] ms. Input actual shutter means as nominal camera readings to E002-456 with zero declared measurement/clock error, symmetric boxcar, illustrative 250 mm/s cap and all declared nuisances PASS. Count exact crossing truth, EXCLUDED_CONDITIONALLY, NOT_EXCLUDED, ABSTAIN, and **false exclusions** (EXCLUDED with truth<c) per stratum. Independently compare a small frozen set of analytic integrals against dense trapezoid numerical quadrature. No calibration tuning on results.

**Kill criterion:** any clean false exclusion falsifies implementation soundness under its stated synthetic assumptions. An unexpected clean abstention is a separate implementation failure. Zero failures verifies only this restricted model, never human correctness.

## Prespecified adversarial controls
Construct a 240-fps, e=1.0-ms V-shape with m=1.99 mm, s=0.25 mm/ms, p=dt/2. It contains a real subthreshold dark-gap closure. Test independently imposed +0.075-mm apparent-aperture biases (brightness, blur, glasses, missingness, gaze); 3% apparent geometry scale error; and a +0.65-ms unreported effective frame separation (sampling, clock, rolling_shutter). The latter uses the **actual** longer dt to generate shutter readings but reports nominal 240-fps dt. Each corrupted world is evaluated twice: with all nuisance flags falsely PASS and with its corresponding flag FAIL. Record false conditional exclusions and fail-closed abstentions. Fault magnitudes are constructed challenges, **not empirically estimated camera tolerances**. Report any fault that does not flip a decision rather than adjusting its magnitude after observation.

## Scientific and release boundaries
All velocity caps, geometry, shutter calibration IDs and nuisance PASS flags in this surrogate are self-declarations. Even 0/12,000 clean failures is not independent verification of a physical speed cap, shutter timing, optical response, or anatomical labels. No real video, subject IDs, or raw human data. Preserve per-stratum negative results, deterministic generator, independent truth oracle, tests and machine-readable aggregate. Do not use E002-470 to release physical hidden-closure, blink duration, PERCLOS, fatigue or medical claims. Product remains ABSTAIN_UNCALIBRATED; PR #26 stays draft. Hush remains separate.
