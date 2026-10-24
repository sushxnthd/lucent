# E002-415 — frozen calibration-provenance spoofing and product-output isolation

**Date:** 2026-10-24. **Evidence tier:** adversarial synthetic instrument / product-interface falsification. No new human annotation, physical camera timing, or independently established velocity bound.

## Hypothesis and setup (frozen before implementation)
E002-408 accepts an operator-supplied `independent_camera_hardware` string and unverified provenance labels. Under synthetic exact calibration, its current machine-readable `decisions` field can contain `CONFIRMED_NO_CROSSING` while `product` remains `ABSTAIN_UNCALIBRATED`. The conditional scientific computation is legitimate **only under the asserted assumptions**; its exposure as an unqualified decision creates a consumer-confusion risk. No self-attested string or Boolean authenticates shutter timing, optical transfer, geometry, or physical speed.

H1: Reusing the existing 120-frame E002-408 synthetic fixture, adversarial operator-supplied camera/calibration metadata yields four conditional `CONFIRMED_NO_CROSSING` results, despite **zero authenticated** physical evidence.

H2: A fail-closed public result contract always exposes `decisions = {ABSTAIN_UNCALIBRATED: clips}` and `product = ABSTAIN_UNCALIBRATED` when the tool has not authenticated physical evidence, even if all asserted gates pass.

H3: Preserve conditional scientific information under a distinctly named `conditional_research_decisions` field, with `conditional_research_only = true` and explicit `physical_calibration_authenticated = false`. The legacy unqualified field must never contain a physical certificate.

H4: Missing/invalid calibration and empirical-sample-max velocity still abstain, and the synthetic oracle's four conditional positives remain reproducible. Earlier E002-407/408/399 checks must remain green.

H5: An independent contract checker fails if any returned top-level `decisions` contain non-abstaining labels while provenance is unauthenticated, and tests deliberate metadata forgery.

## Decision
A falsified product-output boundary must be fixed even if the underlying conditional Lipschitz theorem remains mathematically correct. Never claim this synthetic exploit is an actual deployed clinical failure or a novel scientific theorem. This test does not replace the two missing blinded human sheets or real shutter/velocity calibration. Keep PR #25 draft; do not merge or enable blink duration, PERCLOS, hidden-closure guarantees, or fatigue. No identifiable human images may be uploaded.
