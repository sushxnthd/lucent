# E002-436 — frozen dual-rater physical-reference adjudication

**Frozen 2026-10-25 before implementation.** Parent kernel E002-371. This is a **synthetic/instrument validation substitute**, not human evidence or a product certificate.

## Scientific question

Can an ordinary-camera conditional no-hidden-closure prediction be independently falsified or corroborated using *two blinded anatomical raters* and high-rate samples, without silently treating the absence of a witnessed closure as a verified negative? E002-426 seals the prospective prediction ledger, but does not independently adjudicate physical reference samples. E002-427 labels a single high-rate trace and therefore cannot test disagreement between anatomical raters.

## Predeclared inputs and rules

A trial has an interval [a,b], physical threshold theta (mm), monotone reference sensor frame IDs and nominal hardware sample times, independent rater A/B lower/upper physical aperture intervals, per-frame nuisance/visibility flags, maximum allowed reference sampling gap, a nonnegative bound delta on absolute sample-clock error, and a separately attested physical speed limit V (mm/s) or null. Explicit provenance declarations are required for raw sensor timing, anatomical scale/geometry and rater independence; **self-declared booleans cannot authenticate any of them**. Do not upload real participant records or identifiable imagery to CI.

- If physical calibration, sensor timing, or rater independence is not independently documented, return **UNRESOLVED**. No numerical negative may be issued without an independently attested V.
- A *witnessed crossing* requires both raters to have valid, mutually consistent aperture intervals at the same reference frame, both upper limits <= theta, and the complete clock-uncertainty interval of that frame inside [a,b]. A single-rater crossing or contradictory rater intervals remains **UNRESOLVED**.
- For a *negative conditional* label, all relevant samples must be valid and both raters' intervals overlap. At each frame use the intersection interval [max(lower_A,lower_B), min(upper_A,upper_B)]. Do not infer agreement from just two point estimates.
- With |dx/dt| <= V and sample time error <= delta, each sample gives the conservative cone x(t) >= l_i - V(|t-t_i|+delta), where l_i is the lower endpoint of the rater interval intersection. The exact reference lower envelope is min_{t in [a,b]} max_i (l_i - V(|t-t_i|+delta)). Compute it using piecewise-linear intersections; independent dense-time oracles will verify it.
- A negative conditional requires that exact lower envelope **strictly** exceed theta, the sample series bracket [a,b], all relevant intersample gaps <= preregistered max gap, and no missing/occluded/blurred/unreliable samples. Otherwise **UNRESOLVED**.
- Missing, conflicting or unsynchronized reference data never count as verified negatives. A definite dual-rater positive may still be witnessed despite a different invalid frame, but contradictory annotations at the witnessing frame cannot be called positive.
- Every result includes evidence tier, explicit nonauthorization of physical product claims and reasons for abstention. Labels are research-only; E002-426's sealed prediction ledger must be frozen separately before reference disclosure.

## Predictions to falsify

1. Equal, open, high-margin synthetic traces with independently stipulated V will be NEGATIVE_CONDITIONAL, whereas near-threshold traces at the same sample cadence will be UNRESOLVED.
2. Two raters reporting disjoint intervals at a putative closure cannot yield WITNESSED_CROSSING; a valid common closure at a trusted frame can.
3. A continuous Lipschitz valley between two open reference frames can cross theta while sampled aperture remains open; exact reference-envelope adjudication must refuse to call it negative.
4. Larger clock uncertainty cannot increase the computed reference lower envelope. A missing frame or nuisance flag cannot improve a negative label.
5. An independently implemented dense-time Lipschitz-cone oracle agrees with the exact piecewise-linear algorithm within 1e-6 mm for fixed test cases.
6. Missing physical provenance or a non-attested velocity bound blocks negative labels. All synthetic tests retain product=ABSTAIN_UNCALIBRATED.

## Failure criteria and study handoff

Any false negative-conditional label on a constructed admissible Lipschitz trace, any rater-disagreement promotion, or any product authorization is a failed experiment. Reproduce with standard-library Python unittest. Use this adjudicator on the **privately held** blinded A/B reference sheets in the E002-433 handoff, after externally archiving the E002-426 prediction seal. Real hardware clock, anatomical scale, and speed-limit attestations remain unavailable. This is not a substitute for prospective participant-disjoint human data.
