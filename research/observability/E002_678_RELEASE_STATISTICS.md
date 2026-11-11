# E002-678 | Predeclared human-validation evidence and release decision rule (2026-11-06 UTC)

**Evidence tier:** prospective statistical design and product consequence, NOT human data, a new theorem, or independent validation. This document supplements, and does not replace, frozen E002-671. It does not change E002-371's assumptions.

## Primary endpoint and unit
A **false exclusion** occurs when a calibrated low-frame-rate gap or exposure certificate says closure is impossible, while an independently adjudicated synchronized high-speed reference positively establishes a closure in that same physical interval. Ambiguous reference intervals are **indeterminate**, never counted as true negatives. The numerator is independently adjudicated false exclusions; the denominator is all eligible certificates whose intervals have determinate reference status. Separately report **coverage** as eligible certificates divided by all attempted intervals, with abstentions and acquisition failures included in the denominator. Report participant counts, certified intervals per participant, and all excluded/indeterminate intervals.

## Frozen prediction and controls
Before opening held-out reference labels, freeze the velocity-bound source, shutter/row timing model, exposure integration, clock uncertainty, aperture geometry, confidence intervals, threshold, and code hash. Fit any parameters on disjoint development participants and physically independent instrument calibration. Prespecify participant-disjoint test IDs, conditions, failure and missingness handling, and annotation adjudication. Cross brightness, gaze, glasses/reflection, motion blur, facial geometry, row displacement, missing frames, timestamp jitter, and camera model. Preserve all negative findings.

## Why zero observed errors is not enough
Under an **independent Bernoulli interval** model, the exact one-sided 95% upper confidence limit after zero false exclusions in n determinate certified intervals is 1 - 0.05^(1/n). Thus n=100 gives 2.951%, n=300 gives 0.9936%, n=3000 gives 0.09981%. These numbers do **not** justify a population-level 0.1% claim if intervals from the same participant are correlated or sampled nonrepresentatively. In particular, treating thousands of adjacent frames from one participant as thousands of independent trials is invalid.

## Cluster-aware primary decision
Treat participants as the independent sampling units. Report the number of held-out participants with >=1 false exclusion, with an exact participant-level one-sided 95% binomial bound, and separately report within-participant event counts and coverage distributions. Even with **zero** affected participants, a <1% participant-level upper bound requires at least 299 independent held-out participants (because 1-0.05^(1/299) is approximately 0.997%). This is a planning calculation, not a guaranteed safety rate or a sample-size substitute for representative recruitment. Any confirmed false exclusion is a **hard blocker** for the affected certification regime, irrespective of aggregate error rates.

## Product decision
* **BLOCKED** until physical shutter/row/clock calibration, defensible velocity ceiling, independent reference sensitivity, held-out human test, and external replay exist.
* **ABSTAIN_UNCALIBRATED** on missing/invalid calibration, untrusted provenance, uncertain reference, model mismatch, or nuisance outside validated bounds.
* After sufficient evidence, any allowed statement must be limited to the exact interval, acquisition conditions, and calibration regime tested. Never infer whole-night sleep quality, fatigue, or absence of unobserved blinks from an interval certificate.
* Do not present zero synthetic counterexamples as an empirical false-exclusion rate.

## Research-priority correction
E002-677's rolling-row synthetic counterexample overlaps the earlier E002-512 rolling-scanline falsification. It is a useful independent formulation, **not** a new scientific priority claim. Further synthetic row-timing examples are low priority. The next evidence-changing action is synchronized physical acquisition and blinded held-out human adjudication under E002-671.

No human or physical acquisition was performed for this artifact.
