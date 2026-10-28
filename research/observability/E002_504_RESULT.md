# E002-504 | Static-aperture uncertainty consequence (hosted verification complete)

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

Sixteen self-contained `unittest` test methods encode these frozen cases and are executed by [E002-504 CI](../../.github/workflows/e002-504-static-claim-gate.yml) using Python 3.11. **Hosted verification completed:** [run 40653099759](https://github.com/sushxnthd/lucent/actions/runs/40653099759), on commit `9e1129e0a45ecf5b8d8d970149cf6348079e0189`, finished `success`. Its `frozen-static-geometry-controls` job completed successfully; `Run 16 frozen synthetic controls` was a successful step. This verifies the corrected implementation in GitHub Actions, not its physical accuracy or an independently calibrated human reference.

## Pre-CI numerical falsification and correction

Before accepting a hosted result, inspection of the constructed 4.2 px threshold-touching case identified a floating-point boundary hazard: ordinary binary arithmetic can make the mathematical lower bound 4.1/41 = 0.10 appear strictly greater than 0.10. This could falsely produce a static ABOVE decision. Commit `759ee2c` replaced threshold-critical numerator and denominator operations with decimal-text arithmetic and added a separate exact-threshold regression test. This is a numerical soundness correction found **before** any E002-504 hosted pass, not a new physiological observation. The frozen scientific expectation was unchanged. CI must verify the corrected commit.

## Hosted pre-correction falsification

[GitHub Actions run 40652911423](https://github.com/sushxnthd/lucent/actions/runs/40652911423) completed **FAILURE** on the original binary-float implementation: 13/15 tests passed; both prespecified E002-503 scale-bias cases failed. The evaluator incorrectly returned `RESEARCH_STATIC_ABOVE` and `RESEARCH_STATIC_BELOW` where `ABSTAIN_THRESHOLD_CROSSED` was required. Job logs establish that the failure was an actual hosted execution, not a hypothetical calculation. Preserve this negative result. The decimal-arithmetic correction in commit `759ee2c` and a 16th threshold-boundary regression are committed; their **corrected hosted result passed** in run 40653099759; this supersedes the pending statement. Do not claim the fix verified until that check succeeds.

## External evidence still required

Two independent blinded S01 anatomical reviews, independently authenticated optical camera timebase/shutter, physically justified continuous-time eyelid-speed upper envelopes, participant-disjoint high-rate reference predictions and external reproduction. No new human ratings, videos or physical measurements were obtained here. E002-501 optical alias proxy remains retired; E002-503 remains synthetic. No raw imagery or individual ratings were committed.

**E002-371 physical validation: absent. Human anatomical ratings: 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.**

## Verified stop and next falsifiable experiment

The frozen software failure and correction have now both been observed in hosted execution. **Stop iterating the E002-504 synthetic gate** absent a new externally observed counterexample. The next eligible evidence must be independent human anatomy on the source-verified E002-502 blinded packet, not another software-only proxy. Predeclare before unblinding: per-frame annotation/abstention counts by nuisance, per-rater and inter-rater agreement, failures to identify a fixed x=160 landmark, and any common-mode iris-reference disagreement. Keep raw imagery, landmarks and rater identities private. S01 is one calibration participant; even perfect S01 feasibility cannot estimate a population speed envelope or establish an acquisition shutter. Physical no-hidden-closure claims remain blocked until independently authenticated timebase/shutter and participant-disjoint reference data exist.

Evidence tier: hosted synthetic software controls only. Human anatomical ratings: 0. Physical validation: absent. `ABSTAIN_UNCALIBRATED`; `BLOCKED`.
