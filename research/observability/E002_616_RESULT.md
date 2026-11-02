# E002-616 | Bilateral human full-closure virtual-alias test

**Status (2026-11-03): authentic published-human-source hosted experiment PASSED; aggregate result persisted and independently arithmetically audited.** Parent E002-371. Prospective protocol was frozen *before bilateral source analysis* at [commit d3a3593](https://github.com/sushxnthd/lucent/commit/d3a3593fedb500ede42e44e3b9bddcece8bfada0).

## Main source-derived result

The SHA-256-pinned Silesian5 published human eyelid annotations and acquisition timestamps yielded **279 eligible contiguous simultaneous bilateral full-closure runs** across five source sequences. Bilateral means *both* source FC fields equal `C` (investigator 90–100% closure category) in the same source frame, with valid flanks and without specified nuisance flags. It is not a new independent anatomical rating.

| Preregistered endpoint | Original frame-index selector | Source-timestamp nearest-frame selector |
| --- | ---: | ---: |
| Eligible bilateral runs | 279 | 279 |
| Distinct runs omitted under at least one of ten phases | **39** | **39** |
| Omitted run-phase combinations (279 × 10 = 2,790) | **105** | **105** |
| Long runs (>=4 source frames) omitted | **0** | **0** |

The eligible run-length histogram was **4 one-frame, 14 two-frame, 21 three-frame, and 240 >=4-frame** bilateral runs. The prespecified interior exact floor-index phase law held on **279/279** eligible runs: `4×7 + 14×4 + 21×1 = 105` omitted run-phase combinations. This is a deterministic selector identity, not a population statistic.

**Paired source-timing sensitivity:** Despite identical 105 aggregate omissions under both selectors, **38/2,790 event-phase decisions differed**. The two selectors jointly omitted **86** event-phase pairs; hence **19** were index-only and **19** timestamp-only. Aggregate equality does **not** imply phase-by-event agreement. The experiment does not establish whether the *same* 39 distinct events were ever omitted under the two selectors.

Per-sequence eligible run counts were **98, 27, 50, 72, 32**; per-sequence some-phase omission counts were **4, 3, 13, 17, 2** for both selectors. All source-defined eligibility exclusions were zero. No longer-run timestamp-selector surprise was observed; the possibility was explicitly preserved rather than suppressed by the implementation.

## Provenance and independent checks

- [Frozen protocol](E002_616_FROZEN.md), [source-bound Python executable](e002_616_bilateral_alias.py), [independent synthetic JavaScript oracle](e002_616_independent.cjs).
- [Successful hosted human-source run #41535538159](https://github.com/sushxnthd/lucent/actions/runs/41535538159) on 2026-11-02 UTC, source step logs contain the complete aggregate JSON. The workflow checked the authenticated archive SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`. Python synthetic self-test **6 groups PASS**, JS synthetic oracle **12 checks PASS**, source replay step **PASS**.
- [Persisted source output](E002_616_AGGREGATE.json) copies the JSON emitted by that hosted source step without raw human rows or identifiers. [Independent aggregate arithmetic verifier](e002_616_aggregate_verify.cjs) re-sums five sequences, ten phases, run-length histogram, index law, and paired symmetric difference, and rejects deliberate corrupted aggregates. This is **independent arithmetic**, not independent full-source reannotation or replay.
- Phase trials are dependent; only five source sequences are included. Do **not** interpret 39/279 as a population omission rate or 105/2790 as a field-camera failure probability. Ten phases are counterfactual virtual selections, not ten separate human captures.

## Falsification and product consequences

This source-derived human categorical result supports the **existence** of simultaneous bilateral full-closure events missed by at least one virtual 30-Hz point-sampling phase, under the frozen source definitions. It rejects a blanket assertion that virtual ordinary-rate sampling necessarily observes every source-labelled simultaneous bilateral full closure. It **does not** establish that a real 30-fps camera with nonzero shutter integration misses those same events.

The experiment provides **no physical exposure/shutter calibration**, **no independent continuous-time anatomical aperture trajectory**, **no certified physiological eyelid velocity maximum**, **no independent blinded raters**, and **no held-out synchronized physical-camera predictions**. Source labels are categorical. Consequently it **does not validate the E002-371 shutter-gap/velocity exclusion bound**, nor justify a fatigue/sleepiness claim.

**Next decisive test:** paired ordinary/high-speed physical capture with measured exposure intervals and clock uncertainty, blinded calibrated anatomical aperture ratings, independently justified velocity-envelope premises, and presealed participant-disjoint predictions of which ordinary-camera gaps can hide closure. Test geometry, brightness, missingness, blur, gaze, glasses, and clock error; abstain on violated assumptions. Avoid further source metadata archaeology or synthetic theorem polishing.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. Hush's separate branch and PR #45 are not modified.
