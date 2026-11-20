# E002-615 | Human-source timestamp-aware virtual omission: equal totals conceal changed events

**Executed:** 2026-11-03. **Parent kernel:** E002-371. **Prospective freeze:** [E002_615_FROZEN.md](E002_615_FROZEN.md), commit `d0b0a0c6f659a7a8a02416d0907902676bbfa02f`, before inspecting source timestamp values. **Authenticated source:** [Silesian5/Basler5 research annotations](https://www.blinkingmatters.com/research), archive SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`. **Reproducible source analysis:** [e002_615_timestamp_stress.py](e002_615_timestamp_stress.py), independent *synthetic point-selector* oracle [e002_615_independent.cjs](e002_615_independent.cjs), [machine-readable aggregate](E002_615_AGGREGATE.json). **Corrected hosted source run:** [GitHub Actions #41526585851](https://github.com/sushxnthd/lucent/actions/runs/41526585851), completed successfully. No raw timestamps, filenames, frames, participant identifiers or private human images were committed.

## Preregistered question

The E002-582 human-source experiment found 202 positive eye-closure event-phase omissions under ten nominal 30-Hz **floor-index** sampling phases. Are the same individual omission decisions preserved when virtual 30-Hz point samples use the source's independently provided acquisition timestamp column? The frozen experiment also compares **uniform-timestamp nearest** selection, so a change in point-rounding convention is not misrepresented as source-timestamp jitter.

All five annotation/timestamp member pairs were unambiguously matched by stem and passed strict increasing-frame, increasing-timestamp and exact annotation-frame coverage checks. There are 58,884 source-annotated frames, 58,879 consecutive source intervals and 567 eligible per-eye full-closure runs under the inherited E002-582 label/nuisance rules. This is published human categorical annotation evidence, **not** new blinded anatomical rating or a physically recorded 30-fps camera experiment.

## Source-derived results

| Frozen comparison | Omitted event-phase pairs / 5,670 | Paired decisions changed versus actual timestamp-nearest |
| --- | ---: | ---: |
| Original E002-582 floor-index selector | **202** | **82** |
| Uniform-time nearest selector | **202** | **156** |
| Actual source-time nearest selector | **202** | baseline |

All three selectors have the **same aggregate 202**, but they do **not** omit the same event-phase pairs. Actual timestamp-nearest versus original index changes **82/5,670 = 1.45%** of paired decisions: because totals are equal, 41 formerly omitted pairs become retained and 41 formerly retained pairs become omitted. Actual versus uniform-time nearest changes **156/5,670 = 2.75%**, split 78 in each direction. These are paired changes in deterministic virtual sampling decisions, not estimated error rates or independent trial frequencies.

Actual timestamp-nearest per-phase omission counts are **[25, 16, 21, 22, 16, 17, 24, 24, 14, 23]**, versus original index **[29, 18, 21, 17, 20, 18, 25, 20, 14, 20]**. Each sums to 202. Across the five anonymized sequences, actual-versus-index disagreement counts are **[12, 22, 14, 30, 4]**, and actual-versus-uniform nearest counts are **[10, 28, 50, 64, 4]**. No participant-level inference is justified from only five source sequences.

The source-time interval median is `0.0100` in each sequence **in source-provided units**, not an independently calibrated SI time measurement. Within-sequence dimensionless interval/median quantiles have minima 0.9 and maxima 1.1; the median is 1.0. **Zero of 58,879** positive consecutive intervals are *strictly* more than 10% or 25% away from their sequence median. The timing values are evidently quantized at the precision exposed by the archive; the experiment cannot establish a physical clock uncertainty or exposure start/end time. Even modest per-frame timestamp differences can change virtual selected frames over a long sequence without a large local cadence outlier.

## Important instrumentation failure preserved

The first [hosted run #41514310880](https://github.com/sushxnthd/lucent/actions/runs/41514310880) completed, but incorrectly reported **523 intervals strictly outside ±10%** because it converted exact Decimal ratios to binary floats before testing `abs(ratio-1)>0.1`. Values at the exact +10% boundary were spuriously counted. This was **a software error**, not evidence of 523 source cadence violations. [Correction `2f240dd`](https://github.com/sushxnthd/lucent/commit/2f240ddc603a69c5128ee1f3c8971564f97ce88d) uses exact Decimal threshold comparisons and adds explicit ±10% and ±25% boundary fixtures. The corrected hosted run passed both Python adversarial controls and the independent Node.js selector oracle before re-retrieving the same authenticated human archive. The earlier false result remains linked rather than hidden. The selector's 202/82/156 counts were unaffected by this diagnostic correction.

**Verification tier:** independently checked *synthetic* nearest-time arithmetic and source-file integrity; authenticated *single implementation* source-data analysis; **no independent second-language replay of the full human-source timestamp/annotation pipeline**. An independent verifier must reproduce the 82/156 paired differences before treating those as independently replicated.

## Scientific interpretation and falsification

This falsifies the convenient inference that a preserved **aggregate** count of omitted human FC labels means preserved **individual** omission decisions. The original 202 total is structurally stable in this dataset and these ten deterministic phase definitions, but the event-phase membership is not. The uniform-time control additionally shows that a change from floor-index to nearest-point sampling can alter decisions even before attributing any difference to recorded timing.

This is a real human-source timestamp stress test of a **virtual point selector**. It is **not** a test of shutter integration, rolling shutter, independent physiological speed ceilings, or the sharp E002-371 continuous-time observability boundary. The phase grid is artificial and phase-event pairs are correlated; do not call 202/5,670 a 30-fps physical blink-miss probability. Discrete source `FC=C` labels indicate investigator-annotated 90–100% closure, not continuous aperture trajectories. Nominal 100-fps source cadence is not a calibrated acquisition-clock certificate.

## Direct product consequence and next decisive experiment

- Do not present nominal frame-index omission decisions as timestamp-calibrated physical camera predictions. The observed 82 paired changes make this an explicit claim rejection even when aggregate counts agree.
- Require authenticated acquisition timestamps, exposure intervals, clock uncertainty and calibrated anatomy before any individual hidden-closure exclusion; otherwise `ABSTAIN_UNCALIBRATED`.
- Preserve E002-371's existing shutter-aware sufficient condition only as a conditional mathematical statement. The current production release remains `BLOCKED`.
- The next decisive experiment is synchronized ordinary camera plus high-frame-rate anatomical reference, independently calibrated exposure/clock timing, independent human reviewers and a velocity bound estimated on disjoint calibration sequences, with predictions sealed before inspecting held-out closures. Reuse [E002_612_HUMAN_PROTOCOL.md](E002_612_HUMAN_PROTOCOL.md) and the cross-camera falsifier from E002-609; do **not** spend another run on synthetic cadence algebra.

**E002-371 empirical validation:** **NOT ACHIEVED**. **Hush PR #45:** not modified.
