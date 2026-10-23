# E002-396 — unseen-participant transfer: S01 sign reversal does NOT generalize (2026-10-23)

**Scientific result:** All three preregistered transfer predictions **FAILED**. A simple dark-pixel surrogate has sharply different EEG blink-marker association across two real people, and its operating threshold is highly nuisance-sensitive. Do **not** select the favorable subject or invert the feature after seeing these results.

## Frozen protocol and source integrity

Source: CC0 Eye-BCI SSVEP participant **S19**, Zenodo record **21905748**, MD5 `8a16cf12526f7558b4e49926c4bc5e8e`. The pre-data protocol at `5752804` contained an invalid 31-character transcription of the checksum. First attempt [39964528221](https://github.com/sushxnthd/lucent/actions/runs/39964528221) downloaded but failed before **any image analysis**. The error and authoritative checksum correction were transparently committed at `e870aae`, and the unchanged predictions were rerun.

[GitHub Actions run 39964954577](https://github.com/sushxnthd/lucent/actions/runs/39964954577) **completed successfully** with an independent raw-source and rank-statistic checker (PASS). Source selection was lexicographically first paired session `Sess01/SSVEP191bis`, with **56,911 camera frames**, **68 EEG blink markers**, **36 predeclared matched event/control pairs** (32 markers excluded for missing/gap coverage, none excluded for lack of controls). S19 is a participant not used in S01 threshold fitting or feature selection. No raw identifiable imagery was committed.

The same fixed image ROI, skin normalization, seven-frame max score and S01 training-only threshold **0.7938034188034189** were transferred without fitting.

## Frozen predictions and exact outcomes

| Hypothesis frozen before S19 | Result | Decision |
| --- | --- | --- |
| H1: inverse of S01 event-level score gives AUC >= 0.75 | **0.0733** | **FAILED** |
| H2: original score AUC < 0.50 | **0.9267** | **FAILED** |
| H3: frozen S01 threshold specificity <= 0.50 | **0.9444** | **FAILED** |

On S19 the original score separates EEG-marker windows from nominal controls in the *opposite direction* to S01 (S01 held-out AUC **0.2004**; S19 AUC **0.9267**). The S19 positive AUC was **not** a preregistered success hypothesis and is **not** a transferable measurement guarantee. With the unchanged S01 threshold, S19 had **25/36 marker windows flagged** (69.4% sensitivity) and **34/36 controls rejected** (94.4% specificity).

### Nuisance fragility of the frozen operating threshold

| S19 condition | Direct AUC | Sensitivity | Specificity |
| --- | ---: | ---: | ---: |
| Clean | 0.9267 | 69.4% | 94.4% |
| Gain 0.70 | 0.8978 | 94.4% | **52.8%** |
| Gain 1.30 | 0.9144 | **33.3%** | 97.2% |
| Brightness +25 | 0.9429 | 80.6% | 94.4% |
| Brightness -25 | 0.7932 | 75.0% | 77.8% |
| Blur sigma 2 | 0.9306 | 75.0% | 91.7% |
| Glare rectangle | 0.9120 | 100% | **47.2%** |
| Translation (+8,+6) px | 0.8403 | **36.1%** | 94.4% |

The contrast between sometimes strong *ranking AUC* and unstable *thresholded decisions* is directly relevant to product claims. In particular, glare produces 19/36 false positive controls and a gain increase produces 24/36 missed EEG marker windows. These are **synthetically transformed real human frames**, not naturalistic nuisance frequencies or population risk estimates.

## Evidence limitations

The two participants are not a powered cross-person sample, and event labels are EEG blink-marker timestamps rather than physical eyelid aperture. Control windows may contain unmarked blinks. The frame acquisition clock, shutter exposure, optical transfer, physical velocity envelope, camera identity and unseen-device behavior are not independently calibrated. Neither S01 nor S19 validates E002-371's sharp physical shutter-gap theorem. We cannot infer the *cause* of the sign reversal without blinded physical eyelid annotations and nuisance-controlled acquisition.

## Product consequence and next falsification

- **Retain REJECTED_E002_395** for the unqualified dark-pixel observable. S19's favorable AUC cannot resurrect it: its direction is nonportable and its threshold fails realistic gain/glare/translation controls.
- **Continue ABSTAIN_UNCALIBRATED** for blink duration, PERCLOS, hidden-closure certificates, fatigue diagnosis and any safety-critical decision.
- Next: obtain synchronized ordinary RGB and high-speed reference **with measured shutter/exposure**, blinded independently annotated eyelid aperture and independent velocity envelopes, and freeze predicted no-hidden-closure/abstention decisions on untouched participants/devices. Until then, the exact theorem is a *conditional mathematical result*, not a validated human product measurement.

## Reproduction

`research/observability/E002_396_FROZEN.md`, `E002_396_PREDATA_CLARIFICATION.md`, `E002_396_PREDATA_SOURCE_CORRECTION.md`, `e002_396_unseen_s19.py`, `e002_396_independent_check.py`, and `.github/workflows/e002_396_human.yml`. Anonymous score artifact ID **12506996600** (expires 2026-11-06), SHA256 `708bfc0e098034916003d02a2f2130534cad753bf0270f5027313d1781496641`. No raw human imagery is in the artifact.
