# E002-717 — evidence-free replay acceptance falsifier (2026-11-08 UTC)

## Scope
Source-level adversarial negative control against E002-716, not an anatomical or instrument result. The current evaluator returns `status=NO_OBSERVED_FALSIFICATION` whenever `failures=[]`. This includes three distinct non-evidentiary regimes: no held-out trials, no reference-valid held-out trials, and no issued exclusions. None tests the exclusion certificate's false-exclusion risk. The status is literally true but can be misinterpreted downstream as validation.

## Reproduction
Run `python -m unittest research.observability.test_e002_717_empty_evidence` from the repository root. Three tests deliberately expect evidence-free runs not to return the same status as a scored, certified run with zero failures. On the unmodified E002-716 evaluator, all three should FAIL. These are intentionally red safety regressions; they are not claimed to have run in hosted CI. The existing E002-716 self-test only checks `heldout_scored==0` in one invalid-reference case, not the overall status.

## Enforcement consequence
Introduce explicit `INSUFFICIENT_EVIDENCE` for `heldout_total==0`, `heldout_scored==0`, or `heldout_exclusions==0`; reserve `NO_OBSERVED_FALSIFICATION` for at least one independently reference-valid held-out certified exclusion with zero contradictions. Even that status is *not* physiological calibration, population risk validation or product approval. Preserve raw denominators and make downstream release logic reject `INSUFFICIENT_EVIDENCE` and `FALSIFIED`. Separate missing reference labels from certificate abstentions rather than summing them into a misleading denominator. Avoid claiming statistical confidence without participant-level design and sufficient independent sample size.

## Evidence tier and next decisive action
Software counterexample only; zero new optical recordings, independently bounded human eyelid velocities, physical shutter measurements, or blinded human participants. Do not count this as E002-371 empirical validation. The priority remains frozen E002-714 instrument acquisition and participant-disjoint human replay. Lucent product remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
