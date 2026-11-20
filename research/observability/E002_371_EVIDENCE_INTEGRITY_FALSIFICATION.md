# E002-371 held-out evaluator: audit of evidence-integrity gaps (2026-11-17)

## New falsification / product consequence

The current held-out evaluator accepts a CSV containing only held-out rows and returns `NOT_VALIDATED_BY_ZERO_ERRORS` when there are no false exclusions. It also accepts repeated rows with identical subject and sequence identifiers. Thus an apparently large held-out decision count may be produced by duplicated evidence, and participant-disjointness is checked only among rows actually supplied, not against an authenticated calibration registry. A self-declared `reference_quality_ok=1` is not an independent reference audit.

These are evidence-integrity failure modes, not a failure of the E002-371 mathematical boundary. Until repaired, no numerical validation summary from this evaluator should be treated as independently adjudicated human evidence.

## Required regression cases

1. Held-out-only CSV: reject with a missing-calibration-evidence error.
2. Calibration-only CSV: reject with a missing-held-out-evidence error.
3. Duplicate `(subject_id, sequence_id)` rows: reject even if both labels agree.
4. Blank sequence identifier: reject.
5. Valid calibration and held-out rows with distinct participants and sequences: evaluate but preserve `NOT_VALIDATED_BY_ZERO_ERRORS` status.
6. Calibration registry from outside the CSV: verify provenance and participant exclusions independently; otherwise remain blocked.

## Release consequence

Camera-derived fatigue inference stays disabled. The current self-attested CSV schema is not an evidence-backed physiological calibration interface. Do not convert its zero-error outcome into a release gate pass. This document records a newly identified evaluator falsification; fixes and executed regressions remain outstanding.
