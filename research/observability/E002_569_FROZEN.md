# E002-569 | Frozen release-claim falsification protocol

Date: 2026-10-31. E002-371 remains the sole primary scientific kernel. Existing branch `research/observability-human-boundary`, draft PR #26. This protocol is frozen before implementation or testing.

## Scientific/product question

Can the currently available E002-568 cohort-derived **necessary lower floor** for a hypothetical universal normalized velocity ceiling be accidentally laundered into a **sufficient upper ceiling**, enabling a low-frame-rate claim of no hidden eyelid closure? This is a software claim-boundary falsification, **not** new human anatomy or a novel kinematic theorem.

## Precommitted policy

For all available Lucent evidence as of this protocol, no caller-provided boolean, certificate-looking identifier, source frame-rate string, published cohort speed, or synthetic simulation can authorize any of these claims: `NO_HIDDEN_CLOSURE`, `BLINK_DURATION`, `PERCLOS`, `SLEEPINESS`, `FATIGUE`. These return `ABSTAIN_UNCALIBRATED` even if all optional self-reported validation fields are set to true. The software has no external attestation trust root or human-validated physical calibration. It must never emit `EXCLUDE`, `CERTIFIED`, or a physiological measurement from untrusted inputs.

A separate `ACQUISITION_QUALITY` request may report only non-diagnostic frame-count completeness, never human closure. It must carry `NOT_PHYSIOLOGICALLY_VALIDATED` and `release=BLOCKED`. Nonfinite, boolean-as-number, negative or inconsistent counts are rejected with `INVALID_INPUT`; malformed requests never produce success. Unknown claim types fail closed.

## Adversarial pre-registered cases

1. E002-568's 24.720244/s necessary floor falsely relabeled as a safe upper bound.
2. Nominal 30 fps, zero dropped frames, exact metadata, self-reported calibrated clock/shutter and independent human raters, all true.
3. Two missing 30-Hz frames with plausible hidden closure.
4. Rolling shutter, gaze change, glasses, brightness, blur and unknown timestamp provenance.
5. Negative/boolean/nonintegral/overflow-like frame counts, unknown claim, NaN/Infinity, and impossible observed>expected.
6. Quality-only complete and incomplete frames: report completeness only, no blink or fatigue status.
7. Monotonicity: adding nuisance or missing frames never upgrades a physiological claim.

## Acceptance criteria

- Standard-library-only executable policy in `src/lucent/measurement_claim_gate.py` with immutable typed results.
- Adversarial unit tests run locally and in hosted CI; exact test totals and failures preserved.
- Explicit independent reviewer/hardware gates remain zero and no release-ready claim.
- This experiment is a **product consequence** of the established measurement-science limits, not empirical human validation. Stop software-only iterations after verification and return to independent human anatomical review and physical shutter/clock acquisition.
