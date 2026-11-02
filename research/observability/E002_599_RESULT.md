# E002-599 | Cross-column false-closure falsification and native-review adjudication bridge

Date: 2026-11-02. Primary E002-371 workstream. [Initial frozen protocol](E002_599_FROZEN.md) was committed at `1852acc` before implementation; the [slope-error amendment](E002_599_GEOMETRY_ERROR_EXTENSION_FROZEN.md) was separately committed at `f9e9f86` before the corresponding code changes. Evidence tier: **SYNTHETIC_GEOMETRY_COUNTEREXAMPLE_AND_REVIEW_INSTRUMENT_ONLY**.

## New scientific negative result
The prior E002-598 UI recorded a chosen measurement column x but allowed the upper and lower eyelid y coordinates to be clicked at *different* x positions. A synthetically slanted but constant-aperture eye can therefore appear closed when it is open at every column:

- u(x)=100+0.5x, l(x)=130+0.5x. True vertical aperture is exactly 30 px at every x.
- At the chosen x=58, u=129 and l=159. With independent iris diameter 100 px, true normalized aperture is 0.30, strictly above the 0.20 closure threshold.
- Clicking the upper margin at x=58 (y=129) and the lower margin at x=0 (y=130) instead produces a false apparent aperture of 1 px, normalized 0.01, below the closure threshold.
- The previous interface accepted these mismatched x clicks. The updated interface refuses upper/lower clicks more than 1 native pixel from the chosen column. The actual HTML VM regression now includes the synthetic attack and a same-column control.

**Important second-order limitation:** A 1-pixel column gate is not a physical uncertainty bound. Even within that gate, an unbounded eyelid-margin slope can create arbitrarily large vertical error. E002-599 therefore requires a separately calibrated local upper/lower lid slope ceiling S, and inflates each rater's y uncertainty from e to `e + S*abs(x-x_ref)`. Missing S causes per-clip abstention. This rule is conditional on the independently justified slope premise, not proof that such a premise has been obtained.

## Pre-existing instrument incompatibility corrected without corrupting holdout
E002-598 exports `measurement_x` and deliberately leaves `iris_diameter:null`. The E002-576 held-out evaluator instead demands a legacy six-key row containing a numeric iris diameter and exactly 330 participant-disjoint held-out clips. Direct E002-598-to-E002-576 handoff was therefore invalid. This run adds [E002-599 native bridge](e002_599_native_review_bridge.py), a **development-only** ten-clip x nineteen-frame adjudicator that consumes actual E002-598 native export shapes and an owner-private, separately sourced iris-scale/column/slope budget. It never fills in missing iris diameter, promotes development packets to heldout status, or asserts that owner-provided provenance flags have been externally authenticated.

Two rater intervals must overlap and both entirely establish OPEN or CLOSED. Missing frames, nuisance flags, missing calibration/slope, x registration failure, and threshold straddling abstain. The tool counts only positive native-frame index witnesses for the three predeclared E002-595 phase maps. Zero witnesses never excludes hidden closures. These three phases are not the complete continuous-phase family (E002-596).

## Reproduction and evidence status
- [Python adversarial test suite](test_e002_599_native_review_bridge.py): positive index-witness fixture, cross-column false-closure refusal, missing slope/calibration, threshold overlap, cross-rater column mismatch, nuisance abstention, invalid schema, and non-identifying aggregate.
- [Independent Node.js BigInt oracle](e002_599_independent_replay.cjs): independently computes rational aperture intervals, phase witness and slope-inflated uncertainty without importing Python.
- [Actual offline HTML VM regression](e002_598_offline_rater_test.cjs): replays mismatched-column clicks against the updated real UI code, rather than a reimplementation.
- [Dedicated CI workflow](../../.github/workflows/e002_599_geometry_bridge.yml): runs all three checks and verifies no private source images or ratings in the workspace.
- **At report preparation, hosted E002-599 CI results have not been confirmed.** These are committed tests and a mathematical counterexample, not completed independent human review. A passing CI result would validate implementation behavior on synthetic fixtures only.

For private execution, use `python research/observability/e002_599_native_review_bridge.py --rater-a <private-A.json> --rater-b <private-B.json> --calibration <owner-only-calibration.json>`. Never commit those inputs. The owner-only calibration must supply per-clip iris diameter, iris error, registered x, tolerance <=1 pixel, local margin slope bound, and an external reference ID. The tool does not authenticate that reference; outputs remain **conditional development evidence** even when owner assertions are present.

## Direct product consequence
**Reject** any closure classification assembled from upper/lower eyelid points at different columns without a justified geometric error bound. **Abstain** when iris scale, slope, timing, visibility, independent rater provenance, or motion premises are unverified. No real human annotations, physical shutter calibration, independent velocity ceilings or held-out physical predictions were acquired.

Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`; PR #26 draft/unmerged. Hush branch and PR #45 remain separate and untouched.
