# E002-497 | Frozen local-only S01 human annotation execution test

Frozen 2026-10-28 after E002-496 authentic packet integrity succeeded and before E002-497 viewer implementation. This is a **human-validation handoff instrument**, not human physiological validation.

## Problem
E002-496 proved a real, blinded 20×13-frame S01 packet can be built privately, but deleted the packet at runner exit. E002-492 rater JSON templates exist; the older E002-404 and E002-448 browser tools use **different incompatible schemas and frame geometries**. Without a format-compatible offline interface, real independent anatomical review is not operational.

## Prespecified acceptance / kill criteria
1. A single offline HTML file, no external scripts, CSS, network calls or telemetry, accepts the exact E002-492 `RATER_A_TEMPLATE.json` or `RATER_B_TEMPLATE.json` and the 260 local native `clip_XX_frame_YY.png` images. The owner-only mapping must not be loaded, exported or embedded.
2. Validate exact 20 clips × 13 positions, native PNG geometry 320×288, allowed fields, blank `UNREVIEWED` state, no duplicate or missing filenames. Reject malformed/partial image packs before annotation. No fabricated labels or auto-completion.
3. At a single fixed visible iris-center column, two clicks record upper/lower lid y coordinates. Require lower >= upper, same x within a conservative tolerance, a positive iris diameter, and explicit per-landmark uncertainty. If anatomy is uncertain, the rater must select a nuisance flag or leave `UNREVIEWED`. No auto-estimated anatomical landmarks.
4. Preserve each rater's ID (A or B), framewise flags and numerical fields in the exact E002-492 adjudicator JSON schema. Export only a local file; never send data to a server. Raters work in separate sessions, with no cross-rater or candidate mapping disclosure.
5. Independent static checks verify restrictive CSP and no external resource loading. A format-compatible synthetic fixture must pass E002-492's existing `validate_frame` and `adjudicate` functions; malformed inputs must fail closed.
6. **Falsifier:** if either reviewer cannot reliably mark anatomy, or >20% of dual-measurable frames disagree, stop treating the packet as a useful reference. Even successful annotation is not clock, shutter, or physical-velocity calibration.

## Reproduction / evidence
Recreate the checksum-verified packet only on an authorized local computer:
```bash
python research/observability/e002_492_anatomical_review.py packet --archive /private/S01.zip --outdir /private/lucent_s01_packet
python research/observability/e002_496_packet_integrity.py --packet /private/lucent_s01_packet --output /private/packet_integrity.json
```
Open `research/observability/e002_497_offline_rater.html` in a modern browser, select the private PNGs and one rater template, then export a separate private completed JSON for each independent reviewer. Run `e002_492_anatomical_review.py adjudicate` only after both are frozen. Never upload human frames, per-frame annotations, owner mapping or source indices.

## Evidence tier
Synthetic interface tests and technical packet verification do not constitute independent human annotations. Camera timing remains unauthenticated, physical shutter uncalibrated, hidden-closure exclusion unvalidated. Product: `ABSTAIN_UNCALIBRATED`; release: `BLOCKED`.
