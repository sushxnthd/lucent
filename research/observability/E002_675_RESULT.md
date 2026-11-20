# E002-675 — Calibration provenance cannot be authenticated by self-declared JSON

**Evidence tier:** executed local synthetic regression; no human or physical measurement.

## Failure and enforcement
E002-674 demonstrated that the E002-673 evaluator counts certificates with absent or invalid numerical calibration fields as eligible. E002-675 adds a separate, fail-closed screening prototype, not a replacement for the legacy evaluator. It requires finite positive eyelid-velocity bounds with explicit units, nonnegative finite clock and measurement errors, positive exposure, artifact digest shapes, and an explicit independent-verification assertion. Critically, the assertion and hashes are themselves attacker-controlled JSON and do not authenticate the underlying capture or calibration. Consequently **every claimed certificate abstains** until a trusted, externally verified provenance mechanism exists. This is deliberately nonfunctional for certification, rather than falsely promoting metadata into physical evidence.

## Local verification
Command: `python research/observability/e002_675_strict_audit.py --self-test`.
Observed: `E002-675: 8 fail-closed assertions passed; no independent calibration established`.
Six forged-input cases from E002-674 were screened, plus a superficially complete self-attested manifest and an end-to-end abstention check. No hosted CI or independent replay claimed.

## Limitations and next decisive experiment
This prototype intentionally does not calculate E002-371 exclusion decisions, and its all-abstain output cannot demonstrate useful coverage. A trusted acquisition-to-calibration link requires independent optical shutter/clock calibration, capture hashes authenticated outside the submitted JSON, independently justified velocity bounds, and held-out dual-rater anatomical reference labels. Then evaluate false exclusion and abstention coverage using E002-671; a single confirmed false exclusion blocks the corresponding claim. Do not substitute another metadata audit or theorem extension for these measurements.

Product: `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush untouched.