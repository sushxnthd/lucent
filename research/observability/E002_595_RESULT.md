# E002-595 | Source-bound high-rate/ordinary-rate paired anatomical review instrument

Date: 2026-11-02. Primary kernel E002-371. Frozen *before* authentic source execution in [E002_595_FROZEN.md](E002_595_FROZEN.md).

## New exact prospective design result

A nominal 95-fps to 30-fps **point-sampling** conversion has three distinct one-native-frame-offset phases on each 19-frame review window:

| Nominal phase | Selected 95-fps native frame indices | Frames retained |
|---|---|---:|
| 0/95 s | 0,3,6,10,13,16 | 6/19 |
| 1/95 s | 1,4,7,11,14,17 | 6/19 |
| 2/95 s | 2,5,8,12,15,18 | 6/19 |

The union covers 18 of 19 indices; **native index 9 is absent from all three phase samples**. In the *synthetic index-only* pulse model, the counts of possible starting positions missed by each phase are:

| Consecutive native-frame pulse width | Phase 0 | Phase 1 | Phase 2 |
|---|---:|---:|---:|
| 1 | 13 | 13 | 13 |
| 2 | 7 | 6 | 7 |
| 3 | 1 | 1 | 1 |
| 4 | 0 | 0 | 0 |

These counts are exact combinatorial predictions, **not empirical human blink statistics**. They cannot certify visibility of a continuous-time blink, because both 95-fps and nominal 30-fps frames are temporally integrated, actual LPW shutter/clock calibration is absent, and a pulse defined over native frame indices is not an anatomical event. A 4-index pulse being present in a point sample is not proof that the camera sees a real eyelid closure.

## New human-validation artifact

[Executable](e002_595_lpw_phase_pair.py) creates two source-bound, blinded native 95-fps reviewer packets (10 x 19 PNGs per reviewer) using the already verified E002-578 LPW **development-only** selection. It then creates three nominal 30-fps phase arms per reviewer (10 x 6 PNGs per phase per reviewer). Every low-rate PNG is checked against the corresponding original native-frame SHA-256 and 640x480 geometry. Reviewer templates are blank and omit participant, source-video and native-index mapping. All images, video and owner mappings are confined to a temporary directory destroyed before completion. No private source artifacts are uploaded.

The independent [Node.js BigInt replay](e002_595_independent_replay.cjs) recomputes the phase grids and all pulse-miss counts without importing Python results. A [dedicated GitHub Actions workflow](../../.github/workflows/e002_595_lpw_phase_pair.yml) executes the source-bound test and checks cleanup. The exact index predictions were checked in a local Python harness; **the real-source execution and hosted CI success are not claimed until the workflow finishes and its logs are inspected**.

[Hosted run](https://github.com/sushxnthd/lucent/actions/runs/41345483680) was queued when initially inspected, before the final script fix. Subsequent push-triggered runs must be checked at their actual head SHA.

## Next physical and human experiment

Secure two genuinely independent, blinded anatomical raters; privately distribute authorized source-bound packets; require upper/lower lid margin intervals, visibility and explicit nuisance flags. Seal native-rate annotations before comparing phase arms. Do not infer eyelid closure from pupil-center absence or brightness proxies. Keep participant 1 strictly in development; only after model/premise freeze may a disjoint participant holdout be accessed. Then pair with a **separate physical-camera** study: synchronized high-speed and ordinary cameras, independently calibrated exposure/rolling timing and radiometric transfer, clock/geometry errors, and independently justified continuous-time velocity/acceleration bounds. Precommit each gap's E002-371 prediction before opening held-out anatomical labels; any reference-confirmed closure in a predicted exclusion gap falsifies that certificate or a premise.

## Evidence and release gates

- **Established now:** exact phase-index law; runnable source-bound paired-review instrument; independent oracle; frozen human/physical follow-up protocol.
- **Pending hosted verification:** actual source packet construction, hash binding, cleanup and hosted independent replay.
- **Still zero:** independent human rater pairs, human closure labels, physical shutter/clock certificates, defensible hard human velocity ceilings and participant-disjoint physical exclusion predictions.
- **Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. **Draft PR #26:** unmerged. **Hush:** separate branch/PR #45 untouched in this urgent primary run.
