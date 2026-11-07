# E002-547 RESULT | A 200-Hz reference can integrate away a true closure

Date: 2026-10-30. Primary E002-371 kernel. [Protocol frozen first](E002_547_FROZEN.md) at commit 0192322, before the executable and oracle were committed. Evidence tier: **exact constructed instrument counterexample**. No acquired camera frames, human eyelid measurements or calibrated shutter response.

## Result: high frame rate is not reference sensitivity

Retain E002-546's **hypothetical** triangular 10-ms aperture trajectory, open b=0.9, true minimum 0, threshold c=0.2, and constructed slope magnitude V=180/s. E002-546 treated reference frames as instantaneous point samples. E002-547 instead models each reference output as the exact linear mean aperture over its exposure interval. This is intentionally an optimistic transfer model; real RGB/ISP/segmentation may be worse.

For an exposure L centered at the triangular minimum and L<=10 ms, the **minimum possible exposure-averaged aperture** is V L/4. Thus a reference frame can reach c only if L<=4c/V=1/225 s=4.444... ms. At the equality, only one phase touches the threshold, giving zero detection probability for continuous uniform random phase. Longer exposures never return a positive under this model, **even though the continuous-time aperture actually reaches zero**.

| Reference fps | Exposure | E002-546 instantaneous detection | E002-547 integrated detection | Best possible integrated mean |
|---:|---:|---:|---:|---:|
| 200 | 4 ms | 4/9 = 44.44% | **4/15 = 26.67%** | 0.18 |
| 240 | 4 ms | 8/15 = 53.33% | **8/25 = 32.00%** | 0.18 |
| 200 | 5 ms | 4/9 = 44.44% | **0%** | 0.225 |
| 100 | 10 ms | 2/9 = 22.22% | **0%** | 0.45 |

For the 4-ms cases, the threshold-positive exposure-center interval is exactly 1/750 s (1.333... ms), not E002-546's point-sample width of 1/450 s (2.222... ms). Under a uniform phase independent of the closure, its sampling probability is min(1, fps/750). In the 5-ms 200-Hz case, *no sampling phase* returns a threshold-positive integrated aperture despite the true crossing. This is an instrument-model falsifier, **not** a measured human false-negative rate.

## Independent checks

- [Exact rational Python primitive and adversarial tests](e002_547_exposure_reference.py) independently evaluate boxcar means, threshold boundaries, symmetry, invalid durations and a separate numerical midpoint quadrature.
- [Independent Node.js BigInt oracle](e002_547_independent.cjs) integrates piecewise-linear aperture by trapezoidal area over independently constructed breakpoints. Its centered means 9/50, 9/40 and 9/20, critical 1/5 and phase fractions 4/15 and 8/25 agree exactly.
- Local execution: both scripts passed on 2026-10-30. The first draft of the independent oracle had a **mistaken test expectation** for an off-center 5-ms mean (expected 53/200; exact independently calculated 241/1000). The expectation was corrected *before* commit; no frozen scientific threshold was changed. This is a test-fixture correction, not evidence of a physical anomaly.
- [Hosted CI workflow](../../.github/workflows/e002-547-exposure-reference.yml) committed; its hosted status must be checked independently.

## Validity and limitations

The result depends on an exact triangular *constructed* trajectory, linear temporal integration of normalized anatomical aperture, no noise, an exactly known exposure length, ideal global shutter and uniform independent phase. A real camera reports brightness/pixels rather than aperture and may have gamma, blur, rolling scan, automatic exposure, segmentation error and timing uncertainty. This construction establishes an **existence counterexample** to the assumption that nominal reference fps suffices. It does not quantify real Silesian5/OpenEDS sensitivity, certify a human velocity ceiling, or establish a new general sampling theorem. The sharp integration calculation is elementary; the scientific contribution is a concrete reference-validity kill test for Lucent's intended validation protocol.

## Product and validation decision

Reference-negative frames, even at 200 Hz, remain REFERENCE_NEGATIVE_UNCERTIFIED unless a separate physically calibrated exposure/transfer model and a continuous-time coverage argument establish sensitivity. A reference-positive observation can be a one-sided falsification witness only after anatomical transfer, shutter timing, and label uncertainty are authenticated. In prospective E002-371 testing, retain negative high-rate clips as **censored**, not closure-free ground truth. Report observed-positive sensitivity separately from negative-label certification.

Next decisive work remains an authorized physical shutter/photodiode acquisition and two independent blinded S01 anatomical raters; use the existing [physical handoff](E002_542_PHYSICAL_HANDOFF.md). No additional synthetic reference threshold tuning is justified without a new instrument or human data source.

**Evidence remaining:** authenticated physical captures 0; independent human anatomical ratings 0; certified continuous-time human speed ceilings 0; participant-disjoint physical predictions 0. Product ABSTAIN_UNCALIBRATED; release BLOCKED. Hush PR #45 untouched.
