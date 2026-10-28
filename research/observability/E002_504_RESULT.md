# E002-504 | Static-aperture uncertainty consequence (implementation, CI pending)

Date: 2026-10-28. E002-371 primary research branch, draft PR #26. **Product consequence of E002-503, not a new theorem or physiological result.** Frozen protocol: [E002_504_FROZEN.md](E002_504_FROZEN.md). Executable: [e002_504_static_claim_gate.py](e002_504_static_claim_gate.py).

## Falsification addressed

E002-503's hosted-verified synthetic counterexamples showed 260/260 nominal inter-rater agreement despite a common-mode iris-scale bias that put the nominal aperture interval on the wrong side of c=0.10. The frozen E002-492 anatomical adjudicator only returns agreement metrics, not a threshold label. A downstream consumer **must not** turn agreement into a static aperture threshold or physical hidden-closure certificate.

E002-504 adds a separate, fail-closed, dependency-free *research-only* interpreter. It uses an independently supplied **interval** for iris diameter rather than either rater's point estimate; propagates per-landmark uncertainty conservatively; requires both raters' full intervals to be on the same strict side of the threshold; rejects disjoint intervals, nuisance flags, invalid geometry, unverified common-column provenance, and missing external scale. Even a conditionally classified static aperture retains `product=ABSTAIN_UNCALIBRATED`, `release=BLOCKED` and all physical/medical certificates false.

**Important limitation:** The evaluator accepts a provenance assertion but does **not** authenticate the external calibration or reviewer independence. The frozen rater JSON does not contain observed x-coordinates or independent scale calibration. Therefore any successful research-only static decision is conditional on external verification; it cannot be used as a production safety certificate.

## Prespecified synthetic predictions (not human observations)

- Missing independent scale -> `ABSTAIN_MISSING_INDEPENDENT_SCALE`, regardless of perfect reviewer consensus.
- E002-503's constructed 4.2/44 and 3.8/36 px scale-bias cases with external [39,41] px diameter -> `ABSTAIN_THRESHOLD_CROSSED` in both cases.
- Synthetic gap 8 px -> `RESEARCH_STATIC_ABOVE`; gap 1 px -> `RESEARCH_STATIC_BELOW`, always product-blocked.
- Equal-to-threshold, invalid scale, nonfinite values, missing provenance, nuisance, frame mismatch, disjoint raters and geometry errors -> abstain.
- Changing nominal rater iris diameters without changing external reference must not change the decision.

Fifteen self-contained `unittest` test methods encode these frozen cases and are executed by [E002-504 CI](../../.github/workflows/e002-504-static-claim-gate.yml) using Python 3.11. **At this report's creation, hosted CI results have not yet been independently verified. Do not describe the tests as passed until their job conclusion is inspected.**

## External evidence still required

Two independent blinded S01 anatomical reviews, independently authenticated optical camera timebase/shutter, physically justified continuous-time eyelid-speed upper envelopes, participant-disjoint high-rate reference predictions and external reproduction. No new human ratings, videos or physical measurements were obtained here. E002-501 optical alias proxy remains retired; E002-503 remains synthetic. No raw imagery or individual ratings were committed.

**E002-371 physical validation: absent. Human anatomical ratings: 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.**
