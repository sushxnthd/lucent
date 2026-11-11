# E002-509 | Frozen participant-level falsification and evidence-power gate

Frozen 2026-10-28 before any new human annotation or E002-509 executable. This is the **same E002-371 human-validation kernel**, not a new product, detector, source-video search, or synthetic camera model. Existing branch `research/observability-human-boundary` and draft PR #26. No human data were inspected or obtained.

## Hypothesis to kill

The previously specified `>=8` participant-disjoint holdout in E002-373 is **not statistically capable of establishing a 1% population false-exclusion risk with 95% one-sided confidence**, even if no false exclusions are observed. The experiment here is a pre-data **statistical design falsification**, not a physiological finding. A hard continuous-time guarantee cannot be established from finite human samples at any N.

## Frozen unit, event and assumptions

- One unit is **one previously unseen participant**, not a frame, video, blink or gap. Fix the number and duration of evaluated ordinary-camera windows, device, shutter calibration, nuisance strata and abstention rule before collecting the holdout. A participant is a failure if **any** algorithmically *excluded* hidden closure is contradicted by a valid independently synchronized high-rate anatomical reference in that fixed session, or if a predeclared physical speed envelope is violated. A reference ambiguity is UNKNOWN, not a success.
- A participant with no certifiable windows is **not evidence of usable coverage**. Report number of participants with at least one eligible window, with at least one certificate, with zero certificates, and with unresolved reference labels. The primary population-risk denominator remains all genuinely eligible, fully evaluated participants under the frozen protocol; never select only easy/certified cases after viewing outcomes. A participant with unresolved primary truth cannot be counted as a clean success.
- For the **zero-failure** case only, with `n` independent identically distributed, fully adjudicated participant-level Bernoulli outcomes under a fixed evaluation protocol, the exact one-sided 95% Clopper-Pearson upper confidence bound is `p_U = 1 - 0.05^(1/n)`. This is the probability of **at least one false exclusion during the fixed evaluation session** for a new exchangeable participant, not the risk per frame, a guarantee for each nuisance subgroup, a universal physical speed limit, or a deterministic no-closure certificate.
- Predeclared design target: upper bound `p_U <= 0.01` (1% participant-session failure risk at 95% confidence), with **zero observed participant failures**. Minimal `n = ceil(log(0.05)/log(0.99)) = 299`. Any observed failure requires a separately preregistered nonzero-count exact interval and must not be silently treated as zero. Do not extrapolate an all-abstain model into a useful product: coverage must be independently quantified, and release remains blocked without a separately specified minimum-utility gate.
- If participants, devices, sessions or conditions are dependent or distribution-shifted, this bound is not a valid deployment guarantee. Do not treat repeated gaps or multiple sessions from the same person as independent participants. Report condition-stratified failures and coverage; no subgroup guarantee without its own powered study.
- Stop/kill: if `n=8` and zero failures, upper bound is approximately `31.2344%`, not 1%. If `n=24`, approximately `11.7346%`. Even `n=80` with zero failures is insufficient. A zero-event result at `n=299` would pass **only this statistical risk gate** if all assumptions hold; it does not validate the hard E002-371 velocity premise.

## Preregistered executable controls

Compute upper bounds for `n=8,24,80,298,299,300`; verify minimal sample count by both neighboring values; reject `n<=0`, invalid confidence or target; reject any nonzero failures in the zero-event-only routine; reject uncertified, missing, ambiguous or repeated participant IDs; reject all-abstain coverage as a product-success claim. Independently verify the 8/299 numerical results using a second language. This executable will operate on synthetic **counts only**; no fabricated human ratings or physical measurements.

## Next external evidence and product consequence

Proceed with the unchanged private E002-502 two-rater S01 pilot, authenticated exposure/clock measurement and prospective participant-disjoint high-rate recordings. E002-509 does not replace those steps or change frozen sampling. Treat an 8-person pilot as **feasibility and counterexample discovery**, not a high-confidence population safety certificate. Use no participant-level risk guarantee or fatigue/closure safety claim in Lucent until independent human evidence, calibration, powered holdout, and external replication exist. `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

Literature context only: Lee, Seo & Hwang (2025), 80-volunteer 240-fps eyelid-trajectory study, DOI https://doi.org/10.1007/s13534-025-00522-3. Its 80 volunteers were **not** evaluated for Lucent false exclusions; no outcomes are borrowed or inferred.
