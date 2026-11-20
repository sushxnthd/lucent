# E002-603 | Private-answer synthetic reviewer challenge and source-image custody

Date: 2026-11-02. Parent E002-371. [Frozen protocol](E002_603_FROZEN.md) committed at `b32018e` before implementation. Evidence tier: **SYNTHETIC_INSTRUMENT_REPAIR_ONLY**.

## New executable

[e002_603_private_challenge.py](e002_603_private_challenge.py) replaces the public fixed answer schedule with a secret-seed-dependent permutation of four nuisance and six clean clips and a privately selected set of exactly 11 closed clean frames, at least one per clean clip. The 190 images retain the E002-598 native reviewer packet shape, and the E002-601 class-balanced grader remains unchanged. Per-frame upper-lid position and slope are also seed-dependent. The owner-only manifest stores source-frame SHA-256 and private truth; the grader refuses to run if any source image is missing or altered.

The generator accepts a cryptographically random 256-bit seed by default, and supports an owner-supplied seed for private reproducibility. No human-study seed, source imagery, truth or reviewer exports are committed. Public development seeds in the self-test are **not** valid human qualification seeds.

## Frozen adversarial tests

The self-test checks two *public development seeds*; different private schedules and frame hashes; an ideal synthetic reviewer passing the existing class-balanced gate; the E002-602 public-answer attack being rejected; and tampered-image rejection before grading. The self-test never substitutes generated ideal labels for actual human ratings. These tests verify source custody and removal of the *known* answer-schedule leak, not proof that a human reviewer can annotate a real eyelid.

At report creation, [dedicated hosted CI #41387670731](https://github.com/sushxnthd/lucent/actions/runs/41387670731) was **queued**, so no hosted E002-603 success is claimed. Check the exact run logs before promoting the repair to a verified instrument.

## Human/physical boundary

Even a future independent human pass on this private synthetic challenge would only establish limited competence on a synthetic image family. Actual E002-371 validation still needs two genuinely independent blinded raters on human frames, separately authenticated geometry and scale, synchronized high-speed/ordinary physical cameras, optical shutter and clock calibration, a justified continuous-time velocity envelope, and participant-disjoint held-out predictions. No such evidence was collected in this run. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
