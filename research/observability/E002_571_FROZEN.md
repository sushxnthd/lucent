# E002-571 FROZEN | Real-browser *measured* anatomical-rater handoff

Frozen 2026-10-31 before E002-571 implementation or execution. Same E002-371 kernel, existing `research/observability-human-boundary` branch and draft PR #26. This is a **synthetic-media operational acceptance test**, not human annotation, physical shutter validation, or a new scientific law.

## Specific gap and non-duplication

E002-557 exercised the E002-497 native-frame rater in Chromium by marking **all 260 frames as POOR_GEOMETRY**. That tests abstention/export, not whether the actual two-landmark measurement path can be completed in a real browser, exported in both independently isolated contexts, and interpreted by the existing E002-492 adjudicator. E002-557's early hosted run also failed on an automation/CSP evaluation error; the current script differs from that failed revision. E002-571 is restricted to this **unexercised measured-input path**. Do not change S01 frozen frame selection, thresholds, provenance, E002-371 theorem, or product gate.

## Frozen challenge

1. Use only generated 320x288 synthetic PNGs, the existing E002-492 canonical blank templates, the unchanged E002-497 offline HTML, and a real headless Chromium browser. Load the same 260 filenames in two separate browser contexts; no human images or annotation exports are uploaded.
2. For clip_00 frame_00, rater A clicks upper/lower y=90/110, rater B y=91/109; both enter iris diameter 48 pixels and per-landmark uncertainty 1 pixel. Conservative normalized intervals must overlap.
3. For clip_00 frame_01, rater A clicks y=90/110 and rater B y=100/110, with the same iris scale and uncertainty. The two conservative intervals must be disjoint. These are **deliberately conflicting synthetic rater actions**, not observed human disagreement.
4. For the other 258 frames, each browser independently marks POOR_GEOMETRY and explicitly abstains. Require an incomplete-export rejection before completion, then both JSON downloads, correct 260-frame coverage, and no external network requests.
5. Run the existing E002-492 adjudicator **without changes**. Exact acceptance: total 260, dual reviewed 260, dual measurable 2, interval disagreement 1, agreement intervals 1, nuisance abstention 258, unreviewed 0, geometry abstention 0, disagreement fraction 0.5, `falsification_disagreement_gt_20pct=true`, `human_reference_validated=false`, `release=BLOCKED`.
6. A browser error, export failure, wrong count, false agreement, silent promotion to physiological evidence, or network request is a **failure**. Preserve negative results; do not relax checks to manufacture a pass. Local success is not hosted success.

## Scope and next external action

Passing would establish only that a synthetic user can complete the **measured** and abstention paths in an actual browser and the exported records reach the unchanged adjudicator. It does not authenticate two different humans, validate any pixel geometry, or show that E002-371 works on physical cameras. The next decisive external step remains two genuine blinded S01 raters under E002-567 and independently calibrated optical shutter/clock acquisition. Do not repeat synthetic shutter theory or automated optical proxy tuning. Human rater pairs 0; authenticated physical captures 0; certified hard continuous-time speed ceilings 0; held-out physical predictions 0. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
