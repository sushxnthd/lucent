# E002-601 | Frozen adversarial qualification falsification

Date: 2026-11-02. Existing Lucent E002-371 kernel, same branch and draft PR #26. This is an instrument validity attack, **not** human evidence or shutter validation. Freeze before modifying the E002-600 grader.

## Hypothesis and attacks

The E002-600 aggregate qualification rule can pass reviewers who supply no informative closed-eye decisions. Reproduce two exact, preselected adversarial reviewer exports on the existing private deterministic synthetic fixture (10 clips x 19 frames, 114 clean frames, 76 nuisance frames, 11 clean closed frames, 103 clean open frames).

1. **Vacuous-interval attack:** annotate all 114 clean frames with exact synthetic margins but declare uncertainty 50 px, which straddles the 20-px closure threshold. Abstain on all nuisance frames. Prediction: original rule qualifies despite zero decisive OPEN or CLOSED calls.
2. **Selective-abstention attack:** use exact 0.5-px margin intervals on all clean open frames but abstain on every clean closed frame and all nuisance frames. Prediction: original rule qualifies despite zero closed-eye decisions.

Report the *actual original grader* outputs before repairing it; never present synthetic labels as human annotations. Preserve the failing original gate in a committed report, not in production logic.

## Locked repair gate

Keep original clean coverage >=80%, measured clean interval coverage >=95%, false CLOSED <=1, false OPEN <=1. Add:
- At least 80% of **all truth-closed clean frames** must receive a decisive, correct CLOSED verdict (at least 9/11 in frozen fixture).
- At least 80% of **all truth-open clean frames** must receive a decisive, correct OPEN verdict (at least 83/103).
- At least 75% of the 76 nuisance frames must be abstained (at least 57/76).
- Report class denominators, correct decisive counts, and ambiguous measured counts, so a nominally high measurement rate cannot hide uninformative intervals.
- Apply the identical gate in the independent Node.js oracle. Preserve strict JSON schema, original uncertainty coverage, and fail-closed behavior. Test ideal, blank, both attacks, two false closures, and schema errors.

The numerical thresholds are **synthetic instrument-qualification choices**, not physiological estimates or claims about human raters. If either adversarial attack qualifies after the repair, fail the experiment. Do not infer E002-371 validity. Product remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`; Hush PR #45 untouched.
