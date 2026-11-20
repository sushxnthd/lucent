# E002-602 | Frozen public-template leakage attack on reviewer qualification

Date: 2026-11-02. Primary E002-371 kernel. Freeze this attack before running it or changing the E002-600 generator/grader. Evidence tier: SYNTHETIC_INSTRUMENT_FALSIFICATION, not human data.

## Precommitted hypothesis

The corrected E002-601 class-balanced gate remains vulnerable to answer-key leakage: the public E002-600 source fixes which clips are nuisance, which frame indices are closed, the open/closed aperture gaps (34 and 4 px), the 100-px iris scale, and the range of upper-lid jitter. A reviewer who never views any generated PNG can reconstruct the answers from the public Python constants.

## Attack

1. Build a genuine 190-frame synthetic challenge with a private seed; keep its truth, images and generated reviewer exports out of GitHub.
2. The attacker must NOT read any PNG or owner-only truth before writing the export. Using only public `PULSES` and `NUISANCE` constants, emit for clips 0-5: upper_y=190, lower_y=194 on public pulse indices and 224 otherwise, measurement_x=320, uncertainty_px=5, flags=[]. For clips 6-9 abstain on all 19 frames using the public blank template.
3. Grade against the genuine private truth using the actual patched E002-600 Python grader, and independently replay with E002-600's Node.js oracle. Predict full class-balanced qualification, 114/114 clean measurements, 114/114 interval coverage, 103/103 decisive OPEN, 11/11 decisive CLOSED, 76/76 nuisance abstentions, no errors.
4. Adversarial negative control: change every clean prediction to OPEN (gap 34) and verify failure on closed truth frames.

The attack is a **synthetic answer-key leak**, not evidence that human raters are unreliable. If successful, the E002-601 gate is insufficient to demonstrate image-reading competence, even though it repairs vacuous and selective-abstention cases.

## Locked consequence

Mark all existing publicly specified E002-600 synthetic challenge scores as **NONBLIND_DEMONSTRATION_ONLY**. Do not qualify human anatomical reviewers based on this challenge. A valid future qualification needs an owner-private, independently randomized **per-frame closure schedule and geometry**, sealed before reviewer distribution, with source-image custody, no rater access to truth or generator seed, and a genuinely independent hidden challenge set. Public code may specify the generator *family* but not the actual answer schedule. Preserve E002-601's balanced decision and nuisance criteria. Do not publish a secret seed, truth or image packet. Do not claim the new private challenge has been human-validated until real raters finish it.

E002-371 physical study and product remain blocked: `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush separate branch/PR untouched.
