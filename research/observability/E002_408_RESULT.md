# E002-408 — verified blinded two-rater adjudication and camera-clock enforcement

**Date:** 2026-10-24. **Evidence tier:** independently executed **synthetic annotation-instrument controls** plus existing verified real-human acquisition feasibility; **no human landmark ratings or physical-aperture ground truth**.

## Preregistration and verification

The [E002-408 frozen protocol](E002_408_FROZEN.md) was committed at `ed9f9c41` before the analysis implementation and adversarial tests. The dedicated [GitHub Actions run 40052113841](https://github.com/sushxnthd/lucent/actions/runs/40052113841), head `5adcbd66ce9a2bd48459e81e3d00fd726484af38`, **completed successfully**. Python compilation, E002-408 synthetic fixtures, prior E002-407 blinded-packet privacy/integrity regressions, and the E002-399 independent numerical reference checker all passed. Earlier E002-408 CI runs failed because of test assertions/syntax mistakes; those were repaired and retained in commit history before the passing run. The verified report is based only on the final passing run.

## Frozen synthetic results

| Check | Result |
|---|---|
| Complete two-rater fixture frames | 120 |
| Usable pairwise frames | 117 |
| Nuisance-excluded frames (either rater) | 2 |
| Inverted signed-gap frames excluded | 1 |
| Identical rater IDs | Rejected |
| Incomplete rater sheet | Rejected |
| EEG clock passed off as camera clock | Rejected |
| Nonmonotone camera-hardware timestamps | Rejected |
| Incomplete physical calibration | All 4 clips `ABSTAIN_UNCALIBRATED` |
| Exact synthetic physical calibration and timing | 4/4 **conditional** no-crossing reference certificates |
| Empirical finite-sample velocity maximum substituted for hard bound | All 4 clips `ABSTAIN_UNCALIBRATED` |
| Output contains blinded clip IDs | No |
| Real human landmark ratings present | **No** |

The synthetic positive control demonstrates **code-path reachability under asserted exact synthetic physical calibration**; it is not independent authentication of human physical measurements. The output always retains `product: ABSTAIN_UNCALIBRATED` and explicitly disclaims calibration authentication.

## Direct human-validation consequence

E002-407 has now independently executed full-event rater-packet generation for 8 blinded clips / 632 human eye frames from S01/S19 (see `E002_407_RESULT.md`). E002-408 supplies the previously missing deterministic analysis stage: two independent completed local rater sheets can now be checked for completeness, nuisance exclusions, signed-vertical-gap disagreement and optional independently calibrated reference adequacy. The **first genuinely empirical inter-rater agreement result still requires actual human annotations**; no synthetic oracle substitutes for them.

Even after ratings, the Eye-BCI EEG synchronization timestamps do not certify camera exposure timing. An independently verified hardware clock, optical response, eyelid geometry, row timing, shutter kernel and hard physical velocity envelope are required for deterministic E002-371 closure guarantees. A provenance string cannot prove those quantities. If a hard human velocity ceiling is unavailable, future claims must be statistical, explicitly conditioned on assumptions, rather than deterministic.

## Product decision

**No change in allowed physical measurement claims.** Do not enable blink duration, PERCLOS, hidden-closure exclusion or fatigue diagnosis. Retain `ABSTAIN_UNCALIBRATED`; keep Lucent draft PR #25 open pending real blinded rater sheets and untouched-device physical validation.
