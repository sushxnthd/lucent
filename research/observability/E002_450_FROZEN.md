# E002-450 — frozen adversarial audit of human-annotation eligibility

**Frozen:** 2026-10-26, before implementing the new evaluator or executing the new counterexamples. Parent E002-371; builds on E002-448/449. S19 is pilot only; S21/S22 remain sealed.

## Scientific question

Can the existing E002-448 adjudicator mark an annotation set eligible even though (a) one independent rater is inconsistent across a hidden repeat or (b) almost all views are missing? This is a *reference-measurement reliability* question. It does not provide human anatomical labels or authenticated physical exposure times.

## Precommitted falsification cases

1. Construct one repeated frame with A's normalized aperture changing from 0.10 to 0.14 and B remaining 0.12 on both presentations. Each cross-rater discrepancy is <=0.02, and the two pooled means differ by 0.02. Prediction: E002-448 accepts that repeated frame despite A's within-rater discrepancy of 0.04 exceeding its frozen 0.03 threshold.
2. Give each rater valid annotations for just one unique, nonrepeated view while omitting the other views. Prediction: E002-448 returns `PILOT_2D_CONSENSUS_ONLY` despite grossly incomplete coverage.
3. Build a new independent, read-only quality gate over the frozen private master and both rater files. It must require exact view-set completeness, distinct nonempty rater identities, and **per-rater** repeat consistency <=0.03 before accepting a unique frame. It must reject unknown/duplicate IDs, invalid status, missing reasons for abstention, bad landmarks and cross-rater disagreement. Missing/invalid views must never be treated as witnessed open intervals.
4. Aggregate coverage by medium-gap and short-gap strata, and count eligible candidate pairs, with no per-frame mapping, labels, images, IDs or coordinates in exported summaries. Report any differential reference coverage; never infer a physiological population rate from one participant.
5. A nonzero quality score must not authorize physical eyelid closure, blink duration, PERCLOS, fatigue, or medical claims. `ABSTAIN_UNCALIBRATED` remains mandatory, even for complete synthetic annotation fixtures.

## Independent tests and stop rules

Run the counterexamples against the unchanged E002-448 implementation, then validate the new gate with complete consistent synthetic fixtures, asymmetric rater-repeat failures, partial files, nuisance abstentions, invalid IDs, malformed geometry and differing rater identities. No human observations may be invented. Preserve any surprising or failed results. Do not use S21/S22, retune anatomy proxies, or treat frame counts as independent participants.

## Release consequence

Only a *complete, independently double-annotated, per-rater repeat-consistent* S19 pilot may be eligible for image-space descriptive analysis. Even that is **not** a physical E002-371 validation. Actual human labels, authenticated shutter timing, independent anatomical scale, and a defensible velocity cap remain external blockers.
