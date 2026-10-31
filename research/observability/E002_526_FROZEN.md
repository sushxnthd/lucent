# E002-526 FROZEN | Predicate-locked quantitative human falsification

Date: 2026-10-29. Primary E002-371 branch, draft PR #26. Freeze this protocol **before** implementation or running tests. All examples are artificial, not human measurements.

## Question and attack
E002-525 freezes gap membership and EXCLUDE/ABSTAIN decisions but delegates to categorical E002-519, which accepts a CLOSED_WITNESS label without E002-520's numerical transport. It also does not freeze the ordinary-camera closure threshold. Can a qualitative label or a post-hoc threshold change reverse a falsification outcome?

Prespecified two-world test: reference mean upper 0.19, scale upper 1.2, offset 0, threshold 0.20, gap [10,30] ms, reference exposure [12,20] ms, all independent-attestation flags asserted true. E002-519 calls this a falsification on the category alone; E002-520 must classify UNKNOWN because 1.2*0.19=0.228>0.20. Raising the threshold after observing the reference to 0.23 changes E002-520 to a conditional falsification. A new preregistration must bind the threshold, gap identity, participant/session, prediction, timing and evaluator version before review.

## Prospective test protocol
1. Add separate version E002-526-v1, not a silent edit of the old E002-525 lock. Owner-private manifest fields: version, nonce_hex (32 nonzero random bytes as lowercase hex), evaluator (exactly E002-520-v1), gaps. Every gap must contain exactly id, participant, session, prediction, left_end_max_ms, right_start_min_ms, ordinary_closure_threshold. All numeric values must be finite, booleans rejected, threshold strictly between 0 and 1, positive blind gap, unique IDs.
2. SHA-256 domain-separated commitment of private nonce plus canonical manifest. Only digest is to be published in a genuinely pre-label timestamped commit. A self-supplied digest cannot establish timing.
3. Owner-private E002-520-v1 evidence must include exactly the committed gaps, same participant/session/prediction/timing/threshold and a references list. Fail closed on omissions, extra IDs, changed threshold, altered predictions, or mismatched digest; call the existing quantitative E002-520 evaluator, not E002-519.
4. A qualifying transported witness can conditionally falsify EXCLUDE. OPEN_OBSERVED and missing or insufficient calibration remain censored/unknown, never validated absence. Aggregate output only; release remains BLOCKED.
5. Adversarial tests: qualitative-only attack, threshold switch, omitted/extra windows, abstain switch, swapped participant, missing transport, false geometry/clock flags, threshold equality, malformed nonce/digest, duplicate IDs, unqualified references. Independent Node arithmetic must reproduce 0.228 > 0.20 and 0.228 <= 0.23.

## Predeclared success and kill criteria
Success: executable reproduces both attack reversals; a new locked evaluator refuses posthoc threshold/prediction/denominator changes, and E002-520 yields UNKNOWN for the original 0.20 threshold despite categorical CLOSED_WITNESS. If any attack yields a conditional falsification without numeric transport, fail the gate and do not claim a correction.

No claims of independent human raters, optical clock calibration, genuine human data, hard physiological velocity ceiling, or product release. This is software/study-integrity evidence only. No new dataset searches or synthetic seed sweeps.
