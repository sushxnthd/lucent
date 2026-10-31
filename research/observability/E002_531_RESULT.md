# E002-531 RESULT | A 400-Hz human-marker processing pipeline can erase a closure witness inside an interpolated tracking gap

2026-10-29. Primary Lucent E002-371 observability kernel. Existing branch `research/observability-human-boundary`; draft PR #26. **Evidence tier: exact synthetic instrument-pipeline falsification, anchored to a published real human acquisition method. NOT an experiment on the paper's participants.**

## Why this test is scientifically necessary

Kim et al., *PNAS* (2025), DOI [10.1073/pnas.2508058122](https://doi.org/10.1073/pnas.2508058122), acquired eyelid margin marker trajectories at **400 frames/s** with Vicon cameras, separately recorded **120-fps** HD video, and report linear interpolation of tracking gaps shorter than 10 native samples (25 ms), followed by 10x linear upsampling and 20-Hz zero-lag low-pass filtering. See [primary methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC12358864/). Their 2026 FaceBase release [88-28BJ](https://doi.org/10.25550/88-28BJ) provides a credible future source of human trajectories but is **restricted-access**, not a freely downloadable raw dataset. [FaceBase release notice, September 1, 2026](https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/) explicitly requires an approved human-data access process (General Research Use, Not-for-profit Use Only). We did not obtain access or inspect subject files.

This exposes a practical validation risk: if an independent high-speed *reference* is processed with gap-filling before labeling, its apparent open frames may be imputed rather than actually observed. Treating such imputed frames as verified negatives can invalidate Lucent's E002-371 falsification study.

## Prospective provenance

The [frozen protocol](E002_531_FROZEN.md) was committed at `9394752a` before implementation. It initially misstated a crossing-time duration; [Amendment A](E002_531_AMENDMENT_A.md), committed at `1143794` **before executable construction**, transparently corrects the arithmetic from 9.375 ms to **6.25 ms** without changing the input trajectory or decision rules. No human data were used for this correction.

## Exact synthetic counterexample

A and B are two 400-Hz native-marker worlds, both open (`a=1`) at all observed timestamps. Nine consecutive native frames, indices 30..38, are missing. Their observed bracketing samples at indices 29 and 39 are both `1`, separated by **25 ms**. The nine missing sample positions span **22.5 ms**.

- World A is open throughout.
- World B has missing-frame apertures `0.8,0.6,0.4,0.2,0,0.2,0.4,0.6,0.8`, and is otherwise identical to A. Threshold is `c=0.25`.
- World B has **three actual native threshold witnesses** (indices 33, 34, 35), **6.25 ms** of continuous piecewise-linear below-threshold dwell, and hypothetical maximum sampled-segment slope **80 normalized units/s**. This is *not* a certified human eyelid-speed ceiling.
- Both worlds have **identical observed samples and missingness masks**. Linear interpolation between observed open brackets reconstructs all nine missing frames as open. Therefore both yield identical filled series and necessarily identical results under *any deterministic downstream interpolation/filtering*. This is exact non-identifiability, not a claim about a particular filter implementation.
- An independent 25-fps point-sampling surrogate (16 native samples per step) observes **zero** closed samples at phase 0 and **one** at phase 1 in complete world B. After gap filling, both phases show **zero**. This is not a shutter-integrated 25-fps camera test.

| Quantity | World A | World B (complete) | World B after interpolation |
| --- | ---: | ---: | ---: |
| Native closed samples | 0 | 3 | 0 |
| Below-c dwell (piecewise linear) | 0 | 6.25 ms | 0 |
| 25-fps phase 0 witnesses | 0 | 0 | 0 |
| 25-fps phase 1 witnesses | 0 | 1 | 0 |
| Observable reference data | Identical | Identical | Identical |

**Direct inference:** a reference-camera negative inferred solely from interpolated high-speed marker samples is not independently validated ground truth for the missing interval. The correct decision is `UNKNOWN_MISSING_NATIVE`. If a native positive is actually observed, a `POSITIVE_NATIVE_WITNESS` may be emitted subject to anatomical calibration. Even a fully observed sampled sequence without positive witnesses does not certify absence of continuous-time threshold crossings.

## Verification and negative controls

- [Exact-rational Python simulator](e002_531_native_missingness.py) and [11 adversarial unit tests](test_e002_531_native_missingness.py), **all 11 passed locally** on 2026-10-29.
- [Independent Node.js replay](e002_531_independent_replay.cjs) passed locally, reproducing the 3-frame witness, 6.25-ms dwell, phase reversal and indistinguishability. An initial local Node exact-equality assertion on binary floating-point slope produced `80.00000000000003` rather than 80; the replay was corrected to compute the slope from integer fifths, then passed. This was a software numeric representation issue, not a scientific counterexample.
- Negative control: making central frame 34 observed reveals the closure in B but not A. Boundary-unbracketed missing data are refused. All-abstain/absence certification is not claimed.
- [Dedicated hosted CI](../../.github/workflows/e002_531_native_missingness.yml) is committed; hosted status must be checked separately. No hosted success is assumed.

## Concrete prospective human-validation protocol

**Restricted raw data:** obtain explicit FaceBase access approval before downloading any participant material. If approved, checksum and retain the original 400-Hz pre-interpolation marker streams and native tracking-validity masks privately. Do not publish restricted subject data or identifiable imagery. Use participant-disjoint exploratory subjects 1..6 versus held-out subjects 7..8 only if dataset structure permits; otherwise preregister a replacement before inspecting outcome values. Evaluate spontaneous, voluntary and reflexive blinks separately, retaining all censored intervals and missingness strata.

**Reconstruction:** derive central upper-eyelid displacement in the face-attached frame and normalize to per-subject open/soft-closure reference only if required markers and calibration are available. Separate this marker-motion proxy from true upper/lower anatomical aperture; do not silently equate them. Label native positive threshold witnesses, interpolated unknowns and observed no-witness spans distinctly. Report sample cadence and missingness before any 10x upsampling/20-Hz filtering. Simulate 25/30-fps point-sampling phase sweeps as *sampling surrogates* and compare to the native 400-Hz positives; never treat them as calibrated physical shutter predictions.

**Physical follow-up:** two independent blinded anatomical raters on native video, independently measured exposure/shutter/clock response and independently supported continuous-time speed assumptions are still needed for Lucent's E002-371 exclusion claims. The published Vicon processing and the 120-fps video do not provide those calibrations.

## Claim and release consequences

**Allowed research claim:** finite missing native reference intervals can contain an unobserved threshold closure, and deterministic interpolation cannot recover the distinction; reference absence across such spans must be censored. This is a known mathematical identifiability phenomenon demonstrated in a relevant instrument configuration, **not** a new general theorem or empirical discovery of hidden human blinks.

**Rejected claims:** any population blink sensitivity, hard continuous-time speed ceiling, fatigue inference, PERCLOS accuracy, physical shutter timing, or deployment readiness.

Lucent: `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Independent blinded human anatomical ratings **0**; authenticated physical shutter/clock measurements **0**; certified human speed ceilings **0**; held-out physical predictions **0**. Hush PR #45 untouched.

## Relationship to earlier E002-432 (novelty guard)

[E002-432](E002_432_RESULT.md) already proved a **different missing-frame failure**: dropping an ordinary-camera exposure and compressing timestamps can falsely certify a no-closure gap. E002-531 does **not** rediscover the general missing-data theorem. Its distinct target is **high-speed reference-ground-truth construction**: a real published 400-Hz human marker pipeline fills sub-25-ms tracking gaps before filtering, and this exact counterexample proves why a *reference* absence derived from those imputed intervals cannot falsify a predicted hidden closure. The new empirical next step is obtaining approved **pre-interpolation 400-Hz native markers**, not running another generic missingness sweep. No new human data or physical measurements were obtained.
