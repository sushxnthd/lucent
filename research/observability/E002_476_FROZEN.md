# E002-476 FROZEN — prevent research-conditional classification from becoming a physical product claim

Date: 2026-10-27. Kernel: E002-371. Branch: `research/observability-human-boundary`. **Frozen before implementation or adversarial execution.**

## Scientific question and prior evidence

E002-475 proved that even a participant-level finite-sample maximum cannot establish a universal anatomical speed bound. E002-456 nevertheless deliberately accepts `ILLUSTRATIVE` and `EXTERNAL_HARD_BOUND_DECLARED` as research *assumptions* and may return `EXCLUDED_CONDITIONALLY`. Its dataset aggregate correctly blocks physical release. The interval-level output, however, currently lacks an explicit product-claim field; a downstream consumer could misread `EXCLUDED_CONDITIONALLY` as an observed absence of closure. This run tests that interface boundary without inventing new human evidence.

## Locked adversarial predictions

1. Reuse the existing E002-456 synthetic interval fixture with two 3-mm endpoints at 0 and 10 ms, 2-mm closure threshold, a 100-mm/s *hypothetical* cap, and an independently declared reference. Both `ILLUSTRATIVE` and `EXTERNAL_HARD_BOUND_DECLARED` will yield the **same research conditional exclusion**; changing a provenance string cannot authenticate a physiological bound.
2. Removing reference rows will not prevent a research-conditional exclusion, because a reference witness is not required for the mathematical *conditional* inequality. The absence of a witness does **not** establish anatomical nonclosure.
3. The interval-level API must explicitly return `physical_release_authorized=false`, `product_claim=ABSTAIN_UNCALIBRATED`, and `external_hard_bound_verified_by_this_program=false` for every path, including invalid schemas, all abstentions, valid conditional exclusions, witnessed counterexamples, and self-declared external caps.
4. The dataset-level output must retain the same blocked product decision and participant-disjoint aggregation. All preexisting E002-456, E002-471 and E002-470 regressions must remain green. No existing conditional mathematics or reference classification may change.
5. A new executable downstream consumer must reject raw `EXCLUDED_CONDITIONALLY` or unverified external provenance as a public physical assertion, and must fail closed for missing, forged, nonboolean, or inconsistent authorization fields. It may display `RESEARCH_CONDITIONAL_ONLY` separately with the stated assumptions.

## Falsification and release rule

Any path returning a physical claim from these declared or empirical inputs is a **product-boundary failure**. Any change to the underlying conditional exclusion arithmetic is a **regression**. Passing tests is only software-interface validation, not physical eyelid validation. Do not interpret a string, source DOI, published sample maximum, CI pass, or user-supplied calibration ID as independent metrological authentication.

## Resource and privacy constraints

No new public-dataset search, no reopening held-out human sequences, no physical acquisitions, no participant data in Git, no change to the established branch or draft PR, and no Hush writes during this urgent primary work. Continue the E002-472 independently timed optical/moving-aperture acquisition handoff as the decisive external gate.
