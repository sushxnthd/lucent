# E002-445 — spatial nuisance counterexample and completed human spatial falsification

**2026-10-25; S19 pilot only.** [Frozen protocol](E002_445_FROZEN.md), [implementation](e002_445_spatial_falsification.py), [independent adversarial tests](test_e002_445_spatial_falsification.py), [hosted human run](https://github.com/sushxnthd/lucent/actions/runs/40208482955).

## New adversarial instrument result (synthetic, independently calculated)

A central region occupies 25% of a 320×288 image, and its complement 75%. Both images initially have gray value 50 everywhere. The second image changes **only the border** to gray 80; the center stays exactly 50. The signed whole-image difference has median +30. Under an unconditional global-median subtraction, |D-median(D)| produces **30/255 = 0.117647 normalized optical change in the completely unchanged center**, a spurious localized observation. Direct arithmetic and an independent NumPy fixture agree.

| Center metric | Value |
| --- | ---: |
| Actual raw center change | 0 |
| Naive global-median-corrected center change | **0.117647** (false) |
| Conservative min(|D|, |D-median(D)|) center change | **0** |
| Fraction of pixels with changed border | 0.75 |

**Consequence:** The naive brightness-corrected observable is killed. E002-445 uses the conservative per-pixel minimum, amended in the frozen protocol **before executing any E002-445 human analysis**. It cannot create nonzero motion in an unchanged pixel, but it may remove genuine motion and is not a full camera-motion, illumination or anatomical nuisance solution.

## Prospective human S19 experiment

Analyze the first 12,000 decoded frames of the previously MD5-verified S19 AVI and candidate sync events. Compare the fixed central rectangle x=[80,240), y=[72,216) against the complementary border, raw and conservative brightness-adjusted change. For 10–100-ms candidate gaps versus <=10-ms gaps, compute enrichment ratios and central/border contrast. Compare to 512 predetermined circular shifts, reporting a descriptive rank, **not a valid independent p-value**. A screen requires adjusted central enrichment >=1.5, central/border enrichment ratio >=1.5 and observed contrast above the 95th percentile of shifts. Even a positive screen means only localized optical activity under an *unverified* frame-event alignment.

## Human pilot outcome — hosted run 40208482955 passed

The dedicated [hosted run](https://github.com/sushxnthd/lucent/actions/runs/40208482955) **succeeded**, including **13 independent synthetic/adversarial tests** and processing 12,000 real S19 frames. The exact nonidentifying [machine-readable aggregate](E002_445_HUMAN_AGGREGATE.json) is committed, not merely retained as an expiring workflow artifact. The archive was verified against its published MD5/size.

| S19 optical activity measure | Central region enrichment, medium/short gaps | Border enrichment, medium/short gaps | Central/border ratio |
| --- | ---: | ---: | ---: |
| Raw absolute frame difference | **33.918×** | 15.615× | 2.172× |
| Conservative brightness-adjusted difference | **7.277×** | 3.340× | **2.179×** |

There were 11,972 short-gap pairs, **21 medium-gap pairs**, and six >100-ms pairs. The frozen primary adjusted log-contrast was **0.778661**, versus the 95th percentile **0.312924** across 512 predetermined circular shifts. The descriptive rank fraction was **0.003899** (2/513). This is **not a valid hypothesis-test p-value**; circular shifts are not exchangeable under temporal autocorrelation, nonstationarity, and possible gap clustering.

The preregistered **necessary-only spatial screen passed**: adjusted central enrichment exceeded 1.5×, its central/border enrichment ratio exceeded 1.5×, and the observed contrast exceeded the shift-control 95th percentile. Therefore the correct evidence label is **SPATIALLY_LOCALIZED_OPTICAL_ASSOCIATION_UNVERIFIED**. This strengthens the case that candidate 10–100-ms gaps co-occur with *spatially nonuniform* optical changes, but does not establish an eyelid-specific signal. The border also changed 3.34× more during medium gaps, so camera/gaze/lighting/compression nuisance remains substantial.

**No physical E002-371 validation occurred.** A fixed central rectangle is not an anatomical eyelid-aperture annotation. The candidate event/frame alignment remains unverified; neither physical exposure timing nor independent scale/velocity bounds were obtained. Only one already-inspected pilot participant was used; S21/S22 remain sealed. No product claims are released.

## Evidence tier and decision

This report establishes a **synthetic nuisance counterexample** and an executable falsification design, not a new physiological theorem, measured eyelid velocity, calibrated anatomical aperture or physical shutter clock. Eye movement, illumination gradients, blur, glasses, geometry, sampling, clock uncertainty and compression remain unresolved. The candidate synchronization events may be processing timestamps rather than exposure timestamps. S21/S22 remain sealed for participant-disjoint validation.

**E002-371 physical validation: NOT ESTABLISHED. Product: ABSTAIN_UNCALIBRATED.** Do not merge the draft PR or authorize physical hidden-closure, blink duration, PERCLOS, fatigue or medical claims.
