# E002-419 — frozen partial-identification protocol for unresolved high-speed reference truth

**Frozen 2026-10-24 before implementation.** Sole scientific kernel: E002-371 shutter-gap / eyelid-velocity observability. Evidence tier: finite-set mathematical and synthetic verification, **not** new human anatomical aperture or camera calibration. This study does not reopen the rejected E002-397, E002-412 or E002-417 optical surrogates.

## Question
When ordinary-camera software emits a **no-hidden-closure** certificate but the high-speed reference cannot establish a physical negative (E002-416), what error rate can actually be identified? The observed zero-error rate among *resolved* reference intervals is potentially misleading.

## Frozen classification and law
Input is a complete, predeclared set of ordinary-camera windows, each with a product decision `CERTIFY_NO_HIDDEN_CLOSURE` or `ABSTAIN` and independently adjudicated high-speed reference state `WITNESSED_CLOSURE`, `PHYSICALLY_EXCLUDED_CLOSURE` or `UNRESOLVED`. All reference negatives must meet E002-416 physical-clock/shutter/velocity/geometry requirements; assertions or algorithmic agreement are insufficient. Missing, corrupted or ambiguous reference intervals are `UNRESOLVED`, never silently dropped.

For the N windows on which the product actually issues a certificate, let F have witnessed closure and U have unresolved reference. The *finite-evaluation-set* false-certificate fraction is sharply partially identified by

    F/N <= risk <= (F+U)/N, N>0.

The bounds are attainable by assigning every unresolved reference either no closure or closure. This is **not** a population confidence interval, a new theorem, or a physiological guarantee. For N=0 the selective error is undefined, not zero. Report coverage N/T, witnessed-error count F, unresolved-certified count U, and reference-unresolved count across **all** T windows; never conflate reference abstention with product abstention.

## Prespecified adversarial checks
1. Independently enumerate all binary assignments to unresolved certified reference windows for 1,000 seeded synthetic cases with at most 10 unresolved entries; extrema must equal the proposed sharp bounds.
2. A fixture with 20 certificates, zero witnessed failures and 15 unresolved references must yield [0, 0.75], **not** zero error.
3. All-abstain product, no reference-negative authentication, missing records, duplicated window IDs, unknown states, and malformed evidence must not unlock any product claim.
4. A fixture with 5 witnessed failures and 0 unresolved among 20 certificates must yield exactly 0.25; abstentions must remain in the all-window coverage denominator.
5. The research gate always returns `ABSTAIN_UNCALIBRATED` and `product_claim_authorized=false` until actual independent physical validation and population-risk review exist.

## Scope and prospective human use
Run this contract **only after** two real blinded E002-407/418 raters, E002-408 adjudication and E002-416 physical reference qualification. Report participant-stratified counts; do not infer population risk from frames or use a finite observed maximum as a hard velocity bound. Do not upload human images, raw timestamps, rater sheets or linkage. Reproducible synthetic tests may run in CI. This is a validation-accounting artifact and a product safety gate, not physical E002-371 validation.
