# E002-425 — off-grid optical pulse excitation identifies a finite shutter surrogate, but timing error defeats its physical interpretation

**Date:** 2026-10-25. **Frozen first:** E002_425_FROZEN.md, commit `6040dd79284515e4ca73d800628e2c90e3e01f05`. **Evidence tier:** synthetic, exact finite-dimensional optical pulse inverse problem plus an exploratory clock-mismatch falsification. **No** real camera, photodiode, physical eyelid, independently blinded human rating or physiological speed bound.

## Decisive question and result

E002-424 constructed a shutter-response alias that survived every fixed-width, grid-aligned LED calibration pulse. This run asks whether changing the optical excitation protocol actually removes that *specific* alias at a declared 0.05-ms kernel resolution, and whether a good pulse holdout score suffices under inaccurate pulse timing.

**Yes for the finite-bin inverse problem; no for physical certification.** With 48 nonnegative shutter-bin masses summing to one, the 35 legacy 0.50-ms pulses at 0.10-ms starts yield matrix rank **24/48**, and the uniform/alternating shutter worlds are indistinguishable to <4e-16. In contrast, the 256 frozen off-grid, multiwidth calibration pulses yield rank **48/48**, minimum singular value **0.4950**, and condition number **36.61**. The untouched 128-pulse set separates the same two kernels by up to **0.01943** in normalized response. This is a finite-resolution, assumed-known-pulse result, not universal shutter-kernel identification.

## Frozen outcomes

| Preregistered test | Result | Decision |
|---|---:|---|
| H1: original-grid rank deficiency and exact alias | rank 24; max difference 3.61e-16 | PASS |
| H2: off-grid/multiwidth training rank | 48 of 48 | PASS |
| H3: maximum held-out alias separation >0.01 | 0.0194297 | PASS |
| H4: noiseless NNLS recovery, L1 <1e-5 and held-out MAE <1e-8 | mass L1 5.66e-15; MAE 1.84e-16 | PASS |
| H5: Gaussian response noise SD=0.0005, mass L1 <0.25 and held-out MAE <0.01 | mass L1 0.00993; MAE 0.000134 | PASS |
| H6: real-world product authorization | false; `ABSTAIN_UNCALIBRATED` | PASS |

The wrong uniform kernel has held-out MAE **0.00724456**, so a permissive <0.01 held-out MAE gate would not reliably reject it. The frozen >0.01 **maximum separation** criterion does detect this particular alias; it must not be conflated with a general noise-robust classifier.

## Exploratory timing-mismatch falsification (not a preregistered gate)

A separately seeded, zero-mean **30-microsecond SD** pulse-start timing error was applied to the 256 *physical* training pulses while the inverse model continued using their nominal starts. The true shutter remained the same alternating kernel. The fitted model then had approximately **0.787** mass L1 error despite a clean held-out MAE of only **0.00516**, which is below 0.01. Its nominal training MAE was approximately **0.00627**. These are synthetic clock errors, not observed hardware behavior.

**Consequences:** Full column rank, an apparently acceptable holdout MAE and nonnegative fitted weights do **not** authenticate a physical shutter response when calibration-pulse timing is wrong. A physical instrument must propagate independently measured pulse start/width uncertainty and report an uncertainty *set* for shutter responses. If that set permits opposite hidden-closure decisions, abstain. This is an illustrative instance of classical errors-in-variables/system-identification failure, not a novel mathematical phenomenon.

## Reproduction and independent checks

Run from repository root (Python 3.11+, NumPy and SciPy):

```bash
python -m unittest -v research/observability/test_e002_425_shutter_identification.py
python research/observability/e002_425_shutter_identification.py
```

The independent test implements direct time-domain midpoint quadrature for selected pulses rather than calling the exact overlap-matrix integrator. It separately checks the legacy nullspace, holdout allocation, frozen predictions, timing mismatch, malformed inputs and product abstention. The dedicated GitHub Actions workflow `e002_425_shutter_identification.yml` runs these checks and saves a **synthetic-only** JSON aggregate. The numerical outcomes above are from a local independent reproduction of the frozen design; hosted final-head CI status must be checked separately.

## Concrete human/hardware validation gate (not completed)

1. **Metrology first:** Obtain a synchronized LED driver, independently measured photodiode pulse waveforms and clock, RAW camera response and an auditable row/exposure-mode calibration. Record randomized off-grid phases, at least three independently measured pulse widths, multiple exposure settings, rows and brightness levels. Freeze separate sessions for training and untouched evaluation. A software-generated pulse schedule or camera metadata alone is insufficient.
2. **Finite resolution is not physical truth:** Compare multiple temporal bin widths, model waveform uncertainty and use an out-of-model shutter family. Report worst-case no-closure decision over all compatible response kernels, including sub-bin variation. Fail closed on unbounded optical/timing uncertainty, saturation, nonlinear HDR and rolling-shutter discrepancies.
3. **Human reference:** Have two genuinely independent blinded raters complete the already available E002-418 qualification and E002-407/408 high-speed human landmark sheets. Preserve every unresolved/occluded frame, independently adjudicate anatomical geometry, and never treat the 632 existing frames or the rejected E002-417 computer-vision proxies as physical aperture ground truth.
4. **Prospective E002-371 predictions:** Freeze a candidate velocity envelope from a separate calibration population and state whether it is a *hard physical bound* or only a statistical bound. On untouched participants/devices, predict ordinary-camera intervals as closure-witnessed, conditional no-closure, or unresolved before inspecting reference events. High-speed reference frames themselves need an adequacy bound; use E002-416 and E002-419 to count unresolved reference intervals against false-certificate uncertainty.
5. **Nuisance and stopping rules:** Cross exposure, illumination, gaze, glasses, blur, occlusion, rolling shutter, missing frames and clock drift. Publish coverage, witnessed failures, unresolved fractions, worst-case false-certificate bounds and participant-level uncertainty. Do not promote a deterministic certificate from a finite observed maximum velocity. Stop and abstain whenever the physical calibration/observer gates fail.

The actual equipment, photodiode measurements, two human rater sheets and independent hard speed bound are **not present**. Further synthetic work cannot fill those missing evidence tiers. No hidden-closure exclusion, blink duration, PERCLOS or fatigue claim is authorized.

## Priority/novelty

The matrix-rank argument and noisy least-squares recovery are classical finite-dimensional inverse-problem and system-identification methods. The novelty claimed here is **only** a preregistered, product-relevant experiment that quantifies how a concrete Lucent calibration alias is removed at a stated finite resolution, while demonstrating a different timing-error failure. The E002-371 physical boundary is still unvalidated.
