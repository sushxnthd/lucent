# E002-445 — spatial nuisance counterexample and pending human falsification

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

The hosted human result is **pending** as of this document. Do not infer any human numerical result until the workflow has completed and its aggregate is separately persisted.

## Evidence tier and decision

This report establishes a **synthetic nuisance counterexample** and an executable falsification design, not a new physiological theorem, measured eyelid velocity, calibrated anatomical aperture or physical shutter clock. Eye movement, illumination gradients, blur, glasses, geometry, sampling, clock uncertainty and compression remain unresolved. The candidate synchronization events may be processing timestamps rather than exposure timestamps. S21/S22 remain sealed for participant-disjoint validation.

**E002-371 physical validation: NOT ESTABLISHED. Product: ABSTAIN_UNCALIBRATED.** Do not merge the draft PR or authorize physical hidden-closure, blink duration, PERCLOS, fatigue or medical claims.
