# E002-408 — frozen two-rater human annotation adjudication bridge

Date 2026-10-24. Freeze **before implementing and testing** the bridge. The verified E002-407 S01/S19 local-only pilots produced 632 real human frames, but no completed human rater sheets. E002-408 closes the reproducible analysis gap between future full-event blinded sheets and calibrated physical decisions; it must not invent annotations.

## Inputs

1. One immutable E002-407 blinded manifest and two *completed* independent rater CSV sheets for the **same** pack, validated with the E002-407 validator. No private EEG marker/control mapping is read.
2. Optionally, an independent physical-camera calibration document and blinded-frame timing map. The EEG synchronization clock in E002-407 private linkage is **not** accepted as an independent exposure clock. Source and validity-domain evidence require external verification.

## Frozen predictions / acceptance criteria

- H1: Exactly complete, distinct-rater sheets are accepted; missing frames, duplicate keys, unsafe manifest entries, malformed landmarks, identical rater IDs and incompatible clip sets are rejected.
- H2: The rater-agreement report uses **signed vertical eyelid gap at the center**, not diagonal distance. For each frame where both raters supplied usable six-point annotations and no nuisance flags, calculate absolute rater difference of the center vertical gap in **pixels**; preserve all exclusions and report per-clip aggregate agreement, but never infer physical aperture or threshold crossing from pixel differences alone.
- H3: Nuisance flags from **either** rater exclude a frame from agreement calculations; do not interpolate across missing or unresolved frames. Count all frame states, including unratable.
- H4: Without independently evidenced physical-camera exposure times and the complete E002-399/400/401/402/403/405 calibration set, all four clips receive `ABSTAIN_UNCALIBRATED`. No surrogate EEG timestamp may unlock certificates.
- H5: A separate, opt-in external-timing path can call the existing E002-399 reference-certification implementation **only** after verifying exact blinded-frame key coverage, monotone per-clip camera times, strictly positive finite exposure durations, finite clock-error bounds, explicit camera-hardware clock provenance, and complete independent calibration. The tool labels provenance **asserted, not authenticated**.
- H6: Output contains only aggregate counts and agreement quantiles; never emit blinded clip IDs, participant identity, EEG event/control linkage, raw frames, individual landmark coordinates, or source frame indices. No raw rater sheets are committed or uploaded.

## Scope / stop conditions

This is a human-validation **analysis instrument**, not a completed human validation. Synthetic fixture tests can establish parser and gate behavior, not rater accuracy or hard velocity physics. Two independent humans must annotate locally before E002-371 can be evaluated empirically. Hard physical eyelid speed bounds are especially unresolved: finite sample maxima are statistical, not deterministic. Any incomplete calibration must abstain. Keep PR #25 draft, product restricted to `ABSTAIN_UNCALIBRATED`.
