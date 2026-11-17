# E002-371 prospective human shutter-gap validation (protocol freeze 2026-11-17 UTC)

Status: PROTOCOL ONLY. No human data collected; no physiological validation or release approval.

## Claim under test
For a continuous eyelid-aperture trajectory a(t) with |da/dt| <= V (an independently calibrated upper bound), observed endpoint lower bounds a0 and a1, and closure threshold c, an unobserved closure between two instantaneous observations requires a gap duration T >= ((a0-c)+(a1-c))/V, provided both endpoints exceed c. Equivalently Q=VT/((a0-c)+(a1-c)); Q<1 rules out closure under all stated assumptions. Equality is not an exclusion. Use the maximum physically possible T and maximum plausible V, and minimum endpoint apertures; otherwise abstain. Exposure integration, rolling shutter, unbounded velocity, uncertain geometry, or unresolved reference labels invalidate this simplified test.

## Independent acquisition and pre-registration
Record consented adults with a >=240 fps reference camera (prefer >=500 fps), calibrated physical aperture scale and hardware-timestamped frames; simultaneously record the target ordinary camera (nominal 30/60 fps). Independently measure actual exposure start/end, dropped frames and clock offset using a shared flashing LED/photodiode observable to both streams. Do not infer reference frame rate from encoded playback metadata alone. Save raw files, hashes, sensor configuration, lens distance, reference scale, timing calibration, annotation protocol, and exclusion logs. Treat reference occlusion and temporal ambiguity as unknown rather than negative closure.

Split subjects, not gaps: pilot for apparatus debugging, then calibration participants for estimating a conservative velocity ceiling (including uncertainty and outlier policy), then unseen held-out participants for locked predictions. Freeze V, threshold c, aperture extraction, reference labeling, endpoint intervals, clock uncertainty and abstention criteria before held-out labels are opened. An estimated population percentile is NOT a universal speed bound: any participant outside the validated envelope must cause abstention, and even within it exclusions remain conditional on coverage assumptions.

## Primary endpoint and analysis
Primary endpoint: count of reference-confirmed full closures among confidently excluded gaps, with numerator, number of eligible gaps, number of held-out subjects, and number of subjects with >=1 false exclusion. A single verified false exclusion falsifies the conditional implementation/assumption bundle. Report all exclusions, abstentions, unresolved references and non-exclusions by participant. No binomial gap-level confidence bound treating correlated gaps as independent. Report subject-cluster bootstrap as descriptive only and include a worst-case participant-level failure bound. Prespecify an intended held-out sample size and stopping rule before capture; do not claim validation from zero events in an arbitrarily small sample.

## Nuisance challenge matrix
Within held-out subjects vary gaze (straight/up/down), illumination, exposure/blur, head rotation, distance, glasses, eyelash/eyelid occlusion, frame drops, rolling-shutter direction and clock jitter. Capture a static mechanical aperture surrogate with known imposed velocity and programmable shutter timing to separately test geometry/timing assumptions. Each nuisance has a predeclared out-of-envelope abstention route. Compare against naive nominal-FPS and point-estimate-velocity baselines. Track abstention and utility tradeoff, not just false exclusions.

## Release consequence
Do not enable camera-derived fatigue inference from this theorem alone. A validated closure-exclusion classifier is not a validated fatigue or sleepiness measurement. The bounded alpha may expose a shutter observability diagnostic with explicit conditional assumptions and abstention, while retaining user-reported sleepiness and reaction-time tasks as separate non-diagnostic inputs subject to their own validation.

## Acquisition blocker
No authenticated high-frame-rate human dataset or physical shutter capture is attached to this protocol. Next substantive experiment must be real instrument capture or an independently sourced video with verified native acquisition timing; no further evaluator-only refinements substitute for that evidence.
