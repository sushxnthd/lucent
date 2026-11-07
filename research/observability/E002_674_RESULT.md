# E002-674 | Adversarial provenance-forgery falsification (2026-11-06 UTC)

**Evidence tier:** executable software-level falsification; no human, physical or independent verification.

## Claim killed

The E002-673 auditor's `eligible` count is **not** evidence of calibration validity. Its three boolean flags and the string `independent_hard_bound` are self-declared by the input producer. The auditor does not verify a numerical velocity ceiling, units, calibration provenance, exposure interval, clock-error interval, or measurement-error bound. Consequently a syntactically compliant record with physically impossible or missing calibration parameters can be counted as eligible. This is a trust-boundary defect, not a counterexample to the mathematical shutter-gap theorem.

## Reproduction and expected result

Run `python research/observability/e002_674_auditor_forgery.py` from repository root. Six adversarial rows (absent velocity; negative velocity; zero velocity/unknown units; negative clock uncertainty; negative exposure; NaN measurement error) are asserted to enter `eligible`. A separately constructed confirmed-positive closure remains a correctly detected false exclusion. This regression intentionally asserts the **current unsafe acceptance**; changing the auditor to reject forged/invalid inputs must change the test into an expected-rejection regression.

## Enforcement consequence

Treat `eligible` as *metadata-screened*, not *physically certified*. Release must fail closed until a trusted, immutable calibration manifest is verified independently of record input: physical units and aperture normalization; strictly positive finite velocity ceiling with externally justified provenance; camera-specific exposure and shutter transfer function; nonnegative finite timestamp/measurement uncertainty; per-frame timing evidence; geometry/blur/occlusion controls; and cryptographic or independently controlled linkage between calibration, capture and evaluation. Missing or invalid values abstain, never count toward coverage. The velocity ceiling must not be inferred from the held-out video or finite differences.

No human evidence or shutter experiment was collected. The product stays `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
