# E002-747 | Prospective exclusion scorer and denominator guard

Evidence tier: **T1 software validation only; no new physical or human observations**.

This artifact operationalizes E002-744's frozen primary falsifier. The denominator is the number of **adjudicated intervals predicted EXCLUDE**, not all closed intervals, and an UNCERTAIN reference label is never a successful exclusion. Every confirmed CLOSED interval predicted EXCLUDE is a falsifier. The scorer reports condition-specific denominators and the exact one-sided 95% zero-error upper bound when applicable. A result with zero adjudicated exclusions cannot establish safety. No raw participant identifiers are emitted.

Input CSV columns: participant, condition, lower0, lower1, velocity_ceiling, gap_upper, truth; optional interval_id. All lengths and velocity units must be consistent. Values must already be independently calibrated; this script **does not** verify those attestations. The model excludes only if l0+l1>V D with V,D strictly positive; zero timing or velocity is conservatively abstained pending separate handling. The script cannot adjudicate source videos or independently estimate physiological velocity. Product remains ABSTAIN_UNCALIBRATED/BLOCKED.

Execution: `python3 research/observability/e002_747_prospective_scorer.py predictions_and_blinded_labels.csv`. Keep prediction file and code hash frozen before labels are revealed. Never treat these software checks as evidence of a human speed ceiling.
