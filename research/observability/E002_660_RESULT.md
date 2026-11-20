# E002-660 — Phase-correlated gain confounds shutter-kernel calibration

**Evidence tier:** deterministic synthetic counterexample; locally executed using Python 3 standard library. Not a physical measurement or human validation.

## Falsification

E002-658 uses an LED phase scan to identify temporal shutter weights; E002-659 showed saturation can destroy identifiability. Here even a *linear, unsaturated* sensor does not identify shutter weights when source brightness or detector gain varies with pulse phase. The measured phase response is `y_i = g_i k_i` (up to common scale). Two distinct normalized kernels `k=(1/4,1/4,1/4,1/4)` and `k'=(1/10,1/10,2/5,2/5)` yield identical four-phase measurements with respective gains `g=(1,1,1,1)` and `g'=(5/2,5/2,5/8,5/8)`. All signals are positive and may be rescaled below saturation. A phase scan alone cannot distinguish these worlds.

The dependency-free exact-rational reproduction `e002_660_gain_drift.py` asserts equal observed scans, incorrect rectangular-kernel recovery, and recovery of the asymmetric kernel given an independent simultaneous flat-field gain measurement. It also verifies both kernels remain compatible with bounded but unknown per-phase gains in [1/2,5/2]. Local execution: **PASS**. Independent replay and hosted CI: not yet verified.

## Frozen physical falsification protocol

Use a stable pulse generator and independent photodiode/oscilloscope channel to record incident LED intensity for *every* phase, synchronized to the camera. Acquire interleaved randomized phase order rather than a monotonic sweep. Record exposure, ISO, analog/digital gain, auto-exposure and white-balance settings, raw pixel intensities, black level, sensor saturation flags, and row timing. Compare estimated shutter kernels from (A) camera alone and (B) camera corrected by the independent photodiode/flat-field reference, on held-out phase orders and at two brightness levels. Predeclare calibration refusal if reference channel is absent, if nonlinearity is detected, or if held-out predictions exceed uncertainty envelopes. Do not claim success without raw measurements and timestamp uncertainty.

## Product consequence

A non-saturated LED phase scan is **not** sufficient shutter calibration. Lucent must either independently bound phase-dependent illumination/gain and propagate a set of compatible kernels through the aperture certificate, or abstain. The E002-371 human validation and instrument acquisition remain outstanding. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
