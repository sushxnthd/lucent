# E002-424 — held-out pulse-phase success can hide shutter-kernel aliasing

**Date:** 2026-10-25. **Frozen before implementation:** `E002_424_FROZEN.md`, commit `f8e73777b65bc2e86e79fe313ce35c7c4945296d`. **Evidence tier:** exact synthetic scalar optical-response counterexample with separately implemented midpoint quadrature. **Not** a real camera, photodiode, eyelid measurement or human validation of E002-371.

## Scientific question

E002-423 correctly found that an ideal boxcar shutter can be recovered from a simulated LED phase sweep, including 50 interleaved held-out phases per row. But does a near-zero held-out error *identify* the shutter's within-bin response? **No, not for the fixed pulse-width, grid-aligned experiment.** A second, radically different nonnegative shutter can yield identical responses on every observed phase.

This is a sampling/identifiability counterexample, not a general shutter-inversion theorem or a novel principle of sampling theory.

## Exact construction and results

Both worlds use E=2.4 ms exposure windows centered at 0 and 3.2 ms. The calibration pulses have width 0.50 ms and start at 101 phases from -3.0 to +7.0 ms in 0.10-ms increments. World A uses a uniform boxcar shutter. World B uses a shutter that alternates within each 0.10-ms phase cell between weights (1+0.99)/E and (1-0.99)/E for the first row, and the reversed order for the second row. Both shutters are normalized, strictly positive, and have the same exposure support and nominal row timing. The L1 distance between each pair of response kernels is 0.99; this is not a negligible numerical perturbation.

Every calibration-pulse intersection consists of whole 0.10-ms cells because exposure edges, pulse starts and pulse ends are all grid aligned. The alternating weights integrate to the same area in each cell. Therefore **all 101 pulse measurements are observationally identical**, including all 50 held-out phases per row.

| Frozen test | Result |
|---|---|
| H1: max absolute original-grid LED response difference | row 0: 1.94e-16; row 1: 9.16e-16; **indistinguishable** |
| H1: original E002-423 boxcar fitter | Both worlds fit E=2.4 ms, c=0.0/3.2 ms; held-out RMSE <4e-16 |
| H2: moving aperture, same observed exposure means | Both worlds give (0.281, 0.281), within 1.2e-15 |
| H2: true minimum aperture in world A | **0.201 > 0.20**; always open |
| H2: true minimum aperture in world B | **0.1997625 < 0.20**; hidden threshold crossing |
| H3: 0.45-ms pulse-width rescue | Max row-specific LED response difference **0.020625** > frozen 0.015 |
| H4: shutter normalization and positivity | Passed; minimum shutter weight 0.0041667/ms |
| H5: product claim authorization | **False**; `ABSTAIN_UNCALIBRATED` |

For the aperture experiment, both worlds use a continuous V-shaped scalar physical aperture `a(t)=m+V|t-1.6ms|` with **hypothetical** hard V=0.05/ms (50/s) and threshold 0.20. The uniform shutter world has m=0.201, whereas the subphase-shutter world has m=0.1997625. Both generate the same exposure-weighted aperture observations (0.281, 0.281) and have identical shutter-calibration LED observations. They obey the same speed bound and remain within [0,1]. Thus the E002-422 boxcar-only lower bound would wrongly certify the second world if one substituted a fitted boxcar for the true unmeasured temporal kernel.

The exact mean shift is `alpha*V*cell_width/4 = 0.0012375`. This deliberately probes a near-threshold decision: the example is not evidence of frequent errors on actual cameras or typical human eyelid velocities. The adversarial high-frequency shutter response is **mathematically admissible but not measured as physiologically or technologically typical**.

## Independently checked implementation

`e002_424_subphase_shutter_alias.py` integrates the exact piecewise-constant shutter and piecewise-linear aperture. The separate test oracle computes midpoint quadrature directly from an independently coded shutter evaluator at 0.0005-ms spacing, without calling the exact integrator. Four test groups cover the frozen decisions, optical and aperture quadrature, genuine kernel separation/normalization, malformed inputs and physical abstention.

Run from repository root:

```bash
python -m unittest -v research/observability/test_e002_424_subphase_shutter_alias.py
python research/observability/e002_424_subphase_shutter_alias.py
```

The dedicated CI workflow `e002_424_subphase_shutter_alias.yml` runs the tests, asserts all frozen decisions, and preserves a **synthetic-only** JSON artifact. `E002_424_SYNTHETIC_AGGREGATE.json` records the exact results. The schematic `E002_424_SHUTTER_ALIAS.svg` illustrates the two temporal kernels and indistinguishable measured means. No real human images or private optical traces are distributed.

## Product and physical-study consequence

A fit to fixed-width LED pulses at interleaved grid-aligned phases, even with **zero** held-out error, cannot alone justify a boxcar shutter assumption. An ordinary-camera no-hidden-closure certificate must abstain unless the **effective exposure response kernel** is independently bounded for the relevant sensor row, illumination, RAW response and acquisition mode. E002-423's physical timing requirements remain necessary but are not sufficient if within-bin response structure is left unconstrained.

The 0.45-ms pulse rescue detects *this constructed alias*, not all possible unmodeled kernels. A physical protocol should independently verify pulse widths and optical edges with a photodiode and external clock, randomize off-grid phases, vary pulse widths and exposure settings, test multiple rows and brightness levels, validate linear RAW response, and hold out an independent session/device. Unknown HDR, gain, motion blur, nonlinear intensity, gaze, glasses and image geometry must remain nuisance controls; the shutter experiment does not address anatomical geometry. To bound the actual physical kernel, report uncertainty sets over the full temporal response, not only a point estimate of exposure duration and row center.

Two genuinely independent blinded anatomical landmark annotations, measured eyelid velocity bounds, and prospective unseen-participant predictions are still missing. The human-video surrogate estimators rejected in E002-417 remain rejected. E002-419's unresolved-reference bounds must be used for any later human study. No blink-duration, PERCLOS, fatigue, or physical hidden-closure guarantee is supported.

## Priority and novelty audit

This counterexample uses established temporal sampling and coded-exposure concepts. Relevant prior primary literature includes Paek et al., *Optics Letters* 23, 546–548 (1998), DOI 10.1364/OL.23.000546 (stroboscopic temporal characterization); Gu et al., *ICCP* (2010), DOI 10.1109/ICCPHOT.2010.5585094 (coded rolling shutter); Tendero & Osher, *Research in the Mathematical Sciences* (2016), DOI 10.1186/s40687-015-0051-8 (coded-exposure theory); Dong et al., *Applied Optics* 61, 7838–7845 (2022), DOI 10.1364/AO.468009 (measured rolling-shutter transfer functions); Huai et al., *Optics Letters* 48, 847–850 (2023), DOI 10.1364/OL.474375 (LED panel row timing); and Kurosawa et al., *J. Forensic Sci. Technol.* 29, 135–153 (2024), DOI 10.3408/jafst.875 (physical temporal camera measurement). **Do not claim the aliasing phenomenon, pulse calibration, or inverse-problem nonidentifiability as new.** Lucent's contribution in this run is an executable, product-relevant falsification of a specific insufficient validation protocol.

**Scientific decision:** The synthetic counterexample falsifies sufficiency of the E002-423 fixed-width grid-only pulse protocol for *full shutter-kernel identification*. It does **not** invalidate E002-423's boxcar recovery *under its stated ideal-boxcar model*. E002-371 remains physically unvalidated. The only product decision is `ABSTAIN_UNCALIBRATED`.
