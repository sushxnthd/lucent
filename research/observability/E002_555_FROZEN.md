# E002-555 FROZEN | Offline blinded anatomical video annotation, not a closure certificate

Frozen 2026-10-31 before executable/tests. Primary E002-371 human-validation kernel, existing `research/observability-human-boundary` and draft PR #26. No authorized high-speed human video has been acquired. This is an acquisition/annotation instrument, not human evidence.

## Missing experimental handoff
E002-548/549 adjudicate structured reference-witness assertions but cannot produce two independent anatomical annotations from native video. The new offline instrument must preserve raw blinded rater decisions, distinguish video presentation time from hardware exposure time, and refuse to certify physiology from pixel landmarks.

## Frozen acceptance tests
1. A single-file offline HTML interface accepts a local eye video, opaque packet ID and anonymous rater ID. Compute SHA-256 of complete video bytes; reject videos over 200 MiB rather than hash a prefix. No network, libraries or video upload. Each sample records opaque sample ID, browser presentation timestamp (**not** acquisition timestamp), two eyelid landmarks, pixel separation, label (`closed`, `open`, `uncertain`) and explicit geometry, blur, brightness, gaze, glasses, occlusion, missingness flags. Never treat pixels as calibrated anatomy.
2. Export raw JSON with schema, source SHA-256, packet and rater IDs. Independent raters must work separately and not see predictions or each other's labels.
3. Independent Python audit accepts two exports and rejects mismatched video/packet, identical rater IDs, duplicate/mismatched samples, timestamp differences, malformed coordinates or labels. Flagged nuisances and disagreement => `CENSORED`; concordant closed => `RATER_CONCORDANT_UNCALIBRATED`; concordant open => `REFERENCE_NEGATIVE_CENSORED`, never proof of absence.
4. Audit outputs aggregates only with `human_physical_validation=false`, `certified_exclusions=0`, `release=BLOCKED`, `external_rater_independence_unverified=true`. Strings cannot authenticate rater independence.
5. Adversarial tests cover source mismatch, same-rater, duplicate sample, timing mismatch, negative-only labels, nuisance flags, disagreements, malformed coordinates, valid closure; none can produce certified witness.

## Kill rules and next empirical gate
No inference about an ordinary-camera excluded gap without externally certified exposure support, shutter response, anatomical transfer, hard kinematic ceiling, and prospectively locked predictions. If native video is unavailable or raters disagree, abstain. Acquire authorized native 150/400-fps eye video or consented participant video; record original hardware timing, have two blinded raters annotate and pass externally authenticated positive candidates to E002-548/549. Keep human media out of GitHub. No additional synthetic shutter/codec tuning.
