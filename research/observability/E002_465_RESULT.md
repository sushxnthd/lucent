# E002-465 — shutter timing is not identified by an LED photodiode and common trigger

**Date:** 2026-10-26. **Evidence tier:** frozen synthetic optical-instrument falsification plus independent exact-rational verification; **0 physical acquisitions and 0 new human anatomical labels**. [Frozen protocol](E002_465_FROZEN.md) committed first at `975859fbda123a914c9f3828444022b6dbdddc21`. No new theorem or physiological claim.

## The decisive measurement-model failure

The physical handoffs in E002-461/463/464 call for a photodiode and shared trigger to establish exposure timing. That combination measures **illumination and triggering**, not necessarily the imaging sensor's actual light-integration window. A camera may have unknown exposure-start latency, rolling-row delay, internal buffering, or gain control.

Two explicitly constructed shutter worlds use identical triggers, LED/photodiode signals and constant-scene camera intensities. World A has exposure windows [0,0.40] and [2.00,2.40] ms. World B has [0.20,0.60] and [2.20,2.60] ms. A physical crossing at 0.50 ms lies strictly inside A's unexposed gap but inside B's first exposure. Therefore those external signals alone cannot establish whether the reference crossing is in the *camera's* dark gap. A wrong shutter assumption can corrupt an apparent E002-371 falsification or exclusion.

**Direct enforcement consequence:** `SHUTTER_UNIDENTIFIED` for trigger/photodiode-only metadata. Physical `EXCLUDED_CONDITIONALLY` remains blocked until the actual imaging-path exposure response is independently characterized, including clock/row uncertainty.

## Discriminating intervention

An independently timed narrow optical pulse is scanned across phase and observed in the camera's raw imaging signal. Under an **ideal noiseless, linear, uniform, global shutter**, the response to a pulse [t,t+p] is `overlap([a,b],[t,t+p])/(b-a)`. The positive-response phase support is `(a-p,b)`. For scan step h, a bracketed first positive phase f with previous zero z yields `a in [z+p,f+p]`; a last positive phase l and next zero z' yield `b in [l,z']`. Floating-point replay adds outward numerical slack of 1e-10 ms, **not** physical uncertainty.

Frozen p=0.10 ms and h=0.05 ms separate the two worlds. JS numeric bracket examples (ms):
- A start approximately [0.000,0.050], end [0.350,0.400].
- B start approximately [0.200,0.250], end [0.550,0.600].

An independent Python `fractions.Fraction` implementation reproduced the analytic phase brackets with exact rational arithmetic. The JS evaluator also passed a local frozen-case assertion and fail-closed checks. Twelve Node adversarial tests and a dedicated hosted CI workflow were committed; **hosted pass remains unverified until GitHub reports completion**. This is a one-counterexample instrument challenge, not a large synthetic benchmark.

## Executable physical acquisition protocol (not yet executed)

1. **Optical pulse path:** Use a borrowed pulse generator/LED driver and a separate calibrated photodiode/oscilloscope channel to log the *actual emitted light*, not merely the command TTL. Measure optical pulse width, tail, phase jitter and independent clock offset. Ensure pulses are visible to the camera imaging sensor; a photodiode that only observes the LED cannot identify the shutter.
2. **Camera path:** Lock gain, exposure, frame rate and focus. Record RAW or verified linear sensor values with dark-frame subtraction, a static target and an unsaturated ROI. For rolling shutter, scan multiple rows independently. Record frame loss, camera thermal/gain drift, nonlinear response and per-row latency.
3. **Calibration and holdout:** On development runs, scan pulse phases covering the full frame interval with phase step smaller than the expected shutter-edge uncertainty. Repeat each phase under multiple pulse intensities and widths. Fit a forward optical convolution model, quantify noise, censoring, finite pulse tails and relative clock error. Seal its predicted exposure supports and uncertainty *before* opening held-out phase/row/gain recordings.
4. **Independent falsification:** A held-out pulse with authenticated time and reliably detected imaging-path response outside the claimed shutter support falsifies the claimed support. A non-detection cannot certify zero overlap unless a separately justified sensitivity bound excludes undetected low-energy tails. Unbounded temporal tails, clipping, automatic gain, clock uncertainty or model mismatch force abstention.
5. **Escrowed evidence:** Preserve raw photodiode/oscilloscope and raw camera files with SHA-256 hashes, calibration artifacts, device identifiers, pre-unblinding manifest timestamp, holdout split and independent review. Publish deidentified coverage, support-width uncertainty, false support exclusions and abstention by row, gain, phase and brightness. Do not publish invented hardware measurements.
6. **Anatomical follow-up:** Only after shutter/encoder dynamic calibration, perform the sealed E002-456 participant-disjoint eyelid study with independently annotated physical geometry and velocity-bound assumptions. Even a successful bench scan cannot turn observed blink-velocity maxima into hard physiological limits.

**Crucial limitation:** A positive/zero transition rule from the ideal simulator is **not a field-ready physical estimator**. With any unbounded optical/electronic tail or nonzero detection floor, exact support is not identifiable without a justified bound on undetected signal. The code deliberately refuses these cases rather than using the synthetic bracket as a real certificate.

## Files and product gate

- [Ideal shutter simulator and abstaining inference](e002_465_shutter_phase_scan.mjs).
- [Twelve adversarial tests](test_e002_465_shutter_phase_scan.mjs).
- [Independent exact-rational replay](e002_465_independent_replay.py).
- [Dedicated workflow](../../.github/workflows/e002_465_shutter_identifiability.yml).

**Scientific status:** elementary shutter-support identifiability counterexample; stronger prospective physical measurement protocol; no physical or human validation. **E002-371 remains NOT PHYSICALLY VALIDATED**. No physical hidden-closure, blink duration, PERCLOS, fatigue or medical claim; `ABSTAIN_UNCALIBRATED`. S21/S22 sealed. Draft PR #26 unmerged; Hush PR #45 separate. No purchases, deployments or merges.
