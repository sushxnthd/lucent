# E002-574 | LPW participant-disjoint offline selection implementation freeze

Frozen 2026-11-01 before implementation is committed. Extends [E002-573](E002_573_LPW_HUMAN_REFERENCE_PROTOCOL.md); does not alter its sampling, labels, split or primary E002-371 kernel.

## Precommitted predictions and tests
- On a synthetic inventory with 22 distinct participants, exactly three videos each, and 190/380-frame recordings, the E002-573 participant hash split yields 11 development and 11 held-out participants, 33 held-out videos and 330 nonoverlapping 19-frame blinded windows (ten per video).
- Reordering the input video inventory cannot change the split, selected windows, blinded clip IDs or rater templates.
- The two reviewer templates must contain only blank anatomical fields and opaque clip IDs, with no source participant, video hash, native frame indices, candidate label, or owner mapping.
- Reject unsafe IDs, duplicate video identities or digests, missing videos/participants, invalid frame counts, unexpected schema, symlink inventory and existing output. Write private output outside Git repositories with restricted file permissions.
- Negative control: this planning instrument must never claim that source images were acquired, native timestamps authenticated, eyelid closures annotated, independent raters obtained, or physical shutter calibration completed.

## Input and evidential limits
The script consumes a private, owner-provided JSON inventory with exactly `videos`, each entry containing `participant_id`, `video_id`, `video_sha256`, `native_frame_count`. It does **not** verify that the claimed video hash matches a local file, that frame counts are authentic, that a video belongs to the named participant, or that the original acquisition rate is 95 Hz. Such checks must be performed separately by an authorized source custodian before the plan can be used for human review. It does not download LPW or export frames. The resulting mapping and rater templates stay private.

The implementation is a one-shot **human-validation readiness artifact**, not a new human empirical result. The primary study remains E002-567's synchronized physical-camera experiment. No new synthetic physiology boundary or product claim is permitted. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
