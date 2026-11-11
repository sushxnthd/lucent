# E002-527 FROZEN | Pre-label transport-calibration selection attack

Date: 2026-10-29. Primary E002-371 human-validation branch; continue draft PR #26. Freeze before implementation or inspecting any new outcome. Evidence tier: synthetic study-integrity falsification, not human/physical measurement.

## New question
E002-526 freezes the ordinary-camera closure predicate, gap membership, and reference evaluator, but the E002-520 reference records still carry owner-supplied `transport_scale_upper` and `transport_offset_upper` that can be changed after the reference aperture is observed. Does changing those calibration bounds reverse the conditional falsification while preserving the E002-526 manifest digest?

## Frozen counterexample
Artificial gap [10,30] ms, threshold 0.20, reference exposure [12,20] ms, reference mean aperture upper 0.19, zero transport offset, all six E002-520 validity flags true only by stipulation. Prelabel scale upper 1.20 yields transported upper 0.228 > 0.20: UNKNOWN. Postlabel replacement with scale upper 1.00 yields 0.190 <= 0.20: conditional FALSIFIED. Both must pass the old E002-526 digest because it does not bind calibration. In the reverse direction, postlabel scale inflation can suppress a previously admissible contradiction. These are *software attacks*, not genuine calibration estimates.

## Prospective E002-527 acceptance
1. New version and domain-separated nonce-protected commitment; preserve historical E002-526 unchanged.
2. Each frozen gap must additionally bind a unique, nonempty `calibration_id`, nonnegative finite `transport_scale_upper` and `transport_offset_upper`, as well as E002-526's gap fields and threshold. Reject missing or duplicate gap IDs, invalid values, malformed manifests and changed denominators.
3. Evidence retains E002-520 shape but must include exactly the frozen calibration ID on each reference and must use exactly the precommitted transport bounds. The ID is removed before delegation to E002-520; no silent fallback to evidence-supplied calibration.
4. Reject postlabel shrinkage **and** inflation of calibration, altered predicate/timing/attribution, or any missing/extra gap. Unknown, open or uncalibrated reference remains UNKNOWN/censored, never evidence of absence. Every output keeps `ABSTAIN_UNCALIBRATED` and `BLOCKED`.
5. Tests must reproduce the old gate's two possible classifications under unchanged digest, show that the new gate rejects both switches, retain conditional classification under legitimate precommitted 1.0 and 1.2 values, and reject false flags, invalid calibration IDs, nonfinite/boolean bounds, missing references and changed gaps. Independent JS arithmetic must reproduce 0.19 vs 0.228.

## Limitations and stop rule
A prelabel digest does not authenticate its own timestamp or that a calibration was physically measured, and it does not establish continuous-time eyelid velocity, human anatomy, or actual camera timing. No real S01 or held-out human labels are to be fabricated. This is the final planned *manifest-selection* correction absent actual human/optical evidence; stop further synthetic preregistration variants and obtain independently blinded S01 reviews and optical calibration.