# E002-418 — verified synthetic observer-qualification instrument

**Date:** 2026-10-24. **Frozen protocol:** `E002_418_FROZEN.md`, committed at `5ea848429112f4f75f310bcd1738338e08c9662b` before implementation. **Evidence tier:** synthetic known-geometry instrument verification, not independent human annotation, anatomical aperture, or physical shutter-gap validation.

## Executed results

The standalone generator produced **144 synthetic 190×130 grayscale PNGs**, exactly **16 cases for each of nine nuisance conditions**, in four 36-frame blinded clips. The existing E002-407 manifest/CSV validator accepted the complete pack. All 144 PNG headers, dimensions and SHA-256 digests matched their manifest records in the independent regression. The pack omitted condition labels, geometry truth, participant/event linkage, and the private answer file.

The independent test exercised a two-sheet **synthetic oracle** and three adversarial cases:

| Test | Observed | Decision |
|---|---:|---|
| Oracle on six visible conditions | 96/96 all-six-point correct | PASS |
| Oracle on glare, occlusion, glasses | 48/48 explicit abstentions | PASS |
| Systematically +7-px shifted coordinates | 0/96 visible correct | REJECT |
| Confident coordinates on all obscured cases | 0/48 correct abstentions | REJECT |
| Unresolved flag with hidden coordinate entry | 47/48 correct abstentions, 1 false-confident | Count failure |
| Same rater ID in both sheets | Exception | REJECT |
| Modified public manifest with original private truth | Exception | REJECT |

The challenge has an intentionally high-visibility oracle; **oracle sheets are not actual human ratings**. The masked-coordinate test catches a false abstention that the base E002-407 CSV schema permits syntactically but the new observer qualification must reject. All-frame denominators are retained.

During implementation, the initial fixed pseudorandom challenge seed was identified as a potential answer-leak: a rater with source access could reconstruct the private condition order. The generator was corrected to use OS-backed unpredictable randomness for real challenges; a fixed seed is available only through an internal Python API for regression testing. No private answer files are published or uploaded.

**Hosted independent verification:** [E002-418 CI run 40099253282](https://github.com/sushxnthd/lucent/actions/runs/40099253282) completed **SUCCESS** on commit `c51f1249ec8debc6ff950979e1cf7bfc8cd38b0f`. Its `synthetic-instrument` job passed the new adversarial tests and existing E002-407 regression, with no artifact uploads. The handoff documentation was added afterward without modifying executable code.

## Decision

**Instrument accepted for a prospective synthetic observer-qualification pilot; actual human-rater qualification remains PENDING.** The acceptance thresholds (>=87/96 visible, >=12/16 per visible condition, >=46/48 correct obscured abstentions) are prospective. No human rater has yet taken the challenge, and no independent blinded E002-407 real-human landmark sheets have been completed. A green CI job is not human measurement evidence.

The instrument can detect some operator and annotation-interface failure modes before the expensive real-human study. It cannot establish true anatomical landmark accuracy because the images are synthetic and differ from real eyes; passing raters can still share systematic real-image errors. It is not an independent camera clock, shutter calibration, hard eyelid-velocity bound, or E002-371 validation. E002-417's two automatic image estimators remain rejected. This is a reproducible human-validation **artifact**, not a novel measurement theorem or a validated physiological result.

## Next decisive experiment

An authorized coordinator must locally generate one immutable synthetic pack, obtain two genuinely independent completed human sheets, and score them privately using `E002_418_RATER_HANDOFF.md`. If both pass, the same two raters should independently annotate E002-407's actual high-speed human-eye packs; freeze sheets before E002-408 adjudication. Then calibrate camera exposure/row timing and physical aperture independently, and prospectively score E002-371 on untouched participants/devices. Do not publish raw eye images, linkage, or rater sheets.

**Product consequence:** `ABSTAIN_UNCALIBRATED` remains mandatory for no-hidden-closure certificates, blink duration, PERCLOS and fatigue. The synthetic qualification result does not unlock any physical product measurement. Hush's separate branch and PR #45 were untouched.
