# E002-450 — independent-rater repeat failure can be hidden by pooled means

**Date:** 2026-10-26. **Frozen before implementation:** [E002_450_FROZEN.md](E002_450_FROZEN.md), commit `23620e6bd08c589043d41123ded6c8e7d881498f`. **Evidence tier:** deterministic synthetic counterexample and local 15-test replay; repository-hosted verification pending at initial report. **No new human anatomical labels or physical timing calibration.**

## Falsification of the prior pilot adjudicator

The unchanged E002-448 `adjudicate` function first averages two raters' aperture measurements for each view, then compares these pooled averages between a hidden repeat and its original. This does **not** necessarily enforce the protocol's requirement that **each individual rater** remain consistent across the repeat.

Frozen synthetic counterexample (dimensionless image-space apertures, not observed human measurements):

| Presentation | Rater A | Rater B | Pooled mean |
|---|---:|---:|---:|
| Original | 0.10 | 0.12 | 0.11 |
| Hidden repeat | 0.14 | 0.12 | 0.13 |
| Absolute difference | **0.04** | 0.00 | **0.02** |

The frozen repeat tolerance is **0.03**. Rater A fails it, but the pooled means pass. In a six-unique-frame synthetic fixture, the old scorer accepts **6/6** frames, while the new independently per-rater gate accepts **5/6** and rejects the inconsistent repeated frame. This is an adversarial reference-reliability counterexample, **not** a human-data finding.

A second frozen counterexample gives both raters only **one** annotation in a seven-view fixture. E002-448 reports `PILOT_2D_CONSENSUS_ONLY` for that one accepted frame, although six views are missing. E002-450 returns `NOT_EVALUABLE_INCOMPLETE` and zero eligible frames/pairs.

## Correction and controls

[E002-450 evaluator](e002_450_reference_gate.py) is an additional strict, read-only quality gate, not a retroactive modification of E002-448's frozen result. It checks exact submitted view-set completeness, distinct nonempty rater codes, nuisance flags, valid geometry, **per-rater** repeat differences <=0.03, and between-rater agreement <=0.03. It reports only aggregate candidate medium/short pair coverage, never frame IDs, timestamps, raw coordinates, images, rater identities or the private master key. Rater-code inequality does not prove real-world independence; operators must verify this separately.

The [15 synthetic/adversarial tests](test_e002_450_reference_gate.py) include the two preregistered counterexamples, complete valid fixtures, one- and two-rater repeat failures, between-rater disagreement, nuisance abstentions, invalid geometry, missing records, duplicate/unknown IDs, invalid strata, nonfinite coordinates and no-secret output. Local replay passed **15/15** using a faithful isolated stand-in for the unchanged E002-448 functions. The [dedicated hosted workflow](../../.github/workflows/e002_450_reference_gate.yml) imports the **actual repository implementation** and is the independent integration check; do not claim hosted success until its run completes.

## Scientific and product consequences

This result weakens confidence in the **annotation reference itself**, before physical validation is even considered. For any future human annotation study, only a complete, independently double-annotated, per-rater repeat-consistent pilot may be described as eligible for *image-space* descriptive measurement. A passing synthetic fixture does not constitute human evidence.

E002-371 remains **physically unvalidated**. The existing S19 pack still has **zero human rater labels**, unverified event-to-exposure timing and no anatomical millimeter scale or independent physiological velocity cap. S21/S22 remain sealed. No hidden-closure guarantee, blink duration, PERCLOS, fatigue or medical product claim is allowed: `ABSTAIN_UNCALIBRATED`. No merge or release.

**Next non-synthetic action:** Regenerate the private S19 pack under controlled local storage, obtain two genuinely independent blinded human annotation exports, run the strict gate, and independently authenticate exposure timing and anatomical scale before prospective S21/S22 testing. If those external inputs remain unavailable, report the blocker rather than continuing proxy/theorem polishing.
