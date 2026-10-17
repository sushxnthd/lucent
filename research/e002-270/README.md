# E002-270: reference-validity missingness boundary

## Active question
Can ordinary visible-RGB pupil/iris dynamics recover independently synchronized same-eye eye-tracker diameter waveforms without selective reference-observation bias?

- Signal/reference: normalized RGB pupil/iris waveform versus native-time same-eye pupil diameter (mm).
- Frontier: E002-269 uses RGB-only admission but evaluates waveform metrics only where `valid_ref=1`; a high-validity subset can conceal severe error.
- Scalar: full-grid MSE identified interval, plus prospective admitted-window accuracy under frozen correlation (>=0.75), amplitude (0.75–1.25), NRMSE (<=0.70) and lag (<=67 ms) gates.
- Strongest confounds: reference-validity censoring, optical scale drift, brightness and gaze geometry, and clock offset.
- Decisive falsification: identical RGB and underlying reference, different validity masks; a conditional metric changes PASS/FAIL.
- Publishable success: >=8 untouched human participants, independent clock/label provenance, device/lighting/glasses holdouts, independent checker, mechanism-derived prediction and prior-art audit.
- Product relevance: >=75% accurate admitted human windows at >=50% RGB-only coverage, with no silent full-grid certification from missing-reference intervals.
- Kill: three non-discriminating runs or no useful calibrated admission; switch after two blocked dataset paths.

## SCIENCE ledger
Deterministic synthetic five-second/60-fps trials: reference 3+0.24*sin(2*pi*0.6*t) mm; RGB-derived prediction has a 1.6 mm-equivalent artifact over 5%, 10% or 20% of frames. If reference validity hides precisely those frames, conditional correlation is 1 and NRMSE is 0. With full references, correlations are approximately 0.642, 0.590 and 0.266 and NRMSE values 2.108, 2.981 and 4.216. An equal-sized missingness placebo outside the artifact fails. No real-world missingness mechanism is inferred.

**Exact partial-identification law:** for fixed prediction p_i, observed references y_i (i in O) and missing reference y_i independently bounded in [a,b] (i in M), full-grid MSE lies in the sharp interval
`[ (sum_O(p-y)^2 + sum_M distance(p,[a,b])^2)/N, (sum_O(p-y)^2 + sum_M max((p-a)^2,(p-b)^2))/N ]`.
Each endpoint is attained by an admissible choice of missing values. If M is nonempty and no finite reference range is established, the upper bound is infinite. This is established missing-data partial identification, not a new physiological theorem.

## PRODUCT ledger
E002-269 valid-row metrics are **conditional diagnostics**, not evidence of accuracy across all five seconds. Preserve RGB-only admission; report reference coverage, gap placement and full-grid error bounds or abstain. Illustrative [2.5,3.5] mm bounds in the script are NOT calibrated human physiological limits. Product certificate remains disabled.

## Reproduce
`python3 research/e002-270/run.py && python3 research/e002-270/independent_check.py`
Standard library, no GPU/API spend, no user's laptop. Synthetic replay only; no EVE participant bytes, no human waveform or fatigue claim. This is an algebraic replay of the selection vulnerability, not execution of the complete E002-269 scorer.

## Wildcard (about 10%)
An equal-count placebo mask outside the RGB artifact fails, isolating the location of missing reference samples as the cause rather than the percentage alone.
