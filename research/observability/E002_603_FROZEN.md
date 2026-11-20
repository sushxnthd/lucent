# E002-603 | Frozen private-answer challenge repair after E002-602

Date: 2026-11-02. Parent E002-371. Freeze before implementing a replacement challenge. Evidence tier: SYNTHETIC_INSTRUMENT_REPAIR_ONLY.

## Failure being repaired

E002-602 predicts that the public E002-600 constants reveal the full closure/nuisance answer schedule, allowing a no-image reviewer to qualify under the E002-601 balanced gate. Do not modify the historical fixed challenge or silently rewrite the prior negative results.

## Replacement instrument contract

1. Preserve the existing 190-frame, 10-clip, 19-frame/clip shape, 100-px synthetic iris and 20-px closure threshold for compatibility with the actual offline reviewer and independent grader.
2. Generate a *private-seed-dependent* permutation of six clean and four nuisance clips; the nuisance type is private-seed-dependent too. Select exactly 11 closed clean-frame indices from 114 clean frames, with at least one closed index per clean clip. Vary eyelid upper position and slope by private seed. All generated images must agree with owner-only truth.
3. Never publish the human-study seed, answer schedule, images, or reviewer exports. Public CI fixtures and any public test seeds are development-only and MUST NOT be used to qualify real raters.
4. Require a private manifest with source-frame SHA-256; the owner must verify all image bytes before distributing packets and before grading. Prevent overwriting a nonempty destination. No network upload or GitHub artifacts containing generated data.
5. In independent local tests, distinct private seeds must yield different nuisance/closure schedules and frame hashes; the same seed must replay exactly. The E002-602 public-template attack must fail against the new challenge under at least two fixed *development* seeds, while a programmatic ideal reviewer passes. These are instrument tests, not human competence measurements.
6. Preserve E002-601 class-balanced and nuisance abstention grading. Any unknown geometry/scale or unverified provenance must abstain. The replacement is only a pre-human-study qualification instrument, not an E002-371 physiological/shutter certificate.

Do not infer physical blink sensitivity, human reviewer performance, or independent clock calibration from this work. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
