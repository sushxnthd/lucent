# E002-503 | Frozen iris-reference uncertainty falsifier

Date: 2026-10-28. Parent E002-371, same primary branch/PR. Freeze **before running the E002-503 synthetic counterexample or modifying the E002-492 adjudicator**. No new human ratings, shutter measurements, or held-out outcomes are claimed.

## Scientific question

E002-492/497 records eyelid gap g, pixel landmark uncertainty e, and an iris diameter d, but does **not** record uncertainty in d. Its aperture interval is [(g-2e)/d,(g+2e)/d] (lower truncated at zero), which assumes d is exact. Can two agreeing reviewers, each using the same biased iris scale, return a high-confidence but incorrect operational threshold label? Agreement is not an accuracy certificate.

## Fixed synthetic adversaries and predictions

Operational threshold c=0.10, native geometry 320x288, true iris diameter D=40 px, measured iris diameter d=44 px (10% positive scale error), true eyelid gap g=4.2 px (true aperture 0.105, ABOVE c), landmark uncertainty e=0.05 px. Both synthetic raters submit the same valid measurements on all 260 positions, with empty nuisance flags. Predict: existing adjudicator reports 260/260 interval agreements, 0 disagreements, 0 abstentions, median interval width 0.2/44, and each nominal interval [4.1/44,4.3/44] lies **entirely BELOW c**. The operational closure label is false against the stipulated synthetic truth.

Reverse adversary: D=40, d=36 (10% negative scale error), g=3.8 (true aperture 0.095, BELOW c), e=0.05. Predict both reviewers agree on nominal interval [3.7/36,3.9/36] entirely ABOVE c, again a false operational label. These are constructed examples, not estimated real-human bias magnitudes.

## Independent uncertainty propagation

If a reference diameter is only known to lie in [d-delta,d+delta] with 0 <= delta < d, the sharp positive-ratio envelope under independently bounded numerator and denominator is [max(0,g-2e)/(d+delta),(g+2e)/(d-delta)]. With delta=4 px, both adversaries must return THRESHOLD_UNRESOLVED (their expanded intervals cross c). A hard closure/open decision is permissible only when the **entire** conservative interval lies on one side of c, under all declared geometric assumptions. No statement about between-frame closure follows.

## Falsifiers and stopping rules

1. If the actual E002-492 adjudicator does not report the prespecified agreement/disagreement counts, the software-level prediction fails; preserve failure without retuning.
2. If the conservative interval fails to contain the stipulated true aperture in either fixture, the uncertainty propagation fails.
3. Test invalid denominator bounds (delta >= d), negative uncertainty, zero diameter, and exact delta=0 consistency; fail closed.
4. Do not infer physiological iris measurement errors from these synthetic cases, and do not claim a new mathematical theorem. Existing S01 review packets remain blinded and unannotated. If real denominator uncertainty is not independently measured, future anatomical threshold labels must abstain regardless of dual-rater agreement.

## Evidence tier and release

Synthetic measurement-system falsification only. Physical E002-371 still unvalidated. Product ABSTAIN_UNCALIBRATED; release BLOCKED. No data, timestamps, or participant identifiers leave the local machine. Hush is separate and must not be touched for this experiment.
