# E002-659 | Saturation makes pulse-phase shutter calibration non-identifiable

**Evidence tier:** deterministic exact-rational synthetic adversarial instrument model. No human, camera, or independent experimental evidence.

## New falsification

The E002-658 phase scan assumes a linear unsaturated brightness response. In E002-659, a 20-phase scan of a rectangular shutter and an early-only shutter yields **identical clipped observations** when the detector baseline is already at its saturation ceiling. The normalized shutter kernel is therefore not identifiable from those observations, even though the kernels imply different temporal uncertainty moments. The test explicitly returns no estimate rather than dividing by zero or silently using a rectangular kernel.

For the held-out V=4 synthetic aperture a(t)=0.20+4|t| over a 0.20-second exposure, early-only weighting gives exposure average 0.50. Incorrect rectangular moment correction gives lower bound 0.30 and falsely certifies open at threshold 0.28. Correct early-only correction gives 0.20 and abstains. The actual continuous minimum is 0.20.

## Reproduction

Run `python3 research/observability/e002_659_saturation.py`. Uses Python standard library Fraction, no dependencies. Assertions cover unsaturated recovery, indistinguishable saturated scans, explicit calibration refusal, and erroneous versus corrected certificates. **Execution in hosted CI and independent replay are not yet verified.**

## Consequence and physical falsification

A phase scan is admissible only if its detector response is shown unsaturated over the full relevant brightness and pulse-width range, with an independently measured dark/baseline response and a linearity check. Repeat at multiple gains/exposure settings and reserve unseen phase/amplitude combinations. Any clipped or non-identifiable calibration requires conservative worst-case kernel uncertainty or `ABSTAIN_UNCALIBRATED`; production remains `BLOCKED`.

This is an adversarial counterexample to a calibration assumption, not a validated model of any particular phone camera.
