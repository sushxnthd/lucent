# E002-519 | Frozen one-sided human falsification and interval-censored reference protocol

Date: 2026-10-29. Primary E002-371 kernel. Frozen before any E002-519 human data or software. Existing branch and draft PR #26. Evidence tier: prospective human-validation protocol; **no new human measurements**.

## Question and exact asymmetry

Can a genuinely independently observed eyelid closure falsify an ordinary-camera gap's "hidden closure excluded" prediction without assuming an unverified hard human speed limit? **Yes, one-sidedly.** An independently anatomically supported closure witness whose entire possible high-rate exposure lies inside the ordinary-camera blind gap contradicts exclusion. But no observed closure at high-rate sample times does **not** establish that none occurred between those samples. Do not convert absence of observed closures into a verified negative reference.

## Frozen primary decision rule

For a candidate ordinary-camera gap, let the latest possible left-exposure end be L_max and earliest possible right-exposure start be R_min. The guaranteed blind interior is (L_max,R_min). A reference frame has possible exposure-start interval [s_min,s_max] and possible exposure-end interval [e_min,e_max], from independently measured per-frame timing, including rolling-shutter scanline and clock uncertainty.

A positive **reference closure witness** requires all of: (i) two independent blinded human raters concur that the aperture is at/below the predeclared physical closure threshold with explicit landmark/iris-scale uncertainty; (ii) reference exposure and photometric integration have been calibrated so that the observed image supports at least one true closure within that exposure, not merely a blurred appearance; (iii) independent native-frame provenance; (iv) s_min > L_max and e_max < R_min (strict robust containment); (v) no unresolved geometry, gaze, brightness, glasses, blur, occlusion, missingness or clock flags. If Lucent excluded closure in this gap, output FALSIFIED_BY_REFERENCE_WITNESS. The falsifier does not require a population-wide speed ceiling.

If any requirement is missing, output UNKNOWN/NOT_TESTABLE. If no closure witness is found, output REFERENCE_CENSORED_NOT_FALSIFIED, **never** VERIFIED_NO_HIDDEN_CLOSURE. Even a 240-fps reference has its own blind gaps. No positive result establishes an unconditional physical guarantee.

## Frozen collection and evaluation

1. First conduct the existing private E002-502 S01 two-rater pilot, anatomy only. Do not infer S01 time from AVI nominal fps or unauthenticated Phantom metadata.
2. For a physical pilot, use an independently synchronized high-rate reference (target >=240 captured frames/s, not merely file playback fps), ordinary 30-fps capture, hardware LED/photodiode timing and native-frame ledger. Confirm actual exposure start/end per relevant scanline and clock errors. Borrow equipment; do not purchase.
3. Freeze participant IDs, camera settings, closure threshold, eligible gap sampling, nuisance strata, exclusion decisions and reference adjudication **before** unblinding. Pilot target eight distinct consenting adults for feasibility/counterexample discovery, not statistical release certification. Record ordinary-camera exclusion decisions before viewing high-rate anatomy.
4. Blind both raters to the ordinary-camera exclusion, candidate status and each other's ratings. Resolve only by predeclared interval intersection; disagreement/ambiguous anatomy => UNKNOWN. Preserve raw data privately under consent and licensing.
5. Report all preselected gaps, excluded gaps, witnessed contradictions, reference-censored gaps, nuisance-specific abstentions, native-index failures, clock-calibration failures, and participant-level counts. No cherry-picking, no treating unknown as a clean success.
6. A 299-person zero-failure statistical bound from E002-509 is inapplicable if reference truth remains censored or eligibility was selected after seeing labels. Population claims require a separate adequately powered, participant-disjoint, fully adjudicated study and a stated utility/coverage gate.

## Falsification, stopping and product

One valid witness is enough to refute the specific exclusion. Zero witnesses is not proof of correctness. If reference timing cannot be independently authenticated, or if anatomical/photometric evidence cannot support the closure witness, report only feasibility and stop making hidden-closure claims. Lucent must remain ABSTAIN_UNCALIBRATED, release BLOCKED. This is an asymmetric test protocol, not a new physiological theorem or completed empirical result.
