# E002-718 — Evidence-free replay must fail closed

Evidence tier: software enforcement correction; **not** physical or human validation.

## Falsification and repair
E002-717 showed that E002-716 returned `NO_OBSERVED_FALSIFICATION` with no held-out cases, no valid reference labels, or no certified exclusions. The replay evaluator now emits `INSUFFICIENT_EVIDENCE` whenever no reference-valid held-out exclusion exists, unless an observed false exclusion requires `FALSIFIED`. It also counts reference-indeterminate held-out trials as abstentions, even when the mathematical certificate's prerequisites otherwise hold. This is a conservative change in reporting, not a proof of safety.

## Reproduction
Run `python -m unittest research.observability.test_e002_717_empty_evidence` and `python research/observability/e002_716_blinded_replay.py --selftest`. The E002-717 negative controls are expected to pass after the correction. These commands have **not been executed by this run**; GitHub source persistence alone is verified. The result must not be described as CI-tested until execution is confirmed.

## Evidence boundary
A nonzero count of held-out exclusions with zero observed failures is still `NO_OBSERVED_FALSIFICATION`, not `VALIDATED` or `APPROVED`. Required before any product claim: calibrated independent continuous-time velocity bound, synchronized instrument timing, controlled optical aperture measurement, independent reference labels, participant-disjoint human replay, uncertainty intervals, sample-size justification, and predeclared failure threshold. Preserve `ABSTAIN_UNCALIBRATED` and production `BLOCKED`.

## Next experiment
Execute E002-714 instrument acquisition with independently timed occluder and shutter-phase randomization, then blind replay through this gate. Avoid another mathematical-only iteration unless acquisition reveals a concrete falsification.
