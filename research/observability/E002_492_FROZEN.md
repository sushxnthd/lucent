# E002-492 | Frozen blinded anatomical review packet and interval adjudicator

Frozen 2026-10-28 after inspecting the already-published E002-491 aggregate, **before any anatomical review**. This is the primary E002-371 human-evidence handoff, not a new synthetic theorem.

## Prior observation (not anatomical evidence)
The checksum-verified S01 calibration video was decoded on GitHub Actions run 40563647913: 12,000 native frames, 11,999 pairs, 10,572 nuisance-eligible pairs, 1 localized-motion candidate at native frame index 5356, 1,427 nuisance-confounded pairs, 0 exact duplicates. This is a low-yield **motion proxy**, not a blink classifier; do not reselect thresholds based on this outcome. Original paper's 150 fps, rehost's approximately 500 fps, and AVI 1 fps are inconsistent; **none is an independently authenticated camera clock**.

## Prespecified annotation sample
- Use only S01 (calibration participant). Keep S21-S31 anatomically held out.
- One candidate center = 5356. Generate 19 deterministic control centers using SHA256("E002-492-control-"+integer), sort by digest, take the first 19 indices in [6, 11993] outside +/- 20 frames of 5356 and mutually separated by at least 20 frames. No cherry-picking.
- For each center extract 13 consecutive **native** frames, center +/- 6. Total 260 frame review positions (overlap prohibited). Shuffle 20 clip identifiers using a second fixed SHA256 sort. Do not disclose which clip is the motion candidate to raters.
- Verify S01.zip MD5 fb56109542a13aa7879778833fe4cbaa; reject unsafe ZIP entries, unexpected video member, and decoder failures. Preserve native 320x288 geometry. The review packet is created only on a local, authorized machine; never commit, upload to GitHub, or publish any human frames, crops, or contact sheets.
- Two independent raters, blind to candidate status and each other's results, annotate framewise upper/lower lid landmarks at a fixed visible iris-center column, a reference iris diameter from a clean open frame, pixel uncertainty, and flags for gaze, glasses, blur, lighting, occlusion, missing anatomy and poor geometry. They may abstain. No automated proxy counts as an anatomical reference.

## Prespecified adjudication
- A frame is **measurable** only when both raters supply finite upper/lower coordinates, positive iris diameter and nonnegative uncertainty, no listed nuisance flags, and both landmark orders are physically valid.
- For rater r, aperture interval = [max(0, lower-upper-2*uncertainty)/iris_diameter, (lower-upper+2*uncertainty)/iris_diameter]. If two intervals do not intersect, mark disagreement and abstain; do not average away disagreement. If they intersect, report their intersection as an **annotator-agreement interval**, not an externally validated physical uncertainty bound.
- Report number of review frames, dual-measurable frames, disagreements, abstentions by nuisance, and intervals, plus inter-rater absolute differences. Do not infer duration, velocity, closure between sampled frames, PERCLOS, fatigue or medical status.
- Independently authenticated exposure intervals, camera clock and source geometry are required **before** converting frame indices to time or testing E002-371's physical hidden-closure exclusion on held-out subjects.
- Falsification: if either rater cannot reliably identify anatomy, if >20% of dual-annotated frames disagree, or if the candidate is not anatomically interpretable, do not use the motion screen to choose validation events. Preserve negative findings.

## Security, evidence and product
Keep individual annotations and imagery local pending explicit data-use review. Publish only aggregate counts and code, never frame pixels or identifiable face/eye images. For every possible result: product=ABSTAIN_UNCALIBRATED, release=BLOCKED, physical_hidden_closure_certified=false, acquisition_fps_authenticated=false, human_reference_validated=false. No physical camera acquisition is claimed.
