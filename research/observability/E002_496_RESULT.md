# E002-496 | Authentic S01 blinded-review packet end-to-end experiment

Date: 2026-10-28. Primary E002-371 human validation. Frozen predictions in E002_496_FROZEN.md before checker implementation. This experiment tests **technical annotation handoff**, not anatomical validity.

## Why this was necessary
E002-495 was found to duplicate E002-421's existing sharp equal-boxcar law; the novelty claim was killed and corrected. Further theorem replay cannot substitute for empirical human validation. E002-492 already specified 20 frozen S01 clips and two blinded raters, but authentic archive extraction of the complete private annotation packet had not been independently checked.

## Implementation
Added a dependency-free checker that independently validates the frozen SHA256 of the owner-only manifest, 20 x 13 PNG filenames and native 320x288 geometry, two UNREVIEWED rater templates, absence of source-index/candidate fields in rater material, no symlinks, and private directory permissions. It outputs **only an aggregate**, never images, image hashes, individual ratings or native source indices.

Ten local synthetic adversarial tests passed: complete packet, missing frame, wrong geometry, source-index leak, candidate-field leak, prepopulated rating, owner-map tamper, root permissions, image-directory permissions and symlink injection. A synthetic fixture initially failed the image-size requirement because a highly compressible all-black PNG was below 100 bytes; the fixture was corrected to a valid nontrivial synthetic PNG **before committing**, without weakening the validator.

The hosted [E002-496 workflow](https://github.com/sushxnthd/lucent/actions/workflows/e002_496_packet_integrity.yml) is configured to checksum-verify authentic S01.zip, run the existing E002-492 native-frame packet builder on an ephemeral runner, run the independent checker, delete the archive/private images and upload only the aggregate JSON. **Actual hosted archive extraction and the 260-image integrity result are pending verification**; do not report success until the run completes.

## Limits and next decisive step
This experiment will only establish whether the frozen 260-image review packet can be produced intact, privately and without leaking the candidate assignment to the rater templates. It will not establish whether the images are anatomically interpretable, whether independent raters agree, whether a blink occurred, or whether the video has an authenticated camera clock. The review packet itself is deliberately **not** uploaded, so two authorized human raters still need local, private access to the original dataset and the frozen E002-492 protocol.

No new human anatomical labels, independently measured physiological velocity, calibrated physical shutter or held-out human E002-371 falsification were obtained in this implementation run. E002-493's authentic motion proxy remains rejected. Product ABSTAIN_UNCALIBRATED; release BLOCKED. Hush PR #45 and existing hourly workflow unchanged.

## Reproduction
- E002_496_FROZEN.md
- e002_496_packet_integrity.py
- test_e002_496_packet_integrity.py
- .github/workflows/e002_496_packet_integrity.yml
- E002_492_FROZEN.md and e002_492_anatomical_review.py (unchanged frozen source)
