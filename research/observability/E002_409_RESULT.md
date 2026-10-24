# E002-409 — untouched S06 human-video transfer: frozen glare hypothesis FAILS

**Date:** 2026-10-24. **Evidence tier:** preregistered held-out *human video* with digitally imposed nuisance; EEG blink-marker association, **not** independently measured eyelid aperture or physical shutter-gap validation.

## Protocol and persistence

The [frozen protocol](E002_409_FROZEN.md) was committed as `dd49a10d` before acquiring or evaluating S06. The pre-existing E002-397 Farneback motion feature, ROI, p80 statistic, control offsets, and five nuisance thresholds were not changed. S06 was a previously unused participant, and the source `S06.zip` from [Zenodo record 18978288](https://zenodo.org/records/18978288) passed the preregistered MD5 `8217203472f7393b03aa56102dbc9adc`.

[GitHub Actions run 40054196182](https://github.com/sushxnthd/lucent/actions/runs/40054196182) **completed successfully** at head `0db991200fae35681397b18edaac13f6286267d4`. The real-human job independently recomputed AUCs and Boolean gates using `e002_409_independent_check.py`, which does not import the primary AUC function. The separate synthetic corruption oracle passed. **CI success is a computational result, not a scientific PASS.**

The 14-day anonymous score artifact is [artifact 12544736676](https://github.com/sushxnthd/lucent/actions/runs/40054196182/artifacts/12544736676), SHA-256 ZIP digest `0e5c224483798ee1f720a0f80e233882f3afe4fee082cda3742057044955594a`. The artifact contains aggregate results and per-pair anonymous scalar scores only; no eye images, raw video, EEG event times, or frame IDs.

## Frozen outcomes on 144 human event/control windows

| Fixed input condition | Rank AUC | Change in AUC from clean | Frozen decision |
| --- | ---: | ---: | --- |
| Clean | **0.877701** | — | H1 **PASS**, ≥0.70 |
| Gaussian blur σ=2 | 0.868393 | −0.009307 | H2 **PASS**, loss ≤0.10 |
| Fixed rectangular white glare | **0.375868** | **−0.501833** | H3 **FAIL**, loss >0.10 |
| Gain ×0.70 | 0.884066 | +0.006366 | H4 **PASS** |
| Gain ×1.30 | 0.875241 | −0.002459 | H4 **PASS** |
| Whole-frame translation (+8,+6) px | 0.880980 | +0.003279 | H5 **PASS** |

**Frozen joint decision: FAIL (4 of 5 hypotheses passed).** The white-glare condition reverses useful event/control discrimination to AUC 0.376. This is not a claim that 50.18% of individual blinks were misclassified: AUC is a rank statistic over positive and control score distributions. No per-event clinical or physical error rate was estimated.

The human-video nuisance perturbations are digitally constructed and do **not** estimate real-world glare prevalence. Controls were defined by EEG marker separation, not adjudicated physical nonblink status. Windows are repeated observations within **one** participant, not 144 independent people. No population confidence claim is warranted.

## Falsification and product consequence

The previously frozen decision rule states that **any** realistic nuisance failure rejects E002-397 image-motion energy as a transferable physical-aperture/closure observable. **Enforce that decision:** classify the feature as **REJECTED_FOR_PRODUCT_CLOSURE**; allow only research-only, optics-qualified EEG-event-motion association. Do not promote it to a blink detector, eyelid-velocity estimator, hidden-closure certificate, blink-duration estimator, PERCLOS input, or fatigue measure. Preserve `ABSTAIN_UNCALIBRATED` on those outputs. Do not tune a glare-specific feature on S06 and relabel it a successful untouched-participant replication.

This held-out failure independently reinforces the earlier S01 glare failure (E002-397) while S19 previously exhibited a strong blur failure. Clean-condition association on S06 is genuine evidence about the frozen surrogate's EEG-marker correlation **under this dataset's acquisition**, but it is not physical aperture evidence.

## Remaining decisive E002-371 experiment

Complete two independent blinded E002-407 full-event human landmark sheets and E002-408 adjudication; independently measure reference camera exposure kernel, rolling-shutter row offsets, camera-clock uncertainty, geometry and optical inversion error. Establish a justified velocity envelope independent of the evaluation trajectories; a finite calibration maximum is **not** a deterministic physical bound (E002-405). Freeze ordinary-camera hidden-closure predictions before exposing high-speed reference labels, include nuisance strata (gaze, glasses, glare, blur, brightness, missing frames, camera timing), and count wrong certificates **separately** from abstentions. If deterministic velocity bounds cannot be defended, downgrade to a calibrated statistical-risk claim rather than falsely certifying closure exclusion.

**World-class completion gate remains unmet.** No physical human aperture trajectories, validated hard velocity bounds, prospective unseen-device closure predictions or independently calibrated shutter measurements have been obtained.
