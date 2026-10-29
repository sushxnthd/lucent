# E002-519 | Human/physical study handoff and reference-censoring register

Date: 2026-10-29. No participant was recruited, no instrument used, no video annotated, and no new human result is asserted in this file.

## Why this is a distinct empirical gate

E002-518 establishes that exported CSV row order does not prove native-frame continuity. E002-516 establishes that published blink peak velocities are not a certified hard continuous-time speed ceiling. The next useful experiment is therefore a **positive, independently timed anatomical counterexample search** against frozen ordinary-camera exclusions, not another synthetic parameter sweep or dataset metadata audit.

The test is asymmetric: a fully contained, independently verified closure witness falsifies an exclusion, but an apparently open high-rate sequence cannot certify no hidden closure during the high-rate camera's own blind gaps. This prevents an unobserved reference event from being counted as a negative ground-truth success.

## Operational procedure

**A. Existing authentic S01 anatomy-only pilot.** Run E002-502 on an authorized local machine; distribute only the two blinded reviewer packets; collect two actual independently completed annotations; adjudicate with E002-492. Keep private images, identities, native indices and individual ratings out of GitHub. Report aggregate measurable/disagreement/abstention counts. Because S01's timebase remains unauthenticated, **no duration, speed, or shutter-gap validation** is permitted.

**B. New instrumented physical pilot.** Recruit eight consenting adults, independent of S01, for a preregistered feasibility study. Borrow a high-rate camera capable of verified native acquisition >=240 Hz, and an ordinary 30-Hz camera. Use a photodiode-observed coded LED plus an independent reference clock, a native-index chain and calibrated exposure integration. Record same-eye geometry and iris scale. If one camera is rolling shutter, calibrate scanline timing and row movement. Predeclare exposure/clock uncertainty envelopes and refuse gaps whose robust blind interior is empty. This is a proposed study, not one that has been performed.

**C. Locked unseen-condition predictions.** Before reference anatomy is examined, freeze every ordinary-camera candidate gap, predicted EXCLUDE/ABSTAIN, timing envelope, geometry uncertainty and nuisance strata (lighting, gaze, blur, glasses, occlusion, missingness, head motion). Keep participants disjoint between development and validation; do not use reference labels to tune exclusions.

**D. Blinded reference adjudication.** Two independent raters annotate upper/lower lid and iris scale on native reference frames. For each apparent closure, confirm that its calibrated high-rate exposure is strictly contained in the ordinary-camera guaranteed blind interior under *all* timing uncertainties. An image-integrated darkness/blur proxy alone is not a witness. If closure interpretation, exposure containment, frame continuity or clock trace is uncertain, mark UNKNOWN. Independent reviewers must not be simulated by two AI prompts or copied annotations.

**E. Release-independent audit.** Preserve an owner-private table with these fields:

`participant_pseudonym,session_id,ordinary_gap_id,ordinary_prediction,left_end_max_ms,right_start_min_ms,reference_frame_id,reference_start_min_ms,reference_end_max_ms,dual_rater_closure,photometry_valid,clock_valid,native_provenance_valid,nuisance_clear,reference_decision,reason`

Allowed reference decisions: `FALSIFIED_BY_REFERENCE_WITNESS`, `REFERENCE_CENSORED_NOT_FALSIFIED`, `UNKNOWN`, `NOT_TESTABLE`. There is deliberately **no** `VERIFIED_NO_HIDDEN_CLOSURE` state. The owner must verify uniqueness of participant/session/gap IDs and account for all prespecified windows, including rejected and censored cases.

## Interpretation and go/no-go

- Any valid contained closure witness inside a gap previously excluded by Lucent is a direct counterexample to that specific prediction; preserve it, investigate nuisance and do not retrospectively relabel it away.
- Zero witnesses with censored reference gaps is inconclusive, regardless of sample size.
- If all selected windows abstain, report zero usable coverage, not zero risk.
- Pilot n=8 is for discovering failure modes. E002-509's 299-person zero-failure bound cannot be used unless reference outcomes are fully adjudicated and its independence, sampling and coverage assumptions hold.
- Even a successful pilot does not certify a universal human velocity bound, no-blink guarantee, sleepiness, PERCLOS or medical-grade measurement.

**Evidence count at handoff:** independent human S01 ratings 0; physical calibrated captures 0; independently certified continuous-time speed bounds 0; held-out human predictions 0. Product ABSTAIN_UNCALIBRATED; release BLOCKED. No merge, deployment or scheduling change.
