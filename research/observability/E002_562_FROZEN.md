# E002-562 FROZEN | One-sided held-out human marker replay (400 Hz -> 30 Hz)

Frozen 2026-10-31 before implementation. Primary E002-371 human-validation kernel; existing branch `research/observability-human-boundary`, draft PR #26. Evidence tier is **protocol plus synthetic regression until original authorized human records arrive**. Do not reclassify this as human validation.

## Data-source decision
Two retrieval paths have already been evaluated: (1) FaceBase 88-28BJ, original 400-Hz 3D eyelid-margin motion capture, reported controlled-access, with 120-fps companion video; (2) Guttmann-Flury et al. 2025 Synapse 150-fps Phantom video, no authorized native frames in hand. Published PNAS 2025 supplementary MP4 is an edited visualization, not original 400-Hz sensor evidence. No repeated dataset search in this experiment. Original 400-Hz data must be obtained with authorization, and no human images/identifiers may be committed.

Sources: https://doi.org/10.25550/88-28BJ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12358864/ ; https://doi.org/10.1038/s41597-025-04861-9 .

## Locked hypothesis and prediction target
For each participant-disjoint held-out **anatomical positive** (not a generic blink label), compare the positive timestamp to predeclared ordinary-camera 30-Hz blind gaps. A false exclusion witness requires a high-rate positive observation inside a gap that a conditional E002-371 rule marked EXCLUDE **before** inspecting that participant's high-rate positives. Reference-negative samples are censored and cannot establish no hidden closure.

Input is a private canonical JSON file, generated from original raw 3D marker tracks using a separately documented head-stabilized projection and fixed normalization. Each sample has sensor time (seconds), normalized anatomical aperture, and independent reference-positive flag; reference-positive labels are kept in a separate withheld file until predictions are sealed. Any frame timestamp, original-source hash, marker geometry, anatomical transfer, or nuisance certificate missing => abstain. A claim of certification in a JSON flag is not independently authenticated by software.

## Frozen executable tests
1. Deterministic phase sweep of 30-Hz counterfactual instantaneous samples from 400-Hz reference (13 phases, 2.5 ms apart). A selected 400-Hz sample is not an actual 30-Hz exposure. Account for up to 1.25-ms sample-to-target error, plus independently bounded clock uncertainty.
2. Strict participant-disjoint split: SHA256 of `lucent-e002-550-v1|<original-participant-id>`, first four of eight sorted hashes exploratory, remaining four held out. Reject duplicate IDs, non-monotone times, invalid/negative apertures, nonfinite inputs, unknown sample flags, and an absent certificate. Do not compute hard V from finite differences.
3. Conditional sharp Lipschitz lower envelope for ideal instantaneous endpoints: `L=max(0,(a+b-2e-V*(d+2u))/2)` for consistent endpoints, with `d` the separation of the *actual selected sensor timestamps*, `u` covering sensor/clock uncertainty. `EXCLUDE` only if `L>theta` and all independent certificates and nuisance checks hold. An endpoint whose lower error bound is <=theta is unresolved. Do not apply this to boxcar or rolling shutter.
4. Precompute and SHA256-seal predictions **without reading reference-positive labels**; adjudication is a separate command requiring that sealed prediction artifact. If a positive reference sample lies strictly within an EXCLUDE interval and source/clock/geometry provenance is externally confirmed, flag a *candidate contradiction*; never call it a certified physical falsification from syntactic flags.
5. Positive controls: a synthetic Lipschitz triangular closure with a correct hard V must yield zero candidate false exclusions across all phases. Deliberately understated V must be capable of producing a candidate false exclusion (negative calibration control). Missing V, nuisance, incomplete timing or exposure certification must force abstention. A clean all-open high-rate reference must not be promoted into an absence certificate.
6. Reports must contain per-phase EXCLUDE/ABSTAIN counts, positive witness candidates, participant counts and censorship, never human media or raw identifiers. Human evidence remains zero until original records, independent raters and external provenance review are supplied.

## Release and stop
All counterfactuals are ideal point samples. They do **not** validate a real ordinary-camera exposure, continuous-time human velocity ceiling, or 400-Hz negative-reference sensitivity. If data cannot be acquired, retain synthetic regression and the precise human study handoff; do not do further dataset archaeology or claim product readiness. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
