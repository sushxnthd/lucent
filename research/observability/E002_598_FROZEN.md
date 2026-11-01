# E002-598 | Frozen offline blinded anatomical annotation instrument

Date: 2026-11-02. Primary E002-371 kernel. This protocol is frozen **before implementing and testing** the new offline reviewer UI. It does not preregister a human outcome.

## Goal and source
Remove the remaining manual JSON-editing barrier between the already verified E002-595 authenticated 95-fps/nominal-30-fps LPW private reviewer packets and genuinely independent anatomical ratings. Reuse E002-595's existing blinded `BLANK_ANATOMICAL_RATINGS.json` templates and PNG files, with **no** new video retrieval or participant-selection changes. Development participant 1 only. No held-out participant access.

## Fixed UI contract
- A single static offline HTML file, no external scripts, styles, fonts, images, network calls, storage APIs, service workers or telemetry. User must explicitly select a reviewer template JSON and local PNG folder; never auto-open local files.
- Match images by the template's blind clip IDs and zero-padded local frame numbers; reject missing, duplicate, ambiguous or malformed images. Do not expose native source index, participant ID, owner mapping or video hash.
- Reviewer must choose a single image-column x, click upper and lower lid margins at that column, and record a nonzero measurement uncertainty in pixels. Export upper_y/lower_y only when valid; record `measurement_x` for geometry audit. Iris diameter remains **null** until independently calibrated, not inferred from a closed or obscured iris.
- Explicit `UNREVIEWED`, `OCCLUSION`, `BLUR`, `GAZE`, `GLASSES`, `GEOMETRY`, `BRIGHTNESS`, `MISSING`, `OTHER` nuisance flags. If uncertain or occluded, abstain instead of forcing lid coordinates.
- Export reviewer-facing JSON compatible with E002-595's `clips` object and E002-576's conservative downstream gate. Never invent anatomical labels, reviewer independence, source provenance or camera calibration.
- No autosave. Export must require an explicit click, and must preserve unreviewed frames rather than silently filling them. Any frame missing independent iris-scale provenance remains downstream `UNCERTAIN` even when lid points are supplied.

## Frozen verification and failure criteria
1. Static no-network/no-persistence source audit; test HTML/JS syntax; simulate synthetic template and image-selection mapping.
2. Verify valid 640x480 PNG geometry, blind clip IDs, exact frame enumeration, rater identity, duplicate and missing frame refusal, malformed JSON refusal, and no source identifiers in export.
3. Verify a reviewer can annotate, flag, clear and export without importing any prior ratings; unreviewed frames must remain explicitly unreviewed.
4. Any failure is a research-instrument failure, not a reason to relax E002-371's physical certification gate.
5. Preserve only code, synthetic fixtures, test outputs and aggregate verification. No real human images, reviewer judgments or source mappings in GitHub.

## Physical and human follow-up
Two genuinely independent blinded raters must complete authorized private packets with ethics/privacy review. Separately calibrate iris scale, geometry, shutter exposure/rolling rows, response, clock uncertainty and continuous-time velocity/acceleration envelope. Freeze gap predictions on participant-disjoint physical holdouts before opening reference labels. Any adjudicated closure inside a predicted excluded gap falsifies the claim or a premise. No LPW point-decimation result is a physical shutter certificate.

## Release
Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`; draft PR #26 remains open and unmerged. Hush branch and PR #45 remain separate.
