# E002-519 | One-sided reference-censoring correction for human validation

Date: 2026-10-29. Primary Lucent E002-371 kernel. [Frozen protocol](E002_519_FROZEN.md) preceded the [prospective study handoff](E002_519_HUMAN_STUDY_HANDOFF.md), [noncertifying evaluator](e002_519_reference_censoring.py), and [11 adversarial controls](test_e002_519_reference_censoring.py). Evidence tier: **logical inference rule, prospective physical study protocol and synthetic software checks**, not a new human measurement.

## Result and proof sketch

A finite-frame-rate high-speed reference is itself a sampled measurement, not continuous-time ground truth. Let an ordinary-camera blind interior guaranteed under all shutter/clock uncertainty be (L_max,R_min). If an independently calibrated reference exposure lies wholly inside this interior, and two genuinely independent blinded raters plus a validated radiometric model establish that closure occurred at least once during that exposure, then an ordinary-camera prediction excluding all hidden closures in that interior is **falsified**. This is a positive witness and does not require a hard global eyelid-speed ceiling.

Conversely, a high-rate recording containing no observed closed frames does not logically imply that no closure occurred between its exposures. Two continuous-time eyelid trajectories can agree on all recorded high-rate exposures while one contains an unobserved short closure in a reference blind gap, absent a separately validated motion bound. Therefore the no-witness case is **reference-censored**, not VERIFIED_NO_HIDDEN_CLOSURE. This is a standard sampling identifiability limitation, not claimed as a new universal theorem.

## Enforced behavior

The evaluator requires a frozen EXCLUDE/ABSTAIN decision and explicit timing envelopes, anatomical witness category, independent-rater, photometric, clock, native provenance and nuisance flags. It returns FALSIFIED_BY_REFERENCE_WITNESS only for a strictly contained qualified positive witness. Missing or uncertain evidence is UNKNOWN; no witness is REFERENCE_CENSORED_NOT_FALSIFIED; no robust gap or no EXCLUDE is NOT_TESTABLE. It never emits a clearance certificate, and does not itself authenticate the input booleans.

Eleven local adversarial tests passed on 2026-10-29: contained positive witness; boundary-touch non-witness; open-frame censoring; no reference; unverified clock; missing independence flag; abstention; empty robust gap; positive witness plus unknown; duplicate gap; nonfinite timing. [Hosted CI workflow](../../.github/workflows/e002_519_reference_censoring.yml) was queued at report creation; no hosted pass claimed.

## Scientific and product consequence

This corrects a potential validation error: treating high-rate non-observation as a clean negative could falsely lower estimated exclusion-failure risk, even with many participants. E002-509's statistical confidence calculation is applicable only to independently and fully adjudicated participant outcomes under its assumptions. A genuinely witnessed contradiction can already kill an exclusion, but zero such contradictions does not certify safety. The strongest next empirical step is the unchanged private S01 dual-rater anatomy pilot, followed by borrowed-equipment synchronized high-rate/ordinary-rate capture with independently measured exposures and participant-disjoint frozen predictions.

**Actual independent anatomical ratings: 0. Authenticated physical captures: 0. Certified continuous-time speed bounds: 0. Held-out human predictions: 0.** Product ABSTAIN_UNCALIBRATED; release BLOCKED. No merge or schedule change.
