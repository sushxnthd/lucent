# E002-499 | Static-geometry falsification of anatomical review

Date: 2026-10-28. **Synthetic instrument-validity counterexample**, not a human measurement, physical camera calibration, or new observability theorem. The predictions were frozen in `E002_499_FROZEN.md` before implementation.

## What the existing validation instrument could not observe

The E002-497 offline reviewer previously accepted upper/lower landmarks at any horizontal coordinate as long as the two points within that frame had similar x values. Its E002-492 JSON records only upper/lower y, iris diameter and uncertainty, not x. Therefore, independent raters could measure different image columns of the **same static anatomy**, and a single rater could drift horizontally between frames. The adjudicator cannot distinguish geometric column mismatch from true anatomical disagreement. Reopening a saved frame even displayed the points at x=160 irrespective of their originally selected x.

## Frozen counterexample and expected result

On a static synthetic image, define upper lid y=90 and lower lid y=90+12+0.03(x-160)^2. With iris diameter 40 px and landmark uncertainty 0.5 px, the same image gives:

| Image column | Aperture (px) | Normalized uncertainty interval |
| --- | ---: | --- |
| x=160 | 12 | [0.275, 0.325] |
| x=170 | 15 | [0.350, 0.400] |

The intervals do not intersect. Two perfect raters measuring the same image at different columns will be reported as disagreeing. A reviewer switching columns across time will produce an apparent normalized aperture change of **0.075 with zero motion**. This is a geometric counterexample under specified synthetic curvature, not a measured human effect size.

The new executable invokes the **actual E002-492 adjudicator** with the frozen inputs, asserting one false disagreement for x=160 versus x=170 and zero for both at x=160. It does not require or claim real human images. No physiological claim is supported.

## Pre-label protocol amendment

Before any real ratings, the E002-497 offline interface was amended to require native image x=160 (input tolerance ±0.5 native pixel) for **every** upper and lower point, with a visible vertical guide and consistent restoration of saved points. If the anatomy cannot be measured at that image column, the reviewer must explicitly flag POOR_GEOMETRY, GAZE or MISSING_ANATOMY rather than shifting x. This replaces the former arbitrary iris-center-column instruction. The fixed-column pilot may fail for off-center eyes and must be killed if coverage is inadequate; it does not correct perspective, gaze or physical timing. E002-492 output schema and privacy model remain unchanged.

## Evidence and release decision

New exact-fraction/actual-adjudicator tests and independent Node predicate checks were added. Hosted verification status must be checked on the exact final commit before claiming success. **Human anatomical ratings: 0.** **Authenticated camera clock/shutter: 0.** **Held-out physical predictions: 0.** E002-371 remains physically unvalidated. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

Next decisive step: two independent raters on the checksum-verified S01 private packet, with prespecified fixed-column coverage and disagreement rates, then independently authenticated acquisition timing. Do not repeat synthetic geometry refinements in place of these observations. Hush PR #45 untouched.

## Hosted verification (2026-10-28 02:18 UTC)

[GitHub Actions run 40620041876](https://github.com/sushxnthd/lucent/actions/runs/40620041876) completed **successfully** on implementation/workflow commit `1133a0f490d849fcced5c9796c7b5feb32bb5c8b`. The hosted runner passed **8/8 E002-499 frozen geometry and executable Node predicate tests**, **8/8 existing E002-497 interface/security/schema tests**, and executed the actual E002-492 adjudicator counterexample. Its synthetic aggregate reproduced one false inter-rater disagreement for different columns, zero disagreement at the shared column, and spurious normalized aperture drift 0.075 with no physical motion. The post-report exact-head run `40620047516` was still queued at the last check; do not claim that separate run succeeded.

This is a successful hosted *synthetic instrument-falsification test*. It neither measures eyelids on real humans nor authenticates exposure, camera clock or velocity. The fixed-column patch is a conservative pre-label protocol correction; its usability and anatomical coverage on S01 remain untested.
