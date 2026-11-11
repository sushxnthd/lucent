# E002-633 | Negative adversarial audit of the blinded scorer (2026-11-03)

## Evidence tier
Static adversarial analysis with a committed executable reproducer, not a completed hosted test, human study or physical validation. The exact E002-371 inequality is conditional and is not falsified by these software-input attacks.

## Three counterexamples
Run `python research/observability/e002_633_input_attack.py` from the repository root.

1. **Self-attested calibration:** arbitrary nonempty `calibration_hash` and literal YES flags suffice for EXCLUDE, without any independent proof linking a trial to encoder traces, shutter timing, geometry or uncertainty bounds.
2. **Duplicate CSV headers:** `csv.DictReader` silently overwrites the earlier `independent_velocity_certified=NO` when a second same-named column contains YES. A malformed input can therefore be interpreted as certified.
3. **Duplicate trial IDs:** repeated rows with the same trial ID are scored separately. Counting such rows as independent trials would invalidate binomial confidence claims.

These are software enforcement defects, not observed physiological counterexamples. The reproducer asserts the existing behavior; hosted execution remains pending.

## Direct product consequence
Do not expose EXCLUDE as a production or scientific calibration certificate on the basis of self-attested CSV fields. Require an immutable, independently verified acquisition manifest binding each unique trial ID to raw shutter, encoder and clock traces, calibration procedure and uncertainty envelopes. Reject duplicate headers, duplicate IDs and unsupported schema before scoring; freeze predictions before reference labels are revealed. Report trial/participant clustering rather than treating duplicate acquisitions as independent evidence.

Until independent physical acquisition is obtained and this input-integrity boundary is enforced, retain `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. No new human sequences or instrument recordings were acquired in E002-633. Next work must execute the frozen E002-629/631 physical protocol, not another theoretical refinement.
