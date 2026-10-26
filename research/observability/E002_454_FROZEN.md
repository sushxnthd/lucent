# E002-454 — frozen participant-cluster inferential falsification

Frozen on 2026-10-26 **before running the new calculation**. This is a secondary inferential analysis of the already checksum-verified E002-453 aggregate, not new human acquisition. Source: Culemann et al. (2026), DOI 10.3758/s13428-026-02984-4; OSF Blinks.csv. The input is the committed `E002_453_HUMAN_AGGREGATE.json`, which records 12 training and 5 held-out participants, 649 held-out blink estimates, and zero exceedances of the training maximum. Do not refit, repartition or claim independent new human evidence.

## Frozen predictions and independent checks

1. Under a *continuous exchangeable participant-level maximum* null, with a participant-disjoint prechosen 12/5 split and no ties, the probability of observing **zero held-out exceedances of the training maximum** is exactly `12/(12+5)`, because this event is equivalent to the largest participant maximum lying in the training set. This is a null benchmark, **not** a p-value for a universal physiological cap.
2. With zero observed participant-level exceedance events in five held-out people, the one-sided exact 95% binomial upper limit for the *participant-level chance of at least one exceedance during a comparable session* is `1 - 0.05**(1/5)`, **only if independent comparable participants are sampled**. Compare it with the tempting but inappropriate blink-iid `1 - 0.05**(1/649)`. The participant result must be larger.
3. Test with a separate combinatorial enumerator (17 possible placements of the global maximum) and with exact binomial-tail inversion. Reject invalid participant/holdout counts, nonzero observed exceedances, nonfinite inputs, and mismatched aggregate structure.
4. This diagnostic may weaken the interpretation of E002-453's apparent 0/649 success but cannot establish a hard cap, infer a physiological population maximum, or validate actual hidden eyelid closures. Physical claim remains `ABSTAIN_UNCALIBRATED`; S21/S22 remain untouched.

## Kill / promotion criteria

If the null probability is >= 0.5 or the participant-level upper confidence limit is >= 0.10, **reject** any description of 0/649 as strong out-of-participant validation of a hard speed limit. Keep only the descriptive within-study nonexceedance. Never promote product claims based on these counts. If assumptions fail, mark the calculation conditional and abstain.

Deliver a standard-library executable, synthetic/adversarial tests, deterministic machine-readable aggregate, and report. Do not rewrite E002-453 or other branches. No Hush writes.
