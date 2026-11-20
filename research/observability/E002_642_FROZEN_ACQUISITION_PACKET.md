# E002-642: Frozen acquisition and surrogate falsification packet (2026-11-04 UTC)

## Evidence status
Instrument-design and synthetic model check ONLY. No human data, no independently calibrated acceleration, no real shutter acquisition. This packet must never be cited as physiological validation.

## Pre-registered prediction
For aperture endpoints a,b, certified upper closure threshold c, certified closing/opening velocity ceilings v_c,v_o, and the *maximum possible* shutter gap G including timestamp uncertainty, predict EXCLUDE only if (a-c)/v_c + (b-c)/v_o > G. Equality and every uncalibrated input abstain. Endpoint aperture uncertainty must use lower confidence/certified bounds; threshold uncertainty uses an upper bound. Velocity ceilings must be continuous-time bounds, never finite-difference maxima alone.

## Physical validation protocol (requires external acquisition)
1. Record consenting adults with synchronized >=240 fps reference camera and 30 fps target camera, a visible hardware LED clock and measured exposure windows. Predeclare 30 fps subsampling offsets before reading closure labels. Record raw files, acquisition settings, hashes and consent/privacy policy. No collection is claimed here.
2. Independently calibrate mm-per-pixel and anatomical closure threshold with blinded raters; calibrate continuous-time speed/acceleration ceilings with explicit uncertainty and a separate reference session. Do not use held-out target frames to set bounds.
3. Split by participant (not frames), reserving at least 25% of participants and a separate nuisance challenge set. Freeze all bounds, software hash, trial definitions and predictions before revealing reference closure annotations.
4. Challenge brightness, glasses, gaze, head angle, motion blur, compression, missing frames, geometry and timestamp drift; report per-stratum abstention, exclusion coverage, false-exclusion count and exact binomial upper confidence bound. Any reference-confirmed closure under EXCLUDE blocks release pending adjudication.
5. Expose only calibrated EXCLUDE or ABSTAIN_REACHABLE; never turn reachability into evidence that closure occurred. Fail closed on missing certificates, unverifiable manifests, time sync errors or out-of-domain geometry.

## Surrogate check
Run `python research/observability/e002_642_instrument_trial.py`. Deterministic 144-case exact-rational grid yields 121 EXCLUDE/NO_CLOSURE and 23 ABSTAIN_REACHABLE/CLOSURE under the model. This is a model consistency check, NOT independent validation: the synthetic reference shares the same velocity assumptions as the predictor.

## Release blockers
No independently calibrated human velocity envelope; no reference-camera human recordings; no held-out participant predictions; no externally reviewed instrument timing or anatomical threshold; no real nuisance stress test. Production BLOCKED and ABSTAIN_UNCALIBRATED.

## Next scientific decision
Do not continue synthetic-only grid expansion. Obtain actual reference footage with trustworthy acquisition timestamps or implement a hardware shutter/LED timing validation before claiming an empirical boundary.
