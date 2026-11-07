# E002-451 — frozen adversarial repeat-blinding challenge (2026-10-26)

**Evidence tier planned:** deterministic image-pair falsification and synthetic offline-pack instrument test; no new human annotations, shutter calibration, or physical E002-371 validation.

## Previously untested failure mode
E002-448 writes exactly the same PNG bytes for every hidden-repeat presentation of a selected frame. A rater with access to the pack can hash all PNGs, recognize duplicate pairs before annotating, and potentially copy landmarks. E002-450 checks per-rater repeat consistency but cannot detect such copying. The existing 12-repeat S19 pack is expected to have 12/12 byte-identical hidden-repeat pairs by construction. This is a falsifiable implementation-level result, **not evidence that any human rater cheated**.

## Frozen tests, before writing the challenger
1. Construct a tiny offline pack using the **actual** E002-448 grayscale PNG encoder, with two asymmetric synthetic frames, one repeated once. The original pack must yield exactly one hash-identical duplicate pair.
2. Create a **new, separate** challenger pack by horizontally mirroring only the repeat presentation. Its repeated PNG must differ byte-for-byte from the original. A deliberately left-right-symmetric frame must fail closed, rather than being claimed blinded.
3. Check the anatomical aperture functional on valid synthetic landmark quadruples under horizontal reflection, with canthi re-labeled left/right in display coordinates: the normalized aperture must be invariant to within 1e-12.
4. Reject unexpected image formats, incomplete masters, missing files, nonunique IDs, output overwrite, and mismatched frame/repeat mapping. Do not emit raw images, participant IDs, frame indices, private master keys or annotation coordinates into public result logs.
5. Preserve the original E002-448 pack untouched. All transformed images and mappings remain in authorized **private local storage**. No claim of cryptographic unlinkability: a determined observer can match a mirrored image by inverse transformation, and human recognition remains possible. This is a nuisance-perturbed repeat-consistency *challenge*, not a certified blind test.
6. On an actual asymmetric S19 pack, if later available in authorized private storage, count byte-identical pairs before/after and independently obtain two blinded human annotation exports; do not inspect S21/S22.

## Expected decision
The prior repeat-consistency check is insufficient evidence of truly blind intra-rater reliability. If this frozen synthetic challenge passes, allow an **additional exploratory** mirror-perturbed rater study; do not retroactively relabel E002-448 data, claim human annotation, or upgrade E002-371 product authorization. Physical no-hidden-closure, blink duration, PERCLOS and fatigue remain `ABSTAIN_UNCALIBRATED`.

**Primary priority after this test:** independently annotated real S19 frames and authenticated sensor exposure/geometry/velocity calibration, then preregistered S21/S22 testing. Avoid further surrogate optimization.
