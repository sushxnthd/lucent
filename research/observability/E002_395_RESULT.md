# E002-395 — preregistered human image proxy FALSIFIED (2026-10-23)

**Decision:** KILL the fixed dark-pixel closure proxy as a supported Lucent observable. Preserve the failed prediction and do not invert the score sign or retune the ROI on the held-out recordings.

## Evidence and provenance

Frozen before new video evaluation at commit `dda0f078`. Implemented at `a0e42a7`, independently checked at `a885a476`, and executed against the MD5-verified CC0 Eye-BCI S01 public human recording in [GitHub Actions run 39963691304](https://github.com/sushxnthd/lucent/actions/runs/39963691304) (completed **successfully**). Original archive MD5: `fef02cb7ebf62e4f3efb6303284fd6cb`. Public source: Guttmann-Flury et al., *Scientific Data* 12:587 (2025), DOI 10.1038/s41597-025-04861-9. Results artifact ID **12506595116** (expires 2026-11-06; SHA256 `060237f8cd4379f7ee87bb0761994ae3e47d5da58fe09b7359971925748406a0`) contains anonymous per-pair scores, not raw identifiable video.

Source has 53,680 human eye frames and 112 EEG blink markers. Predeclared eligibility yielded **86 event/control pairs**: 19 markers outside usable camera/gap coverage, six previously inspected examples excluded, one without a valid matched control. Chronological first 51 pairs were training; **last 35 pairs were untouched holdout**. The fixed closure-associated feature was `1 - skin-normalized eye dark-pixel fraction`, not measured eyelid aperture. Training-only threshold was **0.7938034**.

## Preregistered test results

| Condition | Held-out ROC AUC | Predeclared status |
| --- | ---: | --- |
| Clean (primary) | **0.2004** | **FAILED** required AUC >= 0.75 |
| Global gain 0.70 | 0.1576 | Failure retained |
| Global gain 1.30 | 0.2016 | Failure retained |
| Brightness +25 | 0.1396 | Failure retained |
| Brightness -25 | 0.2482 | Failure retained |
| Gaussian blur sigma 2 | 0.2000 | Failure retained |
| Glare rectangle | 0.2004 | Failure retained |
| Geometry translation (+8,+6) | 0.2878 | Failure retained |

Clean AUC paired-bootstrap 95% percentile interval: **[0.0881, 0.3543]**, 1,000 paired resamples, fixed seed 371. At the training-only threshold, **33/35 EEG-marker windows flagged** (94.3% sensitivity) but **32/35 nominal non-event controls also flagged** (8.6% specificity). Thus the apparently high event recall is unusable: the feature mostly calls everything closed. The shuffled-label negative control yielded AUC **0.48** (predeclared null criterion passed).

The *relative* brightness degradation criterion technically passed because the already-broken clean AUC left little room to degrade; **this is not a robustness success**. Glare clipped 24.0% of eye ROI pixels at its worst window. All metrics and the training-only threshold were independently recomputed from anonymous scores by `e002_395_independent_check.py` (oracle PASS). CI success denotes reproducibility, **not scientific validation**.

## Interpretation and scientific limits

This is a real, independent held-out **within-one-participant** falsification of a fixed pixel-intensity surrogate for EEG blink-marker association. The inverse rank ordering is not permission to reverse feature direction post hoc. Candidate causes include gaze/geometry, eyelid lashes, skin reference mismatch, brightness, and imperfect EEG/non-event labels; they are **hypotheses**, not established mechanisms. Non-event windows may contain unmarked spontaneous blinks. No physical aperture labels, independently measured shutter exposure, velocity envelope, device holdout, or physiological inference exists. These results neither validate nor falsify E002-371's *conditional physical-aperture theorem*.

## Product and research consequence

1. Mark this specific dark-pixel proxy **REJECTED_E002_395**; do not deploy it for blink detection, PERCLOS, fatigue, physical aperture, or hard no-hidden-closure certificates. Do not optimize it on the 35 held-out pairs.
2. Continue `ABSTAIN_UNCALIBRATED` for all physical/clinical claims. A 0.20 AUC is not a usable reversed classifier without a **new independently frozen experiment on untouched people/devices**.
3. Next scientifically decisive human study: two blinded annotators independently mark upper/lower eyelid boundaries on sampled high-speed frames, report inter-rater uncertainty and unusable frames, acquire measured exposure and an ordinary RGB camera simultaneously, calibrate velocity on disjoint participants, then freeze E002-371 no-hidden-closure predictions on untouched participant/device holdouts. E002-395's fixed proxy is retired, not retuned.

## Reproduction

Run `e002_395_human_proxy.py --archive S01.zip --output results/` and `e002_395_independent_check.py --archive S01.zip --output results/`. CI workflow: `.github/workflows/e002_395_human.yml`. No identifiable imagery or medical diagnosis is committed.
